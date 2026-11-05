import json
from pathlib import Path
from unittest.mock import Mock

from PIL import Image
import pytest
import requests

from tools.graphics.kie_image import KieAPIError
from tools.video.kie_seedance_video import KieSeedanceVideo


@pytest.fixture
def setup(tmp_path, monkeypatch):
    monkeypatch.setenv('KIE_API_KEY', 'test-secret-never-log')
    project = tmp_path / 'project'; (project / 'artifacts').mkdir(parents=True)
    (project / 'artifacts/script.json').write_text('{}')
    monkeypatch.setattr('lib.narrative_continuity.validate_foundation', lambda *args: {})
    image = tmp_path / 'identity.png'; Image.new('RGB', (300, 300), 'blue').save(image)
    audio = tmp_path / 'voice.wav'; audio.write_bytes(b'original voice fixture')
    video = tmp_path / 'reference.mp4'; video.write_bytes(b'original two second reference fixture')
    tool = KieSeedanceVideo()
    def probe(path):
        if Path(path) == audio:
            return {'streams': [{'codec_type': 'audio'}], 'format': {'duration': '7'}}
        return {'streams': [{'codec_type': 'video', 'r_frame_rate': '24/1', 'nb_frames': '48' if Path(path) == video else '721', 'width': 1280, 'height': 720}, {'codec_type': 'audio'}], 'format': {'duration': '2' if Path(path) == video else '30.0416667'}}
    monkeypatch.setattr(tool, '_probe', probe)
    monkeypatch.setattr(tool, '_upload', Mock(return_value='https://example.com/original-reference'))
    quote = {'quoted_credits': 1216, 'quoted_usd': 6.08, 'balance_before': 4932.36}
    monkeypatch.setattr(tool, '_price_preflight', Mock(return_value=quote))
    inputs = {'prompt': 'Original queen speaks the complete local line.', 'reference_image_paths': [str(image)],
              'reference_audio_paths': [str(audio)], 'reference_video_path': str(video),
              'output_path': str(tmp_path / 'output.mp4'), 'job_path': str(tmp_path / 'private/receipt.json'),
              'project_dir': str(project), 'scene_id': 'C008', 'max_cost_usd': 6.08, 'remaining_budget_usd': 19.68}
    return tool, inputs


def completed(**changes):
    return {'taskId': 'task-1', 'model': KieSeedanceVideo.MODEL, 'state': 'success', 'creditsConsumed': 1216,
            'resultJson': json.dumps({'resultUrls': ['https://example.com/accepted-video']}), **changes}


def mock_download(monkeypatch, content=b'native accepted video fixture'):
    def write(url, path):
        path.parent.mkdir(parents=True, exist_ok=True); path.write_bytes(content)
    monkeypatch.setattr('tools.video.kie_seedance_video.download', write)


def test_unknown_acceptance_is_private_and_never_replayed(setup, monkeypatch):
    tool, inputs = setup
    http = Mock(side_effect=requests.Timeout('test-secret-never-log'))
    monkeypatch.setattr(tool, '_request', http)
    first, second = tool.execute(inputs), tool.execute(inputs)
    receipt = json.loads(Path(inputs['job_path']).read_text())
    assert not first.success and not second.success and http.call_count == 1
    assert receipt['state'] == 'acceptance_unknown' and 'payload' in receipt and receipt['input_sha256']
    assert 'do not replay' in second.error
    assert Path(inputs['job_path']).stat().st_mode & 0o077 == 0
    assert 'test-secret-never-log' not in json.dumps(first.data) + first.error + second.error


def test_pending_resume_success_cache_and_download_hash(setup, monkeypatch):
    tool, inputs = setup
    http = Mock(side_effect=[{'taskId': 'task-1'}, completed(state='generating')])
    monkeypatch.setattr(tool, '_request', http)
    pending = tool.execute(inputs)
    assert not pending.success and pending.data['state'] == 'running'
    http = Mock(return_value=completed()); monkeypatch.setattr(tool, '_request', http); mock_download(monkeypatch)
    result = tool.execute({'output_path': inputs['output_path'], 'job_path': inputs['job_path']})
    cached = tool.execute(inputs)
    assert result.success and cached.success and result.cost_usd == 0 and cached.cost_usd == 0
    assert result.data['output_sha256'] == tool._hash(inputs['output_path'])
    assert http.call_count == 1 and http.call_args.args[0] == 'GET'
    Path(inputs['output_path']).write_bytes(b'changed file')
    assert not tool.execute(inputs).success
    assert http.call_count == 1


@pytest.mark.parametrize('fault', [KieAPIError(403), KieAPIError(422)])
def test_explicit_refusal_is_terminal_no_replay(setup, monkeypatch, fault):
    tool, inputs = setup; http = Mock(side_effect=fault); monkeypatch.setattr(tool, '_request', http)
    assert not tool.execute(inputs).success
    again = tool.execute(inputs)
    assert not again.success and 'do not replay' in again.error and http.call_count == 1
    assert json.loads(Path(inputs['job_path']).read_text())['state'] == 'submission_refused'


