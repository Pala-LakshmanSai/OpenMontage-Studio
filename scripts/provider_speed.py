"""Record observed provider-pass speed without submitting or polling jobs."""
from __future__ import annotations
import argparse
import json
import os
from filelock import FileLock
from pathlib import Path
from datetime import datetime, timezone
from statistics import median

DEFAULT_LEDGER = Path(__file__).resolve().parents[1] / "projects/_shared/provider-speed/events.jsonl"
EVENTS = {"pass_observed", "admitted", "queued", "render_started", "completed", "failed", "cancelled", "allowance_observed", "progress_observed"}
FIELDS = {"event_id", "event", "provider", "workspace", "pass_id", "project_id", "job_id", "model", "route", "resolution", "duration_seconds", "output_duration_seconds", "pass_duration_seconds", "aspect_ratio", "generate_audio", "observed_at", "occurred_at", "allowance_state", "credit_free", "countdown_seconds", "elapsed_seconds", "progress_percent", "pass_started_at", "pass_expires_at", "history_complete", "evidence", "note"}

def stamp(value):
    result = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if result.tzinfo is None:
        raise ValueError("Timestamps must include a timezone")
    return result.astimezone(timezone.utc)

def validate(event):
    extra = set(event) - FIELDS
    if extra:
        raise ValueError(f"Unsupported fields: {sorted(extra)}; never record credentials or personal data")
    for key in ("event_id", "event", "provider", "workspace", "pass_id", "observed_at"):
        if not event.get(key):
            raise ValueError(f"Missing {key}")
    if event["event"] not in EVENTS:
        raise ValueError("Unknown event")
    if event.get("allowance_state", "unknown") not in {"fast", "relaxed", "unknown"}:
        raise ValueError("allowance_state must be fast, relaxed or unknown")
    if event["event"] not in {"pass_observed", "allowance_observed"} and not event.get("job_id"):
        raise ValueError("Job events need an exact provider ID or a clearly labeled local accepted-card ID")
    for key in ("observed_at", "occurred_at", "pass_started_at", "pass_expires_at"):
        if event.get(key): stamp(event[key])
    if event.get("occurred_at") and stamp(event["occurred_at"]) > stamp(event["observed_at"]):
        raise ValueError("occurred_at cannot be after observed_at")
    for key in ("duration_seconds", "output_duration_seconds", "pass_duration_seconds", "countdown_seconds", "elapsed_seconds", "progress_percent"):
        if key in event and (isinstance(event[key], bool) or not isinstance(event[key], (int, float)) or event[key] < 0):
            raise ValueError(f"Invalid {key}")
    if event.get("progress_percent", 0) > 100: raise ValueError("progress_percent cannot exceed 100")
    for key in ("credit_free", "history_complete", "generate_audio"):
        if key in event and not isinstance(event[key], bool): raise ValueError(f"Invalid {key}")
    for value in event.values():
        if isinstance(value, str) and any(word in value.lower() for word in ("bearer ", "https://", "http://", "api_key", "access_token", "authorization:")):
            raise ValueError("No credentials, authorization strings or URLs in the speed ledger")
    if "evidence" in event and (Path(event["evidence"]).is_absolute() or ".." in Path(event["evidence"]).parts):
        raise ValueError("Evidence must be a portable relative file pointer")
    return event

def record(path, event):
    validate(event)
    path.parent.mkdir(parents=True, exist_ok=True)
    with FileLock(str(path) + ".lock", mode=0o600):
        fd = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
        with os.fdopen(fd, "r+", encoding="utf-8") as handle:
            rows = [json.loads(line) for line in handle if line.strip()]
            old = next((row for row in rows if row["event_id"] == event["event_id"]), None)
            if old is not None:
                if old != event: raise ValueError("Conflicting event_id; preserve the original and record a new correction event")
                return {"recorded": False, "duplicate": True, "event_id": event["event_id"]}
            handle.seek(0, os.SEEK_END)
            handle.write(json.dumps(event, sort_keys=True) + "\n")
            handle.flush()
            os.fsync(handle.fileno())
    return {"recorded": True, "event_id": event["event_id"]}

