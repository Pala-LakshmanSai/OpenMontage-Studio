---
name: minimax-h3
description: |
  Generate MiniMax H3 (Hailuo 3.0) video through the official MiniMax v2 API, fal.ai, Runway, ComfyUI Partner Nodes, or local open weights in ComfyUI. Use for 4-15 second 2K clips, first/last-frame animation, and image/video/audio reference-conditioned video.
---

# MiniMax H3

MiniMax H3 is the Hailuo 3.0 family. The first-party API identifier is
`MiniMax-H3`; fal.ai exposes the family as `hailuo-03`, and Runway uses
`hailuo3`. Do not substitute one provider's identifier into another API.

## Choose a route

| Route | Tool call | Execution |
|-------|-----------|-----------|
| MiniMax direct | `minimax_video`, `model: "MiniMax-H3"` | Hosted first-party v2 API; global or mainland-China region |
| fal.ai | `minimax_fal_video` | Hosted gateway; T2V, I2V, reference-to-video |
| Runway | `runway_video`, `model: "hailuo3"` | Hosted; 768P or 2K, 5–15 seconds |
| ComfyUI Partner Node | `comfyui_video`, `model_family: "minimax_h3_api"` | Hosted and billed in Comfy credits |
| ComfyUI open weights | `comfyui_video`, `model_family: "minimax_h3_local"` | Local GPU with official workflow and model stack |

For local ComfyUI, export the official workflow in API format and pass
`workflow_json` or `workflow_path` plus `output_node`. OpenMontage reports the
required diffusion model, Qwen3-VL text encoder, video VAE, and audio VAE; it
does not silently download large weights.

## Operations and prompting

- Text-to-video: concrete ratio; do not use `adaptive` without visual input.
- Image-to-video: provide a first frame.
- First/last-frame: provide both images and describe the motion between them.
- Reference-to-video: images, videos, and audio can be combined. Audio needs at
  least one visual reference.

Write prompts as subject + action + camera path + environment + lighting +
audio intent. MiniMax responds well to explicit camera direction. Keep the
requested motion achievable within 4–15 seconds and inspect native audio as
carefully as the image track.

## Provider differences

fal's `h3_max_video` also accepts `model: "h3-max-turbo"` for text-to-video
and first-frame image-to-video. Verified 2026-10-10 against fal's live schemas.
Turbo has no reference-to-video route or image/audio reference arrays. Reuse
shot anchors for continuity; `target_audio_url` replaces the soundtrack and
does not establish voice conditioning or lip-sync. At 768P the public output
rate is $0.04/second, versus Max's $0.08/second; verify before paid work.
Source: https://fal.ai/models/minimax/h3-max-turbo/image-to-video/api

For continuity-critical Turbo shots explicitly use `prompt_expansion_mode:
"disabled"`. `balanced` is the gateway default and may reinterpret the cast.
Verified failure on 2026-10-10: a prompt describing an offscreen prone prisoner
was expanded into a visible background prisoner, then generated upright despite
an empty-background anchor. Separate visible cast from offscreen state; preserve
posture and visibility explicitly. Review the saved expanded prompt and dense
video frames. Same seed or starting frame does not guarantee consistency.

The direct MiniMax v2 route currently outputs 2K and supports 4–15 seconds.
Runway's Hailuo 3.0 route supports 768P/2K and documents 5–15 seconds. Partner
Nodes require network access and credits. Only the open-weight ComfyUI route is
local/offline after all models are installed.

## Native dialogue and actual conditioning

The Prisoner final mix kept jointly generated native H3 Max speech with its video;
AI33 files were intended voice references. Old request receipts do not prove
transport of their local reference_audio_paths. The Warning native redo instead
passes explicit reference_audio_urls through reference-to-video, using J1TTS
voices as guidance. The generic fal adapter does not convert reference_audio_paths;
upload local references through the official SDK and inspect build_request.
Never replace native on-screen speech with independently timed TTS and call it
synced. Native takes can repeat lines or reconstruct hidden hands/props despite
prompts: review the whole take, preserve paired timing, trim complete first
utterances or regenerate failures, and validate visible coverage/backgrounds.
Reference voices guide timbre; they do not guarantee an exact fixed voice clone.

User acceptance, 10 October2026: the user endorsed the repaired THE WARNING native
dialogue lip-sync and requested this method for future AI movies. Preserve native
paired speech/video; J1TTS is guiding speech, Turbo remains non-speaking default.
This is30s user acceptance, not a guarantee for arbitrary cast/runtime.