def test_failed_accepted_task_never_creates_again(setup, monkeypatch):
    tool, inputs = setup
    http = Mock(side_effect=[{'taskId': 'task-1'}, completed(state='fail', failCode='unknown')]); monkeypatch.setattr(tool, '_request', http)
    assert not tool.execute(inputs).success and not tool.execute(inputs).success
    assert sum(call.args[0] == 'POST' for call in http.call_args_list) == 1
    assert json.loads(Path(inputs['job_path']).read_text())['state'] == 'failed'


@pytest.mark.parametrize('changes', [{'taskId': 'wrong-task'}, {'model': 'different-model'}, {'resultJson': '{malformed'}])
def test_result_identity_and_parsing_do_not_download(setup, monkeypatch, changes):
    tool, inputs = setup; monkeypatch.setattr(tool, '_request', Mock(side_effect=[{'taskId': 'task-1'}, completed(**changes)]))
    downloader = Mock(); monkeypatch.setattr('tools.video.kie_seedance_video.download', downloader)
    assert not tool.execute(inputs).success
    downloader.assert_not_called()
    assert json.loads(Path(inputs['job_path']).read_text())['task_id'] == 'task-1'


def test_invalid_download_preserves_exact_task_and_does_not_commit_output(setup, monkeypatch):
    tool, inputs = setup; monkeypatch.setattr(tool, '_request', Mock(side_effect=[{'taskId': 'task-1'}, completed()])); mock_download(monkeypatch)
    original = tool._probe
    monkeypatch.setattr(tool, '_probe', lambda path: {'streams': [{'codec_type': 'video', 'width': 1920, 'height': 1080, 'r_frame_rate': '24/1'}]} if str(path).endswith('.download') else original(path))
    assert not tool.execute(inputs).success and not Path(inputs['output_path']).exists()
    assert json.loads(Path(inputs['job_path']).read_text())['task_id'] == 'task-1'


def test_reference_changes_rejected_after_acceptance(setup, monkeypatch):
    tool, inputs = setup; http = Mock(side_effect=[{'taskId': 'task-1'}, completed(state='waiting')]); monkeypatch.setattr(tool, '_request', http)
    assert not tool.execute(inputs).success
    Image.new('RGB', (300, 300), 'red').save(inputs['reference_image_paths'][0])
    assert 'input mismatch' in tool.execute(inputs).error
    assert http.call_count == 2


@pytest.mark.parametrize('change', [{'duration_seconds': 25}, {'resolution': '480p'}, {'generate_audio': False}, {'model': 'seedance2'}, {'max_cost_usd': 9}])
def test_fixed_generation_contract_guards_before_network(setup, monkeypatch, change):
    tool, inputs = setup; http = Mock(); monkeypatch.setattr(tool, '_request', http)
    assert not tool.execute({**inputs, **change}).success
    http.assert_not_called(); tool._upload.assert_not_called()


@pytest.mark.parametrize('budget', [6.07, float('nan')])
def test_budget_preflight_rejects_before_http(setup, monkeypatch, budget):
    tool, inputs = setup; http = Mock(); monkeypatch.setattr('requests.get', http)
    with pytest.raises(ValueError, match='budget'):
        KieSeedanceVideo._price_preflight(tool, {**inputs, 'remaining_budget_usd': budget})
    http.assert_not_called()


def test_live_rate_and_credit_guard_read_only(setup, monkeypatch):
    tool, inputs = setup
    response = Mock(text='720P: 38 credits/s ($0.190/s, with video) | 63 credits/s ($0.315/s, no video)')
    monkeypatch.setattr('requests.get', Mock(return_value=response)); http = Mock(return_value=1216); monkeypatch.setattr(tool, '_request', http)
    quote = KieSeedanceVideo._price_preflight(tool, inputs)
    assert quote['quoted_usd'] == 6.08 and quote['quoted_credits'] == 1216
    assert http.call_args.args[0] == 'GET'
    response.text = '720P: 40 credits/s ($0.200/s, with video)'
    with pytest.raises(ValueError, match='rate'):
        KieSeedanceVideo._price_preflight(tool, inputs)


def test_bad_reference_duration_blocks_before_upload(setup, monkeypatch):
    tool, inputs = setup; original = tool._probe
    def probe(path):
        result = original(path)
        if str(path).endswith('reference.mp4'):
            result['streams'][0]['nb_frames'] = '49'
        return result
    monkeypatch.setattr(tool, '_probe', probe); http = Mock(); monkeypatch.setattr(tool, '_request', http)
    assert not tool.execute(inputs).success
    tool._upload.assert_not_called(); http.assert_not_called()
