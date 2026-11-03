import json
from unittest.mock import patch

import pytest

from tools.audio.fal_elevenlabs_sfx import FalElevenLabsSfx
from tools.tool_registry import ToolRegistry


@pytest.fixture
def inputs(tmp_path, monkeypatch):
    monkeypatch.setenv("FAL_KEY", "fake-secret")
    return {"text": "wind outside a wooden house", "duration_seconds": 22,
            "loop": True, "job_path": str(tmp_path / "job.json"),
            "output_path": str(tmp_path / "wind.mp3")}


def accepted():
    base = "https://queue.fal.run/fal-ai/elevenlabs/requests/job-123"
    return {"request_id": "job-123", "status_url": base + "/status", "response_url": base}


def test_schema_price_and_discovery(inputs):
    tool = FalElevenLabsSfx()
    assert tool._build_payload(inputs) == {"text": inputs["text"], "duration_seconds": 22,
        "prompt_influence": 0.3, "loop": True, "output_format": "mp3_44100_128"}
    assert tool.estimate_cost(inputs) == 0.044
    inputs["duration_seconds"] = 0.5
    assert tool.estimate_cost(inputs) == 0.001
    registry = ToolRegistry()
    registry.discover()
    assert registry.get("fal_elevenlabs_sfx").name == "fal_elevenlabs_sfx"


@pytest.mark.parametrize("field,value", [("duration_seconds", 22.1), ("duration_seconds", 0.49),
    ("duration_seconds", float("nan")), ("loop", "false"), ("prompt_influence", 1.1), ("text", " ")])
def test_invalid_never_submits(inputs, field, value):
    inputs[field] = value
    with patch("tools.audio.fal_elevenlabs_sfx.request_json") as request:
        assert not FalElevenLabsSfx().execute(inputs).success
        request.assert_not_called()


@pytest.mark.parametrize("failure", [TimeoutError("unknown URL https://secret.invalid/x"), RuntimeError("HTTP 401 fake-secret")])
def test_unknown_submit_blocks_replay_and_redacts(inputs, failure):
    tool = FalElevenLabsSfx()
    with patch("tools.audio.fal_elevenlabs_sfx.request_json", side_effect=failure) as request:
        first = tool.execute(inputs)
        second = tool.execute(inputs)
    assert request.call_count == 1
    assert not first.success and not second.success
    assert "unknown" in second.error.lower()
    assert "fake-secret" not in first.error and "https://" not in first.error
    assert json.loads(open(inputs["job_path"]).read())["state"] == "submitting"


def test_accepted_resume_and_mismatch(inputs):
    tool = FalElevenLabsSfx()
    with patch("tools.audio.fal_elevenlabs_sfx.request_json", return_value=accepted()) as request, \
         patch("tools.audio.fal_elevenlabs_sfx.poll", side_effect=TimeoutError("expired")):
        first = tool.execute(inputs)
    assert not first.success
    assert request.call_count == 1 and request.call_args.args[0] == "POST"
    receipt = json.loads(open(inputs["job_path"]).read())
    assert receipt["state"] == "accepted"
    assert "https://" not in json.dumps(receipt)
    changed = dict(inputs, text="different")
    with patch("tools.audio.fal_elevenlabs_sfx.request_json") as request:
        assert "differs" in tool.execute(changed).error
        request.assert_not_called()
    with patch("tools.audio.fal_elevenlabs_sfx.request_json", return_value={"audio": {"url": "https://media.invalid/private"}}) as request, \
         patch("tools.audio.fal_elevenlabs_sfx.poll"), \
         patch("tools.audio.fal_elevenlabs_sfx.download", return_value=inputs["output_path"]):
        resumed = tool.execute(inputs)
    assert resumed.success and resumed.data["request_id"] == "job-123"
    assert request.call_count == 1 and request.call_args.args[0] == "GET"
    assert "https://" not in repr(resumed.data)
    assert resumed.cost_usd is None


def test_accepted_identity_survives_invalid_queue_urls(inputs):
    job = accepted()
    job["response_url"] = "https://queue.fal.run/fal-ai/elevenlabs/requests/job-123?access=secret"
    tool = FalElevenLabsSfx()
    with patch("tools.audio.fal_elevenlabs_sfx.request_json", return_value=job) as request:
        first = tool.execute(inputs)
        second = tool.execute(inputs)
    receipt = json.loads(open(inputs["job_path"]).read())
    assert not first.success and "reconciliation" in second.error
    assert request.call_count == 1
    assert receipt["state"] == "accepted_unverified" and receipt["request_id"] == "job-123"
    assert "secret" not in json.dumps(receipt)
