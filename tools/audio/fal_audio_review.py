"""Durable, bounded AI audio review using fal's OpenRouter queue endpoint."""
from __future__ import annotations

import base64
import hashlib
import json
import os
import subprocess
import tempfile
from decimal import Decimal, ROUND_CEILING
from pathlib import Path
from urllib.parse import urlparse

from tools.base_tool import (BaseTool, Determinism, ExecutionMode, ResourceProfile,
                             ResumeSupport, ToolResult, ToolRuntime, ToolStability,
                             ToolStatus, ToolTier)
from tools.provider_jobs import poll

MODEL = 'google/gemini-3.8-flash'
ENDPOINT = 'openrouter/router/audio'
SYSTEM = ('You are an AI audio reviewer, not a human listener. Report uncertainty, '
          'timestamps when possible, intelligibility, artifacts, acoustic continuity '
          'and unwanted vocals. Do not claim lip synchronization can be verified from audio.')


def request_json(method, url, **kwargs):
    import requests
    response = requests.request(method, url, timeout=60, allow_redirects=False, **kwargs)
    if 300 <= response.status_code < 400:
        raise ValueError('authenticated redirect rejected')
    response.raise_for_status()
    return response.json()


def _write(path, obj, *, exclusive=False):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
    if exclusive:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY, 0o600)
        with os.fdopen(fd, 'w') as f:
            json.dump(obj, f, sort_keys=True)
            f.flush()
            os.fsync(f.fileno())
    else:
        fd, tmp = tempfile.mkstemp(dir=path.parent, prefix='.fal-audio-')
        try:
            os.fchmod(fd, 0o600)
            with os.fdopen(fd, 'w') as f:
                json.dump(obj, f, sort_keys=True)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp):
                os.unlink(tmp)
    fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class FalAudioReview(BaseTool):
    name = 'fal_audio_review'
    capability = 'analysis'
    provider = 'fal.ai'
    tier = ToolTier.ANALYZE
    runtime = ToolRuntime.API
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.ASYNC
    determinism = Determinism.STOCHASTIC
    resume_support = ResumeSupport.FROM_CHECKPOINT
    dependencies = ['env:FAL_KEY', 'cmd:ffprobe']
    resource_profile = ResourceProfile(network_required=True)
    capabilities = ['ai_audio_review']
    supports = {'audio_input': True, 'human_listening': False}
    agent_skills = ['video-understand']
    side_effects = ['submits one potentially paid fal job', 'writes analysis and protected receipt']
    user_visible_verification = ['Disclose AI assessment and its limits; verify measured usage']
    input_schema = {'type': 'object', 'required': ['audio_path', 'prompt', 'job_path', 'output_path'],
                    'properties': {'audio_path': {'type': 'string'}, 'prompt': {'type': 'string'},
                                   'job_path': {'type': 'string'}, 'output_path': {'type': 'string'}}}

    def get_status(self):
        return ToolStatus.AVAILABLE if os.getenv('FAL_KEY') else ToolStatus.UNAVAILABLE

    def build_request(self, inputs):
        prompt = inputs['prompt']
        if not isinstance(prompt, str) or not prompt.strip() or len(prompt.encode()) > 4096:
            raise ValueError('prompt must be nonempty and at most 4096 UTF-8 bytes')
        path = Path(inputs['audio_path']).resolve()
        mime = {'.wav': 'audio/wav', '.mp3': 'audio/mpeg', '.aiff': 'audio/aiff',
                '.aac': 'audio/aac', '.ogg': 'audio/ogg', '.flac': 'audio/flac',
                '.m4a': 'audio/mp4'}.get(path.suffix.lower())
        if not mime or not path.is_file() or not 0 < path.stat().st_size <= 30_000_000:
            raise ValueError('audio must be a supported nonempty local file under 30 MB')
        info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
            '-show_entries', 'format=duration:stream=codec_type', '-of', 'json', str(path)], text=True))
        duration = Decimal(str(info['format']['duration']))
        if not duration.is_finite() or not Decimal(0) < duration <= Decimal(1300):
            raise ValueError('audio duration must be positive and no more than 1300 seconds')
        if not any(s.get('codec_type') == 'audio' for s in info['streams']):
            raise ValueError('file contains no audio stream')
        raw = path.read_bytes()
        audio_url = 'data:' + mime + ';base64,' + base64.b64encode(raw).decode()
        if inputs.get('audio_url'):
            parsed = urlparse(inputs['audio_url'])
            host = parsed.hostname or ''
            if (parsed.scheme != 'https' or parsed.username or parsed.password or
                    not (host == 'fal.media' or host.endswith('.fal.media')) or
                    not parsed.path.lower().endswith(path.suffix.lower())):
                raise ValueError('hosted audio must be an extension-matched fal CDN HTTPS URL')
            if inputs.get('audio_sha256') != hashlib.sha256(raw).hexdigest():
                raise ValueError('hosted audio source hash mismatch')
            audio_url = inputs['audio_url']
        payload = {'audio_url': audio_url,
                   'prompt': prompt, 'system_prompt': SYSTEM, 'model': MODEL,
                   'max_tokens': 8192, 'enable_web_search': False, 'reasoning': True}
        # Priority list rates, max output, 32 audio tokens/sec, 8192 text/overhead
        # tokens, and 25% margin. Quote/usage reconciliation remains mandatory.
        reserve = (((duration * 32 + 8192) * Decimal('2.70') +
                    Decimal(8192) * Decimal('13.50')) / 1_000_000 * Decimal('1.25')
                   ).quantize(Decimal('.01'), rounding=ROUND_CEILING)
        return payload, reserve

    def estimate_cost(self, inputs):
        return float(self.build_request(inputs)[1])

    def execute(self, inputs):
        key = os.getenv('FAL_KEY')
        if not key:
            return ToolResult(success=False, error='fal credentials unavailable', cost_usd=None)
        try:
            payload, reserve = self.build_request(inputs)
            job_path, output = Path(inputs['job_path']).resolve(), Path(inputs['output_path']).resolve()
            if job_path == output or job_path == Path(inputs['audio_path']).resolve() or output == Path(inputs['audio_path']).resolve():
                raise ValueError('job and output paths must not overwrite the input')
            fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            if inputs.get('expected_payload_sha256') and inputs['expected_payload_sha256'] != fingerprint:
                raise ValueError('payload changed after reservation; refusing submit')
            if job_path.exists():
                receipt = json.loads(job_path.read_text())
                if receipt.get('sha256') != fingerprint:
                    raise ValueError('saved inputs differ; refusing replay')
                if not receipt.get('job', {}).get('request_id'):
                    raise ValueError('acceptance unknown; reconcile before any replay')
            else:
                _write(job_path, {'sha256': fingerprint, 'state': 'submitting'}, exclusive=True)
                submission = request_json('POST', 'https://queue.fal.run/' + ENDPOINT,
                                          headers={'Authorization': 'Key ' + key}, json=payload)
                if not all(submission.get(k) for k in ('request_id', 'status_url', 'response_url')):
                    raise ValueError('missing queue identity; reconcile before any replay')
                receipt = {'sha256': fingerprint, 'state': 'accepted', 'job': {
                    k: submission[k] for k in ('request_id', 'status_url', 'response_url')}}
                _write(job_path, receipt)
            for k in ('status_url', 'response_url'):
                p = urlparse(receipt['job'][k])
                if p.scheme != 'https' or p.netloc != 'queue.fal.run':
                    raise ValueError('invalid queue URL')
            headers = {'Authorization': 'Key ' + key}
            poll(lambda: request_json('GET', receipt['job']['status_url'], headers=headers),
                 timeout=600, interval=2)
            result = request_json('GET', receipt['job']['response_url'], headers=headers)
            if not isinstance(result.get('output'), str) or not isinstance(result.get('usage'), dict):
                raise ValueError('completed review lacks output or usage')
            if output.exists():
                raise ValueError('output already exists; preserve it')
            _write(output, {'kind': 'AI audio assessment, not human listening',
                            'model': MODEL, 'output': result['output'], 'usage': result['usage']},
                   exclusive=True)
            return ToolResult(success=True, data={'request_id': receipt['job']['request_id'],
                'output': str(output), 'usage': result['usage'], 'reservation_usd': str(reserve)},
                artifacts=[str(output)], cost_usd=None, model=MODEL)
        except Exception as exc:
            # Never return authentication values, URLs or inline media in error text.
            return ToolResult(success=False, error=f'Audio review stopped: {type(exc).__name__}', cost_usd=None)
