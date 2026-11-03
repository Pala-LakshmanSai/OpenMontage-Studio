# Reusable production lessons

These lessons are repository knowledge, not a dependency on a particular chat,
personal memory, SSD or paid reviewer. Read alongside the active style and the
current shared policies in `production-knowledge-index.json`.

## Prepare useful footage, not generic prompts

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
