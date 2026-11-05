"""Prevent missing bridges/stale selections from masquerading as completed films."""
import hashlib
import json

import pytest

from lib.narrative_continuity import (
    NarrativeContinuityError, cuts_digest, validate_foundation, validate_coverage,
)


@pytest.fixture
def movie(tmp_path):
    text = 'Reviewed whole screenplay: departure, rescue, consequential aftermath.'
    (tmp_path / 'screenplay.md').write_text(text)
    f = dict(status='reviewed', source_read_through_ending=True,
             protected_core=['Loss becomes recognition'],
             adaptation_decisions=['Add rescue arrival/contact; remove repeated scenic holds'],
             screenplay_path='screenplay.md', screenplay_sha256=hashlib.sha256(text.encode()).hexdigest(),
             unresolved_gaps=[], ending_sequence_id='S1', sequences=[dict(
                 id='S1', purpose='Rescue changes relationship', action_and_transition='Arrive, reach, grip, haul, react',
                 emotional_turn='Fear to relief with cost', performance_seconds=65,
                 required_beats=[dict(id='rescue', description='Arrival and first contact before haul')])])
    script = dict(version='1.0', title='Rescue', total_duration_seconds=65, sections=[dict(id='S1', text=text, start_seconds=0, end_seconds=65)], metadata=dict(narrative_foundation=f))
    cuts = [dict(id='c1', source='rescue.mp4', in_seconds=3, out_seconds=17)]
    coverage = dict(screenplay_sha256=f['screenplay_sha256'], cuts_sha256=cuts_digest(cuts),
                    unresolved_gaps=[], observations=[dict(beat_id='rescue', cut_id='c1',
                    source_start_seconds=4, source_end_seconds=12, mode='visible_action',
                    observed='Rescuer reaches rim, grips wrist, then pulls')])
    return tmp_path, script, dict(version='1.0', render_runtime='ffmpeg', cuts=cuts, metadata=dict(narrative_coverage=coverage))


def test_valid_observed_coverage_and_intentional_ellipsis(movie):
    project, script, edit = movie
    validate_coverage(project, script, edit)
    edit['metadata']['narrative_coverage']['observations'][0].update(
        mode='legible_ellipsis', observed='Established rope reach, offscreen strain, then same grip and wet survivor on rim')
    validate_coverage(project, script, edit)


@pytest.mark.parametrize('change', ['missing_review', 'unread_ending', 'open_gap', 'missing_screenplay', 'changed_screenplay', 'missing_beat', 'bad_time', 'duplicate_beat', 'wrong_ending'])
def test_reject_incomplete_foundation(movie, change):
    project, script, _ = movie
    f = script['metadata']['narrative_foundation']
    if change == 'missing_review': f['status'] = 'draft'
    if change == 'unread_ending': f['source_read_through_ending'] = False
    if change == 'open_gap': f['unresolved_gaps'] = ['Rescuer teleports into water']
    if change == 'missing_screenplay': (project / 'screenplay.md').unlink()
    if change == 'changed_screenplay': (project / 'screenplay.md').write_text('New ending')
    if change == 'missing_beat': f['sequences'][0]['required_beats'] = []
    if change == 'bad_time': f['sequences'][0]['performance_seconds'] = float('nan')
    if change == 'duplicate_beat': f['sequences'][0]['required_beats'] *= 2
    if change == 'wrong_ending': f['ending_sequence_id'] = 'missing'
    with pytest.raises(NarrativeContinuityError): validate_foundation(project, script)


@pytest.mark.parametrize('change', ['missing', 'unselected', 'trimmed_away', 'new_cuts', 'new_script', 'known_gap', 'prompt_only'])
def test_reject_false_or_stale_coverage(movie, change):
    project, script, edit = movie
    c = edit['metadata']['narrative_coverage']
    if change == 'missing': c['observations'] = []
    if change == 'unselected': c['observations'][0]['cut_id'] = 'unused-source'
    if change == 'trimmed_away': c['observations'][0]['source_start_seconds'] = 1
    if change == 'new_cuts': edit['cuts'][0]['in_seconds'] = 5
    if change == 'new_script': c['screenplay_sha256'] = 'old'
    if change == 'known_gap': c['unresolved_gaps'] = ['First contact never appears']
    if change == 'prompt_only': c['observations'][0]['mode'] = 'prompt_requested'
    with pytest.raises(NarrativeContinuityError): validate_coverage(project, script, edit)


@pytest.mark.parametrize('style', ['ai-movie', 'queen-elizabeth-i'])
def test_new_project_contract_survives_reinit_and_legacy_is_preserved(tmp_path, style):
    from lib.checkpoint import init_project
    new = init_project('new', title='New', pipeline_type='cinematic', pipeline_dir=tmp_path, style_playbook=style)
    init_project('new', title='New title', pipeline_type='cinematic', pipeline_dir=tmp_path, style_playbook=style)
    assert json.loads((new / 'project.json').read_text())['narrative_contract_version'] == 1
    legacy = tmp_path / 'legacy'; legacy.mkdir()
    (legacy / 'project.json').write_text('{"created_at":"2026-11-04"}')
    init_project('legacy', title='Preserved', pipeline_type='cinematic', pipeline_dir=tmp_path, style_playbook=style)
    assert 'narrative_contract_version' not in json.loads((legacy / 'project.json').read_text())


