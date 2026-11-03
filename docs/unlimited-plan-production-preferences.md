# Production during a limited-time unlimited pass

Owner instruction, 3 November 2026: use an authorized unlimited generation window
efficiently. Front-load preparation, start ready independent sequences promptly,
and record actual timing so future estimates improve. Apply this alongside the
current style and [fast production](video-fast-production-preferences.md).

Owner refinement, 3 November 2026: **rolling preparation is the default once the
pass is running**. Lock a concise whole-film causal spine, including the ending,
then finish and release the first useful sequence while later sequences are
written and staged. Do not wait for every line, anchor or shot in the film.
For AI movies use [the Frameo production workflow](ai-movie-frameo-production.md),
including sequence readiness, shared admission ownership and continuous refill.
This explicitly supersedes whole-film-detail-before-generation wording in older
first-pass instructions; every submitted sequence must still be genuinely ready.

Keep this rule in the portable repository workflow through
[portable production knowledge](portable-production-knowledge.md), not only a
single chat or assistant memory. The same shared account queue and deadline
apply across concurrent projects. Honor the owner's requested project order:
prepare a following authorized film while the active film generates, observe the
actual completion/remaining jobs, and release unused capacity incrementally once
the current film's required jobs are accepted. Do not hold an entire allocation
until its slowest job or export finishes. Do not treat another chat's lack of
recent updates as proof that its provider slots are free.

## Prepare outside the paid window when possible

Finish the title-led story, dialogue, useful sequence lengths, identity and voice
references, action/camera staging, continuity states and assembly plan before
activating a time-limited pass. Reuse settled style research and accepted assets.
Do not buy or activate a plan unless the owner explicitly authorizes it.

If the owner has already activated the pass, do not wait for a whole-film planning
document before starting an independently ready sequence. Freeze its story order,
references, spoken lines and continuity first; prepare later sequences in parallel.
Use bounded parallel work within the provider's actual account limit. Keep one
coordinated admission queue so separate workers do not multiply that limit.

## Verify entitlement and references once

Confirm the active window, resolution, model, renewal state and whether API/MCP
usage receives the same entitlement. An unlimited website offer is not proof that
API calls are free. Obtain a free workspace-specific quote before generation; when
the production is authorized only through the pass, refuse nonzero quotes.

Check each newly uploaded reference URL can actually be fetched by the generation
provider, without sending the workspace API key to a media host. A successful
upload does not prove readable media. Cache the successful reference by source
hash. Use the first useful story chunk to establish a valid submission/receipt;
then admit other ready independent chunks without waiting for its full render.
Only shots depending on its actual returned state must wait. Do not add a
separate paid audition or review loop.

Before arming admission, validate the actual resolved request inputs for every
ready chunk, including all selected reference-role names and transport entries.
A plan-shape or dummy-row check alone does not validate a later added scene-state
role. Keep this check local and free; freeze final inputs only after preparation
is settled. A pre-submission configuration failure with no accepted receipt is
repairable without replaying provider work.

Keep accepted jobs and exact receipts. Retry only a diagnosed technical fault with
known terminal failure, a corrected input and a new explicit correction ID. Never
replay uncertain acceptance, bypass provider safety decisions or re-submit usable
footage for cosmetic polish. Preserve native speech-picture pairing and actual
shots of at least two seconds.

## Use the window for generation

Owner refinement, 3 November 2026: for **every AI video style using Frameo's
unlimited plan**, default to **30-second Seedance 2.5 generations**. The owner
observed similar waits for 5-, 15- and 30-second Studio clips; treat that as an
owner observation until this workflow measures it, not a guaranteed API latency
or quality improvement. Use shorter requests only when the required action,
story, reference limit or diagnosed model limitation calls for them.

Pack several deliberately staged shots into one coherent 30-second generation
where appropriate: specify each shot's duration, action, framing, physical camera
path, speech and start/end state. A 30-second request need not be one unbroken
shot. Preserve each style's camera/audio rules and the actual two-second minimum;
never invent extra activity, stretch speech or pad the finished film merely to
fill the request. Plan the film around useful long chunks from the outset to
reduce requests. Preserve already accepted work rather than regenerating it only
to change its nominal length.

