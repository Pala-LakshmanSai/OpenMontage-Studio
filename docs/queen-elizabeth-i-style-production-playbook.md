# Queen Elizabeth I Style — production playbook

Refined 5 November 2026 after the owner's detailed sample/reference comparison.
Read the [style guide](queen-elizabeth-i-style-preferences.md),
[reference evidence](queen-elizabeth-i-style-reference-notes.md),
[production prompt](queen-elizabeth-i-style-prompt-template.md) and
`styles/queen-elizabeth-i.yaml`. First apply the
[whole-screenplay foundation](queen-elizabeth-i-style-screenplay-foundation.md):
review/adapt the complete story and write a coherent revised screenplay through
its ending before any new image, video, speech or music generation. This overrides
the previous spine-only start rule for this style. Follow
[fast production](video-fast-production-preferences.md),
[human performance](ai-video-human-performance-preferences.md) and
[minimum actual shots](minimum-shot-duration-preferences.md).

This is a practical implementation of the historical character-vlog format.
The reference findings use owner-approved timeline/temporal picture samples,
transcripts and local signal measurements. No direct listening or continuous
normal-speed viewing is claimed. The connected Nextlev catalog/transcript tools
worked; its audiovisual watch tool rejected the Free account. Exact timbre,
instrumentation, phoneme sync and creator parity remain unverified. The changes
below are saved direction for future footage, not proof a new film has passed.

## The episode's working engine

Begin with a specific promise the viewer can understand, an original host with a
clear role, and a visible situation. A routine reveals the work and relationships
behind rank. A political episode explains agents and mechanisms through a personal
viewpoint. A place episode earns access and makes architecture socially meaningful.
Write action or object, plain explanation, social implication, then a brief dry
aside when the situation earns it. The next beat follows a result, need, decision,
interruption or revealing reply. A new room alone is not a new story beat.

An input story is an adaptable outline. Preserve its identity, emotion, curiosity,
hooks, setups/payoffs and ending while adding needed bridges, work, reactions and
supporting agency, or removing/reordering/combining weak material. Give action and
emotion performed time. Approximate length may grow roughly 60–70% when useful
(for example ten minutes to sixteen or seventeen), but this is not a padding
target. The actual budget and explicit hard constraints remain real. Record the
reviewed whole screenplay, protected core, concrete adaptation decisions, required
beats and ending in `script.metadata.narrative_foundation`; resolve structural
gaps before new media. No additional owner approval or paid scorer is needed.

Keep a small set of live questions. Pay off the title, the most important early
promise and the human thought before a callback or optional audience invitation.
Vary pressure through curiosity, restriction, embarrassment, disagreement, work,
affection or responsibility. Do not schedule an extreme danger or twist every
fixed number of seconds. A bath routine and a political crisis need different
stakes. Factual history needs authoritative verification; original encounters and
comic incidents must be identified as dramatized fiction.

For a separate Claude Project, paste the single
[story prompt](queen-elizabeth-i-claude-story-prompt.md) with channel links, title
or topic and approximate duration. Retain its researched style bible and reuse
valid learned rules rather than repeating the complete reference study for each
title. The same prompt handles research when needed and the finished story.

## Direct the image before adding adjectives

| Element | Direction to put in the existing scene plan | Avoidable sample tendency |
|---|---|---|
| Opening | One playful near-lens image, then a physical arm extension or camera settle into conversation. Keep it a continuous ordinary shot. | Beginning and remaining in one reserved medium-close view. |
| Host framing | Close/medium-close wide-perspective conversation; change distance, height or attention when action or a listener motivates it. Keep the face readable. | A fixed arm pose and repeated same-corner framing. |
| Interior depth | Foreground work or object, host/listener in a readable plane, background labor or architectural route. Choose period materials with social purpose. | Empty plaster/beams and a table serving every story function. |
| Light | Expose the face and current object from a plausible window, sky or practical source; keep natural room falloff and motivated warm/cool depth. | Uniform flat exposure, an orange wash, or haze used to disguise sparse staging. |
| Wardrobe | A readable original status silhouette and texture appropriate to private/public activity; caused layer changes when the routine needs them. | A generic costume that gives little information about role or occasion. |
| Supporting people | Useful work, a distinct intention and a reaction or reply that affects the next beat. | A person standing behind the speaker waiting for the entire passage. |
| Detail coverage | The object is used, changed or explained. Let hands meet the correct supported surface. | Decorative inserts, display holds and unexplained prop resets. |
| Movement | Physical handheld drift, a useful walk, a turn toward a listener or a motivated handoff. | A smooth orbit, continuous zoom, random wobble or an invisible second operator. |

