# Asset Director - Cinematic Pipeline

For generated human performance, read `docs/ai-video-human-performance-preferences.md` alongside the active style. Reuse selected voices and clean supported references, prepare speech/action/framing/light in the existing shot plan, and qualify through a planned useful dialogue take. This adds no routine review, paid assessment or approval gate. Preserve no-narrator/no-speech and stylized-art rules; premium footage is selective within authorized scope/budget, with the same permitted cast and compatible voice.

## When To Use

**AI movie/Frameo override:** read `docs/ai-movie-preferences.md`,
`docs/ai-movie-frameo-production.md` and `docs/unlimited-plan-production-preferences.md`.
Use the selected Frameo Seedance 2.5 route for speaking and non-speaking movie
footage; do not silently inherit H3 or generic source-insert defaults. Submit
fully ready sequences while later planning and assembly proceed. One account
owner reserves/refills the verified shared capacity, retaining accepted and
uncertain jobs; the adapter's per-job lock is not an account scheduler. No batch
barrier or disposable audition is required. Inspect the first useful performance
for actual dependencies; unrelated prepared work may proceed. Use Kie first for
necessary images and Lyria 3 Pro/fal for background score, ElevenLabs/fal only
when precise timing is needed, all within actual authorization. Fast review and
recorded full-run approval supersede generic sample/repeated-review gates below.

This stage prepares the usable media for the final cinematic edit: source selects, title-card assets, optional support inserts, music, ambience, and subtitle assets when needed.

## Animation authoring for cinematic titles and overlays

Before authoring title cards, name plates, or SVG overlays, read **`skills/meta/animation-runtime-selector.md`** for runtime routing. Cinematic pieces lean on a handful of high-craft motion patterns:

| Cinematic need | Recommended approach |
|---|---|
| Hero title with subtle reveal | Remotion `HeroTitle` component (existing) |
| Logo build / cinematic sting on SVG | GSAP DrawSVG + MotionPath — read `.agents/skills/gsap-plugins/SKILL.md` |
| Curved camera move across a wide still or overlay | GSAP MotionPath — read `.agents/skills/gsap-plugins/SKILL.md` |
| Per-character title reveal (prestige / trailer style) | GSAP SplitText — read `.agents/skills/gsap-plugins/SKILL.md` |
| Cinematic easings (Unreal-style, stuttering, weighted) | GSAP CustomEase / EasePack — read `.agents/skills/gsap-plugins/SKILL.md` |
| Name plate lower-third with elastic settle | Remotion `spring()` is usually enough; GSAP CustomEase if you need stutter |
| Film grain / particle overlay | Remotion `ParticleOverlay` (existing) |
| Color grade / LUT | `tools/enhancement/color_grade.py` (not an animation concern) |

**Cinematic is where GSAP earns its weight most often** — the genre rewards crafted easings and precise curved motion that primitive `interpolate()` struggles to express cleanly. Don't over-use it either: for a fade-in title, Remotion `spring()` still beats a whole GSAP dependency.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/asset_manifest.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]`, `state.artifacts["proposal"]["proposal_packet"]` | Scene intent and beat plan |
| Tools | `subtitle_gen`, `audio_enhance`, `image_selector`, `video_selector`, `pixabay_music` (free, default), `freesound_music` (free), `music_gen` (ElevenLabs, paid) — selectors auto-discover all available providers from the registry. **Default to `pixabay_music` before reaching for `music_gen`.** | Optional support asset creation |
| Playbook | Active style playbook | Brand and typography consistency |

## Process

### Explicit 3D-world path

When the approved delivery promise is a continuous, free-viewpoint 3D world,
`threejs_world` satisfies semantic planning and browser-native motion: it creates
a real scene graph and time-driven camera, not a still-image fallback. Read
`skills/creative/3d-world-generation.md` and `.agents/skills/threejs-world-generation/SKILL.md`,
build into `projects/<id>/hyperframes/`, and review global, regional, walk,
semantic, and wireframe views before the assets gate. Keep
`render_runtime="hyperframes"` and `composition_mode="atelier"` locked for a
browser-native deliverable. For reference-grade video, lock Blender as the 3D
renderer and `render_runtime="ffmpeg"` solely as the image-sequence/audio packager.

For hero/reference-driven work, `quality_tier="production"` is mandatory. Install licensed catalogs with `threejs_asset_catalog`, generate unique meshes with Atlas/fal when useful, assemble and render in Blender, and reject the asset gate if dominant primitives, flat untextured ground, low regional object density, or obvious repetition remain. `blockout` exists only for layout/camera approval.

### 1. Prioritize Source Selects

Start with:

- source footage selects,
- stills,
- title-card backgrounds,
- any approved provided music or ambient beds.

These are the primary materials. Everything else is support.

If `proposal_packet.metadata.motion_required = true`, actual moving footage or generated video clips are mandatory. In that case:

