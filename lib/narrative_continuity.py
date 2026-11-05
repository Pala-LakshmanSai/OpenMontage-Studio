"""Reviewed screenplay evidence integrity. Does not certify audiovisual meaning."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path


class NarrativeContinuityError(ValueError):
    pass


def _require(condition, message):
    if not condition:
        raise NarrativeContinuityError(f"Narrative contract: {message}")


def _text(value):
    return isinstance(value, str) and bool(value.strip())


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def cuts_digest(cuts):
    return hashlib.sha256(json.dumps(cuts, sort_keys=True, separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def validate_foundation(project: Path, script: dict) -> dict:
    """Require a reviewed whole screenplay before media, using existing metadata."""
    f = script.get("metadata", {}).get("narrative_foundation", {})
    _require(isinstance(f, dict) and f.get("status") == "reviewed", "review the whole screenplay before media generation")
    _require(f.get("source_read_through_ending") is True, "read the source/story through its ending")
    for key in ("protected_core", "adaptation_decisions"):
        _require(isinstance(f.get(key), list) and f[key] and all(_text(x) for x in f[key]), f"record {key}")
    _require(f.get("unresolved_gaps") == [], "resolve structural gaps before media generation")
    screenplay = f.get("screenplay_path")
    _require(_text(screenplay), "record the revised whole screenplay path")
    path = Path(screenplay)
    path = path if path.is_absolute() else project / path
    _require(path.is_file() and path.stat().st_size > 0, "revised screenplay file is missing or empty")
    _require(hashlib.sha256(path.read_bytes()).hexdigest() == f.get("screenplay_sha256"), "screenplay changed; refresh the foundation review")
    sequences = f.get("sequences")
    _require(isinstance(sequences, list) and sequences, "record all dramatic sequences through the ending")
    ids, beats = set(), set()
    for s in sequences:
        _require(isinstance(s, dict) and _text(s.get("id")), "sequence needs an id")
        _require(s["id"] not in ids, "duplicate sequence id")
        ids.add(s["id"])
        for key in ("purpose", "action_and_transition", "emotional_turn"):
            _require(_text(s.get(key)), f"sequence {s['id']} needs {key}")
        _require(_number(s.get("performance_seconds")) and s["performance_seconds"] > 0, "budget performed scene time")
        required = s.get("required_beats")
        _require(isinstance(required, list) and required, "sequence needs its required causal/emotional beats")
        for beat in required:
            _require(isinstance(beat, dict) and _text(beat.get("id")) and _text(beat.get("description")), "beat needs id and meaning")
            _require(beat["id"] not in beats, "duplicate required beat id")
            beats.add(beat["id"])
    _require(f.get("ending_sequence_id") == sequences[-1]["id"], "identify the final ending/epilogue sequence")
    return f


def validate_coverage(project: Path, script: dict, edit: dict):
    """Reject stale/missing observations and unselected witnesses; no pixel inference."""
    foundation = validate_foundation(project, script)
    coverage = edit.get("metadata", {}).get("narrative_coverage", {})
    _require(isinstance(coverage, dict), "record observed narrative coverage")
    _require(coverage.get("screenplay_sha256") == foundation["screenplay_sha256"], "coverage belongs to another screenplay")
    cuts = edit.get("cuts", [])
    _require(coverage.get("cuts_sha256") == cuts_digest(cuts), "cuts changed; reconcile narrative coverage")
    _require(coverage.get("unresolved_gaps") == [], "known critical continuity gaps remain")
    cut_map = {c["id"]: c for c in cuts}
    _require(len(cut_map) == len(cuts), "duplicate cut id")
    required = {b["id"] for s in foundation["sequences"] for b in s["required_beats"]}
    observations = coverage.get("observations", [])
    _require(isinstance(observations, list), "observations must be a list")
    covered = set()
    for o in observations:
        _require(isinstance(o, dict) and o.get("beat_id") in required, "unknown observed beat")
        _require(o.get("mode") in {"visible_action", "legible_ellipsis"} and _text(o.get("observed")), "describe the observed action or ellipsis cue/result")
        cut = cut_map.get(o.get("cut_id"))
        _require(cut is not None, "witness is not in the selected edit")
        a, b = o.get("source_start_seconds"), o.get("source_end_seconds")
        _require(_number(a) and _number(b) and cut["in_seconds"] <= a < b <= cut["out_seconds"], "observation lies outside selected source range")
        covered.add(o["beat_id"])
    _require(covered == required, "missing observed required beats: " + ", ".join(sorted(required - covered)))
