"""Lyria 3 Pro through the existing fal music queue and durable resume path."""

from copy import deepcopy

from tools.audio.fal_elevenlabs_music import FalElevenLabsMusic


class FalLyriaMusic(FalElevenLabsMusic):
    name = "fal_lyria_music"
    _MODEL = "fal-ai/lyria3/pro"
    _QUEUE_URL = f"https://queue.fal.run/{_MODEL}"
    agent_skills = ["lyria"]
    fallback_tools = []
    supports = {"instrumental": True, "style_control": True, "exact_duration": False}
    best_for = ["Lyria 3 Pro instrumental cues through an existing fal account"]
    input_schema = deepcopy(FalElevenLabsMusic.input_schema)
    input_schema["properties"]["duration_seconds"].update(
        minimum=5, maximum=184, description="Prompt-guided target; probe actual output"
    )

    def estimate_cost(self, inputs):
        # Published fal flat rate checked 27 October 2026; refresh before future work.
        return 0.08

    def _build_payload(self, inputs):
        duration = float(inputs["duration_seconds"])
        if not 5 <= duration <= 184:
            raise ValueError("Lyria target duration must be between 5 and 184 seconds")
        if not inputs.get("force_instrumental", True):
            raise ValueError("This adapter supports instrumental requests only")
        prompt = inputs["prompt"]
        if not 1 <= len(prompt) <= 5000:
            raise ValueError("Lyria prompt must contain 1 to 5000 characters")
        # Lyria has no native duration or force_instrumental fields.
        return {"prompt": prompt}

    def execute(self, inputs):
        result = super().execute(inputs)
        if result.success:
            result.data["instrumental_requested"] = result.data.pop("force_instrumental")
            result.data["duration_control"] = "prompt_only; measure provider output"
        return result
