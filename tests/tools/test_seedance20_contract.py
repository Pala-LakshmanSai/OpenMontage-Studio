"""fal Seedance 2.0 live reference contract, checked 2026-11-03.

Source: https://fal.ai/models/bytedance/seedance-2.0/reference-to-video/api
Fast source: https://fal.ai/models/bytedance/seedance-2.0/fast/reference-to-video/api
These tests use no provider credentials or live generation.
"""
import hashlib
import json

import pytest
import requests

from tools.video.seedance_video import SeedanceVideo


def reference_inputs(**overrides):
    return {
        "prompt": "@Image1 is the same original traveler; @Audio1 guides his voice.",
        "model_version": "2.0", "model_variant": "standard",
        "operation": "reference_to_video", "duration": "8",
        "resolution": "720p", "aspect_ratio": "16:9", "generate_audio": True,
        "reference_image_urls": ["https://example.com/host.png"],
        "reference_video_urls": ["https://example.com/motion.mp4"],
        "reference_audio_urls": ["https://example.com/voice.wav"],
        **overrides,
    }


@pytest.mark.parametrize("variant", ["standard", "fast"])
def test_seedance20_references_reach_current_fal_fields(variant):
    inputs = reference_inputs(model_variant=variant)
    endpoint, payload = SeedanceVideo.build_request(inputs)
    prefix = "bytedance/seedance-2.0" + ("/fast" if variant == "fast" else "")
    assert endpoint == prefix + "/reference-to-video"
    assert payload["image_urls"] == inputs["reference_image_urls"]
    assert payload["video_urls"] == inputs["reference_video_urls"]
    assert payload["audio_urls"] == inputs["reference_audio_urls"]
    assert not any(key.startswith("reference_") for key in payload)
    assert payload["duration"] == "8" and payload["resolution"] == "720p"
    assert payload["generate_audio"] is True


def test_seedance25_reference_transport_unchanged():
    inputs = reference_inputs(model_version="2.5", duration="30")
    endpoint, payload = SeedanceVideo.build_request(inputs)
    assert endpoint == "bytedance/seedance-2.5/reference-to-video"
    assert payload["image_urls"] == inputs["reference_image_urls"]
    assert payload["video_urls"] == inputs["reference_video_urls"]
    assert payload["audio_urls"] == inputs["reference_audio_urls"]
    assert payload["duration"] == "30"


@pytest.mark.parametrize("duration", ["3", "16", "30", "5.0", 5])
def test_seedance20_rejects_duration_outside_live_enum(duration):
    with pytest.raises(ValueError, match="4.*15"):
        SeedanceVideo.build_request(reference_inputs(duration=duration))


@pytest.mark.parametrize("duration", ["auto", "4", "15"])
def test_seedance20_accepts_live_duration_edges(duration):
    assert SeedanceVideo.build_request(reference_inputs(duration=duration))[1]["duration"] == duration


def test_seedance20_combined_reference_limit():
    inputs = reference_inputs(
        reference_image_urls=["https://example.com/image.png"] * 9,
        reference_video_urls=["https://example.com/video.mp4"] * 3,
    )
    with pytest.raises(ValueError, match="12"):
        SeedanceVideo.build_request(inputs)
    inputs["reference_video_urls"] = inputs["reference_video_urls"][:2]
    assert len(SeedanceVideo.build_request(inputs)[1]["image_urls"]) == 9


def test_seedance20_audio_reference_requires_visual_reference():
    with pytest.raises(ValueError, match="image or video"):
        SeedanceVideo.build_request(reference_inputs(reference_image_urls=[], reference_video_urls=[]))


def test_existing_seedance20_receipt_resumes_saved_payload_without_post_or_rebuild(tmp_path, monkeypatch):
    """Contract fixes never rewrite an already accepted legacy request."""
    monkeypatch.setenv("FAL_KEY", "unit-test-key")
    tool = SeedanceVideo()
    inputs = reference_inputs(
        job_path=str(tmp_path / "job.json"), output_path=str(tmp_path / "clip.mp4"),
        max_poll_seconds=0,
    )
    legacy_payload = {"prompt": inputs["prompt"], "reference_image_urls": inputs["reference_image_urls"]}
    receipt = {
        "version": 1, "state": "IN_QUEUE", "input_hash": tool._input_hash(inputs),
        "payload_hash": hashlib.sha256(json.dumps(legacy_payload, sort_keys=True).encode()).hexdigest(),
        "model": "bytedance/seedance-2.0/reference-to-video", "payload": legacy_payload,
        "request_id": "already-accepted", "status_url": "https://queue.fal.run/accepted/status",
        "response_url": "https://queue.fal.run/accepted/result",
    }
    path = tmp_path / "job.json"
    path.write_text(json.dumps(receipt))
    monkeypatch.setattr(requests, "post", lambda *a, **k: pytest.fail("accepted job replayed"))
    monkeypatch.setattr(tool, "build_request", lambda *a, **k: pytest.fail("accepted payload rebuilt"))

    class Response:
        def raise_for_status(self):
            pass

        def json(self):
            return {"status": "IN_QUEUE"}

    gets = []
    monkeypatch.setattr(requests, "get", lambda url, **kwargs: (gets.append(url) or Response()))
    result = tool.execute(inputs)
    assert not result.success and "pending" in result.error
    assert gets == [receipt["status_url"]]
    saved = json.loads(path.read_text())
    assert saved["payload"] == legacy_payload
    assert saved["payload_hash"] == receipt["payload_hash"]
