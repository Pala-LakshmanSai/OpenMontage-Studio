"""fal's post-trained H3 Max; deliberately distinct from MiniMax H3."""

from tools.fal_media import FalMedia


class H3MaxVideo(FalMedia):
    name = "h3_max_video"
    capability = "video_generation"
    capabilities = ["text_to_video", "image_to_video", "reference_to_video"]
    supports = dict.fromkeys(
        ["text_to_video", "image_to_video", "reference_to_video", "native_audio"], True
    )
    best_for = ["Fast H3 Max drafts and final clips with reference control"]
    routes = {
        "h3-max": {op: f"minimax/h3-max/{op.replace('_', '-')}" for op in capabilities},
        "h3-max-turbo": {
            op: f"minimax/h3-max-turbo/{op.replace('_', '-')}"
            for op in ("text_to_video", "image_to_video")
        },
    }

    def build_request(self, inputs):
        model, operation, endpoint, payload = super().build_request(inputs)
        if operation == "reference_to_video" and not any(
            payload.get(key)
            for key in (
                "reference_image_urls",
                "reference_video_urls",
                "reference_audio_urls",
            )
        ):
            raise ValueError(
                "H3 Max reference-to-video requires a separate image, video, "
                "or audio reference; a starting keyframe alone is insufficient. "
                "Use image_to_video for a starting image without references."
            )
        return model, operation, endpoint, payload
