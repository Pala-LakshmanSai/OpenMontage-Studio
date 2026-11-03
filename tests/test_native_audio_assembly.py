"""AAC join padding must not become cumulative audio/video delay."""
from pathlib import Path
import shutil
import subprocess
import wave

import numpy as np
import pytest

from lib.native_audio_assembly import decode_native_audio_timestamped


@pytest.mark.skipif(not shutil.which("ffmpeg"), reason="FFmpeg required for real AAC regression")
def test_copied_aac_joins_keep_first_middle_last_marker_on_video_timeline(tmp_path):
    def run(*args):
        subprocess.run(["ffmpeg", "-v", "error", "-y", *args], check=True, capture_output=True)

    part = tmp_path / "part.mp4"
    run("-f", "lavfi", "-i", "color=c=blue:s=64x64:r=24:d=1.25",
        "-f", "lavfi", "-i",
        r"aevalsrc=0.5*sin(2*PI*(430+250*t)*t)*between(t\,0.1\,0.7):s=48000:d=1.25",
        "-c:v", "libx264", "-preset", "ultrafast", "-threads", "1",
        "-c:a", "aac", "-b:a", "128k", "-ac", "2", str(part))
    listing = tmp_path / "parts.ffconcat"
    listing.write_text("ffconcat version 1.0\n" + f"file '{part}'\n" * 10)
    native = tmp_path / "native.mp4"
    run("-f", "concat", "-safe", "0", "-i", str(listing), "-c", "copy", str(native))
    source_wav, linear_wav, fixed_wav = (tmp_path / name for name in ("source.wav", "linear.wav", "fixed.wav"))
    run("-i", str(part), "-vn", "-c:a", "pcm_s16le", str(source_wav))
    # This is the old pydub decode path: packet samples appended without their PTS.
    run("-i", str(native), "-vn", "-c:a", "pcm_s16le", str(linear_wav))
    decode_native_audio_timestamped(native, fixed_wav)

    def samples(path: Path):
        with wave.open(str(path)) as stream:
            assert stream.getframerate() == 48000
            return np.frombuffer(stream.readframes(stream.getnframes()), np.int16).reshape(
                -1, stream.getnchannels()).mean(axis=1)[::6]

    rate = 8000
    reference = samples(source_wav)[round(.15 * rate):round(.65 * rate)]

    def offsets(path):
        audio = samples(path)
        result = []
        for index in (0, 4, 9):
            start = index * 1.25 + .05
            segment = audio[round(start * rate):round((start + 1) * rate)]
            best = int(np.argmax(np.correlate(segment, reference, mode="valid")))
            result.append(start + best / rate - (index * 1.25 + .15))
        return result

    linear, fixed = offsets(linear_wav), offsets(fixed_wav)
    assert linear[-1] - linear[0] > .25  # Reproduces accumulating AAC padding.
    assert max(fixed) - min(fixed) < .001
    assert max(abs(value) for value in fixed) < 1 / 24
