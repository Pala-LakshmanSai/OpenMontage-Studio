from unittest.mock import patch

from tools.audio.fal_lyria_music import FalLyriaMusic
from tools.tool_registry import ToolRegistry


def test_lyria_native_contract_and_registry():
    tool = FalLyriaMusic()
    assert tool._QUEUE_URL == "https://queue.fal.run/fal-ai/lyria3/pro"
    assert tool._build_payload({"prompt": "55-second instrumental piano cue", "duration_seconds": 55}) == {
        "prompt": "55-second instrumental piano cue"
    }
    assert not tool.supports["exact_duration"]
    assert tool.estimate_cost({"duration_seconds": 55}) == 0.08
    registry = ToolRegistry()
    registry.discover()
    assert registry.get("fal_lyria_music").name == "fal_lyria_music"


def test_invalid_input_never_submits(monkeypatch):
    monkeypatch.setenv("FAL_KEY", "test-key")
    with patch("requests.post") as post:
        result = FalLyriaMusic().execute({"prompt": "piano", "duration_seconds": 300})
    assert not result.success
    post.assert_not_called()


def test_ambiguous_lyria_submit_is_not_replayed(tmp_path, monkeypatch):
    monkeypatch.setenv("FAL_KEY", "test-key")
    inputs = {"prompt": "55-second instrumental piano", "duration_seconds": 55,
              "job_path": str(tmp_path / "job.json")}
    with patch("requests.post", side_effect=TimeoutError("unknown acceptance")) as post:
        tool = FalLyriaMusic()
        assert not tool.execute(inputs).success
        assert not tool.execute(inputs).success
        assert post.call_count == 1
