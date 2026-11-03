"""Durable audiovisual reference review through fal's documented video router."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path
from urllib.parse import urlparse

from tools.base_tool import (BaseTool, ToolResult, ToolStatus, ToolTier, ToolRuntime,
                             ToolStability, ResourceProfile, ResumeSupport)
from tools.audio.fal_audio_review import _write, request_json
from tools.provider_jobs import poll

MODEL = 'google/gemini-3.8-flash'
ENDPOINT = 'openrouter/router/video'
SCHEMA_SOURCE = 'https://fal.ai/models/openrouter/router/video/api'
SYSTEM = ('You are an AI audiovisual reviewer, not a human viewer. Review actual '
          'video and audio together, report timecoded evidence, uncertainty and '
          'coverage limits. Never infer sounds from pictures or title alone.')


class FalVideoReview(BaseTool):
    name = 'fal_video_review'
    capability = 'analysis'
    provider = 'fal.ai'
    tier = ToolTier.ANALYZE
    runtime = ToolRuntime.API
    stability = ToolStability.BETA
    resource_profile = ResourceProfile(network_required=True)
    resume_support = ResumeSupport.FROM_CHECKPOINT
    dependencies = ['env:FAL_KEY', 'cmd:ffprobe', 'python:fal_client']
    agent_skills = ['video-understand', 'provider-model-refresh']
    capabilities = ['ai_audiovisual_review']
    supports = {'video_input': True, 'audio_input': True, 'human_viewing': False}
    side_effects = ['uploads source video to fal storage', 'submits paid analysis',
                    'writes protected receipt and assessment']
    input_schema = {'type': 'object', 'required': ['video_path', 'prompt', 'job_path', 'output_path'],
                    'properties': {k: {'type': 'string'} for k in
                                   ('video_path', 'prompt', 'job_path', 'output_path')}}

    def get_status(self):
        return ToolStatus.AVAILABLE if os.getenv('FAL_KEY') else ToolStatus.UNAVAILABLE

    def build_request(self, inputs):
        path = Path(inputs['video_path']).resolve()
        prompt = inputs['prompt']
        if not isinstance(prompt, str) or not prompt.strip() or len(prompt.encode()) > 12000:
            raise ValueError('prompt must be nonempty and at most 12000 UTF-8 bytes')
        if path.suffix.lower() not in ('.mp4', '.mpeg', '.mov', '.webm') or not path.is_file():
            raise ValueError('supported local video required')
        # fal inlines the hosted file for AI Studio. Its 20 MB body ceiling
        # includes base64 expansion, so reject oversize media before spending.
        if not 0 < path.stat().st_size <= 14_000_000:
            raise ValueError('video must be nonempty and under 14 MB for provider body limit')
        info = json.loads(subprocess.check_output(['ffprobe', '-v', 'error',
            '-show_entries', 'format=duration:stream=codec_type', '-of', 'json', str(path)], text=True))
        duration = float(info['format']['duration'])
        if not 0 < duration <= 1800:
            raise ValueError('duration must be positive and no more than 1800 seconds')
        if not {'video', 'audio'} <= {s.get('codec_type') for s in info['streams']}:
            raise ValueError('audiovisual review requires video and audio streams')
        payload = {'prompt': prompt, 'system_prompt': SYSTEM, 'model': MODEL,
                   'max_tokens': 16000, 'reasoning': True, 'temperature': 0.1,
                   'enable_web_search': False}
        identity = {'source_sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
                    'duration_seconds': duration, 'payload': payload}
        return payload, identity

    def estimate_cost(self, inputs):
        # Conservative planning reserve, not a price quote or spending cap.
        self.build_request(inputs)
        return 2.0

    def execute(self, inputs):
        if not os.getenv('FAL_KEY'):
            return ToolResult(success=False, error='fal credentials unavailable', cost_usd=None)
        try:
            payload, identity = self.build_request(inputs)
            path = Path(inputs['video_path']).resolve()
            job_path, output = Path(inputs['job_path']).resolve(), Path(inputs['output_path']).resolve()
            if len({path, job_path, output}) != 3:
                raise ValueError('input, job and output paths must differ')
            fingerprint = hashlib.sha256(json.dumps(identity, sort_keys=True).encode()).hexdigest()
            if output.exists():
                return ToolResult(success=False, error='assessment already exists; preserve it', cost_usd=None)
            if job_path.exists():
                receipt = json.loads(job_path.read_text())
                if receipt.get('sha256') != fingerprint:
                    raise ValueError('saved inputs differ; refusing replay')
                if receipt.get('state') == 'submitting' and not receipt.get('job'):
                    raise ValueError('acceptance unknown; reconcile before any replay')
            else:
                _write(job_path, {'sha256': fingerprint, 'state': 'uploading',
                                 'identity': identity}, exclusive=True)
                receipt = json.loads(job_path.read_text())
            if not receipt.get('video_url'):
                import fal_client
                receipt['video_url'] = fal_client.upload_file(str(path))
                p = urlparse(receipt['video_url'])
                if p.scheme != 'https' or not (p.hostname or '').endswith('.fal.media'):
                    raise ValueError('unexpected media host')
                receipt['state'] = 'uploaded'
                _write(job_path, receipt)
            if not receipt.get('job'):
                payload['video_urls'] = [receipt['video_url']]
                receipt['state'] = 'submitting'
                _write(job_path, receipt)
                submission = request_json('POST', 'https://queue.fal.run/' + ENDPOINT,
                    headers={'Authorization': 'Key ' + os.environ['FAL_KEY']}, json=payload)
                if not all(submission.get(k) for k in ('request_id', 'status_url', 'response_url')):
                    raise ValueError('queue identity missing; do not replay')
                receipt['job'] = {k: submission[k] for k in ('request_id', 'status_url', 'response_url')}
                receipt['state'] = 'accepted'
                _write(job_path, receipt)
            for k in ('status_url', 'response_url'):
                p = urlparse(receipt['job'][k])
                if p.scheme != 'https' or p.netloc != 'queue.fal.run':
                    raise ValueError('invalid queue host')
            headers = {'Authorization': 'Key ' + os.environ['FAL_KEY']}
            poll(lambda: request_json('GET', receipt['job']['status_url'], headers=headers),
                 timeout=900, interval=3)
            result = request_json('GET', receipt['job']['response_url'], headers=headers)
            if not isinstance(result.get('output'), str) or not isinstance(result.get('usage'), dict):
                raise ValueError('review lacks output or usage')
            _write(output, {'kind': 'AI audiovisual assessment, not direct human viewing',
                'model': MODEL, 'endpoint': ENDPOINT, 'source_sha256': identity['source_sha256'],
                'source_duration_seconds': identity['duration_seconds'],
                'output': result['output'], 'usage': result['usage']}, exclusive=True)
            return ToolResult(success=True, data={'output_path': str(output), 'usage': result['usage'],
                'request_id': receipt['job']['request_id']}, artifacts=[str(output)],
                cost_usd=None, model=MODEL)
        except Exception as exc:
            return ToolResult(success=False, error=f'Video review stopped: {type(exc).__name__}', cost_usd=None)
