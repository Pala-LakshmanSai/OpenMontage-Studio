# Voiceover-to-footage alignment

Use for a supplied narration that must be illustrated with real moving footage.
This specializes the hybrid pipeline; it does not replace its checkpoints.
Set `brief.metadata.anchor_medium = "broll_footage"` and
`brief.metadata.footage_alignment_required = true`.

## Acceptance order

1. Preserve the requested narration, historical truth and visual restrictions.
2. Match each spoken clause to an observed subject **and action**.
3. Avoid repeated excerpts, camera takes and recurring visual patterns.
4. Optimize production time within those constraints.

Urgency never authorizes generic filler. A valid container, moving pixels,
many sources, source branding or hundreds of sampled frames do not prove relevance.

## Plan from the narration, not the downloaded inventory

Transcribe once with word timestamps. Read the complete narration. Split it into
short meaning units, preserving each unit's named entity, action, object,
location/date and practical consequence. Sections organize research; they do not
decide shots. Put a cut near the phrase that changes the visual subject rather
than blindly rotating a clip every three seconds. Respect the user's cut limit.

Preserve the transcriber's actual word timings in `script.metadata.narration_words`
as `{text, start_seconds, end_seconds}` entries. Never invent or uniformly spread
word timings. Each shot's `narration_quote` must contain exactly the words
overlapping its timeline interval, including words straddling a cut; use `[pause]`
only when no word overlaps. A long ASR segment or chapter summary is not the
spoken text of every shot inside it. The checkpoint validates against these words.

For each unit, write a concrete visible target and targeted source queries before
selection. For example:

| Spoken subject | Strong visible target | Reject |
|---|---|---|
| Echo sharing an internet connection | Actual Echo/Ring use, relevant controls or household device connection | Coffee, grocery aisles, arbitrary phone scrolling |
| Deleting stored Alexa recordings | Hands using the relevant Alexa controls; a specific privacy action with an honest contextual relation | Generic keyboard work or a store tour |
| Checking product reviews | A buyer comparing the discussed product and checking its reviews | Prepared-food counters, warehouse belts |
| Returning an item without packaging | Customer handing the unpackaged item to a returns worker | A delivery van merely because both involve parcels |

An abstract passage still needs its concrete mechanism or consequence. Do not
reduce every financial point to cash counting or every technology point to servers.
Never pretend a contextual example depicts the named historical event/person.

## Acquire and index efficiently

- Search exact entities/actions first, using sources allowed by the user.
- Preview small proxies/contact sheets before large downloads. Prefer a small
  number of rich, relevant sources over dozens of loosely related files.
- Divide sources at real camera cuts. Record original source identity, take ID,
  usable source interval, observed subject/action, date and restrictions.
- Inspect the exact interval's start, middle and end; reject embedded ads,
  documents, titles, unsuitable framing and unrelated internal cuts.
- Index a source once. Reuse its verified observations, cached frames and local
  media across projects. Reconsider its relationship to each new narration.
- Search/download/frame extraction may overlap in bounded batches when tools
  permit. Keep one transcript, one source index and one final shot map.
- Audit coverage before rendering. Search only the missing subjects/actions.
  If relevant coverage remains unavailable, record that shortage honestly; do
  not silently fill it from a generic or exhausted pool.
- Cache accepted cut renders. After an edit change, re-review and re-render only
  changed cuts, then repeat the appropriate assembled-output checks.

Do not copy another video's beat-to-source mapping, titles, brief or review result.
Do not use random selection, source rotation, broad topic tags, titles or keyword
scores as final editorial approval. They may retrieve candidates, never accept them.
Do not treat the hybrid EP's nominal 12-minute budget as permission to weaken quality.

## Repetition: zero by default

Default `brief.metadata.footage_reuse_policy.max_reused_fraction = 0`.
If the user permits very rare repetition, an explicit policy may allow at most
`0.01` (1% of running time), with `min_gap_seconds >= 360`. No take may appear
more than twice. Measure the gap from the prior use's end to the next use's start.

Keep the same `source_scene_id` for the original continuous camera take, even
after a crop, speed change, file copy or selection of different seconds. A new
excerpt is not automatically a fresh visual. Overlapping source frames are also
reuse, even if someone changes the scene ID.

Review rolling one-minute sequences and the whole film for recurring activities,
angles and settings. Distinct grocery aisles or repeated Echo-on-desk views can
still feel repetitive. Use truthful `visual_motif` keys describing the visible
subject/action, not artificial labels such as `shot-17`. Three consecutive cuts
with the same motif cannot pass. Varied framing cannot rescue an irrelevant shot.

## Record observations before accepting the edit

Populate `edit_decisions.footage_alignment` using its schema. Each cut needs:

- its actual narration quote, from the matching script interval;
- observed `visible_subject`, `visible_action` and a specific `relation`;
- `match`: `direct`, `specific_context`, `generic`, `mismatch` or `unverified`;
- original `source_scene_id` and honest `visual_motif`;
- three project-local frame samples at the selected source interval's
  start/middle/end, with source timestamps and SHA256 hashes.

Only `direct` and `specific_context` can pass. `specific_context` must explain a
concrete action/consequence that supports this clause, without implying false
identity, place or chronology. "Same topic", "shopping", "Amazon" and "phone"
are not explanations. Inspect frames with the narration alongside them; do not
generate passing observations from search metadata or uninspected captions.

After inspection, seal the reviewed bindings:

```python
from lib.footage_alignment import alignment_digest, validate_footage_alignment
review = edit_decisions["footage_alignment"]
review["cuts_sha256"] = alignment_digest(edit_decisions["cuts"])
review["script_sha256"] = alignment_digest(script)
validate_footage_alignment(project_dir, brief, script, edit_decisions, asset_manifest)
```

The checkpoint writer enforces this before accepting an edit and before
compose/publish, including direct FFmpeg runs. Changed cuts or narration
invalidate the review. Technical validation checks coverage, current evidence,
reuse and obvious motif runs; it **does not perform vision or certify the
truth of an agent's descriptions**. Do not report a numerical semantic accuracy
score without an independent measured evaluation.

Before delivery, inspect every selected shot against the words it accompanies,
with especially close attention to the opening, weak contextual matches and
repetition. Record unresolved issues in `pattern_issues`; a nonempty list blocks
acceptance. Keep editorial acceptance separate from decode/audio/browser proof.
