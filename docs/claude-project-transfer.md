# Transfer OpenMontage to a fresh assistant

Owner instruction, 5 November 2026: production training must travel with this
repository. Do not depend on the owner's Codex memory, previous chats, private
Pages, original drive paths or an assistant's recollection. This applies to
Claude Projects and to a friend's fresh Codex checkout.

## Create the context from current source

Use `python scripts/export_claude_project.py --output <directory>` on a clean,
reviewed checkout of the public repository. The exporter creates searchable
knowledge and production-source Markdown, a file/hash manifest and a bootstrap.
These contain exact repository text with original path headings. Upload the
Markdown files as project knowledge and use the bootstrap as project instructions.
Keep each attachment below 200KB: the first live Claude test observed a 262144-byte
read cap and unreliable source search inside multi-megabyte bundles. The exporter
therefore splits at roughly180KB. Include every numbered part and the manifest;
read adjacent parts when a file continues. Remove superseded giant bundles after
the new parts are visibly saved. Do not equate successful upload with full reading.
The public repository remains the executable install/update source. A ZIP may be
retained for installation, but the Claude Project uploader rejected ZIP context
on 5 November; do not claim it is attached because a file chooser accepted it.

The knowledge file must contain every indexed style, its optional production and
screenplay guides, and all shared policies. The source file contains the local
pipeline, adapters, schemas, stage skills, validators and setup entrypoints.
The manifest proves file inclusion and bytes, not whether a model will follow them.
Exclude live configuration, credentials, private history, generated projects,
caches and media. Configure permitted provider credentials separately.

## Retrieve without prior memory

Start with `AGENT_GUIDE.md` and `docs/production-knowledge-index.json`. Select the
named style, then read its guide, template, reference notes and playbook plus
applicable shared policies. Current owner instructions and newer canonical rules
override older examples. In particular, AI Movie and Queen Elizabeth I require
whole-story adaptation and a reviewed complete screenplay through the ending
before new media. Their foundation guides supersede spine-only start wording.
Afterward overlap independent detailed preparation, generation and assembly.

Preserve each style's source, art and sound contract. Raw observational documentary
rules do not become a narrator/music rule for science or historical vlogs. Retain
selected cast/voice/world state, meaningful causal actions, natural performance,
native speech-picture timing, complete endings, actual two-second minimum shots,
720p/768p defaults, real budgets and accepted/uncertain-job safeguards.

## Test transfer before claiming it works

Owner update, 6 November 2026 IST: include
`docs/ai-video-action-clarity-and-pacing.md` and the updated AI Movie style/prompt,
foundation, editorial playbook and stage instructions. In a fresh planning-only
chat, present an ambiguous edge lean followed by an underwater shot. The assistant
must not certify a voluntary dive from those states; it should identify missing
decision/movement evidence and propose concise visible staging. Also present a
long repeated approach with no new information. It should tighten that passage
while protecting the choice and completed action, rather than prescribe more
runtime or random faster cuts. Text retrieval success is not finished-film proof.

Use fresh chats inside the destination project, not an existing production chat.
Request read-only planning; prohibit media generation, purchases and paid review.
Check the answers against the actual canonical files. Do not feed the expected
answer into every test and then call repetition independent discovery.

1. Ask for all registered styles and correct file routes, scheduling exceptions,
   sound/source differences, provider choices, runtime and delivery defaults.
2. Give a short title/style/length brief. Check a causal story and actual staging:
   hook, attempts, changed tactic, cost, payoff, transitions and meaningful reaction.
   Raw activity documentaries should film work rather than present objects to camera.
3. Present conflicting old guidance, a stale screenplay/cut list, a concealed prop,
   an irreversible state change, a queued uncertain job and a live pass deadline.
   Check the current rule, local remedy, independent work and no-replay response.
4. Ask which execution tools, credentials, media and observed evidence are actually
   available. Source attachments do not install adapters or grant account access.

Record actual prompts, observed answers, corrections and remaining gaps locally.
Save only reusable lessons and a sanitized result summary in the public project.
If an answer fails, repair the canonical rule/routing or context package, update
project instructions/files, and rerun the affected case in a new chat. Retain
successful rules; do not add paid scoring or unbounded cosmetic review loops.
Text tests establish scoped instruction retrieval/application, not absence of every
possible gap, subjective storytelling parity or finished-film speed/quality.

## Inventory and evidence discipline in fresh-context tests

Fresh Mac-app audit, 6 November 2026: correctly recalling shared rules did not
prevent mistaking an engine routing label for an installed YAML, incomplete
style-guide retrieval or
an overconfident claim about the semantic coverage validator. Correct that layer
without changing successful production aesthetics or adding routine paid review.

