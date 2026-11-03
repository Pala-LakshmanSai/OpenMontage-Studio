"""Evidence-contract regressions; these tests do not claim to test vision."""

import copy
import hashlib
import json

import pytest

from lib.checkpoint import CheckpointValidationError, init_project, write_checkpoint
from lib.footage_alignment import (
    FootageAlignmentError, alignment_digest, validate_footage_alignment,
)
from tests.contracts.test_phase0_contracts import sample_artifact


def make_edit(project, durations=(3, 3), starts=None):
    project.mkdir(parents=True, exist_ok=True)
    source = project / "source.mp4"
    source.write_bytes(b"source fixture; decoding is tested separately")
    frame = project / "frame.jpg"
    frame.write_bytes(b"frame fixture; semantic judgment is not machine-verified")
    frame_hash = hashlib.sha256(frame.read_bytes()).hexdigest()
    cuts, rows, sections = [], [], []
    cursor = 0
    for i, duration in enumerate(durations):
        start = starts[i] if starts else i * 1000
        cut = {"id": f"cut-{i}", "source": str(source),
               "in_seconds": start, "out_seconds": start + duration}
        quote = f"Concrete subject {i} performs action {i}."
        cuts.append(cut)
        rows.append({"cut_id": cut["id"], "narration_quote": quote,
                     "visible_subject": f"subject {i}", "visible_action": f"action {i}",
                     "match": "direct", "relation": f"Observed action supports clause {i}",
                     "source_scene_id": f"source:take-{i}", "visual_motif": f"subject action {i}",
                     "samples": [{"path": "frame.jpg", "source_seconds": stamp, "sha256": frame_hash}
                                 for stamp in (start + .05, start + duration / 2, start + duration - .05)]})
        sections.append({"id": f"s{i}", "text": quote, "start_seconds": cursor,
                         "end_seconds": cursor + duration})
        cursor += duration
    words = []
    for section in sections:
        tokens = section["text"].split()
        step = (section["end_seconds"] - section["start_seconds"]) / len(tokens)
        words.extend({"text": token, "start_seconds": section["start_seconds"] + i * step,
                      "end_seconds": min(section["end_seconds"], section["start_seconds"] + (i + 1) * step)}
                     for i, token in enumerate(tokens))
    script = {"version": "1.0", "title": "Fixture", "total_duration_seconds": cursor,
              "sections": sections, "metadata": {"narration_words": words}}
    edit = {"version": "1.0", "render_runtime": "ffmpeg", "cuts": cuts, "footage_alignment": {
        "version": "1.0", "status": "pass", "cuts_sha256": alignment_digest(cuts),
        "script_sha256": alignment_digest(script), "pattern_issues": [], "shots": rows,
    }}
    brief = sample_artifact("brief")
    brief["metadata"] = {"anchor_medium": "broll_footage"}
    brief["target_duration_seconds"] = cursor
    return brief, script, edit


def seal(edit, script):
    edit["footage_alignment"].update(cuts_sha256=alignment_digest(edit["cuts"]),
                                    script_sha256=alignment_digest(script))


def test_valid_observation_contract(tmp_path):
    brief, script, edit = make_edit(tmp_path)
    result = validate_footage_alignment(tmp_path, brief, script, edit)
    assert result["shots"] == 2 and result["reused_seconds"] == 0
    assert result["semantic_judgment"] == "agent-reviewed; not machine-verified"


def test_section_membership_is_not_enough_to_prove_word_alignment(tmp_path):
    brief, script, edit = make_edit(tmp_path)
    script["sections"] = [{"id": "whole", "text": " ".join(s["text"] for s in script["sections"]),
                           "start_seconds": 0, "end_seconds": 6}]
    edit["footage_alignment"]["shots"][0]["narration_quote"] = edit["footage_alignment"]["shots"][1]["narration_quote"]
    seal(edit, script)
    with pytest.raises(FootageAlignmentError, match="narration interval"):
        validate_footage_alignment(tmp_path, brief, script, edit)


def test_missing_word_timestamps_cannot_fall_back_to_section_tags(tmp_path):
    brief, script, edit = make_edit(tmp_path)
    script["metadata"] = {}
    seal(edit, script)
    with pytest.raises(FootageAlignmentError, match="word timestamps"):
        validate_footage_alignment(tmp_path, brief, script, edit)


