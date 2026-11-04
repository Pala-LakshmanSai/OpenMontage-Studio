# Portable production knowledge

Owner instruction, 3 November 2026: production preferences, style training and
reusable corrections belong in this project. A new chat or another computer must
be able to discover them from the copied repository without the original chat or
the owner's personal Codex memory.

## Read automatically before production

Read [the style and policy index](production-knowledge-index.json) first. It lists
all saved AI production profiles and the shared rules inherited by current
and future styles. Installation/update requests follow
[the portable install guide](install-and-update.md), including authorized private
API setup. Run `python scripts/check_production_knowledge.py` after changing the
training or moving the repository; it requires no personal memory or paid calls.

Every assistant entrypoint must lead to `AGENT_GUIDE.md`. Read that guide, then
the current style's preferences, reference notes, prompt template and playbook.
Follow their links to shared policies; do not ask the owner to repeat already
recorded training. Current explicit owner instructions and verified provider
state override older saved guidance. Preserve the current style's art, source,
voice, sound and approval rules rather than blending incompatible styles.

Shared production policies include:

- [AI Movie editorial and continuity playbook](ai-movie-editorial-continuity-playbook.md): portable sequence/state/reference/camera/edit practice distilled from the owner-requested delivered-film review; read for AI Movie, generalize shared causes without importing its aesthetic into other styles.

- [Extreme story and surprise planning before generation](ai-video-story-engagement-preferences.md): apply the operational hook/escalation/choice/cost/payoff contract, not just generic promises of danger.

- [Fast production and zero routine paid reviews](video-fast-production-preferences.md).
- [Frameo unlimited: useful 30-second chunks, shared parallel slots and deadline-aware generation](unlimited-plan-production-preferences.md).
- [Realism, causal story development and environmental continuity](ai-video-global-realism-preferences.md).
- [Extreme story turns and consequential surprises](ai-video-story-engagement-preferences.md).
- [Human performance](ai-video-human-performance-preferences.md), [voice selection](ai-video-voice-selection-preferences.md), and [minimum actual shot duration](minimum-shot-duration-preferences.md).
- [Image providers](ai-image-generation-preferences.md), [music and sound rules](ai-music-preferences.md), and [first-pass preparation](ai-style-first-pass-sop.md).
- [Reusable production failure lessons](ai-video-production-lessons.md) and
  [portable delivery defaults](video-delivery-preferences.md).

The shared policies apply to existing and future styles when relevant. A new
playbook or template must inherit them through explicit links. Frameo's current
account limit is shared by all chats and workers, not allocated separately to
each film. Follow the owner's project priority and coordinate handoffs against
the actual running jobs and remaining generation window.

## Preserve learning in the project first

### Generalize owner feedback before saving it

Owner clarification, 3 November 2026: this applies to corrections from any chat
or production, not only the current film. Identify the underlying failure and
causal reason, save the smallest actionable shared principle, then test its scope
mentally against similar situations involving different subjects or tools. Keep
the reported scene as supporting evidence/example, not the whole instruction.
Use the [global principles](ai-video-global-realism-preferences.md) for persistent
state, physical causality, object affordance, spatial relations, motivated
performance, perceptual readability and temporal/edit continuity. A local dressing
error, for example, reveals the wider need to preserve all attached/changed object
states across views; it must not become a hand-only rule.

Put a correction at the narrowest correct scope: shared policy for a general
failure, named style for its aesthetic, project ledger for this film's concrete
facts, and provider guidance for a verified technical constraint. Keep deliberate
style exceptions and current authorization intact. Merge overlapping corrections
into canonical guidance; do not copy a growing checklist into every style or
convert a specific preference into an unsupported universal requirement. Update
existing templates/routing to inherit the principle and keep evidence honest.
Apply this when incorporating saved past lessons and all future owner feedback;
do not claim unrelated chat history was exhaustively reviewed when it was not.

Implement learning in existing preparation and concise references/prompts, with
one brief essential check and targeted fault repair. A new complaint does not
automatically justify another review service, test, approval gate or retake loop.

When the owner adds or corrects a durable production preference, update the
relevant shared policy or style document, its reusable prompt template and any
affected routing/playbook. Keep one canonical rule and link to it instead of
copying a conflicting version into every file. Preserve accepted identities,
voices, reference-study evidence and concrete failure lessons in the relevant
project artifacts. Separate owner acceptance from technical delivery and state
which claims have actually been verified.

Record the decision and rationale, source/date, applicable styles and important
evidence or next step. Do not turn temporary queue status, speculative quality
claims or account latency observations into permanent guarantees. Update the
configured Project Memory index and relevant Pages when accessible. Optional
assistant memory can point to these repository files; it must not be the only
copy or a prerequisite for production. Do not assume the receiving assistant has
this owner's personal memory or access to the same Pages.

## Moving to another computer

Copy the repository's instruction files, `docs/`, `styles/`, pipeline manifests,
skills and required project artifacts together. Resolve required selected media
and external-drive paths before production; copying a symlink does not copy its
target. Use project-relative references where supported and discover the current
export directory, storage and provider availability on the receiving computer.
Never copy private credentials into these instructions, prompts, memory or public
handoffs. Configure authorized credentials separately and verify actual account
entitlement and supported controls instead of inheriting dated access claims.

The instruction routing makes the knowledge discoverable across assistants. It
does not establish that a different computer has been tested or guarantee that
every model follows instructions or produces accepted footage.
