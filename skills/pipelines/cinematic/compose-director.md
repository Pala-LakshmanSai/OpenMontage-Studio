# Compose Director - Cinematic Pipeline

For a requested video upscale, read `docs/video-upscaling-preferences.md` and
`skills/creative/upscale-usage.md`: ByteDance API only. Do not replace enhancement
with a local resize or another provider. Technical split/join/audio-copy/checks
remain allowed; preserve source frames, native audio and the complete edit.
Every requested upscale must pass the canonical post-upscale technical audit
after full reassembly and before delivery/upload: complete coverage/order/joins,
frames/timestamps/resolution, original audio/sync, full decode and file identity.
Use its local evidence as the enhancement final check; no repeat story review,
routine paid scoring or extra approval stage.

## When To Use

Render the cinematic piece with careful attention to grade, audio dynamics, and frame treatment. This is not a generic export step.

## Runtime Routing (MANDATORY first step)

Read `edit_decisions.render_runtime`. Cinematic work routes to:

- **`render_runtime="remotion"`** — default for video-led trailers using `CinematicRenderer`. Keeps video clips, transitions, and ambient overlays in one React-based pass.
- **`render_runtime="hyperframes"`** — for kinetic title cards, HTML/GSAP-driven trailers, launch-reel-style compositions, or explicit Three.js world fly-throughs. See `skills/core/hyperframes.md`. `hyperframes check` must pass before render.
- **`render_runtime="ffmpeg"`** — simple source-footage concat with no composition.

For a Blender world film, FFmpeg is the approved packager for the numbered
Blender image sequence and audio. It must not synthesize camera motion or replace
missing Blender frames with pan/zoom effects.

`delivery_promise.motion_required=true` means the locked runtime is a commitment. Silent swap to another runtime (including FFmpeg Ken Burns) is a CRITICAL governance violation. If the locked runtime fails, escalate per AGENT_GUIDE.md > "Escalate Blockers Explicitly."

**Pass `proposal_packet` to `video_compose.execute()`** so the tool's `runtime_swap_detected` check compares directly against `proposal_packet.production_plan.render_runtime`. Without it the swap check is skipped in-tool and only the reviewer skill catches the drift.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/render_report.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["edit"]["edit_decisions"]`, `state.artifacts["assets"]["asset_manifest"]` | Edit plan and media assets |
| Tools | `video_compose`, `audio_mixer`, `video_stitch`, `video_trimmer`, `color_grade`, `audio_enhance` | Render and finishing |
| Playbook | Active style playbook | Finish consistency |

## Process

### 0. Check Hard Requirements Before Rendering

If the approved brief or scene plan makes motion a hard requirement, verify that the render path still preserves that promise.

- If Remotion is required and unavailable or failing, stop and bubble the issue to the user immediately.
- Do not switch to an FFmpeg-only still-image fallback for a motion-led trailer, teaser, or agent video.
- Do not convert the piece into an animatic unless the user explicitly approves that downgrade.
- If the render engine changes materially, tell the user before rendering and explain why.

**Mandatory Remotion preflight (run before every render when the scene plan includes any Remotion scene type — title cards, stat cards, anime/hero_title, end-tag, overlays):**

```bash
python -c "
from tools.tool_registry import registry
registry.discover()
info = registry.get('video_compose').get_info()
print('Render engines:', info.get('render_engines'))
print('Remotion note:', info.get('remotion_note'))
"
```

If Remotion is not in the available render engines, stop and report to the user per the Decision Communication Contract. Do not substitute a reduced-fidelity render path without approval.

### 1. Use Frame Treatment Deliberately

Follow the owner's active full-frame rule: no letterbox, baked-in bars or padded
sides, including AI Movie. Use 24fps intent or grading only when they help the
piece; the word cinematic alone does not justify either.

### 2. Preserve Audio Dynamics

For AI Videos Documentary Style, follow its verified audio-only finishing
guidance in `docs/ai-videos-documentary-preferences.md`. When the reviewed picture
is unchanged and only audio packaging is defective, preserve the original render
and locally mux a copied video stream with the aligned original mix. Verify
encoded picture identity, frame count, final duration, audio lag/levels and full
decode. This is finishing of the approved Remotion picture, not a runtime or
creative substitution, and it must not be used to bypass a visual repair.

The mix should allow:

- quiet moments,
- impact moments,
- clear dialogue or narration,
- controlled music swells.

### 3. Verify The Final Mood

For AI Movie, follow `docs/ai-movie-editorial-continuity-playbook.md`: the existing
brief check uses moving opening, consequential interaction/transition and ending
passages, with relevant state/text evidence. Four attractive stills, a valid file
and a minimum-shot pass cannot establish coherent cuts or complete performances.
Keep claims bounded and distinguish technical delivery from owner acceptance.

In the existing brief essential check, inspect the actual moving final passage and
sound boundary: complete outcome/reaction, legible optional-stinger separation and
intentional final picture/sound. Do not infer closure from nominal runtime, a still
near the end or the provider job succeeding. Follow **Complete endings and flexible
runtime** in the shared engagement guide; add no separate routine review stage.

Check:

- opening frame,
- reveal beat,
- final landing,
- subtitle readability where relevant.

### 4. Use Render Metadata

Recommended metadata keys:

- `frame_treatment`
- `grade_profile`
- `mix_notes`
- `variant_outputs`

## Common Pitfalls

- Flattening the audio so the piece loses dynamics.
- Applying letterbox to footage that needs every pixel.
- Letting grading or sharpening damage faces or text.
- Silently swapping a blocked Remotion render for a lower-fidelity still-image export.
