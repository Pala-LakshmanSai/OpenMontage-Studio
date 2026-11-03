"""Portable routing and private-install preservation without network or generation."""
import importlib.util
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]


def load_script(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_relocated_knowledge_without_personal_memory(tmp_path):
    checker = load_script('check_production_knowledge')
    original = checker.check(ROOT)
    assert original['passed'], original['errors']
    # Copy regular training/source files only into a different path. No home,
    # personal memory, mounted SSD, provider credentials or network is copied.
    for relative in original['file_sha256']:
        target = tmp_path / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, target)
    for source in (ROOT / 'styles').glob('*.yaml'):
        target = tmp_path / 'styles' / source.name
        target.parent.mkdir(exist_ok=True)
        shutil.copyfile(source, target)
    result = checker.check(tmp_path)
    assert result['passed'], result['errors']
    assert result['style_profiles'] == 6 and result['playbooks'] == 10
    (tmp_path / 'docs/primitive-desert-style-preferences.md').unlink()
    broken = checker.check(tmp_path)
    assert not broken['passed']
    assert any('primitive-desert' in error for error in broken['errors'])


def test_private_environment_preserves_local_values_and_refresh_is_explicit():
    installer = load_script('install_openmontage')
    old = '# local\nFAL_KEY=local-value\nKIE_API_KEY=\n'
    incoming = 'FAL_KEY=owner-value\nKIE_API_KEY=owner-image\nJ1TTS_API_KEY=owner-voice\n'
    merged = installer.merge_environment(old, incoming)
    assert 'FAL_KEY=local-value' in merged
    assert 'KIE_API_KEY=owner-image' in merged
    assert 'J1TTS_API_KEY=owner-voice' in merged
    assert merged.count('FAL_KEY=') == 1
    refreshed = installer.merge_environment(old, incoming, replace=True)
    assert 'FAL_KEY=owner-value' in refreshed


def test_private_asset_installs_only_named_files_and_local_key_path(tmp_path, monkeypatch, capsys):
    installer = load_script('install_openmontage')
    home = tmp_path / 'friend-home'
    home.mkdir()
    root = tmp_path / 'repo'
    root.mkdir()
    monkeypatch.setattr(installer.shutil, 'which', lambda name: '/fake/gh')
    monkeypatch.setattr(installer.Path, 'home', lambda: home)

    def download(command, **kwargs):
        destination = Path(command[command.index('--dir') + 1]) / installer.PRIVATE_ASSET
        with zipfile.ZipFile(destination, 'w') as archive:
            archive.writestr('provider.env', 'FAL_KEY=test-secret-do-not-print\n')
            archive.writestr('frameo-api-key', 'workspace-secret-do-not-print')
            archive.writestr('../outside', 'must never extract arbitrary archive paths')

    monkeypatch.setattr(installer.subprocess, 'run', download)
    installer.private_setup(root)
    text = (root / '.env').read_text()
    assert 'test-secret-do-not-print' in text
    assert (home / '.config/openmontage/frameo-api-key').read_text() == 'workspace-secret-do-not-print'
    assert (home / '.config/openmontage/frameo-api-key').as_posix() in text
    assert not (tmp_path / 'outside').exists()
    assert 'secret-do-not-print' not in capsys.readouterr().out


def test_saved_resolution_matches_fallback_defaults():
    from lib.config_model import OpenMontageConfig
    for config in (OpenMontageConfig(), OpenMontageConfig.load(ROOT / 'config.yaml')):
        assert config.output.default_resolution == '1280x720'
        assert config.output.default_fps == 24


def test_local_private_setup_needs_no_github_access(tmp_path, monkeypatch):
    installer = load_script('install_openmontage')
    root = tmp_path / 'repo'
    root.mkdir()
    bundle = tmp_path / 'provided.zip'
    with zipfile.ZipFile(bundle, 'w') as archive:
        archive.writestr('provider.env', 'KIE_API_KEY=local-provided-secret\n')
    monkeypatch.setattr(installer.shutil, 'which', lambda name: None)
    monkeypatch.setattr(installer.subprocess, 'run', lambda *a, **kw: (_ for _ in ()).throw(AssertionError('No network allowed')))
    installer.private_setup(root, archive_path=bundle)
    assert 'KIE_API_KEY=local-provided-secret' in (root / '.env').read_text()
