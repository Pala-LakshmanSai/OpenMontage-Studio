#!/usr/bin/env python3
"""Export credential-free, discoverable training from a clean public checkout."""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import runpy


BOOTSTRAP = """Use the attached OpenMontage knowledge and production source as this project's canonical training. Read AGENT_GUIDE.md and docs/production-knowledge-index.json first, then the selected style's guide/template/reference notes/playbook and shared policies. Files are delimited by original repository paths. No prior chat, personal memory or original Mac path is required. Current owner instructions and newer canonical rules override old examples.
Read docs/ai-video-action-clarity-and-pacing.md: show consequential decisions and decisive movement clearly, distinguishing voluntary action from accidents in actual selected footage. Preserve necessary continuity while trimming repeated information, idle tails and slow padding. Flexible runtime is not a target expansion. Direct every relevant visible person: inherited posture/task/attention, motivated action and emotional change, including silent or background people. Use necessary readable, film-designed time cues before the first affected scene, with an unambiguous temporal origin and flashback return when needed. Reconcile title promises with the adaptable outline before generation; the owner expects a recognizable multi-headed Leviathan for future title-led Leviathan films unless explicitly different. Plan several consequential gripping developments, without filler or repetitive crises. Custom assembly must honor existing observed narrative coverage; run python -m lib.narrative_continuity path/to/project before a finished-film claim. Do not fabricate observations or certify audiovisual quality from technical checks.
AI Movie and Queen Elizabeth I Style require a reviewed complete revised screenplay through its ending before any new media. Preserve story identity, emotion, curiosity, setups/payoffs and complete ending; add needed causal bridges/agency/reactions and remove repetition. Allow earned flexible runtime within actual authority. Then overlap detailed ready sequences, generation and assembly. Record narrative foundation and actual observed selected coverage, not prompt intent. Other styles retain their own scheduling, art, source and sound contracts.
Keep exact cast/voice/world and irreversible state, natural action, native speech-picture timing, complete utterances and reactions. Actual ordinary shots including internal cuts/screens last at least two seconds. Default full-frame landscape720p/768p, no bars/portrait filler. Raw AI documentary/Primitive Desert uses synchronized activity and ambience with no added music/narrator by default. Preserve all other named-style differences.
Use authorized Frameo Studio/API on disjoint ready sequences under one verified shared capacity ledger, useful30s requests and current exact quotes. Accepted, queued, submitting and uncertain work retains its reservation; never replay it. Verify live entitlement/pricing, preserve project priority and don't buy/renew/top-up/overflow or exceed budget without authority. Prefer Kie-first necessary anchors and settled permitted native voices. Routine paid scoring/review budget is zero. Use cached local technical checks, brief essential review and targeted fault repair without new routine approval gates.
Read the full policies for image/music routes, causal staging, reference roles, exports, filenames, upscales and requested sharing. Deliver regular MP4s to this user's Downloads; retain prior versions. Do not clone creators or fabricate history/reference listening. Technical success does not certify artistic acceptance.
Source context is not installed runtime, media, credentials or provider access. Use only tools actually available. Install the real public repo in an authorized execution environment for production; keep private setup separate. Identify concrete capability gaps and continue independent useful preparation. Never invent jobs, playback, exports, public links, quality parity or speed. Do not generate paid media merely to test setup. Attachments are dated snapshots: safely check public updates and refresh changed files before later work when supported. Save durable feedback in canonical repo policies/templates/index first. Follow docs/claude-project-transfer.md for fresh-chat transfer tests.
Retrieval: zero search results do not establish absence. Directly read relevant numbered parts and adjacent continuations. Helper agents may lack project-file access: the parent must retrieve required missing files itself. Read the active style fully, not all styles for every film. Report public-checkout fallback separately from attachment retrieval. Reconcile shot sums, scene ranges, feasible provider requests and physical elapsed time in the existing plan before generation.
Before presenting a complete screenplay or ready sequence, reconcile the actual means, material elapsed time, final claimed result and shot/scene/request arithmetic once as part of writing. An authorization, attempt or dispatch is not the completed result it enables. Show a necessary completion or keep the claim pending. Physically process clothing/props in a feasible state and allow drying/heating/travel time through legible ellipses. No scene may silently exceed its mapped request duration. This is an internal writing completion check, not a new paid review, owner gate or repeated audit.
Public source: https://github.com/Pala-LakshmanSai/OpenMontage-Studio
"""


