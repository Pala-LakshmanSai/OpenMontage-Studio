"""Fixed J1TTS performances on generated footage, with durable fal acceptance."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import time
from pathlib import Path
from urllib.parse import urlparse

import jsonschema
import requests

from tools.base_tool import (BaseTool, Determinism, ExecutionMode, ResourceProfile,
                             ResumeSupport, ToolResult, ToolRuntime, ToolStability,
                             ToolTier, ToolStatus)
from tools.provider_jobs import download, save_job


class FalLipSync(BaseTool):
    name = "fal_lip_sync"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "avatar"
    provider = "fal.ai"
    runtime = ToolRuntime.API
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.ASYNC
    determinism = Determinism.STOCHASTIC
    dependencies = ["env:FAL_KEY", "cmd:ffprobe", "python:fal_client"]
    install_instructions = "Configure FAL_KEY using https://fal.ai/dashboard/keys; pip install fal-client."
    agent_skills = ["fal-lip-sync"]
    capabilities = ["lip_sync", "audio_video_alignment"]
    resume_support = ResumeSupport.FROM_CHECKPOINT
    resource_profile = ResourceProfile(network_required=True)
    side_effects = ["submits one paid lip-sync job", "writes video and durable receipt"]
    user_visible_verification = ["Check every speaking face against the supplied audio"]
    input_schema = {
        "type": "object", "additionalProperties": False,
        "required": ["video_path", "audio_path", "output_path", "job_path"],
        "properties": {
            **{k: {"type": "string", "minLength": 1} for k in
               ["video_path", "audio_path", "output_path", "job_path", "project_dir", "scene_id"]},
            "poll_timeout": {"type": "number", "exclusiveMinimum": 0},
            "poll_interval": {"type": "number", "exclusiveMinimum": 0},
        },
    }
    _ENDPOINT = "fal-ai/sync-lipsync/v2/pro"

    def get_status(self):
        from importlib.util import find_spec
        return ToolStatus.AVAILABLE if os.getenv("FAL_KEY") and find_spec("fal_client") else ToolStatus.UNAVAILABLE

    @staticmethod
    def _upload(path):
        import fal_client
        url = fal_client.upload_file(str(path))
        parsed = urlparse(url)
        if parsed.scheme != "https" or not (parsed.hostname == "fal.media" or (parsed.hostname or "").endswith(".fal.media")):
            raise ValueError("Invalid fal CDN upload URL")
        return url

    @staticmethod
    def _duration(path):
        data = json.loads(subprocess.check_output([
            "ffprobe", "-v", "error", "-show_format", "-of", "json", str(path)]))
        duration = float(data["format"]["duration"])
        if not 0 < duration < 3600:
            raise ValueError("Invalid media duration")
        return duration

    def estimate_cost(self, inputs):
        return self._duration(inputs["video_path"]) * 5 / 60

    @staticmethod
    def _request(method, url, **kwargs):
        parsed = urlparse(url)
        if parsed.scheme != "https" or parsed.netloc != "queue.fal.run":
            raise ValueError("Invalid authenticated fal URL")
        r = requests.request(method, url, headers={"Authorization": "Key " + os.environ["FAL_KEY"]},
                             timeout=(15, 120), allow_redirects=False, **kwargs)
        if 300 <= r.status_code < 400:
            raise ValueError("Authenticated redirect rejected")
        r.raise_for_status()
        return r.json()

    def execute(self, inputs):
        started = time.monotonic()
        job = {}
        try:
            jsonschema.validate(inputs, self.input_schema)
            self.check_dependencies()
            paths = [Path(inputs[k]).resolve() for k in ["video_path", "audio_path"]]
            output = Path(inputs["output_path"]).resolve()
            receipt = Path(inputs["job_path"]).resolve()
            if output in paths or receipt in paths or output == receipt:
                raise ValueError("Output and receipt must preserve source files")
            duration = self._duration(paths[0])
            if abs(duration - self._duration(paths[1])) > .05:
                raise ValueError("Pad speech to source duration before syncing; no automatic loop or retime")
            spec = {"endpoint": self._ENDPOINT, "sync_mode": "cut_off", "transport": "fal-cdn",
                    "source_sha256": [hashlib.sha256(p.read_bytes()).hexdigest() for p in paths],
                    "output_path": str(output)}
            digest = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
            if receipt.exists():
                job = json.loads(receipt.read_text())
                if job.get("input_sha256") != digest:
                    raise ValueError("Saved inputs changed; preserve accepted work")
                if job.get("status") == "completed" and output.is_file() and job.get("output_sha256") == hashlib.sha256(output.read_bytes()).hexdigest():
                    return ToolResult(success=True, data=job, artifacts=[str(output), str(receipt)], cost_usd=0)
                if not job.get("request_id"):
                    raise ValueError("Submission acceptance unknown; reconcile fal history, never replay")
                if job.get("status") == "failed":
                    raise ValueError("Saved generation failed; do not replay")
            else:
                # The partner endpoint rejects data URIs despite the generic fal API examples.
                payload = {"sync_mode": "cut_off", "video_url": self._upload(paths[0]),
                           "audio_url": self._upload(paths[1])}
                job = {**spec, "input_sha256": digest, "status": "submitting", "submitted_at": time.time(),
                       "quoted_usd": duration * 5 / 60, "cost_status": "estimate_not_invoice",
                       "uploaded_inputs": {k: payload[k] for k in ["video_url", "audio_url"]}}
                receipt.parent.mkdir(parents=True, exist_ok=True)
                with receipt.open("x") as f:
                    json.dump(job, f); f.flush(); os.fsync(f.fileno())
                result = self._request("POST", "https://queue.fal.run/" + self._ENDPOINT, json=payload)
                for k in ["request_id", "status_url", "response_url"]:
                    if not isinstance(result.get(k), str) or not result[k]:
                        raise ValueError("No complete acceptance receipt; do not replay")
                job.update({k: result[k] for k in ["request_id", "status_url", "response_url"]})
                job["status"] = "accepted"
                save_job(receipt, job)
            for field in ["status_url", "response_url"]:
                parsed = urlparse(job[field])
                expected = "/fal-ai/sync-lipsync/"
                if (parsed.scheme != "https" or parsed.netloc != "queue.fal.run"
                        or not parsed.path.startswith(expected)
                        or "/requests/" + job["request_id"] not in parsed.path):
                    raise ValueError("Saved fal request identity mismatch")
            deadline = time.monotonic() + inputs.get("poll_timeout", 600)
            while time.monotonic() < deadline:
                state = self._request("GET", job["status_url"])
                if state.get("request_id", job["request_id"]) != job["request_id"]:
                    raise ValueError("Provider request identity mismatch")
                job["status"] = state.get("status")
                if state.get("error") or job["status"] in ["FAILED", "CANCELLED"]:
                    job["status"] = "failed"; save_job(receipt, job)
                    raise ValueError("Provider lip-sync failed; preserve task")
                save_job(receipt, job)
                if job["status"] == "COMPLETED":
                    break
                time.sleep(inputs.get("poll_interval", 3))
            else:
                raise ValueError("Known task pending; resume exact receipt")
            result = self._request("GET", job["response_url"])
            download(result["video"]["url"], output)
            if abs(self._duration(output) - duration) > .10:
                raise ValueError("Sync output changed duration; inspect before use")
            job.update(status="completed", output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(),
                       completed_at=time.time(), output_path=str(output))
            save_job(receipt, job)
            return ToolResult(success=True, data=job, artifacts=[str(output), str(receipt)],
                              cost_usd=None, duration_seconds=time.monotonic()-started, model="lipsync-2-pro")
        except Exception as e:
            if isinstance(e, requests.HTTPError) and e.response is not None and e.response.status_code == 422 and job.get("request_id"):
                job.update(status="failed", failure="provider_validation_422")
                save_job(receipt, job)
            error = str(e) if isinstance(e, ValueError) and not isinstance(e, jsonschema.ValidationError) else type(e).__name__
            return ToolResult(success=False, error=error, data=job, cost_usd=None,
                              duration_seconds=time.monotonic()-started)
