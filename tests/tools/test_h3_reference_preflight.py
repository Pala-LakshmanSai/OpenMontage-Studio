"""Reject the observed reference-route validation failure before submission."""

import pytest

from tools.video.h3_max_video import H3MaxVideo


def request(**extra):
    return {
        "model": "h3-max",
        "operation": "reference_to_video",
        "prompt": "A seated woman holds her cup.",
        "image_url": "https://example.com/start.png",
        "duration": 5,
        "resolution": "768P",
        **extra,
    }


@pytest.mark.parametrize("extra", [{}, {"reference_image_urls": []}])
def test_start_frame_does_not_replace_required_reference(extra):
    with pytest.raises(ValueError, match="separate image, video, or audio reference"):
        H3MaxVideo().build_request(request(**extra))


def test_separate_reference_is_preserved():
    reference = ["https://example.com/identity.png"]
    *_, payload = H3MaxVideo().build_request(request(reference_image_urls=reference))
    assert payload["reference_image_urls"] == reference


def test_start_frame_without_reference_uses_image_route():
    _, operation, endpoint, payload = H3MaxVideo().build_request(
        request(operation="image_to_video")
    )
    assert operation == "image_to_video"
    assert endpoint == "minimax/h3-max/image-to-video"
    assert payload["image_url"] == "https://example.com/start.png"
