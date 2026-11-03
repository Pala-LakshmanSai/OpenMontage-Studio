# The Last Day — timed narration comparison A

3 November 2026. Free local timing analysis of the full Nepal and ocean-asteroid references, compared with the completed nuclear sample. This is a response to the owner's explicit request for closer storytelling, narrator pacing and sound treatment. It does not claim audible assessment of voice quality.

## Route and evidence

Read `tools/analysis/transcriber.py`, the local video-understanding skill and the registry's linked speech-to-text skill. The linked speech-to-text skill describes ElevenLabs, but the actual selected **registry Transcriber** implementation runs **faster-whisper locally**. No ElevenLabs service was used. Settings: cached **base**, English language, CPU/int8, word timestamps enabled, VAD enabled, diarization disabled. The schema calls this `model_size=base, language=en`, not a separately downloaded `base.en` checkpoint. Offline environment flags were set.

Each complete reference was transcribed **once**. Nepal completed in 182.59 seconds and asteroid in 178.50 seconds, concurrently. Existing full timed reference results were not available; previously cached reference ASR covered only the first two minutes. The sample's existing result was reused without another pass.

Raw copyrighted text remains in a **local research cache (not a production dependency)**. Portable evidence IDs are `asr-vfIaNeGVaVo`, `asr-hxlGCMo6ihI` and `asr-our_sample`; the aggregate JSON retains their source-result hashes.

The durable [aggregate JSON](narration-a.json) contains editorial-window measurements, complete thirty-second bins, pause locations and operational definitions, without full transcripts or excerpts. There were no paid calls, generation calls, audible playback or canonical-style edits.

## Main finding: average speed does not explain the mismatch

The sample's overall recognized word density is essentially the same as the asteroid reference. Its difference is **shorter speech runs, faster speech within those runs, and more frequent breaks**. “Make the narrator faster” is therefore not a supported general repair.

| ASR timing metric | Nepal | Asteroid | Nuclear sample |
|---|---:|---:|---:|
| Recognized lexical word entries | 2,480 | 2,680 | 1,340 |
| Whole-file words/minute, including gaps | 128.4 | 133.7 | 133.8 |
| Thirty-second-bin median words/minute | 132 | 136 | 132 |
| Thirty-second-bin 10th–90th percentile | 116–140.6 | 116–148 | 128–144.2 |
| Word-alignment occupancy proxy | 84.2% | 82.9% | 77.0% |
| Median words per gap-delimited run | 8.5 | 9 | 7 |
| 90th-percentile words per run | 21 | 26.4 | 14 |
| Median eligible run-rate proxy | 152.5 WPM | 161.3 WPM | 175.2 WPM |
| Gaps longer than 0.35 seconds | 235 | 216 | 172 |
| Gaps longer than 1.2 seconds | 9 | 12 | 18 |
| Machine-punctuated sentence-terminal gaps | 141 | 158 | 112 |

Nepal includes a pre-narration attention opener with other sound/possible speech. Starting its main narration region at26.533 seconds yields **2,455 words, 130.1 elapsed WPM and six gaps over1.2 seconds**, rather than assigning the opening's recognized words to the narrator. Occasional other voices later remain unseparated.

A “run” here means adjacent recognized words separated by no gap above0.35 seconds. It is an analytical unit, not a linguist's phrase. The eligible run-rate proxy uses runs with at least four words and one second of span. It excludes larger breaks and **must not become a direction to deliver a whole film at175 WPM**. Occupancy is the union of estimated word-alignment intervals, not a measured voiced/unvoiced ratio.

The sample has about17.2 gaps over0.35 seconds per minute, versus12.2 for Nepal and10.8 for asteroid. Its machine punctuation also gives more sentence endings per hundred words: approximately8.4 versus5.7/5.9. Together these support investigating a more segmented script/performance. They do not prove unnaturalness or a particular pitch contour.

## Timing changes across narrative roles

These windows follow the earlier visual/transcript study. They are analyst-defined editorial ranges, not exact creator chapter boundaries.

| Reference and role | Time window | Elapsed WPM | Occupancy proxy | Gaps >1.2s |
|---|---|---:|---:|---:|
| Nepal narrated hook | 0:26.533–1:26.920 | 127.2 | 82.2% | 0 |
| Nepal geography/initial mechanism | 1:26.920–7:28 | 127.6 | 86.7% | 1 |
| Nepal secondary-hazard climax | 7:28–9:01 | 132.3 | 83.4% | 1 |
| Nepal human/logistical aftermath | 9:01–15:20 | 132.3 | 85.0% | 4 |
| Nepal future risk/recovery | 15:20–18:18 | 132.1 | 88.1% | 0 |
| Nepal ending callback | 18:18–19:18.633 | 124.7 | 77.9% | 0 |
| Asteroid hook | 0:00–1:18.567 | 148.9 | 84.7% | 0 |
| Asteroid scale/impact setup | 1:18.567–5:04 | 136.3 | 82.6% | 2 |
| Asteroid cavity/rebound climax | 5:04–6:20 | 144.5 | 91.0% | 0 |
| Asteroid wave correction/coast | 6:20–10:59 | 132.3 | 80.5% | 3 |
| Asteroid atmosphere | 10:59–12:43 | 137.3 | 85.2% | 1 |
| Asteroid network cascade | 12:43–15:08 | 127.9 | 82.7% | 2 |
| Asteroid historical payoff | 15:08–17:29 | 121.3 | 80.9% | 2 |
| Asteroid detection/agency | 17:29–19:10 | 137.2 | 87.9% | 1 |
| Asteroid ending recap | 19:10–20:02.200 | 128.7 | 73.8% | 0 |

