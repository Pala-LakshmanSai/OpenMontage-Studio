import json
from pathlib import Path
from unittest.mock import Mock

import requests
from filelock import FileLock
import pytest

from tools.enhancement.fal_bytedance_upscale import FalBytedanceUpscale, OPTIONS, MAX_SOURCE_BYTES


def test_unicode_source_upload_uses_temporary_ascii_symlink(tmp_path, monkeypatch):
    import fal_client
    source = tmp_path / "Film… glowing creature.mp4"
    source.write_bytes(b"original video")
    aliases = []

    def upload(path):
        alias = Path(path)
        aliases.append(alias)
        assert alias.name == "input.mp4" and alias.name.isascii()
        assert alias.is_symlink() and alias.resolve() == source.resolve()
        assert alias.read_bytes() == b"original video"
        return "https://v3.fal.media/files/test/video.mp4"

    monkeypatch.setattr(fal_client, "upload_file", upload)
    assert FalBytedanceUpscale._upload(source).endswith("/video.mp4")
    assert source.read_bytes() == b"original video"
    assert len(aliases) == 1 and not aliases[0].parent.exists()


def setup(tmp_path, monkeypatch):
    source = tmp_path / "source.mp4"; source.write_bytes(b"source")
    args = {"video_path": str(source), "output_path": str(tmp_path / "output.mp4"),
            "job_path": str(tmp_path / "job.json"), "poll_timeout": 0}
    tool = FalBytedanceUpscale()
    monkeypatch.setenv("FAL_KEY", "not-a-real-key")
    monkeypatch.setattr(tool, "check_dependencies", lambda: None)
    monkeypatch.setattr(tool, "_probe", lambda p: (1798.375, {"width": 1920, "height": 1080}))
    monkeypatch.setattr(tool, "_upload", Mock(return_value="https://v3.fal.media/files/test/source.mp4"))
    monkeypatch.setattr("tools.enhancement.fal_bytedance_upscale.download", lambda u, p: p.write_bytes(b"result"))
    return tool, args


def accepted():
    base = "https://queue.fal.run/fal-ai/bytedance-upscaler/requests/test-id"
    return {"request_id": "test-id", "status_url": base + "/status", "response_url": base}