- stills may be used only as reference material or backing elements inside a larger motion composition,
- stills may not replace the planned motion shots,
- a still-image teaser is not an acceptable fallback unless the user explicitly approves an animatic.

### 1b. Sample Preview (Prevents Wasted Spend)

Before batch-generating support assets, produce one sample of each expensive generated type and show the user:

1. **Generated insert sample** (if using `image_selector` or `video_selector`): Generate one representative visual. Confirm it complements the source footage before batching.
2. **Music sample** (try `pixabay_music` first — free, searchable by mood/BPM; fall back to `freesound_music` for cues and ambience; only reach for `music_gen` when the search tools miss the brief): sample or retrieve a short clip. Confirm mood and energy match the beat plan.

If `motion_required = true`, the representative visual must be a video clip sample, not a still image sample.

If rejected, adjust parameters and retry (max 3 iterations). Do not batch until approved.

Before the sample is generated, tell the user exactly which generation path will be used:

- tool,
- provider,
- model or variant,
- generation mode,
- why it was selected.

If that path fails, stop and ask before trying a different provider, model, or generation mode.

### 2. Generate Support Assets Only Where Needed

Optional generated assets should fill clear gaps:

- missing transitional b-roll,
- concept-led inserts,
- texture or atmosphere cards,
- simple textural motion backgrounds.

For motion-required jobs, use `video_selector` first for generated shots. `image_selector` may support look development, concept frames, or embedded design layers, but it does not satisfy the motion requirement by itself.

### 2b. Character and scene-state continuity for generated films

Apply **Coherent reference geometry** in
`docs/ai-video-global-realism-preferences.md` during existing image inspection
before binding any reference, including non-first-frame masters. Require distinct
boundaries/thickness, clear depth/contact, valid attachments/support and anatomy
clearance; simplify crowded masters or separate compatible reference roles.
Quarantine known faulty masters and only their dependents, correct future
bindings, preserve accepted/uncertain jobs and continue independent production.
No added review service, blanket paid call, per-clip audit or approval gate;
reject known faults without promising error-free probabilistic generation.

For AI Videos Documentary Style, apply the bounded concurrency protocol in
`docs/ai-videos-documentary-preferences.md`: overlap only independently planned
assets with reviewed inputs, unique recoverable receipts and one shared spend
ledger. Inspect the hardest required moving take first and each actual preceding
take before scheduling a dependent continuation. Never weaken character, prop,
environment, sound or final-join review for speed. Use conservative per-provider
concurrency until account behavior is established; record actual wall time, costs
and failures rather than claiming unmeasured speed or reliability.

For that style, also use its action-complexity and practical-review guidance:
plan clear single actions with motivated coverage instead of unnecessary
multi-prop choreography. Accept physically credible optional gesture variations
when all story and continuity requirements still hold; reject concrete defects
and missing essential results. Verify route-specific reference requirements
before submitting, including H3 Max's separate reference requirement on its
reference-to-video route. Review actual moving outcomes before descendants.
Reuse the current approved bible, read skills and time-stamped unchanged
provider/schema/pricing checks within their verified scope. Validate each new
payload, input, cost and durable job identity; refresh shared checks when a
change, stale evidence or error warrants it. Do not restart broad discovery or
repeat a completed review without a new unresolved question.

Maintain a shot ledger before generation: visible cast, offscreen cast, posture,
location, scale, eyelines, anatomy, costume, prop attachment and start/end action
state. Separate the persistent world state from the visible subjects. Describe
only the visible cast in the shot's identity paragraph; explicitly keep offscreen
subjects out of frame and in their established posture. A starting image alone
does not prevent a video model from inventing a background subject.

Lock physical blocking independently of identity: body support side, cuffed arm,
elbow bend, palm orientation, finger direction, head support and ground contacts.
Compare adjoining wide/insert anchors side by side before animation. Prompt new
camera coverage without permitting new blocking; identity masters alone do not
preserve pose. Derive tighter coverage from an approved moving take when framing
and detail allow it, or reject/regenerate the mismatched anchor before animation.

For a continuous generated reveal, prefer one supported-duration take. If it must
be extended, extract the exact final usable frame at the intended edit point for
the next first-frame anchor where supported. Preserve framing and camera/action
phase, direction and speed, not just appearance. Check first/last-frame controls
against the live route schema and review the actual joining frames. Conditioning
alone does not prove a seamless join, and new angles require separate coverage
planning rather than blindly inheriting the last camera view.

For tightly constrained H3 Max Turbo shots, explicitly set
`prompt_expansion_mode="disabled"`; the gateway's default is `balanced`.
When expansion is used, inspect the saved `expanded_prompt` for invented subjects
or actions. Do not copy Max's multi-reference prompt verbatim into Turbo: verify
the route's supported conditioning and rewrite the prompt for the visible anchor.

