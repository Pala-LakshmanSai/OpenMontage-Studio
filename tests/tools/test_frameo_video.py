"""No network or paid generation: Frameo pass/no-replay boundaries."""
import hashlib
import json

import pytest
import requests

from tools.video.frameo_video import FrameoVideo


class Response:
    def __init__(self, data=None, status=200, content=b"video"):
        self.data, self.status_code, self.content = data, status, content
    def json(self): return self.data
    def raise_for_status(self):
        if self.status_code >= 400: raise requests.HTTPError("private provider URL")
    def iter_content(self, size): yield self.content


@pytest.fixture
def inputs(tmp_path):
    key = tmp_path / "key"
    key.write_text("test-secret")
    key.chmod(0o600)
    return dict(prompt="A wholly original traveler speaks naturally.", duration_seconds=30,
                api_key_path=str(key), job_path=str(tmp_path / "job.json"),
                output_path=str(tmp_path / "clip.mp4"), pass_expires_at="2099-01-01T00:00:00Z",
                max_poll_seconds=0)


def receipt(inputs, **changes):
    body = FrameoVideo.build_request(inputs)
    value = dict(input_hash=hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest(),
                 payload=body, generation_id="gen_accepted", state="running", idempotency_key="original")
    value.update(changes)
    from pathlib import Path
    Path(inputs["job_path"]).write_text(json.dumps(value))
    return value


def test_payload_is_exact_native_720p_contract(inputs):
    inputs.update(images=[{"url": "https://example.com/person.png", "role": "reference"}],
                  audios=[{"url": "https://example.com/voice.wav"}])
    body = FrameoVideo.build_request(inputs)
    assert body["model"] == "seedance_2_5"
    assert body["resolution"] == "720p" and body["generate_audio"] is True
    assert "api_key_path" not in body and "job_path" not in body
    assert body["images"] == inputs["images"] and body["audios"] == inputs["audios"]


def test_explicit_1080p_is_forwarded_without_draft_or_conversion(inputs):
    from jsonschema import validate
    inputs["resolution"] = "1080p"
    validate(inputs, FrameoVideo.input_schema)
    body = FrameoVideo.build_request(inputs)
    assert body["resolution"] == "1080p"
    assert "draft" not in body and "videos" not in body


@pytest.mark.parametrize("change", [{"model": "seedance_2_0"}, {"resolution": "2160p"},
                                    {"generate_audio": False}, {"duration_seconds": 31}])
def test_wrong_route_or_output_rejected(inputs, change):
    with pytest.raises(ValueError): FrameoVideo.build_request({**inputs, **change})


@pytest.mark.parametrize("resolution,credits", [("720p", 840), ("1080p", 2160)])
def test_nonzero_quote_never_submits(inputs, monkeypatch, resolution, credits):
    inputs["resolution"] = resolution
    calls = []
    def post(url, **kwargs):
        calls.append(url)
        assert kwargs["json"]["resolution"] == resolution
        return Response({"model": "seedance_2_5", "credits": credits, "standard_credits": credits})
    monkeypatch.setattr(requests, "post", post)
    result = FrameoVideo().execute(inputs)
    assert not result.success and calls == [FrameoVideo.API + "/estimates"]
    from pathlib import Path
    assert not Path(inputs["job_path"]).exists()


def test_expired_pass_never_submits_or_estimates(inputs, monkeypatch):
    inputs["pass_expires_at"] = "2000-01-01T00:00:00Z"
    monkeypatch.setattr(requests, "post", lambda *a, **k: pytest.fail("expired pass POST"))
    assert not FrameoVideo().execute(inputs).success


def test_unknown_acceptance_is_never_replayed(inputs, monkeypatch):
    calls = []
    def post(url, **kwargs):
        calls.append(url)
        if url.endswith("/estimates"):
            return Response({"model": "seedance_2_5", "credits": 0, "standard_credits": 840})
        assert kwargs["headers"]["Idempotency-Key"]
        raise requests.Timeout("secret test-secret provider URL")
    monkeypatch.setattr(requests, "post", post)
    first = FrameoVideo().execute(inputs)
    second = FrameoVideo().execute(inputs)
    assert not first.success and not second.success and len(calls) == 2
    assert "test-secret" not in first.error
    assert "uncertain" in second.error


def test_accepted_job_can_resume_after_pass_and_preserves_native_output(inputs, monkeypatch):
    receipt(inputs)
    inputs["pass_expires_at"] = "2000-01-01T00:00:00Z"
    monkeypatch.setattr(requests, "post", lambda *a, **k: pytest.fail("accepted job POST"))
    generation = dict(id="gen_accepted", model="seedance_2_5", status="succeeded",
                      outputs=[{"type": "video", "url": "https://example.com/video.mp4"}],
                      credits={"charged": 0, "standard": 840})
    def get(url, **kwargs):
        if url.startswith(FrameoVideo.API): return Response(generation)
        assert "headers" not in kwargs  # Never forward key to media storage.
        return Response(content=b"native-picture-and-speech")
    monkeypatch.setattr(requests, "get", get)
    result = FrameoVideo().execute(inputs)
    assert result.success and result.data["credits"]["charged"] == 0
    from pathlib import Path
    assert Path(inputs["output_path"]).read_bytes() == b"native-picture-and-speech"
    assert Path(inputs["job_path"]).stat().st_mode & 0o077 == 0


def test_terminal_job_not_replayed(inputs, monkeypatch):
    receipt(inputs, state="failed")
    monkeypatch.setattr(requests, "post", lambda *a, **k: pytest.fail("terminal replay"))
    monkeypatch.setattr(requests, "get", lambda *a, **k: pytest.fail("terminal poll"))
    assert not FrameoVideo().execute(inputs).success


