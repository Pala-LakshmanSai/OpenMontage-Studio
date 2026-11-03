# The Last Day — measured audio comparison and quieter-score correction

3 November 2026. The owner reports that the pilot's background music is louder
than the popular references and requests closer storytelling, narrator cadence
and audio balance. This study uses free local measurements of five complete
cached reference mixes, the delivered pilot and its available audio components.
No audible playback, paid analysis, ASR, new generation or video rerender occurred.
The owner feedback is the artistic direction; measurements identify a practical
correction without claiming they prove a reference's unavailable stem balance.

## Whole-mix measurements

Measured with FFmpeg `ebur128`, including true-peak estimation, over each entire
first audio stream. Source SHA256, codec/stream details, short-window statistics
and thirty-second level summaries are in [audio-measurements.json](audio-measurements.json).
The references are cached stereo 48 kHz Opus deliveries; the pilot is stereo
48 kHz AAC. These are not the creators' original masters.

| Complete decoded mix | Integrated LUFS | LRA, LU | Approximate true peak, dBTP |
|---|---:|---:|---:|
| [Nepal glacier](https://www.youtube.com/watch?v=vfIaNeGVaVo) | −14.46 | 3.18 | −0.04 |
| [Moon collision](https://www.youtube.com/watch?v=eGfbwdXL3wg) | −14.44 | 3.63 | +0.02 |
| [Ocean asteroid](https://www.youtube.com/watch?v=hxlGCMo6ihI) | −14.39 | 2.96 | +0.12 |
| [Lituya Bay](https://www.youtube.com/watch?v=nhaTh5gGXiM) | −16.13 | 5.87 | +0.18 |
| [Earth without humans](https://www.youtube.com/watch?v=vtUUjqQGk1o) | −16.18 | 6.33 | 0.00 |
| Nuclear pilot, delivered original | −16.15 | 3.91 | −1.00 |

The pilot is close to two references in overall integrated loudness and quieter
than three. That does **not** contradict the owner's score complaint: integrated
loudness combines voice, music, ambience and effects. Turning the entire mix down
would reduce narration too, leaving its internal balance essentially unchanged.
The references' music-versus-narrator ratios cannot be recovered from these
full-mix figures. Near-zero decoded reference true peaks are observations, not
mastering targets to imitate; retain output headroom and measure the final AAC.

LRA also does not measure narrator expression. The five references span roughly
3–6 LU rather than one universal number. Full-mix momentary low-level fractions
cannot establish pauses between spoken phrases because music/effects continue.
No exact reference WPM, voice identity, articulation, emotional delivery or
pause cadence is claimed from this analysis.

## What the pilot's available components reveal

The pilot's `native-normalized` component includes offscreen narration **and**
generated ambience/effects. It is not an isolated voice stem. The added
`score-bed` is a separate instrumental component. Both cover exactly the same
600.833333-second timeline.

| Component before final addition | Integrated LUFS | LRA, LU | Approximate peak |
|---|---:|---:|---:|
| Native unnormalized mix | −17.19 | 4.17 | −2.00 dBTP |
| Native normalized mix | −16.03 | 4.18 | −1.50 dBTP |
| Original added score bed | −27.01 | 7.54 | −12.77 dBTP |

The score's actual −27.01 LUFS is louder than its nominal −28 cue-normalization
setting; assembling/crossfading/trimming cues does not guarantee the complete
bed retains each cue's target. Use measured output values, not only knob labels.

Matched 400 ms momentary windows sampled every 100 ms, excluding the first three
seconds, give 4,903 windows where native momentary loudness exceeds −30 LUFS.
This selects an **active-native signal proxy**, not verified speech activity.
Within those windows:

- Median native-minus-music difference: **10.94 LU**.
- Tenth percentile difference: **4.32 LU**; fifth percentile: **1.76 LU**.
- Music is within 10 LU of native in **41.42%** of windows, within 6 LU in
  **15.64%**, and above native in **3.18%**.

Weak syllables, pauses and generated ambience affect that proxy, so these are
not claims that music masks a particular word. They do show why a globally quiet
score can approach the native signal during portions of this film. The remedy
should lower the added score while preserving narration gain and timing.

## Concrete correction prepared

Created new scratch PCM assets under the pilot's `assembly/audio-refinement/`;
original sources, the original mix and the delivered MP4 were preserved.

- `score-minus9db.wav`: original added bed multiplied by
  `10^(-9/20) = 0.3548133892` in amplitude. Measured **−36.01 LUFS**, LRA7.54LU,
  approximate peak−21.83dBTP.
- `mix-music-minus9db.wav`: normalized native component at unity gain plus that
  attenuated score, `amix normalize=0`, existing −1dB peak limiter with latency
  compensation. Measured **−15.98 LUFS**, LRA4.18LU, approximate peak−1.20dBTP.
- Both are 48 kHz stereo 24-bit PCM with **28,840,000 samples**, exactly
  **600.833333 seconds**. No phrase retiming, silence removal, narration
  regeneration, image change or native source replacement was performed.

The mixed integrated number can increase slightly when music is reduced because
EBU loudness gating changes which low-level blocks contribute; it does not mean
the voice was boosted. Native input gain remains 0dB. The limiter may still change
rare summed peaks; the narration source itself is preserved.

The new score shifts the same aligned native-minus-music differences by +9LU:
median about **19.94LU**, tenth percentile **13.32LU**. This is a derived difference
for unchanged components, not a perceptual listening result. It makes the score
substantially quieter while keeping it available for atmosphere. Artistic
acceptance and comparison at matched playback gain remain separate.

The parent owns final remux/export/sharing. Preserve the picture and exact native
sample timeline, encode the new mix once to the intended delivery codec, and
measure resulting peak/loudness. Do not compensate by normalizing the score back
to −28, enabling amix's default averaging without accounting for it, or boosting
the whole mix simply to reach the loudest reference's integrated value.

## Portable voice-first sound default

For this named style, start with a much quieter score than the pilot's original
bed: about **20–24 LU below typical narration-active short-term level**, with
narrator intelligibility controlling the choice. This is an owner-responsive
production target, **not a measured channel stem ratio**. With native narration
near −16LUFS, roughly −36 to −40LUFS for a steady underscore is a useful starting
point; actual simultaneous windows and cue peaks matter more than two unrelated
integrated values. The prepared −9dB change is the concrete pilot correction.

Plan music entries, exits and silence around explanation/reversal/payoff, not
provider chunks or a fixed percentage of runtime. Keep score restrained through
technical explanations. Do not automatically swell in every narrator breath;
quiet or silence can carry the beat. Reuse authorized music where available;
this direction adds no external music-generation authority.

If a particular cue still competes, prefer a small local automation reduction at
that thought group. Where supported, use an extra approximately 3–6dB of ducking
under narration, with a gentle roughly 50–100ms attack and 500–1000ms release.
These are starting settings, not proven output. Confirm actual gain reduction
and avoid audible pumping. Use the settled narration track/envelope as the key,
not the whole final music-bearing mix. If the only native track contains loud
effects, its envelope is an imperfect key: use prepared phrase windows or local
cue gain rather than assuming a speech-only signal. No default source-separation
service or per-clip paid analysis is needed.

For closer cadence, solve the writing/performance contract before mixing:
connected thought groups, varying sentence length, an urgent concrete opening,
clear mechanism explanation, meaningful emphasis and a restrained ending.
Do not force every 63–72-word paragraph to occupy one full 30-second source or
insert a pause at every generation boundary. Retain complete natural phrases;
never use speed changes to imitate a reference. Reuse one original permitted
voice reference and state delivery intention per thought. Conditioning and
loudness matching alone do not prove voice continuity or a similar human feel.

## Reproducible local method

For each locally resolved asset, without changing it or playing audio:

```sh
ffmpeg -hide_banner -nostdin -i INPUT -map 0:a:0 -vn \
  -af 'ebur128=peak=true:metadata=1,ametadata=print:file=-' -f null -
```

Parse each `pts_time` and `lavfi.r128.M`, `S`, `I`, `LRA`, `true_peak` value.
The last `I`/`LRA` values summarize the run. Convert cumulative linear true peak
to dBTP with `20*log10(true_peak)`; FFmpeg prints the linear metadata to limited
precision, so especially low peaks should not be treated as exact hundredths.
M is 400 ms, S is 3 seconds; percentiles exclude the first three seconds of
warm-up. Align native/score windows within 10ms before comparing them. Hash every
input, record codec/sample rate, and identify sources by public video ID or
portable project asset ID rather than private paths.

The corrected scratch mix's equivalent filter is recorded in the JSON. It
resamples both components to48kHz, lowers only music9dB, adds without automatic
normalization, applies the same compensated limiter and caps to the exact existing
sample count. Reference measurements, known-stem comparisons, owner preference
and proposed future settings remain explicitly distinct. This requested study is
not a new routine analysis requirement for every subsequent film.
