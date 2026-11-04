# The Last Day — explanation, continuity and edit playbook

Adopted 3 November 2026 after the owner's requested comparison of the complete
nuclear pilot with the five most popular reference films. Read with the
[style guide](the-last-day-style-preferences.md),
[prompt template](the-last-day-style-prompt-template.md) and
[Frameo workflow](the-last-day-frameo-production.md). These are production
instructions, not proof that the next film will match the reference. The
[comparison](the-last-day-refinement-20261103.md) separates observations,
measurements, hypotheses and review limits. Reuse this training; do not repeat
the channel study during normal production.

## The central change

Make the viewer follow a changing physical system, not a succession of narrated
topic illustrations. A technically valid export can still explain the wrong
cause. Every important beat needs an understandable incoming condition, a
specific cause, an observable change and a consequence that persists. Attractive
footage of a field is not evidence of crop failure; mechanically correct tap
rotation is not evidence that a pump lost power.

Thirty seconds is the preferred provider request envelope. It is **not** a
paragraph length, chapter length, music cue, mandatory retained duration or
reason to abandon an unresolved process. Outline variable explanation beats
first; pack compatible shots and complete utterances into generation requests
afterward. Plan useful coverage and clean phrase/action boundaries, not excess
filler. Preserve the requested finished duration using useful story coverage.

## Make the opening's picture and promise agree

Within the first useful shots, show the title's distinctive event or a concrete
consequence that makes the question urgent. Establish counterfactual rules in a
short intelligible passage while something meaningful happens. Essential truth
must remain explicit, but two introductory half-minute disclaimers are not a
default. A historical film must not invent an event to manufacture its hook.

Write the opening as pairs: **spoken proposition → visible evidence or explicitly
identified illustration**. If the line says empty, the image must not show plenty.
If a normal scene supplies a baseline or deliberate irony, signal that relationship
before the viewer has to guess. A familiar object can carry stakes more clearly
than a montage of unrelated explosions. Do not promise inevitable starvation,
extinction, a precise toll or a model result unsupported by the scenario.

Keep two distinct obligations: the immediate question that earns attention, and
the answer the ending owes. Owner correction, 4 November 2026: the hook normally
lasts about 8–12 seconds (15-second maximum); begin the premise or mechanism by 15 seconds. Use useful
2–6-second opening picture beats, each at least two seconds, rather than retaining
a first shot or diagram for the provider's 30-second envelope. Essential setup
continues as new explanation after the hook. These are production instructions,
not a retention formula or measurements of every reference opening.

### Check the actual opening once

The black-hole film exposed two missed faults: a substantial narration phrase
repeated inside the opening and an overlong first diagram shot. A source hash,
quiet endpoint or complete final sentence cannot prove that a take says its text
once. A generation can repeat its own clause, and neighboring chunks can replay
the same thought even when both were retained in full.

Before generation, give every spoken thought a unique utterance ID and one place
in the final sequence. Compare each chunk's first and last clauses with its
neighbors; do not put the preceding clause into the next chunk's speech contract.
Tell the provider to use any voice reference for vocal character only, never its
spoken content, and to speak the exact assigned text once without restarts.

Before delivery, make one bounded local check of the actual assembled first
60–90 seconds, including joins. Reuse the cached transcript keyed to that exact
audio/source hash, or transcribe only this excerpt locally if absent. Compare
substantial repeated clauses, the actual hook endpoint and observed picture cuts.
Investigate an identified overlap later in the film with just its neighboring
phrases; this is not routine whole-film or per-clip ASR, paid review or a new
approval gate. A deliberate callback needs a reason and evidence, not a blanket
exception for repeated words. Preserve negation and meaning when comparing text.