The asteroid film does not use one universal solemn speed. Its rhetorical opening and physical cavity explanation are relatively dense; its historical payoff and network consequences are less dense. Nepal is more consistent through its middle and eases into its ending. This supports changing delivery with narrative function, rather than copying a single average or imposing one pause after each sentence.

For comparison, the sample opening measures131.8 WPM with only67.8% word-alignment occupancy and two gaps over1.2 seconds. Its atmospheric passage at5:00.417–6:30.542 measures127.8 WPM,70.9% occupancy and five gaps over1.2 seconds. Its ending remains133.8 WPM and81.2% occupancy. The sample therefore spends more time in early/middle breaks while its final landing is not correspondingly less dense. These are directions for a focused performance change, not evidence that every phrase is poor.

## Long pauses are useful when the picture earns them

The references do not simply avoid pauses. Asteroid has estimated gaps of **8.93 seconds around8:28.82–8:37.75** and **10.88 seconds around15:28.77–15:39.65**. The earlier visual study places these near a wave-to-coast transition and a historical impact passage. The pause sits beside major imagery rather than a routine topic label. Alignment/VAD estimates do not independently prove complete acoustic silence.

Sample timing includes:

- 0:07.92–0:10.08:2.16 seconds.
- 0:17.82–0:21.72:3.90 seconds.
- 2:19.52–2:22.66:3.14 seconds.
- 5:29.86–5:33.96:4.10 seconds, straddling a generation-chunk boundary.
- 6:06.52–6:09.63:3.11 seconds.
- 6:13.89–6:16.52:2.63 seconds.

These are candidates for checking the relationship between words and action. Their existence alone is not a fault. The useful question is whether each interval shows a consequential change, a comprehensible reaction or an earned landing. Do not cut every gap or time-stretch the finished narration. A generative chunk beginning is not itself a dramatic reason to pause.

## Transcription uncertainty

Nepal has96 recognized word entries below0.5 model probability; asteroid73; sample30. These are uncertainty indicators, **not calibrated word-error rates**. Low confidence occurs around names, complex geography, music and mixed voices. The English-forced Nepal opening has recognized words before the main documentary narration, which must not be treated as a clean narrator sample.

Word boundaries, punctuation and zeros/overlaps can distort run lengths and pause estimates. Proper names and numerical readings may differ from the saved untimed transcript without proving which one is right. ASR can also fill a real pause with a hallucinated word or miss quiet speech, shortening or lengthening measured gaps. No new audible verification or forced-alignment pass was performed. Use the broad consistent comparisons; do not hard-code millisecond cadence from these files.

## Actionable refinement for the parent style update

1. **Preserve connected thought groups.** Combine adjacent short statements when they form one causal explanation; use a short emphatic sentence where the idea turns. Do not let every sentence reset performance. The sample's shorter runs and higher sentence-ending density support this priority.
2. **Keep average density near the references without forcing identical timing.** Roughly130–140 elapsed WPM is already achieved by the sample. The stronger difference is the shape: intelligible longer runs, fewer arbitrary gaps, and changes between inquiry, explanation, consequence and ending. Faster bursts plus long pauses are not equivalent to flowing speech at the same average.
3. **Choose a role-specific contour.** An asteroid-like urgent curiosity opening can be denser than its reflective ending; a Nepal-like investigative account may retain steadier middle density. These are observed examples, not a requirement that every topic hit149WPM in its hook.
4. **Plan sound and picture around meaningful pauses.** Allow a useful physical transformation or consequence to carry a break. Avoid automatic lead-in/tail silence at every thirty-second generator boundary. Preserve complete native utterances and timing.
5. **Treat the owner's quieter-score request as an explicit mix preference.** Keep background score subordinate to narration and contextual effects, especially during explanation; reserve restrained rises for actual word-free action. This ASR study cannot determine the current score/voice loudness difference, prescribe a verified dB offset, or establish perceived masking. Do not fabricate those measurements. No separate paid music authorization follows from this analysis.
6. **Match the storytelling and delivery behavior with an original consistent narrator.** These metrics do not establish timbre, resonance, accent, prosodic intent or exact identity matching. A copied word rate is not the reference performance.

Apply these during normal script and performance preparation. This explicit whole-reference timing study is reusable training evidence, not a new routine per-video ASR audit or paid review stage.
