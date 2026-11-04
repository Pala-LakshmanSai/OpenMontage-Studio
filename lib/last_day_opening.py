"""Bounded local opening evidence check; consumes cached ASR, never runs it.

This flags exact repeated substantial phrases, not semantic duplicates or voice
quality. Segment timestamps locate evidence; they are not word-accurate cut points.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
from pathlib import Path
import re

VERSION = 1
MIN_REPEAT_WORDS = 8
_WORD = re.compile(r"[\w]+(?:['’][\w]+)*", re.UNICODE)
_NEGATIONS = {"not", "no", "never", "cannot", "can't", "won't", "don't", "doesn't",
              "didn't", "isn't", "aren't", "wasn't", "weren't", "without"}


class LastDayOpeningError(ValueError):
    """Actual opening evidence is missing, stale or unresolved."""


def _words(text):
    return [m.group().lower().replace('’', "'") for m in _WORD.finditer(text)]


def _number(value):
    return isinstance(value, (int, float)) and not isinstance(value, bool) and math.isfinite(value)


def repeated_phrases(segments):
    """Find nearby disjoint exact repeats without stripping meaning/negation."""
    tokens, spans, negations = [], [], []
    for segment in segments:
        for clause in re.split(r'[.!?;:]+', segment['text']):
            words = _words(clause)
            signature = tuple(word for word in words if word in _NEGATIONS)
            tokens.extend(words)
            spans.extend([(segment['start'], segment['end'])] * len(words))
            negations.extend([signature] * len(words))
    seen, candidates = {}, []
    for right in range(len(tokens) - MIN_REPEAT_WORDS + 1):
        key = tuple(tokens[right:right + MIN_REPEAT_WORDS])
        for left in seen.get(key, []):
            if right - left < MIN_REPEAT_WORDS or spans[right][0] - spans[left][1] > 35:
                continue
            # An unchanged tail inside opposing claims is not a repeated claim.
            if negations[left] != negations[right]:
                continue
            length = MIN_REPEAT_WORDS
            while (left + length < right and right + length < len(tokens)
                   and tokens[left + length] == tokens[right + length]):
                length += 1
            candidates.append((left, right, length))
        seen.setdefault(key, []).append(right)
    selected = []
    for left, right, length in sorted(candidates, key=lambda x: -x[2]):
        if any(a <= left and left + length <= a + n and
               b <= right and right + length <= b + n for a, b, n in selected):
            continue
        selected.append((left, right, length))
    return [{'phrase': ' '.join(tokens[right:right + length]), 'word_count': length,
             'first_evidence_seconds': [spans[left][0], spans[left + length - 1][1]],
             'repeat_evidence_seconds': [spans[right][0], spans[right + length - 1][1]]}
            for left, right, length in sorted(selected)]


def check_opening(data):
    """Check supplied actual evidence. Missing evidence cannot produce a pass."""
    issues = []
    source_hash = data.get('source_sha256', '')
    if (not isinstance(source_hash, str) or not re.fullmatch(r'[0-9a-f]{64}', source_hash)
            or data.get('transcript_source_sha256') != source_hash
            or data.get('actual_audio_transcribed') is not True):
        issues.append('Actual opening audio and matching source/transcript SHA256 evidence required.')
    window = data.get('window_end_seconds')
    if not _number(window) or not 60 <= window <= 90:
        issues.append('Declare a bounded actual opening transcript window of 60–90 seconds.')
    hook = data.get('hook_end_seconds')
    if not _number(hook) or hook <= 0 or not data.get('hook_evidence'):
        issues.append('Observed hook endpoint and passage/transition evidence required.')
    elif hook > 15:
        issues.append(f'Hook lasts {hook:g} seconds; move into the premise/mechanism by 15 seconds.')
    boundaries = data.get('picture_boundaries_seconds', [])
    if (not isinstance(boundaries, list) or len(boundaries) < 2
            or any(not _number(x) for x in boundaries) or boundaries[0] != 0
            or any(b <= a for a, b in zip(boundaries, boundaries[1:]))
            or not data.get('picture_boundary_evidence')):
        issues.append('Actual opening picture boundaries and observation/scan evidence required.')
    elif boundaries[1] > 6:
        issues.append(f'First picture shot lasts {boundaries[1]:g} seconds; opening coverage should develop within 2–6 seconds.')
    elif boundaries[1] < 2:
        issues.append('First picture shot is shorter than the actual two-second minimum.')
    segments = data.get('segments', [])
    valid = isinstance(segments, list) and bool(segments)
    prior = -1
    if valid:
        for segment in segments:
            if (not isinstance(segment, dict) or not isinstance(segment.get('text'), str)
                    or not _number(segment.get('start')) or not _number(segment.get('end'))
                    or not 0 <= segment['start'] < segment['end']
                    or segment['start'] < prior
                    or (_number(window) and segment['end'] > window + .05)):
                valid = False
                break
            prior = segment['start']
    if valid and not any(_words(segment['text']) for segment in segments):
        valid = False
    if not valid:
        issues.append('Nonempty timestamped actual transcript segments within the declared window required.')
    repeats = repeated_phrases(segments) if valid else []
    dispositions = data.get('repeat_dispositions') or []
    accepted = {' '.join(_words(d['phrase'])) for d in dispositions
                if isinstance(d, dict) and isinstance(d.get('phrase'), str)
                and d.get('reason') and d.get('evidence')}
    unresolved = [repeat for repeat in repeats if repeat['phrase'] not in accepted]
    if unresolved:
        issues.append('Substantial repeated nearby narration needs removal or explicit intentional-callback evidence.')
    return {'checker_version': VERSION, 'status': 'needs_review' if issues else 'pass',
            'source_sha256': source_hash, 'window_end_seconds': window,
            'hook_end_seconds': hook, 'repeated_phrases': repeats,
            'unresolved_repeated_phrases': unresolved, 'issues': issues,
            'scope': 'Supplied cached actual opening transcript and observed timing only; no ASR/provider calls, semantic-duplicate proof, word-accurate cut points or whole-film certification.'}


def validate_render_opening(project, render_report, *, metadata=None):
    """Bind a passing pure check to the actual MP4 bytes; never invoke ASR."""
    if not isinstance(render_report, dict):
        raise LastDayOpeningError('The Last Day opening check requires a render_report.')
    render_metadata = render_report.get('metadata') or {}
    if not isinstance(render_metadata, dict) or (metadata is not None and not isinstance(metadata, dict)):
        raise LastDayOpeningError('The Last Day opening metadata must be a JSON object.')
    options = {**render_metadata, **(metadata or {})}
    evidence_path = options.get('last_day_opening_check_input')
    if not isinstance(evidence_path, str) or not evidence_path.strip():
        raise LastDayOpeningError('The Last Day compose completion requires last_day_opening_check_input evidence.')
    path = Path(evidence_path)
    if not path.is_absolute():
        path = Path(project) / path
    try:
        data = json.loads(path.read_text(encoding='utf-8'))
        if not isinstance(data, dict):
            raise ValueError('Opening evidence must be a JSON object')
        report = check_opening(data)
    except (OSError, ValueError, TypeError, KeyError, AttributeError):
        raise LastDayOpeningError('The Last Day opening input is missing or invalid; no pass recorded.') from None
    if report['status'] != 'pass':
        raise LastDayOpeningError('The Last Day opening check needs review: ' + '; '.join(report['issues']))
    raw_outputs = render_report.get('outputs')
    if not isinstance(raw_outputs, list):
        raise LastDayOpeningError('The Last Day opening check requires actual MP4 outputs.')
    outputs = [output for output in raw_outputs
               if isinstance(output, dict) and
               (str(output.get('format', '')).lower() == 'mp4' or
                Path(str(output.get('path', ''))).suffix.lower() == '.mp4')]
    if not outputs:
        raise LastDayOpeningError('The Last Day opening check requires an actual MP4 output.')
    for output in outputs:
        video = Path(output.get('path') or '')
        if not video.is_absolute():
            video = Path(project) / video
        try:
            if not video.is_file() or not video.stat().st_size:
                raise ValueError('Missing MP4')
            hasher = hashlib.sha256()
            with video.open('rb') as source:
                for block in iter(lambda: source.read(1024 * 1024), b''):
                    hasher.update(block)
            digest = hasher.hexdigest()
        except (OSError, ValueError):
            raise LastDayOpeningError('The Last Day MP4 is missing or unreadable; no opening pass recorded.') from None
        if digest != data['source_sha256']:
            raise LastDayOpeningError('The Last Day opening evidence source_sha256 does not match the actual MP4 output.')
    return report


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('input', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    raw = args.input.read_bytes()
    identity = hashlib.sha256(raw).hexdigest()
    result = check_opening(json.loads(raw))
    result['input_sha256'] = identity
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))
    raise SystemExit(0 if result['status'] == 'pass' else 2)


if __name__ == '__main__':
    main()
