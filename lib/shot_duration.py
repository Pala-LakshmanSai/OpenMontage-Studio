"""Local hard-cut candidates for the owner's two-second ordinary-shot floor.

Scene differences are a heuristic, not semantic proof of a cut. Unresolved short
intervals stop a new final checkpoint; this module never edits picture or sound.
"""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import re
import subprocess
import tempfile
from typing import Any

MIN_SHOT_SECONDS = 2.0
SCENE_THRESHOLD = 0.10
VIDEO_SUFFIXES = {".mp4", ".mov", ".mkv", ".webm", ".avi", ".m4v", ".mpeg", ".mpg"}


class ShotDurationError(ValueError):
    pass


def _run(command: list[str]) -> subprocess.CompletedProcess[str]:
    try:
        return subprocess.run(command, text=True, capture_output=True, check=True, timeout=1800)
    except (OSError, subprocess.SubprocessError) as exc:
        # FFmpeg stderr can contain metadata; don't echo it into chat/error logs.
        raise ShotDurationError(f"Local shot-duration scan failed ({type(exc).__name__}); no pass recorded") from exc


def _number(value: Any) -> float:
    try:
        number = float(value)
    except (TypeError, ValueError) as exc:
        raise ShotDurationError("Shot-duration times must be finite numbers") from exc
    if not math.isfinite(number):
        raise ShotDurationError("Shot-duration times must be finite numbers")
    return number


def scan_shots(video_path: str | Path, *, cache_dir: str | Path | None = None,
               minimum_seconds: float = MIN_SHOT_SECONDS,
               scene_threshold: float = SCENE_THRESHOLD) -> dict[str, Any]:
    """Scan every actual frame; do not suppress neighboring cut candidates."""
    path = Path(video_path).resolve()
    minimum, threshold = _number(minimum_seconds), _number(scene_threshold)
    if minimum <= 0 or not 0 < threshold < 1:
        raise ShotDurationError("Invalid minimum shot duration or scene threshold")
    if not path.is_file():
        raise ShotDurationError(f"Final video missing for shot-duration scan: {path.name}")
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    identity = {"version": 1, "source_sha256": digest.hexdigest(),
                "minimum_seconds": minimum, "scene_threshold": threshold}
    key = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
    cache = Path(cache_dir) / f"{key}.json" if cache_dir is not None else None
    if cache and cache.is_file():
        try:
            saved = json.loads(cache.read_text())
            if saved.get("identity") == identity and saved.get("scan_completed") is True:
                return saved
        except (OSError, ValueError):
            pass
    try:
        info = json.loads(_run(["ffprobe", "-v", "error", "-select_streams", "v:0",
            "-show_entries", "stream=duration:format=duration", "-of", "json", str(path)]).stdout)
        streams = info.get("streams", [])
        if not streams:
            raise ShotDurationError("Final output has no video stream")
        raw_duration = streams[0].get("duration")
        if raw_duration in (None, "N/A"):
            raw_duration = info.get("format", {}).get("duration")
        duration = _number(raw_duration)
        if duration <= 0:
            raise ShotDurationError("Final output has no positive video duration")
    except (ValueError, KeyError, TypeError) as exc:
        if isinstance(exc, ShotDurationError):
            raise
        raise ShotDurationError("Cannot determine final video duration; no pass recorded") from exc
    result = _run(["ffmpeg", "-hide_banner", "-nostdin", "-i", str(path), "-map", "0:v:0",
        "-vf", f"select='gt(scene,{threshold})',showinfo", "-an", "-f", "null", "-"])
    cuts = sorted(set(float(x) for x in re.findall(r"pts_time:([0-9.eE+-]+)", result.stderr)))
    boundaries = [0.0] + [x for x in cuts if 0 < x < duration] + [duration]
    short = [{"start_seconds": start, "end_seconds": end, "duration_seconds": end - start}
             for start, end in zip(boundaries, boundaries[1:]) if end - start < minimum - 1e-6]
    report = {"identity": identity, "scan_completed": True, "duration_seconds": duration,
              "boundaries_seconds": boundaries, "short_intervals": short,
              "method": "FFmpeg frame scene difference; candidates require local disposition, not paid review"}
    if cache:
        cache.parent.mkdir(parents=True, exist_ok=True)
        with tempfile.NamedTemporaryFile("w", dir=cache.parent, delete=False) as handle:
            json.dump(report, handle, sort_keys=True)
            temporary = Path(handle.name)
        temporary.replace(cache)
    return report


