"""Install the repository and optional owner-authorized private API setup."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import venv
import zipfile

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_REPO = 'Pala-LakshmanSai/OpenMontage'
PRIVATE_TAG = 'owner-private-setup'
PRIVATE_ASSET = 'openmontage-private-setup.zip'


def run(command, *, cwd=ROOT):
    subprocess.run([str(x) for x in command], cwd=cwd, check=True)


def merge_environment(existing: str, incoming: str, *, replace=False) -> str:
    """Preserve local values by default; retain exact values without logging them."""
    lines = existing.splitlines()
    positions = {}
    for i, line in enumerate(lines):
        if '=' in line and not line.lstrip().startswith('#'):
            positions[line.split('=', 1)[0].strip()] = i
    for line in incoming.splitlines():
        if '=' not in line or line.lstrip().startswith('#'):
            continue
        key, value = line.split('=', 1)
        key = key.strip()
        if not key or not value.strip():
            continue
        if key in positions:
            i = positions[key]
            old = lines[i].split('=', 1)[1].strip()
            if replace or not old:
                lines[i] = key + '=' + value
        else:
            positions[key] = len(lines)
            lines.append(key + '=' + value)
    return '\n'.join(lines) + '\n'


def private_setup(root: Path, *, refresh=False, archive_path: Path | None = None):
    if archive_path is None and not shutil.which('gh'):
        raise RuntimeError('Private setup needs GitHub CLI authenticated with access to the private repository.')
    with tempfile.TemporaryDirectory(prefix='openmontage-private-') as temporary:
        # Capture diagnostics: neither archive contents nor credential values enter logs.
        if archive_path is not None:
            shutil.copyfile(archive_path, Path(temporary) / PRIVATE_ASSET)
        else:
            subprocess.run(['gh', 'release', 'download', PRIVATE_TAG, '--repo', PRIVATE_REPO,
                            '--pattern', PRIVATE_ASSET, '--dir', temporary],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
        with zipfile.ZipFile(Path(temporary) / PRIVATE_ASSET) as archive:
            incoming = archive.read('provider.env').decode('utf-8')
            frameo = archive.read('frameo-api-key') if 'frameo-api-key' in archive.namelist() else None
        target = root / '.env'
        old = target.read_text(encoding='utf-8') if target.exists() else ''
        if refresh and target.exists():
            backups = root / '.private-config'
            backups.mkdir(exist_ok=True)
            shutil.copy2(target, backups / ('env-' + datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')))
        if frameo:
            directory = Path.home() / '.config/openmontage'
            directory.mkdir(parents=True, exist_ok=True)
            key_file = directory / 'frameo-api-key'
            if refresh or not key_file.exists():
                key_file.write_bytes(frameo)
                key_file.chmod(0o600)
            # This is a receiving-device path, never the publisher's Mac path.
            incoming += '\nFRAMEO_API_KEY_FILE=' + json.dumps(key_file.as_posix()) + '\n'
        text = merge_environment(old, incoming, replace=refresh)
        fd, temporary_env = tempfile.mkstemp(prefix='.env.install-', dir=root)
        try:
            with os.fdopen(fd, 'w', encoding='utf-8') as handle:
                handle.write(text)
            os.chmod(temporary_env, 0o600)
            os.replace(temporary_env, target)
        finally:
            Path(temporary_env).unlink(missing_ok=True)
    print('Authorized private provider setup installed; values are not displayed.')


def readiness(root: Path) -> dict:
    env_python = root / '.venv' / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    return {'python_compatible': sys.version_info >= (3, 10),
            'commands': {name: bool(shutil.which(name)) for name in ('git', 'node', 'npm', 'ffmpeg', 'ffprobe')},
            'environment_python': env_python.is_file(),
            'composer_installed': (root / 'remotion-composer/node_modules/remotion').is_dir(),
            'private_environment_present': (root / '.env').is_file()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check', action='store_true', help='Local readiness only; no install or provider calls.')
    parser.add_argument('--with-private-config', action='store_true')
    parser.add_argument('--private-config', type=Path, help='Owner-supplied local setup ZIP; no per-key entry.')
    parser.add_argument('--refresh-private-config', action='store_true')
    args = parser.parse_args()
    state = readiness(ROOT)
    if args.check:
        run([sys.executable, ROOT / 'scripts/check_production_knowledge.py'])
        print(json.dumps(state, indent=2))
        raise SystemExit(0 if state['python_compatible'] and all(state['commands'].values())
                         and state['environment_python'] and state['composer_installed'] else 1)
    if not state['python_compatible']:
        raise SystemExit('Python3.10 or newer is required.')
    missing = [name for name, ready in state['commands'].items() if not ready]
    if missing:
        raise SystemExit('Install missing system prerequisites through the platform package manager: ' + ', '.join(missing))
    environment = ROOT / '.venv'
    python = environment / ('Scripts/python.exe' if os.name == 'nt' else 'bin/python')
    if not python.exists():
        venv.EnvBuilder(with_pip=True).create(environment)
    run([python, '-m', 'pip', 'install', '-r', ROOT / 'requirements.txt'])
    npm = shutil.which('npm')
    # Explicit executable works on Windows without depending on a Unix make shell.
    if os.name == 'nt' and npm and npm.lower().endswith('.cmd'):
        run([os.environ.get('COMSPEC', 'cmd.exe'), '/d', '/c', 'npm', 'install'], cwd=ROOT / 'remotion-composer')
    else:
        run([npm, 'install'], cwd=ROOT / 'remotion-composer')
    if args.with_private_config or args.refresh_private_config or args.private_config:
        private_setup(ROOT, refresh=args.refresh_private_config, archive_path=args.private_config)
    elif not (ROOT / '.env').exists():
        shutil.copyfile(ROOT / '.env.example', ROOT / '.env')
        (ROOT / '.env').chmod(0o600)
    run([python, ROOT / 'scripts/check_production_knowledge.py'])
    run([python, '-c', 'from tools.tool_registry import registry; registry.discover(); print("Registered production tools discovered; no generation started.")'])
    print('Install complete. Open this repository in Codex and request a saved style, title and length.')


if __name__ == '__main__':
    try:
        main()
    except subprocess.CalledProcessError:
        raise SystemExit('Setup command failed; private diagnostics suppressed. Preserve current files and resolve access/dependencies before resuming.')
