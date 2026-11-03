import json
from unittest.mock import patch

import pytest

from tools.analysis.fal_video_review import FalVideoReview, MODEL


def request(tmp_path):
    video = tmp_path / 'source.mp4'
    video.write_bytes(b'video')
    return {'video_path': str(video), 'prompt': 'Review all audio and video',
            'job_path': str(tmp_path / 'job.json'), 'output_path': str(tmp_path / 'review.json')}


def probe(types=('video', 'audio'), duration=1346.99):
    return json.dumps({'format': {'duration': duration}, 'streams': [{'codec_type': x} for x in types]})


def test_native_audio_and_reasoning_required(tmp_path):
    with patch('subprocess.check_output', return_value=probe()):
        payload, identity = FalVideoReview().build_request(request(tmp_path))
    assert payload['model'] == MODEL
    assert payload['reasoning'] is True
    assert payload['enable_web_search'] is False
    assert identity['duration_seconds'] == 1346.99


def test_silent_video_rejected(tmp_path):
    with patch('subprocess.check_output', return_value=probe(('video',))):
        with pytest.raises(ValueError, match='audio streams'):
            FalVideoReview().build_request(request(tmp_path))


def test_provider_body_limit_before_paid_request(tmp_path):
    inputs = request(tmp_path)
    from pathlib import Path
    with Path(inputs['video_path']).open('wb') as f:
        f.truncate(14_000_001)
    with pytest.raises(ValueError, match='provider body limit'):
        FalVideoReview().build_request(inputs)


def test_unknown_submit_cannot_replay(tmp_path, monkeypatch):
    monkeypatch.setenv('FAL_KEY', 'test-only')
    inputs = request(tmp_path)
    with patch('subprocess.check_output', return_value=probe()):
        tool = FalVideoReview()
        _, identity = tool.build_request(inputs)
        import hashlib
        fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
        from pathlib import Path
        Path(inputs['job_path']).write_text(json.dumps({'sha256': fingerprint, 'state': 'submitting'}))
        with patch('tools.analysis.fal_video_review.request_json') as submit:
            result = tool.execute(inputs)
        assert not result.success
        submit.assert_not_called()