def validate_video_shots(video_path: str | Path, *, cache_dir: str | Path | None = None,
                         metadata: dict[str, Any] | None = None) -> dict[str, Any]:
    """Apply only explicit owner exceptions and documented false-cut dispositions."""
    metadata = metadata or {}
    report = scan_shots(video_path, cache_dir=cache_dir)
    exceptions = metadata.get("short_shot_exceptions", [])
    dispositions = metadata.get("shot_boundary_dispositions", [])
    if not isinstance(exceptions, list) or not isinstance(dispositions, list):
        raise ShotDurationError("Shot exceptions/dispositions must be lists")
    ignored = set()
    for row in dispositions:
        if (not isinstance(row, dict) or not isinstance(row.get("reason"), str)
                or not row["reason"].strip() or not isinstance(row.get("evidence"), str)
                or not row["evidence"].strip()):
            raise ShotDurationError("A false-cut disposition needs at_seconds, reason and evidence")
        at = _number(row.get("at_seconds"))
        matches = [x for x in report["boundaries_seconds"][1:-1] if abs(x - at) < 1e-5]
        if not matches:
            raise ShotDurationError("False-cut disposition does not match a detected boundary")
        ignored.add(matches[0])
    allowed = []
    for row in exceptions:
        if (not isinstance(row, dict) or not isinstance(row.get("owner_instruction"), str)
                or not row["owner_instruction"].strip()):
            raise ShotDurationError("A short-shot exception requires the explicit owner_instruction")
        begin, end = _number(row.get("start_seconds")), _number(row.get("end_seconds"))
        if begin < 0 or end <= begin:
            raise ShotDurationError("Invalid short-shot exception interval")
        allowed.append((begin, end))
    boundaries = [x for x in report["boundaries_seconds"] if x not in ignored]
    unresolved = [{"start_seconds": start, "end_seconds": end, "duration_seconds": end - start}
                  for start, end in zip(boundaries, boundaries[1:])
                  if end - start < MIN_SHOT_SECONDS - 1e-6
                  and not any(begin <= start + 1e-6 and stop >= end - 1e-6 for begin, stop in allowed)]
    if unresolved:
        times = ", ".join(f"{x['start_seconds']:.3f}–{x['end_seconds']:.3f}s" for x in unresolved[:12])
        raise ShotDurationError(
            f"SHORT SHOT: {Path(video_path).name}: {times}; ordinary shots must be at least 2s. "
            "Use actual source cut boundaries and preserve complete speech. Only explicit owner requests "
            "permit metadata.short_shot_exceptions (start_seconds, end_seconds, owner_instruction). "
            "For a detector false positive, record metadata.shot_boundary_dispositions "
            "(at_seconds, reason, evidence) after inspecting that flagged range.")
    return {**report, "resolved_boundaries_seconds": boundaries, "unresolved_short_intervals": []}


def validate_render_shots(project: str | Path, render_report: dict[str, Any], *,
                          metadata: dict[str, Any] | None = None) -> list[dict[str, Any]]:
    project = Path(project)
    reports = []
    combined = {**render_report.get("metadata", {}), **(metadata or {})}
    for output in render_report.get("outputs", []):
        path = Path(output.get("path", ""))
        if (path.suffix.lower() not in VIDEO_SUFFIXES
                and "." + str(output.get("format", "")).lower() not in VIDEO_SUFFIXES):
            continue
        if not path.is_absolute():
            path = project / path
        reports.append(validate_video_shots(path, cache_dir=project / "artifacts/shot-duration-cache",
                                            metadata=combined))
    return reports


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("video")
    parser.add_argument("--cache-dir")
    args = parser.parse_args()
    result = scan_shots(args.video, cache_dir=args.cache_dir)
    print(json.dumps({"duration_seconds": result["duration_seconds"],
                      "short_intervals": result["short_intervals"],
                      "boundaries_seconds": result["boundaries_seconds"]}, indent=2))
    raise SystemExit(1 if result["short_intervals"] else 0)
