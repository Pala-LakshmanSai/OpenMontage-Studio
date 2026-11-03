# Narration timing study B: variation rather than a faster average

3 November 2026. Explicitly requested free local analysis of three full references and comparison with the existing full timed transcript of the approximately ten-minute nuclear sample. This is timing evidence, not an audible voice or mix review.

## Method and evidence boundary

The registry transcriber ran local faster-whisper **base**, English, CPU int8, word timestamps and VAD enabled. Network access for model retrieval was disabled; the already available model was used. Moon, Lituya and without-humans ran sequentially, successfully, without a paid call. The sample transcript was reused. Raw copyrighted transcripts remain only in temporary local research caches; this report and its JSON publish aggregate measurements, public source IDs and timing landmarks, not transcript text.

Words per minute (WPM) here means recognized lexical tokens divided by the entire elapsed window, including pauses. Tokens are assigned by their timestamp midpoint. Thirty-second variability uses complete nonoverlapping windows; a partial final window is excluded from that statistic. **Gap share** is time between adjacent recognized words when the gap is at least 0.3 seconds, clipped to the measurement window. It excludes the leading interval before the first recognized word and trailing interval after the last. Music or effects can continue through any such gap: this is not measured acoustic silence. Word-span coverage is the union of ASR word intervals, also only a proxy.

Narrative windows are selected using the earlier visual/text study, with opening landmarks refined from the new timed segments. They are not identically sized experimental conditions. Word boundaries and counts are approximate. No audible playback, independent alignment pass, speaker matching, source separation or generation was performed.

## Whole-film comparison

