# The Last Day — Frameo production workflow

Owner direction, 3 November 2026: create a reusable **The Last Day** style from
the popular videos of `@TheLastDay01`, then produce original films from a title
and duration range, primarily with **Seedance 2.5 through Frameo's unlimited
daily pass**. “Frame.io” in the request refers to this established Frameo
generation route; Adobe Frame.io is not the selected generator.

Read [style preferences](the-last-day-style-preferences.md),
[reference notes](the-last-day-style-reference-notes.md) and
[prompt template](the-last-day-style-prompt-template.md) for the creative
contract. This document defines production scheduling, not reference findings.
It supplements [shared unlimited-pass policy](unlimited-plan-production-preferences.md)
and [fast production](video-fast-production-preferences.md). Reuse the saved
study for subsequent films; do not spend the generation window researching the
same channel again. Creating this style does not itself start a film, activate a
pass, authorize a purchase or establish reference-quality parity.

## Start from title and duration

When an actual film is authorized, use the cinematic pipeline and its canonical
artifacts. Read each stage director before its work. Apply the named style's
story, art and sound contract instead of incompatible generic trailer defaults.
Record full-run authorization where given; do not add routine voice auditions,
paid review gates or another style-selection interview. Preserve explicitly
required missing rights, actual spending limits and delivery authorization.

1. Resolve the title's concrete promise, duration range and selected/original
   cast. Choose a target within the range, allowing useful trims. Establish the
   ending and required payoff before writing isolated spectacular shots.
2. Lock a compact whole-film spine: opening question, cause of the threat,
   ordered attempts, consequential reversals, persistent losses or changes,
   final choice, climax and aftermath. Allocate approximate sequence durations
   and identify every setup needed by the ending. Lock geography, world rules,
   cast/voice, visual grammar and sound strategy once.
3. Prepare only the first useful sequence to submission depth. Freeze its
   dialogue where applicable, timed actions, shot plan, references and state.
   Start it as soon as its dependencies and admission conditions are satisfied.
   Write and stage later independent sequences while it generates.
4. Protect complete story coverage: prepare required opening, high-risk
   dependency footage, climax and ending early. An ending can be prepared or
   generated out of order only when its incoming state is already fixed; its
   final timeline position remains canonical story order.

Prepare before pass activation when possible. If the pass is already running,
do not wait for a fully detailed whole-film screenplay, every anchor or a first
render to finish before submitting other genuinely independent ready sequences.
Do not generate speculative filler to make a slot counter look busy.

## One sequence becomes ready when its contract is complete

Apply the [editorial playbook](the-last-day-editorial-playbook.md) before packaging
requests. Beat, utterance, shot and chunk IDs are distinct: a meaningful process
can span chunks and a chunk can cover several complete short beats. Store each
critical clause's intended picture, actual causal trigger and changed state.
Include `visual_job`, `claim_ids`, `incoming_state`, `trigger`, `outgoing_state`,
`utterance_ids`, `audio_role` and assigned local graphic IDs in sequence metadata.
These are agent contracts, not new schema requirements or automatic validation.

Keep contracts in `scene_plan.metadata.sequence_contracts`, keyed by canonical
scene/chunk ID, with readiness/revisions in `script.metadata`. Standard scene
rows remain schema-valid. Keep partial whole-film stages `in_progress`; publish
frozen sequence revisions and `metadata.partial_progress` without falsely
marking the entire script or asset batch completed.

| Contract item | Concrete contents |
|---|---|
| Identity and order | Project, sequence, canonical scene IDs, chunk ID, frozen revision and story position |
| Narrative change | Cause, action or decision, visible result, persistent cost and payoff obligation |
| Timing | Requested duration, useful intended duration, explicit internal shots, complete action and speech |
| Five aspects | Subject, subject motion, scene/overlays, spatial framing and camera for every shot group |
| Continuity | Exact cast, wardrobe, props, injuries/wetness, positions, axis, environment, time/light/weather |
| Sound | Style-specific narration/dialogue rule, exact lines if any, stable voice guidance, activity sounds and ambience |
| Reference inputs | Stable role names, source hashes, resolved supported transport entries and readable media |
| Dependency | Independent from the frozen bible, or exact predecessor output/edit-point state required |
| Editing | Intended entry/exit action, native audio pairing and stable final state without next-scene spillover |
| Admission | Authorized scope, unique private receipt/output paths, pass deadline and resolved actual request inputs |

Type each dependency as voice, identity/location master, exact editpoint frame or
required prior state. Resolve its actual media/hash/transport before freezing.
Do not copy a pilot's voice-ready boolean or assume an intended callback image
was attached. Ready independent footage proceeds while true dependencies wait.
During a necessary voice root, prepare later bindings, local graphics and sound
cues so reference extraction/upload does not create an avoidable refill gap.

Use the adapter's local request validation on the final resolved inputs before
reserving a new submission. A dummy planning row does not validate real reference
roles or transports. Cache readable reference uploads by source hash; never send
the workspace API key to a media host. Keep signed URLs and private receipts out
of portable documentation, shared reports and public artifacts.

