"""Schema-backed fal media jobs with explicit endpoint selection and resume."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from abc import abstractmethod
from pathlib import Path
from urllib.parse import urlparse

from jsonschema import Draft202012Validator

from tools.provider_pricing import PriceQuoteRequired

from tools.base_tool import (
    BaseTool,
    ToolTier,
    ToolRuntime,
    ToolStability,
    ToolStatus,
    Determinism,
    ResourceProfile,
    ResumeSupport,
    ToolResult,
)
from tools.provider_jobs import request_json, download, poll

CONTRACTS = json.loads(
    (Path(__file__).parent / "provider_contracts/fal_models.json").read_text(
        encoding="utf-8"
    )
)


def _write_receipt(path: Path, receipt: dict, *, exclusive: bool = False) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    data = json.dumps(receipt, sort_keys=True).encode("utf-8")
    if exclusive:
        fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
        with os.fdopen(fd, "wb") as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
    else:
        fd, temporary = tempfile.mkstemp(dir=path.parent, prefix=".fal-job-")
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(data)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(temporary, path)
        finally:
            if os.path.exists(temporary):
                os.unlink(temporary)
    directory_fd = os.open(path.parent, os.O_RDONLY)
    try:
        os.fsync(directory_fd)
    finally:
        os.close(directory_fd)


class FalMedia(BaseTool):
    provider = "fal.ai"
    runtime = ToolRuntime.API
    tier = ToolTier.GENERATE
    stability = ToolStability.BETA
    determinism = Determinism.STOCHASTIC
    dependencies = ["env:FAL_KEY"]
    install_instructions = "Configure FAL_KEY using https://fal.ai/dashboard/keys."
    resource_profile = ResourceProfile(network_required=True)
    resume_support = ResumeSupport.FROM_CHECKPOINT
    agent_skills = ["provider-model-refresh"]
    side_effects = [
        "submits a paid fal job",
        "writes media and optional job checkpoint",
    ]
    user_visible_verification = ["Inspect generated media and provider provenance"]
    idempotency_key_fields = [
        "model",
        "operation",
        "generation_mode",
        "prompt",
        "image_urls",
        "mask_url",
        "seed",
        "duration",
        "resolution",
        "provider_params",
    ]

    @property
    @abstractmethod
    def routes(self):
        """Map public model names to operation -> exact fal endpoint."""

    def __init__(self):
        models = list(self.routes)
        props = {}
        for routes in self.routes.values():
            for endpoint in routes.values():
                props.update(CONTRACTS[endpoint]["input_schema"]["properties"])
        # Full endpoint-specific validation happens before submitting a job.
        props = {
            key: {"description": value.get("description", key)}
            for key, value in props.items()
        }
        props.update(
            {
                "model": {"type": "string", "enum": models, "default": models[0]},
                "operation": {"type": "string"},
                "generation_mode": {"type": "string"},
                "image_url": {"type": "string"},
                "image_path": {"type": "string"},
                "mask_path": {"type": "string"},
                "image_paths": {"type": "array", "items": {"type": "string"}},
                "provider_params": {"type": "object"},
                "resume_job": {"type": "object"},
                "job_path": {"type": "string"},
                "output_path": {"type": "string"},
                "poll_timeout": {"type": "number", "exclusiveMinimum": 0},
                "poll_interval": {"type": "number", "exclusiveMinimum": 0},
            }
        )
        self.input_schema = {"type": "object", "properties": props}
        self.idempotency_key_fields = sorted(
            set(props)
            - {"resume_job", "job_path", "output_path", "poll_timeout", "poll_interval"}
        )

    def get_status(self):
        return (
            ToolStatus.AVAILABLE
            if os.getenv("FAL_KEY") or os.getenv("FAL_AI_API_KEY")
            else ToolStatus.UNAVAILABLE
        )

    def get_info(self):
        info = super().get_info()
        info["hosting_provider"] = "fal.ai"
        info["model_catalog"] = {
            m: {
                "routes": r,
                "verified_on": "2026-10-03",
                "pricing_status": "quote_required",
            }
            for m, r in self.routes.items()
        }
        return info

    def estimate_cost(self, inputs):
        # No fabricated per-image/per-second rates. Callers must obtain a quote.
        raise PriceQuoteRequired(
            "A current fal price quote is required for this model/operation"
        )

    def build_request(self, inputs):
        model = inputs.get("model", next(iter(self.routes)))
        references = any(
            inputs.get(k)
            for k in ("image_path", "image_paths", "image_url", "image_urls")
        )
        operation = (
            inputs.get("generation_mode")
            or inputs.get("operation")
            or (
                "edit"
                if references and self.capability == "image_generation"
                else "image_to_video"
                if references
                else next(iter(self.routes.get(model, {})), "")
            )
        )
        if operation == "generate":
            operation = (
                "generate"
                if "generate" in self.routes.get(model, {})
                else "text_to_video"
            )
        endpoint = self.routes.get(model, {}).get(operation)
        if not endpoint:
            raise ValueError(f"Unsupported model/operation: {model}/{operation}")
        schema = CONTRACTS[endpoint]["input_schema"]
        props = schema["properties"]
        payload = {k: v for k, v in inputs.items() if k in props}
        native = inputs.get("provider_params", {})
        if not isinstance(native, dict):
            raise ValueError("provider_params must be an object")
        payload.update(native)
        if "prompt_expansion_mode" in props:
            payload.setdefault("prompt_expansion_mode", "balanced")
        if inputs.get("image_url") and "start_image_url" in props:
            payload["start_image_url"] = inputs["image_url"]
        if inputs.get("image_url") and "image_urls" in props:
            payload["image_urls"] = [
                inputs["image_url"],
                *payload.get("image_urls", []),
            ]
        if inputs.get("mask_path"):
            if "mask_url" not in props:
                raise ValueError(f"{endpoint} does not accept a mask")
            from tools.schema_media import local_image

            payload["mask_url"] = local_image(inputs["mask_path"])
        paths = list(inputs.get("image_paths") or [])
        if inputs.get("image_path"):
            paths.insert(0, inputs["image_path"])
        if paths:
            import mimetypes, base64

            refs = [
                "data:"
                + (mimetypes.guess_type(p)[0] or "image/png")
                + ";base64,"
                + base64.b64encode(Path(p).read_bytes()).decode()
                for p in paths
            ]
            if "image_urls" in props:
                payload["image_urls"] = list(payload.get("image_urls") or []) + refs
            elif len(refs) == 1 and (
                "image_url" in props or "start_image_url" in props
            ):
                if payload.get("image_url") or payload.get("start_image_url"):
                    raise ValueError(
                        "This route accepts one source image; do not combine URL and local path"
                    )
                payload[
                    "start_image_url" if "start_image_url" in props else "image_url"
                ] = refs[0]
            else:
                raise ValueError("This route does not support the supplied image paths")
        if inputs.get("generate_audio") is not None and "audio" in props:
            payload["audio"] = inputs["generate_audio"]
        if inputs.get("n") is not None and "num_images" in props:
            payload["num_images"] = inputs["n"]
        if operation == "precise_edit":
            payload["edit_precision"] = "high"
        for key in (
            "image_url",
            "image_urls",
            "mask_url",
            "reference_image_urls",
            "reference_video_urls",
            "reference_audio_urls",
            "target_audio_url",
        ):
            if (
                inputs.get(key)
                and key not in props
                and not (
                    key == "image_url"
                    and ("start_image_url" in props or "image_urls" in props)
                )
            ):
                raise ValueError(f"{endpoint} does not accept {key}")
        Draft202012Validator(schema).validate(payload)
        if payload.get("mask_url") and len(payload.get("reference_image_urls", [])) > 3:
            raise ValueError(
                "Masked Ideogram edits allow at most three reference images"
            )
        if (payload.get("web_url") or payload.get("file_url")) and not payload.get(
            "enable_thinking"
        ):
            raise ValueError("web_url/file_url requires enable_thinking")
        return model, operation, endpoint, payload

    def execute(self, inputs):
        job = dict(inputs.get("resume_job") or {})
        try:
            key = os.getenv("FAL_KEY") or os.getenv("FAL_AI_API_KEY")
            if not key:
                raise ValueError("FAL_KEY is not configured")
            headers = {"Authorization": f"Key {key}"}
            job_path = (
                Path(inputs["job_path"]).resolve() if inputs.get("job_path") else None
            )
            if job_path:
                local_inputs = [inputs.get("image_path"), inputs.get("mask_path")]
                local_inputs.extend(inputs.get("image_paths") or [])
                extension = (
                    ".mp4"
                    if self.capability == "video_generation"
                    else "." + inputs.get("output_format", "png")
                )
                proposed_output = Path(inputs.get("output_path") or self.name + extension)
                local_inputs.extend(
                    [proposed_output, proposed_output.with_name(proposed_output.name + ".part")]
                )
                if any(p and Path(p).resolve() == job_path for p in local_inputs):
                    raise ValueError("Job receipt must not overwrite media input or output")
                try:
                    receipt = json.loads(job_path.read_text(encoding="utf-8"))
                except FileNotFoundError:
                    receipt = None
                legacy_fields = {
                    "request_id", "status_url", "response_url", "model",
                    "operation", "endpoint", "tool",
                }
                if isinstance(receipt, dict) and set(receipt) == legacy_fields:
                    # Legacy receipts cannot prove their original payload. Poll only
                    # when the caller supplies the identical accepted job, without
                    # presenting unverifiable request fields as a matching payload.
                    resume_fields = {"resume_job", "job_path", "output_path", "poll_timeout", "poll_interval"}
                    if not job or job != receipt or set(inputs) - resume_fields:
                        raise ValueError("Legacy receipt requires matching resume job without request inputs")
                    if not all(isinstance(receipt[k], str) and receipt[k] for k in legacy_fields):
                        raise ValueError("Legacy receipt lacks a complete job identity")
                    job = receipt
                else:
                    model, operation, endpoint, payload = self.build_request(inputs)
                    fingerprint = hashlib.sha256(
                        json.dumps(
                            {"model": model, "operation": operation, "endpoint": endpoint, "payload": payload},
                            sort_keys=True,
                            separators=(",", ":"),
                            ensure_ascii=False,
                        ).encode("utf-8")
                    ).hexdigest()
                    if receipt is None:
                        if job:
                            raise ValueError("Cannot bind a supplied resume job to a missing receipt")
                        try:
                            _write_receipt(
                                job_path,
                                {"state": "submitting", "sha256": fingerprint},
                                exclusive=True,
                            )
                        except FileExistsError:
                            raise ValueError("Job receipt already exists; inspect it before resuming")
                    else:
                        if not isinstance(receipt, dict) or receipt.get("sha256") != fingerprint:
                            raise ValueError("Saved request differs; refusing replay")
                        if receipt.get("state") != "accepted" or not receipt.get("request_id"):
                            raise ValueError("Acceptance unknown; reconcile before any replay")
                        if job and job != receipt:
                            raise ValueError("Supplied resume job differs from saved receipt")
                        job = receipt
            if not job:
                if not job_path:
                    model, operation, endpoint, payload = self.build_request(inputs)
                submitted = request_json(
                    "POST",
                    f"https://queue.fal.run/{endpoint}",
                    headers=headers,
                    json=payload,
                )
                job = {
                    k: submitted[k]
                    for k in ("request_id", "status_url", "response_url")
                }
                job.update(
                    model=model, operation=operation, endpoint=endpoint, tool=self.name
                )
                if job_path:
                    job.update(state="accepted", sha256=fingerprint)
                    _write_receipt(job_path, job)
            if job.get("tool") != self.name or self.routes.get(
                job.get("model"), {}
            ).get(job.get("operation")) != job.get("endpoint"):
                raise ValueError("Resume job belongs to a different tool or endpoint")
            for field in ("status_url", "response_url"):
                parsed = urlparse(job[field])
                if parsed.scheme != "https" or parsed.netloc != "queue.fal.run":
                    raise ValueError("Invalid fal job URL")
            poll(
                lambda: request_json("GET", job["status_url"], headers=headers),
                timeout=float(inputs.get("poll_timeout", 600)),
                interval=float(inputs.get("poll_interval", 2)),
            )
            result = request_json("GET", job["response_url"], headers=headers)
            values = result.get("images") or (
                [result["video"]]
                if result.get("video")
                else [result["audio"]]
                if result.get("audio")
                else []
            )
            if not values:
                raise ValueError("Completed job returned no media")
            ext = (
                ".mp4"
                if self.capability == "video_generation"
                else "." + inputs.get("output_format", "png")
            )
            path = Path(inputs.get("output_path") or self.name + ext)
            output_paths = [
                path if i == 0 else path.with_name(f"{path.stem}_{i + 1}{path.suffix}")
                for i in range(len(values))
            ]
            if job_path and any(
                job_path in {p.resolve(), p.with_name(p.name + ".part").resolve()}
                for p in output_paths
            ):
                raise ValueError("Job receipt must not overwrite media input or output")
            outputs = [
                download(v["url"], output_paths[i]) for i, v in enumerate(values)
            ]
            return ToolResult(
                success=True,
                data={
                    "provider": self.provider,
                    "hosting_provider": "fal.ai",
                    "model": job["model"],
                    "operation": job["operation"],
                    "output": outputs[0],
                    "outputs": outputs,
                    "resume_job": job,
                    "cost_status": "unquoted",
                    "provider_result": result,
                },
                artifacts=outputs,
                cost_usd=None,
                model=job["model"],
            )
        except Exception as exc:
            if inputs.get("job_path"):
                safe_errors = {
                    "FAL_KEY is not configured",
                    "Job receipt must not overwrite media input or output",
                    "Cannot bind a supplied resume job to a missing receipt",
                    "Job receipt already exists; inspect it before resuming",
                    "Saved request differs; refusing replay",
                    "Acceptance unknown; reconcile before any replay",
                    "Supplied resume job differs from saved receipt",
                    "Legacy receipt requires matching resume job without request inputs",
                    "Legacy receipt lacks a complete job identity",
                    "Resume job belongs to a different tool or endpoint",
                    "Invalid fal job URL",
                }
                message = (
                    str(exc)
                    if type(exc) is ValueError and str(exc) in safe_errors
                    else f"Fal job stopped: {type(exc).__name__}; inspect the receipt"
                )
                return ToolResult(
                    success=False, error=message, data={"resume_job": job} if job else {}
                )
            return ToolResult(
                success=False, error=str(exc), data={"resume_job": job} if job else {}
            )
