"""ByteDance Standard 1080p enhancement; source files must be <=250 MiB.

The 262144000-byte provider limit was verified by a definitive HTTP 422 response.
Larger films require separately authorized chunks and distinct durable receipts.
"""
from __future__ import annotations

import hashlib
import json
import math
import os
import subprocess
import tempfile
import time
from pathlib import Path
from urllib.parse import urlparse

import jsonschema
import requests

from tools.base_tool import (BaseTool, ExecutionMode, ResourceProfile, ResumeSupport,
                             ToolResult, ToolRuntime, ToolStability, ToolTier)
from tools.audio.fal_audio_review import _write
from tools.provider_jobs import download

ENDPOINT = "fal-ai/bytedance-upscaler/upscale/video"
SCHEMA_SOURCE = "https://fal.ai/models/fal-ai/bytedance-upscaler/upscale/video/api"
MAX_SOURCE_BYTES = 262144000
OPTIONS = {"target_resolution": "1080p", "target_fps": 24,
           "enhancement_preset": "aigc", "enhancement_tier": "standard",
           "fidelity": "high", "bit_depth": 8}


def _sha(path):
    digest = hashlib.sha256()
    with Path(path).open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class FalBytedanceUpscale(BaseTool):
    name = "fal_bytedance_upscale"
    tier = ToolTier.ENHANCE
    capability = "enhancement"
    capabilities = ["video_upscale"]
    provider = "fal.ai"
    runtime = ToolRuntime.API
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.ASYNC
    resume_support = ResumeSupport.FROM_CHECKPOINT
    dependencies = ["env:FAL_KEY", "cmd:ffprobe", "python:fal_client", "python:filelock"]
    agent_skills = ["ffmpeg"]
    resource_profile = ResourceProfile(network_required=True)
    side_effects = ["uploads source to fal storage", "submits one paid enhancement",
                    "writes private durable receipt and output video"]
    input_schema = {
        "type": "object", "additionalProperties": False,
        "required": ["video_path", "output_path", "job_path"],
        "properties": {
            **{k: {"type": "string", "minLength": 1} for k in
               ["video_path", "output_path", "job_path", "project_dir", "scene_id"]},
            "video_path": {"type": "string", "minLength": 1,
                           "description": "Local source video, at most 262144000 bytes (250 MiB).",
                           "x-max-file-size-bytes": MAX_SOURCE_BYTES},
            "poll_timeout": {"type": "number", "minimum": 0, "default": 40},
            "poll_interval": {"type": "number", "exclusiveMinimum": 0, "default": 5},
            **{k: {"enum": [v], "default": v} for k, v in OPTIONS.items()},
        },
    }

    @staticmethod
    def _probe(path):
        data = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_format", "-show_streams", "-of", "json", str(path)]))
        duration = float(data["format"]["duration"])
        video = next(s for s in data["streams"] if s.get("codec_type") == "video")
        if not math.isfinite(duration) or duration <= 0:
            raise ValueError("Positive finite video duration required")
        return duration, video

    def estimate_cost(self, inputs):
        return self._probe(inputs["video_path"])[0] * .0072

    @staticmethod
    def _upload(path):
        import fal_client
        # The SDK puts the basename into multipart headers, which require ASCII.
        # Keep the source/receipt identity intact without copying the video.
        with tempfile.TemporaryDirectory(prefix="om-fal-") as directory:
            alias = Path(directory) / "input.mp4"
            alias.symlink_to(Path(path).resolve())
            url = fal_client.upload_file(str(alias))
        p = urlparse(url)
        if p.scheme != "https" or not (p.hostname == "fal.media" or (p.hostname or "").endswith(".fal.media")):
            raise ValueError("Unexpected upload host")
        return url

    @staticmethod
    def _request(method, url, **kwargs):
        p = urlparse(url)
        if p.scheme != "https" or p.netloc != "queue.fal.run":
            raise ValueError("Invalid authenticated queue host")
        response = requests.request(method, url,
            headers={"Authorization": "Key " + os.environ["FAL_KEY"]},
            timeout=(15, 120), allow_redirects=False, **kwargs)
        if 300 <= response.status_code < 400:
            raise ValueError("Authenticated redirect refused")
        response.raise_for_status()
        return response.json()

    @staticmethod
    def _validate_job(job):
        rid = job.get("request_id")
        if not isinstance(rid, str) or not rid or any(c not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for c in rid):
            raise ValueError("Invalid saved queue identity")
        for field, suffix in [("status_url", "/status"), ("response_url", "")]:
            p = urlparse(job.get(field, ""))
            paths = {f"/{base}/requests/{rid}{suffix}" for base in
                     ["fal-ai/bytedance-upscaler", ENDPOINT]}
            if p.scheme != "https" or p.netloc != "queue.fal.run" or p.path not in paths or p.query or p.fragment:
                raise ValueError("Saved queue URL differs from accepted identity")

    @staticmethod
    def _public(job):
        return {k: job.get(k) for k in ["request_id", "state", "output_path", "output_sha256",
                                      "estimated_usd", "cost_status", "source_duration_seconds"]}

    def execute(self, inputs):
        started = time.monotonic()
        job = {}
        receipt = None
        lock = None
        try:
            jsonschema.validate(inputs, self.input_schema)
            self.check_dependencies()
            from filelock import FileLock
            source, output, receipt = [Path(inputs[k]).resolve() for k in
                                       ["video_path", "output_path", "job_path"]]
            if len({source, output, receipt, output.with_name(output.name + ".part")}) != 4:
                raise ValueError("Source, output, receipt and download temporary paths must differ")
            lock_path = receipt.with_name(receipt.name + ".lock")
            if lock_path in {source, output, output.with_name(output.name + ".part")}:
                raise ValueError("Receipt lock must preserve source and output")
            receipt.parent.mkdir(parents=True, exist_ok=True)
            lock = FileLock(str(lock_path), timeout=0, mode=0o600)
            lock.acquire()
            if not source.is_file() or not source.stat().st_size:
                raise ValueError("Nonempty source video required")
            duration, _ = self._probe(source)
            spec = {"endpoint": ENDPOINT, "options": OPTIONS, "source_sha256": _sha(source),
                    "source_duration_seconds": duration, "output_path": str(output)}
            fingerprint = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
            if receipt.exists():
                job = json.loads(receipt.read_text())
                if job.get("input_sha256") != fingerprint:
                    raise ValueError("Saved inputs changed; preserve accepted work")
                if job.get("state") == "failed":
                    raise ValueError("Saved task failed; no automatic replay")
                if job.get("state") == "submitting" and not job.get("request_id"):
                    raise ValueError("Acceptance unknown; reconcile fal history, never replay")
                if job.get("state") == "completed" and output.is_file() and _sha(output) == job.get("output_sha256"):
                    return ToolResult(success=True, data=self._public(job), artifacts=[str(output), str(receipt)], cost_usd=0)
            else:
                if output.exists():
                    raise ValueError("Unrelated output exists; preserve it")
                job = {**spec, "tool": self.name, "input_sha256": fingerprint,
                       "state": "uploading", "estimated_usd": duration * .0072,
                       "cost_status": "estimate_not_invoice", "created_at": time.time()}
                _write(receipt, job, exclusive=True)
            if not job.get("request_id"):
                if job.get("state") not in {"uploading", "uploaded"}:
                    raise ValueError("Acceptance unknown; reconcile fal history, never replay")
                # Accepted jobs remain resumable; reject oversized new submissions
                # even when a prior invocation already uploaded their source.
                if source.stat().st_size > MAX_SOURCE_BYTES:
                    raise ValueError("Source exceeds 262144000-byte (250 MiB) provider limit; split before submission")
                if not job.get("video_url"):
                    job.update(video_url=self._upload(source), state="uploaded")
                    _write(receipt, job)
                if _sha(source) != spec["source_sha256"]:
                    raise ValueError("Source changed during upload; no submission made")
                job.update(state="submitting", submitted_at=time.time())
                _write(receipt, job)
                accepted = self._request("POST", "https://queue.fal.run/" + ENDPOINT,
                                         json={**OPTIONS, "video_url": job["video_url"]})
                # Persist any returned identity before validation/polling. Never lose acceptance.
                job.update({k: accepted[k] for k in ["request_id", "status_url", "response_url"] if accepted.get(k)})
                job.update(state="accepted", accepted_at=time.time())
                _write(receipt, job)
            self._validate_job(job)
            deadline = time.monotonic() + inputs.get("poll_timeout", 40)
            while True:
                state = self._request("GET", job["status_url"])
                if state.get("request_id", job["request_id"]) != job["request_id"]:
                    raise ValueError("Provider request identity differs")
                job["provider_status"] = state.get("status")
                if state.get("error") or str(state.get("status", "")).upper() in {"FAILED", "CANCELLED", "CANCELED", "ERROR"}:
                    job["state"] = "failed"; _write(receipt, job)
                    raise ValueError("Provider task failed; preserve receipt")
                _write(receipt, job)
                if str(state.get("status", "")).upper() == "COMPLETED":
                    break
                if time.monotonic() >= deadline:
                    return ToolResult(success=False, data=self._public(job), error="Known task pending; resume exact receipt", cost_usd=None)
                time.sleep(min(inputs.get("poll_interval", 5), max(0, deadline - time.monotonic())))
            result = self._request("GET", job["response_url"])
            job.update(state="downloading", provider_result=result)
            _write(receipt, job)
            download(result["video"]["url"], output)
            out_duration, video = self._probe(output)
            if abs(out_duration - duration) > .25 or (video.get("width"), video.get("height")) != (1920, 1080):
                raise ValueError("Returned output requires duration/resolution inspection; do not resubmit")
            job.update(state="completed", output_sha256=_sha(output), completed_at=time.time(),
                       output_bytes=output.stat().st_size, billing_duration_reported=result.get("duration"))
            _write(receipt, job)
            return ToolResult(success=True, data=self._public(job), artifacts=[str(output), str(receipt)],
                              cost_usd=None, model=ENDPOINT, duration_seconds=time.monotonic()-started)
        except Exception as exc:
            if (isinstance(exc, requests.HTTPError) and exc.response is not None
                    and exc.response.status_code in {402, 422} and receipt and job):
                code = exc.response.status_code
                job.update(state="failed", failure_http_status=code,
                           failure="provider_payment_required" if code == 402 else "provider_validation_rejected")
                _write(receipt, job)
            # Raw HTTP/upload exceptions may contain signed URLs. Keep them out of event logs.
            safe = {"Positive finite video duration required", "Unexpected upload host",
                    "Invalid authenticated queue host", "Authenticated redirect refused",
                    "Invalid saved queue identity", "Saved queue URL differs from accepted identity",
                    "Source, output, receipt and download temporary paths must differ",
                    "Receipt lock must preserve source and output", "Nonempty source video required",
                    "Saved inputs changed; preserve accepted work", "Saved task failed; no automatic replay",
                    "Acceptance unknown; reconcile fal history, never replay", "Unrelated output exists; preserve it",
                    "Source changed during upload; no submission made", "Provider request identity differs",
                    "Source exceeds 262144000-byte (250 MiB) provider limit; split before submission",
                    "Provider task failed; preserve receipt",
                    "Returned output requires duration/resolution inspection; do not resubmit"}
            message = str(exc) if type(exc) is ValueError and str(exc) in safe else type(exc).__name__
            return ToolResult(success=False, data=self._public(job), error=message,
                              cost_usd=None, duration_seconds=time.monotonic()-started)
        finally:
            if lock is not None:
                lock.release()