def test_technical_edit_without_alignment_is_rejected(tmp_path):
    brief, script, edit = make_edit(tmp_path)
    del edit["footage_alignment"]
    with pytest.raises(FootageAlignmentError, match="missing per-cut"):
        validate_footage_alignment(tmp_path, brief, script, edit)


@pytest.mark.parametrize("match", ["generic", "mismatch", "unverified"])
def test_weak_pair_cannot_be_accepted_by_technical_pass(tmp_path, match):
    brief, script, edit = make_edit(tmp_path)
    edit["footage_alignment"]["shots"][0]["match"] = match
    with pytest.raises(FootageAlignmentError, match=f"is {match}"):
        validate_footage_alignment(tmp_path, brief, script, edit)


@pytest.mark.parametrize("mutation", ["trim", "crop", "speed", "source", "narration"])
def test_changed_binding_invalidates_old_review(tmp_path, mutation):
    brief, script, edit = make_edit(tmp_path)
    if mutation == "narration":
        script["sections"][0]["text"] = "Different narration."
    else:
        key, value = {"trim": ("in_seconds", .1), "crop": ("transform", {"scale": 1.2}),
                      "speed": ("speed", .9), "source": ("source", "other.mp4")}[mutation]
        edit["cuts"][0][key] = value
    with pytest.raises(FootageAlignmentError, match="stale review"):
        validate_footage_alignment(tmp_path, brief, script, edit)


@pytest.mark.parametrize("mutation", ["missing", "duplicate", "wrong_interval", "sample_changed",
                                      "opening_only", "issues", "blank"])
def test_false_or_incomplete_review_is_rejected(tmp_path, mutation):
    brief, script, edit = make_edit(tmp_path)
    review = edit["footage_alignment"]
    if mutation == "missing":
        review["shots"].pop()
    elif mutation == "duplicate":
        review["shots"][1] = copy.deepcopy(review["shots"][0])
    elif mutation == "wrong_interval":
        review["shots"][0]["narration_quote"] = script["sections"][1]["text"]
    elif mutation == "sample_changed":
        (tmp_path / "frame.jpg").write_bytes(b"different evidence")
    elif mutation == "opening_only":
        for sample, stamp in zip(review["shots"][0]["samples"], [.05, .1, .15]):
            sample["source_seconds"] = stamp
    elif mutation == "issues":
        review["pattern_issues"] = ["Coffee appears under Alexa privacy"]
    else:
        review["shots"][0]["visible_action"] = "   "
    with pytest.raises(FootageAlignmentError):
        validate_footage_alignment(tmp_path, brief, script, edit)


def test_disjoint_seconds_of_same_camera_take_are_still_reuse(tmp_path):
    brief, script, edit = make_edit(tmp_path)
    edit["footage_alignment"]["shots"][1]["source_scene_id"] = "source:take-0"
    with pytest.raises(FootageAlignmentError, match="gap is too short"):
        validate_footage_alignment(tmp_path, brief, script, edit)


def test_overlap_cannot_be_hidden_by_new_scene_id_or_asset_alias(tmp_path):
    brief, script, edit = make_edit(tmp_path, starts=[0, 1])
    source = edit["cuts"][1]["source"]
    edit["cuts"][1]["source"] = "alias"
    seal(edit, script)
    with pytest.raises(FootageAlignmentError, match="gap is too short"):
        validate_footage_alignment(tmp_path, brief, script, edit,
                                   {"assets": [{"id": "alias", "path": source}]})


def test_long_gap_does_not_override_zero_repetition_default(tmp_path):
    brief, script, edit = make_edit(tmp_path, durations=[3, 360, 3])
    edit["footage_alignment"]["shots"][2]["source_scene_id"] = "source:take-0"
    with pytest.raises(FootageAlignmentError, match="allowed 0.00%"):
        validate_footage_alignment(tmp_path, brief, script, edit)


