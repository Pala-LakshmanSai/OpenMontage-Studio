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
