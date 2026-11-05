"""Vertical / arbitrary-resolution support for video_compose's FFmpeg compose.

Regression test for a silent-dimension bug: the compose target resolution was
resolved from `profile` (and the documented `metadata.compose_target` hook) but
the per-segment scale/pad filter hardcoded 1920x1080, so vertical profiles like
`tiktok` silently produced landscape output. These tests run the real FFmpeg
path on a tiny lavfi fixture and assert the output dimensions.
"""

from __future__ import annotations

import shutil
import subprocess
import json
from fractions import Fraction
from pathlib import Path

import pytest

from tools.video.video_compose import VideoCompose

pytestmark = pytest.mark.skipif(
    shutil.which("ffmpeg") is None or shutil.which("ffprobe") is None,
    reason="ffmpeg/ffprobe not available",
)


def _make_clip(path: Path, w: int = 1280, h: int = 720, d: int = 2) -> None:
    subprocess.run(
        ["ffmpeg", "-y", "-f", "lavfi", "-i",
         f"color=c=teal:s={w}x{h}:d={d}:r=30",
         "-c:v", "libx264", "-crf", "28", "-pix_fmt", "yuv420p",
         "-g", "30", "-keyint_min", "30", str(path)],
        capture_output=True, check=True,
    )


def _dims(path: Path) -> tuple[int, int]:
    out = subprocess.check_output(
        ["ffprobe", "-v", "error", "-select_streams", "v:0",
         "-show_entries", "stream=width,height", "-of", "csv=p=0", str(path)]
    ).decode().strip()
    w, h = out.split(",")
    return int(w), int(h)


def _edit_decisions(src: Path, metadata: dict | None = None) -> dict:
    ed = {
        "version": "1.0",
        "render_runtime": "ffmpeg",
        "cuts": [{"id": "c1", "source": str(src), "in_seconds": 0, "out_seconds": 2}],
    }
    if metadata:
        ed["metadata"] = metadata
    return ed


def test_compose_default_is_landscape_hd(tmp_path):
    """No profile / no target → unchanged 1920x1080 default (backward compatible)."""
    src = tmp_path / "in.mp4"
    _make_clip(src)
    out = tmp_path / "out.mp4"
    r = VideoCompose().execute(
        {"operation": "compose", "edit_decisions": _edit_decisions(src), "output_path": str(out)}
    )
    assert r.success, r.error
    assert _dims(out) == (1920, 1080)


def test_compose_vertical_profile(tmp_path, monkeypatch):
    """profile='tiktok' → 1080x1920 (the bug: previously stayed 1920x1080)."""
    src = tmp_path / "in.mp4"
    _make_clip(src)
    out = tmp_path / "out.mp4"
    tool = VideoCompose()
    commands = []
    run_command = tool.run_command

    def record(command, **kwargs):
        commands.append(command)
        return run_command(command, **kwargs)

    monkeypatch.setattr(tool, "run_command", record)
    r = tool.execute(
        {"operation": "compose", "edit_decisions": _edit_decisions(src, {
            "compose_target": {"width": 320, "height": 180, "fps": 24}}),
         "profile": "tiktok", "output_path": str(out)}
    )
    assert r.success, r.error
    assert _dims(out) == (1080, 1920)
    assert _video_stream(out)["r_frame_rate"] == "30/1"  # Profile overrides target cadence too.
    final_command = commands[-1]
    assert final_command[final_command.index("-c:v") + 1] == "copy"


def test_compose_target_override_cover(tmp_path):
    """metadata.compose_target with fit='cover' → exact requested dims, cropped to fill."""
    src = tmp_path / "in.mp4"
    _make_clip(src)
    out = tmp_path / "out.mp4"
    ed = _edit_decisions(src, metadata={"compose_target": {"width": 720, "height": 1280, "fit": "cover"}})
    r = VideoCompose().execute(
        {"operation": "compose", "edit_decisions": ed, "output_path": str(out)}
    )
    assert r.success, r.error
    assert _dims(out) == (720, 1280)


def _video_stream(path):
    info = json.loads(subprocess.check_output([
        "ffprobe", "-v", "error", "-select_streams", "v:0",
        "-show_entries", "stream=r_frame_rate,nb_frames,duration", "-of", "json", str(path)]))
    return info["streams"][0]


@pytest.mark.parametrize("rate,with_audio", [(24, True), (24, False), ("24000/1001", False)])
def test_compose_explicit_cadence_preserves_frames_and_performed_time(tmp_path, rate, with_audio):
    src, out = tmp_path / "native.mp4", tmp_path / "out.mp4"
    command = ["ffmpeg", "-v", "error", "-y", "-f", "lavfi", "-i",
               "testsrc2=s=160x90:r=24:d=2"]
    if with_audio:
        command += ["-f", "lavfi", "-i", "sine=frequency=440:sample_rate=48000:duration=2"]
    command += ["-c:v", "libx264", "-pix_fmt", "yuv420p"]
    if with_audio:
        command += ["-c:a", "aac"]
    subprocess.run(command + [str(src)], check=True, capture_output=True)
    edits = _edit_decisions(src, {"compose_target": {
        "width": 160, "height": 90, "fit": "cover", "fps": rate}})
    result = VideoCompose().execute({"operation": "compose", "edit_decisions": edits,
                                     "output_path": str(out), "preset": "ultrafast"})
    assert result.success, result.error
    stream = _video_stream(out)
    assert Fraction(stream["r_frame_rate"]) == Fraction(str(rate))
    assert int(stream["nb_frames"]) == 48
    assert float(stream["duration"]) == pytest.approx(48 / float(Fraction(str(rate))), abs=.002)


@pytest.mark.parametrize("rate", [0, 241, "nan", "1/0", None, True])
def test_compose_rejects_invalid_cadence_before_encoding(tmp_path, rate):
    output = tmp_path / "out.mp4"
    edits = _edit_decisions(tmp_path / "not-read.mp4", {"compose_target": {"fps": rate}})
    result = VideoCompose().execute({"operation": "compose", "edit_decisions": edits,
                                     "output_path": str(output)})
    assert not result.success
    assert "compose_target.fps" in result.error
    assert not output.exists()