`python -m lib.last_day_opening opening-evidence.json --output opening-check.json`
consumes the cached evidence without calling an ASR or provider. Its JSON input
contains the final MP4's `source_sha256`, matching `transcript_source_sha256`,
`actual_audio_transcribed: true`, `window_end_seconds` (60–90), observed
`hook_end_seconds` with `hook_evidence`, `picture_boundaries_seconds` beginning
at zero with `picture_boundary_evidence`, and transcript `segments` containing
`start`, `end` and `text`. Keep the input/report with the existing edit artifacts.
Optional `repeat_dispositions` require exact `phrase`, `reason` and `evidence`.
New `the-last-day` compose completion requires the input path under
`last_day_opening_check_input` in checkpoint metadata or `render_report.metadata`.
Use a project-relative or absolute path. The checkpoint recomputes this pure check
and requires a pass matching the actual MP4 bytes; a saved `status: pass` report
alone is insufficient. Both source-hash fields bind the transcript evidence to the
full final MP4, not just a WAV/excerpt. Retain an excerpt hash separately for ASR
cache reuse. The checkpoint runs no ASR, network or paid service and adds no user
approval stage. Publishing an older completed export is not retroactively gated.
The checker flags substantial exact nearby repeats, a hook beyond 15 seconds,
and any opening picture beat starting before 15 seconds outside 2–6 seconds. Boundary evidence must cover that interval and agree with the cached actual cut report; a short first shot cannot excuse a long second hold. A flag needs a concrete repair or documented
intentional treatment before delivery; missing actual evidence is not a pass.
The transcript is the reusable expensive result; the checker itself is local and
cheap. ASR can miss or mishear words, and this lexical check cannot guarantee no
semantic repetition, natural delivery or every future editing fault. Inspect the
specific flagged passage and record the limits honestly.

## Follow one thing through several changes

Choose a small recurring set of recognizable places/systems/objects appropriate
to the title. For example, one water service, its neighboring clinic and a
household food supply; not a new anonymous household for every sentence.
Establish identity through a master view, geography, material details and stable
references. Record each return's changed state and unanswered question. Never
reset damage, available supplies, water level, light or elapsed time accidentally.

Use a scale ladder when it reveals causality:

1. Establish the functioning system and its relevant input.
2. Show the cause changing that input or a component.
3. Reveal the hidden relation with a material insert or accurate cutaway.
4. Return to the same system's changed output.
5. Show what a person, ecosystem or connected service can no longer do, or does
   differently. Carry that constraint into the next beat.

Not every beat needs all five steps. A two-shot demonstration may be enough;
complicated mechanisms may need more than one generation. Alternate process,
human consequence and scale deliberately. Each cut should change useful
information, reveal a cause/result or give an action time to complete.

Create turns that revise the viewer's understanding: an intact building is not
a functioning hospital; a harvest somewhere is not a delivered meal here; a
large local wave is not automatically an equal wave across an ocean. Use only
factually defensible turns for the selected premise. Do not add random disasters
or force every title into the same food-system plot.

## Attach uncertainty to the thing it changes

State the global scenario boundary clearly once, then retain specific limitations
at their relevant claims. Replace repeated generic uncertainty paragraphs with
a concrete comparison where possible. For smoke, for example, distinguish lower
air where removal can occur from a conditional pathway that carries soot higher;
do not equate a detonation mushroom cloud with proof of persistent fire soot.
Use verified sources for the actual mechanism and model assumptions.

A qualitative diagram must announce its qualitative nature through its design
and wording. Never invent quantitative axes, threshold heights, timings or
geographical damage rings. Keep one graphic language across the film: consistent
colors for the same substances, spatial orientation, typography, units and
temporal conventions. Highlight the changing relation rather than replacing
one broad flowchart with another. Diagrams reveal invisible relations; return
to a recognizable physical consequence afterward.

Give every essential local diagram an asset ID, factual claim, exact labels,
encoding/scale limits, owner, timeline placement and completion status. An
instruction to add labels later is an outstanding deliverable. Prefer a correct
local diagram from the start when geometry or text carries the explanation.
Do not routinely generate misleading science footage and plan to repair it.

## Narration and sound belong to the explanation

Apply the [sound/narration guide](the-last-day-sound-and-narration.md), including
the owner's substantially quieter score correction and measured cadence findings.

