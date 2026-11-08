# Reusable production lessons

These lessons are repository knowledge, not a dependency on a particular chat,
personal memory, SSD or paid reviewer. Read alongside the active style and the
current shared policies in `production-knowledge-index.json`.

Owner clarification, 3 November 2026: preserve the general cause of a production
failure, not merely its visible symptom. Apply the shared persistent-state,
physical-causality, object-affordance, spatial, performance/readability and editorial
principles in `ai-video-global-realism-preferences.md` across analogous situations.
For example, a displaced bandage is an attached-state continuity failure, a knob
pressed like a button is an affordance failure, and a person disappearing in a
wide is an occupancy/spatial failure. These examples do not limit the rules.
Incorporate existing saved corrections and future feedback through the process in
`portable-production-knowledge.md`; consolidate rather than grow review stages.

## Prepare useful footage, not generic prompts

Owner-requested lizard-film review, 4 November 2026: a valid29:49.75/720p export
with all detected shots over2s was rejected for continuity and abrupt ending.
Full-timeline shot sampling and selected temporal windows found invented cast,
duplicated roles, restored injuries/possessions, changing growth/scale, altered
vehicle layouts and missed cause/result.53of60original provider chunks had been
kept whole; this is a risk signal, not a rule banning full takes. Successful jobs
and detailed prompts did not prove a usable sequence. The portable
[editorial-continuity playbook](ai-movie-editorial-continuity-playbook.md) implements
the fixes in existing story/state/reference/camera/edit preparation. The detailed
review was specifically requested after rejection; do not make it a routine loop.

Start with the title's visible promise, an immediate open question and several
distinct consequential turns. Use `ai-video-story-engagement-preferences.md`:
seed trouble, force a choice, show effort and a changed method, preserve the cost,
and earn the payoff. A long film needs new developments, not repeated chores,
reaction shots or a single incident stretched to runtime. Extreme fictional
stakes are encouraged when appropriate; factual footage must remain factual.

Before each ready sequence, record scene ID/story order, exact visible cast and
offscreen state, current inventory, action phases, camera side/path and useful
shot lengths. State who is on which side of a door, vehicle or barrier. Bind each
spoken phrase to its visible mouth window; finish speech before a physical camera
turn and resume only in its intended view. Vary cadence with situation, not voice
identity. Do not stretch a short phrase to fill a 30-second envelope.

Independent story beats reuse original clean identity/voice roots. A true
same-shot continuation uses the actual outgoing edit frame where supported.
Name each reference's role: a portrait's background is not current inventory.
Long recursive chains can drift; static room references can encourage repeated
poses or state resets. Neither references nor prompts prove the returned state.

## Use the active generation window efficiently

Follow `unlimited-plan-production-preferences.md`: prepare before activation,
default to useful 30-second multi-shot Frameo chunks, keep one shared account
queue at its verified limit, refill ready required scenes, and measure the time
remaining. Shorter speaking takes are appropriate when a long envelope dilates
delivery. No artificial filler, automatic premium upgrade or extra generation
merely to occupy slots. Theoretical capacity is not usable finished-film length.

Download accepted jobs promptly and publish scene/path/range/state immediately.
Conform those selections while later independent work runs. Release generation
capacity at required-generation completion, before editing/export/sharing.
Only coordinate other chats when the owner has authorized that coordination.
Inspect actual process, task, lock and lease ownership before declaring a blocker;
a stale checkpoint or an idle chat is not proof of resource contention.

Preserve exact accepted receipts, frozen request hashes, uncertain submissions,
cancelled work and previous exports. Never replay an unknown POST. Resolve a
local configuration fault before submission without inventing a provider failure.
Reference upload success is insufficient: verify readable transport without
forwarding a provider key to a media host. Safety rejection is not a fallback cue.

## Select actual action and preserve sound timing

Requested shot timings differ from actual returned cuts. Use actual boundaries;
ordinary visible shots and meaningful screen states last at least two seconds.
Trim a concrete wrong pose, geography reset, invented tool or tiny tail rather
than retaining everything to hit duration. Do not blindly drop every final shot.
Accepted moving footage determines the next state; revise the ledger accordingly.