## Make thirty seconds useful

Default to 30-second Seedance 2.5 requests under the selected unlimited plan.
This is a throughput strategy, not a requirement to retain thirty seconds in
the edit. Use shorter supported requests when action, speech, reference limits
or a diagnosed model limitation warrants them. Do not stretch ordinary movement,
invent filler or pad the finished film to consume the nominal duration.

Write explicit timed shots and hard cuts where coverage helps: spatial context,
consequential action, readable reaction/result and the changed state. The exact
shot count follows the story; three to six shots is a useful planning example,
not a reference measurement or quota. Plan ordinary shots at least two seconds
long, with enough time for complete actions and native utterances. Give the final
shot a clean settled endpoint, not a flash of the following scene.

Do not force the same three long shots and 65–70 words into every request.
Plan clause/action boundaries and useful handles without filler. Each retained
range needs a visual or narrative keep reason. Full retention is valid when
useful; source availability alone does not determine the final edit. Do not
overgenerate a fixed percentage as insurance: forecast from actual useful
coverage and obtain only required missing material within authority.

Use the Seedance section order and named locks from
`.agents/skills/seedance-2-5/SKILL.md`: global style, scene, characters, location,
initial blocking, timed shots, camera, physics, light and audio. Stable identity,
count, screen direction and state locks matter more than adjective density.
Use the active style's sound rule explicitly; provider audio defaults do not
decide whether this style has narration, speech or music.

Independent setups use original identity/location masters plus the frozen state
ledger. A real same-shot continuation waits for its exact outgoing edit-point
frame where supported, with compatible lens, distance, motion and sound. Only
that dependency waits. Do not serialize the entire film through recursive final
frames, and do not call a visibly discontinuous cut a seamless continuation.

## Parallel ownership

The owner explicitly requests multiple agents for this workflow. Use available
agents with exclusive file/sequence responsibilities; combine roles when fewer
workers are available. Every worker preserves other workers' edits and accepted
assets. One coordinator merges canonical artifacts and one assembler owns the
final timeline.

| Role | Owns | Publishes immediately |
|---|---|---|
| Coordinator/admission owner | Whole-film spine, account capacity, reservations, submission identities, priorities and final canonical merges | Current occupancy, ready queue, receipts and capacity handoffs |
| Writer/stager | Assigned later sequence files, causal turns, timing, blocking and start/end state | Each completed frozen ready contract, without waiting for the entire branch |
| Reference/sound preparer | Necessary masters/state anchors and authorized sound preparation | Resolved reference roles/hashes and ready assets |
| Downloader/assembler | Exact-job collection, cached selections, ordered rough assembly, final edit and export | Canonical scene ID, local asset path, actual usable range and native audio link |

The reference/sound preparer does not acquire extra generation capacity or add
unrequested paid analysis. The assembler writes selections before a prose report,
so assembly can consume them while later jobs run. No two workers write the same
canonical timeline. A worker restart resumes saved identities rather than issuing
replacement jobs. Hand off exact owned processes; never stop cohorts with broad
command-line matching that could kill unrelated active production.

## Keep the verified account capacity full

Before first admission, establish the one account-wide admission owner and read
the current account's active jobs, expiry, model/resolution entitlement and API
coverage. Reconcile jobs from other projects/chats and any uncertain submissions.
Ten simultaneous jobs and a USD 100 pass are dated owner observations, not live
verification or universal terms. Agent count never multiplies provider capacity.
If another coordinator owns the account, obtain an explicit capacity handoff.

The working occupancy is the union of provider queued/running jobs, local
submitting reservations and acceptance-uncertain requests, deduplicated by exact
job identity. Count a reservation that becomes a known job once. Local timeouts,
dead workers or missing chat updates do not prove that capacity is free.

On every completed-job or newly-ready-sequence event:

1. Reconcile exact receipts and current provider status. Release only capacity
   proved free by a terminal result or confirmed nonacceptance. Keep uncertain
   submissions occupied and preserve their receipt for reconciliation.
2. Pick a required ready chunk whose actual dependencies are satisfied. Prioritize
   missing essential coverage and dependency-unblocking work over alternatives.
3. Reserve capacity under the sole admission owner. Recheck frozen inputs and
   the expiry safety margin; let the adapter obtain its fresh workspace quote.
   Submit once only when the net-credit estimate is zero for this pass-only route.
4. Refill the next free slot immediately. Do not wait for a complete batch, the
   slowest earlier job, a download or a final export. Use bounded polling/resume
   so one pending job does not monopolize the coordinator.
5. Collect successful media and publish selections promptly. A confirmed terminal
   provider job may free its generation slot while download/edit continues;
   retain the output obligation until the local file is safe and checked.

This is an agent operating protocol. It is not a newly installed account lock,
daemon or automatic scheduler. Without a reliable view of shared occupancy, do
not invent free slots. Continue preparation/assembly while reconciling capacity.