Use the account's full verified parallel capacity, promptly refilling each freed
slot from a prepared queue rather than waiting for a whole batch to finish. The
owner specifies a ten-job Frameo workspace limit and describes a USD 100 daily
pass; these are the requested operating assumptions, not a universal current
price, entitlement or fresh account verification. Recheck the account's actual
API limit and pass coverage once per run, then use all available authorized slots
up to that limit. Coordinate all workers against that single capacity; agent count
is not extra provider capacity. Count queued, submitting and uncertain requests
as occupied until provider reconciliation establishes their status. A local
timeout or worker exit does not release a provider slot.
Use exact receipt locks/cached successes when front and back story queues meet.
Keep essential opening, payoff and difficult dependency footage covered early,
then complete the remaining required story before optional variations.

The single admission owner must observe all participating projects and account
jobs, including work submitted outside the current chat. The current
`frameo_video` adapter locks individual receipts; it does **not** implement a
shared account concurrency limit. Do not describe this written coordination
policy as an installed background scheduler or an account-wide software lock.
Use one coordinator for admission and separate workers for preparation,
download/selection and assembly. If another coordinator owns the account, agree
an explicit capacity handoff rather than starting a competing admission loop.

When replacing a worker cohort, identify its exact owned process/session and
verify the other active cohorts remain alive after handoff. Do not stop workers
with a broad command-line suffix match that can select both cohorts. Preserve
accepted jobs and resume their exact receipts after any local interruption.
Record polling/admission gaps separately in timing evidence: delayed result
collection is part of production wall time, not proof of slow provider inference.

Recalculate the remaining plan from actual usable coverage, remaining required
chunks, observed completion/download times, active slots and pass time left.
Keep enough time for the slow end of observed job latency and necessary repairs;
submit required work early rather than waiting until the expiry margin. When
time tightens, simplify achievable staging and reduce redundant coverage while
preserving the complete story, selected cast and required quality. Do not spend
scarce pass time on optional research, reports, cosmetic retakes or final export.
Preparation, downloads and cached assembly may run independently when they do
not delay admission; final editing/export/sharing can finish after the pass.

Generate independent chunks concurrently, download successful outputs promptly,
and assemble cached selections while later chunks run. Editing, free local checks,
export and delivery can continue after the generation window when account access
allows. Do not lengthen every chunk to its maximum if the action or dialogue does
not justify it, and do not pad the final film to hide missing story coverage.

Stop new submissions before pass expiry with a small explicit safety margin.
Continue read-only recovery/download of exact accepted jobs where permitted.
Do not reactivate renewal, purchase credits or start a separately billed route
without owner authorization. Cancellation at period end may preserve already-paid
access; verify the actual provider state instead of assuming either outcome.

## Measure actual elapsed time

Keep a small production timing record in UTC with: owner start instruction,
pass start/end, preparation start/end, each job's submit/accept/complete/download
times, assembly start, export complete and delivery complete. Record available
parallel slots and observed running jobs. Separate preparation time, provider
queue/inference time and end-to-end delivery time; overlapping stages are not
added as if they ran serially. Keep failures and correction counts in the record.

Use observed throughput and usable footage, not advertised unlimited volume or
planned clip length, when forecasting the next film. Label unmeasured scenarios
as estimates. Never promise a fixed complete-film duration from a pass alone.

Capacity planning: approximate completed requests as available parallel slots
times available generation minutes divided by observed request minutes. Multiply
by usable seconds per result for footage capacity, then reserve time for slow
jobs, corrections, dependencies and downloads. Owner example: 10 slots with
10-minute requests over 180 minutes could yield 180 thirty-second clips, or
90 minutes of raw footage, under steady ideal conditions. This is a theoretical
ceiling, not a guaranteed finished-film length or an instruction to generate
unneeded footage. Build a sufficiently prepared story queue to exploit capacity
within the requested scope; report actual successful usable output separately.

When the owner authorizes several projects/chats under the same pass, coordinate
one shared capacity limit. After all required jobs for the current film have
been accepted, publish its remaining active count and release free slots to the
next authorized project incrementally. Release the whole generation allocation
as soon as its required footage is complete; do not hold API slots until editing,
export or sharing finishes. Use a timestamped capacity/release marker and notify
the receiving chat under the owner's messaging authorization. Any later needed
generation must reacquire shared capacity before submission. Never infer a new
film's authorization or budget from unused capacity alone.

Delivery note verified 3 November 2026: the connected Google Drive upload tool
rejected this 488 MB export before invocation because its transport limit was
100 MiB. Browser file upload preserved the full-quality file and succeeded.
For exports above that verified connector limit, use the supported browser file
chooser directly, then verify exact remote size and requested link permissions
through connector metadata. Avoid a failed connector attempt or unnecessary
compression; do not open an audible Drive preview for this check.
