"""Narrow Kie Seedance2.5 recovery with fixed cost and durable no-replay receipts.

30s/720p/16:9/native audio only, using one measured2s original video reference.
Local reference transport reuses Kie's existing authorized upload client. A
private receipt and lock fence every paid createTask; no submission is retried.
"""
from __future__ import annotations

from fractions import Fraction
import hashlib
import html
import json
import math
import os
from pathlib import Path
import re
import subprocess
import tempfile
import time
import uuid

from filelock import FileLock
import jsonschema
import requests
from PIL import Image

from tools.base_tool import BaseTool, ExecutionMode, ResourceProfile, ResumeSupport, RetryPolicy, ToolResult, ToolRuntime, ToolStability, ToolStatus, ToolTier
from tools.graphics.kie_image import KieAPIError, KieImage
from tools.provider_jobs import download


class KieSeedanceVideo(BaseTool):
    name = 'kie_seedance_video'
    version = '0.1.0'
    capability = 'video_generation'
    provider = 'kie'
    tier = ToolTier.GENERATE
    runtime = ToolRuntime.API
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.ASYNC
    dependencies = ['env:KIE_API_KEY', 'python:requests', 'python:jsonschema', 'python:filelock']
    install_instructions = 'Use the existing authorized private Kie API credential; no automatic purchase or account setup.'
    agent_skills = ['seedance-2-5', 'kie-image']
    capabilities = ['reference_to_video', 'native_audio', 'durable_resume']
    supports = {'reference_image': True, 'multiple_reference_images': True, 'reference_video': True, 'reference_audio': True, 'native_audio': True}
    retry_policy = RetryPolicy(max_retries=0)
    resume_support = ResumeSupport.FROM_CHECKPOINT
    resource_profile = ResourceProfile(cpu_cores=1, ram_mb=512, disk_mb=500, network_required=True)
    side_effects = ['uploads local references', 'creates paid Kie task once', 'writes private receipt and downloaded video']
    MODEL = 'bytedance/seedance-2-5'
    PRICE_PAGE = 'https://kie.ai/seedance-2-5'
    EXPECTED_CREDITS = 1216
    EXPECTED_USD = 6.08
    input_schema = {'type': 'object', 'additionalProperties': False,
        'required': ['output_path', 'job_path'], 'properties': {
            'prompt': {'type': 'string', 'minLength': 1, 'maxLength': 20000},
            'model': {'const': MODEL}, 'duration_seconds': {'const': 30},
            'resolution': {'const': '720p'}, 'aspect_ratio': {'const': '16:9'}, 'generate_audio': {'const': True},
            'reference_image_paths': {'type': 'array', 'minItems': 1, 'maxItems': 30, 'items': {'type': 'string'}},
            'reference_audio_paths': {'type': 'array', 'minItems': 1, 'maxItems': 10, 'items': {'type': 'string'}},
            'reference_video_path': {'type': 'string'},
            'output_path': {'type': 'string'}, 'job_path': {'type': 'string'},
            'project_dir': {'type': 'string'}, 'scene_id': {'type': 'string'},
            'max_cost_usd': {'type': 'number', 'minimum': 0, 'maximum': 6.08},
            'remaining_budget_usd': {'type': 'number', 'minimum': 0, 'maximum': 19.68},
            'poll_timeout': {'type': 'number', 'minimum': 0}, 'poll_interval': {'type': 'number', 'exclusiveMinimum': 0}}}

    def get_status(self):
        return ToolStatus.AVAILABLE if os.environ.get('KIE_API_KEY') else ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs):
        return self.EXPECTED_USD

    @staticmethod
    def _hash(path):
        value = hashlib.sha256()
        with Path(path).open('rb') as stream:
            for block in iter(lambda: stream.read(1024 * 1024), b''):
                value.update(block)
        return value.hexdigest()

    @staticmethod
    def _save(path, job):
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, temporary = tempfile.mkstemp(prefix='.kie-video-', dir=path.parent)
        try:
            with os.fdopen(fd, 'w') as stream:
                os.fchmod(stream.fileno(), 0o600)
                json.dump(job, stream, indent=2); stream.flush(); os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            Path(temporary).unlink(missing_ok=True)

    @staticmethod
    def _probe(path):
        result = subprocess.run(['ffprobe', '-v', 'error', '-show_format', '-show_streams', '-of', 'json', str(path)], capture_output=True, text=True)
        if result.returncode:
            raise ValueError('Media probe failed; no paid submission')
        return json.loads(result.stdout)

    def prepare_spec(self, inputs):
        """Pure local validation/hash preparation, with no uploads or HTTP."""
        jsonschema.validate(inputs, self.input_schema)
        if not inputs.get('prompt') or not inputs.get('reference_image_paths') or not inputs.get('reference_audio_paths') or not inputs.get('reference_video_path') or not inputs.get('project_dir'):
            raise ValueError('New task requires prompt, original image/audio/video references and project_dir')
        references = {'images': [], 'audios': [], 'video': []}
        audio_seconds = 0
        for kind, paths in [('images', inputs['reference_image_paths']), ('audios', inputs['reference_audio_paths']), ('video', [inputs['reference_video_path']])]:
            for raw in paths:
                path = Path(raw).expanduser().resolve()
                limit = {'images': 30, 'audios': 15, 'video': 200}[kind] * 1024 * 1024
                if not path.is_file() or not 0 < path.stat().st_size <= limit:
                    raise ValueError('Local reference missing or exceeds media size limit')
                if kind == 'images':
                    with Image.open(path) as image:
                        if image.format not in ['JPEG', 'PNG', 'WEBP'] or not all(300 <= side <= 6000 for side in image.size):
                            raise ValueError('Reference image format/dimensions invalid')
                        image.verify()
                else:
                    info = self._probe(path)
                    if kind == 'video':
                        video = next(row for row in info['streams'] if row['codec_type'] == 'video')
                        if Fraction(video['r_frame_rate']) != 24 or int(video.get('nb_frames', 0)) != 48 or (video['width'], video['height']) != (1280, 720):
                            raise ValueError('Video reference must be exactly48native24fps frames at720p (2seconds)')
                        if abs(float(info['format']['duration']) - 2) > 0.001:
                            raise ValueError('Reference container duration must be exactly2seconds for bounded billing')
                    else:
                        if path.suffix.lower() not in ['.wav', '.mp3'] or not any(row['codec_type'] == 'audio' for row in info['streams']):
                            raise ValueError('Original voice reference must be WAV/MP3 audio')
                        duration = float(info['format']['duration'])
                        if not 2 <= duration <= 30:
                            raise ValueError('Audio reference must be2–30seconds')
                        audio_seconds += duration
                references[kind].append({'path': str(path), 'sha256': self._hash(path)})
        if audio_seconds > 30:
            raise ValueError('Combined voice references exceed30seconds')
        return {'model': self.MODEL, 'prompt': inputs['prompt'], 'references': references,
                'duration': 30, 'resolution': '720p', 'aspect_ratio': '16:9', 'generate_audio': True}

    def _request(self, method, url, **kwargs):
        return KieImage()._request(method, url, **kwargs)

    def _upload(self, reference):
        return KieImage()._upload(reference)

    def _price_preflight(self, inputs):
        limits = [float(inputs.get(key, 0)) for key in ['max_cost_usd', 'remaining_budget_usd']]
        if not all(math.isfinite(value) and value >= 0 for value in limits) or self.EXPECTED_USD > min(limits) + 1e-8:
            raise ValueError('Expected task cost exceeds explicit remaining budget')
        response = requests.get(self.PRICE_PAGE, timeout=30)
        response.raise_for_status()
        page = re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', response.text)))
        if not re.search(r'720[Pp].{0,120}38\s*credits/s\s*\(\$0\.190/s,\s*with video\)', page):
            raise ValueError('Live official720p with-video rate is not confirmed38credits/s; no paid submission')
        credits = self._request('GET', 'https://api.kie.ai/api/v1/chat/credit')
        if isinstance(credits, bool) or not isinstance(credits, (int, float)) or not math.isfinite(credits) or credits < self.EXPECTED_CREDITS:
            raise ValueError('Existing Kie credits do not cover expected task; no purchase permitted')
        return {'url': self.PRICE_PAGE, 'credits_per_second': 38, 'reference_video_seconds': 2,
                'output_seconds': 30, 'quoted_credits': self.EXPECTED_CREDITS, 'quoted_usd': self.EXPECTED_USD,
                'balance_before': credits, 'checked_at': time.time()}

    @staticmethod
    def _safe(job):
        return {key: job[key] for key in ['provider', 'model', 'state', 'task_id', 'output_path', 'output_sha256',
            'input_sha256', 'quoted_credits', 'quoted_usd', 'reported_credits', 'unexpected_charge', 'failure_code',
            'duration_seconds', 'frames', 'fps', 'width', 'height'] if key in job}

    def execute(self, inputs):
        started = time.monotonic(); job = {}; new_submission = False
        try:
            jsonschema.validate(inputs, self.input_schema)
            output = Path(inputs['output_path']).expanduser().resolve()
            receipt = Path(inputs['job_path']).expanduser().resolve()
            receipt.parent.mkdir(parents=True, exist_ok=True)
            with FileLock(str(receipt) + '.lock', timeout=0):
                if receipt.exists():
                    job = json.loads(receipt.read_text())
                    if job.get('provider') != 'kie' or job.get('model') != self.MODEL or job.get('output_path') != str(output):
                        raise ValueError('Saved provider/model/output mismatch; preserve receipt')
                spec = self.prepare_spec(inputs) if 'prompt' in inputs else None
                spec_hash = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest() if spec else None
                if job and spec_hash and job.get('input_sha256') != spec_hash:
                    raise ValueError('Saved input mismatch; accepted or uncertain task must not change')
                if job.get('state') in ['failed', 'submission_refused']:
                    raise ValueError('Terminal Kie task/refusal preserved; do not replay')
                if job and not job.get('task_id') and job.get('state') != 'preparing':
                    raise ValueError('Submission acceptance unresolved; do not replay')
                if output.exists():
                    expected_hash = job.get('output_sha256') or job.get('download_sha256')
                    if not expected_hash or self._hash(output) != expected_hash:
                        raise ValueError('Existing output hash mismatch or unowned output; preserve file')
                    job.update(state='succeeded', output_sha256=expected_hash)
                    self._save(receipt, job)
                    return ToolResult(success=True, data={**self._safe(job), 'new_paid_submission': False}, cost_usd=0, artifacts=[str(output), str(receipt)])
                if not job.get('task_id'):
                    if spec is None:
                        raise ValueError('New task requires complete frozen inputs')
                    from lib.narrative_continuity import validate_foundation
                    project = Path(inputs['project_dir'])
                    validate_foundation(project, json.loads((project / 'artifacts/script.json').read_text()))
                    quote = self._price_preflight(inputs)
                    if not job:
                        job = {'provider': 'kie', 'model': self.MODEL, 'state': 'preparing',
                            'input_sha256': spec_hash, 'spec': spec, 'output_path': str(output),
                            'local_idempotency_key': str(uuid.uuid4()), 'uploaded_references': {}, **quote}
                        self._save(receipt, job)
                    refs = {}
                    for kind, descriptors in spec['references'].items():
                        refs[kind] = []
                        for descriptor in descriptors:
                            identity = descriptor['sha256']
                            url = job['uploaded_references'].get(identity)
                            if not url:
                                url = self._upload(descriptor)
                                KieImage._https(url)
                                job['uploaded_references'][identity] = url; self._save(receipt, job)
                            refs[kind].append(url)
                    payload = {'model': self.MODEL, 'input': {key: spec[key] for key in ['prompt', 'duration', 'resolution', 'aspect_ratio', 'generate_audio']}}
                    payload['input'].update(reference_image_urls=refs['images'], reference_audio_urls=refs['audios'], reference_video_urls=refs['video'], output_format='mp4')
                    # Unknown acceptance is durable BEFORE the sole paid POST.
                    job.update(state='acceptance_unknown', payload=payload, submission_started_at=time.time(), **quote)
                    self._save(receipt, job)
                    try:
                        accepted = self._request('POST', 'https://api.kie.ai/api/v1/jobs/createTask', json=payload)
                    except KieAPIError as error:
                        if error.code in [400, 401, 402, 403, 404, 422]:
                            job.update(state='submission_refused', failure_code=error.code); self._save(receipt, job)
                        raise
                    task_id = accepted.get('taskId') if isinstance(accepted, dict) else None
                    if not isinstance(task_id, str) or not re.fullmatch(r'[A-Za-z0-9_-]{1,160}', task_id):
                        raise ValueError('No confirmed task ID; acceptance remains unresolved, do not replay')
                    new_submission = True; job.update(task_id=task_id, state='queued', accepted_at=time.time()); self._save(receipt, job)
                deadline = time.monotonic() + float(inputs.get('poll_timeout', 0))
                while True:
                    data = self._request('GET', 'https://api.kie.ai/api/v1/jobs/recordInfo', params={'taskId': job['task_id']})
                    if not isinstance(data, dict) or data.get('taskId') != job['task_id'] or data.get('model') != self.MODEL:
                        raise ValueError('Provider task/model identity mismatch')
                    state = data.get('state')
                    if state not in ['waiting', 'queuing', 'generating', 'success', 'fail']:
                        raise ValueError('Unknown task state; resume the exact accepted task')
                    job.update(provider_state=state, state={'waiting': 'queued', 'queuing': 'queued', 'generating': 'running', 'success': 'succeeded', 'fail': 'failed'}[state])
                    credits = data.get('creditsConsumed')
                    if type(credits) in [int, float] and math.isfinite(credits) and credits >= 0:
                        job['reported_credits'] = credits
                        job['unexpected_charge'] = credits > self.EXPECTED_CREDITS
                    self._save(receipt, job)
                    if state == 'fail':
                        job['failure_code'] = data.get('failCode'); self._save(receipt, job)
                        raise ValueError('Kie generation failed; terminal task preserved, do not replay')
                    if state == 'success':
                        try:
                            result = json.loads(data['resultJson']) if isinstance(data.get('resultJson'), str) else data.get('resultJson')
                            urls = result.get('resultUrls') if isinstance(result, dict) else None
                        except (ValueError, KeyError):
                            raise ValueError('Invalid result JSON; resume exact accepted task') from None
                        if not isinstance(urls, list) or len(urls) != 1:
                            raise ValueError('Expected one video result; resume exact accepted task')
                        url = KieImage._https(urls[0]); temporary = output.with_name(output.name + '.download')
                        download(url, temporary)
                        info = self._probe(temporary); video = next(row for row in info['streams'] if row['codec_type'] == 'video')
                        if (video['width'], video['height']) != (1280, 720) or Fraction(video['r_frame_rate']) != 24 or not any(row['codec_type'] == 'audio' for row in info['streams']):
                            raise ValueError('Downloaded result is not native720p24 video with audio; preserve exact task')
                        frames = int(video['nb_frames'])
                        if not 29.5 <= frames / 24 <= 30.5:
                            raise ValueError('Downloaded result duration does not match30second request')
                        job.update(download_sha256=self._hash(temporary), width=1280, height=720, fps=24, frames=frames, duration_seconds=frames / 24)
                        self._save(receipt, job); output.parent.mkdir(parents=True, exist_ok=True); temporary.replace(output)
                        job.update(output_sha256=job['download_sha256'], completed_at=time.time()); self._save(receipt, job)
                        return ToolResult(success=True, data={**self._safe(job), 'new_paid_submission': new_submission}, cost_usd=self.EXPECTED_USD if new_submission else 0, artifacts=[str(output), str(receipt)], model=self.MODEL)
                    if time.monotonic() >= deadline:
                        return ToolResult(success=False, data={**self._safe(job), 'new_paid_submission': new_submission}, error='Known Kie task pending; resume exact receipt', cost_usd=self.EXPECTED_USD if new_submission else 0, model=self.MODEL)
                    time.sleep(min(float(inputs.get('poll_interval', 5)), max(0, deadline - time.monotonic())))
        except Exception as error:
            message = ('Kie video input schema invalid' if isinstance(error, jsonschema.ValidationError)
                       else str(error) if type(error) in [ValueError, KieAPIError] else 'Kie video ' + type(error).__name__)
            message = message.replace(os.environ.get('KIE_API_KEY') or '\0', '[REDACTED]')
            return ToolResult(success=False, error=message, data=self._safe(job), cost_usd=None, duration_seconds=time.monotonic() - started)