Write complete thought groups with varied sentence length and intention. Track
the preceding and following thought across request boundaries. Leave natural
space for a result to register; do not fill every 30-second request with the
same 65–70 words. Use the settled voice and authorized route. Native reference
conditioning helps continuity but does not establish identical timbre/prosody.

Mark audio roles: offscreen narration, visible dialogue, synchronized action,
ambience and music. Offscreen explanation may bridge a motivated change of
illustrative picture when its meaning and timing stay honest. Visible dialogue
and meaningful synchronized actions retain their native pairing. A mixed native
track does not magically supply clean stems: do not detach a sound that would
misrepresent its source, or promise isolated dialogue that the route cannot
return. Preserve all necessary words, breath and action; an edit is not permission
to truncate speech. Separate TTS/stem services still need actual authorization.

Map score changes to story turns: curiosity, demonstration, widening consequences,
decision, aftermath and reflection as appropriate. Use only available authorized
cues, with a deliberate source range, placement, transition and breathing space.
Do not calculate the emotional ending from a fixed percentage of runtime or
restart music per generation. Repeated motifs can be intentional; loudness
numbers and crossfades alone do not establish a good mix. No available authorized
score means continue with permitted native sound, not a purchase or broken path.

End with a complete final phrase and a meaningful picture/sound landing. Plan
the tail before generation. Do not manufacture a long static hold or slow speech
to fill length. Explicitly signal a counterfactual's return to present reality;
a restored full table must not imply an unearned recovery inside the disaster.

## Compact records in the existing cinematic artifacts

Use existing metadata fields and sequence contracts; do not introduce a second
pipeline or claim this document is executable enforcement. Store the details
where writer, admission owner and assembler can share them.

| Record | Minimum useful fields |
|---|---|
| Explanation beat | ID; incoming question; new information; claim IDs; mechanism; visible demonstration; consequence; next question; duration range; required/payoff status |
| Utterance | ID; exact words; voice reference/hash; intention; prior/next thought; complete phrase boundaries; actual timing when available; audio role/stem availability |
| Shot | ID; beat ID; five aspects; visual job; incoming state; triggering cause; outgoing state; phrase/claim correspondence; required synchronized sound |
| Generation chunk | ID/revision; included beat/shot/utterance IDs; requested duration; typed dependencies; resolved references/hashes; ready status; priority; immutable receipt identity |
| Selection | Source hash; actual frame range; actual cut boundaries; keep reason; audio source/range; complete speech/action; picture override if any; selected runtime |
| Local graphic or cue | ID; owner; exact content/authorized source; narrative purpose; timeline range; completion/hash; transitions or encoding limits |

Dependencies are typed: a settled voice, a reusable location master, an exact
outgoing editpoint frame or a required generated state. Only genuine dependencies
wait. A later independent shot is not ready if its essential reference has not
actually been resolved, even if its prose prompt is complete.

## A worked redesign of the nuclear pilot

This is an original planning example, **not a generated replacement**, scientific
forecast or fixed template for every subject. Recheck primary claims for a real
production. Retain the pilot's impossible simultaneous in-place premise and its
limits; do not silently substitute a targeted city-attack model.

An opening could establish an ordinary supply chain, interrupt its delivery in
the illustrative scenario, and promise to explain how a remote detonation can
matter to an intact home. Say it could threaten delivery, not that an empty plate
is a certain global outcome. If using an empty-place-setting image, actually
stage that image; if using bread as the baseline, explain that it is the ordinary
chain being examined. Briefly label the whole scenario a thought experiment.

