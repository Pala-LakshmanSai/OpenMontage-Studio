"""AI33 asynchronous audio; persist acceptance before polling, never replay POSTs."""

from __future__ import annotations

import hashlib
import json
import os
import re
import time
from pathlib import Path
from typing import Any

import jsonschema
import requests

from tools.base_tool import (BaseTool, Determinism, ExecutionMode, ResourceProfile,
                             ResumeSupport, ToolResult, ToolRuntime, ToolStability,
                             ToolTier)
from tools.provider_jobs import download, poll, request_json, save_job
from tools.provider_pricing import PriceQuoteRequired


class AI33Audio(BaseTool):
    name = "ai33_audio"
    version = "0.1.0"
    tier = ToolTier.GENERATE
    capability = "audio_generation"
    provider = "ai33"
    stability = ToolStability.BETA
    execution_mode = ExecutionMode.ASYNC
    determinism = Determinism.STOCHASTIC
    runtime = ToolRuntime.API
    dependencies = ["env:AI33_API_KEY", "python:requests", "python:jsonschema"]
    install_instructions = "Set AI33_API_KEY in local .env; never include it in tool inputs."
    agent_skills = ["ai33-audio"]
    capabilities = ["text_to_speech", "generate_sound_effects", "generate_background_music"]
    supports = {"voice_selection": True, "looping_sfx": True, "instrumental": True}
    best_for = ["fixed-voice dialogue", "continuous ambience and Foley stems", "instrumental score"]
    not_good_for = ["lip-sync generation", "automatic replay of an uncertain submission"]
    resume_support = ResumeSupport.FROM_CHECKPOINT
    resource_profile = ResourceProfile(network_required=True)
    side_effects = ["paid AI33 task", "writes audio and resumable job receipt"]
    user_visible_verification = ["Listen to complete output; inspect duration and clean audio tails"]
    input_schema = {
        "type": "object", "additionalProperties": False,
        "required": ["operation", "output_path"],
        "properties": {
            "operation": {"type": "string", "enum": ["tts", "sfx", "music"]},
            "output_path": {"type": "string", "minLength": 1},
            "text": {"type": "string", "minLength": 1, "maxLength": 1000000},
            "voice_id": {"type": "string", "pattern": "^(elevenlabs|minimax|clone|edge|kokoro|vbee|fishaudio)_.+"},
            "speed": {"type": "number", "minimum": 0.5, "maximum": 1.5},
            "with_transcript": {"type": "boolean"},
            "duration_seconds": {"type": ["number", "null"], "minimum": 0.5, "maximum": 30},
            "prompt_influence": {"type": "number", "minimum": 0, "maximum": 1},
            "loop": {"type": "boolean"},
            "prompt": {"type": "string", "minLength": 1, "maxLength": 500},
            "instrumental": {"type": "boolean", "default": True},
            "track_index": {"type": "integer", "minimum": 0},
            "job_id": {"type": "string", "pattern": "^[A-Za-z0-9_-]+$"},
            "job_path": {"type": "string", "minLength": 1},
            "poll_timeout": {"type": "number", "exclusiveMinimum": 0},
            "poll_interval": {"type": "number", "exclusiveMinimum": 0},
            "project_dir": {"type": "string"},
            "scene_id": {"type": "string"},
        },
        "allOf": [
            {"if": {"not": {"required": ["job_id"]}}, "then": {
                "allOf": [
                    {"if": {"properties": {"operation": {"const": "tts"}}}, "then": {"required": ["text", "voice_id"]}},
                    {"if": {"properties": {"operation": {"const": "sfx"}}}, "then": {"required": ["text"], "properties": {"text": {"maxLength": 450}}}},
                    {"if": {"properties": {"operation": {"const": "music"}}}, "then": {"required": ["prompt"]}},
                ]}},
        ],
    }

    _BASE = "https://api.ai33.pro"

    def estimate_cost(self, inputs: dict[str, Any]) -> float:
        raise PriceQuoteRequired("AI33 bills credits; USD conversion and TTS/music tariff depend on the account. SFX: auto 200 credits, specified max(50, 50*seconds).")

    @staticmethod
    def _submission(inputs):
        operation = inputs["operation"]
        if operation == "tts":
            body = {"text": inputs["text"], "voice_id": inputs["voice_id"],
                    "speed": str(inputs.get("speed", 1)),
                    "with_transcript": str(inputs.get("with_transcript", False)).lower()}
            return "/v3/text-to-speech", {"files": {k: (None, v) for k, v in body.items()}}, body
        if operation == "sfx":
            body = {"text": inputs["text"], "model_id": "eleven_text_to_sound_v2",
                    "duration_seconds": inputs.get("duration_seconds"),
                    "prompt_influence": inputs.get("prompt_influence", 0.3), "loop": inputs.get("loop", False)}
            return "/v1/task/sound-effect", {"json": body}, body
        body = {"create_mode": "simple", "gpt_description_prompt": inputs["prompt"],
                "make_instrumental": inputs.get("instrumental", True)}
        return "/v1s/task/music-generation", {"json": body}, body

    def execute(self, inputs: dict[str, Any]) -> ToolResult:
        started = time.monotonic()
        job = {}
        try:
            jsonschema.validate(inputs, self.input_schema)
            self.check_dependencies()
            headers = {"xi-api-key": os.environ["AI33_API_KEY"]}
            output = Path(inputs["output_path"])
            job_path = Path(inputs.get("job_path", str(output) + ".ai33-job.json"))
            existing_receipt = job_path.exists()
            if existing_receipt:
                job = json.loads(job_path.read_text())
                if job.get("operation") != inputs["operation"]:
                    raise ValueError("Saved task operation differs from request")
            supplied_id = inputs.get("job_id")
            if supplied_id and job.get("job_id") not in (None, supplied_id):
                raise ValueError("Supplied job_id differs from saved task")
            job_id = supplied_id or job.get("job_id")
            if job_id:
                if not isinstance(job_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", job_id):
                    raise ValueError("Invalid saved job id")
                can_check_payload = (inputs["operation"] == "tts" and "text" in inputs and "voice_id" in inputs) or (inputs["operation"] == "sfx" and "text" in inputs) or (inputs["operation"] == "music" and "prompt" in inputs)
                if job.get("payload_sha256") and can_check_payload:
                    payload = self._submission(inputs)[2]
                    digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                    if digest != job["payload_sha256"]:
                        raise ValueError("Saved job payload differs; resume the original inputs")
                job.update(operation=inputs["operation"], job_id=job_id)
            else:
                if existing_receipt:
                    raise ValueError("Submission outcome is uncertain or rejected; do not replay. Reconcile provider tasks first.")
                route, kwargs, payload = self._submission(inputs)
                digest = hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()
                job = {"provider": "ai33", "operation": inputs["operation"], "status": "submitting", "payload_sha256": digest}
                # A crash/timeout during POST must leave a durable no-replay marker.
                job_path.parent.mkdir(parents=True, exist_ok=True)
                with job_path.open("x", encoding="utf-8") as receipt:
                    json.dump(job, receipt, indent=2)
                    receipt.flush()
                    os.fsync(receipt.fileno())
                response = request_json("POST", self._BASE + route, headers=headers, **kwargs)
                if not response.get("success") or not response.get("task_id"):
                    raise RuntimeError("AI33 did not confirm a task id; reconcile provider tasks before any resubmission")
                job_id = response["task_id"]
                if not isinstance(job_id, str) or not re.fullmatch(r"[A-Za-z0-9_-]+", job_id):
                    raise RuntimeError("AI33 returned an invalid task id")
                job.update(job_id=job_id, status="accepted")
            save_job(job_path, job)

            def fetch():
                response = request_json("GET", f"{self._BASE}/v1/task/{job_id}", headers=headers)
                status = response.get("status", "")
                job["status"] = status
                if "credit_cost" in response:
                    job["credit_cost"] = response["credit_cost"]
                save_job(job_path, job)
                # Shared poll accepts completed; AI33 calls the same state done.
                return {**response, "status": "completed" if status == "done" else status,
                        "error": "AI33 task failed"}

            response = poll(fetch, timeout=inputs.get("poll_timeout", 900), interval=inputs.get("poll_interval", 3))
            metadata = response.get("metadata") or {}
            if isinstance(metadata, str):
                metadata = json.loads(metadata)
            urls = metadata.get("all_audio_urls") or []
            index = inputs.get("track_index", 0)
            if urls:
                if index >= len(urls):
                    raise ValueError("track_index exceeds returned tracks")
                url = urls[index]
            else:
                if index:
                    raise ValueError("Provider returned only one audio track")
                url = response.get("output_uri") or metadata.get("output_uri") or metadata.get("audio_url")
            if not url:
                raise RuntimeError("Completed task has no final audio URL")
            download(url, output)
            job.update(status="done", output_path=str(output))
            save_job(job_path, job)
            return ToolResult(success=True, data={**job, "output": str(output), "job_path": str(job_path)},
                              artifacts=[str(output), str(job_path)], cost_usd=None,
                              duration_seconds=time.monotonic() - started, model="ai33/" + inputs["operation"])
        except Exception as exc:
            # Provider error bodies and request exceptions must never leak auth or signed URLs.
            if isinstance(exc, (ValueError, jsonschema.ValidationError)):
                error = "Input schema validation failed" if isinstance(exc, jsonschema.ValidationError) else "Invalid input or saved job: " + str(exc)
            elif isinstance(exc, requests.HTTPError):
                error = f"AI33 HTTP {exc.response.status_code}; retained task receipt, do not resubmit"
            elif isinstance(exc, TimeoutError):
                error = "AI33 task pending; resume this job_id/job_path, do not resubmit"
            else:
                error = f"AI33 {type(exc).__name__}; retained task receipt, do not resubmit"
            return ToolResult(success=False, error=error, data=job, cost_usd=None,
                              duration_seconds=time.monotonic() - started)
