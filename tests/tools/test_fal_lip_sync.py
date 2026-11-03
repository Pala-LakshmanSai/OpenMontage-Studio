import json
from pathlib import Path
from unittest.mock import Mock

import requests

from tools.avatar.fal_lip_sync import FalLipSync


def inputs(tmp_path):
    for name in ["source.mp4", "speech.wav"]:
        (tmp_path / name).write_bytes(name.encode())
    return {"video_path": str(tmp_path / "source.mp4"), "audio_path": str(tmp_path / "speech.wav"),
            "output_path": str(tmp_path / "synced.mp4"), "job_path": str(tmp_path / "job.json")}


def ready(monkeypatch):
    monkeypatch.setenv("FAL_KEY", "test-key")
    tool = FalLipSync()
    monkeypatch.setattr(tool, "check_dependencies", lambda: None)
    monkeypatch.setattr(tool, "_duration", lambda path: 5.)
    monkeypatch.setattr(tool, "_upload", lambda path: "https://v3.fal.media/files/test/" + path.name)
    return tool


def complete(tool, monkeypatch):
    base = "https://queue.fal.run/fal-ai/sync-lipsync/requests/test-id"
    request = Mock(side_effect=[{"request_id": "test-id", "status_url": base + "/status", "response_url": base},
                               {"status": "COMPLETED", "request_id": "test-id"},
                               {"video": {"url": "https://media.example/output.mp4"}}])
    monkeypatch.setattr(tool, "_request", request)
    monkeypatch.setattr("tools.avatar.fal_lip_sync.download", lambda url, p: p.write_bytes(b"synced-video"))
    return request


def test_acceptance_resume_and_completed_reuse(tmp_path, monkeypatch):
    tool = ready(monkeypatch); args = inputs(tmp_path); request = complete(tool, monkeypatch)
    result = tool.execute(args)
    assert result.success
    assert request.call_count == 3
    receipt = json.loads(Path(args["job_path"]).read_text())
    assert receipt["quoted_usd"] == 5 * 5 / 60
    assert "test-key" not in Path(args["job_path"]).read_text()
    request.reset_mock()
    reused = tool.execute(args)
    assert reused.success and reused.cost_usd == 0 and not request.called
    Path(args["output_path"]).unlink()
    request.side_effect = [{"status": "COMPLETED"}, {"video": {"url": "https://media.example/output.mp4"}}]
    assert tool.execute(args).success
    assert all(call.args[0] == "GET" for call in request.call_args_list)


def test_unknown_submission_never_replayed(tmp_path, monkeypatch):
    tool = ready(monkeypatch); args = inputs(tmp_path)
    request = Mock(side_effect=requests.Timeout())
    monkeypatch.setattr(tool, "_request", request)
    assert not tool.execute(args).success
    assert json.loads(Path(args["job_path"]).read_text())["status"] == "submitting"
    request.reset_mock()
    result = tool.execute(args)
    assert not result.success and "unknown" in result.error and not request.called


def test_changed_inputs_do_not_submit(tmp_path, monkeypatch):
    tool = ready(monkeypatch); args = inputs(tmp_path); request = complete(tool, monkeypatch)
    assert tool.execute(args).success
    Path(args["audio_path"]).write_bytes(b"different-speech"); request.reset_mock()
    result = tool.execute(args)
    assert not result.success and "changed" in result.error and not request.called


def test_duration_mismatch_rejected_before_spend(tmp_path, monkeypatch):
    tool = ready(monkeypatch); args = inputs(tmp_path)
    monkeypatch.setattr(tool, "_duration", lambda p: 5 if Path(p).suffix == ".mp4" else 8)
    request = Mock(); monkeypatch.setattr(tool, "_request", request)
    assert not tool.execute(args).success and not request.called
    assert not Path(args["job_path"]).exists()


def test_bad_authenticated_host_never_called(monkeypatch):
    request = Mock(); monkeypatch.setattr(requests, "request", request)
    try:
        FalLipSync._request("GET", "https://foreign.example/status")
    except ValueError:
        pass
    else:
        raise AssertionError("Foreign host accepted")
    assert not request.called


def test_provider_identity_mismatch_preserves_acceptance(tmp_path, monkeypatch):
    tool = ready(monkeypatch); args = inputs(tmp_path); request = complete(tool, monkeypatch)
    base = "https://queue.fal.run/fal-ai/sync-lipsync/requests/test-id"
    request.side_effect = [{"request_id": "test-id", "status_url": base + "/status", "response_url": base},
                           {"status": "COMPLETED", "request_id": "wrong-id"}]
    result = tool.execute(args)
    assert not result.success and "identity" in result.error
    assert json.loads(Path(args["job_path"]).read_text())["request_id"] == "test-id"


def test_public_urls_only_and_terminal_validation_no_replay(tmp_path, monkeypatch):
    tool = ready(monkeypatch); args = inputs(tmp_path); request = complete(tool, monkeypatch)
    response = requests.Response(); response.status_code = 422
    base = "https://queue.fal.run/fal-ai/sync-lipsync/requests/test-id"
    request.side_effect = [{"request_id": "test-id", "status_url": base + "/status", "response_url": base},
                           {"status": "COMPLETED"}, requests.HTTPError(response=response)]
    result = tool.execute(args)
    assert not result.success
    payload = request.call_args_list[0].kwargs["json"]
    assert all(payload[k].startswith("https://") for k in ["video_url", "audio_url"])
    assert json.loads(Path(args["job_path"]).read_text())["status"] == "failed"
    request.reset_mock()
    assert not tool.execute(args).success and not request.called