def report(rows):
    cohorts = {}
    for event in rows:
        key = (event["provider"], event["workspace"], event["pass_id"])
        cohorts.setdefault(key, []).append(event)
    output = []
    for key, events in cohorts.items():
        events.sort(key=lambda e: stamp(e["observed_at"]))
        jobs = {}
        for event in events:
            if event.get("job_id"): jobs.setdefault(event["job_id"], []).append(event)
        results = []
        for job_id, history in jobs.items():
            states = {}
            for event in history:
                if event["event"] in {"admitted", "render_started", "completed", "failed", "cancelled"}: states.setdefault(event["event"], event)
            result = {"job_id": job_id, "project_id": history[0].get("project_id"), "model": history[0].get("model"), "duration_seconds": next((e["duration_seconds"] for e in history if "duration_seconds" in e), None), "allowance_state": next((e["allowance_state"] for e in history if e.get("allowance_state") in {"fast", "relaxed"}), "unknown"), "credit_free": next((e["credit_free"] for e in history if "credit_free" in e), None)}
            for field in ("resolution", "route", "aspect_ratio", "generate_audio", "output_duration_seconds"):
                result[field] = next((e[field] for e in history if field in e), None)
            for label, start, end in (("queue", "admitted", "render_started"), ("render", "render_started", "completed"), ("total", "admitted", "completed")):
                if start in states and end in states:
                    a, b = states[start], states[end]
                    basis = "provider_times" if a.get("occurred_at") and b.get("occurred_at") else "observation_times"
                    # Never mix one provider timestamp with one polling timestamp.
                    field = "occurred_at" if basis == "provider_times" else "observed_at"
                    value = (stamp(b[field]) - stamp(a[field])).total_seconds()
                    if value < 0: raise ValueError(f"Negative {label} interval for {job_id}")
                    result[label + "_seconds"] = value
                    result[label + "_basis"] = basis
            result["state"] = next((s for s in ("completed", "failed", "cancelled", "render_started", "admitted") if s in states), "partially_observed")
            result["latest_progress"] = next(({k: e[k] for k in ("observed_at", "countdown_seconds", "elapsed_seconds", "progress_percent") if k in e} for e in reversed(history) if e["event"] == "progress_observed"), None)
            result["partial_observation"] = "admitted" not in states
            results.append(result)
        relaxed = next((e for e in events if e.get("allowance_state") == "relaxed"), None)
        before_by_job = {}
        for e in events:
            if e["event"] == "admitted" and relaxed and stamp(e["observed_at"]) < stamp(relaxed["observed_at"]): before_by_job.setdefault(e["job_id"], e)
        before = list(before_by_job.values())
        comparisons = {}
        for job in results:
            if job.get("credit_free") is not True or job.get("allowance_state") == "unknown" or "total_seconds" not in job: continue
            setting = (job.get("model"), job.get("resolution"), job.get("duration_seconds"), job.get("route"), job.get("aspect_ratio"), job.get("generate_audio"), job.get("total_basis"))
            comparisons.setdefault(setting, {"fast": [], "relaxed": []})[job["allowance_state"]].append(job["total_seconds"])
        comparison_rows = []
        for setting, groups in comparisons.items():
            item = {"settings": list(setting), "counts": {k: len(v) for k, v in groups.items()}, "median_total_seconds": {k: median(v) if v else None for k, v in groups.items()}}
            fast, slow = item["median_total_seconds"]["fast"], item["median_total_seconds"]["relaxed"]
            item["relaxed_to_fast_ratio"] = slow / fast if fast and slow is not None else None
            comparison_rows.append(item)
        output.append({"provider": key[0], "workspace": key[1], "pass_id": key[2], "observed_job_count": len(results), "admitted_count": len({e["job_id"] for e in events if e["event"] == "admitted"}), "completed_count": sum(j["state"] == "completed" for j in results), "completed_nominal_seconds": sum(j["duration_seconds"] or 0 for j in results if j["state"] == "completed"), "measured_completed_output_seconds": sum(j.get("output_duration_seconds") or 0 for j in results if j["state"] == "completed"), "completed_jobs_with_measured_duration": sum(j.get("output_duration_seconds") is not None for j in results if j["state"] == "completed"), "first_relaxed_observed_at": relaxed["observed_at"] if relaxed else None, "admissions_observed_before_first_relaxed": len(before) if relaxed else None, "requested_seconds_observed_before_first_relaxed": sum(e.get("duration_seconds", 0) for e in before) if relaxed else None, "complete_pass_history_verified": any(e.get("history_complete") is True for e in events), "exact_fast_allowance_quota": None, "quota_caveat": "Observed transition counts are not an exact fixed allowance: earlier history, clip settings, replenishment and queue contention can differ. Slow clips alone do not prove allowance exhaustion.", "jobs": results, "comparisons": comparison_rows})
    return {"cohorts": output, "provider_calls": 0}

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=Path(os.environ.get("OPENMONTAGE_PROVIDER_SPEED_LEDGER", DEFAULT_LEDGER)))
    sub = parser.add_subparsers(dest="command", required=True)
    rec = sub.add_parser("record")
    rec.add_argument("--json-file", type=Path, required=True)
    sub.add_parser("report")
    args = parser.parse_args()
    if args.command == "record":
        result = record(args.ledger, json.loads(args.json_file.read_text()))
    else:
        result = report([json.loads(line) for line in args.ledger.read_text().splitlines() if line.strip()] if args.ledger.exists() else [])
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
