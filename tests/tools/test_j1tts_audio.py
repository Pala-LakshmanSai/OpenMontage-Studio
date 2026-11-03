import json
from unittest.mock import patch
import requests
from tools.audio.j1tts_audio import J1TTSAudio


def test_uncertain_submission_is_not_replayed_or_leaked(tmp_path, monkeypatch):
    monkeypatch.setenv("J1TTS_API_KEY", "test-secret")
    t=J1TTSAudio(); q={"operation":"tts","text":"Turn it off.","voice_id":"voice-1","output_path":str(tmp_path/"line.mp3")}
    with patch.object(t,"_request",side_effect=requests.Timeout("test-secret")) as http:
        a=t.execute(q);b=t.execute(q)
    assert not a.success and not b.success and http.call_count==1
    assert "test-secret" not in a.error+b.error
    assert "do not replay" in b.error
    assert json.loads((tmp_path/"line.mp3.j1tts-job.json").read_text())["status"]=="submitting"


def test_known_job_resumes_and_rejects_payload_change(tmp_path, monkeypatch):
    monkeypatch.setenv("J1TTS_API_KEY", "test-secret")
    t=J1TTSAudio(); out=tmp_path/"line.mp3"
    q={"operation":"tts","text":"Turn it off.","voice_id":"voice-1","output_path":str(out)}
    class R:
        headers={"content-type":"audio/mpeg"}
        def __init__(self,data=None):self.data=data
        def json(self):return self.data
        def iter_content(self,size):return iter([b"audio"])
    with patch.object(t,"_request",side_effect=[R({"id":"job-1"}),R({"id":"job-1","status":"completed"}),R()]) as http:
        assert t.execute(q).success
        assert t.execute(q).success
        assert not t.execute({**q,"text":"Changed paid input"}).success
    assert http.call_count==3
    assert "test-secret" not in (tmp_path/"line.mp3.j1tts-job.json").read_text()


def test_existing_import_and_uncertain_import_reconcile_exact_id(tmp_path, monkeypatch):
    monkeypatch.setenv("J1TTS_API_KEY", "test-secret")
    t=J1TTSAudio();q={"operation":"import","voice_id":"voice-1","job_path":str(tmp_path/"import.json")}
    with patch.object(t,"_voices",side_effect=[[],[{"voice_id":"voice-1","name":"Exact"}]]),patch.object(t,"_request",side_effect=requests.Timeout()) as http:
        assert t.execute(q).success
    assert http.call_count==1
    with patch.object(t,"_voices",return_value=[{"voice_id":"voice-1","name":"Exact"}]),patch.object(t,"_request") as http:
        assert t.execute(q).success
    http.assert_not_called()


def test_import_receipt_rejects_different_voice_before_network(tmp_path, monkeypatch):
    monkeypatch.setenv("J1TTS_API_KEY", "test-secret")
    receipt=tmp_path/"import.json"
    receipt.write_text(json.dumps({"operation":"import","voice_id":"voice-1","status":"submitting"}))
    t=J1TTSAudio()
    with patch.object(t,"_voices") as catalog:
        r=t.execute({"operation":"import","voice_id":"voice-2","job_path":str(receipt)})
    assert not r.success and "Saved voice id mismatch" in r.error
    catalog.assert_not_called()


def test_authenticated_requests_never_follow_redirects(monkeypatch):
    monkeypatch.setenv("J1TTS_API_KEY", "test-secret")
    class Redirect:
        status_code=302
    with patch("requests.request",return_value=Redirect()) as http:
        try:
            J1TTSAudio()._request("GET","/v1/my-voices")
        except RuntimeError as e:
            assert str(e)=="J1TTS redirect rejected"
        else:
            assert False,"Redirect must be rejected"
    assert http.call_args.kwargs["allow_redirects"] is False