| Approximate finished time | Explanatory job and visual development |
|---|---|
| 0:00–0:12 | Short title event and a specific ordinary dependency; clear hypothetical status and one unanswered consequence, with useful 2–6-second picture development |
| 0:12–1:05 | Enter the premise immediately: in-place simultaneous rule, different environments, why weapon count is not one giant bomb; simple honest comparative illustration |
| 1:05–2:15 | Light/heat then pressure at one established illustrative place; component damage, obstructed access and persistent consequence |
| 2:15–3:05 | Fallout versus immediate radiation; changing local deposition demonstrated without invented precise safe zones |
| 3:05–4:25 | Same clinic/water service: operating component → loss of input → failed output → harder care; carry supply/access constraints forward |
| 4:25–5:45 | Fire soot differs from fallout; visible atmospheric pathway comparison, conditional persistence and its relevant assumption |
| 5:45–7:00 | Return to the established field/supply chain at a legibly later timescale; sunlight/growing conditions and harvest vulnerability, no instant magical crop death |
| 7:00–8:15 | Food present versus food deliverable; specific port/transport/processing constraint and limited alternatives rather than a list of systems |
| 8:15–9:15 | A bounded illustrative community response changes one established problem without undoing losses; integrate remaining scientific limits where they matter |
| 9:15–10:00 | Answer the title, distinguish planetary survival from human/system harm, explicitly return to reality and revisit the original dependency with changed understanding |

These unequal sequence lengths total ten minutes as a planning allocation;
actual complete delivery and useful picture determine the edit. They are not
measured reference timings or an instruction to pad. The whole-film spine is
prepared once; later sequences reach submission depth while ready work runs.

Worked water beat: begin with the same pump drawing water and a recognizable
open tap. Establish a scenario-justified power interruption; show the pump
stopping and explain the distribution dependency with an accurate cutaway if
needed. Return to the **still-open** tap as flow changes, allowing realistic
pressure/storage delay. Show the clinic's constrained response. If local storage
or gravity maintains flow, preserve that fact rather than forcing an immediate
stop. A person closing the valve would demonstrate a different cause.

Worked smoke beat: distinguish burning material and airborne soot from radioactive
fallout. Use an illustrative layered atmosphere with source-verified process
arrows and sparse labels. Reveal the different removal/persistence pathways in
place, then return to the same farm at the appropriate timescale. Do not show
anonymous smoke columns as if they prove a specific climate result.

## Fast production and a better final check

Keep the [fast production default](video-fast-production-preferences.md). No new
routine per-clip ASR, contact sheets, paid scoring, auditions, approval gates or
every-frame review. Prepare the semantic contract once; use brief checks for
actual dependencies and concrete faults. One final local batch checks:

- Title event, major mechanisms and opening payoff are present and intelligible.
- The actual joined opening has one short hook, timely picture development and no
  accidental phrase replay; keep its bounded local transcript/cut evidence.
- Critical spoken propositions agree with the visible action, cause and timescale.
- Recurring places retain consequential state; the ending does not reset it silently.
- Actual selected shots satisfy the two-second minimum; complete speech/actions,
  native audio timestamps, full-frame 720p and playable export remain intact.
- Essential diagrams are finished and factually legible; available sound is
  sensibly mixed and the final phrase/ending is complete within the review method.

Use actual selected ranges with keep reasons. Retain an entire generated chunk
when useful, not by default. Repair a concrete fault locally when suitable and
authorized, preserving accepted assets; a necessary new generation obeys existing
budget, entitlement and no-replay rules. Do not add retakes merely to reach a
shot-count target. Deeper study occurs when explicitly requested or a concrete
fault warrants it, and its method/limits must be recorded honestly.

## Fresh context and another computer

The canonical route is repository entrypoint → `AGENT_GUIDE.md` →
`docs/production-knowledge-index.json` → named style guide/template/playbook →
this playbook and Frameo workflow. It does not depend on personal Codex memory,
Pages access, cached reference videos or the pilot's media. Use the
[installer/update guide](install-and-update.md) and
`python scripts/check_production_knowledge.py`.

Resolve the receiving user's storage, Downloads and filename restrictions at
runtime; record unavoidable platform-safe filename mapping. Do not copy the
pilot's hardcoded expiry, capacity, SSD paths, private music, receipts or voice
URLs. New films establish original permitted references; continuations explicitly
transfer the selected reference bytes and verify hashes. Verify current account
entitlement and one shared admission owner, especially across computers. The
repository transfers knowledge and supported code, not an unlimited pass,
authenticated session, distributed scheduler or guaranteed creative result.
