# Keep the private production repository current

Owner authorization, 3 November 2026: publish the trained project and keep durable
preferences, new styles, reusable corrections and completed tool fixes updated on
the public `Pala-LakshmanSai/OpenMontage-Studio` repository. The existing private
`Pala-LakshmanSai/OpenMontage` retains its history and private setup asset.
The owner also authorizes the private setup asset
for the friend's installation. Keep private setup material separate from public source. An authorized reader
with access to the private asset can use the owner's
configured provider accounts. Do not put credentials in ordinary source commits,
Pages, logs, model prompts or public artifacts.

## Every durable correction

Update the canonical shared policy or named style guide first, then affected
templates/playbooks/routing. Add a new style to `production-knowledge-index.json`.
Preserve style-specific sound/source/art rules and acceptance status. Generalize
the useful cause and repair; do not copy raw chats, private correspondence,
unrelated memory or an entire temporary production log into training.

## Scheduled publication

1. Read `AGENT_GUIDE.md`, the knowledge index and current repository status. Check
   whether any relevant file is still being edited by an active production.
   Snapshot only completed source/training changes; do not interrupt workers.
2. Run `scripts/check_production_knowledge.py`, relevant local tests and YAML/schema
   checks. Run no paid media generation or reviews. Skip unchanged updates.
3. Use the isolated public publication checkout or a `codex/` worktree based
   on its public origin. Never push private Git history; it contains historical
   credentials. Publish reviewed current files only.
   Preserve remote-only changes and concurrent local edits. Copy the reviewed
   source changes, including required untracked adapters/tests/docs; do not assume
   `git diff` includes untracked training files. Never add the entire home folder.
4. Exclude `.env`, private key files, `.private-config`, generated projects/media,
   local caches, model weights, private URLs/receipts and machine-only settings.
   Scan the exact staged content for credential values without printing them.
   The credential setup asset is a separate explicitly authorized private release.
   Research packs publish distilled craft notes, coverage metadata and public-field
   summaries. Raw external analysis responses, private service job identifiers and
   original provider receipts remain local even when stored under `docs/evidence`;
   that directory name does not make them publishable. Link a sanitized summary
   instead of requiring those private files on a fresh checkout. Preserve originals.
5. Commit a coherent tested snapshot and push normally to the public default
   branch. No force push, history rewrite, reset, clean or deletion of other work.
   If remote changes or unresolved faults prevent a safe push, preserve the
   snapshot and report the specific actionable issue.
6. Verify the remote commit and required files from the resulting tree. Save a
   lightweight local publication receipt. Report only a new published update or
   an actionable failure; remain quiet when nothing meaningful changed.

The friend's agent updates through `docs/install-and-update.md`. New production
requests discover current training from the source tree automatically. Updating
code does not grant fresh paid-film authority or extend an expired unlimited pass.

## Private setup changes

The current bundle contains named `provider.env` and `frameo-api-key` entries,
served as `openmontage-private-setup.zip` on private release `owner-private-setup`.
Create it in a private temporary directory from authorized local configuration,
upload with authenticated GitHub CLI, and remove the temporary archive afterward.
Do not expose values, publish a public release, put signed URLs in memory, or
overwrite a friend's existing local keys without the explicit refresh option.
The installer reads only named entries rather than extracting arbitrary ZIP paths.
An earlier private remote commit included `.env`; current publication removes it
from the current tree. This is not a claim that historical Git objects were erased.
History rewriting or key rotation requires separate deliberate coordination.

The public repository starts from a clean current-file snapshot with no private
history or setup assets. A local credential ZIP can instead be supplied to the
installer through `--private-config`; no per-key entry or private GitHub login is
needed for that local route.