def test_oversize_source_rejected_before_upload_or_submission(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    with Path(args["video_path"]).open("wb") as stream:
        stream.truncate(MAX_SOURCE_BYTES + 1)
    request = Mock(); monkeypatch.setattr(tool, "_request", request)
    result = tool.execute(args)
    assert not result.success and "250 MiB" in result.error
    assert not tool._upload.called and not request.called
    assert tool.input_schema["properties"]["video_path"]["x-max-file-size-bytes"] == MAX_SOURCE_BYTES


def test_accept_pending_resume_completed_no_replay(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    request = Mock(side_effect=[accepted(), {"status": "IN_PROGRESS"}]); monkeypatch.setattr(tool, "_request", request)
    result = tool.execute(args)
    assert not result.success and "pending" in result.error
    assert request.call_args_list[0].kwargs["json"] == {**OPTIONS, "video_url": tool._upload.return_value}
    assert "https://" not in json.dumps(result.data)
    receipt = json.loads(Path(args["job_path"]).read_text())
    assert receipt["state"] == "accepted" and receipt["estimated_usd"] == 1798.375 * .0072
    assert Path(args["job_path"]).stat().st_mode & 0o777 == 0o600
    request.reset_mock(); request.side_effect = [{"status": "COMPLETED"}, {"video": {"url": "https://media.example/output.mp4"}, "duration": 1798.375}]
    assert tool.execute(args).success
    assert all(c.args[0] == "GET" for c in request.call_args_list)
    assert tool._upload.call_count == 1
    request.reset_mock(); assert tool.execute(args).success and not request.called


def test_unknown_post_never_replayed(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    request = Mock(side_effect=requests.Timeout("private signed URL")); monkeypatch.setattr(tool, "_request", request)
    assert not tool.execute(args).success
    assert json.loads(Path(args["job_path"]).read_text())["state"] == "submitting"
    request.reset_mock(); result = tool.execute(args)
    assert "unknown" in result.error and not request.called


def test_upload_failure_resumes_before_paid_submission(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    tool._upload.side_effect = ValueError("https://secret.example/token")
    request = Mock(); monkeypatch.setattr(tool, "_request", request)
    result = tool.execute(args); assert result.error == "ValueError" and not request.called
    assert json.loads(Path(args["job_path"]).read_text())["state"] == "uploading"
    tool._upload.side_effect = None; request.side_effect = [accepted(), {"status": "IN_QUEUE"}]
    tool.execute(args); assert sum(c.args[0] == "POST" for c in request.call_args_list) == 1


def test_changed_source_and_tier_refused(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    request = Mock(side_effect=[accepted(), {"status": "IN_QUEUE"}]); monkeypatch.setattr(tool, "_request", request)
    tool.execute(args); request.reset_mock(); Path(args["video_path"]).write_bytes(b"changed")
    assert "changed" in tool.execute(args).error and not request.called
    assert not tool.execute({**args, "enhancement_tier": "pro"}).success and not request.called


def test_terminal_failure_no_replay(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    request = Mock(side_effect=[accepted(), {"status": "FAILED", "error": "private provider detail"}]); monkeypatch.setattr(tool, "_request", request)
    assert not tool.execute(args).success
    assert json.loads(Path(args["job_path"]).read_text())["state"] == "failed"
    request.reset_mock(); assert not tool.execute(args).success and not request.called


def test_bad_acceptance_identity_preserved_without_following_url(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    request = Mock(return_value={**accepted(), "status_url": "https://evil.example/status"}); monkeypatch.setattr(tool, "_request", request)
    assert not tool.execute(args).success and request.call_count == 1
    assert json.loads(Path(args["job_path"]).read_text())["request_id"] == "test-id"
    request.reset_mock(); assert not tool.execute(args).success and not request.called


def test_concurrent_receipt_owner_refused_before_upload(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    with FileLock(args["job_path"] + ".lock", timeout=0):
        result = tool.execute(args)
        assert not result.success and not tool._upload.called


@pytest.mark.parametrize("code", [402, 422])
def test_definitive_rejection_persisted_without_replay(tmp_path, monkeypatch, code):
    tool, args = setup(tmp_path, monkeypatch)
    response = requests.Response(); response.status_code = code
    request = Mock(side_effect=requests.HTTPError("secret provider body", response=response))
    monkeypatch.setattr(tool, "_request", request)
    result = tool.execute(args); assert result.error == "HTTPError"
    job = json.loads(Path(args["job_path"]).read_text())
    assert job["state"] == "failed" and job["failure_http_status"] == code
    assert "secret provider body" not in Path(args["job_path"]).read_text()
    request.reset_mock(); assert not tool.execute(args).success and not request.called


def test_authenticated_foreign_host_never_requested(monkeypatch):
    request = Mock(); monkeypatch.setattr(requests, "request", request)
    try:
        FalBytedanceUpscale._request("GET", "https://foreign.example/status")
    except ValueError:
        pass
    else:
        raise AssertionError("Foreign authenticated host accepted")
    assert not request.called


def test_native_25fps_archival_ratio_720p_and_exact_resume(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    args.update(target_fps=25, enhancement_preset="old_film", scale_ratio=20/9)
    source = {"width": 576, "height": 324, "avg_frame_rate": "25/1"}
    output = {"width": 1280, "height": 720, "avg_frame_rate": "25/1"}
    monkeypatch.setattr(tool, "_probe", lambda p: (3.12, source if Path(p) == Path(args['video_path']) else output))
    request = Mock(side_effect=[accepted(), {"status": "IN_QUEUE"}])
    monkeypatch.setattr(tool, "_request", request)
    assert not tool.execute(args).success
    body = request.call_args_list[0].kwargs['json']
    assert body['target_fps'] == 25 and body['enhancement_preset'] == 'old_film'
    assert body['scale_ratio'] == 20/9 and 'target_resolution' not in body
    request.reset_mock(); request.side_effect = [{"status": "COMPLETED"}, {"video": {"url": "https://media.example/output.mp4"}, "duration": 3.12}]
    assert tool.execute(args).success
    assert all(c.args[0] == 'GET' for c in request.call_args_list)
    request.reset_mock()
    assert not tool.execute({**args, 'scale_ratio': 2}).success and not request.called


def test_ratio_rejects_competing_target_or_frame_interpolation_before_upload(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    request = Mock(); monkeypatch.setattr(tool, '_request', request)
    assert not tool.execute({**args, 'scale_ratio': 2, 'target_resolution': '1080p'}).success
    monkeypatch.setattr(tool, '_probe', lambda p: (3.12, {'width': 576, 'height': 324, 'avg_frame_rate': '25/1'}))
    result = tool.execute({**args, 'scale_ratio': 20/9, 'target_fps': 24})
    assert not result.success and 'preserve source frame rate' in result.error
    assert not tool._upload.called and not request.called


def test_ratio_rejects_pixel_limit_and_wrong_returned_fps(tmp_path, monkeypatch):
    tool, args = setup(tmp_path, monkeypatch)
    request = Mock(); monkeypatch.setattr(tool, '_request', request)
    monkeypatch.setattr(tool, '_probe', lambda p: (3.12, {'width': 1920, 'height': 1080, 'avg_frame_rate': '25/1'}))
    assert not tool.execute({**args, 'scale_ratio': 3, 'target_fps': 25}).success
    assert not request.called and not tool._upload.called
    monkeypatch.setattr(tool, '_probe', lambda p: (3.12, {'width': 576, 'height': 324, 'avg_frame_rate': '25/1'} if Path(p) == Path(args['video_path']) else {'width': 1280, 'height': 720, 'avg_frame_rate': '24/1'}))
    request.side_effect = [accepted(), {'status': 'COMPLETED'}, {'video': {'url': 'https://media.example/output.mp4'}, 'duration': 3.12}]
    assert not tool.execute({**args, 'scale_ratio': 20/9, 'target_fps': 25}).success
    request.reset_mock(); request.side_effect = [{'status': 'COMPLETED'}, {'video': {'url': 'https://media.example/output.mp4'}, 'duration': 3.12}]
    assert not tool.execute({**args, 'scale_ratio': 20/9, 'target_fps': 25}).success
    assert all(c.args[0] == 'GET' for c in request.call_args_list)
