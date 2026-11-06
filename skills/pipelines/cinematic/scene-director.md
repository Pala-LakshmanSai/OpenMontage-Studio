# Scene Director - Cinematic Pipeline

For narrative AI action, apply `docs/ai-video-action-clarity-and-pacing.md`.
Stage the pivotal choice and decisive movement so accident, coercion and voluntary
action cannot be casually confused. Keep target, support, contact and resulting
state legible in the chosen framing. One clear take may replace several vague
views; do not pad a provider request with repeated setup or idle reactions.

Direct every relevant visible participant or group in existing scene fields:
knowledge/goal, ongoing task, stimulus, gaze, pose/support, emotional progression
and exit state. Give silent witnesses/listeners a character-appropriate response;
do not leave a parent neutral through an emergency or a lead idling while helpers
struggle without a readable reason. Silence, shock and stillness may be deliberate,
but need a motivated onset and continuation. Preserve posture changes across cuts.

Owner correction, 5 November 2026 — **AI Movie writing comes first**:
follow `docs/ai-movie-screenplay-foundation.md`. Treat a supplied story as an
adaptable outline. Review and strengthen the whole story and revised screenplay
through its ending before any media generation, preserving its dramatic/emotional
core, curiosity, hooks and setups/payoffs. Add needed connective action and reactions;
remove/reorder weak or repetitive material. Give scenes performed time; an approximate
30-minute request may become 45 or 55 minutes, or shorter, when the story needs it.
This supersedes older AI Movie spine-only immediate-start instructions. After the
foundation, overlap detailed prompts/references, independent generation and editing.
Record required beats and observed selected coverage in existing artifacts under
that guide's narrative contract. No new owner approval or paid review service.

For **Queen Elizabeth I Style**, also follow
`docs/queen-elizabeth-i-style-screenplay-foundation.md`. Review and strengthen the
whole story and write the complete revised screenplay through its ending before
any new image, video, voice or music generation. Treat supplied prose as an
adaptable outline while protecting its core, emotional arc, curiosity and
setups/payoffs. Give scenes earned performed time within the actual budget; this
adds no human approval or paid review service. After this foundation, overlap
ready-sequence detail, independent generation and assembly. Preserve the style's
historical character-vlog grammar rather than importing AI Movie aesthetics.



For **authorized Frameo daily/unlimited API styles other than AI Movie and Queen Elizabeth I Style**, follow the immediate-start
rule in `docs/unlimited-plan-production-preferences.md`: a concise ending-aware
spine plus the first useful sequence's exact ready inputs permits its release.
Do not wait for the full scene plan, complete screenplay, all anchors or whole-film
stage completion. Plan later sequences during generation/assembly and publish
partial canonical artifacts honestly. Recorded full-run authorization adds no
per-stage stop; scope, zero quotes, no-replay, native continuity and minimum shots
still apply.

For AI Movie, apply `docs/ai-movie-editorial-continuity-playbook.md`. One coherent
sequence geography governs cast count/roles, seats/carriers/supports, scale anchors,
camera side/height, eyelines and motivated light. Bind current compatible state
references at meaningful changes; do not rely on text to override old/future-state
pixels. Specify a manageable causal action and its visible result, entry/exit state
and next-cut intent in existing shot metadata. A lens label or identity portrait
does not establish physical geography. No new audit or approval stage.

For every AI style, apply the general principles in
`docs/ai-video-global-realism-preferences.md`: persistent entity/attached state,
causal functional interaction, spatial/relational continuity, motivated readable
performance and temporal/editorial continuity. Specify relevant invariant facts
and allowed caused changes in the existing scene plan, then select clear current-
state references. Generalize owner feedback by failure class rather than copying
only a pictured example; follow `docs/portable-production-knowledge.md`. Simplify
choreography and reuse state facts; add no separate review layer.

For AI movies, select each view for its dramatic information and emotion: reveal
danger/scale with understandable geography, use relational coverage for choices
and close detail for recognition or consequence. Let the audience sometimes see
a clue before a character when that creates purposeful suspense. Vary distance,
movement, duration and quiet/urgent rhythm with the event; no decorative universal
camera move or repeated reaction template. Bold spectacle must change the story.

For narrative AI productions, read `docs/ai-video-story-engagement-preferences.md` before writing beats or shots. Populate the existing artifact with the short hook, distinct extreme turns, seeded consequential surprises, choices, costs and visible payoffs. Preserve factual/source/style boundaries and the current fast autonomous policy; this adds no review or approval stage.

For generated human performance, read `docs/ai-video-human-performance-preferences.md` alongside the active style. Reuse selected voices and clean supported references, prepare speech/action/framing/light in the existing shot plan, and qualify through a planned useful dialogue take. This adds no routine review, paid assessment or approval gate. Preserve no-narrator/no-speech and stylized-art rules; premium footage is selective within authorized scope/budget, with the same permitted cast and compatible voice.

