# AI movie reference study — Relatos de Eterya

Research date: **3 November 2026**. This is reference evidence for improving OpenMontage's existing AI movie style, not an approved production sample, measured retention study, or claim that OpenMontage already matches the channel. The owner requested deliberate research before providing a new sample title. No movie generation was performed. The initial review used free local tools; owner-authorized Algrow audiovisual reports for Alien and Island were subsequently incorporated as separately attributed evidence layers (6 existing credits each; the parent task reports 46 total across five analyses, within its 47-credit authorization).

## Selection and review coverage

Channel: [Relatos de Eterya](https://www.youtube.com/@RelatosdeEterya/videos), resolved by Algrow to `UCt7J_BNEiy2qJzKqZXAGvig`. Algrow's Videos tab with `sort=popular`, retrieved 2026-11-03, returned the following leading films. Counts are dated observations, not permanent rankings.

| Popular order | Film | Views returned | Length | Study treatment |
|---|---|---:|---:|---|
| 1 | [An Alien Asked Me to SAVE His Offspring… While His Giants Destroyed Our World](https://www.youtube.com/watch?v=uUbeeBsNEjI) | 24,676,070 | 21:16 | Full-timeline dense visual study, including ending; local ASR and motion windows |
| 2 | [Beautiful Woman Falls on a Lost Island and a Reptilian Humanoid Hunts Her Down](https://www.youtube.com/watch?v=IfYeyO9KU5I) | 21,301,807 | 20:39 | Full-timeline dense visual study, including ending; local ASR and motion windows |
| 3 | [The Tomb Raider Awakened Something That Should Have Never Been Awakened](https://www.youtube.com/watch?v=qnK-pO-gHaI) | 7,523,531 | 31:05 | Acquired with an English caption file; not visually reviewed, so not used for craft conclusions below |

**Exact limits:** the first two files were downloaded at at most 480p and inspected chronologically through **638 and 619 frame samples respectively**, spaced every two seconds. All 14 Alien contact sheets and all 13 Island sheets were inspected, including the promotional endings. Three four-second motion windows per film were additionally inspected at four frames per second: Alien 02:20–02:24, 07:30–07:34, 13:24–13:28; Island 00:35–00:39, 11:08–11:12, 17:48–17:52. This is **dense full-timeline frame-sampled review, not continuous natural-speed viewing**. Samples can miss very short cuts. Times in the tables are approximate sequence landmarks, not frame-accurate edit points.

The repository's local `VideoAnalyzer` ran standard analysis, scene detection, optical-flow motion classification, keyframes and audio-energy extraction. Separate local faster-whisper base ASR processed both complete soundtracks. This local pass used no paid transcription. No audible playback was performed. The later authorized Algrow reports supply model-described audio observations, distinguished below from independently checked evidence. Their internal claims of continuous viewing, waveform monitoring and frame-accurate inspection are **not independently verified**; they do not turn the local review into continuous audiovisual watching. Speech transcription is useful but fallible, and cannot establish that no other speech exists.

Evidence stays under `projects/ai-movie-style-study-20261103/eterya/`: `popular-selection.json`, `review-coverage.json`, source MP4s, `alien-sheet-00.jpg` through `alien-sheet-13.jpg`, `island-sheet-00.jpg` through `island-sheet-12.jpg`, six `*-motion-*.jpg` strips, and per-video `analysis/` / `transcript-result.json`. Portable conclusions are in this tracked document; a new machine does not need those large working files to use the style rules.

## Film 1: Alien — structure from opening through ending

The film opens in an active military confrontation, not with a biography, title montage or explanation. A pale humanoid alien stands in a snowy military compound, with a red-clad human observer giving the spectacle a readable emotional viewpoint. Its strongest general technique is a change of moral interpretation: something frightening and overwhelmingly powerful is connected to a very small, vulnerable child. The human-scale dilemma remains visually available while global destruction expands the stakes.

| Time | Observed progression | Transferable craft |
|---|---|---|
| 00:00–00:30 | A snowy compound, ranks of armored vehicles, armed soldiers, alien details, the observer taking cover; shots alternate threat, weapon, impact and human face. | Establish the immediate power imbalance and audience viewpoint before explaining the world. The title promise is visible immediately. |
| 00:30–03:30 | The alien survives attacks, deforms a gun barrel, throws soldiers, lifts vehicles; the observer hides beneath a vehicle and is exposed when it rises. | Give extraordinary power concrete material tests. Repeated action should change the protagonist's available shelter or escape route. Keep geography readable by returning to the compound wide shot. |
| 03:30–05:10 | A missile drives the alien into the mountain opening; pilots approach; a giant tentacled creature rises and catches aircraft. The alien later emerges with its wound visibly closing. | Escalate by changing the scale and invalidating an apparent solution. Show the apparent victory, then the new consequence. Avoid relying on an arbitrary narrator announcement. |
| 05:10–06:30 | The human is carried into the dark opening, struggles, passes through an enclosed descent and reaches a blue-lit impossible environment. | Bridge locations with physical transit and changing light. Fear stays connected to a recognizable body and face rather than only an environment montage. |
| 06:30–08:30 | Floating rocks and a vast blue sphere give scale; the human finds and cradles a small alien baby, examines it, and moves toward the sphere. | Turn the threat into a duty through an observable act of care. A close two-shot of face, hands and infant is the emotional counterweight to the giant exterior. |
| 08:30–10:20 | Eye close-ups connect the blue chamber to imagery of animal exploitation, mines, waste, fire, war, confinement and mass consumption, then return to the distressed caregiver. | The visual montage changes what the protagonist understands. It is a thematic argument rather than a new literal location journey. Our films must make any vision/memory transition legible and must not treat unexplained montage as causal action. |
| 10:20–12:20 | Military forces attack the giant again; vehicles, pilots and monster impacts intercut, then the film returns to the small chamber. | Counterpoint public force with private vulnerability. Each return should advance the deadline or decision, not merely repeat a spectacular shot. |
| 12:20–18:10 | Alien, human and infant share the chamber; city attacks unfold through bridges, offices, landmarks, a bus, a bar, roads and tourist spaces. | Giant scale is sold with foreground humans and familiar architecture. Several mini-scenes show ordinary activity, an eyeline/reaction, the revealed threat and physical destruction. These can be prepared as independent parallel sequences if their shared world state is fixed. |
| 18:10–20:28 | Chamber close-ups and worldwide destruction continue. Local ASR captures the human challenging the alien about children on the surface around 18:42–18:46. | Bring the moral choice back to the title conflict: compassion must extend beyond one protected child. Avoid letting the disaster montage swallow the central character's agency. |
| 20:28–21:16 | Complete-series promotional text appears. A short comic coda shows a gamer noticing a giant outside; signup cards finish the upload. | **This public upload is not a resolved standalone movie.** Do not copy the promotional cliffhanger or blooper/coda structure into a user request for a complete film. |

### Five-aspect production vocabulary: Alien

| Shot group | Subject | Subject motion | Scene, POV, overlays | Spatial framing | Camera / focus evidence |
|---|---|---|---|---|---|
| Compound conflict, 00:00–05:10 | Pale tall alien; red-clad human; groups of soldiers; armor and aircraft | Alien advances, survives impacts and manipulates material; humans fire, flee and hide | Snow, mountain bunker, overcast daylight, smoke and debris. Low ground views, aerial/compound views. Small opening production credits are an overlay, not scene signage. | Alternates eye/hand/weapon details, medium faces and very wide force layout; foreground vehicle undersides constrain the human | Ground-level angles amplify vulnerability; wide coverage clarifies force scale. 02:20 motion strip confirms a hand opening followed by a wider military view with individual moving bodies/drones; do not infer exact lens millimeters. |
| Infant chamber, 06:30–08:30 and later returns | Human and small alien infant; later adult alien | Human cradles, examines, looks toward a destination; faces and hands carry modest action | Blue luminous cavern/sphere, dark foreground rock; no explanatory captions visible in the study samples | Intimate medium two-shots and close faces against immense establishing views; red costume separates from blue environment | Stable intimate coverage and shallow-looking background separation. 07:30–07:34 shows a continuous caregiving reach and changing gaze, not a static portrait. |
| Office attack, about 13:20–13:52 | Office workers and giant outside glass | Workers turn, recoil, duck; creature passes windows and structure breaks | Daylit open-plan office, outside city high-rises, glass and debris. Overlays N/A in this group | Human foreground and giant background share the frame; interior wide → over-shoulder/medium → collapse coverage | 13:24–13:28 motion strip shows the worker moving at the window while the giant advances outside. Human eyeline motivates the reveal; exact camera rig and lens unknown. |

### Strengths and cautions

- Strong visual hierarchy: a distinctive red costume, a pale alien, blue cavern light and readable silhouettes keep the leads recognizable across large set pieces.
- The child gives the premise an emotional contradiction that spectacle alone could not supply. The human's care and final moral argument are more reusable than the particular alien design or landmark destruction.
- Ordinary people encountering a giant through a window, mirror, vehicle or doorway makes scale concrete. Foreground framing gives depth and a physical viewing position.
- The second half devotes substantial screen time to repeated city destruction. For OpenMontage, each escalation must change knowledge, resources, allegiance, risk or the protagonist's plan. More landmarks are not automatically more story.
- Many faces hold similarly extreme fear expressions. Our performance plan should include evaluation, restraint, tactical focus, relief and grief, with expression changing because an event changes the character's understanding.
- The visible letterboxing, very brief cuts and commercial ending are not imported. Owner rules require full-frame landscape, ordinary shots of at least two seconds and a complete requested story.

## Film 2: Island — structure from opening through ending

The actual opening is already a creature chase; the channel description's waking-on-an-island premise is not an opening scene observed here. A blond human in dark clothing flees through a dense tropical setting. The pursuer/rescuer relationship is repeatedly reinterpreted, and a small symbol gradually opens a larger world mystery.

| Time | Observed progression | Transferable craft |
|---|---|---|
| 00:00–02:05 | Pursuit through trees; a low hiding space and crawling insects make concealment uncomfortable; the large creature destroys the hiding space. | Begin with a readable objective and a failed tactic. Use terrain and small tactile details to make danger specific. |
| 02:05–03:25 | Escape into water reveals another enormous threat; competing creatures and a waterfall remove the apparent safe route. | An escape solves one immediate problem but creates a different one. Make the next obstacle follow the geography already entered. |
| 03:25–05:15 | A humanoid reptile confronts and carries the human to a cave; it offers a grub she rejects. | Replace a simple predator question with an intention question. A concrete food offer communicates incompatible needs without a speech explaining the species. |
| 05:15–07:50 | She escapes, encounters another predator, is rescued and carried through forest toward a narrow rock space; they are cornered. | A choice causes the setback; rescue changes the relationship. Establish the narrow route before making it a tactical constraint. |
| 07:50–09:40 | The humanoid fights the creature with a branch while the human reacts from shelter; the enemy falls and the rescuer is visibly affected. | Give the powerful protector a cost. Weapon contact, failed attacks and recovering balance are more legible than a generic fighting montage. |
| 09:40–11:50 | The humanoid leaves; the human returns to the cave, touches it gently, receives berries instead of the rejected grub, and begins communication. | Trust is earned through changed behavior: remembering what the other person can eat is a small, readable payoff to an earlier setup. |
| 11:50–12:50 | A triangular mark on a metal fragment becomes a shared object; pointing and taking a hand lead toward an intended destination; sunset moves into a rest scene. | Introduce a physical clue before its significance is explained. Let a prop shift the story from surviving to investigating. |
| 12:50–14:20 | Night exterior and cave coverage; a tether/holding detail preserves uncertainty; the following morning brings food and a wide view of the landscape. | Quiet scenes can contain unresolved danger. Show time passage through environmental cues and behavior, not random lighting changes within one action. |
| 14:20–16:25 | Forest micro-details, large insects and a waterfall route; the pair negotiate rapids, drops and underwater transit. | Vary scale without abandoning one objective. Use wide topography before close bodily danger, then show a destination/arrival. |
| 16:25–18:35 | The human notices debris with the same triangle, finds an overgrown facility, and matches the symbol to a mark on the humanoid. | Three-step clue ladder: object → environment → character. A repeated visual motif changes meaning and connects setting to personal stakes. |
| 18:35–19:58 | She enters the damaged facility, finds a monitor and operates a transmission-looking control; the protector and new creature imagery complicate apparent safety. | Let character action open the final complication. A screen belongs inside the scene; no duplicate floating explanation is needed. The exact technical function is not verified from the sampled screen alone. |
| 19:58–20:39 | The film switches to labeled failed takes/bloopers, complete-series promotion and signup cards. | **The public upload leaves the central mystery open.** A complete commissioned movie needs its own causal climax and consequence before any optional sequel seed. |

### Five-aspect production vocabulary: Island

| Shot group | Subject | Subject motion | Scene, POV, overlays | Spatial framing | Camera / focus evidence |
|---|---|---|---|---|---|
| Forest pursuit, 00:00–02:05 | Human in dark clothing; large quadruped predator | Runs, trips, crawls, hides; predator lunges and breaks cover | Dense damp forest, roots, fallen timber, canopy shafts and ground texture; low-level pursuit and reaction viewpoints. Small opening credits are separate overlays. | Feet/hands/eyes inserts intercut with medium running faces and wide human–predator spatial relationships | 00:35–00:39 strip shows a body roll and claw/head action across changing ground-level views. Fast coverage includes cuts under two seconds, which must be lengthened or redesigned for owner productions. |
| Cave care, 09:40–12:50 | Human and humanoid reptile, food and triangle fragment | Touch, offering, cautious eating, pointing and hand-taking | Dark rock chamber, cool entrance light, soft highlights on wet skin/scales; overlays N/A | Hand/food inserts and close reactions support medium two-shots; shared prop anchors eyelines | 11:08–11:12 confirms an actual berry pick-up/eating action across close views, then the reptile's reaction. Restrained coverage gives the gesture weight. |
| Facility discovery, 16:25–19:58 | Human, humanoid, marked debris and abandoned structures | Examines shard, approaches building, compares marks, enters, works a control | Overgrown industrial ruin with hard geometry behind vegetation, then cooler interior and red indicator light; screen content is diegetic | Shard close-up → wide building → face → shared two-shot → corridor depth → monitor/hand detail | 17:48–17:52 strip moves from a behind-human approach view to an eye close-up and an architectural wide. This is edited discovery coverage, not one camera movement. |

### Strengths and cautions

- The protagonist's repeated attempts to escape give the action a simple direction. Each new location offers an apparent solution and a new cost.
- The strongest emotional beat is behavioral reciprocity: unwanted food becomes suitable food, and terror becomes an offered hand. This transfers to any genre without copying creatures, costumes or scenes.
- The symbol is planted before the facility reveal. Future prompts should carry a persistent prop ID and material/mark description so generated inserts genuinely match later evidence.
- Sustained close-ups are used for emotion, but extended repeated frightened reactions can flatten performance. Write what changes in the character's appraisal on each return.
- The human is carried or rescued for much of the action. Our original movie should give the lead a consequential skill, tactic or sacrifice that the protector cannot supply. Dependence can be a phase, not the whole arc.
- Do not copy the title's attractiveness framing, specific character likeness, monster design, plot or commercial cliffhanger. Transfer suspense, tactile staging, setup/payoff and changing trust into an original premise.

## Measured pacing and what it does — not a quota

Local content-based scene detection used a 0.5-second minimum. Alien: **379 candidate shots**, mean 3.37 seconds, median 1.933 seconds, 193 candidates under two seconds. Island: **292 candidate shots**, mean 4.24 seconds, median 2.1 seconds, 132 candidates under two seconds. Detection is heuristic and may split movement or miss cuts; these are not hand-certified shot counts. The optical-flow classifier labeled 360/379 Alien candidates and 275/292 Island candidates as motion clips, consistent with inspected subject movement. It does not identify the generation model or prove flawless motion.

The useful pacing lesson is **contrast**: rapid action information and spatial reorientation, followed by longer intimate care/recognition moments. Do not copy the references' many sub-two-second fragments. Design useful internal shots of at least two seconds in a 30-second generation and preserve complete native speech/actions when selecting them. One generation is a sequence container, not a requirement to hold one angle for thirty seconds.

## Speech, score and sound: evidence boundaries

Alien local ASR returned 13 sparse speech segments: brief military commands, caregiving phrases around 07:28–08:05 and a moral challenge near 18:15–18:46. Island ASR returned only a few lines, with word timestamps around 11:26 (introducing a name), 12:10 (requesting a destination), and 18:02–18:11 (insisting on investigating the place). Its segment-level timestamp spans several minutes, so use the saved word timings rather than treating that as one continuous spoken passage. These automatic transcripts may omit speech or mistranscribe names.

This evidence supports planning **visual action with sparse purposeful character speech** as an available treatment; it does not warrant copying a voice or asserting that the soundtrack has been fully heard. Music instrumentation, loudness, thematic recurrence, transitions and exact foley remain unverified in this local study. For our films, prepare an original cue map linked to dramatic function—danger, uncertain alliance, wonder, costly choice, release—using the current AI music policy. Leave space for native dialogue and physical sound. This is a recommended production technique, not an observation falsely attributed to these references.

## Authorized audiovisual report: useful claims and reconciliation

Source: `uUbeeBsNEjI-algrow-analysis.md` (private research file), with the raw service receipt alongside it. The existing job completed and reported **6 credits charged**. The report covers the whole listed runtime and was read in full. Its account of how the model internally inspected media is not observable evidence. The Island submission initially returned `INVALID_ARGUMENT` without a job ID. The parent subsequently recovered its accepted, completed job through Algrow job history, verified the video ID and 6-credit receipt, and saved its full report. No resubmission or paid retry was made; its findings and limitations are recorded below.

### Soundtrack map reported by Algrow — not independently heard

The ranges identify broad dramatic passages. Exact cue boundaries and instrumentation are the report's descriptions, not measured or independently auditioned facts. They are useful hypotheses for understanding sound's role and designing an original score, not source audio to reuse.

| Passage | Model-described sound | Dramatic role and derived original-film application |
|---|---|---|
| Compound, approximately 00:00–03:30 | Driving percussion, low brass and choral accents under weapons, vehicles and drones; metallic electrical/sizzling accent during weapon deformation | Give the threat a recognizable physical sound. Specify important contact sounds and perspective rather than indiscriminate loudness. |
| Aircraft/giant, approximately 03:30–05:25 | Turbines, cockpit alarms, rockfalls, creature bass and constriction impacts | Alternate intimate cockpit information with exterior scale. A change of acoustic perspective can connect one event across cuts. |
| Descent/cavern, approximately 06:04–08:32 visually | Battle sound yielding to hollow/reverberant space, then soft synth pads, chimes, infant sounds and breathing | Let a real location boundary change ambience. Small bodily sounds can make vulnerability matter after spectacle. The report's 05:25 freefall/cue timestamp contradicts imagery; no corrected exact audio onset is asserted. |
| Ecological vision, approximately 08:33–10:22 | Industrial and war sounds with tragic orchestral/string material | Tie sound to what the character learns. Establish whether the passage is memory, vision or literal geography. |
| Military return/chamber, approximately 10:23–13:02 | Dense weapons/rumble followed by restrained drones and a resonant alien voice | Contrast public catastrophe with private moral exchange. Leave dialogue intelligible and let its outcome change the next scene. Reported alien lines lack local ASR corroboration. |
| Cities, approximately 13:03–20:28 | Sirens, glass, masonry and creature calls under orchestral/elegiac material | Differentiate imminent risk, impact and aftermath; reserve a score rise for a consequential change. Repeated loud destruction can lose force. |
| Gamer coda, approximately 20:38–21:06 | Dry game/eating sounds followed by sudden structural/creature impacts | Ordinary near-field sound can prepare a scale reveal. The abrupt comic tone is reference-specific, not a default serious-movie ending. |

No measured spectrum, dynamic-range values, stem separation or cue files were supplied. The report's claims of infrasound, binaural processing, exact orchestral entries and effects before *every* giant appearance are not retained as verified properties. Broad cue contrast is a creative lead, not a guarantee of soundtrack effectiveness. Island now has its own attributed audiovisual report below; neither soundtrack was independently auditioned in this local study.

### What matches, what needs correction

- **Supported visual relationship:** large-threat/small-infant contrast, blue sanctuary versus exterior destruction, everyday foreground objects selling giant scale, and eye-led vision transitions agree with local imagery. ASR also supports caring speech near 07:28–07:42 and a plea for surface children around 18:42–18:46. Empathy and a moral argument are reasonable interpretations; exact alien cosmology is not established.
- **Timeline error:** the report places vehicle lifting/exposure at 05:17–05:22. Local sheets place the earlier vehicle-lift reveal around 03:16–03:22. At 05:18–05:22 the woman is against a vehicle as the alien gestures; at 05:24–05:32 it draws her forward and picks her up. The shaft fall appears around 06:04. Its 05:25 sound transition cannot be adopted as a reliable editpoint.
- **Unsupported ending certainty:** its completed extinction and accepted guardianship are stronger interpretations than the public upload supports. Local imagery shows ongoing destruction, series promotion from approximately 20:28, an overlaid human/alien return at 20:32, provider cards, then the gamer coda and signup. The infant's fate and protagonist's ultimate success are unresolved. A claimed calm mother/infant payoff at 20:31 is not demonstrated by those frames.
- **Dialogue gap:** several model-reported philosophical telepathic lines and an early “why brought me” line were not captured by local ASR. Omission does not prove absence, but those quotations and delivery are unconfirmed and unnecessary to the retained rules. Local ASR places a similar human question around 18:14, not the report's 07:49 setup; the report also describes a 07:16 payoff before that alleged setup.
- **Camera precision:** wide/close contrast, low viewpoints, foreground scale, human eyelines and physical transitions are locally supported. Exact 45-degree orbits, rack-focus behavior, whip-pan timing, lenses and rigs are not confirmed by this sampling. Camera terms describe screen behavior, not proven equipment or generation providers.
- **Agency and provenance:** claiming the woman makes no choices after descent overlooks caregiving and her argument for other children. The narrower useful criticism is that these choices have limited visible influence on later destruction. The vision montage is not proven archival documentary footage; subject matter alone establishes neither provenance nor factual events.

### Island: recovered audiovisual report and soundtrack findings

Source: `IfYeyO9KU5I-algrow-analysis.md` (private research file), read in full; raw receipt `IfYeyO9KU5I-algrow-analysis.txt`. The recovered job is completed for the correct video and reports **6 credits charged**. Its claimed continuous, multi-pass audiovisual inspection is a model-authored description, not independently observable proof. Reuse the existing full-timeline local imagery and ASR as the cross-check layer.

| Passage | Algrow's audio description, not independently heard | Derived use in an original film |
|---|---|---|
| Opening pursuit and cramped hiding, approximately 00:00–02:00 | Low brass/string dissonance, footstep bass and brush contact; reduced musical density around close breathing/insect sounds | Vary chase tension through actual terrain and available movement. Intimate contact sounds can make a pause feel more dangerous than another loud sprint. |
| Lake threat and first humanoid encounter, approximately 02:00–04:40 | Water impacts, large creature voices and orchestral surge, then atmospheric vocal/pad material, clicks and splashes | Change the question from immediate predation to uncertain intent. Let acoustic perspective follow distance and bodily proximity. |
| Escape, rescue and duel, approximately 05:20–09:30 | Fast percussion, soil/contact sounds, creature strain, bodies against stone and wood splintering; reduced music following the fight | Make the material tactic audible and preserve a meaningful aftermath. Repeated rescue should not replace protagonist decisions. |
| Berries, shared object and rest, approximately 10:55–14:15 | Warm string/pad motif, restrained voices, cave drips, wind and night insects | A warmer cue can accompany earned trust after changed behavior. Keep the clue/gesture understandable without music explaining it. |
| Waterfall and ruins, approximately 14:55–18:50 | Orchestral rise, water roar, muffled underwater perspective, then a quieter uneasy environment | Motivate sound changes with medium and location. Preserve the same action across water/air transitions and let unfamiliar quiet prepare discovery. |
| Terminal and final threat, approximately 19:10–19:58 | Electronic pulse, monitor/relay sounds, distorted communication and a final creature accent | Screen operation and incoming communication can make information an event. A reveal should change the character's plan and have a consequence before the ending. |
| Bloopers/promotion, approximately 19:58–20:39 | Brighter commercial-style music | This is a marked promotional tonal break, not a template for a completed dramatic film. |

**Reconciliation and limits:**

- The report agrees with locally observed pursuit, rescuer reinterpretation, grub/berry contrast, triangle clue ladder, waterfall journey, facility/brand connection and labeled blooper ending. Those remain the reliable general craft examples.
- It claims a very specific twist: the protagonist is **Dr. Hannah Keller**, creator/handler of **Subject 17**, recognizes herself in surveillance footage, and confesses responsibility. Local ASR does not establish these names or lines. Saved 19:14–19:18 samples show a corridor/creature monitor image; they do not establish the described laboratory-clothed protagonist locking doors. Treat the identity, complicity and alleged intercom wording as **unconfirmed report claims**, not the film's verified explanation. The visible association between facility, brand and creature is established; full backstory is not.
- The report's section for the brand places it at 18:50–19:23, but existing samples show the clear arm/triangle comparison at 18:28–18:34, doorway approach at 18:44–18:50 and corridor at 18:52. Other passages in the report give the earlier time correctly. Use the local sequence landmarks, not every report timestamp.
- The sound diagram is illustrative, not measured dB evidence: it even places an 11:00 label before 08:00. No measurement supports its exact 40–50 Hz tone, below-200-Hz underwater cutoff, 1.8-second echo, precise pitch intervals or 2.5-second ambient lead. Calling ambience that begins before the next visual an L-cut is also misleading; it would ordinarily be a J-cut. Retain the general ambient-bridge idea without asserting that timing or terminology as verified.
- The report calls fleeing the cave irrational, but abduction and uncertain intent make escape a plausible choice even after a food offer. The stronger craft lesson is to show the character's understandable risk assessment and let it cause the setback. Its criticism of repeated last-moment rescues, prolonged passive reaction and promotional tonal disruption is useful without treating those judgments as measured audience effects.

**Additional original-film recommendations:** reveal new meaning through an established prop and motivated character action; if using a culpability reversal, plant fair evidence beforehand and show the protagonist choosing how to respond. Let the physically weaker lead contribute a unique observation, tactic or sacrifice to the ally's victory. Design geographic obstacles that change the available action, and use an original cue progression to support a relationship already earned on screen. These are derived choices, not copied identities, dialogue, creature designs or plot instructions.

## Portable rules for the AI movie style

1. Translate the title into an immediately visible conflict and an unanswered emotional question. Establish protagonist, objective, obstacle and physical geography before lore.
2. Map the ending and a few irreversible turns early, then fully stage the first ready sequence. Later scene detail may be planned during generation; downstream additions must respect already accepted character/world states.
3. Write sequences as **attempt → obstruction → choice → changed state**. An escape or apparent victory should cause the next problem. Plan a quieter consequence beat after a major action beat.
4. Give the spectacular force a vulnerable connection, and make empathy visible through action, props and altered behavior. Use two or three planted details with later changed meanings.
5. Prepare each 30-second sequence with a small readable cast, one geography, one continuity state, five-aspect shot instructions, dialogue timing and a useful end state. Split complex fights into readable causes and responses; do not cram unrelated locations into one prompt.
6. Reserve wide frames for spatial comprehension and meaningful scale; let close-ups reveal decisions rather than merely repeat fear. Motivate movement by following, revealing, approaching or escaping something.
7. Separate parallel-ready cutaways/set pieces from true continuations. Parallel city/secondary-character sequences can share a fixed world state; a direct continuation requires the returned outgoing state/reference. Keep one shared cast/prop/environment ledger.
8. Generate only required story coverage. Long provider duration should increase usable narrative seconds, not encourage redundant destruction, repeated rescues or padding.
9. Preserve original cast, available-light/material credibility, within-day continuity, native speech-picture pairing, ordinary shots ≥2 seconds, and full-frame landscape. Reference flaws do not override owner requirements.
10. Deliver the requested whole movie with a consequential climax and visible aftermath. An optional sequel question comes after resolution; external signup pitches and unresolved promotional endings are not the default.

Audience retention, relative visual superiority, actual production speed and usable seconds per Frameo slot remain **unmeasured** until an authorized original production is completed and timed.


## Derived preparation pattern for consistent 30-second sequences

This is an original production recommendation, not a reconstruction of the references' prompts or proof of their tools. Apply it within current AI-movie/Frameo policies. Detailed preparation should reduce ambiguous model choices without adding a review stage.

Before spending, write the full movie's causal spine and ending, irreversible turns, setup/payoff locations, cast/voice identities and persistent world facts. Divide it into useful 30-second sequences, each starting from a known state and causing one meaningful changed state. Prepare ready sequences using the same canonical references and descriptions. Actual same-shot continuation still depends on its real outgoing frame. Maintain full verified concurrency for independent ready sequences without inventing capacity or replaying accepted jobs.

Each sequence prompt should contain these concrete fields once:

1. **Purpose and state change:** whose immediate goal is blocked, the practical choice, its cost and observable end state. Identify the earlier setup paid off or why this makes the next sequence necessary.
2. **Identity and continuity:** exact cast/reference IDs, settled native voices, costume/damage, carried objects and holding hand, injuries/fatigue, knowledge and relationship. Reuse the same descriptions; avoid replacing the established person with a generic face.
3. **Stage geography:** actor, obstacle, exit and light-source positions; screen direction; contact points; reachable distances and plausible order of physical work. State what the actor can actually see.
4. **Light and material:** motivated source direction, time/weather and persistent conditions; contact, weight and reaction. A light change requires movement or an environmental cause.
5. **Timed shot plan:** for every internal shot, specify subject, action, scene/POV, framing and camera/focus behavior. Motivate movement with action or a reveal. Use a manageable number of useful shots, each at least two seconds, without a fixed cut-count quota.
6. **Performance and speech:** appraisal before/after the event, gaze target, action pauses and exact short lines with speaker and sufficient spoken duration. Leave breath/response time and preserve native speech-picture pairing. Avoid simultaneous complex combat, long speech and multiple emotional changes.
7. **Sound and ending:** location bed, key synchronized contacts, any original cue's role and dialogue space; last usable action/state and transition intent. Avoid mid-film credits or unwanted fades.

An illustrative six-shot allocation is **0–5 / 5–10 / 10–15 / 15–20 / 20–25 / 25–30 seconds**: establish actionable obstacle → attempt → physical resistance → appraisal/choice → changed tactic with contact → consequence and next need. This is not a required rhythm. Dialogue may need three longer shots; discovery may need four with a longer recognition hold. The plan should total the requested duration, let actions complete, and never use a one-second fragment to squeeze in another event.

Consistency comes from preserving concrete identity, geometry, props and causal end states before the call. Use existing brief local checks for real defects, returned internal cuts, minimum duration and export/audio usability; no routine paid analysis, repeated external reviews, per-clip scoring or new approval checkpoint. Repair a concrete fault within authorization and continue. Preparation improves the chance of consistency; quality and speed remain unmeasured until a new sample is produced.
