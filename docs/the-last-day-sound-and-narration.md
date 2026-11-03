# The Last Day — narration performance and sound mix

Owner refinement, 3 November 2026: match the reference's restrained commentary
and background-score relationship much more closely. The nuclear pilot's music
was too prominent. This is an operative style instruction alongside the
[editorial playbook](the-last-day-editorial-playbook.md),
[human performance](ai-video-human-performance-preferences.md),
[voice selection](ai-video-voice-selection-preferences.md) and
[fast production](video-fast-production-preferences.md). It adds no paid service,
audition/review loop or approval gate.

## Evidence is not a single loudness target

The five complete cached reference mixes measure approximately −14.4 to −16.2
LUFS integrated, with 3–6 LU loudness range. The original pilot measures about
−16.15 LUFS: making the whole film quieter would not fix its music-to-voice
balance. Its separate score actually measures −27.01 LUFS against a native
narration/ambience component at −16.03 LUFS. In aligned active-native windows,
the median difference is only 10.94 LU. Native ambience/effects make this a signal
proxy, not a pure speech-stem measurement. Reference stems are unavailable.

See [audio study](evidence/the-last-day-refinement-20261103/audio-study.md) and
[measurements](evidence/the-last-day-refinement-20261103/audio-measurements.json)
for exact methods and limits. Earlier external model descriptions support a
restrained mature documentary register, clear diction, low instrumental tension
and selective physical effects; their accent, WPM, dB and instrument precision
was not independently established. Do not treat those reports as a voice-cloning
recipe or claim their listening was performed by the current agent.

## Write and direct a connected commentary

Use one original, permitted, consistent offscreen narrator. Prefer a clear mature
low/mid-register documentary voice when selecting a new voice, with calm authority,
conversational intelligibility and restrained emotion. Reuse a suitable settled
voice. Do not impersonate the channel narrator or force a theatrical bass voice,
whisper, exaggerated accent or ominous delivery on every line.

Give each thought group a function and performance direction:

| Function | Writing and performance |
|---|---|
| Immediate hook | One concrete image or contradiction; a direct phrase followed by the question it creates; purposeful urgency without shouting |
| Mechanism | Clear nouns and physical verbs; explain one relation at a time; stress the causal verb and unfamiliar term, then let its result register |
| Reversal | Establish the plausible expectation, turn on one precise word, leave a brief useful beat, then supply the reason; avoid a pause before every sentence |
| Escalation | Connected clauses and greater momentum as consequences accumulate; intensity comes from changed stakes and words, not uniform loudness or faster playback |
| Human aftermath | Specific action/constraint, restrained delivery, room for material sound; no generic solemn warning after every image |
| Payoff/ending | Resolve the question in plain language, revisit the object with changed meaning, finish the last phrase naturally and allow a purposeful landing |

Write variable sentence lengths and thought groups before allocating generator
time. A short consequential sentence can follow a fuller explanation. Keep
technical terms speakable, quantities accurate and emphases sparse. Avoid a
repeated “but this is only the beginning” rhythm, identical rhetorical questions,
endlessly falling dramatic phrases and uniform paragraph resets.

120–145 words per finished minute remains an initial whole-film planning envelope,
not a required per-minute pace. Actual references differ by passage and film.
Timing analysis must separate words per whole elapsed minute, words during speech,
and gaps; these are different quantities. A matching average does not establish
matching cadence. Never speed up the finished voice or stretch pauses to hit a
reference number or fill thirty seconds.

For each ready chunk record exact text, complete phrase windows, delivery intention,
prior/next thought, stable voice guidance and a clean endpoint. Keep technical
explanation connected across source boundaries. The next request resumes the
thought, not a fresh channel introduction. Preserve complete native visible speech
and synchronized actions. When the supported route returns only a native mixed
track, be explicit about that limitation; no assumed voice/effects separation.

## What the complete local timing study changes

Free local full-file faster-whisper base/English analysis gives these recognized
word densities, including gaps and non-narrator opening material where present:

| Film | Approximate elapsed words/minute |
|---|---:|
| Nepal | 128.4 |
| Moon | 129.0 |
| Asteroid | 133.7 |
| Lituya | 134.3 |
| Without humans | 126.5 |
| Nuclear pilot | 133.8 |

The pilot already matches the upper end of these averages. In the consistently
computed Nepal/asteroid/pilot comparison, its median gap-delimited run has seven
words versus 8.5/nine; it has eighteen estimated gaps longer than 1.2 seconds in
ten minutes, versus nine/twelve across the roughly nineteen/twenty-minute
references. The pilot's words inside eligible runs are faster, despite similar
whole-film density. This supports changing the **burst-and-gap pattern**, not
blanket acceleration. The definition uses estimated interword gaps above 0.35s;
these runs are analytical units, not linguistic phrases or exact acoustic silence.

Reference delivery also changes with narrative job: the asteroid opening and
cavity explanation are around149/145 elapsed WPM, versus121 for its historical
payoff and129 for its ending. Nepal's middle is steadier, around128–132, with
an ending near125. These are observed examples, not hard targets for every title.
The Moon/Lituya/without-humans thirty-second bins vary more than the pilot's
narrow126–146WPM bins, even comparing only the interior narrative sections.
Lituya's human crisis is denser than its mechanism, while without-humans gives
its collapse payoff more space and its ending remains fluent. Do not prescribe
“all climaxes fast, all endings slow”; choose the local information/performance job.

