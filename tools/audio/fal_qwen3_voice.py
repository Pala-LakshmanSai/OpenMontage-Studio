"""Two independent, resumable fal Qwen3 voice jobs: clone then speech."""
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
from tools.audio.fal_zonos2 import cdn_url
from tools.provider_jobs import poll

ROUTES = {'clone': 'fal-ai/qwen-3-tts/clone-voice/1.7b',
          'speech': 'fal-ai/qwen-3-tts/text-to-speech/1.7b'}


def returned_url(url):
    parsed = urlparse(url)
    if (parsed.scheme != 'https' or parsed.username or parsed.password or
            not (parsed.hostname == 'storage.googleapis.com' or parsed.hostname == 'fal.media'
                 or (parsed.hostname or '').endswith('.fal.media'))):
        raise ValueError('invalid provider media host')
    return url


def local_hash(path):
    p = Path(path).resolve()
    if not p.is_file() or not 0 < p.stat().st_size <= 15_000_000:
        raise ValueError('missing or oversized reference')
    return hashlib.sha256(p.read_bytes()).hexdigest()


class FalQwen3Voice(BaseTool):
    name = 'fal_qwen3_voice'
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
    capabilities = ['text_to_speech', 'voice_cloning']
    supports = {'reference_audio': True, 'lip_sync': False}
    side_effects = ['submits one fal queue job', 'writes protected receipt and result']
    input_schema = {'type': 'object', 'required': ['operation', 'job_path', 'output_path'], 'properties': {
        'operation': {'type': 'string', 'enum': ['clone', 'speech']}}}

    def get_status(self):
        return ToolStatus.AVAILABLE if os.getenv('FAL_KEY') else ToolStatus.UNAVAILABLE

    def build_request(self, inputs):
        op = inputs['operation']
        if op == 'clone':
            source = Path(inputs['audio_path']).resolve()
            if local_hash(source) != inputs['audio_sha256']:
                raise ValueError('reference hash mismatch')
            info = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
                'format=duration:stream=codec_type','-of','json',str(source)],text=True))
            if not 0 < float(info['format']['duration']) <= 30 or not any(
                    x.get('codec_type') == 'audio' for x in info['streams']):
                raise ValueError('reference must contain at most 30 seconds of audio')
            payload = {'audio_url': cdn_url(inputs['audio_url'], source.suffix), 'enable_safety_checker': True}
            if inputs.get('reference_text'):
                text = inputs['reference_text']
                if not isinstance(text, str) or len(text) > 300:
                    raise ValueError('invalid reference transcript')
                payload['reference_text'] = text
            return payload
        if op == 'speech':
            text = inputs['text']
            if not isinstance(text, str) or not text.strip() or len(text) > 300:
                raise ValueError('speech text must be a short line')
            if local_hash(inputs['embedding_path']) != inputs['embedding_sha256']:
                raise ValueError('embedding hash mismatch')
            payload = {'text': text, 'language': 'English',
                       'speaker_voice_embedding_file_url': returned_url(inputs['embedding_url']),
                       'enable_safety_checker': True}
            if inputs.get('reference_text'):
                if not isinstance(inputs['reference_text'], str) or len(inputs['reference_text']) > 300:
                    raise ValueError('invalid reference transcript')
                payload['reference_text'] = inputs['reference_text']
            return payload
        raise ValueError('unsupported operation')

    def estimate_cost(self, inputs):
        self.build_request(inputs)
        # Dashboard billed one whole $0.09 character unit for a short line;
        # reserve an additional $0.06 against billing uncertainty.
        return .15 if inputs['operation'] == 'speech' else .05

    def execute(self, inputs):
        key = os.getenv('FAL_KEY')
        if not key:
            return ToolResult(success=False, error='fal credentials unavailable', cost_usd=None)
        try:
            op = inputs['operation']; endpoint = ROUTES[op]; payload = self.build_request(inputs)
            job_path = Path(inputs['job_path']).resolve(); output = Path(inputs['output_path']).resolve()
            fingerprint = hashlib.sha256(json.dumps(payload, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
            if inputs.get('expected_payload_sha256') != fingerprint or output == job_path:
                raise ValueError('payload does not match reservation')
            if job_path.exists():
                receipt = json.loads(job_path.read_text())
                if receipt.get('sha256') != fingerprint or not receipt.get('job', {}).get('request_id'):
                    raise ValueError('acceptance unknown or payload changed; never replay')
            else:
                _write(job_path, {'sha256': fingerprint, 'state': 'submitting'}, exclusive=True)
                submission = request_json('POST', 'https://queue.fal.run/' + endpoint,
                                          headers={'Authorization': 'Key ' + key}, json=payload)
                if not all(submission.get(k) for k in ('request_id', 'status_url', 'response_url')):
                    raise ValueError('missing queue identity')
                receipt = {'sha256': fingerprint, 'state': 'accepted', 'job': {
                    k: submission[k] for k in ('request_id', 'status_url', 'response_url')}}
                _write(job_path, receipt)
            for k in ('status_url', 'response_url'):
                q = urlparse(receipt['job'][k])
                if q.scheme != 'https' or q.netloc != 'queue.fal.run':
                    raise ValueError('invalid queue URL')
            headers = {'Authorization': 'Key ' + key}
            poll(lambda: request_json('GET', receipt['job']['status_url'], headers=headers), timeout=600, interval=2)
            result = request_json('GET', receipt['job']['response_url'], headers=headers)
            url = returned_url(result['speaker_embedding' if op == 'clone' else 'audio']['url'])
            if output.exists():
                raise ValueError('output already exists')
            import requests
            response = requests.get(url, timeout=120, allow_redirects=False, stream=True)
            if 300 <= response.status_code < 400:
                raise ValueError('provider media redirect rejected')
            response.raise_for_status()
            output.parent.mkdir(parents=True, exist_ok=True, mode=0o700)
            artifact = output.with_name(output.name + '.safetensors') if op == 'clone' else output
            tmp = artifact.with_name(artifact.name + '.part')
            with open(tmp, 'xb') as f:
                os.chmod(tmp, 0o600); count = 0
                for block in response.iter_content(chunk_size=65536):
                    count += len(block)
                    if count > (1_000_000 if op == 'clone' else 25_000_000):
                        raise ValueError('provider output exceeds limit')
                    f.write(block)
                f.flush(); os.fsync(f.fileno())
            if count == 0:
                raise ValueError('empty provider output')
            if op == 'speech':
                info = json.loads(subprocess.check_output(['ffprobe','-v','error','-show_entries',
                    'format=duration:stream=codec_type','-of','json',str(tmp)],text=True))
                duration = float(info['format']['duration'])
                if not 0 < duration <= 120 or not any(x.get('codec_type') == 'audio' for x in info['streams']):
                    raise ValueError('invalid speech output')
            os.link(tmp, artifact); tmp.unlink()
            if op == 'clone':
                _write(output, {'request_id': receipt['job']['request_id'], 'embedding_url': url,
                                'embedding_path': str(artifact), 'embedding_sha256': local_hash(artifact)}, exclusive=True)
            return ToolResult(success=True, data={'request_id': receipt['job']['request_id'],
                'output': str(output)}, artifacts=[str(output)], cost_usd=None)
        except Exception as exc:
            return ToolResult(success=False, error=f'Qwen3 voice stopped: {type(exc).__name__}', cost_usd=None)
