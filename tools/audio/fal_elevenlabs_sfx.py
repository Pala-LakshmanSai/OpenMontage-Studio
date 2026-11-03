"""ElevenLabs Sound Effects V2 via fal, with a durable no-replay receipt."""
from __future__ import annotations

import hashlib
import json
import math
import os
import re
from pathlib import Path
from urllib.parse import urlparse

from tools.audio.fal_elevenlabs_music import FalElevenLabsMusic
from tools.base_tool import ToolResult
from tools.fal_media import _write_receipt
from tools.provider_jobs import download, poll, request_json


class FalElevenLabsSfx(FalElevenLabsMusic):
    name = "fal_elevenlabs_sfx"
    capability = "sound_effects_generation"
    _MODEL = "fal-ai/elevenlabs/sound-effects/v2"
    _QUEUE_URL = f"https://queue.fal.run/{_MODEL}"
    agent_skills = ["sound-effects"]
    fallback_tools = []
    capabilities = ["generate_sound_effects", "generate_ambience"]
    supports = {"loop": True, "duration_control": True}
    best_for = ["ambient and Foley sounds via fal"]
    not_good_for = ["speech", "music"]
    idempotency_key_fields = ["text", "duration_seconds", "prompt_influence", "loop"]
    input_schema = {
        "type": "object", "required": ["text", "duration_seconds", "output_path", "job_path"],
        "properties": {
            "text": {"type": "string", "minLength": 1},
            "duration_seconds": {"type": "number", "minimum": 0.5, "maximum": 22},
            "prompt_influence": {"type": "number", "minimum": 0, "maximum": 1, "default": 0.3},
            "loop": {"type": "boolean", "default": False},
            "output_path": {"type": "string"},
            "job_path": {"type": "string"},
            "poll_timeout": {"type": "number", "exclusiveMinimum": 0},
            "poll_interval": {"type": "number", "exclusiveMinimum": 0},
        },
    }
    side_effects = ["submits one paid fal job", "writes audio and durable receipt"]
    user_visible_verification = ["Inspect sound and measured duration"]

    def _build_payload(self, inputs):
        text = inputs.get("text")
        duration = inputs.get("duration_seconds")
        influence = inputs.get("prompt_influence", 0.3)
        loop = inputs.get("loop", False)
        if not isinstance(text, str) or not text.strip():
            raise ValueError("text is required")
        if isinstance(duration, bool) or not isinstance(duration, (int, float)) or not math.isfinite(duration) or not 0.5 <= duration <= 22:
            raise ValueError("duration_seconds must be between 0.5 and 22")
        if isinstance(influence, bool) or not isinstance(influence, (int, float)) or not math.isfinite(influence) or not 0 <= influence <= 1:
            raise ValueError("prompt_influence must be between 0 and 1")
        if not isinstance(loop, bool):
            raise ValueError("loop must be a boolean")
        return {"text": text, "duration_seconds": duration, "prompt_influence": influence,
                "loop": loop, "output_format": "mp3_44100_128"}

    def estimate_cost(self, inputs):
        return round(self._build_payload(inputs)["duration_seconds"] * 0.002, 6)

    @staticmethod
    def _queue_paths(job):
        request_id = job.get("request_id")
        if not isinstance(request_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", request_id):
            raise ValueError("Invalid request id")
        paths = []
        for field in ("status_url", "response_url"):
            value = job.get(field)
            if not isinstance(value, str):
                raise ValueError("Invalid queue endpoint")
            parsed = urlparse(value)
            if parsed.scheme != "https" or parsed.netloc != "queue.fal.run" or parsed.query or parsed.fragment:
                raise ValueError("Invalid queue endpoint")
            paths.append(parsed.path)
        status, response = paths
        if response not in {f"/fal-ai/elevenlabs/requests/{request_id}",
                            f"/fal-ai/elevenlabs/sound-effects/v2/requests/{request_id}"} or status != response + "/status":
            raise ValueError("Invalid queue endpoint")
        return status, response

    def execute(self, inputs):
        try:
            key = self._get_api_key()
            if not key:
                raise ValueError("FAL_KEY is not configured")
            payload = self._build_payload(inputs)
            if not inputs.get("job_path") or not inputs.get("output_path"):
                raise ValueError("job_path and output_path are required")
            receipt_path = Path(inputs["job_path"]).resolve()
            output = Path(inputs["output_path"]).resolve()
            if receipt_path in (output, output.with_name(output.name + ".part")):
                raise ValueError("Receipt and output must be distinct")
            timeout, interval = inputs.get("poll_timeout", 600), inputs.get("poll_interval", 2)
            if any(isinstance(x, bool) or not isinstance(x, (int, float)) or not math.isfinite(x) or x <= 0 for x in (timeout, interval)):
                raise ValueError("Poll timeout and interval must be positive")
            fingerprint = hashlib.sha256(json.dumps({"model": self._MODEL, "payload": payload}, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
            headers = {"Authorization": f"Key {key}"}
            try:
                saved = json.loads(receipt_path.read_text())
            except FileNotFoundError:
                saved = None
            if saved is None:
                _write_receipt(receipt_path, {"state": "submitting", "sha256": fingerprint, "model": self._MODEL}, exclusive=True)
                submitted = request_json("POST", self._QUEUE_URL, headers=headers, json=payload)
                request_id = submitted.get("request_id")
                if not isinstance(request_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", request_id):
                    raise ValueError("Invalid request id")
                # Persist the accepted identity even if queue URL validation or the next write fails.
                _write_receipt(receipt_path, {"state": "accepted_unverified", "sha256": fingerprint,
                                             "model": self._MODEL, "request_id": request_id})
                status_path, response_path = self._queue_paths(submitted)
                saved = {"state": "accepted", "sha256": fingerprint, "model": self._MODEL,
                         "request_id": submitted["request_id"], "status_path": status_path, "response_path": response_path}
                _write_receipt(receipt_path, saved)
            else:
                if not isinstance(saved, dict) or saved.get("sha256") != fingerprint or saved.get("model") != self._MODEL:
                    raise ValueError("Saved request differs; refusing replay")
                if saved.get("state") == "accepted_unverified" and saved.get("request_id"):
                    raise ValueError("Accepted job needs provider reconciliation")
                if saved.get("state") != "accepted" or not saved.get("request_id"):
                    raise ValueError("Acceptance unknown; reconcile before any replay")
                # Verify saved paths before using credentials, even on resume.
                self._queue_paths({"request_id": saved["request_id"],
                    "status_url": "https://queue.fal.run" + saved.get("status_path", ""),
                    "response_url": "https://queue.fal.run" + saved.get("response_path", "")})
            base = "https://queue.fal.run"
            poll(lambda: request_json("GET", base + saved["status_path"], headers=headers), timeout=timeout, interval=interval)
            result = request_json("GET", base + saved["response_path"], headers=headers)
            audio = result["audio"]["url"]
            downloaded = download(audio, output)
            return ToolResult(success=True, data={"provider": "fal.ai", "model": self._MODEL,
                "output": downloaded, "request_id": saved["request_id"], "job_path": str(receipt_path),
                "estimated_cost_usd": self.estimate_cost(inputs)}, artifacts=[downloaded],
                cost_usd=None, model=self._MODEL)
        except Exception as exc:
            safe = {"FAL_KEY is not configured", "text is required", "duration_seconds must be between 0.5 and 22",
                    "prompt_influence must be between 0 and 1", "loop must be a boolean", "job_path and output_path are required",
                    "Receipt and output must be distinct", "Poll timeout and interval must be positive",
                    "Saved request differs; refusing replay", "Acceptance unknown; reconcile before any replay",
                    "Accepted job needs provider reconciliation"}
            message = str(exc) if type(exc) is ValueError and str(exc) in safe else f"fal SFX stopped: {type(exc).__name__}; inspect receipt"
            return ToolResult(success=False, error=message)