| Film | ASR duration | Word tokens | Overall WPM | Full 30s-bin WPM range | Rate variation (CV) | Gap share |
|---|---:|---:|---:|---:|---:|---:|
| [Moon collision](https://www.youtube.com/watch?v=eGfbwdXL3wg) | 1256.29s | 2,701 | 129.0 | 82–152 | 10.3% | 21.8% |
| [Lituya Bay](https://www.youtube.com/watch?v=nhaTh5gGXiM) | 751.49s | 1,682 | 134.3 | 106–172 | 10.8% | 18.3% |
| [Earth without humans](https://www.youtube.com/watch?v=vtUUjqQGk1o) | 1158.69s | 2,443 | 126.5 | 84–156 | 11.6% | 19.3% |
| Our nuclear sample | 600.85s | 1,340 | 133.8 | 126–146 | 4.6% | 22.3% |

**The sample is not slower on average than these references.** Its 133.8 WPM is close to Lituya’s 134.3 and above Moon’s 129.0 and without-humans’ 126.5. A blanket speed increase is therefore not supported. The stronger difference is regularity: our twenty blocks stay between 126 and 146 WPM, whereas the references have substantially broader passage-to-passage variation. CV is standard deviation divided by mean, not a quality score.

This persists when excluding the first and final ninety seconds: inner-body CV is 9.1% for Moon, 11.1% for Lituya and 9.8% for without-humans, against 5.1% for our sample. The difference is not explained solely by the references’ opening teasers. It supports varying sentence load and pause placement by scene role. It does **not** prove that the sample voice is emotionally flat or that higher variability causes better retention.

## Hooks: refine earlier visual-only timing assumptions

- **Moon:** the question sequence ends around 87.97s in ASR; a transition segment starts at 88.75s. The 0–90s opening averages 112.7 WPM, with 31.0% gap share. One detected gap runs 7.56–14.13s after its brief alarm-style introduction. The gap need not be silent. This does not authorize reproducing misleading news framing.
- **Lituya:** the opening promise ends around 85.55s; the explanation reset starts at 86.35s. The 0–86.35s opening averages 139.7 WPM with 17.6% gap share. It uses a denser human predicament than Moon, rather than matching Moon’s pause pattern.
- **Without-humans:** first recognized narration begins at 12.27s, following the sampled collapse teaser. Its promise finishes around 90.87s, followed by the first day marker at 91.71s. The whole 0–91.71s opening averages 121.0 WPM; that includes the 12.27s unrecognized lead. Earlier approximately78s visual-reset estimates should not be retained as the full narrated-hook duration.
- **Our sample:** 0–30s averages 132.0 WPM with 30.3% gap share; its first90s includes two additional premise/inventory blocks. Comparing only our thirty-second hook to a ninety-second reference opening would mix different narrative functions. The JSON includes identical first30s/first90s windows for transparent comparison.

These approximately86–92s narrative-opening landmarks include setup, questions and transitions. They are evidence for these films, not a rule to lengthen every future hook. An immediate meaningful grab and the longer narrative promise are separate design decisions.

## Mechanism, crisis and ending windows

| Film / role | Window (seconds) | WPM | Gap share ≥0.3s | Word-span coverage |
|---|---:|---:|---:|---:|
| Moon collision: rules and acceleration | 90.00–200.00 | 125.5 | 26.2% | 73.2% |
| Moon collision: tidal disruption | 394.00–489.00 | 122.5 | 26.6% | 72.7% |
| Moon collision: close approach / disruption | 721.00–840.00 | 134.6 | 20.2% | 78.7% |
| Moon collision: reality check / ending | 1142.00–1256.29 | 131.2 | 19.9% | 77.7% |
| Lituya Bay: landslide / water mechanism | 264.00–462.00 | 126.7 | 20.2% | 79.7% |
| Lituya Bay: human decision / wave | 480.00–605.00 | 150.7 | 20.3% | 79.5% |
| Lituya Bay: wider aftermath / ending | 660.00–751.49 | 124.6 | 17.4% | 81.5% |
| Earth without humans: roof / roots / corrosion | 278.00–470.00 | 126.9 | 20.7% | 78.8% |
| Earth without humans: accumulated collapse payoff | 552.00–690.00 | 115.7 | 21.3% | 78.2% |
| Earth without humans: permanence callback / ending | 1048.15–1158.69 | 133.5 | 15.8% | 76.7% |
| Our nuclear sample: water dependency | 240.00–270.00 | 146.0 | 18.7% | 81.3% |
| Our nuclear sample: soot / altitude / climate | 300.00–390.00 | 128.7 | 28.8% | 70.9% |
| Our nuclear sample: food / ocean consequences | 390.00–480.00 | 129.3 | 23.4% | 76.1% |
| Our nuclear sample: reality check / ending | 540.00–600.85 | 132.1 | 15.7% | 82.7% |

Lituya’s decision/wave passage is about24 WPM denser than its mechanism passage, despite similar gap share. Without-humans does the reverse around accumulated collapse: its selected payoff passage is about11 WPM less dense than its material-mechanism passage. Moon becomes denser at close approach than during its opening and orbital explanation. Endings are not uniformly slow: without-humans’ selected reflective ending is denser than its collapse sequence. Thus **make the rate serve the local dramatic job; do not prescribe “all climaxes fast, all endings slow.”** These differences also reflect vocabulary and sentence length; ASR cannot isolate acting choices from writing choices.

## Pauses: quantity alone is not the missing ingredient

Our total gap share is22.3%, compared with21.8% for Moon,18.3% for Lituya and19.3% for without-humans. Our sample already has substantial space between recognized words. Adding indiscriminate pauses could make it more padded. The question is what a pause lets the viewer notice, predict or understand.

| Film | Gaps ≥1s | Gaps ≥2s | Median gap among gaps ≥0.3s | 90th percentile |
|---|---:|---:|---:|---:|
| Moon collision | 42 | 15 | 0.64s | 1.02s |
| Lituya Bay | 12 | 0 | 0.66s | 0.94s |
| Earth without humans | 39 | 9 | 0.66s | 1.10s |
| Our nuclear sample | 28 | 6 | 0.56s | 1.18s |

Counts cover films of unequal length and should not be compared as raw quotas. Lituya has no measured interword gap reaching two seconds, yet varies its narrative rate substantially. Long pauses are not a universal reference signature. Without-humans also has a12.27s unrecognized lead and8.10s unrecognized tail; these lie outside the interword-gap counts. Do not call either interval silence without acoustic evidence.

Useful exact ASR candidates for relating pause placement to existing visuals: Moon415.57–422.55s (6.98s); Lituya357.09–358.65s (1.56s); without-humans422.41–426.22s (3.81s). Our longest detected gap is329.86–333.96s (4.10s), crossing a30-second production-package boundary, and another is17.82–21.72s (3.90s). These are evidence pointers, not automatically intentional pauses or faults; missed words can lengthen them.

## Portable planning implications

1. **Keep a natural average, vary local intention.** The measured references average roughly126–134 WPM, but their local passages vary. This is a useful evidence range, not a mandatory target, a voice identity specification or permission to time-stretch audio. Plan a curious hook, lucid mechanism, consequential crisis and earned final thought with different sentence shapes and emphasis.
2. **Stop making every generation package the same rhetorical size.** Our sample’s narrow thirty-second word-count band is consistent with its twenty equal explanatory blocks. A causal sequence can span several jobs, and a job can include a shorter spoken idea followed by a useful visual result. Keep native speech complete and final runtime honest; do not fill unused capacity with slow delivery or redundant prose.
3. **Assign a purpose to space.** Pause after the viewer receives the missing causal link, before a consequential reveal, or while a visible action completes. Reduce generic repeated caveats and reset phrases when they do not advance a new branch; preserve all necessary factual boundaries. Do not insert blank time solely to imitate a gap count.
4. **Use the contrasting references, not one average template.** A human decision can tighten; a large-scale consequence may need room. A reflective ending can remain conversational and fluent. Choose by what the scene asks the viewer to process, then maintain one original narrator identity. This study does not authorize cloning or establish a precise reference accent/timbre.
5. **Respect the score correction separately.** The owner explicitly reports that our score is too loud. Narration must remain foreground and the score should support it at a quieter perceived level. Whole-mix loudness and word timing cannot establish music-to-voice balance. This study supplies no reference-matched dB ratio, equalizer curve or measured music ducking target. Do not present the previous -16.2LUFS total-mix reading as evidence that the score balance was satisfactory.

## Reliability and completion

All three full reference runs completed, and first/last recognized-word positions are retained in the JSON. Low-confidence tokens below0.5 comprise about2.0% of Moon,2.9% of Lituya,3.7% of without-humans and2.2% of the sample. These percentages are diagnostic model outputs, not calibrated transcription accuracy. The Lituya place name is visibly mistranscribed in the raw ASR, and other proper names/numbers may be wrong. No factual claim is validated by transcription.

No listening-based claims are made about narrator warmth, stress, pitch, accent, emotional variation, score audibility, instrumentation, music entry/exit, sound effects or intelligibility. Nor do inferred word spans prove exact articulation or acoustic silence. These findings are enough to refine the **planned distribution of speech and space**, while the owner’s loud-score correction independently guides mix treatment. This requested study creates no routine per-film transcription or paid-review requirement.