Native visible speech keeps its original picture/audio pair and matching source
offsets. ASR checks words, not articulation. For a reported sync fault compare the
original take, conformed selection and final output before choosing a repair.
The travel run exposed about 40.667 ms of AAC join padding per join, accumulating
roughly two seconds after 50 chunks when decoded linearly. Use timestamp-aware
PCM preparation in `lib/native_audio_assembly.py` and the registered audio mixer,
or decode/trim each source to its selected frame range before concatenating PCM.
Encode the final AAC once; do not assume a pydub linear decode of copied AAC joins
preserves the timeline. This repairs timing, not bad generated mouth shapes.

Keep exact selected frames and corresponding PCM samples. Nominal 24 fps packet
copying may differ by one mux tick in average-rate metadata; inspect exact frame
count, presentation timestamps and measured drift rather than rebuilding a film
because a rational average-rate string is not literally `24/1`. Never suppress a
meaningful gap or actual drift. Preserve the rendered picture for an audio-only
repair; verify decode, timing and picture identity afterward.

## Finish quickly and report truthfully

Routine paid review/scoring budget is USD 0. Use the existing cached local cut
guard, decode/probe, essential story/identity views, audio checks and requested
sharing verification. Further inspection is for a concrete fault, not every clip
or every join by default. Targeted justified corrections remain allowed within
actual authority/budget. A technical pass is not owner artistic acceptance.

Final exports go to the receiving user's Downloads directory, working files to
available project/SSD storage. No black bars, portrait filler or still-motion
substitution. For supplied voiceover preserve its exact basename. Quiet previews
are muted and paused/closed immediately. Large Drive uploads can use the supported
browser chooser when the connector transport limit is insufficient; verify name,
exact bytes and public Viewer permissions without opening an audible preview.

Observed winter run on 3 November 2026: 44 useful 30-second requests completed in
30m51s through ten shared slots, zero additional charged credits under the existing
pass. The selected film was 19:03.583 at 720p24. Increasing local Remotion workers
from two to four reduced one 30-second render from about 31–32s to about 20s on
the tested Mac. Different footage and one device make these observations, not
benchmarks or guarantees for another computer. Measure the receiving hardware.

Detailed historical media/receipts remain with their original projects; none are
required to understand these rules. Reference-study notes and acceptance limits
are shipped with each style. Do not copy the owner's unrelated private history.

## Optional authorized video enhancement — 4 November 2026

The registered `fal_bytedance_upscale` adapter provides a deliberately narrow
ByteDance Standard route: 1080p, 24fps, AIGC preset, high fidelity and 8-bit output.
Use it only when enhancement/upload and its separate spending are authorized;
a Frameo pass does not cover this service. Preserve the accepted original and
label the result as enhanced/upscaled, not native higher-resolution generation.
Discover its current input schema and estimate before admission; an estimate is
not an invoice or spending authority. No automatic model tournament or paid review.

The source limit enforced by this adapter is 262144000 bytes (250 MiB), observed
from a definitive provider rejection on 4 November. Validate size before upload
or paid submission; prepare bounded coherent source sections when necessary,
with distinct immutable receipts and a source-to-output frame map. Recheck the
current provider contract when it changes. Unicode filenames are uploaded through
a temporary ASCII-named symlink without renaming or copying the original media.
Authenticated requests remain on the validated fal queue host. Private media
URLs and provider responses stay in private receipts, never public training.

Resume exact accepted receipts. An uncertain POST remains uncertain; worker exit
or timeout does not authorize replay. Definitive failures stay recorded. Changed
inputs, conflicting file paths and unrelated existing outputs must be preserved.
The adapter checks basic resolution/duration, but that does not prove exact frame
alignment, unchanged audio, natural detail or better perceptual quality. Returned
padding or an altered timeline can require a local frame correction. Align the
picture using actual source/output correspondence and remux the preserved finished
audio only after frame count, timing and synchronization agree. Do not blindly
trim every result by a fixed number of frames or stretch narration. Reuse the
existing brief final check and inspect concrete enhancement faults proportionately;
no quality parity, runtime or receiving-device throughput guarantee follows.

## 8 November 2026: staging and continuity audit (I Fell Into a Black Hole)

A delivered film still contained staging faults that the owner found: an empty cockpit seen from outside, and a character pointing at a black hole while looking the other way. A one-frame-per-second audit found 19 more continuity, state, text and scale faults that a one-frame-per-shot check had missed. The durable rules are in `docs/ai-video-global-realism-preferences.md` ("Visible occupancy" and "Staging geography, attention, persistent state and screen truth"). The film's evidence and fixes are in `projects/i-fell-into-a-black-hole-20261107/production/mistakes-audit-20261108.md`.
