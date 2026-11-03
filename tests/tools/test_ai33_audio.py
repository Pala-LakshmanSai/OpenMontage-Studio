import json
from unittest.mock import patch

import requests

from tools.audio.ai33_audio import AI33Audio


def test_payload_auth_resume_and_uncertain_submission_never_replayed(tmp_path, monkeypatch):
    monkeypatch.setenv("AI33_API_KEY", "secret-test-key")
    tool = AI33Audio()
    target = tmp_path / "voice.mp3"
    inputs = {"operation": "tts", "text": "It is a restraint.", "voice_id": "elevenlabs_sarah", "output_path": str(target)}
    calls = []

    def request(method, url, **kwargs):
        calls.append((method, url, kwargs))
        assert kwargs["headers"] == {"xi-api-key": "secret-test-key"}
        if method == "POST":
            assert kwargs["files"]["voice_id"] == (None, "elevenlabs_sarah")
            return {"success": True, "task_id": "job-1"}
        return {"status": "done", "credit_cost": 17, "metadata": {"audio_url": "https://example.com/audio.mp3"}}

    def freeze(url, path):
        path.write_bytes(b"audio")
        return str(path)

    with patch("tools.audio.ai33_audio.request_json", side_effect=request), patch("tools.audio.ai33_audio.download", side_effect=freeze):
        result = tool.execute(inputs)
        assert result.success and result.cost_usd is None and result.data["credit_cost"] == 17
        assert tool.execute({"operation": "tts", "job_id": "job-1", "output_path": str(target)}).success
    assert [c[0] for c in calls] == ["POST", "GET", "GET"]
    receipt = target.with_name(target.name + ".ai33-job.json")
    assert "secret-test-key" not in receipt.read_text()

    pending = {"operation": "sfx", "text": "Heavy chain straining", "duration_seconds": 6, "output_path": str(tmp_path / "chain.mp3")}
    with patch("tools.audio.ai33_audio.request_json", side_effect=requests.Timeout("secret-test-key")) as http:
        first = tool.execute(pending)
        second = tool.execute(pending)
    assert not first.success and not second.success and http.call_count == 1
    assert "secret-test-key" not in first.error + second.error
    assert json.loads((tmp_path / "chain.mp3.ai33-job.json").read_text())["status"] == "submitting"
    assert "do not replay" in second.error


def test_sfx_music_payload_and_validation(tmp_path, monkeypatch):
    monkeypatch.setenv("AI33_API_KEY", "secret-test-key")
    tool = AI33Audio()
    route, kwargs, body = tool._submission({"operation": "sfx", "text": "wind", "duration_seconds": 30, "loop": True})
    assert route == "/v1/task/sound-effect" and kwargs["json"]["model_id"] == "eleven_text_to_sound_v2"
    route, kwargs, body = tool._submission({"operation": "music", "prompt": "dark orchestral tension"})
    assert route == "/v1s/task/music-generation" and body["make_instrumental"] is True
    with patch("tools.audio.ai33_audio.request_json") as http:
        assert not tool.execute({"operation": "sfx", "text": "wind", "duration_seconds": 31, "output_path": str(tmp_path / "bad.mp3")}).success
        assert not tool.execute({"operation": "tts", "text": "hello", "voice_id": "unprefixed", "output_path": str(tmp_path / "bad.mp3")}).success
    http.assert_not_called()
