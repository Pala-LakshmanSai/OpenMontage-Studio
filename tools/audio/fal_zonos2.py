"""Bounded fal Zonos2 offscreen speech with durable queue identity."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from tools.base_tool import (BaseTool, Determinism, ExecutionMode, ResourceProfile,
                             ResumeSupport, ToolResult, ToolRuntime, ToolStability,
                             ToolStatus, ToolTier)
from tools.audio.fal_audio_review import _write, request_json
from tools.provider_jobs import poll

ENDPOINT = 'fal-ai/zonos2'


def cdn_url(url, suffix=None):
    p = urlparse(url)
    host = p.hostname or ''
    if (p.scheme != 'https' or p.username or p.password or
            not (host == 'fal.media' or host.endswith('.fal.media')) or
            (suffix is not None and not p.path.lower().endswith(suffix.lower()))):
        raise ValueError('invalid fal CDN URL')
    return url


class FalZonos2(BaseTool):
    name = 'fal_zonos2'
    capability = 'audio_generation'
    provider = 'fal.ai'
    tier = ToolTier.GENERATE
    runtime = ToolRuntime.API
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.ASYNC
    determinism = Determinism.STOCHASTIC
    resume_support = ResumeSupport.FROM_CHECKPOINT
    dependencies = ['env:FAL_KEY', 'cmd:ffprobe']
    resource_profile = ResourceProfile(network_required=True)
    capabilities = ['text_to_speech']
    supports = {'reference_audio': True, 'lip_sync': False}
    side_effects = ['submits one potentially paid fal job', 'writes audio and protected receipt']
    input_schema = {'type': 'object', 'required': ['text', 'audio_path', 'audio_url', 'audio_sha256', 'job_path', 'output_path'], 'properties': {'accurate_mode': {'type': 'boolean', 'default': True}}}

    def get_status(self):
        return ToolStatus.AVAILABLE if os.getenv('FAL_KEY') else ToolStatus.UNAVAILABLE

    def build_request(self, inputs):
        text = inputs['text']
        if not isinstance(text, str) or not text.strip() or len(text) > 300:
            raise ValueError('one short speech line of at most 300 characters required')
        source = Path(inputs['audio_path']).resolve()
        if not source.is_file() or source.stat().st_size == 0 or source.stat().st_size > 15_000_000:
            raise ValueError('invalid reference audio')
        if hashlib.sha256(source.read_bytes()).hexdigest() != inputs['audio_sha256']:
            raise ValueError('reference hash mismatch')
        info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
            'format=duration:stream=codec_type', '-of', 'json', str(source)], text=True))
        if not 0 < float(info['format']['duration']) <= 30 or not any(
                stream.get('codec_type') == 'audio' for stream in info['streams']):
            raise ValueError('reference must contain up to 30 seconds of audio')
        url = cdn_url(inputs['audio_url'], source.suffix)
        accurate_mode = inputs.get('accurate_mode', True)
        if type(accurate_mode) is not bool:
            raise ValueError('accurate_mode must be boolean')
        return {'reference_audio_url': url, 'text': text, 'language': 'en_us',
                'accurate_mode': accurate_mode, 'max_tokens': 1000, 'enable_safety_checker': True}

    def estimate_cost(self, inputs):
        self.build_request(inputs)
        return .05

    def execute(self, inputs):
        key = os.getenv('FAL_KEY')
        if not key:
            return ToolResult(success=False, error='fal credentials unavailable', cost_usd=None)
        try:
            payload = self.build_request(inputs)
            job_path = Path(inputs['job_path']).resolve()
            output = Path(inputs['output_path']).resolve()
            source = Path(inputs['audio_path']).resolve()
            if len({job_path, output, source}) != 3 or output.suffix.lower() != '.wav':
                raise ValueError('invalid output or receipt path')
            fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            if inputs.get('expected_payload_sha256') != fingerprint:
                raise ValueError('payload does not match reservation')
            if job_path.exists():
                receipt = json.loads(job_path.read_text())
                if receipt.get('sha256') != fingerprint or not receipt.get('job', {}).get('request_id'):
                    raise ValueError('acceptance unknown or payload changed; never replay')
            else:
                _write(job_path, {'sha256': fingerprint, 'state': 'submitting'}, exclusive=True)
                response = request_json('POST', 'https://queue.fal.run/' + ENDPOINT,
                                        headers={'Authorization': 'Key ' + key}, json=payload)
                if not all(response.get(k) for k in ('request_id', 'status_url', 'response_url')):
                    raise ValueError('missing acceptance identity')
                receipt = {'sha256': fingerprint, 'state': 'accepted', 'job': {
                    k: response[k] for k in ('request_id', 'status_url', 'response_url')}}
                _write(job_path, receipt)
            for name in ('status_url', 'response_url'):
                p = urlparse(receipt['job'][name])
                if p.scheme != 'https' or p.netloc != 'queue.fal.run':
                    raise ValueError('invalid queue URL')
            headers = {'Authorization': 'Key ' + key}
            poll(lambda: request_json('GET', receipt['job']['status_url'], headers=headers), timeout=600, interval=2)
            result = request_json('GET', receipt['job']['response_url'], headers=headers)
            url = cdn_url(result['audio']['url'])
            if output.exists():
                raise ValueError('output already exists')
            import requests
            response = requests.get(url, timeout=120, allow_redirects=False, stream=True)
            if 300 <= response.status_code < 400:
                raise ValueError('media redirect rejected')
            response.raise_for_status()
            output.parent.mkdir(parents=True, exist_ok=True)
            tmp = output.with_name(output.name + '.part')
            with open(tmp, 'xb') as f:
                count = 0
                for chunk in response.iter_content(chunk_size=65536):
                    count += len(chunk)
                    if count > 25_000_000:
                        raise ValueError('audio exceeds limit')
                    f.write(chunk)
                f.flush(); os.fsync(f.fileno())
            info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error', '-show_entries',
                'format=duration:stream=codec_type', '-of', 'json', str(tmp)], text=True))
            duration = float(info['format']['duration'])
            if duration > 120:
                return ToolResult(success=False, error='Audio exceeded reserved duration; reconcile billing',
                                  data={'billing_reconciliation_required': True}, cost_usd=None)
            if not 0 < duration or not any(x.get('codec_type') == 'audio' for x in info['streams']):
                raise ValueError('unexpected audio duration or format; reconcile billing')
            os.link(tmp, output)
            tmp.unlink()
            return ToolResult(success=True, data={'request_id': receipt['job']['request_id'],
                'output': str(output), 'duration_seconds': duration}, artifacts=[str(output)], cost_usd=None)
        except Exception as exc:
            return ToolResult(success=False, error=f'Zonos2 stopped: {type(exc).__name__}', cost_usd=None)
