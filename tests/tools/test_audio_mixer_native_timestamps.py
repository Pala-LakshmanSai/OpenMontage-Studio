"""Registered mixing/extraction must not accumulate copied AAC join padding."""
from pathlib import Path
import shutil
import subprocess

import numpy as np
import pytest

from tools.audio.audio_mixer import AudioMixer


def _run(*args):
    subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True, capture_output=True)


def _samples(path):
    raw = subprocess.check_output([
        "ffmpeg", "-v", "error", "-i", str(path), "-vn", "-ar", "8000",
        "-ac", "1", "-f", "f32le", "-",
    ])
    return np.frombuffer(raw, np.float32).astype(np.float64)


def _marker_offsets(path, reference, delay=0):
    audio, rate = _samples(path), 8000
    offsets = []
    for index in (0, 4, 9):
        expected = index * 1.25 + .15 + delay
        start = expected - .1
        region = audio[round(start * rate):round((start + 1) * rate)]
        best = int(np.argmax(np.correlate(region, reference, mode="valid")))
        offsets.append(start + best / rate - expected)
    return offsets


@pytest.fixture(scope="module")
def copied_aac(tmp_path_factory):
    if not shutil.which("ffmpeg"):
        pytest.skip("FFmpeg required for real AAC regression")
    root = tmp_path_factory.mktemp("mixer-aac-timestamps")
    part, native, music = (root / name for name in ("part.mp4", "native.mp4", "silence.wav"))
    _run("-f", "lavfi", "-i", "color=c=blue:s=64x64:r=24:d=1.25",
         "-f", "lavfi", "-i",
         r"aevalsrc=0.5*sin(2*PI*(430+250*t)*t)*between(t\,0.1\,0.7):s=48000:d=1.25",
         "-c:v", "libx264", "-preset", "ultrafast", "-threads", "1",
         "-c:a", "aac", "-b:a", "128k", "-ac", "2", str(part))
    listing = root / "native.ffconcat"
    listing.write_text("ffconcat version 1.0\n" + f"file '{part}'\n" * 10)
    _run("-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(native))
    _run("-f", "lavfi", "-i", "anullsrc=r=48000:cl=stereo", "-t", "1", str(music))
    source, linear = root / "source.wav", root / "linear.wav"
    _run("-i", str(part), "-vn", "-c:a", "pcm_s16le", str(source))
    _run("-i", str(native), "-vn", "-c:a", "pcm_s16le", str(linear))
    reference = _samples(source)[1200:5200]
    old = _marker_offsets(linear, reference)
    assert old[-1] - old[0] > .25  # The fixture reproduces the original failure.
    return native, music, reference


@pytest.mark.parametrize("operation", ["mix", "full_mix", "duck", "extract", "segmented_music"])
def test_registered_paths_preserve_native_marker_timing(copied_aac, tmp_path, operation):
    native, music, reference = copied_aac
    delay = .375 if operation in ("mix", "full_mix") else 0
    output = tmp_path / ("mixed.mp4" if operation == "segmented_music" else "mixed.wav")
    result = AudioMixer().execute({
        "operation": operation, "normalize": False, "ducking": {"enabled": False},
        "tracks": [{"path": str(native), "role": "speech", "start_seconds": delay}],
        "primary_audio": str(native), "secondary_audio": str(music),
        "input_path": str(native), "video_path": str(native), "music_path": str(music),
        "music_volume": 0, "segments": [{"start": 0, "end": 1}], "output_path": str(output),
    })
    assert result.success, result.error
    offsets = _marker_offsets(output, reference, delay)
    assert max(offsets) - min(offsets) < .001
    # The deliberate track delay remains intact; no resetting after adelay.
    assert max(abs(value) for value in offsets) < 1 / 24
