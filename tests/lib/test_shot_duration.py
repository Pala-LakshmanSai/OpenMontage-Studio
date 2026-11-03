import json
from pathlib import Path
import shutil
import subprocess

import pytest

from lib.shot_duration import ShotDurationError, scan_shots, validate_video_shots


@pytest.fixture(scope="module")
def videos(tmp_path_factory):
    if not shutil.which("ffmpeg") or not shutil.which("ffprobe"):
        pytest.skip("FFmpeg/ffprobe required for actual internal-cut regression")
    root = tmp_path_factory.mktemp("shot-duration")
    paths = {}
    for name, lengths in [("short", [2.5, 1, 2.5]), ("valid", [2, 2, 2])]:
        path = root / f"{name}.mp4"
        command = ["ffmpeg", "-hide_banner", "-loglevel", "error", "-n"]
        for color, duration in zip(["red", "blue", "green"], lengths):
            command += ["-f", "lavfi", "-i", f"color=c={color}:s=160x90:r=24:d={duration}"]
        command += ["-filter_complex", "[0:v][1:v][2:v]concat=n=3:v=1:a=0[v]", "-map", "[v]",
                    "-c:v", "libx264", "-pix_fmt", "yuv420p", str(path)]
        subprocess.run(command, check=True, capture_output=True)
        paths[name] = path
    return paths


def test_real_one_second_internal_shot_is_blocked(videos, tmp_path):
    # One six-second file conceals a one-second shot in its middle.
    report = scan_shots(videos["short"], cache_dir=tmp_path)
    assert report["duration_seconds"] == pytest.approx(6)
    assert report["short_intervals"] == [{"start_seconds": 2.5, "end_seconds": 3.5, "duration_seconds": 1.0}]
    with pytest.raises(ShotDurationError, match=r"2\.500–3\.500s"):
        validate_video_shots(videos["short"], cache_dir=tmp_path)


def test_exact_two_second_shots_pass(videos, tmp_path):
    result = validate_video_shots(videos["valid"], cache_dir=tmp_path)
    assert result["boundaries_seconds"] == pytest.approx([0, 2, 4, 6])
    assert result["unresolved_short_intervals"] == []


def test_explicit_owner_exception_only_covers_its_interval(videos, tmp_path):
    exception = {"start_seconds": 2.5, "end_seconds": 3.5,
                 "owner_instruction": "Use a one-second insert at this point."}
    validate_video_shots(videos["short"], cache_dir=tmp_path,
                         metadata={"short_shot_exceptions": [exception]})
    with pytest.raises(ShotDurationError, match="SHORT SHOT"):
        validate_video_shots(videos["short"], cache_dir=tmp_path,
            metadata={"short_shot_exceptions": [{**exception, "start_seconds": 0, "end_seconds": 1}]})
    with pytest.raises(ShotDurationError, match="explicit owner_instruction"):
        validate_video_shots(videos["short"], cache_dir=tmp_path,
            metadata={"short_shot_exceptions": [{**exception, "owner_instruction": True}]})


def test_documented_false_boundary_needs_real_candidate_and_evidence(videos, tmp_path):
    disposition = {"at_seconds": 2.5, "reason": "Continuous camera movement, not a cut",
                   "evidence": "local inspected range 2–4 seconds"}
    validate_video_shots(videos["short"], cache_dir=tmp_path,
                         metadata={"shot_boundary_dispositions": [disposition]})
    with pytest.raises(ShotDurationError, match="does not match"):
        validate_video_shots(videos["short"], cache_dir=tmp_path,
            metadata={"shot_boundary_dispositions": [{**disposition, "at_seconds": 1}]})
    with pytest.raises(ShotDurationError, match="reason and evidence"):
        validate_video_shots(videos["short"], cache_dir=tmp_path,
            metadata={"shot_boundary_dispositions": [{**disposition, "evidence": ""}]})


def test_completed_scan_cache_avoids_another_probe_or_decode(videos, tmp_path, monkeypatch):
    first = scan_shots(videos["valid"], cache_dir=tmp_path)
    def forbidden(*args, **kwargs):
        pytest.fail("Cached scan must not run FFmpeg/ffprobe again")
    monkeypatch.setattr("lib.shot_duration._run", forbidden)
    assert scan_shots(videos["valid"], cache_dir=tmp_path) == first


def test_scan_failure_is_closed_and_sanitized(videos, tmp_path, monkeypatch):
    def failed(*args, **kwargs):
        raise subprocess.CalledProcessError(1, ["ffprobe"], stderr="Authorization: PRIVATE_VALUE")
    monkeypatch.setattr("lib.shot_duration.subprocess.run", failed)
    with pytest.raises(ShotDurationError) as caught:
        validate_video_shots(videos["valid"], cache_dir=tmp_path)
    assert "no pass recorded" in str(caught.value)
    assert "PRIVATE_VALUE" not in str(caught.value)
    assert not list(tmp_path.glob("*.json"))


def test_missing_video_is_not_a_pass(tmp_path):
    with pytest.raises(ShotDurationError, match="Final video missing"):
        validate_video_shots(tmp_path / "missing.mp4")


def test_shared_checkpoint_blocks_actual_short_export_and_reuses_publish_scan(videos, tmp_path, monkeypatch):
    from lib.checkpoint import CheckpointValidationError, write_checkpoint
    monkeypatch.setattr("lib.checkpoint._enforce_stage_prerequisites", lambda *args: None)
    def artifact(path):
        return {"version": "1.0", "outputs": [{"path": str(path), "format": "mp4",
                "resolution": "160x90", "duration_seconds": 6}]}
    with pytest.raises(CheckpointValidationError, match="SHORT SHOT"):
        write_checkpoint(tmp_path, "run", "compose", "completed",
                         {"render_report": artifact(videos["short"])})
    assert not (tmp_path / "run/checkpoint_compose.json").exists()
    write_checkpoint(tmp_path, "run", "compose", "completed",
                     {"render_report": artifact(videos["valid"])})
    def forbidden(*args, **kwargs):
        pytest.fail("Publish must reuse unchanged final output scan")
    monkeypatch.setattr("lib.shot_duration._run", forbidden)
    write_checkpoint(tmp_path, "run", "publish", "completed",
                     {"publish_log": {"version": "1.0", "entries": []}})
    assert json.loads((tmp_path / "run/checkpoint_publish.json").read_text())["status"] == "completed"