def export(root, output):
    root, output = Path(root).resolve(), Path(output).resolve()
    remote = subprocess.check_output(['git', 'remote', 'get-url', 'origin'], cwd=root, text=True).strip()
    if not remote.endswith(('Pala-LakshmanSai/OpenMontage-Studio.git', 'Pala-LakshmanSai/OpenMontage-Studio')):
        raise ValueError('Export from the reviewed public checkout, never private history/configuration')
    if subprocess.check_output(['git', 'status', '--porcelain'], cwd=root).strip():
        raise ValueError('Use a clean reviewed checkout so the source commit is exact')
    commit = subprocess.check_output(['git', 'rev-parse', 'HEAD'], cwd=root, text=True).strip()
    tracked = set(subprocess.check_output(['git', 'ls-files'], cwd=root, text=True).splitlines())
    index = json.loads((root / 'docs/production-knowledge-index.json').read_text())
    knowledge = set(index['policies']) | {'AGENT_GUIDE.md', 'PROJECT_CONTEXT.md',
        'docs/production-knowledge-index.json', 'docs/install-and-update.md', 'docs/claude-project-transfer.md'}
    for style in index['style_profiles']:
        knowledge.update(style[k] for k in ('guide', 'template', 'reference_notes', 'playbook',
            'production_playbook', 'screenplay_foundation', 'story_prompt') if k in style)
    source = {f for f in tracked if f.startswith(('tools/', 'lib/', 'scripts/', 'schemas/',
        'skills/', 'pipeline_defs/', 'styles/')) or ('/' not in f and Path(f).suffix in
        ('.py', '.md', '.toml', '.txt', '.yaml', '.json'))}
    for name in ('ai-video-gen', 'seedance-2-5', 'kie-image', 'j1tts-audio', 'lyria',
                 'fal-lip-sync', 'ffmpeg', 'video-edit', 'video-understand', 'provider-model-refresh', 'hyperframes'):
        path = f'.agents/skills/{name}/SKILL.md'
        if path in tracked:
            source.add(path)
    checked = runpy.run_path(str(root / 'scripts/check_production_knowledge.py'))['check'](root)
    if not checked['passed']:
        raise ValueError('Portable knowledge check failed: ' + '; '.join(checked['errors']))
    source.update(set(checked['file_sha256']) - knowledge)
    manifest = {'source_commit': commit, 'repository': remote, 'personal_memory_required': False,
                'execution_verified': False, 'required_files': sorted(checked['file_sha256']),
                'files': {}, 'outputs': {}}
    output.mkdir(parents=True, exist_ok=True)
    for filename, paths in [('OpenMontage-Production-Knowledge.md', knowledge),
                            ('OpenMontage-Production-Source.md', source)]:
        chunks = [f'# OpenMontage readable repository snapshot\n\nSource commit: {commit}\n'
                  'Original FILE paths follow. Source is knowledge, not installed tools. '
                  'The repository is the executable source; no ZIP attachment is assumed.\n']
        for relative in sorted(paths):
            path = root / relative
            if relative not in tracked or not path.is_file() or path.is_symlink():
                raise ValueError(f'Missing regular tracked source: {relative}')
            raw = path.read_bytes()
            text = raw.decode('utf-8')
            chunks.append(f'\n\n# FILE: {relative}\n\n{text}')
            manifest['files'][relative] = hashlib.sha256(raw).hexdigest()
        # The receiving assistant observed a 262144-byte read cap. Keep every
        # attachment well below that cap; do not rely on search finding a giant file.
        parts, current = [], ''
        for chunk in chunks:
            for line in chunk.splitlines(keepends=True):
                if len((current + line).encode()) > 180000 and current:
                    parts.append(current)
                    current = ''
                while len(line.encode()) > 180000:
                    piece, line = line[:40000], line[40000:]
                    if current:
                        parts.append(current)
                        current = ''
                    parts.append(piece)
                current += line
        if current:
            parts.append(current)
        stem = Path(filename).stem
        for i, part in enumerate(parts, 1):
            name = f'{stem}-{i:02d}.md'
            raw = (f'# {stem} part {i}/{len(parts)}\nSource commit: {commit}\n'
                   'Read adjacent parts when a source file continues across a boundary.\n\n' + part).encode()
            (output / name).write_bytes(raw)
            manifest['outputs'][name] = {'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()}
    (output / 'OpenMontage-Project-Instructions.txt').write_text(BOOTSTRAP + '\nSource commit: ' + commit + '\n')
    (output / 'OpenMontage-Context-Manifest.json').write_text(json.dumps(manifest, indent=2) + '\n')
    return manifest


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', default=Path(__file__).resolve().parents[1])
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    result = export(args.root, args.output)
    print(json.dumps({'source_commit': result['source_commit'], 'files': len(result['files']),
                      'outputs': result['outputs']}, indent=2))
