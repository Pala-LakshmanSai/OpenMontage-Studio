"""Validate recorded editorial evidence, not semantic relevance itself.

The agent inspects footage and judges meaning. This module prevents missing,
stale, generic, or repetitive selections from being checkpointed as accepted.
It performs no search, ranking, vision inference, or automatic editorial review.
"""

from __future__ import annotations

import hashlib
import json
import math
from collections import Counter
from pathlib import Path

from schemas.artifacts import validate_artifact


class FootageAlignmentError(ValueError):
    pass


def alignment_digest(value: object) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode()
    ).hexdigest()


def requires_footage_alignment(brief: dict) -> bool:
    metadata = brief.get("metadata", {})
    return metadata.get("anchor_medium") == "broll_footage" or metadata.get(
        "footage_alignment_required"
    ) is True


def validate_footage_alignment(
    project: Path, brief: dict, script: dict, edit: dict, assets: dict | None = None,
) -> dict:
    """Check complete, current per-cut observations and a near-zero reuse budget.

    A passing result verifies the evidence contract. It cannot establish that
    an agent truthfully described pixels; that remains an explicit visual review.
    """
    report = edit.get("footage_alignment")
    if not report:
        raise FootageAlignmentError(
            "FOOTAGE ALIGNMENT: missing per-cut visible-action review. Read "
            "skills/core/voiceover-footage.md; technical QA is not editorial acceptance."
        )
    validate_artifact("edit_decisions", edit)
    if report["status"] != "pass" or report["pattern_issues"]:
        raise FootageAlignmentError("FOOTAGE ALIGNMENT: unresolved editorial or repetition issues")
    cuts = edit["cuts"]
    if report["cuts_sha256"] != alignment_digest(cuts):
        raise FootageAlignmentError("FOOTAGE ALIGNMENT: stale review after cut changes")
    if report["script_sha256"] != alignment_digest(script):
        raise FootageAlignmentError("FOOTAGE ALIGNMENT: stale review after narration changes")
    words = script.get("metadata", {}).get("narration_words")
    if not isinstance(words, list) or not words:
        raise FootageAlignmentError("FOOTAGE ALIGNMENT: canonical narration word timestamps are required")
    previous_start = -1
    for word in words:
        if (not isinstance(word, dict) or not isinstance(word.get("text"), str)
                or not word["text"].strip()):
            raise FootageAlignmentError("FOOTAGE ALIGNMENT: invalid narration word")
        start, end = word.get("start_seconds"), word.get("end_seconds")
        if (any(isinstance(t, bool) or not isinstance(t, (int, float)) or not math.isfinite(t)
                for t in (start, end)) or not 0 <= start <= end <= script["total_duration_seconds"] + .125
                or start < previous_start):
            raise FootageAlignmentError("FOOTAGE ALIGNMENT: invalid narration word timestamps")
        previous_start = start
    ids = [cut["id"] for cut in cuts]
    rows = report["shots"]
    if len(set(ids)) != len(ids) or Counter(row["cut_id"] for row in rows) != Counter(ids):
        raise FootageAlignmentError("FOOTAGE ALIGNMENT: every cut needs exactly one review")
    by_id = {row["cut_id"]: row for row in rows}
    policy = brief.get("metadata", {}).get("footage_reuse_policy", {})
    budget = policy.get("max_reused_fraction", 0)
    gap_floor = policy.get("min_gap_seconds", 360)
    if (isinstance(budget, bool) or not isinstance(budget, (int, float))
            or not 0 <= budget <= .01 or isinstance(gap_floor, bool)
            or not isinstance(gap_floor, (int, float)) or gap_floor < 360):
        raise FootageAlignmentError("FOOTAGE ALIGNMENT: reuse budget must be 0–1%, gap at least 360s")
    project = project.resolve()
    asset_paths = {asset["id"]: asset["path"] for asset in (assets or {}).get("assets", [])}
    previous = []
    motifs = []
    reused_seconds = 0.0
    cursor = 0.0
    normalize = lambda text: " ".join(text.casefold().split())
    for cut in cuts:
        row = by_id[cut["id"]]
        if any(not normalize(row[key]) for key in (
            "visible_subject", "visible_action", "relation", "source_scene_id", "visual_motif",
        )):
            raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: empty observations for {cut['id']}")
        if row["match"] not in {"direct", "specific_context"}:
            raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: {cut['id']} is {row['match']}")
        if cut.get("layer", "primary") != "primary" or any(
            cut.get(key, "cut") not in {"cut", "none", ""}
            for key in ("transition_in", "transition_out")
        ):
            raise FootageAlignmentError("FOOTAGE ALIGNMENT: this contract requires a primary hard-cut timeline")
        start, end = cut["in_seconds"], cut["out_seconds"]
        if end <= start:
            raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: invalid source interval in {cut['id']}")
        duration = (end - start) / cut.get("speed", 1)
        spoken = " ".join(word["text"] for word in words
                          if word["end_seconds"] > cursor
                          and word["start_seconds"] < cursor + duration)
        quote = normalize(row["narration_quote"])
        if quote != normalize(spoken or "[pause]"):
            raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: {cut['id']} quote does not match its narration interval")
        samples = row["samples"]
        times = [sample["source_seconds"] for sample in samples]
        margin = min(.25, (end - start) * .2)
        if (times != sorted(set(times)) or times[0] < start or times[-1] > end
                or times[0] > start + margin or times[-1] < end - margin
                or abs(times[1] - (start + end) / 2) > (end - start) * .2):
            raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: {cut['id']} needs exact-trim start/middle/end evidence")
        for sample in samples:
            path = Path(sample["path"])
            path = (project / path).resolve() if not path.is_absolute() else path.resolve()
            if not path.is_relative_to(project) or not path.is_file():
                raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: missing project-local sample for {cut['id']}")
            with path.open("rb") as handle:
                digest = hashlib.sha256()
                for chunk in iter(lambda: handle.read(1024 * 1024), b""):
                    digest.update(chunk)
                if digest.hexdigest() != sample["sha256"]:
                    raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: changed sample for {cut['id']}")
        # Scene IDs identify original camera takes, across crops, file copies and
        # speed changes. Paths alone cannot distinguish repackaged copies.
        scene = normalize(row["source_scene_id"])
        source_path = Path(asset_paths.get(cut["source"], cut["source"]))
        source_path = source_path if source_path.is_absolute() else project / source_path
        if not source_path.is_file():
            raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: missing source for {cut['id']}")
        source = str(source_path.resolve())
        same = [old for old in previous if old["scene"] == scene]
        overlaps = [old for old in previous if old["source"] == source
                    and min(end, old["end"]) - max(start, old["start"]) > .001]
        repeats = {old["id"]: old for old in same + overlaps}
        if repeats:
            if len(repeats) > 1:
                raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: {cut['id']} repeats a source take more than once")
            old = next(iter(repeats.values()))
            if cursor - old["timeline_end"] < gap_floor:
                raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: {cut['id']} reprise gap is too short")
            reused_seconds += duration
        motif = normalize(row["visual_motif"])
        motifs.append(motif)
        if len(motifs) >= 3 and len(set(motifs[-3:])) == 1:
            raise FootageAlignmentError(f"FOOTAGE ALIGNMENT: repetitive visual pattern ending at {cut['id']}")
        previous.append({"id": cut["id"], "scene": scene, "source": source,
                         "start": start, "end": end, "timeline_end": cursor + duration})
        cursor += duration
    if abs(cursor - script["total_duration_seconds"]) > .125:
        raise FootageAlignmentError("FOOTAGE ALIGNMENT: cut coverage differs from full narration duration")
    fraction = reused_seconds / cursor if cursor else 0
    if fraction > budget + 1e-9:
        raise FootageAlignmentError(
            f"FOOTAGE ALIGNMENT: reused camera takes cover {fraction:.2%}; allowed {budget:.2%}"
        )
    return {"status": "pass", "shots": len(cuts), "reused_seconds": reused_seconds,
            "reused_fraction": fraction, "semantic_judgment": "agent-reviewed; not machine-verified"}
