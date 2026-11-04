from copy import deepcopy

from lib.last_day_opening import check_opening, repeated_phrases


def evidence():
    return {'source_sha256': 'a'*64, 'transcript_source_sha256': 'a'*64,
            'actual_audio_transcribed': True, 'window_end_seconds': 60,
            'hook_end_seconds': 12, 'hook_evidence': 'Hook ends after the causal question; next thought defines the premise.',
            'picture_boundaries_seconds': [0, 4, 8, 12, 18],
            'picture_boundary_evidence': 'Observed encoded cuts, frame-exact source selections.',
            'segments': [{'start':0., 'end':12.,
                          'text':'Your feet fall faster than your head. Why can a larger black hole feel safer?'},
                         {'start':12.2, 'end':24.,
                          'text':'Start with gravity across one body. Each part follows a different falling path.'},
                         {'start':44., 'end':58.,
                          'text':'Motion continues through a curved region. Compare the nearby paths while the traveler and the distant observer measure different parts of this one event.'}]}


def test_concise_opening_with_actual_evidence_passes():
    assert check_opening(evidence())['status'] == 'pass'


def test_repeated_phrase_inside_one_returned_take_is_not_hidden_by_full_retention():
    data = evidence()
    data['segments'] = [{'start':0.,'end':30.,'text':
        'But the strangest part is where it happens. But the strangest part is where it happens.'}]
    report = check_opening(data)
    assert report['status'] == 'needs_review'
    assert len(report['unresolved_repeated_phrases']) == 1
    assert report['repeated_phrases'][0]['phrase'] == 'but the strangest part is where it happens'


def test_overlapping_adjacent_take_narration_is_flagged():
    repeated = 'You could cross the point of no return before feeling catastrophic tides.'
    report = repeated_phrases([{'start':16.,'end':26.,'text':repeated},
                               {'start':30.,'end':39.,'text':repeated}])
    assert len(report) == 1
    assert report[0]['first_evidence_seconds'] == [16.,26.]
    assert report[0]['repeat_evidence_seconds'] == [30.,39.]


def test_recurring_short_technical_terms_are_not_a_duplicate_clause():
    assert not repeated_phrases([{'start':0.,'end':12.,'text':
        'The black hole is massive. A black hole curves paths. This black hole has no disk.'}])


def test_negated_claim_is_not_mistaken_for_repeated_affirmative_claim():
    assert not repeated_phrases([{'start':0.,'end':12.,'text':
        'You can escape the event horizon by moving in this direction.'},
        {'start':13.,'end':25.,'text':
        'You cannot escape the event horizon by moving in this direction.'}])


def test_explicit_intentional_callback_can_be_resolved_with_evidence():
    data = evidence()
    phrase = 'The boundary is a change in which futures remain reachable.'
    data['segments'] = [{'start':0.,'end':8.,'text':phrase}, {'start':20.,'end':29.,'text':phrase}]
    data['segments'].append(evidence()['segments'][-1])
    data['repeat_dispositions'] = [{'phrase':phrase, 'reason':'Explicit comparison return.',
                                  'evidence':'Second occurrence is introduced as a quoted callback to the earlier model.'}]
    assert check_opening(data)['status'] == 'pass'
    del data['repeat_dispositions'][0]['evidence']
    assert check_opening(data)['status'] == 'needs_review'


def test_long_hook_and_unbroken_first_picture_are_independent_faults():
    data = evidence()
    data.update(hook_end_seconds=30, picture_boundaries_seconds=[0,17.833333,24,30])
    report = check_opening(data)
    assert report['status'] == 'needs_review'
    assert any('Hook lasts' in issue for issue in report['issues'])
    assert any('First picture shot lasts' in issue for issue in report['issues'])


def test_planned_text_or_hash_mismatch_cannot_establish_actual_opening_pass():
    for change in [{'actual_audio_transcribed':False}, {'transcript_source_sha256':'b'*64},
                   {'segments':[]}, {'segments':[{'start':0,'end':10,'text':'  '}]},
                   {'picture_boundary_evidence':''}, {'hook_evidence':''}]:
        data = deepcopy(evidence())
        data.update(change)
        assert check_opening(data)['status'] == 'needs_review'


def test_short_first_shot_cannot_hide_a_long_second_opening_hold():
    data = evidence()
    data['picture_boundaries_seconds'] = [0, 4, 64]
    report = check_opening(data)
    assert report['status'] == 'needs_review'
    assert any('Opening picture shot lasts 60 seconds' in issue for issue in report['issues'])


def test_picture_boundary_evidence_must_reach_the_whole_hook_window():
    data = evidence()
    data['picture_boundaries_seconds'] = [0, 4, 8, 12]
    assert any('first 15 seconds' in issue for issue in check_opening(data)['issues'])


def test_one_word_stub_cannot_claim_a_full_opening_transcript():
    data = evidence()
    data['segments'] = [{'start':0.,'end':.1,'text':'Oxygen'}]
    assert any('only a stub' in issue for issue in check_opening(data)['issues'])


def test_real_speech_with_a_quiet_middle_gap_remains_valid():
    data = evidence()
    data['segments'] = [data['segments'][0], data['segments'][-1]]
    assert check_opening(data)['status'] == 'pass'
