# Edit Director - Cinematic Pipeline

Apply `docs/ai-video-action-clarity-and-pacing.md` to narrative action. Check what
a viewer without the screenplay would infer: chosen action or accident, who acts,
by what means, and with what result. Record actual selected evidence; an authored
cut reason is not an observation. Trim repeated information, duplicate action,
idle tails and unnecessary pauses while preserving complete action/native speech
and developing emotion. Keep rhythm varied; continuity is not slow literalism.

For true continuations, include relevant supporting/background behavior in that
same observation: task, attention, emotional response, pose/support and location.
Do not qualify a shot solely by its featured face while other affected people
freeze or reset. Preserve quiet meaningful responses; remove idle waiting and
duplicate reaction coverage. No blanket demand for louder or constant acting.

For AI Movie, stage necessary time cues before/at the affected scene opening,
using restrained readable film-specific typography and sound treatment. Preserve
legible hold, safe placement and consistent time origin. Reconcile flashback
entry/return and epilogue ages; do not interrupt a decisive action with a card.

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



## When To Use

This stage turns the beat map into a paced cinematic timeline. Rhythm and restraint matter more than effect count.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/edit_decisions.schema.json` | Artifact validation |
| Prior artifacts | `state.artifacts["assets"]["asset_manifest"]`, `state.artifacts["scene_plan"]["scene_plan"]`, `state.artifacts["script"]["script"]` | Assets, hero frames, beat map |
| Playbook | Active style playbook | Typography and transition consistency |

## Process

### 1. Cut By Emotion First

For AI Movie, read `docs/ai-movie-editorial-continuity-playbook.md`. Source files
are coverage. Do not create the final edit by taking every ordered file from
zero to its last frame merely because it downloaded. Select complete actions,
new information and reactions; retain a full take only for its dramatic purpose.
Record entry/exit state and next-cut intent in existing edit metadata. Repair
incompatible cast, injury, scale or geography at the source/selection; a dissolve
cannot make them continuous. Native speech stays at its source mouth offset.

Cuts should follow:

- emotional emphasis,
- reveal timing,
- musical turns,
- visual contrast.

Do not optimize only for information density.

### 2. Protect Strong Moments

If a look, line, or gesture is doing the work, let it live. Do not over-cover it with extra inserts.

### 3. Use Sound To Push The Edit

Ambience, impacts, dropouts, and music changes should help create momentum between scenes.

For AI Movie, direct the actual passage transition rather than concatenating
generated30second containers. Carry a motivated stimulus/reaction, look or action
into compatible new coverage; preserve axis, movement phase and physical state.
Use a relevant incoming sound pre-lap (J-cut), outgoing tail (L-cut), listener view
or match-on-action when useful for immersion. Maintain room/sea ambience; do not
add a transition effect to every cut or conceal missing movement with a dissolve.
Visible native speech retains its original word-to-mouth offset: a pre-lapped
speaker must be revealed at the matching already-elapsed picture time, never at
the beginning of the same mouth take. This belongs in existing edit decisions
and the brief essential check, not another routine audit or approval stage.

### Camera and time continuity at boundaries

Plan subject scale, framing, lens/axis, exposure, action phase and camera/action
velocity at intended boundaries. Same-view crop jumps and restarted/replayed takes
are continuity failures even with identical anatomy. Prefer one continuous moving
take for a continuous reveal; for generated extensions, condition on the exact
final usable frame at the intended cut where supported, preserving the motion
plan. New angles need deliberate match-on-action or eyeline planning. Under the
current fast-production policy, inspect adjoining end/start motion only for actual
continuation dependencies or a concrete fault, not every join. Use the existing
single cached actual-cut/minimum-shot check and brief final batch review. Do not
use arbitrary dissolves or morphs to conceal mismatches. Retiming must preserve
visible mouth/dialogue synchronization.

### 4. Use Metadata For Timing Logic

Apply **Complete endings and flexible runtime** in the shared engagement guide.
Edit by actual complete performance, not generation-container endpoints. Protect
the outcome, consequence and emotional landing, then deliberately finish the final
picture/native sound. Separate a source's optional after-title stinger from the
completed main ending without automatically adding titles. Use the moving final
passage in the existing brief check; a duration match, final still or fade does not
establish closure. Approximate runtime may flex within actual authority.

Recommended metadata keys:

- `beat_timing`
- `audio_turns`
- `title_card_windows`
- `reframe_notes`

### 5. Quality Gate

- the emotional arc is intact,
- reveals land clearly,
- title cards are sparse and timed with intent,
- strong moments are not buried under coverage.

## Common Pitfalls

- Overcutting emotional material.
- Using speed ramps or flashy transitions by default.
- Letting title cards replace editorial clarity.

## AI Movie and Queen Elizabeth I narrative coverage contract

Populate `edit_decisions.metadata.narrative_coverage` under
the active style's foundation guide (`docs/ai-movie-screenplay-foundation.md` or
`docs/queen-elizabeth-i-style-screenplay-foundation.md`) using actual selected cuts and required
beat observations. Use `cuts_digest(cuts)` from `lib.narrative_continuity` and the
reviewed screenplay hash; reconcile after any screenplay/cut change. Include
critical arrival/contact/result, secondary agency, reactions, temporal cues and
setups/payoffs in the appropriate sequence, without mandatory trivial travel.
Known missing bridges cannot pass on a downloaded/usable flag or minimum shot
length. Record deliberate readable ellipses, not explanations of unseen footage.
New contract-version1 checkpoints for these styles reject stale/missing coverage
before render. This validates
recorded observations, not their visual meaning or owner artistic acceptance.