@pytest.mark.parametrize('style', ['ai-movie', 'queen-elizabeth-i'])
def test_checkpoint_blocks_media_before_review_without_mutating_work(tmp_path, monkeypatch, style):
    import lib.checkpoint as checkpoint
    checkpoint.init_project('new', title='New', pipeline_type='cinematic', pipeline_dir=tmp_path, style_playbook=style)
    monkeypatch.setattr(checkpoint, '_enforce_stage_prerequisites', lambda *a: None)
    monkeypatch.setattr(checkpoint, '_stage_requires_approval', lambda *a: False)
    with pytest.raises(checkpoint.CheckpointValidationError, match='review the whole screenplay'):
        checkpoint.write_checkpoint(tmp_path, 'new', 'assets', 'in_progress', {})
    assert not (tmp_path / 'new/checkpoint_assets.json').exists()


@pytest.mark.parametrize('style', ['ai-movie', 'queen-elizabeth-i'])
def test_checkpoint_cannot_render_unobserved_rescue(movie, monkeypatch, style):
    import lib.checkpoint as checkpoint
    project, script, edit = movie
    marker = dict(project_id='film', pipeline_type='cinematic', style_playbook=style, narrative_contract_version=1)
    (project / 'project.json').write_text(json.dumps(marker))
    (project / 'checkpoint_script.json').write_text(json.dumps(dict(version='1.0', project_id=project.name, pipeline_type='cinematic', stage='script', status='completed', timestamp='2026-11-05T00:00:00Z', artifacts=dict(script=script))))
    edit['metadata']['narrative_coverage']['observations'] = []
    (project / 'checkpoint_edit.json').write_text(json.dumps(dict(version='1.0', project_id=project.name, pipeline_type='cinematic', stage='edit', status='completed', timestamp='2026-11-05T00:00:00Z', artifacts=dict(edit_decisions=edit))))
    monkeypatch.setattr(checkpoint, '_enforce_stage_prerequisites', lambda *a: None)
    monkeypatch.setattr(checkpoint, '_stage_requires_approval', lambda *a: False)
    with pytest.raises(checkpoint.CheckpointValidationError, match='missing observed required beats: rescue'):
        checkpoint.write_checkpoint(project.parent, project.name, 'compose', 'in_progress', {})
    assert not (project / 'checkpoint_compose.json').exists()


@pytest.mark.parametrize('changed_screenplay', [False, True])
def test_queen_reviewed_foundation_permits_media_but_stale_review_blocks_it(movie, monkeypatch, changed_screenplay):
    import lib.checkpoint as checkpoint
    project, script, _ = movie
    checkpoint.init_project(project.name, title='Queen', pipeline_type='cinematic',
                            pipeline_dir=project.parent, style_playbook='queen-elizabeth-i')
    monkeypatch.setattr(checkpoint, '_enforce_stage_prerequisites', lambda *a: None)
    monkeypatch.setattr(checkpoint, '_stage_requires_approval', lambda *a: False)
    checkpoint.write_checkpoint(project.parent, project.name, 'script', 'completed', {'script': script})
    accepted = project / 'assets/video/accepted.mp4'
    accepted.write_bytes(b'existing accepted output must remain untouched')
    if changed_screenplay:
        (project / 'screenplay.md').write_text('A revised ending that has not been reviewed')
        with pytest.raises(checkpoint.CheckpointValidationError, match='screenplay changed'):
            checkpoint.write_checkpoint(project.parent, project.name, 'assets', 'in_progress', {})
        assert not (project / 'checkpoint_assets.json').exists()
    else:
        result = checkpoint.write_checkpoint(project.parent, project.name, 'assets', 'in_progress', {})
        assert json.loads(result.read_text())['status'] == 'in_progress'
    assert accepted.read_bytes() == b'existing accepted output must remain untouched'


@pytest.mark.parametrize('style,legacy', [('mira-beyond-the-screen', False), ('queen-elizabeth-i', True)])
def test_other_styles_and_legacy_queen_are_not_retroactively_blocked(tmp_path, monkeypatch, style, legacy):
    import lib.checkpoint as checkpoint
    project = tmp_path / 'preserved'
    if legacy:
        project.mkdir()
        (project / 'project.json').write_text(json.dumps({'created_at': '2026-11-04'}))
    checkpoint.init_project(project.name, title='Preserved', pipeline_type='cinematic',
                            pipeline_dir=tmp_path, style_playbook=style)
    monkeypatch.setattr(checkpoint, '_enforce_stage_prerequisites', lambda *a: None)
    monkeypatch.setattr(checkpoint, '_stage_requires_approval', lambda *a: False)
    assert 'narrative_contract_version' not in json.loads((project / 'project.json').read_text())
    result = checkpoint.write_checkpoint(tmp_path, project.name, 'assets', 'in_progress', {})
    assert result.is_file()


def test_queen_contract_cannot_be_bypassed_by_changing_explicit_style(tmp_path, monkeypatch):
    import lib.checkpoint as checkpoint
    checkpoint.init_project('queen', title='Queen', pipeline_type='cinematic',
                            pipeline_dir=tmp_path, style_playbook='queen-elizabeth-i')
    monkeypatch.setattr(checkpoint, '_enforce_stage_prerequisites', lambda *a: None)
    monkeypatch.setattr(checkpoint, '_stage_requires_approval', lambda *a: False)
    with pytest.raises(checkpoint.CheckpointValidationError, match='style disagrees'):
        checkpoint.write_checkpoint(tmp_path, 'queen', 'assets', 'in_progress', {},
                                    style_playbook='mira-beyond-the-screen')
