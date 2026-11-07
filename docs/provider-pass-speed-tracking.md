# Shared provider-pass speed tracking

Owner instruction, 7 November 2026: measure KreatorFlow free/pass generation speed
across **all projects**, including the initial fast allowance, any later relaxed
queue, and how speed changes with cumulative use. Record observations while normal
authorized production runs; do not buy tests, generate benchmark-only clips, poll
more often, or add an approval/review stage for measurement.

## One shared ledger

Every KreatorFlow Studio or consumer-MCP production records accepted jobs and
observed progress/completion using `scripts/provider_speed.py`. Its default ledger
is `projects/_shared/provider-speed/events.jsonl`, shared by every project in this
installation and ignored by Git. Set `OPENMONTAGE_PROVIDER_SPEED_LEDGER` once to
an available working-storage path when multiple checkouts share the same account.
Use that same path in every chat/project; never create a separate film-only speed
history. Keep portable policy/code in the repository and actual account/pass/job
records in working storage. Never store keys, cookies, emails, authorization
headers, access-bearing URLs or raw network dumps. Use nonpersonal workspace and
pass aliases and portable relative evidence pointers.

The helper uses the repository's existing portable `filelock` dependency and a
sidecar lock for concurrent writers. On Windows, keep the ledger in a user-private
ACL-protected directory; Unix mode bits do not verify Windows permissions.

The helper only records/reports observations. It makes **zero provider calls**,
does not own admission capacity and never retries, cancels or replaces a job.
Exact provider receipts remain authoritative. Ordinary accepted/uncertain-job,
cost, entitlement, selected-model, speech and continuity rules remain unchanged.

## Record once at each meaningful transition

Use a stable `event_id` per job transition. Identical replay is a no-op; conflicting
content is rejected. Preserve the original; use a new correction observation when
necessary. Record one `admitted` event per real job, including jobs from other
projects using the same pass. A local accepted-card ID must be clearly labeled
`local-card:...` until an exact ID is available; do not count its later provider ID
as another job. Keep one stable ledger job ID and add the exact ID to project
receipts/evidence instead. Workspace/pass identity must not change mid-job.

Required fields: `event_id`, `event`, `provider`, `workspace`, `pass_id`,
`observed_at`. Job events also require `job_id`. Events are `pass_observed`,
`admitted`, `queued`, `render_started`, `progress_observed`, `completed`, `failed`,
`cancelled`, `allowance_observed`.

Record model, route, nominal `duration_seconds`, resolution, aspect ratio,
`generate_audio`, and actual `credit_free` status. At completion, add
`output_duration_seconds` if measured. A pass observation can include model,
`pass_started_at`, `pass_expires_at`, `pass_duration_seconds`, and
`history_complete` (true only after exact whole-pass history is reconciled).
Do not infer pass purchase/expiry or free billing from a badge alone.

All timestamps need UTC offsets. `observed_at` means when the state was actually
observed. Optional `occurred_at` means an exact provider timestamp, never a guess
from a countdown, elapsed display or job order. Record `elapsed_seconds`,
`countdown_seconds`, and `progress_percent` only when shown. Unknown/missing values
stay absent. A partially observed existing job must remain partial: never invent
submission or render-start times from progress percentages/estimated time left.

`allowance_state` is `fast`, `relaxed` or `unknown`. Use fast/relaxed only when the
provider explicitly identifies that mode or its allowance transition. A slower
clip, a nonzero countdown, ordinary serial queueing, or two competing jobs alone
does not establish allowance exhaustion. Put the exact short UI observation and
its relative evidence pointer in `note`/`evidence`.

```json
{
  "event_id": "example-pass:clip-001:admitted",
  "event": "admitted",
  "provider": "kreatorflow",
  "workspace": "owner-workspace",
  "pass_id": "seedance25-pass-20261107",
  "project_id": "example-film",
  "job_id": "local-card:clip-001",
  "model": "seedance_2_5",
  "route": "studio",
  "resolution": "720p",
  "aspect_ratio": "16:9",
  "generate_audio": true,
  "duration_seconds": 30,
  "credit_free": true,
  "allowance_state": "unknown",
  "observed_at": "2026-11-07T06:40:00Z",
  "evidence": "projects/example-film/receipts/clip-001.json"
}
```

The example is a schema illustration, not a real job. Save a real observation to
a local JSON file, then run:

```sh
rtk proxy python3 scripts/provider_speed.py record --json-file /tmp/speed-event.json
rtk proxy python3 scripts/provider_speed.py report
```

Use `--ledger /available/shared/events.jsonl` **before** `record` or `report` to
override the shared location. No report or sidecar belongs in Downloads.

## Interpret measured speed honestly

Reports separate queue (accepted to render start), render (render start to
completion) and total (accepted to completion). Each interval uses either two
provider timestamps or two observation timestamps, never a mixture. Observation
intervals include polling uncertainty; a partial job has no invented total.

Summaries count observed admissions/completions, cumulative completed nominal
seconds and measured output seconds separately (including measured-duration sample
counts). The first explicitly observed relaxed transition also reports preceding
observed admissions/requested seconds. These are **observed transition counts**,
not a fixed fast quota, particularly when earlier history is incomplete, allowance
replenishes, clip durations/resolutions differ, or other projects use the pass.
Never turn a provider estimate into a measured latency or missed output into a
terminal failure.

Compare fast versus relaxed total turnaround only for like model, duration,
resolution, aspect ratio, audio, route and timestamp basis; reports include sample
counts, medians and their ratio. Keep unknown-mode jobs separate. The ledger's
per-job queue/render intervals and displayed countdowns explain where a slowdown
appears. A measured slowdown is not proof of its scheduler cause. Do not generalize
one clip or one pass to guaranteed future speed.

## Observed capacity interaction, 7 November 2026

During Moonwalk production on a Creator workspace, Studio showed an Unlimited
quote with “Starts after your 1 lined-up clip”, but submitting the next prepared
clip was explicitly refused: “Creator limit reached”, usage1/1, “Wait for one
video to finish before starting another”. No next job was created; its archived
receipt is `projects/moonwalk-night-1983-20261105/receipts/kreatorflow/C011-r01-capacity-rejection.json`.
The next clip was accepted after the active pass clip completed. Treat a refused
request as zero admissions; a promised queued UI state is not an accepted job.
Distinguish the underlying workspace admission limit, a pass's serial-render rule
and any fast/relaxed queue. This observation does not establish API concurrency
or prove that upgrading a paid plan raises the unlimited pass's one-clip limit.
