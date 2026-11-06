# Queen Elizabeth I Style — adapt the whole story before media

Owner correction, 5 November 2026. This is the first creative production step for
every new **Queen Elizabeth I Style** episode: supplied story, title-led original
or authorized Frameo unlimited production. Read with the
[style preferences](queen-elizabeth-i-style-preferences.md),
[production playbook](queen-elizabeth-i-style-production-playbook.md),
[human performance](ai-video-human-performance-preferences.md) and
[fast production](video-fast-production-preferences.md).

Review and strengthen the whole story, then write a coherent revised screenplay
through its ending **before any new image, video, speech or music generation**.
This supersedes starting media from only an ending-aware spine and one ready
sequence. It adds no owner approval, paid review service or quality score. After
the foundation is coherent, detailed sequence preparation, independent generation
and assembly overlap under actual shared capacity.

## Adapt the source without losing its identity

Treat a supplied story as an adaptable outline, not a literal shot list. Read it
through the actual ending and aftermath. For a title-only brief, develop the
complete story first and review that story through its ending. Do not describe
an unread, absent or unwritten ending as reviewed.

Preserve the central premise and viewpoint, selected characters and motivations,
emotional core, curiosity and revelation order, hooks, meaningful setups/payoffs,
important relationships, outcome and ending. Preserve explicit owner constraints
and the factual record where the episode presents history. Improve the expression:
add needed connective action, intelligible explanation, useful listener responses,
supporting agency and physical results. Remove boring holds, repeated exposition,
redundant incidents and jokes without a situation. Reorder or combine passages
when that strengthens causality without losing the protected obligations.
Adaptation does not authorize replacing the premise with another familiar plot,
silently recasting the host, fabricating history or exceeding the actual budget.

Keep the primary historical character-vlog grammar. The insider host reveals a
routine, place or political mechanism through concrete work, social meaning and
earned dry commentary. A supporting person can change the scene through useful
work, information, permission, disagreement or a response. Do not import AI Movie
survival escalation, spectacle, a twist quota or Chloe's modern visitor persona
simply because stronger writing is needed. Use a visitor-led format only when
the brief calls for it, with that choice recorded.

## Write the performed episode, not a container plan

The revised screenplay includes every sequence, its purpose, meaningful actions
and interactions, relevant dialogue or offscreen explanation, emotional movement,
transitions and complete ending. A logline with an ending, a list of clip IDs or
four equal thirty-second requests is insufficient. Exact lenses, all shot prompts,
new reference images and provider payloads may be prepared incrementally after
the complete screenplay is coherent.

Give each sequence a reason to begin, an intelligible action or encounter, a
change and a reason to move on. Resistance can be practical work, limited access,
embarrassment, a boast contradicted, responsibility or a political disagreement;
it need not become extreme danger. A quiet exchange should alter attachment,
expectation, understanding or the next choice. Tie concrete period information
to something the audience can see or understand in the situation. Verify factual
assertions and identify invented incidents as dramatized fiction.

For important transitions, include the needed cause, means, result and response.
If an attendant is sent for a letter, show the useful delivery or establish a
clear offscreen return before the letter appears in the host's hand. If clothing
or a practical object changes state, make the useful operation and result readable.
A political message should lead intelligibly to a decision and consequential
action, not merely another speech in a different room. Let an earned human
response follow the result before a callback closes it.

Full-film refinement,6November2026: make the opening promise understandable to a
viewer without prior knowledge. Place one concrete consequence near it; explain
an unfamiliar political/social mechanism before asking a clever reversal to pay
it off. Establish who needs what, the observable attempt or permission and what
changes. Do not count proper names or implication as an explained procedure.
For reports or earlier-event inserts, first establish the present-time speakers,
who attended and how they know; return to the listener when the meaning changes.
Separate visible speakers from offscreen commentary and let a simple time/action
cue carry major ellipses. Preserve the source's viewpoint and factual boundaries.
Give a recurring task a readable changed state/result and a reason to end; assign
changing intentions rather than a smile after every sentence. Put these choices
in the existing screenplay and sequence cards, not another approval artifact.

Do not show every footstep, fastening or journey. An instruction, established
destination or visible time cue can justify omitting uneventful work. Record the
cue and why the omitted action is inferable and expendable. A missing cause,
changed room, restored departed object or accidental early reveal is not an
elegant ellipsis. Preserve camera ownership, period geography, native speech-picture
pairing and current physical state at the actual cut.

## Give action and emotion necessary screen time