The near-lens opening is a recurring Elizabeth reference signature. Chloe's studied
openings instead establish a modern visitor in a destination with a practical or
sensory problem. Keep the selected primary format. Do not make every secondary
reference inherit Elizabeth's opening or make the Elizabeth host behave like a
modern tourist. Exact lenses and capture hardware are not established.

## Keep a long shot active

A sustained shot can contain a completed thought, a hand using an object, a shift
of attention and a listener's response. The reference does not require rapid
cutting to make these changes readable. At Get Ready 148–159 seconds, the cloth
is actually used before another dental object enters the conversation. At
357–368 seconds, the ruff, attendant's work and framing support the current thought.
At Palace 282–293 seconds, a tangible book leads from a personal claim into a
physical turn toward an attendant's reply. These are temporal sample observations,
not exact universal timing targets.

In the improved sample, the search passage at 24.29–54.33 seconds preserves
continuity but spends substantial time in one view; around 36–44 seconds an
outstretched palm and looks repeat while the attendant waits. A stronger script
would let a search result, useful work or a reply change the next action. A trim
can remove an idle tail; it cannot create missing historical insight, an absent
relationship or a more expressive performance. Solve those before generation.

Keep short concrete thought groups and allow their natural rhythm. Full-minute
ASR counts were roughly 80–95 words per minute for the Elizabeth references,
about 75 for the improved sample, and roughly 115–156 for the five Chloe references.
These include silence/actions and are fallible transcript measurements, not
articulation settings. Do not accelerate native audio or force a long request to
contain continuous speech. Repeated pauses after every sentence are not wit.

Actual shot boundaries follow complete words and useful action. Preserve ordinary
shots of at least two seconds. Earlier reference detector medians around 6–29
seconds were candidates, not certified shot counts; a lower-threshold rescan
oversegmented moving reference footage and was rejected. Do not use either to
enforce a numerical cut frequency. Do not retain all 30 generated seconds merely
because they exist.

## Use one concise sequence card

Put these fields in the existing scene plan and provider prompt. Do not create a
separate approval document for each clip.

```text
Sequence ID / story order / required payoff:
Entry state → caused change → exit state:
Subject: original host and named supporting roles; identity/wardrobe references.
Subject Motion: one main achievable action at a time; contact, support and result.
Scene: period/place, time/light, background work; overlays listed separately or none.
Spatial Framing: opening size/position/depth; what change earns the next framing.
Camera: holder/support, physical path, normal speed, incoming/outgoing relation.
Speech: named speaker, exact local line IDs, listener/intention, visible-mouth or
        offscreen window, natural completion/reaction room. Staging is not speech.
Sound: native voice and matching mouth; coherent room/footstep/fabric/contact sound.
Reference roles: identity only / geometry only / current-state first frame.
Dependency: independent scene OR exact prior usable state required.
Edit intent: complete action/phrase to keep; likely release point; no next-scene spill.
```

An original fictional court-clothes beat could begin with a host attempting to
dress without help. A back fastening makes the problem visible; an attendant
continues fastening while the host comments on the employment this arrangement
creates. The attendant asks for the other arm, changing the host's posture and
puncturing the boast. The costume's physical design supplies information, work
and humor in one situation. Verify any claim that this fastening represents a
particular historical garment. This example is a writing/staging recipe, not a
copied reference scene, a generated take or a required future plot.

For that beat, a provider prompt should name the actual fastening location and
support, keep the host's hand free of an impossible reach, assign the camera to
the other hand or an established support, and put any demanding turn between
complete phrases. Finish the line before a large camera turn. Bring the face back
before a new visible-mouth line. A supporting reply needs its own consistent
original voice and visible/offscreen assignment; reuse a settled voice without
an audition contest.

## Prevent the two expensive state mistakes

