import json
from unittest.mock import patch

import pytest
import requests
from PIL import Image

from tools.graphics.kie_image import KieAPIError, KieImage


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setenv("KIE_API_KEY", "test-secret")
    return KieImage(), {"model": "nano-banana-2-1", "prompt": "Keep pose and costume.",
                        "resolution": "2K", "output_path": str(tmp_path / "shot.png")}


def finished(task_id="task-1", model="nano-banana-2-1"):
    return {"taskId": task_id, "model": model, "state": "success", "creditsConsumed": 6,
            "resultJson": json.dumps({"resultUrls": ["https://example.com/image.png"]})}


def image_download(url, path):
    Image.new("RGB", (48, 27), "gray").save(path, format="PNG")


def test_uncertain_paid_submission_never_replayed(setup):
    tool, inputs = setup
    with patch.object(tool, "_request", side_effect=requests.Timeout("test-secret")) as http:
        first = tool.execute(inputs)
        second = tool.execute(inputs)
    assert not first.success and not second.success and http.call_count == 1
    assert "do not replay" in second.error
    assert "test-secret" not in first.error + second.error + json.dumps(first.data)


def test_known_task_resume_reuse_and_input_identity(setup):
    tool, inputs = setup
    with patch.object(tool, "_request", side_effect=[{"taskId": "task-1"}, requests.Timeout()]) as http:
        with patch("time.sleep"), patch("time.monotonic", side_effect=[0, 0, 0, 899, 900, 901]):
            pending = tool.execute({**inputs, "poll_timeout": 900})
    assert not pending.success and pending.data["task_id"] == "task-1"
    with patch.object(tool, "_request", return_value=finished()) as http, patch("tools.graphics.kie_image.download", side_effect=image_download):
        result = tool.execute(inputs)
        assert result.success and result.data["reported_credits"] == 6
        assert result.cost_usd == 0 and result.data["quoted_usd"] == .03
        cached = tool.execute(inputs)
        assert cached.success and cached.cost_usd == 0
        assert not tool.execute({**inputs, "prompt": "Change accepted pose."}).success
    assert http.call_count == 1


@pytest.mark.parametrize("details", [finished(task_id="wrong"), finished(model="nano-banana-2")])
def test_provider_task_and_model_mismatch_rejected(setup, details):
    tool, inputs = setup
    with patch.object(tool, "_request", side_effect=[{"taskId": "task-1"}, details]), patch("tools.graphics.kie_image.download") as download:
        assert not tool.execute(inputs).success
    download.assert_not_called()


def test_local_reference_upload_and_changed_content_guard(setup, tmp_path):
    tool, inputs = setup
    ref = tmp_path / "reference.png"
    Image.new("RGB", (32, 18), "blue").save(ref)
    inputs["reference_images"] = [str(ref)]
    with patch.object(tool, "_request", side_effect=[{"downloadUrl": "https://example.com/reference.png"}, {"taskId": "task-1"}, finished()]) as http, patch("tools.graphics.kie_image.download", side_effect=image_download):
        assert tool.execute(inputs).success
    upload = http.call_args_list[0]
    assert upload.args[1] == tool._UPLOAD and "file" in upload.kwargs["files"]
    payload = http.call_args_list[1].kwargs["json"]
    assert payload["model"] == "nano-banana-2-1"
    assert payload["input"]["image_input"] == ["https://example.com/reference.png"]
    assert payload["input"]["resolution"] == "2K"
    Image.new("RGB", (32, 18), "red").save(ref)
    with patch.object(tool, "_request") as http:
        assert not tool.execute(inputs).success
    http.assert_not_called()


def test_http_200_body_error_and_auth_redirect(monkeypatch):
    monkeypatch.setenv("KIE_API_KEY", "test-secret")
    class Response:
        status_code = 200
        headers = {"Retry-After": "7"}
        def raise_for_status(self): pass
        def json(self): return {"code": 429, "msg": "test-secret"}
    with patch("requests.request", return_value=Response()) as http:
        with pytest.raises(KieAPIError) as error:
            KieImage()._request("GET", "https://api.kie.ai/api/v1/chat/credit")
        assert error.value.code == 429 and error.value.retry_after == 7
        assert http.call_args.kwargs["allow_redirects"] is False
        Response.status_code = 302
        with pytest.raises(ValueError, match="redirect"):
            KieImage()._request("GET", "https://api.kie.ai/api/v1/chat/credit")


def test_transient_poll_backoff_never_resubmits(setup):
    tool, inputs = setup
    with patch.object(tool, "_request", side_effect=[{"taskId": "task-1"}, KieAPIError(429, 7), finished()]) as http, patch("time.sleep") as sleep, patch("tools.graphics.kie_image.download", side_effect=image_download):
        assert tool.execute(inputs).success
    assert sum(call.args[0] == "POST" for call in http.call_args_list) == 1
    sleep.assert_called_once_with(7)


def test_rejects_over_limit_refs_and_unowned_output(setup):
    tool, inputs = setup
    with patch.object(tool, "_request") as http:
        assert not tool.execute({**inputs, "reference_images": ["https://example.com/ref.png"] * 11}).success
        from pathlib import Path
        Path(inputs["output_path"]).write_bytes(b"preserve")
        assert not tool.execute(inputs).success
        assert Path(inputs["output_path"]).read_bytes() == b"preserve"
    http.assert_not_called()


def test_default_1k_price_and_corrupt_download_preserves_output(setup):
    tool, inputs = setup
    assert tool.estimate_cost({}) == .02
    def corrupt(url, path): path.write_text("<html>not an image</html>")
    with patch.object(tool, "_request", side_effect=[{"taskId": "task-1"}, finished()]), patch("tools.graphics.kie_image.download", side_effect=corrupt):
        result = tool.execute(inputs)
    assert not result.success and result.data["task_id"] == "task-1"
    from pathlib import Path
    assert not Path(inputs["output_path"]).exists()

@pytest.mark.parametrize('code,message,classification', [(500, 'InternalError', 'provider_internal_error'), (400, 'Safety filter', 'unclassified')])
def test_terminal_failure_is_saved_for_guard_classification(setup, code, message, classification):
    tool, inputs = setup
    failure = {'taskId': 'task-1', 'model': 'nano-banana-2-1', 'state': 'fail',
               'failCode': code, 'failMsg': message, 'creditsConsumed': 0}
    with patch.object(tool, '_request', side_effect=[{'taskId': 'task-1'}, failure]) as http:
        result = tool.execute(inputs)
    assert not result.success and result.data['failure_class'] == classification
    assert result.data['failure_code'] == code and result.data['reported_credits'] == 0
    assert sum(c.args[0] == 'POST' for c in http.call_args_list) == 1
