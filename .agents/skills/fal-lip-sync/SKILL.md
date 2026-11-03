---
name: fal-lip-sync
description: Synchronize fixed J1TTS character speech to generated video through fal Sync Lipsync 2 Pro.
---

# fal lip-sync

Qualification warning, 10 October2026: the user rejected perceived lip-sync on
THE WARNING Asha/Elias faces despite successful API, timing, ASR and frame checks.
Do not use this postprocessor as the default AI-movie dialogue route or describe
that technical pass as perceptual acceptance. The requested alternative generates
native speech and picture jointly with H3 Max audio references and preserves the
paired native audio. Exact voice cloning/phoneme quality still needs review.

Use `fal_lip_sync` after the cinematic assets director. This is a postprocessing
step, not another video-generation model or voice provider. Main footage remains
the selected H3 model; speech remains J1TTS.

Exact endpoint: `fal-ai/sync-lipsync/v2/pro`. Inputs are video_url, audio_url and
sync_mode (`cut_off`). Upload local MP4/WAV with official `fal_client.upload_file`
and send returned HTTPS CDN URLs. Live 10 October2026 validation rejected both
inline data URIs with422 despite generic API examples suggesting their support.
FAL_KEY uses Key auth at queue.fal.run and the official SDK handles CDN upload auth.
Source video and padded speech must have equal durations;
no looping, bounce, remapping or truncated words. Published 10 October 2026 quote
is $5/minute of processed video; recheck before spending, retain quoted cost as
an estimate rather than settled billing.

Use isolated single-speaker coverage with an unobstructed near-frontal face.
Keep the counterpart offscreen in its established state. Render/normalize frame
cadence and speech timing BEFORE sync. Preserve padded original speech and mux
that same speech in the final film; exclude any unrelated native audio. Do not
retime picture separately after syncing. The adapter saves a submitting marker
and exact source hashes before POST; accepted request IDs resume polling and
download. Unknown acceptance never permits another POST. Preserve receipts.

Test one actual face before batching; humanoid alien skin/anatomy remains an
unqualified edge case until reviewed. Review dense speaking frames and normal
speed playback for onset, closures and word timing, face identity, teeth, jaw
jitter and expression. ASR only checks words. Do not claim exact phoneme sync
from metadata or thumbnails; reject failed speaking shots rather than substituting
a narration-only film.

Primary API/pricing: https://fal.ai/models/fal-ai/sync-lipsync/v2/pro/api
and https://fal.ai/models/fal-ai/sync-lipsync/v2/pro
File handling: https://fal.ai/docs/documentation/model-apis/fal-cdn