The baseline sample exposed a concealed stamp before its intended discovery,
then a later internal cut restored a letter that had already departed. Preserve
the successful footage, but do not treat those as stylistic preferences.

Use a clean identity reference for independent scenes; use an accepted current-state
frame for an actual continuation where supported. Declare room geometry separately
from live props. Repeat irreversible changes in later shot contracts, including
inside a multi-shot request: who owns the object, what left, what remains and who
is now present. Keep a concealed discovery region out of frame until its planned
action when that is the reliable staging choice. A negative instruction alone is
not evidence the returned footage obeyed it.

Do not chain every unrelated scene from a progressively degraded face frame. A
continuation frame preserves a real dependency; a clean master preserves identity.
Keep the same selected character, age, costume attachments, geography, light and
native voice. A local trim must not remove the actual mechanism, needed clue or
last word merely to hide a contradiction.

## Faster production with the same useful coverage

1. Reuse this study and the selected cast/voice/world where applicable. Read the
   supplied story through its ending, review and strengthen it, and write the
   complete coherent revised screenplay before new media. For title-only work,
   develop and review that complete story first. Follow this named style's own
   foundation without importing AI Movie genre rules. Afterward, finish the first
   detailed ready sequence while later prompts/references continue in parallel.
2. Prepare each identity/location asset once. Before admission, verify a new
   transport URL is publicly fetchable with the correct media bytes, without
   forwarding credentials to the host. Cache it by source hash. The sample's
   Frameo upload succeeded but its public fetch returned HTTP401; an existing
   authorized file-hosting route resolved transport without changing the model.
   Do this before occupying a generation slot, not after a failed video request.
3. Give ready independent sequences to available authorized Studio/API routes
   with disjoint IDs under one shared admission owner and ledger. Default to useful
   30-second multi-shot requests under the verified unlimited entitlement. Shorten
   only for an actual story/action/reference/model constraint; do not pad speech.
   A state-dependent continuation waits for its needed outgoing frame while other
   independent work proceeds. Agent count is not extra provider capacity.
4. Obtain the exact route's current zero-credit quote when pass-only generation
   is authorized. Count accepted, queued, submitting and uncertain jobs against
   actual shared capacity. Resume exact receipts; never replay uncertain work.
   Reconcile a stale handoff against current evidence instead of waiting on an
   idle chat indefinitely. Preserve the owner's current project priority.
5. Download a completed asset promptly and publish its canonical scene ID, actual
   usable range and state into the selections artifact immediately. Assemble
   cached selections while later jobs run. Preserve native frame cadence and
   speech-picture pairing; use timestamp-aware PCM preparation in
   `lib/native_audio_assembly.py` before sample-based native-audio mixing. A frame
   rate control alone does not certify audio-padding or mouth articulation.
   Map required story beats to observed selected ranges in the existing narrative
   coverage metadata. Prompt intent or completed downloads do not establish a
   missing bridge, useful reply, physical result or emotional payoff. Preserve
   accepted work and reconcile only affected dependencies after a material
   screenplay change; do not replay uncertain jobs.
6. Use a brief state/obvious-defect check for an actual dependency, then one final
   local batch check for playable full-frame720p/768p output, complete speech and
   ending, sensible audio, essential identity/state continuity, minimum actual
   shots and regular Downloads delivery. Cache unchanged cut/conform results.
   This requested detailed study is not a new per-film full-audit requirement.
7. Repair the responsible layer and smallest useful passage. Reuse successful
   reveal/work/payoff footage, prefer a sound selection or trim where sufficient,
   and regenerate only a concrete material fault within the real budget. No routine
   paid scoring, per-clip ASR, repeated contact sheets, cosmetic reroll loop or
   new owner approval gate. Release generation capacity once required usable
   footage is complete; local export and delivery can continue afterward.

For native24fps landscape footage, explicitly set the low-level FFmpeg compose
target rather than relying on a legacy default or an unrelated export profile:

```json
{"metadata":{"compose_target":{"width":1280,"height":720,"fit":"cover","fps":24}}}
```

