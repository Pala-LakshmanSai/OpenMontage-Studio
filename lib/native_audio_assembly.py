"""Decode native audio on its packet timeline before sample-based editing.

Copied AAC concatenations can contain overlapping encoder-padding packets at
joins. A plain linear decode (including pydub's default decoder) appends those
samples and drifts from the video. FFmpeg's timestamp-aware resampler drops or
fills discontinuities before PCM is handed to a sample-based mixer.
"""
from __future__ import annotations

import os
from pathlib import Path
import subprocess
import tempfile

NATIVE_AUDIO_TIMESTAMP_OPTIONS = "async=1:first_pts=0:min_hard_comp=0.001"


def decode_native_audio_timestamped(source: str | Path, output: str | Path) -> Path:
    """Write stereo 48 kHz PCM aligned to the source's audio packet timestamps.

    This repairs timestamp discontinuities, not speech pace or model phonemes.
    Existing outputs are preserved. No video or performance retiming occurs.
    """
    source, output = Path(source), Path(output)
    if output.exists():
        raise FileExistsError(output)
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".native-timed-", suffix=".wav", dir=output.parent)
    os.close(fd)
    try:
        subprocess.run(
            ["ffmpeg", "-hide_banner", "-loglevel", "error", "-y", "-i", str(source),
             "-map", "0:a:0", "-vn", "-af",
             "aresample=48000:" + NATIVE_AUDIO_TIMESTAMP_OPTIONS,
             "-ar", "48000", "-ac", "2", "-c:a", "pcm_s16le", temporary],
            check=True, capture_output=True,
        )
        os.replace(temporary, output)
    finally:
        Path(temporary).unlink(missing_ok=True)
    return output
