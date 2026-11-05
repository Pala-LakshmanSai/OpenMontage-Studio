"""Validate portable instruction routing with only Python's standard library."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path


def check(root: Path) -> dict:
    root = root.resolve()
    errors = []
    index_path = root / 'docs/production-knowledge-index.json'
    try:
        index = json.loads(index_path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as exc:
        return {'passed': False, 'errors': [f'Knowledge index unavailable: {type(exc).__name__}']}
    paths = set(index['entrypoints'] + index['policies'] + index['shared_capabilities'])
    paths.update([index['installation'], 'INSTALL.md', 'docs/production-knowledge-index.json',
                  'scripts/check_production_knowledge.py', 'scripts/install_openmontage.py',
                  'requirements.txt', 'requirements-production-constraints.txt', '.env.example',
                  'remotion-composer/package.json', 'remotion-composer/package-lock.json'])
    for style in index['style_profiles']:
        paths.update(style[k] for k in ('guide', 'template', 'reference_notes', 'playbook',
                                      'production_playbook', 'screenplay_foundation',
                                      'story_prompt') if k in style)
        paths.add(style['pipeline'])
        for key in ('guide', 'template'):
            path = root / style[key]
            if path.is_file():
                text = path.read_text(encoding='utf-8')
                for policy in ('video-fast-production-preferences.md', 'ai-video-human-performance-preferences.md'):
                    if policy not in text:
                        errors.append(f'{style[key]} does not inherit {policy}')
        foundation = style.get('screenplay_foundation')
        if foundation:
            for relative in (style['guide'], style['template'], style['playbook'], 'AGENT_GUIDE.md',
                             'skills/pipelines/cinematic/script-director.md',
                             'skills/pipelines/cinematic/scene-director.md',
                             'skills/pipelines/cinematic/asset-director.md',
                             'skills/pipelines/cinematic/edit-director.md',
                             'skills/pipelines/cinematic/compose-director.md'):
                paths.add(relative)
                path = root / relative
                if path.is_file() and Path(foundation).name not in path.read_text(encoding='utf-8'):
                    errors.append(f'{relative} does not route to {style["name"]} screenplay foundation')
    narrative = index.get('ai_movie_narrative_contract', {})
    for key in ('guide', 'validator', 'example', 'tests'):
        if key not in narrative:
            errors.append(f'Missing portable AI Movie narrative contract {key}')
        else:
            paths.add(narrative[key])
    for relative in ('AGENT_GUIDE.md', 'docs/ai-movie-preferences.md',
                     'docs/ai-movie-prompt-template.md', 'styles/ai-movie.yaml',
                     'skills/pipelines/cinematic/script-director.md',
                     'skills/pipelines/cinematic/executive-producer.md',
                     'skills/pipelines/cinematic/proposal-director.md',
                     'pipeline_defs/cinematic.yaml',
                     'skills/pipelines/cinematic/asset-director.md',
                     'skills/pipelines/cinematic/edit-director.md'):
        path = root / relative
        paths.add(relative)
        if path.is_file() and 'ai-movie-screenplay-foundation.md' not in path.read_text(encoding='utf-8'):
            errors.append(f'{relative} does not route to AI Movie screenplay foundation')
    hashes = {}
    for relative in sorted(paths):
        path = root / relative
        if Path(relative).is_absolute() or '..' in Path(relative).parts:
            errors.append(f'Nonportable manifest path: {relative}')
        elif not path.is_file():
            errors.append(f'Missing file: {relative}')
        else:
            hashes[relative] = hashlib.sha256(path.read_bytes()).hexdigest()
    for relative in index['entrypoints']:
        path = root / relative
        if path.is_file() and relative != 'AGENT_GUIDE.md':
            if 'AGENT_GUIDE.md' not in path.read_text(encoding='utf-8'):
                errors.append(f'{relative} does not route to AGENT_GUIDE.md')
    guide = (root / 'AGENT_GUIDE.md').read_text(encoding='utf-8')
    for name in ('portable-production-knowledge.md', 'production-knowledge-index.json', 'install-and-update.md'):
        if name not in guide:
            errors.append(f'Agent guide does not route to {name}')
    for path in sorted((root / 'styles').glob('*.yaml')):
        text = path.read_text(encoding='utf-8')
        for name in ('video-fast-production-preferences.md', 'ai-video-human-performance-preferences.md'):
            if name not in text:
                errors.append(f'{path.name} does not inherit {name}')
    return {'passed': not errors, 'errors': errors, 'style_profiles': len(index['style_profiles']),
            'playbooks': len(list((root / 'styles').glob('*.yaml'))),
            'shared_policies': len(index['policies']), 'required_files': len(paths),
            'file_sha256': hashes, 'personal_memory_required': False,
            'provider_calls': 0, 'scope': 'Instruction routing and files; not audiovisual quality or other-device execution.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    result = check(args.root)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, indent=2) + '\n', encoding='utf-8')
    print(json.dumps({k: v for k, v in result.items() if k != 'file_sha256'}, indent=2))
    raise SystemExit(0 if result['passed'] else 1)


if __name__ == '__main__':
    main()
