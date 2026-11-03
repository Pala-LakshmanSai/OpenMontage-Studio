"""J1TTS narration with durable acceptance and no ambiguous submission replay."""
from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path

import jsonschema
import requests

from tools.base_tool import (BaseTool, Determinism, ExecutionMode, ResourceProfile,
                             ResumeSupport, ToolResult, ToolRuntime, ToolStability,
                             ToolTier)
from tools.provider_jobs import save_job
from tools.provider_pricing import PriceQuoteRequired


class J1TTSAudio(BaseTool):
    name = "j1tts_audio"
    version = "0.1.0"
    tier = ToolTier.VOICE
    capability = "tts"
    provider = "j1tts"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.ASYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API
    dependencies = ["env:J1TTS_API_KEY", "python:requests", "python:jsonschema"]
    install_instructions = "Set J1TTS_API_KEY in a private .env."
    agent_skills = ["j1tts-audio"]
    capabilities = ["text_to_speech", "list_voices", "import_voice"]
    supports = {"voice_selection": True}
    resume_support = ResumeSupport.FROM_CHECKPOINT
    resource_profile = ResourceProfile(network_required=True)
    side_effects = ["creates J1TTS jobs or imports voices", "writes audio and job receipts"]
    user_visible_verification = ["Play output and verify words, voice and pacing"]
    input_schema = {
        "type": "object", "additionalProperties": False, "required": ["operation"],
        "properties": {
            "operation": {"enum": ["voices", "import", "tts"]},
            "voice_id": {"type": "string", "pattern": "^[A-Za-z0-9_-]{1,160}$"},
            "text": {"type": "string", "minLength": 1},
            "file_name": {"type": "string", "pattern": "^[A-Za-z0-9_.-]+$"},
            "output_path": {"type": "string", "minLength": 1},
            "job_path": {"type": "string", "minLength": 1},
            "job_id": {"type": "string", "pattern": "^[A-Za-z0-9_-]{1,160}$"},
            "poll_timeout": {"type": "number", "exclusiveMinimum": 0},
            "poll_interval": {"type": "number", "exclusiveMinimum": 0},
            "project_dir": {"type": "string"}, "scene_id": {"type": "string"},
        },
        "allOf": [
            {"if": {"properties": {"operation": {"const": "tts"}}},
             "then": {"required": ["output_path"]}},
            {"if": {"properties": {"operation": {"const": "import"}}},
             "then": {"required": ["voice_id", "job_path"]}},
        ],
    }
    _BASE = "https://api.j1tts.com"

    def estimate_cost(self, inputs):
        if inputs.get("operation") == "voices":
            return 0.0
        raise PriceQuoteRequired("J1TTS depends on the user's plan; this user's unlimited plan has $0 reported incremental TTS cost.")

    def _request(self, method, path, **kwargs):
        r = requests.request(method, self._BASE + path, headers={
            "Authorization": "Bearer " + os.environ["J1TTS_API_KEY"],
            "User-Agent": "OpenMontage/1.0",
        }, allow_redirects=False, timeout=(10, 300 if path.endswith("/download") else 30), **kwargs)
        if 300 <= r.status_code < 400:
            raise RuntimeError("J1TTS redirect rejected")
        r.raise_for_status()
        return r

    def _voices(self):
        voices = {}
        for path in ["/v1/voices", "/v1/my-voices"]:
            data = self._request("GET", path).json()
            rows = data if isinstance(data, list) else data.get("voices")
            if not isinstance(rows, list):
                raise ValueError("Invalid voice catalog")
            for v in rows:
                if isinstance(v, dict) and re.fullmatch(r"[A-Za-z0-9_-]{1,160}", str(v.get("voice_id", ""))):
                    voices[v["voice_id"]] = v
        return list(voices.values())

    def execute(self, inputs):
        started = time.monotonic()
        job = {}
        try:
            jsonschema.validate(inputs, self.input_schema)
            self.check_dependencies()
            op = inputs["operation"]
            if op == "voices":
                return ToolResult(success=True, data={"voices": self._voices()}, cost_usd=0)
            output = Path(inputs.get("output_path", "."))
            receipt = Path(inputs.get("job_path", str(output) + ".j1tts-job.json"))
            if receipt.exists():
                job = json.loads(receipt.read_text())
                if job.get("operation") != op:
                    raise ValueError("Saved operation mismatch")
            if op == "import":
                voice_id = inputs["voice_id"]
                if job and job.get("voice_id") != voice_id:
                    raise ValueError("Saved voice id mismatch; preserve original import")
                available = self._voices()
                if not any(v["voice_id"] == voice_id for v in available):
                    if job:
                        raise ValueError("Import acceptance unresolved; do not replay")
                    job = {"provider": "j1tts", "operation": op, "voice_id": voice_id, "status": "submitting"}
                    save_job(receipt, job)
                    try:
                        self._request("POST", "/v1/voices/import", json={"voice_ids": voice_id})
                    except (requests.RequestException, RuntimeError):
                        # Already-imported and uncertain responses require exact-ID readback.
                        pass
                    available = self._voices()
                found = next((v for v in available if v["voice_id"] == voice_id), None)
                if not found:
                    raise ValueError("Requested voice unavailable after import; do not replay")
                job.update(provider="j1tts", operation=op, voice_id=voice_id, status="available")
                save_job(receipt, job)
                return ToolResult(success=True, data={"voice": found, **job}, artifacts=[str(receipt)], cost_usd=None)
            payload = None
            if "text" in inputs and "voice_id" in inputs:
                payload = {"text": inputs["text"], "voice_id": inputs["voice_id"],
                           "file_name": inputs.get("file_name", output.stem)}
                digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                if job.get("payload_sha256") and job["payload_sha256"] != digest:
                    raise ValueError("Saved payload mismatch; preserve original inputs")
            job_id = inputs.get("job_id") or job.get("job_id")
            if inputs.get("job_id") and job.get("job_id") not in (None, job_id):
                raise ValueError("Saved job id mismatch")
            if not job_id:
                if job:
                    raise ValueError("Submission acceptance unresolved; do not replay")
                if payload is None:
                    raise ValueError("New TTS requires text and voice_id")
                job = {"provider": "j1tts", "operation": op, "status": "submitting", "payload_sha256": digest,
                       "voice_id": inputs["voice_id"], "submitted_at": time.time()}
                receipt.parent.mkdir(parents=True, exist_ok=True)
                with receipt.open("x") as f:
                    json.dump(job, f); f.flush(); os.fsync(f.fileno())
                data = self._request("POST", "/v1/tts", json=payload).json()
                job_id = data.get("id")
                if not isinstance(job_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]{1,160}", job_id):
                    raise ValueError("No confirmed job id; do not replay")
            if not re.fullmatch(r"[A-Za-z0-9_-]{1,160}", job_id):
                raise ValueError("Invalid saved job id")
            job.update(provider="j1tts", operation=op, job_id=job_id)
            save_job(receipt, job)
            if job.get("status") == "completed" and output.is_file() and job.get("output_sha256") == hashlib.sha256(output.read_bytes()).hexdigest():
                return ToolResult(success=True, data=job, artifacts=[str(output), str(receipt)], cost_usd=None)
            deadline = time.monotonic() + inputs.get("poll_timeout", 900)
            while time.monotonic() < deadline:
                data = self._request("GET", "/v1/tts/" + job_id).json()
                if data.get("id") != job_id:
                    raise ValueError("Provider job identity mismatch")
                job["status"] = data.get("status")
                save_job(receipt, job)
                if job["status"] == "failed":
                    raise RuntimeError("J1TTS generation failed")
                if job["status"] == "completed":
                    break
                time.sleep(inputs.get("poll_interval", 3))
            else:
                raise TimeoutError("Known task pending; resume exact job")
            r = self._request("GET", "/v1/tts/" + job_id + "/download", stream=True)
            if any(x in r.headers.get("content-type", "") for x in ["text/", "json"]):
                raise ValueError("Provider returned non-audio")
            output.parent.mkdir(parents=True, exist_ok=True)
            temp = output.with_suffix(output.suffix + ".part")
            with temp.open("wb") as f:
                for chunk in r.iter_content(1024 * 1024):
                    f.write(chunk)
            if temp.stat().st_size == 0:
                raise ValueError("Empty audio")
            temp.replace(output)
            job.update(output_path=str(output), output_sha256=hashlib.sha256(output.read_bytes()).hexdigest(), completed_at=time.time())
            save_job(receipt, job)
            return ToolResult(success=True, data=job, artifacts=[str(output), str(receipt)], cost_usd=None,
                              duration_seconds=time.monotonic()-started, model="j1tts/provider-default")
        except Exception as e:
            error = f"J1TTS HTTP {e.response.status_code}" if isinstance(e, requests.HTTPError) else (str(e) if isinstance(e, ValueError) else "J1TTS " + type(e).__name__)
            if isinstance(e, jsonschema.ValidationError): error = "J1TTS input schema invalid"
            return ToolResult(success=False, error=error, data=job, cost_usd=None, duration_seconds=time.monotonic()-started)
