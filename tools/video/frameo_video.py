"""Frameo Seedance 2.5: zero-credit pass generation with durable no-replay receipts.

Contract verified against https://api.frameo.ai/v1/openapi.json, 2026-11-03.
No generation is submitted without a fresh zero-credit estimate and an active
caller-specified pass window. Accepted jobs may still be fetched after expiry.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import math
import mimetypes
import os
import re
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import requests

from tools.base_tool import BaseTool, ToolResult, ToolStatus, ToolTier, ToolStability, ToolRuntime


class FrameoVideo(BaseTool):
    name = "frameo_video"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "frameo"
    stability = ToolStability.BETA
    runtime = ToolRuntime.API
    dependencies = ["requests"]
    install_instructions = "Use the authorized workspace API key from Frameo's Developers page; store it in a private file."
    agent_skills = ["seedance-2-5"]
    capabilities = ["text_to_video", "image_to_video", "reference_to_video"]
    supports = {"native_audio": True, "reference_image": True, "multiple_reference_images": True}
    fallback_tools = []
    side_effects = ["calls Frameo API", "writes private job receipt and generated video"]
    input_schema = {
        "type": "object",
        "required": ["prompt", "api_key_path", "job_path", "output_path", "pass_expires_at"],
        "properties": {
            "prompt": {"type": "string"}, "api_key_path": {"type": "string"},
            "job_path": {"type": "string"}, "output_path": {"type": "string"},
            "pass_expires_at": {"type": "string"},
            "duration_seconds": {"type": "integer", "minimum": 4, "maximum": 30},
            "model": {"type": "string", "enum": ["seedance_2_5"]},
            "resolution": {"type": "string", "enum": ["720p"]},
            "aspect_ratio": {"type": "string", "enum": ["16:9"]},
            "generate_audio": {"type": "boolean", "const": True},
            "images": {"type": "array"}, "videos": {"type": "array"}, "audios": {"type": "array"},
            "max_poll_seconds": {"type": "number"}, "poll_interval_seconds": {"type": "number"},
        },
    }
    API = "https://api.frameo.ai/v1"

    @staticmethod
    def _utc_now() -> str:
        return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    def get_status(self) -> ToolStatus:
        path = os.environ.get("FRAMEO_API_KEY_FILE")
        return ToolStatus.AVAILABLE if path and Path(path).is_file() else ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        # This adapter refuses nonzero quotes; a live workspace estimate is mandatory.
        return 0.0

    @staticmethod
    def _save(path: Path, data: dict) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".frameo-", dir=path.parent)
        try:
            with os.fdopen(fd, "w") as f:
                os.fchmod(f.fileno(), 0o600)
                json.dump(data, f, indent=2)
                f.flush()
                os.fsync(f.fileno())
            os.replace(tmp, path)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)

    @staticmethod
    def _headers(api_key_path: str) -> dict[str, str]:
        path = Path(api_key_path)
        if path.stat().st_mode & 0o077:
            raise ValueError("API key file must be private (mode 0600)")
        value = path.read_text().strip()
        if not value or "\n" in value:
            raise ValueError("API key file must contain one nonempty key")
        return {"Authorization": "Bearer " + value, "Content-Type": "application/json"}

    @staticmethod
    def _https(url: str) -> bool:
        parsed = urlparse(url)
        return parsed.scheme == "https" and bool(parsed.netloc) and not parsed.username and not parsed.password

    @classmethod
    def build_request(cls, inputs: dict[str, Any]) -> dict[str, Any]:
        if inputs.get("model", "seedance_2_5") != "seedance_2_5":
            raise ValueError("Only Seedance 2.5 is authorized by this adapter")
        if inputs.get("resolution", "720p") != "720p" or inputs.get("aspect_ratio", "16:9") != "16:9":
            raise ValueError("Only 720p landscape output is supported")
        if inputs.get("generate_audio", True) is not True:
            raise ValueError("Native audio must remain enabled")
        prompt = inputs.get("prompt")
        duration = inputs.get("duration_seconds", 30)
        if not isinstance(prompt, str) or not prompt.strip() or len(prompt) > 20000:
            raise ValueError("Prompt must contain 1 to 20000 characters")
        if type(duration) is not int or not 4 <= duration <= 30:
            raise ValueError("Duration must be an integer from 4 to 30")
        body = {"model": "seedance_2_5", "prompt": prompt, "duration_seconds": duration,
                "resolution": "720p", "aspect_ratio": "16:9", "generate_audio": True}
        for kind, limit in (("images", 30), ("videos", 8), ("audios", 8)):
            media = inputs.get(kind, [])
            if not isinstance(media, list) or len(media) > limit:
                raise ValueError(f"Too many {kind}")
            for item in media:
                if not isinstance(item, dict) or set(item) - {"url", "role"} or not cls._https(item.get("url", "")):
                    raise ValueError(f"Invalid {kind} reference")
                if kind == "images" and item.get("role") not in (None, "reference", "first_frame", "last_frame"):
                    raise ValueError("Invalid image role")
                if kind == "videos" and item.get("role") not in (None, "reference"):
                    raise ValueError("Invalid video role")
                if kind == "audios" and item.get("role") is not None:
                    raise ValueError("Audio references have no role")
            if media: body[kind] = media
        for key in ("negative_prompt", "seed"):
            if key in inputs: body[key] = inputs[key]
        return body

    @staticmethod
    def _before_expiry(inputs: dict) -> None:
        expiry = datetime.fromisoformat(inputs["pass_expires_at"].replace("Z", "+00:00"))
        if expiry.tzinfo is None:
            raise ValueError("Pass expiry must include its timezone")
        margin = float(inputs.get("submission_margin_seconds", 60))
        if not math.isfinite(margin) or margin < 0:
            raise ValueError("Submission margin must be nonnegative")
        if datetime.now(timezone.utc).timestamp() + margin >= expiry.timestamp():
            raise ValueError("Pass submission window ended; accepted jobs remain resumable")

    @classmethod
    def estimate_request(cls, body: dict, api_key_path: str) -> dict:
        response = requests.post(cls.API + "/estimates", headers=cls._headers(api_key_path), json=body, timeout=30)
        response.raise_for_status()
        quote = response.json()
        if quote.get("model") != "seedance_2_5" or type(quote.get("credits")) is not int:
            raise ValueError("Invalid workspace estimate")
        return quote

    @classmethod
    def upload_file(cls, path: str, api_key_path: str) -> str:
        """Upload once, with no credential forwarded to the signed storage URL."""
        source = Path(path)
        content_type = mimetypes.guess_type(source.name)[0] or "application/octet-stream"
        try:
            response = requests.post(cls.API + "/uploads", headers=cls._headers(api_key_path),
                                     json={"content_type": content_type}, timeout=30)
            response.raise_for_status()
            info = response.json()
            if not cls._https(info.get("upload_url", "")) or not cls._https(info.get("url", "")):
                raise ValueError("Invalid upload response")
            storage_headers = {"Content-Type": content_type}
            # Frameo currently returns an Azure SAS URL, without upload headers.
            # Azure Put Blob requires this header even when SAS authenticates it.
            # https://learn.microsoft.com/en-us/rest/api/storageservices/put-blob
            host = urlparse(info["upload_url"]).hostname or ""
            if host.endswith(".blob.core.windows.net"):
                storage_headers["x-ms-blob-type"] = "BlockBlob"
            with source.open("rb") as data:
                upload = requests.put(info["upload_url"], data=data, headers=storage_headers, timeout=120)
                upload.raise_for_status()
            # A successful storage PUT is not sufficient: current Frameo upload
            # responses can contain private content URLs that model workers cannot
            # fetch. Reject those before any generation spends a pass slot.
            probe = requests.get(info["url"], headers={"Range": "bytes=0-31"}, stream=True, timeout=20)
            try:
                if probe.status_code not in (200, 206):
                    raise ValueError(f"Uploaded reference is not publicly fetchable (HTTP {probe.status_code}); use an authorized readable media URL")
            finally:
                if hasattr(probe, "close"): probe.close()
            return info["url"]
        except requests.RequestException as exc:
            status = getattr(getattr(exc, "response", None), "status_code", None)
            # Do not expose bearer credentials or signed storage URLs in callers' tracebacks.
            raise RuntimeError(f"Frameo upload failed ({type(exc).__name__}, HTTP {status})") from None

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        started = time.monotonic()
        try:
            body = self.build_request(inputs)
            job = Path(inputs["job_path"])
            out = Path(inputs["output_path"])
            headers = self._headers(inputs["api_key_path"])
            seconds = float(inputs.get("max_poll_seconds", 600))
            interval = float(inputs.get("poll_interval_seconds", 5))
            if not math.isfinite(seconds) or not 0 <= seconds <= 3600 or not math.isfinite(interval) or not 0 < interval <= 60:
                raise ValueError("Invalid polling interval or duration")
            digest = hashlib.sha256(json.dumps(body, sort_keys=True).encode()).hexdigest()
            job.parent.mkdir(parents=True, exist_ok=True)
            with open(str(job) + ".lock", "a") as lock:
                os.chmod(lock.name, 0o600)
                fcntl.flock(lock, fcntl.LOCK_EX)
                if job.exists():
                    os.chmod(job, 0o600)
                    receipt = json.loads(job.read_text())
                    if receipt.get("input_hash") != digest:
                        raise ValueError("Receipt input mismatch; no submission or resume")
                    if not receipt.get("generation_id"):
                        raise ValueError("Acceptance uncertain or refused; preserve receipt and do not replay")
                    if receipt.get("state") in ("failed", "cancelled"):
                        return ToolResult(success=False, error="Terminal generation preserved; no replay")
                else:
                    self._before_expiry(inputs)
                    quote = self.estimate_request(body, inputs["api_key_path"])
                    if quote["credits"] != 0:
                        return ToolResult(success=False, error="Nonzero estimate; no generation submitted", data={"credits": quote["credits"]})
                    self._before_expiry(inputs)
                    receipt = {"version": 1, "input_hash": digest, "payload": body,
                               "idempotency_key": str(uuid.uuid4()), "state": "submitting", "estimate": quote,
                               "submitted_at": self._utc_now()}
                    self._save(job, receipt)
                    response = requests.post(self.API + "/generations", json=body,
                                             headers={**headers, "Idempotency-Key": receipt["idempotency_key"]}, timeout=45)
                    if response.status_code != 202:
                        receipt.update(state="submission_refused" if response.status_code < 500 else "acceptance_unknown",
                                       http_status=response.status_code)
                        self._save(job, receipt)
                        return ToolResult(success=False, error="Submission not confirmed; preserve receipt, no automatic replay")
                    generation = response.json()
                    generation_id = generation.get("id", "")
                    if not re.fullmatch(r"gen_[A-Za-z0-9_-]+", generation_id):
                        raise ValueError("Missing confirmed generation ID; no replay")
                    receipt.update(generation_id=generation_id, state=generation.get("status", "queued"),
                                   accepted_at=self._utc_now())
                    self._save(job, receipt)

                deadline = time.monotonic() + seconds
                for attempt in range(max(1, math.ceil(seconds / interval))):
                    response = requests.get(self.API + "/generations/" + receipt["generation_id"], headers=headers, timeout=30)
                    response.raise_for_status()
                    generation = response.json()
                    if generation.get("id") != receipt["generation_id"] or generation.get("model") != "seedance_2_5":
                        raise ValueError("Provider returned a different generation or model")
                    receipt.update(state=generation.get("status"), generation=generation)
                    if receipt["state"] == "running":
                        receipt.setdefault("running_first_seen_at", self._utc_now())
                    elif receipt["state"] in ("succeeded", "failed", "cancelled"):
                        receipt.setdefault("completed_seen_at", self._utc_now())
                    self._save(job, receipt)
                    if receipt["state"] in ("failed", "cancelled"):
                        return ToolResult(success=False, error="Generation ended without usable output; no replay",
                                          data={"state": receipt["state"], "generation_id": receipt["generation_id"]})
                    if receipt["state"] == "succeeded":
                        return self._download(generation, out, receipt, job, started)
                    if time.monotonic() >= deadline or attempt + 1 >= max(1, math.ceil(seconds / interval)):
                        break
                    time.sleep(min(interval, max(0, deadline - time.monotonic())))
                return ToolResult(success=False, error="Generation pending; resume exact receipt",
                                  data={"state": receipt["state"], "generation_id": receipt["generation_id"]})
        except Exception as exc:
            # Provider exceptions can contain signed URLs or credentials. Never echo them.
            message = str(exc) if type(exc) is ValueError else type(exc).__name__
            return ToolResult(success=False, error="Frameo: " + message)

    def _download(self, generation: dict, out: Path, receipt: dict, job: Path, started: float) -> ToolResult:
        credits = generation.get("credits") or {}
        outputs = generation.get("outputs") or []
        video = next((x for x in outputs if x.get("type") == "video"), None)
        if not video or not self._https(video.get("url", "")):
            raise ValueError("Success response lacks a valid video output")
        if out.exists() and receipt.get("output_sha256"):
            if hashlib.sha256(out.read_bytes()).hexdigest() == receipt["output_sha256"]:
                return ToolResult(success=True, artifacts=[str(out)], data={"generation_id": receipt["generation_id"], "credits": credits, "cached": True}, model="seedance_2_5")
        elif out.exists():
            raise ValueError("Output already exists without a matching receipt; preserve it")
        out.parent.mkdir(parents=True, exist_ok=True)
        fd, tmp = tempfile.mkstemp(prefix=".frameo-video-", suffix=".mp4", dir=out.parent)
        try:
            response = requests.get(video["url"], stream=True, timeout=180)
            response.raise_for_status()
            with os.fdopen(fd, "wb") as f:
                for chunk in response.iter_content(1024 * 1024):
                    if chunk: f.write(chunk)
            if not Path(tmp).stat().st_size:
                raise ValueError("Empty output download")
            os.replace(tmp, out)
        finally:
            if os.path.exists(tmp): os.unlink(tmp)
        receipt.update(output_path=str(out), output_sha256=hashlib.sha256(out.read_bytes()).hexdigest(),
                       download_completed_at=self._utc_now())
        self._save(job, receipt)
        # Preserve any unexpectedly charged result for billing reconciliation, without another POST.
        return ToolResult(success=True, artifacts=[str(out)], data={"generation_id": receipt["generation_id"], "credits": credits,
                          "unexpected_charge": credits.get("charged") not in (None, 0)}, model="seedance_2_5", duration_seconds=time.monotonic() - started)
