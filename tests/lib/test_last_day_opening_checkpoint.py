import hashlib
import json
import shutil
import subprocess

import pytest

from lib.checkpoint import CheckpointValidationError, write_checkpoint
from tests.lib.test_last_day_opening import evidence


@pytest.fixture(scope='module')
def video(tmp_path_factory):
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):
        pytest.skip('FFmpeg/ffprobe required for actual MP4 checkpoint regression')
    path = tmp_path_factory.mktemp('last-day-opening')/'output.mp4'
    subprocess.run(['ffmpeg','-hide_banner','-loglevel','error','-n',
                    '-f','lavfi','-i','color=c=blue:s=160x90:r=24:d=60',
                    '-c:v','libx264','-pix_fmt','yuv420p',str(path)],
                   check=True,capture_output=True)
    return path


@pytest.fixture
def checkpoint_case(tmp_path, monkeypatch, video):
    monkeypatch.setattr('lib.checkpoint._enforce_stage_prerequisites',lambda *args:None)
    project = tmp_path/'run'
    project.mkdir()
    data = evidence()
    data['source_sha256'] = data['transcript_source_sha256'] = hashlib.sha256(video.read_bytes()).hexdigest()
    path = project/'opening-input.json'
    path.write_text(json.dumps(data))
    render = {'version':'1.0','outputs':[{'path':str(video),'format':'mp4',
              'resolution':'160x90','duration_seconds':60}]}
    return project, path, data, render


def complete(project, render, **kwargs):
    return write_checkpoint(project.parent,project.name,'compose','completed',
                            {'render_report':render},style_playbook='the-last-day',**kwargs)


def test_last_day_completion_rejects_missing_opening_input(checkpoint_case):
    project, _, _, render = checkpoint_case
    with pytest.raises(CheckpointValidationError,match='requires last_day_opening_check_input'):
        complete(project,render)
    assert not (project/'checkpoint_compose.json').exists()


def test_marker_derived_last_day_style_cannot_skip_the_opening_requirement(checkpoint_case):
    project, _, _, render = checkpoint_case
    (project/'project.json').write_text(json.dumps({'style_playbook':'the-last-day'}))
    with pytest.raises(CheckpointValidationError,match='requires last_day_opening_check_input'):
        write_checkpoint(project.parent,project.name,'compose','completed',{'render_report':render})


def test_in_progress_last_day_compose_does_not_start_an_evidence_or_approval_wait(checkpoint_case):
    project, _, _, _ = checkpoint_case
    path = write_checkpoint(project.parent,project.name,'compose','in_progress',{},
                            style_playbook='the-last-day')
    assert json.loads(path.read_text())['status'] == 'in_progress'


def test_actual_repeated_native_phrase_blocks_completion(checkpoint_case):
    project, path, data, render = checkpoint_case
    data['segments'] = [{'start':14.73,'end':17.25,'text':'But the strangest part is where it happens.'},
                        {'start':18.49,'end':20.89,'text':'But the strangest part is where it happens.'}]
    path.write_text(json.dumps(data))
    with pytest.raises(CheckpointValidationError,match='repeated nearby narration'):
        complete(project,render,metadata={'last_day_opening_check_input':'opening-input.json'})
    assert not (project/'checkpoint_compose.json').exists()


@pytest.mark.parametrize('location',['checkpoint','render'])
def test_clean_matching_actual_output_completes(checkpoint_case,location):
    project, path, _, render = checkpoint_case
    metadata = {'last_day_opening_check_input':str(path)}
    if location == 'render':
        render['metadata'] = metadata
        metadata = None
    completed = complete(project,render,metadata=metadata)
    assert json.loads(completed.read_text())['status'] == 'completed'


def test_another_render_cannot_reuse_a_passing_opening_input(checkpoint_case):
    project, path, data, render = checkpoint_case
    data['source_sha256'] = data['transcript_source_sha256'] = 'b'*64
    path.write_text(json.dumps(data))
    with pytest.raises(CheckpointValidationError,match='does not match the actual MP4'):
        complete(project,render,metadata={'last_day_opening_check_input':str(path)})


def test_other_styles_keep_existing_compose_behavior(checkpoint_case):
    project, _, _, render = checkpoint_case
    completed = write_checkpoint(project.parent,project.name,'compose','completed',
                                 {'render_report':render},style_playbook='clean-professional')
    assert json.loads(completed.read_text())['status'] == 'completed'


def test_publishing_older_completed_last_day_export_does_not_add_opening_gate(checkpoint_case):
    project, _, _, render = checkpoint_case
    old = write_checkpoint(project.parent,project.name,'compose','completed',
                           {'render_report':render},style_playbook='clean-professional')
    legacy = json.loads(old.read_text())
    legacy['style_playbook'] = 'the-last-day'
    old.write_text(json.dumps(legacy))
    published = write_checkpoint(project.parent,project.name,'publish','completed',
                                 {'publish_log':{'version':'1.0','entries':[]}},
                                 style_playbook='the-last-day')
    assert json.loads(published.read_text())['status'] == 'completed'


def test_report_with_only_a_claimed_pass_cannot_bypass_input_check(checkpoint_case):
    project, path, _, render = checkpoint_case
    path.write_text(json.dumps({'status':'pass'}))
    with pytest.raises(CheckpointValidationError,match='opening check needs review'):
        complete(project,render,metadata={'last_day_opening_check_input':str(path)})