This belongs inside the `edit_decisions` artifact. The compose utility now resolves
that requested cadence for both native-audio and silent-source segments. A named
profile overrides target dimensions and fps, so a30fps/1080p profile is unsuitable
for this720p24 request. It also avoids a redundant final picture encode when the
segments already meet the profile and no visual filter requires another encode.
This is a local pipeline improvement, not a measured provider speedup or an AAC
join/articulation fix. Preserve native sound and actual frame timing when mixing.

The sample's timing evidence explains why scheduling matters. Initial style
completion was 09:40:45UTC and the first job acceptance was 11:38:46UTC, a gap of
about118 minutes dominated by shared admission availability/coordination rather
than encoding. Original accepted-job-to-download observations were roughly
5.5–11.3 minutes; the two targeted repairs overlapped within about9.1 minutes
wall time. Poll observations are not exact inference durations or a future speed
guarantee. Measure preparation, shared admission wait, provider observations,
downloads, assembly and delivery separately; do not add overlapping stages as
if they were serial.

## Diagnose and retain the lesson

| Observed gap | Responsible layer | Correct there |
|---|---|---|
| Fixed framing replaces the repeated near-lens-to-conversation reference opening | Style interpretation / camera plan | Restore the camera signature on an original face. |
| A generic prop joke teaches little about the period or relationship | Story / screenplay | Give the object a concrete function, social implication and useful interaction. |
| Host gestures and attendant waits through a whole take | Blocking / performance | Stage actual work, a meaningful response and a caused next action. |
| Hidden or departed object appears in the wrong state | Reference/state contract / generation | Use correct state/framing, repair the affected passage and its dependency only. |
| Complete phrase followed by unnecessary inactivity | Selection / edit | Remove the idle interval at actual boundaries without retiming speech. |
| Measured edit offset or accumulation at joins | Assembly | Correct the measured timing mechanism; do not dub over an incorrect mouth. |
| Exact voice, score or lip quality cannot be assessed | Evidence capability | State the limit; do not mark it heard, matched or passed from ASR/metadata. |

Save durable corrections in these canonical project files and their indexed
templates/playbook, with observed evidence and scope. On another computer, copy
the repository knowledge and configure permitted providers separately; resolve
media paths and that user's Downloads directory. Neither the original Mac/SSD
paths, private Pages nor personal Codex memory are prerequisites for using the
style. Portable instructions transfer the method, not entitlements or guaranteed
creator-level results.


## Full-film implementation evidence — Cleopatra Rome,6November2026

The first full film was delivered as11:22.833333 of native720p24 footage from the supplied adaptable outline. Current25sources and49required beats are explicit selected coverage;26raw revisions remain preserved. This is observed production/technical evidence, not owner aesthetic acceptance or a creator-parity claim. Detailed case: `projects/cleopatra-rome-20261105/production/production-lessons.md`; final artifacts and hashes are under that project.

Historical invisible-camera handoffs should be staged through empty hand-to-lens movement, physical framing change and free hands; literal named capture objects repeatedly exposed modern hardware. Preserve complete native words before picture repair: a verified listener crop can retain an entire reply when the last phoneme overlaps a bad handback. Use actual returned source cuts for edit exits: this film's first encoded check caught a three-frame modern-device spill missed by coarse end samples; the targeted local trim and final cached check resolved it without new generation. Keep earlier/daytime review voices and the final lamp/child/December landing coherent.

Actual coverage may justify a reviewed minor adaptation through the ending. Here a visible shared local dice game established friendship/language learning; no precise initial defeat was invented when it was not observed. The later translation and actual counter win/wave remained. A brief warming-layer ellipsis linked lavender public clothes to the dark cloak in the final address/child scene. These are specific editorial decisions preserving core/emotion/payoffs, not permission to erase a missing cause or fake coverage.

The Frameo pass ended before three queued required scenes yielded usable outputs. No99.99USD/day renewal or nonzeroFrameo overflow was purchased. Existing20USD authority supported only three necessary same-model Kie replacements with original cast/voice and useful short video references, at3648reportedcredits/18.24USD rate-card estimate; whole-chat estimate18.56USD. The registered narrow adapter and fresh pricing/budget guards are documented in the Seedance2.5 skill; never infer a general free/paid fallback entitlement. Release/ping the next authorized chat once all required usable generation is finished, before editing/export, and include actual entitlement gaps.