Approximate duration is a flexible creative target. The owner explicitly permits
roughly **60–70% more time when the story benefits**: an approximately ten-minute
episode may become sixteen or seventeen minutes when its actions, interactions,
curiosity and emotional ending need that time. A stronger shorter version is
valid too. This is permission, not a default expansion, minimum length or reason
to pad. Explicit hard duration requirements, actual budget, provider authorization
and pass limits remain binding.

Estimate time from behavior: orient the viewer, finish the thought or operation,
show the consequential reaction, and leave motivated anticipation or aftermath.
Dialogue word count and source-outline timestamps alone do not measure performed
time. First reclaim repetition and empty holds; expand only to serve the episode.
Do not cut a required setup, bridge, meaningful reply or ending for nominal length.
If a hard constraint requires compression, rewrite remaining unsubmitted material
coherently within it.

Thirty-second generation is an acquisition unit, not a dramatic scene boundary.
Several requests may serve one sequence; one request may contain several useful
beats. Ordinary actual shots remain at least two seconds, but that floor does not
make a rushed explanation, operation or emotional exchange readable. Never create
duration by stretching native speech, looping, freezing or keeping an empty tail.

## Use the existing narrative evidence contract

Put the review in `script.metadata.narrative_foundation`, not a new workflow or
approval form. Record:

- `status: "reviewed"` and truthful `source_read_through_ending`;
- `protected_core`: story identity, emotion, curiosity and important obligations;
- `adaptation_decisions`: concrete additions, removals, combinations or reordering
  with reasons, or why a reviewed passage already works;
- `screenplay_path` and `screenplay_sha256` for the actual complete revised file;
- ordered `sequences`, each with `id`, `purpose`, `action_and_transition`,
  `emotional_turn`, useful `performance_seconds` and named `required_beats`
  containing IDs and descriptions;
- `ending_sequence_id` matching the final ending/aftermath sequence;
- `unresolved_gaps: []` only after known structural problems are resolved.

A ready flag or hash alone does not establish thoughtful review. The screenplay
must exist, cover the whole episode and support the claims. A material change
requires a refreshed review/hash and affected sequence/coverage records before
new dependent work. Keep accepted assets and exact receipts; revise affected
unsubmitted material or make a justified targeted pickup within authorization.

Initialize new projects through `lib.checkpoint.init_project` with
`style_playbook="queen-elizabeth-i"`. New projects use the existing versioned
narrative contract. Script completion and assets admission validate the foundation
through `lib.narrative_continuity.validate_foundation`; direct media dispatchers
must run the check before admission too. Read-only provider discovery, budget and
capacity checks, and inspection of accepted assets may proceed while writing;
they do not generate new media.

Legacy accepted projects are not automatically rewritten or replayed. Before new
generation in a legacy project, deliberately adopt the contract and preserve
accepted or uncertain work. This correction does not request another version of
an already delivered sample or resume a stopped film.

## Carry required meaning into returned footage and editing

Map each required causal/emotional beat to what was actually observed inside a
selected source range. Use `edit_decisions.metadata.narrative_coverage`: current
screenplay hash, current cut-list digest, observations tied to `beat_id` and
`cut_id`, source start/end, `mode: "visible_action"` or `"legible_ellipsis"`,
and a truthful description of the observed action or cue/result. Unknown or
missing critical coverage remains an unresolved gap. Before/after clips, successful
jobs, transcripts and technical decode do not prove the bridge or response occurred.

The existing validator checks this coverage before edit completion or compose/
publish starts. These are integrity checks, not machine certification of history,
visual meaning, engagement, continuity or lip sync. Inspect key action and actual
continuation dependencies while selecting useful ranges; reuse the observations.
Do not add automatic per-clip ASR, paid scoring, contact sheets or repeated full-film
audits. Resolve concrete gaps through better selection, motivated editing, revised
unsubmitted action or affordable targeted pickup. Keep independent ready work moving.

Assemble performed sequences, not a sorted list of successful files. Protect
native words, physical results, necessary listener responses and the ending's
meaning. Use existing brief final moving-output and cached technical checks for
essential causes/payoffs, flow, identity/state, picture/native sound finish, shot
duration and delivery. More review follows a concrete fault or explicit request.
Describe actual viewing/listening; background playback, sampled frames and ASR
do not constitute full audiovisual review.

This guide and linked style/template/playbook live in the portable repository.
No personal Codex memory, private Pages or original Mac/SSD path is required.
Use the receiving computer's working storage, Downloads directory, actual capacity,
entitlement and budget. The contract supports reliable execution; future creative
quality and speed still need demonstration in the footage.