Plan a fuller causal thought where the sample chopped it into resets, then a
short sentence at the actual reversal. For example: “The building is still
standing, but its pumps need electricity and its staff need a road they can use.
The damage outside has followed them in.” Match the image to that specific
claim and make its context conditional where required. Allow breath and useful
visual action; do not simply remove every gap or prescribe one sentence length.

Detailed timing methods, passage windows and uncertainty:
[Nepal/asteroid/pilot](evidence/the-last-day-refinement-20261103/narration-a.md),
[Moon/Lituya/without-humans](evidence/the-last-day-refinement-20261103/narration-b.md).
ASR can miss quiet speech, invent words in gaps and misplace boundaries. It does
not measure emotional expression, timbre, accent or perceived naturalness. No
new voice-cloning or paid review route follows from these measurements.

## Much quieter score under speech

The default is **voice first, music felt behind it**. Start a steady bed roughly
20–24 LU below typical narration-active short-term level. With native narration
near −16 LUFS, a score around −36 to −40 LUFS is a useful starting range. These
are owner-responsive production choices, **not measured reference stem ratios**.
Measure simultaneous passages and cue peaks when a concrete balance issue occurs;
two unrelated integrated track values cannot guarantee intelligibility.

The pilot correction reduces its existing score by **9 dB**, from approximately
−27.01 to −36.01 LUFS, retaining native narration input at unity gain and the exact
sample timeline. The aligned median native/music difference becomes approximately
19.94 LU. Do not normalize that score back up afterward. Preserve headroom; the
near-zero decoded reference peaks are not a target to copy.

Keep the score low through technical clauses and quiet endings. Use selective
silence instead of continuous musical pressure. Allow a modest rise only in a
planned genuinely speech-free event or transition, then settle before the next
important word. Do not swell into every breath, use a cinematic hit at every cut,
or keep prominent drums/melody under a scientific explanation.

Use prepared phrase/cue gain automation first for an isolated competition. Where
appropriate and supported, an additional 3–6 dB of gentle ducking can help; start
around 50–100 ms attack and 500–1000 ms release, inspect actual reduction and avoid
pumping. These settings are starting choices, not verified channel settings.
Use a real narration stem/envelope when available. A native track containing
effects is an imperfect key; use known phrase windows rather than pretending
it is isolated speech. Do not add a paid stem-separation dependency.

## Sound tells the same physical story as the picture

Keep a small palette of contextual ambience and material effects: water movement,
metal strain, glass/debris, footsteps, mechanisms and room tone as the scene
requires. An effect must have an intelligible source, distance and time. Do not
put a close explosion on a remote flash before its delayed sound arrives, or
present vacuum sound as literal recorded physics. Illustrative non-diegetic
sound is a design choice and must not confuse the explanation.

Let an established ambience bridge compatible adjacent views; change it when
location or time changes. Hold important quiet material detail against a reduced
score. Do not layer an extra boom on a native effect merely because a cut occurs.
Avoid redundant bass rumble beneath every sentence. Dialogue intelligibility and
causal clarity outrank spectacle.

Plan a cue map tied to actual story turns: baseline/curiosity, mechanism,
consequence, reversal, aftermath and payoff where relevant. Record available
authorized asset/hash, purpose, in/out, gain, transition and intentional silence.
Reuse a motif meaningfully; do not loop one cue mechanically across most of the
film or calculate the ending cue as a fixed fraction of runtime. Crossfades alone
do not make inappropriate musical developments fit.

Frameo requests should specify whether native music is unwanted so a coherent
later score can be controlled. Keep intended native narration and useful activity
sound. Use only authorized available music; external generation follows the
existing [music policy](ai-music-preferences.md). Missing score assets do not stop
an otherwise authorized film or grant new spending: continue with permitted
native sound and an intentional music-free treatment.

## Assemble, check and preserve the result

Decode native AAC with its presentation timestamps before sample-based editing;
preserve exact complete phrases and causal audio-picture alignment. Do not use
independent nominal chunk lengths to accumulate padding drift. Mix without
unintended automatic averaging or later normalization that reverses the chosen
balance. Treat integrated loudness, short-window balance, loudness range and
true peak as separate checks. Around −16 LUFS with adequate headroom is a useful
delivery starting point; do not force the loudest reference's value.

Inspect the actual encoded result for a concrete fault, not merely the pre-encode
WAV. An audio-only correction can stream-copy the picture, preserve the original
export and publish a clearly identified new version under
[delivery preferences](video-delivery-preferences.md). Record changed music gain,
native gain, sample count, picture hash, encoded loudness/peak and review limits.

Normal production retains one brief local final check and targeted repairs for
identified defects. The owner's explicit reference re-study permits the current
whole-film measurements and timing analysis; it does not turn those into a routine
per-clip review requirement. Describe unavailable direct listening, subjective
voice matching and untested artistic results honestly.