For a requested complete style comparison, derive trained profiles and exact
original file routes from the current knowledge index, then read each compared
style guide for its distinguishing contract. Derive generic playbooks from actual
current `styles/` files or an exact source manifest, not remembered product names.
A routing-summary answer is explicitly partial when its underlying guides remain
unread; finish those reads before calling the requested comparison complete. An
ordinary film still reads only its active style and applicable policies. Before
authoring even a preliminary plan, directly read the active preferences, template,
reference notes and applicable policy text; search excerpts and routing summaries
are navigation, not completion of mandatory reads. Do not defer that step until
after presenting the plan. If retrieval truly fails, name the missing source and
keep that portion provisional rather than claiming style readiness.

Keep supplied scenario descriptions, directly inspected footage, recorded metadata
and executed validation distinct. A hypothetical cut description supports a
conditional diagnosis, not a claim that frames or performances were observed.
`lib.narrative_continuity` checks recorded coverage integrity; a semantic picture
fault is not guaranteed to fail it if metadata is stale or falsely asserts the
intended beat. Describe the actual run/result only after running it; never turn
an expected failure into a measured failure. Unaccessed runtime, credentials or
media are unverified, not proven absent. Name the actual missing read, permission
or evidence and continue available preparation. Existing/continued films retain
approved cast bindings when media is unavailable; do not silently substitute a
new face to resolve missing access.

## Keep the transfer current

Attachments are snapshots, not automatic Git synchronization. Record their source
commit and manifest. Before later productions, use the install/update guide on a
real checkout, or compare the current public commit and refresh changed context
files when supported. Replace stale attached versions rather than accumulating
contradictory copies. Do not wait for every unrelated edit to finish: publish a
coherent reviewed snapshot, then export that exact version. Continue publishing
durable new feedback in canonical policies/templates first.

For a fresh Codex or Claude Code environment, install/open the actual repository
and run `python scripts/check_production_knowledge.py`. Use the receiving device's
storage and Downloads. The setup does not by itself transfer account entitlement,
the original film's cast media, tool permissions or observed performance evidence.

## Verified transfer lessons — 5 November 2026

Live fresh-project chats retrieved all nine styles, the whole-screenplay foundation,
exact native-audio/state/short-shot rules and Frameo receipt implementation from
numbered attachments. An original two-minute court-comedy trial applied concealed
prop staging, supporting-character action and persistent exit states. This was a
text planning trial, not finished-film acceptance or proof of equal creative quality.
The audit found and repaired a recurring documentary sample gate, a missing indexed
vlog efficiency guide and its broken link. The Frameo adapter now uses the existing
portable filelock dependency rather than importing POSIX-only fcntl; preserve the
same receipt lock path and no-replay behavior. POSIX mode checks remain enforced.
On Windows, keep credentials and receipts in a user-private ACL-protected directory;
a Unix mode bit is not proof of a Windows ACL. No Windows live generation was tested.

The Claude web project has readable source context, not an installed local runtime.
Its execution/tool and provider-access gaps must be checked in the selected Claude
Code/local environment. Native desktop UI inspection failed during this setup;
do not describe that local-folder connection as verified. Attachments also do not
include private selected-cast media or existing production receipts: transfer those
separately when continuing an existing film, preserving their project-relative
references and private access. New title-led films can establish their own cast.


A second-account Mac-app trial on5November saved36 readable attachments and the
source-derived bootstrap. The fresh story answer applied raw work-led sound and
state costs, but its planned shot sums and30-second source assignment disagreed.
This is a failed initial timing test, not parity proof. The canonical realism guide
now requires ledger arithmetic, feasible request boundaries and credible material
elapsed time before generation; retest that case after transfer. Attachment search
may return no results even when files are saved. Directly read numbered parts;
when permitted, a clean public checkout at the exact manifest commit is a fallback.
Record which source was actually read. A public clone tests repository portability,
not proof that every attached part was retrieved. Never infer installed provider
access, private cast assets or credentials from a successful source read.


In the Mac-app audit, helper agents could not access project files even though the
parent could read them. Do not keep delegating identical failed reads or finish a
required-file audit with those files unread. The parent directly reads the relevant
numbered parts and continuations. Ordinary production reads its selected style and
applicable shared policies rather than all styles at once. Public-checkout fallback
is reported separately from attachment retrieval; test the source actually used.


## Mac update and application test — 6 November 2026

