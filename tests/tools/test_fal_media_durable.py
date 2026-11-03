import json
import threading
from concurrent.futures import ThreadPoolExecutor

import tools.fal_media as fal_media
from tools.video.h3_max_video import H3MaxVideo


def _inputs(tmp_path):
    return {
        "model": "h3-max",
        "operation": "text_to_video",
        "prompt": "A quiet winter scene",
        "duration": 5,
        "resolution": "768P",
        "prompt_expansion_mode": "disabled",
        "job_path": str(tmp_path / "job.json"),
        "output_path": str(tmp_path / "out.mp4"),
    }


def test_unknown_acceptance_blocks_second_submission(monkeypatch, tmp_path):
    monkeypatch.setenv("FAL_KEY", "private-test-key")
    calls = []
    inputs = _inputs(tmp_path)

    def interrupted(method, url, **kwargs):
        calls.append(method)
        marker = json.loads((tmp_path / "job.json").read_text())
        assert marker["state"] == "submitting"
        assert len(marker["sha256"]) == 64
        assert "private-test-key" not in (tmp_path / "job.json").read_text()
        raise TimeoutError("provider acceptance is unknown")

    monkeypatch.setattr(fal_media, "request_json", interrupted)
    tool = H3MaxVideo()
    assert not tool.execute(inputs).success
    retry = tool.execute(inputs)
    assert not retry.success
    assert "Acceptance unknown" in retry.error
    assert calls == ["POST"]


def test_concurrent_same_receipt_submits_only_once(monkeypatch, tmp_path):
    monkeypatch.setenv("FAL_KEY", "test")
    entered = threading.Event()
    release = threading.Event()
    calls = []

    def interrupted(method, url, **kwargs):
        calls.append(method)
        entered.set()
        assert release.wait(timeout=5)
        raise TimeoutError("acceptance unknown")

    monkeypatch.setattr(fal_media, "request_json", interrupted)
    with ThreadPoolExecutor(max_workers=2) as pool:
        first = pool.submit(H3MaxVideo().execute, _inputs(tmp_path))
        assert entered.wait(timeout=5)
        second = pool.submit(H3MaxVideo().execute, _inputs(tmp_path))
        try:
            result = second.result(timeout=5)
            assert not result.success and "Acceptance unknown" in result.error
        finally:
            release.set()
        assert not first.result(timeout=5).success
    assert calls == ["POST"]


def test_accepted_receipt_resumes_and_rejects_changed_payload(monkeypatch, tmp_path):
    monkeypatch.setenv("FAL_KEY", "private-test-key")
    calls = []
    inputs = _inputs(tmp_path)

    def request(method, url, **kwargs):
        calls.append(method)
        if method == "POST":
            return {
                "request_id": "request-1",
                "status_url": "https://queue.fal.run/status",
                "response_url": "https://queue.fal.run/result",
            }
        if url.endswith("status"):
            return {"status": "COMPLETED"}
        return {"video": {"url": "data:video/mp4;base64,dmlkZW8="}}

    monkeypatch.setattr(fal_media, "request_json", request)
    monkeypatch.setattr(
        fal_media, "poll", lambda *a, **k: (_ for _ in ()).throw(TimeoutError())
    )
    tool = H3MaxVideo()
    first = tool.execute(inputs)
    assert not first.success
    receipt = json.loads((tmp_path / "job.json").read_text())
    assert receipt["state"] == "accepted"
    assert receipt["request_id"] == "request-1"
    assert "private-test-key" not in (tmp_path / "job.json").read_text()

    changed = tool.execute({**inputs, "prompt": "A different winter scene"})
    assert not changed.success and "Saved request differs" in changed.error
    assert json.loads((tmp_path / "job.json").read_text()) == receipt
    monkeypatch.setattr(fal_media, "poll", lambda fetch, **kwargs: fetch())
    resumed = tool.execute(inputs)
    assert resumed.success
    assert (tmp_path / "out.mp4").read_bytes() == b"video"
    assert calls.count("POST") == 1


def test_receipt_path_cannot_replace_output(monkeypatch, tmp_path):
    monkeypatch.setenv("FAL_KEY", "test")
    inputs = _inputs(tmp_path)
    inputs["output_path"] = inputs["job_path"]
    result = H3MaxVideo().execute(inputs)
    assert not result.success
    assert "must not overwrite" in result.error
    assert not (tmp_path / "job.json").exists()