def test_explicit_rare_reprise_budget_counts_whole_take_duration(tmp_path):
    brief, script, edit = make_edit(tmp_path, durations=[3, 360, 3])
    edit["footage_alignment"]["shots"][2]["source_scene_id"] = "source:take-0"
    brief["metadata"]["footage_reuse_policy"] = {"max_reused_fraction": .01}
    assert validate_footage_alignment(tmp_path, brief, script, edit)["reused_seconds"] == 3
    brief["metadata"]["footage_reuse_policy"]["max_reused_fraction"] = .005
    with pytest.raises(FootageAlignmentError, match="allowed 0.50%"):
        validate_footage_alignment(tmp_path, brief, script, edit)


def test_third_use_rejected_even_with_long_gaps_and_tiny_total_fraction(tmp_path):
    brief, script, edit = make_edit(tmp_path, durations=[1, 360, 1, 360, 1])
    for i in (2, 4):
        edit["footage_alignment"]["shots"][i]["source_scene_id"] = "source:take-0"
    brief["metadata"]["footage_reuse_policy"] = {"max_reused_fraction": .01}
    with pytest.raises(FootageAlignmentError, match="more than once"):
        validate_footage_alignment(tmp_path, brief, script, edit)


def test_distinct_excerpts_with_same_motif_are_not_visual_variety(tmp_path):
    brief, script, edit = make_edit(tmp_path, durations=[3, 3, 3])
    for row in edit["footage_alignment"]["shots"]:
        row["visual_motif"] = "shopper walking grocery aisle"
    with pytest.raises(FootageAlignmentError, match="repetitive visual pattern"):
        validate_footage_alignment(tmp_path, brief, script, edit)


@pytest.mark.parametrize("policy", [{"max_reused_fraction": .02}, {"min_gap_seconds": 359},
                                     {"max_reused_fraction": True}])
def test_reuse_policy_cannot_silently_relax_near_zero_requirement(tmp_path, policy):
    brief, script, edit = make_edit(tmp_path)
    brief["metadata"]["footage_reuse_policy"] = policy
    with pytest.raises(FootageAlignmentError, match="reuse budget"):
        validate_footage_alignment(tmp_path, brief, script, edit)


def prepare_project(tmp_path, required=True):
    project = init_project("run", title="Run", pipeline_type="hybrid", pipeline_dir=tmp_path)
    brief, script, edit = make_edit(project)
    if not required:
        brief["metadata"] = {"anchor_medium": "talking_head"}
    for stage, key, artifact in [
        ("idea", "brief", brief), ("script", "script", script),
        ("scene_plan", "scene_plan", sample_artifact("scene_plan")),
        ("assets", "asset_manifest", sample_artifact("asset_manifest")),
    ]:
        write_checkpoint(tmp_path, "run", stage, "completed", {key: artifact},
                         pipeline_type="hybrid", human_approved=True)
    return project, edit


def test_checkpoint_blocks_unreviewed_edit_before_writing(tmp_path):
    project, edit = prepare_project(tmp_path)
    del edit["footage_alignment"]
    with pytest.raises(CheckpointValidationError, match="missing per-cut"):
        write_checkpoint(tmp_path, "run", "edit", "completed", {"edit_decisions": edit},
                         human_approved=True)
    assert not (project / "checkpoint_edit.json").exists()


def test_compose_start_rechecks_persisted_edit_even_without_pipeline_argument(tmp_path):
    project, edit = prepare_project(tmp_path)
    path = write_checkpoint(tmp_path, "run", "edit", "completed", {"edit_decisions": edit},
                            human_approved=True)
    write_checkpoint(tmp_path, "run", "compose", "in_progress", {})
    saved = json.loads(path.read_text())
    del saved["artifacts"]["edit_decisions"]["footage_alignment"]
    path.write_text(json.dumps(saved))
    with pytest.raises(CheckpointValidationError, match="missing per-cut"):
        write_checkpoint(tmp_path, "run", "compose", "in_progress", {})


def test_other_hybrid_modes_remain_compatible(tmp_path):
    project, edit = prepare_project(tmp_path, required=False)
    del edit["footage_alignment"]
    path = write_checkpoint(tmp_path, "run", "edit", "completed", {"edit_decisions": edit},
                            human_approved=True)
    assert path.is_file()
