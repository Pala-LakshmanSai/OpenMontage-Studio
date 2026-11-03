"""Seedance queue receipts must never replay a potentially accepted paid job."""

import json
import stat
from pathlib import Path

import pytest
import requests

from tools.video.seedance_video import SeedanceVideo


class Response:
    def __init__(self, payload=None, content=b"video", status_code=200):
        self.payload = payload or {}
        self.status_code = status_code
        self.content = content

    def raise_for_status(self):
        pass

    def json(self):
        return self.payload


@pytest.fixture
def setup(monkeypatch, tmp_path):
    monkeypatch.setenv("FAL_KEY", "test-secret")
    monkeypatch.setattr("tools.video._shared.probe_output", lambda path: {})
    inputs = {
        "prompt": "Original person works beside the river",
        "model_version": "2.5", "operation": "reference_to_video",
        "duration": "12", "resolution": "720p",
        "reference_image_urls": ["https://image.example/identity"],
        "job_path": str(tmp_path / "job.json"),
        "output_path": str(tmp_path / "clip.mp4"), "max_poll_seconds": 0,
    }
    return SeedanceVideo(), inputs


def test_confirmed_job_resumes_exact_urls_without_post(setup, monkeypatch):
    tool, inputs = setup
    calls = {"post": 0, "get": []}
    status = ["IN_QUEUE", "COMPLETED"]

    def post(url, **kwargs):
        calls["post"] += 1
        receipt_path = Path(inputs["job_path"])
        receipt = json.loads(receipt_path.read_text())
        assert receipt["state"] == "submitting"
        assert stat.S_IMODE(receipt_path.stat().st_mode) == 0o600
        assert "test-secret" not in receipt_path.read_text()
        return Response({
            "request_id": "accepted-job-1",
            "status_url": "https://queue.fal.run/exact/status",
            "response_url": "https://queue.fal.run/exact/result",
        })

    def get(url, **kwargs):
        calls["get"].append(url)
        if url.endswith("/status"):
            return Response({"status": status.pop(0)})
        if url.endswith("/result"):
            return Response({"video": {"url": "https://media.example/result"}})
        return Response(content=b"mp4")

    monkeypatch.setattr(requests, "post", post)
    monkeypatch.setattr(requests, "get", get)
    assert not tool.execute(inputs).success
    receipt = json.loads(Path(inputs["job_path"]).read_text())
    assert receipt["request_id"] == "accepted-job-1"
    monkeypatch.setattr(requests, "post", lambda *a, **k: pytest.fail("resume submitted paid job"))
    result = tool.execute(inputs)
    assert result.success, result.error
    assert calls["post"] == 1
    assert calls["get"] == [
        "https://queue.fal.run/exact/status", "https://queue.fal.run/exact/status",
        "https://queue.fal.run/exact/result", "https://media.example/result",
    ]


def test_unknown_acceptance_receipt_blocks_replay_and_hides_provider_error(setup, monkeypatch):
    tool, inputs = setup
    calls = []

    def post(*args, **kwargs):
        calls.append(True)
        raise requests.Timeout("https://private.example/?token=SECRET")

    monkeypatch.setattr(requests, "post", post)
    result = tool.execute(inputs)
    assert not result.success
    assert "private.example" not in result.error and "SECRET" not in result.error
    monkeypatch.setattr(requests, "post", lambda *a, **k: pytest.fail("unknown job replayed"))
    result = tool.execute(inputs)
    assert not result.success and "unknown" in result.error
    assert len(calls) == 1