def test_receipt_cannot_be_default_output_or_temporary_download(monkeypatch, tmp_path):
    monkeypatch.setenv("FAL_KEY", "test")
    monkeypatch.chdir(tmp_path)
    tool = H3MaxVideo()
    inputs = _inputs(tmp_path)
    inputs.pop("output_path")
    inputs["job_path"] = str(tmp_path / "h3_max_video.mp4")
    assert "must not overwrite" in tool.execute(inputs).error
    assert not (tmp_path / "h3_max_video.mp4").exists()

    inputs["job_path"] = str(tmp_path / "h3_max_video.mp4.part")
    assert "must not overwrite" in tool.execute(inputs).error
    assert not (tmp_path / "h3_max_video.mp4.part").exists()


def test_second_output_cannot_overwrite_accepted_receipt(monkeypatch, tmp_path):
    monkeypatch.setenv("FAL_KEY", "test")
    inputs = _inputs(tmp_path)
    inputs["job_path"] = str(tmp_path / "out_2.mp4")

    def request(method, url, **kwargs):
        if method == "POST":
            return {
                "request_id": "request-1",
                "status_url": "https://queue.fal.run/status",
                "response_url": "https://queue.fal.run/result",
            }
        if url.endswith("status"):
            return {"status": "COMPLETED"}
        return {"images": [{"url": "data:image/png;base64,YQ=="}] * 2}

    monkeypatch.setattr(fal_media, "request_json", request)
    monkeypatch.setattr(fal_media, "poll", lambda fetch, **kwargs: fetch())
    result = H3MaxVideo().execute(inputs)
    assert not result.success and "must not overwrite" in result.error
    assert json.loads((tmp_path / "out_2.mp4").read_text())["state"] == "accepted"
    assert not (tmp_path / "out.mp4").exists()


def test_crash_before_accepted_receipt_is_saved_blocks_replay(monkeypatch, tmp_path):
    monkeypatch.setenv("FAL_KEY", "test")
    calls = []
    original_write = fal_media._write_receipt

    def write(path, receipt, *, exclusive=False):
        if receipt["state"] == "accepted":
            raise OSError("simulated write failure")
        return original_write(path, receipt, exclusive=exclusive)

    def request(method, url, **kwargs):
        calls.append(method)
        return {
            "request_id": "request-1",
            "status_url": "https://queue.fal.run/status",
            "response_url": "https://queue.fal.run/result",
        }

    monkeypatch.setattr(fal_media, "_write_receipt", write)
    monkeypatch.setattr(fal_media, "request_json", request)
    tool = H3MaxVideo()
    first = tool.execute(_inputs(tmp_path))
    assert not first.success
    assert first.data["resume_job"]["request_id"] == "request-1"
    assert json.loads((tmp_path / "job.json").read_text())["state"] == "submitting"
    second = tool.execute(_inputs(tmp_path))
    assert not second.success and "Acceptance unknown" in second.error
    assert calls == ["POST"]


def test_legacy_accepted_receipt_resumes_without_post_or_mutation(monkeypatch, tmp_path):
    monkeypatch.setenv("FAL_KEY", "test")
    receipt = {
        "request_id": "legacy-request",
        "status_url": "https://queue.fal.run/status",
        "response_url": "https://queue.fal.run/result",
        "model": "h3-max",
        "operation": "text_to_video",
        "endpoint": "minimax/h3-max/text-to-video",
        "tool": "h3_max_video",
    }
    path = tmp_path / "legacy.json"
    original = json.dumps(receipt, indent=2)
    path.write_text(original)
    calls = []

    def request(method, url, **kwargs):
        calls.append(method)
        assert method == "GET"
        if url.endswith("status"):
            return {"status": "COMPLETED"}
        return {"video": {"url": "data:video/mp4;base64,dmlkZW8="}}

    monkeypatch.setattr(fal_media, "request_json", request)
    monkeypatch.setattr(fal_media, "poll", lambda fetch, **kwargs: fetch())
    inputs = {"job_path": str(path), "resume_job": receipt, "output_path": str(tmp_path / "out.mp4")}
    result = H3MaxVideo().execute(inputs)
    assert result.success
    assert (tmp_path / "out.mp4").read_bytes() == b"video"
    assert calls == ["GET", "GET"]
    assert path.read_text() == original

    calls.clear()
    changed = H3MaxVideo().execute({**inputs, "prompt": "unverifiable change"})
    assert not changed.success and "without request inputs" in changed.error
    changed_job = H3MaxVideo().execute({**inputs, "resume_job": {**receipt, "request_id": "other"}})
    assert not changed_job.success
    assert calls == []
    assert path.read_text() == original
