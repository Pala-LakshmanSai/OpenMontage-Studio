# Edit Director - Cinematic Pipeline

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
