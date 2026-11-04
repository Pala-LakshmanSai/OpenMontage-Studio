# AI movies with the Frameo daily pass

Owner direction, 3 November 2026. Use this when the owner chooses Frameo Seedance
2.5 for an authorized AI movie. It supplements [AI movie preferences](ai-movie-preferences.md),
[unlimited-pass production](unlimited-plan-production-preferences.md) and
[fast production](video-fast-production-preferences.md). This training task does
not itself authorize a movie, pass purchase, routine production review or media
generation. The owner's separate one-time reference-analysis authorization is
recorded in the reference notes; it does not carry into future film reviews.

## Goal and precedence

Produce the complete original story at the requested approximate scale, with strong
screenplay, readable staging, emotional performance and a purposeful score,
while minimizing end-to-end production time. Use useful 30-second multi-shot
requests and the full verified shared capacity. Longer requests are a throughput
choice, not a reason to slow actions, add filler or keep bad internal cuts.

Apply [complete endings and flexible runtime](ai-video-story-engagement-preferences.md#complete-endings-and-flexible-runtime--owner-correction-4-november-2026).
Thirty-second requests are acquisition units, not mandatory scene lengths or a
fixed final container count. Reserve the climax, aftermath and payoff in the
existing spine, then use their actual useful performances in the edit. Approximate
runtime can flex; explicit hard limits, budget and pass expiry remain binding.
The final accepted job is not automatically the film's final edit point, and an
optional stinger needs a completed main ending before it.

Read the [editorial-continuity playbook](ai-movie-editorial-continuity-playbook.md).
Publish source availability separately from actual usable selects. Do not turn an
ordered download list into a full-range final timeline. Prepare compatible current
state/scale/cast and entry/exit intent per ready sequence, and let the editor choose
complete actions and native lines from returned coverage. Use exact returned state
for real continuations; independent work still refills capacity. No recurring audit.

Owner refinement: quality means a strong original premise, audience curiosity,
emotional and consequential turns, directed cinematography and actual continuity,
not just a playable export. Improve completion time through the critical path:
prepare the shared causal/state foundation once, parallel independent detailed
writing and references, publish ready chunks immediately, refill actual available
capacity and select/conform returns while generation continues. Reuse settled
voices and accepted assets; no audition/root delay when clean guidance already
exists. Simpler clear physical action can support a more ambitious dramatic idea.
Only a true observed-state dependency blocks its own branch. Existing brief
essential evidence and targeted repair replace repeated broad review handoffs.
For an explicit "style first" request, complete that requested update before
generation, then reuse it for later films without a recurring retraining barrier.

The owner reports that short and 30-second jobs take similar time and specifies
ten simultaneous jobs on a USD 100 daily pass. Treat those as owner observations
and requested operating assumptions. Verify current workspace/API entitlement,
expiry and concurrency; measure real latency and usable yield. Do not advertise
these figures as universal provider terms, a measured speedup or a finished-film
guarantee. Unused slots do not authorize another title or additional spending.

For this selected route, Frameo Seedance 2.5 takes precedence over the movie
guide's older H3/Turbo default. Keep native speech and picture paired, original
cast/voice continuity, 720p landscape and ordinary actual shots of at least two
seconds. Keep existing music/image budgets; a video pass is not an unlimited
music or image subscription. Use the selected native voice/reference method
supported by this route; do not silently add postprocessed lips or change models.

## Start the first ready sequence early

Owner clarification, 4 November 2026: the cross-style
[immediate-start rule](unlimited-plan-production-preferences.md#immediate-start-for-every-frameo-style--owner-clarification-4-november-2026)
applies on every fresh installation. Start once the ending-aware concise spine
and first sequence's exact inputs are ready; neither all anchors nor complete
whole-film stage artifacts/gates may delay that authorized submission. Keep
later preparation, generation and assembly overlapping under shared admission.

Prepare before pass activation when possible. Once an authorized pass is live,
do not make full-film detailed screenplay or complete anchor production a barrier
to the first generation. Replace that barrier with two levels of preparation:

1. **Whole-film spine, once:** title promise, duration range, protagonist's want
   and emotional need, governing world rules, initial problem, causal escalation,
   consequential reversal, costly final choice, ending/payoff and essential setup
   plants. Assign ordered sequence IDs and approximate time budgets. Lock cast,
   voices, principal geography, visual grammar, sound strategy and actual budget.
   This is a concise ending-aware outline, not every shot or spoken line.
2. **Ready sequence, incrementally:** finish its exact dialogue, achievable
   action, shot timings, emotional turn, references, blocking, start/end state,
   light/weather/axis, native sound and edit intention. Freeze the inputs before
   submission. Write later sequences while this sequence generates.

The opening should establish a specific unsettled situation quickly, not consume
the first several requests on generic scenery. Every later sequence must change
the situation through a choice, discovery, conflict or result. Before freezing
one, check it against the already locked ending and outstanding setup/payoff
obligations. Expand or simplify unsubmitted material to fit actual runtime;
never rewrite an accepted chunk's inputs under the same receipt.

A first useful take may establish transport, identity and dialogue behavior.
Do not launch a separate paid audition, ten-pose asset trial or scoring loop.
Independent sequences whose references and state are already settled can proceed
while that take runs. Only true dependencies wait for its observed result.

## Minimum ready-chunk contract

Make ready priority explicit, rather than defaulting to chronological filenames:
include the opening, a useful difficult interaction/reveal and the required climax
coverage early when their real dependencies are ready. Prepare their critical
state references first or independently where possible. Do not chain an unrelated
exterior/creature shot behind a room-state image it does not need, or reserve all
difficult material for the final wave. Keep free slots filled with other required
ready work; never cancel accepted jobs or add disposable tests to force priority.
Select a returned hard take promptly so a concrete pickup can overlap remaining
generation rather than extending the whole run after assembly is otherwise done.

Store sequence-specific contracts in `scene_plan.metadata.sequence_contracts`,
keyed by canonical scene/chunk ID; put script readiness and revision notes in
`script.metadata`. Keep canonical scene rows and timing fields schema-valid:
do not add unsupported per-scene keys. Contracts contain entry/exit state,
dependencies, frozen revision and internal shot timing. Partially ready artifacts
must not claim full-film completion; this adds no new schema or approval stage.

Keep the following in the existing scene plan and a lightweight readiness entry;
do not create a new approval ceremony. One ready chunk contains:

| Field | Required meaning |
|---|---|
| Identity | Film, sequence, canonical story order, chunk ID and revision |
| Narrative job | What changes; its cause, character choice and resulting cost/payoff |
| Duration | Requested seconds, useful intended range and runtime contribution |
| Shots | Timed subject/action/setting/framing/camera beats; no planned sub-two-second flashes |
| Dialogue | Exact lines, speaker, natural delivery time, reactions and breathing room |
| Continuity | Cast, wardrobe, props, injury/wetness state, positions, axis, local time and light |
| References | Stable roles and hashes, supported readable transports, voice guidance where supported |
| Dependencies | Independent from frozen bible, or exact predecessor output/state required |
| Edit and sound | Entry/exit action, native audio pairing, ambience and score intention |
| Admission | Authorized scope, current zero-credit quote, pass deadline, unique receipt/output paths |

Resolve the real transport entries before declaring readiness. Run the adapter's
local request validation on the final resolved inputs; dummy references or a
planning-row schema check do not validate the actual request. Keep access-bearing
media URLs and provider receipts private; portable guides contain roles/hashes,
not credentials or signed links.

Apply [coherent reference geometry](ai-video-global-realism-preferences.md#coherent-reference-geometry--owner-correction-4-november-2026)
before binding masters, even with `role="reference"` rather than `first_frame`.
Use the existing image inspection to reject known fused solids, invalid mounts/
support or ambiguous depth; simplify crowded masters or separate compatible
identity/location/mechanism roles. Correct future bindings and quarantine only
affected dependents while independent ready work fills available capacity.
Accepted inputs stay immutable and uncertain jobs stay reserved, never replayed.
No new review service, blanket paid image call, per-clip audit or approval gate.

Use roughly three to six purposeful shots within a 30-second passage when the
scene benefits from coverage, with time allocated to complete actions and speech.
That is a planning example, not a fixed shot quota. A focused long take or fewer
shots may work better. Spell out hard cuts and each shot's framing; do not request
a vague montage. End at a stable usable story state without a teaser fragment of
the next scene. Actual returned cuts, not requested timestamps, determine the edit.

## Parallel roles with a single admission owner

When the user authorizes multiple agents, divide responsibility explicitly:

- **Coordinator:** owns the whole-film spine, shared provider capacity, job
  admission and durable receipts. Only this owner approves a slot reservation and
  a new submission; independent agent counts do not multiply the provider limit.
- **Sequence writer/stager:** prepares the next independent sequence and maintains
  its state and payoff obligations. Publishes ready chunks incrementally.
- **Reference/sound preparer:** reuses masters, prepares necessary state anchors
  and score cues within their separate authority; never starts competing video
  admission or an unrequested paid review.
- **Assembler:** downloads/selects returned footage, updates the asset manifest
  and builds cached ordered sequences while generation continues. One owner merges
  final edit decisions, sound and export; no competing final-timeline writers.

Combine roles when fewer agents are available. Use bounded workers and persistent
artifacts rather than a required agent count. Preserve concurrent edits and prior
accepted work. Give workers exclusive sequence files; the coordinator merges
canonical artifacts and maintains append-only decision history.

Independent camera setups may start from original identity/location masters plus
the agreed state ledger. Do not serialize the whole movie through a recursively
copied final frame. A true same-shot continuation waits for its exact outgoing
edit-point frame where supported and matches lens, framing, motion and sound.
An unresolved predecessor blocks only its dependent branch; fill capacity from
other required ready sequences. Choose a motivated cut when appropriate, never
pretend a discontinuity is a seamless continuation.

## Continuous admission, not batch barriers

Maintain one shared account capacity record across projects. Record the verified
limit, owner, pass expiry, active reservations and the source/time of observation.
At startup reconcile existing accepted and uncertain jobs before new admission.
Observe any other account users or active chats; silence is not proof of vacancy.

Conceptually, on each terminal-job or ready-chunk event:

1. Collect exact job status and preserve returned outputs/receipts. Count queued,
   running, submitting and acceptance-uncertain jobs as occupied. Local polling
   timeout, stale heartbeat or worker exit is not provider termination.
2. Release only reconciled free capacity. Select the highest-priority ready
   required chunk whose dependencies are satisfied and whose authorizations hold.
3. Reserve a slot before submission. Validate frozen inputs and active deadline,
   obtain the adapter's fresh zero-credit estimate and submit once with its durable
   identity. An uncertain POST keeps its reservation and is reconciled, not replayed.
4. Refill immediately when possible. Do not wait for nine other jobs because one
   earlier batch member is slow. Do not await a long individual poll before
   considering other available capacity; use bounded tool polling/resume and
   concurrent authorized invocations under this single admission owner.
5. Download successful outputs and publish usable selections promptly. A terminal
   provider job may release its provider slot while download/edit work proceeds;
   the output remains tracked until safely retained. Account storage, bandwidth
   and provider-specific semantics still apply.

Priority is required opening and dependency-unblocking work, required climax and
payoff, remaining causal story coverage, then diagnosed essential repairs. Avoid
repeated decorative alternatives. Keep a ready buffer ahead of the running jobs,
ideally one capacity-sized group when practical, but never hold the first ready
chunk until that buffer is full. If the buffer drains, prepare the next required
independent unit; do not invent filler to improve an occupancy metric.

When several films are authorized, use the owner's project order. Once the
current film's required jobs are accepted, release surplus/free allocation to the
next authorized film while current jobs finish. Editing/export never reserves
provider slots. A later essential repair reacquires capacity explicitly. Stop
when authorized useful work is exhausted, even if pass time remains.

## Pass-aware completion and accounting

Recalculate needed usable seconds and remaining required chunks from returned
footage. Plan admission against observed latency range, pending critical paths,
downloads and pass expiry. Submit the ending and difficult essential footage
early enough to avoid an unfinished story at the deadline. Reduce redundant
coverage or staging complexity when needed; do not drop causal outcomes or turn
a full movie into a trailer. Never claim the requested length from raw nominal
generation seconds alone.

Stop fresh submissions before expiry using an explicit safety margin; continue
exact accepted-job polling/download where permitted. Nonzero estimates stop that
new submission without destroying accepted work. Unexpected charges are preserved
for reconciliation, and further new admission pauses until entitlement is resolved.
No automatic renewal, pass activation, credit purchase or separately billed route.
Assembly/export and requested delivery may continue after the generation window.

Record UTC timestamps already exposed by receipts: submitted, accepted, first
observed running, first observed complete and download complete. Also record
ready time, coordinator reservation/release, planning start, export and delivery.
First-observed completion is not necessarily the provider's exact completion time.
Measure time to first accepted generation, useful seconds per elapsed hour,
ready-queue starvation, submission/collection gaps and actual finished films.
Count overlapping preparation, generation and assembly once in wall time.
Distinguish provider waiting from local polling delays and from final delivery.

Slot occupancy is diagnostic, not the goal by itself. Count paid-pass cost
separately from incremental generation, images, music and repairs. If the owner
wants an effective cost per film, divide actual attributed pass cost by completed
delivered films and disclose the allocation; raw clips are not completed movies.
Do not convert zero-credit estimates into claims of zero total production cost.

## Current implementation boundary and portable handoff

Local source inspected 3 November 2026: `tools/video/frameo_video.py` provides
one-request submission/resume, native output retention, private receipts,
per-receipt file locking, input hashes, expiry checks and refusal of nonzero
estimates. It does **not** implement a cross-project semaphore, background
scheduler, automatic story planning or complete pass/account verification. The
coordination above is an agent operating protocol, not newly shipped scheduler
software. On another machine, discover current registry support and private
configuration, then appoint the admission owner before starting workers.

The adapter accepts `seedance_2_5`, 720p or explicitly selected 1080p, 16:9,
native audio enabled, integer durations 4–30 seconds, and at most 30 images,
8 videos and 8 audios. The 3 November adapter update forwards 1080p directly
without silently converting a 720p request. Keep 720p as the production default;
1080p still needs explicit owner selection and a fresh zero-credit estimate.
Request support does not establish pass coverage, provider internal rendering,
availability or free generation at any duration. A nonzero quote refuses the new
submission for either resolution; no automatic purchase or paid overflow.
Image roles are `reference`, `first_frame` or `last_frame`; video role is
`reference`; audio entries have no role. Use the adapter's current schema instead
of another host's reference limits. Its `max_poll_seconds=0` still performs one
status observation; pending jobs resume with the exact unchanged receipt/input.
Never change its payload or invent a fresh job path to escape an uncertain receipt.

Provider contract pointer: [Frameo OpenAPI](https://api.frameo.ai/v1/openapi.json).
The adapter records a 3 November contract verification. This workflow audit's
unauthenticated re-fetch returned HTTP 403; it did not independently verify current
account concurrency, price or entitlement and made no generation requests.
Offline boundary examples are in `tests/tools/test_frameo_video.py`; mocked
tests do not prove production latency, frame quality or provider availability.

Use canonical cinematic proposal/script/scene-plan/assets/edit/compose artifacts.
Read each applicable stage skill before its work. With full-run authorization
recorded, keep unfinished whole-film stages `in_progress` and publish frozen
sequence revisions/readiness plus `metadata.partial_progress`; do not falsely
mark the complete screenplay or asset batch finished to start useful work.
Merge final canonical artifacts and validate them before whole-film completion.
Retain one receipt identity, state ledger and ordered selections across resumes.

Finish with one brief local batch check: decode, requested approximate length,
720p/frame fill, actual minimum shot duration, sensible audio, required story and
identity, then requested delivery. Preserve complete native utterances with their
matching picture; inspect known faults/dependencies without routine per-clip ASR,
contact sheets, paid scores, repeated full reviews or cosmetic rerolls. Save a
real nonempty MP4 in the current user's Downloads and working files on available
project storage. Quality parity and production speed remain unproven until a
new film is actually generated, checked and accepted.