Follow the active fast-production policy: prepare these invariants in the ledger,
then use quick obvious-defect checks for actual continuation dependencies and one
brief final batch check. Dense temporal review of every clip/boundary is not a
routine requirement. Inspect a concrete suspect interval when an observed fault
needs diagnosis; repair unmotivated posture changes, extra subjects/limbs, costume
drift or disconnected props proportionately. Preserve accepted/uncertain jobs.

### 3. Prepare A Real Audio Plan

Store:

- chosen music track or prompt,
- ambience layers,
- impact or transition sounds,
- subtitle assets if dialogue or narration is present.

### 4. Use Metadata For Rights And Intent

Recommended metadata keys:

- `source_selects`
- `music_plan`
- `ambience_plan`
- `title_assets`
- `generated_support_assets`
- `rights_notes`

### Pre/Post Self-Review for Generation Prompts

Current fast-production override: specify the five aspects directly in the ready
sequence prompt. A separate scored pre/critique/post triplet and its metadata log
are optional debugging techniques, not routine work or a gate. The historical
method below applies only when explicitly useful for a concrete prompt defect.

> Before sending a prompt to any image or video generation tool, run a three-step self-review modeled on the CHAI oversight loop ("Building a Precise Video Language with Human-AI Oversight", arXiv 2604.21718v2). Cost is small (no extra tool calls); benefit is large (avoids wasted generations). For cinematic, this matters most for **hero-frame prompts** — one bad hero frame ruins the piece, and hero frames are the most expensive shots to regenerate.
>
> **Step 1 — Pre-caption pass.** Write the prompt the way you'd write it today. Do not over-edit; aim for a complete first draft.
>
> **Step 2 — Critique pass.** Score the draft against the 5-aspect checklist (Subject / Subject Motion / Scene / Spatial Framing / Camera). For each aspect:
> - Is it specified? If not, is the omission deliberate (e.g., "no subject — scenery shot") or accidental?
> - Are confusable terms disambiguated? (dolly vs zoom, pan vs truck, bird's-eye vs aerial, fisheye vs barrel, full shot vs close-up)
> - Are emotional adjectives ("epic", "moody", "cinematic") replaced with their visual causes (low-key lighting, slow push-in, anamorphic flare, deep shadows)?
> - For multi-shot prompts and identity-anchored hero frames: is identity anchored verbatim across shots?
>
> **Step 3 — Post-caption pass.** Rewrite filling the missing aspects, fixing confusable terms, and replacing subjective language. The post-caption is what gets sent to the generation tool.
>
> Log the (pre, critique, post) triplet in the asset metadata for traceability. This mirrors the CHAI workflow and creates a record the reviewer can audit.

### 5. Quality Gate

- source and support assets are clearly distinguished,
- generated inserts are limited and purposeful,
- audio plan matches the beat map,
- every referenced file exists.
- if motion is required, the asset set contains actual video clips for the motion-led beats.

### Mid-Production Fact Verification

If you encounter uncertainty during asset generation:
- Use `web_search` to verify visual accuracy of subjects (e.g. what does this building actually look like?)
- Use `web_search` to find reference images before generating illustrations
- Log verification in the decision log: `category="visual_accuracy_check"`

Visual accuracy matters. If the script mentions a specific place, person, or object,
verify what it actually looks like before generating images. Don't rely on
the AI model's training data — it may be wrong or outdated.

## Common Pitfalls

- Generating extra shots before proving the source edit works.
- Treating music as a single loop instead of a beat-aware element.
- Forgetting rights or provenance notes for supplied assets.
- Quietly downgrading from video clips to still images because one provider or renderer failed.
- Quietly switching providers or models after the user approved a generation path.


## When You Do Not Know How

If you encounter a generation technique, provider behavior, or prompting pattern you are unsure about:

1. **Search the web** for current best practices — models and APIs change frequently, and the agent's training data may be stale
2. **Check `.agents/skills/`** for existing Layer 3 knowledge (provider-specific prompting guides, API patterns)
3. **If neither helps**, write a project-scoped skill at `projects/<project-name>/skills/<name>.md` documenting what you learned
4. **Reference source URLs** in the skill so the knowledge is traceable
5. **Log it** in the decision log: `category: "capability_extension"`, `subject: "learned technique: <name>"`

This is especially important for:
- **Video generation prompting** — models respond to specific vocabularies that change with each version
- **Image model parameters** — optimal settings for FLUX, GPT Image, Imagen differ and evolve
- **Audio provider quirks** — voice cloning, music generation, and TTS each have model-specific best practices
- **Remotion component patterns** — new composition techniques emerge as the framework evolves

Do not rely on stale knowledge. When in doubt, search first.

---

## Gate Reminder (Binding)

This stage gates on human approval (`human_approval_default: true`). After review passes:
checkpoint with `status="awaiting_human"`, present the summary (the Backlot board renders
the artifact), and **END YOUR TURN**. Do not start the next stage in the same response.
Approval is per-gate — an earlier "go ahead" does not cover this gate.
