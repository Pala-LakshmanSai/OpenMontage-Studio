"""Seedance 2.0 and 2.5 (ByteDance) video generation via fal.ai API.

Best for cinematic clips with native audio, director-level camera control,
and lip-sync from quoted dialogue in prompts.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import tempfile
import time
from pathlib import Path
from typing import Any

from tools.base_tool import (
    BaseTool,
    Determinism,
    ExecutionMode,
    ResourceProfile,
    RetryPolicy,
    ToolResult,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    ToolTier,
)


class _SeedanceInputError(ValueError):
    """Safe validation messages containing no provider response text."""


class SeedanceVideo(BaseTool):
    name = "seedance_video"
    version = "0.3.0"
    tier = ToolTier.GENERATE
    capability = "video_generation"
    provider = "seedance"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.SYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API

    dependencies = []
    install_instructions = (
        "Set FAL_KEY to your fal.ai API key.\n"
        "  Get one at https://fal.ai/dashboard/keys"
    )
    agent_skills = ["seedance-2-0", "seedance-2-5", "ai-video-gen"]

    capabilities = ["text_to_video", "image_to_video", "reference_to_video"]
    supports = {
        "text_to_video": True,
        "image_to_video": True,
        "reference_to_video": True,
        "multiple_reference_images": True,
        "reference_image": True,
        "native_audio": True,
        "cinematic_quality": True,
        "camera_direction": True,
        "lip_sync": True,
        "multi_shot": True,
        "aspect_ratio": True,
        "seed": True,
    }
    best_for = [
        "preferred premium video gen when FAL_KEY is available",
        "cinematic trailers, teasers, and high-fidelity clips with native synchronized audio",
        "director-level camera control and multi-shot editing in a single generation",
        "lip-sync from quoted dialogue in prompts",
        "Seedance 2.5 reference generation (up to 30 images + 10 video + 10 audio clips)",
        "consistent character identity across shots",
    ]
    not_good_for = ["offline generation", "budget-constrained projects"]
    fallback_tools = ["veo_video", "kling_video", "minimax_video"]
    # Premium model — beat out "experimental stability" baseline. The scoring
    # engine reads quality_score directly when present (see lib/scoring.py).
    quality_score = 0.95

    input_schema = {
        "type": "object",
        "required": ["prompt"],
        "properties": {
            "prompt": {"type": "string"},
            "operation": {
                "type": "string",
                "enum": ["text_to_video", "image_to_video", "reference_to_video"],
                "default": "text_to_video",
            },
            "model_variant": {
                "type": "string",
                "enum": ["standard", "fast"],
                "default": "standard",
                "description": "standard = highest quality, fast = lower latency and cost",
            },
            "model_version": {
                "type": "string",
                "enum": ["2.0", "2.5"],
                "default": "2.0",
                "description": "Seedance 2.5 is the current high-quality model; 2.0 retains fast-tier access.",
            },
            "duration": {
                "type": "string",
                "enum": [
                    "auto",
                    "4",
                    "5",
                    "6",
                    "7",
                    "8",
                    "9",
                    "10",
                    "11",
                    "12",
                    "13",
                    "14",
                    "15",
                    "16",
                    "17",
                    "18",
                    "19",
                    "20",
                    "21",
                    "22",
                    "23",
                    "24",
                    "25",
                    "26",
                    "27",
                    "28",
                    "29",
                    "30",
                ],
                "default": "5",
                "description": "Duration in seconds. 'auto' lets the model decide.",
            },
            "aspect_ratio": {
                "type": "string",
                "enum": ["auto", "21:9", "16:9", "4:3", "1:1", "3:4", "9:16"],
                "default": "16:9",
            },
            "resolution": {
                "type": "string",
                "enum": ["480p", "720p"],
                "default": "720p",
            },
            "generate_audio": {
                "type": "boolean",
                "default": True,
                "description": "Generate synchronized audio (speech, SFX, ambient)",
            },
            "image_url": {
                "type": "string",
                "description": "Start frame image URL for image_to_video (jpg, png, webp)",
            },
            "image_path": {
                "type": "string",
                "description": "Local start-frame path for image_to_video. Auto-uploaded to fal.ai storage.",
            },
            "end_image_url": {
                "type": "string",
                "description": "Optional end frame URL for image_to_video",
            },
            "reference_image_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Up to 9 (2.0) or 30 (2.5) reference image URLs for reference_to_video (identity / wardrobe / setting / style anchors).",
            },
            "reference_image_paths": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Local reference image paths for reference_to_video. Auto-uploaded to fal.ai storage.",
            },
            "reference_video_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Up to 3 (2.0) or 10 (2.5) reference video clip URLs for reference_to_video (motion / camera / pacing anchors).",
            },
            "reference_audio_urls": {
                "type": "array",
                "items": {"type": "string"},
                "description": "Up to 3 (2.0) or 10 (2.5) reference audio clip URLs for reference_to_video (voice / music / ambience anchors).",
            },
            "seed": {
                "type": "integer",
                "description": "Optional seed for reproducibility",
            },
            "output_path": {"type": "string"},
            "job_path": {
                "type": "string",
                "description": "Private durable queue receipt; reuse with identical inputs to resume without submitting again.",
            },
            "max_poll_seconds": {"type": "number", "default": 600},
            "poll_interval_seconds": {"type": "number", "default": 5},
            "reference_video_duration_seconds": {
                "type": "number",
                "description": "Combined reference video duration for billing estimate; omitted duration conservatively assumes 30 seconds per video.",
            },
        },
    }

    resource_profile = ResourceProfile(
        cpu_cores=1, ram_mb=512, vram_mb=0, disk_mb=500, network_required=True
    )
    retry_policy = RetryPolicy(
        max_retries=2, retryable_errors=["rate_limit", "timeout"]
    )
    idempotency_key_fields = [
        "prompt",
        "model_version",
        "model_variant",
        "operation",
        "duration",
        "seed",
    ]
    side_effects = ["writes video file to output_path", "calls fal.ai API"]
    user_visible_verification = [
        "Watch generated clip for motion coherence, audio sync, and visual quality"
    ]

    def _get_api_key(self) -> str | None:
        return os.environ.get("FAL_KEY") or os.environ.get("FAL_AI_API_KEY")

    def get_status(self) -> ToolStatus:
        if self._get_api_key():
            return ToolStatus.AVAILABLE
        return ToolStatus.UNAVAILABLE

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        if inputs.get("model_version", "2.0") == "2.5":
            # Conservative ceiling over published ~$0.473/s at 720p.
            duration = inputs.get("duration", "5")
            secs = 30 if duration == "auto" else int(duration)
            rate = 0.23 if inputs.get("resolution", "720p") == "480p" else 0.50
            videos = inputs.get("reference_video_urls") or []
            if videos:
                secs = 0.6 * (secs + float(inputs.get(
                    "reference_video_duration_seconds", 30 * len(videos)
                )))
            return round(rate * secs, 2)
        variant = inputs.get("model_variant", "standard")
        duration = inputs.get("duration", "5")
        secs = 5 if duration == "auto" else int(duration)
        rate = 0.2419 if variant == "fast" else 0.3034
        return round(rate * secs, 2)

    def estimate_runtime(self, inputs: dict[str, Any]) -> float:
        if inputs.get("model_version", "2.0") == "2.5":
            return 150.0
        variant = inputs.get("model_variant", "standard")
        return 60.0 if variant == "fast" else 120.0

    @staticmethod
    def build_request(inputs: dict[str, Any]) -> tuple[str, dict[str, Any]]:
        """Pure endpoint/payload preflight. Local images must already be uploaded."""
        operation = inputs.get("operation", "text_to_video")
        model_version = inputs.get("model_version", "2.0")
        variant = inputs.get("model_variant", "standard")
        operation_path = operation.replace("_", "-")

        if model_version == "2.5":
            if variant == "fast":
                raise _SeedanceInputError("Seedance 2.5 on fal.ai has no fast endpoint; use model_variant='standard'.")
            model_path = f"bytedance/seedance-2.5/{operation_path}"
        elif variant == "fast":
            model_path = f"bytedance/seedance-2.0/fast/{operation_path}"
        else:
            model_path = f"bytedance/seedance-2.0/{operation_path}"

        if model_version == "2.0" and "duration" in inputs:
            if inputs["duration"] not in {"auto", *(str(seconds) for seconds in range(4, 16))}:
                raise _SeedanceInputError("Seedance 2.0 duration must be 'auto' or an integer string from 4 to 15 seconds.")

        payload: dict[str, Any] = {"prompt": inputs["prompt"]}

        if inputs.get("duration"):
            payload["duration"] = inputs["duration"]
        if inputs.get("aspect_ratio"):
            payload["aspect_ratio"] = inputs["aspect_ratio"]
        if inputs.get("resolution"):
            payload["resolution"] = inputs["resolution"]
        if "generate_audio" in inputs:
            payload["generate_audio"] = inputs["generate_audio"]
        if inputs.get("seed") is not None:
            payload["seed"] = inputs["seed"]

        if operation == "image_to_video":
            if inputs.get("image_url"):
                payload["image_url"] = inputs["image_url"]
            elif inputs.get("image_path"):
                raise _SeedanceInputError("build_request requires uploaded image_url for local image_path")
            if inputs.get("end_image_url"):
                payload["end_image_url"] = inputs["end_image_url"]
            if model_version == "2.5":
                payload["aspect_ratio"] = "auto"

        if operation == "reference_to_video":
            ref_image_urls = list(inputs.get("reference_image_urls") or [])
            if inputs.get("reference_image_paths"):
                raise _SeedanceInputError("build_request requires uploaded reference_image_urls for local references")
            max_images = 30 if model_version == "2.5" else 9
            max_videos = 10 if model_version == "2.5" else 3
            max_audios = 10 if model_version == "2.5" else 3
            if len(ref_image_urls) > max_images:
                raise _SeedanceInputError(f"Seedance {model_version} reference_to_video accepts at most {max_images} reference images; got {len(ref_image_urls)}")
            ref_video_urls = list(inputs.get("reference_video_urls") or [])
            if len(ref_video_urls) > max_videos:
                raise _SeedanceInputError(f"Seedance {model_version} reference_to_video accepts at most {max_videos} reference videos; got {len(ref_video_urls)}")
            ref_audio_urls = list(inputs.get("reference_audio_urls") or [])
            if len(ref_audio_urls) > max_audios:
                raise _SeedanceInputError(f"Seedance {model_version} reference_to_video accepts at most {max_audios} reference audio clips; got {len(ref_audio_urls)}")
            if model_version == "2.0":
                if len(ref_image_urls) + len(ref_video_urls) + len(ref_audio_urls) > 12:
                    raise _SeedanceInputError("Seedance 2.0 accepts at most 12 combined reference files.")
                if ref_audio_urls and not (ref_image_urls or ref_video_urls):
                    raise _SeedanceInputError("Seedance 2.0 audio references require an image or video reference.")
            # fal's standard/fast 2.0 reference-to-video API (verified 2026-11-03):
            # https://fal.ai/models/bytedance/seedance-2.0/reference-to-video/api
            # Both versions use these native fields; reference_* remain adapter inputs.
            if ref_image_urls:
                payload["image_urls"] = ref_image_urls
            if ref_video_urls:
                payload["video_urls"] = ref_video_urls
            if ref_audio_urls:
                payload["audio_urls"] = ref_audio_urls

        return model_path, payload

    @staticmethod
    def _input_hash(inputs: dict[str, Any]) -> str:
        material = {k: v for k, v in inputs.items() if k not in {
            "job_path", "output_path", "max_poll_seconds", "poll_interval_seconds"
        }}
        for key in ("image_path", "reference_image_paths"):
            paths = material.get(key)
            if paths:
                paths = [paths] if isinstance(paths, str) else paths
                material[key] = [{
                    "path": str(path),
                    "sha256": hashlib.sha256(Path(path).read_bytes()).hexdigest(),
                } for path in paths]
        return hashlib.sha256(json.dumps(material, sort_keys=True).encode()).hexdigest()

    @staticmethod
    def _save_job(path: Path, receipt: dict[str, Any], *, create: bool = False) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        if create:
            fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
            with os.fdopen(fd, "w") as handle:
                json.dump(receipt, handle)
                handle.flush()
                os.fsync(handle.fileno())
            return
        fd, temporary = tempfile.mkstemp(prefix=".seedance-", dir=path.parent)
        try:
            with os.fdopen(fd, "w") as handle:
                json.dump(receipt, handle)
                handle.flush()
                os.fsync(handle.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)

    @staticmethod
    def _record_rejection(response: Any, receipt: dict[str, Any]) -> None:
        """Keep only classified provider details, never echoed inputs or URLs."""
        try:
            detail = response.json().get("detail", [])
        except (ValueError, AttributeError):
            detail = []
        if isinstance(detail, dict):
            detail = [detail]
        details = []
        for entry in detail if isinstance(detail, list) else []:
            if not isinstance(entry, dict):
                continue
            policy = entry.get("type") == "content_policy_violation"
            error_type = "content_policy_violation" if policy else "invalid_request"
            # Provider messages can echo access-bearing inputs; retain known causes only.
            message = "Provider rejected the request inputs."
            if policy:
                message = "Provider content checker rejected the request."
                if "detected an identifiable real person" in str(entry.get("msg", "")):
                    message = "Provider detected an identifiable real person."
            location = entry.get("loc", [])
            if not isinstance(location, list):
                location = []
            location = [value for value in location if (
                isinstance(value, int) or (
                    isinstance(value, str) and value.replace("_", "").isalnum()
                    and len(value) <= 80
                )
            )]
            details.append({"loc": location, "msg": message, "type": error_type})
        policy = any(entry["type"] == "content_policy_violation" for entry in details)
        receipt["terminal_error_type"] = "content_policy_violation" if policy else "invalid_request"
        receipt["terminal_error_detail"] = details
        receipt["state"] = "REJECTED_CONTENT" if policy else "REJECTED_INPUT"

    @staticmethod
    def _rejection_result(receipt: dict[str, Any]) -> ToolResult:
        policy = receipt["state"] == "REJECTED_CONTENT"
        message = "Provider rejected the request inputs."
        if policy:
            message = "Provider content checker rejected the request."
            if any(entry.get("msg") == "Provider detected an identifiable real person."
                   for entry in receipt.get("terminal_error_detail", [])):
                message = "Provider detected an identifiable real person."
            message += " Stop this request; do not retry or switch providers to evade rejection."
        return ToolResult(
            success=False,
            error=f"Seedance {receipt['terminal_error_type']}: {message}",
            data={"state": receipt["state"], "terminal_error_type": receipt["terminal_error_type"]},
        )

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        api_key = self._get_api_key()
        if not api_key:
            return ToolResult(success=False, error="FAL_KEY not set. " + self.install_instructions)

        import requests

        start = time.time()
        model_version = inputs.get("model_version", "2.0")
        operation = inputs.get("operation", "text_to_video")
        variant = inputs.get("model_variant", "standard")
        job_path = Path(inputs["job_path"]) if inputs.get("job_path") else None
        receipt: dict[str, Any] = {}
        try:
            poll_seconds = float(inputs.get("max_poll_seconds", 600))
            poll_interval = float(inputs.get("poll_interval_seconds", 5))
            if not math.isfinite(poll_seconds) or not 0 <= poll_seconds <= 3600:
                raise _SeedanceInputError("max_poll_seconds must be between 0 and 3600")
            if not math.isfinite(poll_interval) or not 0 < poll_interval <= 60:
                raise _SeedanceInputError("poll_interval_seconds must be between 0 and 60")
            input_hash = self._input_hash(inputs)
            if job_path and job_path.exists():
                os.chmod(job_path, 0o600)
                receipt = json.loads(job_path.read_text())
                if receipt.get("input_hash") != input_hash:
                    raise _SeedanceInputError("Receipt input mismatch; refusing to submit or resume")
                model_path, payload = receipt["model"], receipt["payload"]
                expected = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                if receipt.get("payload_hash") != expected:
                    raise _SeedanceInputError("Receipt payload mismatch; refusing to resume")
                if receipt.get("state") in ("REJECTED_CONTENT", "REJECTED_INPUT"):
                    return self._rejection_result(receipt)
                if not all(receipt.get(k) for k in ("request_id", "status_url", "response_url")):
                    raise _SeedanceInputError("Submission acceptance unknown; receipt blocks replay. Reconcile with provider before any new job")
            else:
                resolved = dict(inputs)
                if resolved.get("image_path") and not resolved.get("image_url"):
                    from tools.video._shared import upload_image_fal
                    resolved["image_url"] = upload_image_fal(resolved.pop("image_path"))
                if resolved.get("reference_image_paths"):
                    from tools.video._shared import upload_image_fal
                    resolved["reference_image_urls"] = list(resolved.get("reference_image_urls") or []) + [
                        upload_image_fal(path) for path in resolved.pop("reference_image_paths")
                    ]
                model_path, payload = self.build_request(resolved)
                receipt = {
                    "version": 1, "state": "submitting", "input_hash": input_hash,
                    "payload_hash": hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest(),
                    "model": model_path, "payload": payload,
                }
                if job_path:
                    self._save_job(job_path, receipt, create=True)
        except Exception as exc:
            # Validation text is ours; provider errors must never expose signed URLs.
            error = str(exc) if isinstance(exc, _SeedanceInputError) else type(exc).__name__
            return ToolResult(success=False, error=f"Seedance preflight failed: {error}")

        headers = {
            "Authorization": f"Key {api_key}",
            "Content-Type": "application/json",
        }

        try:
            if not receipt.get("status_url"):
                submit_resp = requests.post(
                    f"https://queue.fal.run/{model_path}", headers=headers,
                    json=payload, timeout=30,
                )
                if getattr(submit_resp, "status_code", None) == 422:
                    self._record_rejection(submit_resp, receipt)
                    if job_path:
                        self._save_job(job_path, receipt)
                    return self._rejection_result(receipt)
                submit_resp.raise_for_status()
                queue_data = submit_resp.json()
                receipt.update({
                    "state": "accepted", "request_id": queue_data.get("request_id"),
                    "status_url": queue_data.get("status_url"),
                    "response_url": queue_data.get("response_url"),
                })
                if job_path:
                    self._save_job(job_path, receipt)
                    if not receipt.get("request_id"):
                        raise _SeedanceInputError("Queue acceptance lacks confirmed request ID")
            status_url = receipt["status_url"]
            response_url = receipt["response_url"]
            deadline = time.monotonic() + poll_seconds
            # Also bound attempts when a test clock or system clock does not advance.
            for attempt in range(max(1, math.ceil(poll_seconds / poll_interval))):
                status_resp = requests.get(status_url, headers=headers, timeout=15)
                status_resp.raise_for_status()
                status = status_resp.json().get("status", "UNKNOWN")
                receipt["state"] = status
                if job_path:
                    self._save_job(job_path, receipt)
                if status == "COMPLETED":
                    break
                if status in ("FAILED", "CANCELLED"):
                    return ToolResult(success=False, error=f"Seedance {model_version} video generation {status.lower()}")
                if time.monotonic() >= deadline or attempt + 1 >= max(1, math.ceil(poll_seconds / poll_interval)):
                    return ToolResult(success=False, error="Seedance job remains pending; resume the same job_path for read-only polling")
                time.sleep(min(poll_interval, max(0, deadline - time.monotonic())))

            result_resp = requests.get(response_url, headers=headers, timeout=30)
            if getattr(result_resp, "status_code", None) == 422:
                self._record_rejection(result_resp, receipt)
                if job_path:
                    self._save_job(job_path, receipt)
                return self._rejection_result(receipt)
            result_resp.raise_for_status()
            data = result_resp.json()

            video_url = data["video"]["url"]
            receipt["video_url"] = video_url
            if job_path:
                self._save_job(job_path, receipt)
            video_response = requests.get(video_url, timeout=120)
            video_response.raise_for_status()

            output_path = Path(inputs.get("output_path", "seedance_output.mp4"))
            output_path.parent.mkdir(parents=True, exist_ok=True)
            output_path.write_bytes(video_response.content)

        except Exception as e:
            return ToolResult(
                success=False,
                error=f"Seedance {model_version} operation interrupted ({type(e).__name__}); preserve and resume the same job_path. Submission without a confirmed receipt must not be replayed.",
            )

        from tools.video._shared import probe_output

        probed = probe_output(output_path)
        return ToolResult(
            success=True,
            data={
                "provider": "seedance",
                "request_id": receipt.get("request_id"),
                "job_path": str(job_path) if job_path else None,
                "model": model_path,
                "prompt": inputs["prompt"],
                "operation": operation,
                "variant": variant,
                "model_version": model_version,
                "aspect_ratio": inputs.get("aspect_ratio", "16:9"),
                "resolution": inputs.get("resolution", "720p"),
                "generate_audio": inputs.get("generate_audio", True),
                "seed": data.get("seed"),
                "output": str(output_path),
                "output_path": str(output_path),
                "format": "mp4",
                **probed,
            },
            artifacts=[str(output_path)],
            cost_usd=self.estimate_cost(inputs),
            duration_seconds=round(time.time() - start, 2),
            model=model_path,
        )