## When To Use

**AI movie override:** apply `docs/ai-movie-reference-notes.md` and
`styles/ai-movie.yaml`. Stage scenes as intelligible action and emotional change:
establish geography, show the cause/attempt, preserve reactions, then show its
consequence. Record all five aspects below plus start/end state, exact native
speech and score intention. Choose physical camera movement for a dramatic reason;
do not make every shot an orbit or push. In Frameo unlimited mode, use
`docs/ai-movie-frameo-production.md`: publish ready frozen sequences incrementally,
prefer useful 30-second multi-shot passages with complete actions/utterances and
ordinary actual shots at least two seconds. Label exact-frame dependencies versus
independent reference-conditioned setups. Generated footage is the primary movie
medium; source-led inserts and title-card defaults below do not override it.

You are deciding how each cinematic beat will look and transition. This is where mood becomes a visual plan.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/scene_plan.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["script"]["script"]`, `state.artifacts["proposal"]["proposal_packet"]` | Beat map and source truth |
| Tools | `frame_sampler`, `scene_detect` | Source inspection and reframing checks |
| Playbook | Active style playbook | Color and typography consistency |

## Process

### 1. Make Hero Frames Explicit

Every cinematic piece needs a few memorable frames. Define them directly:

- opening image,
- reveal image,
- final image,
- any title-card hero moments.

### 2. Keep Source-Led Scenes Primary

If source footage exists, let it carry the piece. Generated inserts or text cards should support transitions, emphasis, or missing coverage, not dominate the timeline.

### 3. Limit Transition Vocabulary

Choose a small set:

- hard cut,
- fade to black,
- slow dissolve,
- restrained push or punch-in.

Too many transition types kill the mood.

### 4. Use Metadata For Visual Rules

Recommended metadata keys:

- `hero_frames`
- `transition_rules`
- `aspect_ratio_rules`
- `title_card_rules`
- `support_insert_rules`

### 5. 5-Aspect Scene-Plan Checklist

> Every scene beat — and especially every hero frame — must specify all five aspects. Cinematic relies on a small number of memorable frames; vague hero-frame specs are the single most common failure mode and produce unpredictable model output. Marking an aspect as N/A is allowed but must be explicit (e.g., "no subject — establishing scenery shot"). Silent omission is forbidden.
>
> 1. **Subject** — type + key visual attributes; if multiple, how to disambiguate. For hero frames, identity must be anchored verbatim across shots.
> 2. **Subject Motion** — actions in temporal order; subject↔object / subject↔subject interactions.
> 3. **Scene** — overlays (separately!) + POV + setting + time of day + scene dynamics.
> 4. **Spatial Framing** — shot size + position-in-frame + depth (FG/MG/BG) + camera-height-relative; and how those CHANGE across the beat.
> 5. **Camera** — playback speed → lens distortion → height → angle → focus/DoF → steadiness → movement.
>
> See `skills/creative/video-gen-prompting.md` for the primitive vocabulary.

> **Overlays callout.** Overlays (titles, subtitles, HUD, watermarks, framing graphics, lower-thirds, name plates, end-tag cards) are NOT part of the scene's foreground/midground/background depth axis. List them separately in scene metadata (`overlays: [...]`) with content and placement. Never describe an overlay as "in the foreground" — that confuses both downstream tools and any video-understanding model that re-analyzes the output.

### 6. Quality Gate

- every beat has a scene treatment,
- hero frames are identifiable AND fully specified across all 5 aspects,
- support inserts are justified,
- overlays are recorded under `overlays:`, never inside the depth/framing description,
- the visual language stays consistent across the piece.

## Common Pitfalls

- Using title cards as filler.
- Treating generated inserts like the primary story without saying so.
- Planning flashy transitions for every beat.

---

## Gate Reminder (Binding)

The recorded full-run authorization exception in the executive-producer contract
applies here: continue authorized production without a new per-stage approval
or end-turn pause. Rolling AI-movie scene plans represent ready sequences honestly;
they do not claim unfinished later scenes are complete.

This stage gates on human approval (`human_approval_default: true`). After review passes:
checkpoint with `status="awaiting_human"`, present the summary (the Backlot board renders
the artifact), and **END YOUR TURN**. Do not start the next stage in the same response.
This per-gate default applies only when full-run authorization has not been recorded.


## Queen Elizabeth I scene-plan foundation

Load the current reviewed whole screenplay under
`docs/queen-elizabeth-i-style-screenplay-foundation.md` before releasing media
work. Keep its required causal/emotional beats and ending intact while preparing
provider-sized sequence detail. Do not replace it with a short spine or a count
of thirty-second jobs. New contract-version1 scene-plan checkpoints validate the
same saved foundation; only later detailed shot preparation may remain rolling.