def test_changed_payload_cannot_reuse_accepted_receipt(inputs, monkeypatch):
    receipt(inputs)
    inputs["prompt"] = "A different request"
    monkeypatch.setattr(requests, "post", lambda *a, **k: pytest.fail("changed replay"))
    result = FrameoVideo().execute(inputs)
    assert not result.success and "mismatch" in result.error


def test_upload_uses_signed_put_without_bearer_key(inputs, tmp_path, monkeypatch):
    source = tmp_path / "reference.png"
    source.write_bytes(b"image")
    monkeypatch.setattr(requests, "post", lambda *a, **k: Response({
        "upload_url": "https://storage.example.com/signed", "url": "https://storage.example.com/reference"}))
    def put(url, **kwargs):
        assert kwargs["headers"] == {"Content-Type": "image/png"}
        assert kwargs["data"].read() == b"image"
        return Response()
    monkeypatch.setattr(requests, "put", put)
    monkeypatch.setattr(requests, "get", lambda *a, **k: Response(status=206))
    assert FrameoVideo.upload_file(str(source), inputs["api_key_path"]) == "https://storage.example.com/reference"


def test_azure_upload_sends_required_blockblob_header(inputs, tmp_path, monkeypatch):
    source = tmp_path / "reference.png"
    source.write_bytes(b"image")
    monkeypatch.setattr(requests, "post", lambda *a, **k: Response({
        "upload_url": "https://frameo.blob.core.windows.net/files/input?sig=private",
        "url": "https://storage.example.com/reference"}))
    def put(url, **kwargs):
        assert kwargs["headers"] == {"Content-Type": "image/png", "x-ms-blob-type": "BlockBlob"}
        return Response()
    monkeypatch.setattr(requests, "put", put)
    monkeypatch.setattr(requests, "get", lambda *a, **k: Response(status=200))
    FrameoVideo.upload_file(str(source), inputs["api_key_path"])


def test_upload_error_never_exposes_signed_url(inputs, tmp_path, monkeypatch):
    source = tmp_path / "reference.png"
    source.write_bytes(b"image")
    monkeypatch.setattr(requests, "post", lambda *a, **k: Response({
        "upload_url": "https://frameo.blob.core.windows.net/files/input?sig=private",
        "url": "https://storage.example.com/reference"}))
    def put(*args, **kwargs):
        error = requests.HTTPError("400 from https://frameo.blob.core.windows.net/files/input?sig=private")
        error.response = Response(status=400)
        raise error
    monkeypatch.setattr(requests, "put", put)
    with pytest.raises(RuntimeError) as caught:
        FrameoVideo.upload_file(str(source), inputs["api_key_path"])
    assert "400" in str(caught.value) and "sig=" not in str(caught.value)


def test_private_uploaded_reference_is_rejected_before_generation(inputs, tmp_path, monkeypatch):
    source = tmp_path / "reference.png"
    source.write_bytes(b"image")
    monkeypatch.setattr(requests, "post", lambda *a, **k: Response({
        "upload_url": "https://frameo.blob.core.windows.net/files/input?sig=private",
        "url": "https://content.frameo.ai/private-reference"}))
    monkeypatch.setattr(requests, "put", lambda *a, **k: Response(status=201))
    def get(url, **kwargs):
        assert "Authorization" not in kwargs["headers"]
        return Response(status=401)
    monkeypatch.setattr(requests, "get", get)
    with pytest.raises(ValueError, match="not publicly fetchable.*401"):
        FrameoVideo.upload_file(str(source), inputs["api_key_path"])


def test_receipt_records_observed_utc_timing_once(inputs, monkeypatch):
    from datetime import datetime
    from pathlib import Path
    inputs.update(max_poll_seconds=2, poll_interval_seconds=0.1)
    def post(url, **kwargs):
        if url.endswith("/estimates"):
            return Response({"model": "seedance_2_5", "credits": 0, "standard_credits": 840})
        return Response({"id": "gen_timing", "status": "queued"}, status=202)
    states = iter(["running", "running", "succeeded"])
    def get(url, **kwargs):
        if url.startswith(FrameoVideo.API):
            state = next(states)
            return Response(dict(id="gen_timing", model="seedance_2_5", status=state,
                                 outputs=[{"type": "video", "url": "https://example.com/video.mp4"}],
                                 credits={"charged": 0, "standard": 840}))
        return Response(content=b"timed-native-video")
    monkeypatch.setattr(requests, "post", post)
    monkeypatch.setattr(requests, "get", get)
    ticks = iter([f"2026-11-03T08:00:0{i}Z" for i in range(7)])
    monkeypatch.setattr(FrameoVideo, "_utc_now", staticmethod(lambda: next(ticks)))
    result = FrameoVideo().execute(inputs)
    assert result.success
    saved = json.loads(Path(inputs["job_path"]).read_text())
    assert saved["submitted_at"] == "2026-11-03T08:00:00Z"
    assert saved["accepted_at"] == "2026-11-03T08:00:01Z"
    assert saved["running_first_seen_at"] == "2026-11-03T08:00:02Z"
    fields = ["submitted_at", "accepted_at", "running_first_seen_at", "completed_seen_at", "download_completed_at"]
    times = [datetime.fromisoformat(saved[k].replace("Z", "+00:00")) for k in fields]
    assert times == sorted(times) and all(saved[k].endswith("Z") for k in fields)
