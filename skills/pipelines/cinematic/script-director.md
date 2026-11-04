# Script Director - Cinematic Pipeline

Apply **Complete endings and flexible runtime** in
`docs/ai-video-story-engagement-preferences.md`. Read any supplied source through
its actual end. Put resolution, consequence, relationship payoff, epilogue and any
separate stinger in the existing beat map before assigning provider units. Reserve
useful ending performance; ordinary target durations are approximate unless the
owner states a hard limit. Do not compress the payoff to fill a preset clip count
or expand empty coverage to hit runtime. This adds no separate review/gate.

For AI Movie, read `docs/ai-movie-editorial-continuity-playbook.md`. Write the
audience/character discovery order, action→result and changed state, not a list
of thirty-second containers. Keep future reveals out of earlier references and
spoken staging out of dialogue. Story-bearing cast/role, resource, injury and
growth changes persist. Fit this into existing beat/scene metadata and retain
rolling preparation; no new recurring review process.

For AI movies, apply **Multiple earned tension peaks** in
`docs/ai-video-story-engagement-preferences.md`: build several distinct substantial
suspense sequences into the existing ending-aware beat map. Record feared loss,
setup, active attempt, seeded complication, costly choice, visible outcome and
consequence that drives the next predicament. Vary tactics/pressure, escalate
emotional and practical costs, earn relief and pay off earlier setups at the
climax. Allocate useful action coverage before routine connective material;
backstory reveals, concerned reactions and loud score do not constitute tension
sequences. This adds no review/score/approval loop. Owner rejected the delivered
Living Witness film's tension but requested future-style training only: preserve
its files and receipts; do not automatically rewrite or regenerate it.

Apply `docs/ai-video-global-realism-preferences.md` at the causal story level:
consistent world rules, purposeful actions with appropriate means, established
causes before consequences, persistent costs and legible transitions. Generalize
owner corrections through `docs/portable-production-knowledge.md`; concrete past
examples are not the limit of the rule. Keep these in existing beats, without a
new review or approval stage and without blending distinct style contracts.

For AI Movie Style, follow its current creative-ambition rule: develop an
original high-concept promise, immediate specific curiosity, evolving audience
expectations, emotionally consequential choices, seeded reversals and a complete
payoff. Do not accept a weak premise and hope coverage, spectacle or music will
repair it. Dramatic scale is not limited to a small live shoot; physical/world
coherence and actual authorization remain. Put this once in existing beat metadata.

For narrative AI productions, read `docs/ai-video-story-engagement-preferences.md` before writing beats or shots. Populate the existing artifact with the short hook, distinct extreme turns, seeded consequential surprises, choices, costs and visible payoffs. Preserve factual/source/style boundaries and the current fast autonomous policy; this adds no review or approval stage.

Apply its **Story strength before coverage** correction: runtime is earned by an
interacting chain of goals, opposition, choices, changed tactics and persistent
consequences, not by expanding a short plot into more clip IDs. Track audience
interpretation and supporting-character agency in the existing beat map. Revise
redundant or weak causal sequences before releasing them, then resume authorized
rolling production. Native performance, continuity and a technically valid ending
do not alone qualify the screenplay; no new scoring/review/approval loop.

Use the owner's forty-six-point feedback synthesis in that guide to fill the
same foundation: causal logline/core question, want versus need, early defining
choice, understandable mistakes and learned competence, independent threat logic,
active tactics/geography, changing audience knowledge, setups/reversals/low point,
chosen climax, heart/theme and complete ending. Design visible and sonic evidence,
speech economy and tension/relief. Suggested percentages/line counts are flexible
craft tools. Do not generate fake quality numbers or a new recurring checklist.

After an owner rejects repeated storytelling, use title/style as creative
constraints rather than keeping the sample's incidents. A fresh narrative needs
a changed opening, goal, central question, opposition, causal turns and ending;
all-new generated footage of the same plot does not satisfy that request. Only
an explicit remake/retelling asks to preserve the old narrative. Record the new
causal engine once in the existing foundation before rolling scene release.

For generated human performance, read `docs/ai-video-human-performance-preferences.md` alongside the active style. Reuse selected voices and clean supported references, prepare speech/action/framing/light in the existing shot plan, and qualify through a planned useful dialogue take. This adds no routine review, paid assessment or approval gate. Preserve no-narrator/no-speech and stylized-art rules; premium footage is selective within authorized scope/budget, with the same permitted cast and compatible voice.

## When To Use

**AI movie override:** read `docs/ai-movie-preferences.md` and
`docs/ai-movie-reference-notes.md`. Write a complete character-driven screenplay,
not a sparse trailer/title-card sequence. Every scene has a want, opposition,
choice, changed state and consequence; track emotional attachment and setup/payoff
through the ending. Dialogue performs a task, tests trust or changes a decision;
narration is not a workaround for visible speech. Scale acts to the requested
runtime rather than padding an outline. For selected Frameo unlimited, follow
`docs/ai-movie-frameo-production.md`: lock the global ending-aware spine first,
then freeze exact lines/staging per ready sequence while later writing continues.
Keep partial artifacts truthful and honor recorded full-run authorization rather
than adding routine gates from the generic trailer workflow below.

This stage builds the beat map, selected lines, title-card copy, and reveal structure for the cinematic piece. You are shaping rhythm, not writing a dense explainer.

## Prerequisites

| Layer | Resource | Purpose |
|-------|----------|---------|
| Schema | `schemas/artifacts/script.schema.json` | Artifact validation |
| Prior artifact | `state.artifacts["proposal"]["proposal_packet"]` | Emotional arc and source truth |
| Tools | `transcriber`, `scene_detect` | Optional dialogue mining and source review |

## Process

### 1. Build A Beat Map First

Use a simple structure:

- hook,
- escalation,
- reveal,
- landing.

If the piece is longer, add one midpoint turn. Do not let it become essay-shaped.

### 2. Use Dialogue Sparingly

If source speech exists, use `transcriber` to find:

- strong standalone lines,
- emotional phrases,
- concise declarations,
- reveal phrases.

If there is no useful dialogue, keep the script title-led or narration-led and say so in metadata.

### 3. Keep Title Cards Short

Title-card copy should feel trailer-like:

- fewer words,
- more contrast,
- more whitespace,
- more timing precision.

### 4. Store Beat Truth In Metadata

Recommended metadata keys:

- `beat_map`
- `dialogue_selects`
- `title_card_copy`
- `music_turns`
- `silence_windows`

### 5. Quality Gate

- the beat map escalates cleanly,
- dialogue and title cards do not explain the same thing twice,
- the reveal lands distinctly,
- the landing gives the viewer a final feeling or action.

### Mid-Production Fact Verification

If you encounter uncertainty during script writing:
- Use `web_search` to verify factual claims before committing them to the script
- Use `web_search` to find reference images for visual accuracy
- Log verification in the decision log: `category="visual_accuracy_check"`

Every factual claim in the script should be traceable to the `research_brief`.
If you make a claim that isn't in the research, do additional research and
add the source. Do not invent statistics, dates, or attributions.

## Common Pitfalls

- Writing full explanatory paragraphs instead of beats.
- Using too many title cards.
- Revealing the best moment too early.

---

## Gate Reminder (Binding)

This stage gates on human approval (`human_approval_default: true`). After review passes:
checkpoint with `status="awaiting_human"`, present the summary (the Backlot board renders
the artifact), and **END YOUR TURN**. Do not start the next stage in the same response.
Approval is per-gate — an earlier "go ahead" does not cover this gate.
