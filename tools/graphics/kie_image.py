"""Nano Banana 2.1 on Kie with durable paid-task acceptance and local references."""
from __future__ import annotations

import hashlib
import json
import math
import mimetypes
import os
import re
import time
import uuid
from pathlib import Path
from urllib.parse import urlparse

import jsonschema
import requests
from PIL import Image

from tools.base_tool import (BaseTool, Determinism, ExecutionMode, ResourceProfile,
                             ResumeSupport, RetryPolicy, ToolResult, ToolRuntime,
                             ToolStability, ToolTier)
from tools.provider_jobs import download, save_job


class KieAPIError(RuntimeError):
    def __init__(self, code, retry_after=0):
        super().__init__(f"Kie API code {code}")
        self.code = code
        self.retry_after = retry_after


class KieImage(BaseTool):
    name = "kie_image"
    capability = "image_generation"
    provider = "kie"
    tier = ToolTier.GENERATE
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.ASYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API
    dependencies = ["env:KIE_API_KEY", "python:requests", "python:jsonschema", "python:PIL"]
    install_instructions = "Set KIE_API_KEY in a private .env; https://kie.ai/api-key"
    agent_skills = ["kie-image"]
    capabilities = ["text_to_image", "image_edit", "account_credits"]
    supports = {"image_edit": True, "multiple_reference_images": True, "local_reference_images": True}
    resume_support = ResumeSupport.FROM_CHECKPOINT
    retry_policy = RetryPolicy(max_retries=0)
    resource_profile = ResourceProfile(network_required=True)
    side_effects = ["uploads references", "creates paid Kie image tasks", "writes images and receipts"]
    user_visible_verification = ["Inspect identity, anatomy, pose and frame composition"]
    _MODEL = "nano-banana-2-1"
    _BASE = "https://api.kie.ai"
    _UPLOAD = "https://kieai.redpandaai.co/api/file-stream-upload"
    _CREDITS = {"1K": 4, "2K": 6, "4K": 9}
    input_schema = {
        "type": "object", "additionalProperties": False,
        "properties": {
            "operation": {"enum": ["generate", "credits"], "default": "generate"},
            "model": {"enum": ["nano-banana-2-1"], "default": "nano-banana-2-1"},
            "prompt": {"type": "string", "minLength": 1, "maxLength": 20000},
            # English Kie market page says 10; do not assume Google's 14-input limit.
            "reference_images": {"type": "array", "maxItems": 10,
                                 "items": {"type": "string", "minLength": 1}},
            "aspect_ratio": {"enum": ["1:1", "2:3", "3:2", "1:4", "4:1", "3:4", "4:3", "4:5", "5:4", "1:8", "8:1", "9:16", "16:9", "21:9", "auto"], "default": "16:9"},
            "resolution": {"enum": ["1K", "2K", "4K"], "default": "1K"},
            "output_format": {"enum": ["png", "jpg"], "default": "png"},
            "output_path": {"type": "string", "minLength": 1},
            "job_path": {"type": "string", "minLength": 1},
            "task_id": {"type": "string", "pattern": "^[A-Za-z0-9_-]{1,160}$"},
            "poll_timeout": {"type": "number", "exclusiveMinimum": 0},
            "poll_interval": {"type": "number", "exclusiveMinimum": 0},
            "project_dir": {"type": "string"}, "scene_id": {"type": "string"},
        },
    }

    def estimate_cost(self, inputs):
        return 0.0 if inputs.get("operation") == "credits" else self._CREDITS[inputs.get("resolution", "1K")] * .005

    def _request(self, method, url, **kwargs):
        if not (url.startswith(self._BASE + "/") or url == self._UPLOAD):
            raise ValueError("Unapproved authenticated Kie endpoint")
        r = requests.request(method, url, headers={"Authorization": "Bearer " + os.environ["KIE_API_KEY"]},
                             allow_redirects=False, timeout=(10, 60), **kwargs)
        if 300 <= r.status_code < 400:
            raise ValueError("Kie authentication redirect rejected")
        if r.status_code == 429 or r.status_code >= 500:
            raise KieAPIError(r.status_code, self._retry_after(r))
        r.raise_for_status()
        data = r.json()
        if not isinstance(data, dict) or data.get("code") != 200:
            raise KieAPIError(data.get("code") if isinstance(data, dict) else "invalid", self._retry_after(r))
        return data.get("data")

    @staticmethod
    def _retry_after(response):
        try:
            return max(0, float(response.headers.get("Retry-After", 0)))
        except (TypeError, ValueError):
            return 0

    @staticmethod
    def _https(url):
        parsed = urlparse(url)
        if parsed.scheme != "https" or not parsed.hostname or parsed.username or parsed.password:
            raise ValueError("Reference/result URL must be credential-free HTTPS")
        return url

    def _references(self, references):
        descriptors = []
        for source in references:
            if urlparse(source).scheme == "https":
                descriptors.append({"url": self._https(source)})
            else:
                path = Path(source)
                if not path.is_file() or path.stat().st_size > 30 * 1024 * 1024:
                    raise ValueError("Reference must be an existing image of at most 30MB")
                with Image.open(path) as im:
                    if im.format not in {"JPEG", "PNG", "WEBP"}:
                        raise ValueError("Reference must be JPEG, PNG or WebP")
                    im.verify()
                descriptors.append({"path": str(path.resolve()), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
        return descriptors

    def _upload(self, reference):
        if "url" in reference:
            return reference["url"]
        path = Path(reference["path"])
        filename = "om-" + uuid.uuid4().hex + path.suffix.lower()
        with path.open("rb") as f:
            data = self._request("POST", self._UPLOAD,
                                 files={"file": (filename, f, mimetypes.guess_type(path.name)[0] or "application/octet-stream")},
                                 data={"uploadPath": "images/openmontage", "fileName": filename})
        return self._https(data["downloadUrl"])

    def execute(self, inputs):
        started = time.monotonic()
        job = {}
        submitted = False
        try:
            jsonschema.validate(inputs, self.input_schema)
            self.check_dependencies()
            if inputs.get("operation") == "credits":
                credits = self._request("GET", self._BASE + "/api/v1/chat/credit")
                if isinstance(credits, bool) or not isinstance(credits, (int, float)) or not math.isfinite(credits):
                    raise ValueError("Invalid Kie credit balance")
                return ToolResult(success=True, data={"credits": credits}, cost_usd=0)
            if not inputs.get("output_path"):
                raise ValueError("Generation/resume requires output_path")
            output = Path(inputs["output_path"])
            receipt = Path(inputs.get("job_path", str(output) + ".kie-job.json"))
            if receipt.exists():
                job = json.loads(receipt.read_text())
                if job.get("provider") != "kie" or job.get("model") != self._MODEL:
                    raise ValueError("Saved provider/model mismatch")
                if job.get("output_path") != str(output.resolve()):
                    raise ValueError("Saved output path mismatch")
            spec = None
            if "prompt" in inputs:
                spec = {"model": self._MODEL, "prompt": inputs["prompt"],
                        "references": self._references(inputs.get("reference_images", [])),
                        "aspect_ratio": inputs.get("aspect_ratio", "16:9"),
                        "resolution": inputs.get("resolution", "1K"), "output_format": inputs.get("output_format", "png")}
                digest = hashlib.sha256(json.dumps(spec, sort_keys=True).encode()).hexdigest()
                if job.get("input_sha256") and job["input_sha256"] != digest:
                    raise ValueError("Saved input mismatch; preserve accepted inputs")
            task_id = inputs.get("task_id") or job.get("task_id")
            if inputs.get("task_id") and job.get("task_id") not in (None, task_id):
                raise ValueError("Saved task ID mismatch")
            if not task_id:
                if job:
                    raise ValueError("Submission acceptance unresolved; do not replay")
                if spec is None:
                    raise ValueError("New generation requires prompt")
                if output.exists():
                    raise ValueError("Refusing to overwrite output without its task receipt")
                payload = {"model": self._MODEL, "input": {k: spec[k] for k in ["prompt", "aspect_ratio", "resolution", "output_format"]}}
                payload["input"]["image_input"] = [self._upload(ref) for ref in spec["references"]]
                job = {"provider": "kie", "model": self._MODEL, "status": "submitting", "input_sha256": digest,
                       "payload": payload, "output_path": str(output.resolve()), "submitted_at": time.time(),
                       "quoted_credits": self._CREDITS[spec["resolution"]], "quoted_usd": self.estimate_cost(inputs)}
                receipt.parent.mkdir(parents=True, exist_ok=True)
                with receipt.open("x") as f:
                    json.dump(job, f); f.flush(); os.fsync(f.fileno())
                data = self._request("POST", self._BASE + "/api/v1/jobs/createTask", json=payload)
                task_id = data.get("taskId") if isinstance(data, dict) else None
                if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,160}", task_id):
                    raise ValueError("No confirmed task ID; do not replay")
                submitted = True
            if not isinstance(task_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,160}", task_id):
                raise ValueError("Invalid saved task ID")
            if not job and output.exists():
                raise ValueError("Refusing to overwrite unowned output")
            job.update(provider="kie", model=self._MODEL, task_id=task_id, output_path=str(output.resolve()))
            save_job(receipt, job)
            if job.get("status") == "success" and output.is_file() and job.get("output_sha256") == hashlib.sha256(output.read_bytes()).hexdigest():
                return ToolResult(success=True, data={**job, "new_paid_submission": False}, artifacts=[str(output), str(receipt)], cost_usd=0, model=self._MODEL)
            deadline = time.monotonic() + inputs.get("poll_timeout", 900)
            interval = inputs.get("poll_interval", 3)
            while time.monotonic() < deadline:
                try:
                    data = self._request("GET", self._BASE + "/api/v1/jobs/recordInfo", params={"taskId": task_id})
                except (requests.Timeout, requests.ConnectionError, KieAPIError) as e:
                    if isinstance(e, KieAPIError) and e.code != 429 and not (isinstance(e.code, int) and e.code >= 500):
                        raise
                    delay = max(interval, getattr(e, "retry_after", 0))
                    if delay >= deadline-time.monotonic():
                        raise ValueError("Known Kie task pending; resume after provider backoff")
                    time.sleep(delay)
                    interval = min(interval*1.3, 15)
                    continue
                if not isinstance(data, dict) or data.get("taskId") != task_id or data.get("model") != self._MODEL:
                    raise ValueError("Provider task identity/model mismatch")
                state = data.get("state")
                if state not in {"waiting", "queuing", "generating", "success", "fail"}:
                    raise ValueError("Unknown Kie task state; resume exact task")
                job["status"] = state
                credits = data.get("creditsConsumed")
                if isinstance(credits, (int, float)) and not isinstance(credits, bool) and math.isfinite(credits) and credits >= 0:
                    job["reported_credits"] = credits
                save_job(receipt, job)
                if state == "fail":
                    # Persist only the narrowly recognized provider-side fault; all
                    # other failure reasons remain ineligible for retry treatment.
                    job["failure_code"] = data.get("failCode")
                    job["failure_class"] = ("provider_internal_error" if str(data.get("failCode")) == "500"
                                            and data.get("failMsg") in {"Internal Error", "InternalError"} else "unclassified")
                    save_job(receipt, job)
                    raise ValueError("Kie generation failed; inspect exact task logs, do not replay")
                if state == "success":
                    result = json.loads(data["resultJson"]) if isinstance(data.get("resultJson"), str) else data.get("resultJson")
                    urls = result.get("resultUrls") if isinstance(result, dict) else None
                    if not isinstance(urls, list) or len(urls) != 1:
                        raise ValueError("Expected one Kie image result")
                    result_url = self._https(urls[0])
                    temporary = output.with_name(output.name + ".download")
                    download(result_url, temporary)
                    with Image.open(temporary) as im:
                        if im.format not in {"JPEG", "PNG", "WEBP"}:
                            raise ValueError("Kie result is not a supported image")
                        job["width"], job["height"] = im.size
                        im.verify()
                    temporary.replace(output)
                    job.update(output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(), result_url=result_url, completed_at=time.time())
                    save_job(receipt, job)
                    return ToolResult(success=True, data={**job, "new_paid_submission": submitted}, artifacts=[str(output), str(receipt)], cost_usd=job.get("quoted_usd") if submitted else 0,
                                      duration_seconds=time.monotonic()-started, model=self._MODEL)
                time.sleep(min(interval, max(0, deadline-time.monotonic())))
                interval = min(interval*1.3, 15)
            raise ValueError("Known Kie task pending; resume exact task ID")
        except Exception as e:
            # Do not expose raw provider messages or request exception headers.
            error = "Kie input schema invalid" if isinstance(e, jsonschema.ValidationError) else (str(e) if type(e) in {ValueError, KieAPIError} else "Kie " + type(e).__name__)
            error = error.replace(os.environ.get("KIE_API_KEY") or "\0", "[REDACTED]")
            return ToolResult(success=False, error=error, data=job, cost_usd=None, duration_seconds=time.monotonic()-started)