## Deadline and recovery

Reforecast from remaining required story coverage, observed usable seconds per
result, actual active capacity, measured job latency and time until expiry.
Track the slow observed jobs as well as typical latency; sparse early data is
uncertain. Submit essential work early, retaining an explicit safety margin.
Reduce redundant coverage or simplify unsubmitted staging if time tightens;
preserve causes, outcomes, identity and the requested complete story.

A useful estimate is `available slots × remaining generation time ÷ observed
job time × usable seconds per result`, discounted for existing occupancy,
dependencies, slow jobs, faults and download limits. It is an estimate, not a
finished-film guarantee. Nominal thirty-second totals do not establish usable
runtime. Never promise a film count or quality level from “unlimited” alone.

Stop new submissions before the authorized pass deadline. Continue exact-job
polling/download after expiry where permitted; do not purchase, renew, activate
a new pass or switch to a billed route automatically. Preserve unexpectedly
charged output, record the charge and pause further new admission until resolved.
Do not throw away accepted work to solve a billing or local download fault.

Use a new correction ID only for a diagnosed necessary repair with confirmed
terminal/nonaccepted prior work and authorization. Never change frozen inputs
under an accepted receipt, replay an uncertain POST, bypass a provider rejection
or reroll usable footage for cosmetic polish. An unresolved branch does not
stop other authorized independent work. Release capacity incrementally to the
next authorized project when the current film's required jobs are accepted;
editing/export must not hold an otherwise free generation allocation.

## Measure and finish

Record UTC times for preparation start, sequence ready, reservation, submission,
acceptance, first observed running/completion, download, assembly, export and
delivery. Distinguish first-observed completion from exact provider completion.
Measure time to first accepted generation, ready-queue starvation, admission and
collection gaps, usable footage per elapsed hour and delivered runtime. Count
overlapping stages once in total wall time. Separate actual pass cost from
incremental images/music/repairs; a zero-credit quote does not mean a free pass.

Assemble cached selections in story order using actual returned cuts. Preserve
native speech-picture pairing and complete utterances. Run the cached local
minimum-shot check on actual selections, including internal cuts and meaningful
screen changes. Resolve ordinary shots below two seconds unless explicitly
requested for that film. Routine paid review/scoring remains USD 0.

Write actual source-frame and audio ranges, role and keep reason into selections.
Offscreen narration may bridge honest illustrative cuts; visible speech and
synchronized action remain paired. Do not assume isolated stems from native mixed
audio. Track essential local graphics to completion rather than leaving “labels
later” in a prompt. Place sound cues at named story turns, with quiet narration-first
balance from [sound guidance](the-last-day-sound-and-narration.md), not a fixed
fraction of total runtime.
The brief final semantic check includes cause/claim agreement, persistent state,
opening promise and ending payoff; correct anatomy or valid encoding is insufficient.

Finish with one brief local batch check for playable output, requested duration
range, 720p landscape/frame fill, sensible audio, essential story and selected
identity continuity. Investigate concrete faults without a routine per-clip ASR,
contact-sheet, every-join or cosmetic-retake loop. Complete local repairs,
export and requested delivery after the generation window if needed. Deliver a
regular nonempty MP4 in the current user's Downloads; retain working assets in
project storage. Do not autoplay audible previews or leave a player running.

## Verified implementation boundary — 3 November 2026

Read-only inspection of `tools/video/frameo_video.py` confirms:

- `frameo_video`, `model="seedance_2_5"`, integer durations 4–30, 720p, 16:9,
  native audio enabled; prompt length 1–20,000 characters.
- Up to 30 image, 8 video and 8 audio references. Image roles: `reference`,
  `first_frame`, `last_frame`; video role: `reference`; audio has no role.
- Local payload validation, fresh zero-credit workspace estimate, expiry check,
  durable private receipt, input hash and per-receipt file lock.
- Exact accepted-job resume after expiry, unknown-acceptance/no-replay guards,
  hash-checked cached output and nonempty atomic media downloads.
- `max_poll_seconds=0` still observes status once; a pending result is resumed
  with the same payload and receipt. It is not a failed generation to replay.
- No account-wide semaphore, background scheduler, automatic entitlement/renewal
  audit, story planner or global capacity discovery is implemented by this adapter.

`tests/tools/test_frameo_video.py` contains offline boundary tests for quotes,
expiry, uncertain acceptance, exact resume, payload changes, safe reference
upload and timing. These tests cannot prove live concurrency, current commercial
terms, latency, generated quality or reliable voice identity. The workflow itself
adds no paid test. The later nuclear pilot supplied dated production observations:
twenty included jobs, observed capacity ten, 600.833s export and 20m43s first-acceptance
to last-download. Those are not total production time, current entitlement or a
quality guarantee. See the [pilot refinement](the-last-day-refinement-20261103.md)
for observed failures and corrections. Revised-film parity and owner artistic
acceptance remain unproven.