@pytest.mark.parametrize("change", ["input", "payload"])
def test_mismatched_input_or_receipt_payload_rejects_before_network(setup, monkeypatch, change):
    tool, inputs = setup
    monkeypatch.setattr(requests, "post", lambda *a, **k: Response({
        "request_id": "one", "status_url": "https://status", "response_url": "https://result",
    }))
    monkeypatch.setattr(requests, "get", lambda *a, **k: Response({"status": "IN_QUEUE"}))
    assert not tool.execute(inputs).success
    if change == "input":
        inputs["prompt"] = "Changed scene"
    else:
        path = Path(inputs["job_path"])
        receipt = json.loads(path.read_text())
        receipt["payload"]["prompt"] = "Changed payload"
        path.write_text(json.dumps(receipt))
    monkeypatch.setattr(requests, "post", lambda *a, **k: pytest.fail("mismatch POST"))
    monkeypatch.setattr(requests, "get", lambda *a, **k: pytest.fail("mismatch GET"))
    result = tool.execute(inputs)
    assert not result.success and "mismatch" in result.error


def test_pure_preflight_routes_and_conservative_costs(setup):
    tool, inputs = setup
    model, payload = tool.build_request(inputs)
    assert model == "bytedance/seedance-2.5/reference-to-video"
    assert payload["image_urls"] == inputs["reference_image_urls"]
    model, payload = tool.build_request({**inputs, "operation": "image_to_video", "image_url": "https://image"})
    assert model.endswith("/image-to-video") and payload["aspect_ratio"] == "auto"
    assert tool.estimate_cost(inputs) == 6.0
    assert tool.estimate_cost({**inputs, "resolution": "480p"}) == 2.76
    assert tool.estimate_cost({**inputs, "reference_video_urls": ["https://video"], "reference_video_duration_seconds": 3}) == 4.5
    assert tool.estimate_cost({**inputs, "duration": "auto"}) == 15.0
    model, payload = tool.build_request({"prompt": "scene", "model_version": "2.0", "model_variant": "fast"})
    assert model == "bytedance/seedance-2.0/fast/text-to-video"


@pytest.mark.parametrize("stage", ["submit", "result"])
@pytest.mark.parametrize("error_type,state", [
    ("content_policy_violation", "REJECTED_CONTENT"),
    ("invalid_request", "REJECTED_INPUT"),
])
def test_http_422_records_safe_terminal_rejection_and_never_repolls(
    setup, monkeypatch, stage, error_type, state
):
    tool, inputs = setup
    rejection = Response({"detail": [{
        "loc": ["body", "image_urls", 0, "https://private.example/token=SECRET"],
        "type": error_type,
        "msg": "The content could not be processed because it contained material flagged by a content checker. Cause: the provider detected an identifiable real person. https://private.example/?token=SECRET",
        "input": {"prompt": "MUST_NOT_RETAIN", "image_url": "https://private.example/?token=SECRET"},
    }], "payload": "MUST_NOT_RETAIN"}, status_code=422)
    posts = []

    def post(*args, **kwargs):
        posts.append(True)
        if stage == "submit":
            return rejection
        return Response({"request_id": "one", "status_url": "https://status", "response_url": "https://result"})

    monkeypatch.setattr(requests, "post", post)
    monkeypatch.setattr(requests, "get", lambda url, **kwargs: (
        Response({"status": "COMPLETED"}) if url == "https://status" else rejection
    ))
    result = tool.execute(inputs)
    assert not result.success and error_type in result.error
    assert result.data["state"] == state
    if error_type == "content_policy_violation":
        assert "identifiable real person" in result.error
        assert "Stop" in result.error and "do not retry" in result.error
    receipt_text = Path(inputs["job_path"]).read_text()
    assert "SECRET" not in receipt_text and "MUST_NOT_RETAIN" not in receipt_text
    assert "private.example" not in receipt_text and "private.example" not in result.error
    receipt = json.loads(receipt_text)
    assert receipt["state"] == state
    assert receipt["terminal_error_type"] == error_type
    assert receipt["terminal_error_detail"][0]["loc"] == ["body", "image_urls", 0]
    monkeypatch.setattr(requests, "post", lambda *a, **k: pytest.fail("rejected job POST"))
    monkeypatch.setattr(requests, "get", lambda *a, **k: pytest.fail("rejected job GET"))
    resumed = tool.execute(inputs)
    assert not resumed.success and resumed.error == result.error
    assert len(posts) == 1