When the native file chooser fails, the app's Add text content control can save
readable source chunks. Keep complete original FILE blocks below200KB and supply
a source-commit/path/hash/part manifest. An exact current-file delta may override
matching older snapshot paths when instructions make precedence explicit; preserve
unchanged required files and verify available project capacity. This is a source
snapshot, not automatic upload of later repository changes. Prefer a current linked
checkout when permitted, and distinguish that read from attached-text retrieval.

A fresh rules test applied the6November action/performance/time-cue/title and
historical-vlog rules from the linked current source. A separate minimal title-led
script retrieved updated attached text but skipped material processing, confused an
intermediate authorization with a completed outcome and misfit scene/request time.
Thus retrieval alone did not prove application. The global realism guide/bootstrap
now makes the existing authoring completion check explicit; test a corrected plan
and a fresh minimal brief before claiming scoped transfer success. No text result
certifies future footage quality or absence of all possible gaps.


## Automatic maintenance of the configured Claude Project

Owner instruction, 6 November 2026: new durable preferences, style improvements
and reusable production fixes must reach the configured Claude Project without
another update request. Save canonical repository changes first. At the end of a
coherent publication, refresh the configured project when native computer use is
available; the existing hourly repository heartbeat also catches up missed syncs.
Do not create a second competing updater or wait for unrelated active edits.

Keep machine-specific targeting and progress in ignored
`.private-config/claude-project-sync.json`, never in public source. Record the
native app, expected account label, project URL/name, linked public checkout,
base attachment commit, current override entries/manifest, last successful source
commit and timestamp, and any pending target or concrete failure. No credentials,
private setup or access-bearing URLs belong in context or public receipts.

Each run compares the latest reviewed public source with the last successfully
synced Claude version, even when there is nothing new to publish. Verify the
selected native app account and project before writing; do not switch to a
similarly named project in another browser/account. Prefer the linked current
public checkout for production reads. Its changing files and attached snapshots
are different sources: refresh changed attached canonical FILE blocks, their
commit/path/hash manifest and project instructions when relevant source changes.
Use the exporter on the exact clean reviewed public commit. A delta must preserve
unchanged baseline files and contain the cumulative current overrides since that
baseline, not only the most recent commit. Explain precedence explicitly.

Prefer editing generated text entries in place when the UI supports it. Verify
controls rather than assuming editing exists. If entries cannot be edited, add a
small clearly versioned override while capacity allows; avoid duplicate full packs
or an unbounded pile of snapshots. If a complete refresh cannot fit, retain the
existing project and record attachment sync as pending. Continue through the
verified linked source where available; do not silently omit affected rules or
claim attachments are current. Do not permanently remove old knowledge without
the confirmation required by the UI policy. Preserve the previous local export.

Verify saved instructions and context entries in the actual UI before advancing
the successful-sync receipt. Record linked-source, instructions and attachment
versions separately when only some succeeded; retry the pending portion later.
The native app silently truncated project instructions at about10,000 characters
in the7November maintenance run. Keep the complete instruction text below9,900
characters and reopen it to verify the final precedence/rule, not only the commit
near the beginning. Compress repeated summaries without removing unique rules;
retain canonical attached/linked source and all required snapshot precedence.
If unique required instructions cannot fit, record that portion as pending rather
than treating a successful Save or partial readback as a complete synchronization.
If the app is unavailable, account differs, access is missing or capacity blocks
the refresh, preserve the pending target and continue safe repository work.
A scheduled UI refresh requires this Mac and its signed-in apps to be available;
this is not a server-side Git attachment integration.

Skip unchanged checks and avoid routine Claude model calls, paid media or reviews.
For a substantive retrieval/routing change or an observed failure, use the fresh
planning-only test above and record its scoped result. Updating knowledge does not
retroactively change existing chat responses or prove future footage quality.


## Native linked-source access — 6 November 2026

A read-only planning task may still need the normal per-session folder grant.
In the Mac trial, initial computer/list calls failed without that grant; after
allowing the reviewed public checkout for the session, native commands read its
current commit, guide, index and production policies. The user did not need to
reteach the production preferences. Request only the already-authorized reviewed
public source folder, respect the task's read-only restriction and keep private
configuration outside it. A folder grant does not establish provider entitlement,
private cast access or a completed runtime installation.

An attachment-only test with terminal commands disabled checks a different route.
Record that limitation rather than inferring that normal source access is broken
or that an uninspected runtime is absent. Prefer the verified linked source for
normal production; use exact dated attachments when that route is unavailable.
Keep retrieval coverage and actual creative application as separate test results.
