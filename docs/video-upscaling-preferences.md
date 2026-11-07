# Video upscaling — owner preference

Saved 4 November 2026. Applies across all video styles and projects.

Use **ByteDance's video upscaling API only** for requested video enhancement.
The installed route is `fal_bytedance_upscale`, hosted by fal.ai. Do not substitute
FFmpeg resizing, Real-ESRGAN, Topaz or another model/provider as the upscale.
If ByteDance is unavailable, preserve accepted work and report the actual block;
do not silently switch. This is the owner's provider choice, not a comparative
quality guarantee.

Retain the current resolution-selection rule: production defaults to 720p/768p;
ask for an unspecified higher upscale target. For the revised lizard movie the
owner explicitly selected 1080p. Do not infer a universal 1080p or 4K target.

For clean generated movies, use the validated Standard/AIGC/high-fidelity/8-bit
contract and original frame rate, without interpolation or competing scale_ratio.
The installed default remains 1080p/24 fps. The 7 November 2026 archival extension
also validates native25fps, Standard/old_film/high-fidelity/8-bit and an explicit
scale_ratio when a720p result is requested. Ratio requests omit the competing
target_resolution, check source-fps equality and expected output dimensions, and
retain exact option fingerprints/no-replay protection. Other targets or source
frame rates require a validated contract update before submission; never silently
force footage to24fps or substitute local resizing for enhancement.
Verify current schema, availability and cost before submission; a different tier
is not automatically authorized. Never purchase credits or subscriptions.

Local technical tools, including FFmpeg, may losslessly segment transport inputs,
rebase timestamps, concatenate enhanced picture, copy the original audio and check
the export. These operations are not the upscale. Preserve source exports, exact
frame order/count, native audio and complete ending. Use the provider's actual
input-size limit (currently 250 MiB), durable receipts and exact accepted-job
resume; do not replay uncertain submissions. Inspect a concrete frame-count or
alignment mismatch before correcting it locally. Do not assume all outputs have
the same padding offset. Keep the existing brief final check; add no recurring
paid review, scoring or approval gate.

## Required technical audit after upscaling

Owner refinement, 4 November 2026: every requested AI-style video upscale includes
this audit **after the complete enhanced movie has been reassembled and before
delivery/upload**. A queue success, individual chunk output, or higher-resolution
metadata does not establish a complete upscaled film. This is technical completion
verification, not another storytelling, screenplay or artistic review.

Use one local evidence report in the project's existing production artifacts:

- Freeze the exact approved source identity, target and chronological transport
  manifest. Reconcile every required accepted/failed/uncertain request and downloaded
  output. Prove complete source-frame coverage with no missing, duplicated,
  overlapping or reordered sections, including the original final frame/ending.
- Verify every selected enhanced chunk and the joined movie: requested dimensions,
  aspect/frame fill, original frame rate, frame count, duration, continuous valid
  timestamps and correct first/last frame. If the provider adds padding or changes
  timing, establish the actual correspondence before any local correction; keep raw
  outputs and a derivation receipt. Never hide a gap by freezing, repeating,
  stretching or interpolating footage.
- Verify the actual joins and picture correspondence with brief local observations
  at chunk boundaries and representative source/output anchors. Confirm all selected
  enhanced picture is stitched in order; where stream-copied, normalized video
  payload identity can provide stronger whole-assembly evidence. Check for introduced
  black/frozen gaps or truncation, distinguishing deliberate source black/silence.
- Preserve original full-film audio, native speech and synchronization. When audio
  is copied, compare encoded audio payload and packet timing/priming; also verify
  stream presence, start/end and format. Run one full local A/V decode and check
  the actual decoded frame count. Keep checks scoped to enhancement/assembly.
- Verify a nonzero regular MP4, matching final SSD/Downloads size/hash and a clear
  derivative filename. Record the audit outcome and material limitations. Repair
  concrete faults before delivery; retain exact accepted work, no blind API replay.

No routine paid analysis/scoring, per-clip ASR, new story review, repeated audits or
approval gate is added. Reuse this one technical audit as the final enhancement
check. Original production/story acceptance remains separate. A user's upscale
request invokes this workflow; do not upscale unrequested films automatically.

Save the finished derivative as a regular MP4 in the current user's Downloads.
When Drive/public delivery is requested, upload **only after this audit passes**,
verify the uploaded filename/size and saved anyone-with-link **viewer** access,
and return the actual observed public link. Do not claim upload/sharing while only
local export exists, open an audible autoplay preview, or share without authority.
Use the receiving device's available storage and Downloads; credentials are
installed separately, never copied into portable policy or prompts.

## Long-film transport and recovery

Prefer bounded transport chunks of roughly 180–300 seconds at valid keyframes,
also below the actual 250 MiB input cap. Use lossless segmentation when usable;
do not equate a very large accepted upload with a parseable inference input.
In the revised lizard film, one approximately 646-second input failed the provider
file-parsing check twice, including after normalization; three roughly
164–242-second transports of that same material succeeded. Other longer chunks
also succeeded, so this does **not** establish a universal duration limit or a
proven root cause. Preserve those receipts and never treat a parse error as a
content-policy rejection or try to bypass moderation. Repair only definitively
failed technical inputs; resume accepted/uncertain identities exactly.

If technical re-encoding is necessary, retain dimensions/frame rate and every
source frame, record the derivation and validate it before submission. When using
frame-index timestamps through a stream with changing decoded properties,
prevent filter reinitialization from resetting the frame index (`reinit_filter=0`
in the verified FFmpeg transport repair); assert exact frame count before upload.
This remains technical transport preparation, never the upscale itself. Keep
independent accepted sections moving and verify actual correspondence after
reassembly. No separate paid test/review or new approval stage is required.
