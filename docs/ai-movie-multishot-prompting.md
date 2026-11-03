# AI movie: consistent multi-shot passages in one 30-second request

Owner refinement, 3 November 2026. This is reusable preparation guidance, not an
extra review stage or a generated sample. Read with [movie training](ai-movie-preferences.md),
[Frameo production](ai-movie-frameo-production.md),
[fast production](video-fast-production-preferences.md) and
[human performance](ai-video-human-performance-preferences.md).

## One generation contains several shots; one scene changes something

Thirty seconds is an efficient request size when it contains useful story. It is
not a thirty-second camera hold, a fixed edit length or a guarantee of continuity.
Choose the shot count from action and speech. Examples: a dialogue turn can use
three 8–12-second views; urgent physical action can use five or six 4–7-second
views; a discovery can combine a wide, detail, recognition and consequential move.
These are starting patterns, not quotas. Ordinary **actual** visible shots must
remain at least two seconds, including internal cuts and meaningful screen states.

Give one passage a manageable causal change: notice a problem, decide, attempt,
receive a result. Avoid packing a new location, new cast, weather change, fight,
speech, flashback and climax into one request. Deliberate time/location changes
may be separate ready roots with explicit transitions. Long generation reduces
some between-request seams; it does not remove drift at internal cuts.

Changing from close/medium to wide does not reset who is present. Carry each
participant's world position and task into the wide; show anyone whose location
falls in that view. A person's absence needs a real crop/occlusion, exit or time
change. An empty room is a geometry reference, never proof that the active scene
has become unoccupied. Use an occupied wide state when cast presence matters.

## Compact continuity contract, reused rather than re-researched

Keep one film bible and sequence state ledger. The prompt only carries applicable
invariants and the changes needed for this passage; do not paste the whole film
or describe every offscreen character as visible.

| Layer | Fixed until a visible cause changes it |
|---|---|
| Character | Reference identity, age, face/hair, anatomy/scale, voice, wardrobe, injury and wetness |
| Relationship/performance | Who knows what, who trusts whom, current intention, emotional intensity and listener |
| Environment | Map, doors/barriers, travel direction, sun/practical-light sources, time/weather, surface condition and ambience |
| Object/action | Exact count, identifying marks, hand/owner, contact, tool state, damage, attachment and completed action |
| Camera | Side of axis/barrier, height, distance, shot size, movement and screen direction within each shot |
| Sound | Speaker and exact line, native timing, acoustic space, continuous ambient bed and intended cue transition |

Add the acting target and machine/animal state directly to those same shot
fields: **look/orient → reach/approach → supported contact → visible result**.
Name what the actor sees and where it is, including head/eye height. A glance
away has a separate cue and beat. An occupied container remains visibly occupied
in each exposed view; do not use an empty-set image as proof of the current state.
Show the control and actual stop before hands approach a moving mechanism; a
fantasy light source does not waive normal mechanics or aquatic buoyancy/gills.
Bodies, carried animals/bags and cameras follow a real clear opening and path;
solid railings/doors/walls remain solid and the side of each barrier persists.
Show the stair-entry gap and feet on actual treads instead of asking for a vague
ascent that lets the model route the body through iron rods.
Keep a motivated practical light on faces/hands/creature when the story beacon
fades. This is prompt preparation and reuse, not another review layer.

Resolve identity once using clean supported masters. Use state anchors when a
different costume/pose/location actually needs one, not an automatic image per
shot. Label references by role and scope: character identity does not import its
old clothes, luggage or background. For an object clue, keep the same geometry,
mark, orientation and damage across inserts and later payoff shots.

At a cut, restate what matters from the preceding action. "Same character" alone
does not preserve the held tool, hand, side of a doorway or completed repair.
Specify the next visible state positively. Avoid contradictory locks such as
"hands never move" while requesting a knot, or "single continuous shot" alongside
hard cuts. Native 30-second dialogue must fit actual speech plus reaction time;
do not slow every syllable or fill the entire request with words.

For multi-character dialogue, assign each complete phrase to one named speaker
and visible face window. Specify when that speaker stops and the listener reacts;
do not give both faces the same global paragraph. Use character-specific reference
roles supported by the actual route. If a clean accepted native take establishes
needed voice behavior, only takes dependent on that new voice wait for it. Other
ready work continues. A reference image/audio is conditioning, not proof that the
returned face, voice and articulation stayed consistent.

## Prompt assembly order

```text
SEQUENCE ID / NARRATIVE CHANGE
  [What choice/result changes the story and what the next sequence inherits.]

GLOBAL LOOK / WORLD
  [Original genre/look, 16:9, natural speed, motivated light, material behavior.]

REFERENCE ROLES / CAST
  [Identity A, identity B, location geometry, optional voice/state reference.]
  [Only visible cast; exact distinguishing wardrobe, anatomy/scale.]

START STATE / GEOGRAPHY / PERSISTENT LOCKS
  [Positions, axis, light, props/hands, injury/weather and offscreen boundaries.]

00:00–00:__ SHOT 1
  Subject; action in temporal order; environment; framing/depth; camera path.
  Exact short dialogue, speaker/listener and room for response if present.
  What is true at the end of the shot. HARD CUT to Shot 2.

00:__–00:__ SHOT 2 ...
  [Restate the relevant carried state. A new angle does not repeat the action.]

... through 00:30

NATIVE SOUND / END STATE
  [Continuous acoustics/ambience, specific synchronized sounds, scripted voices
   only, no unwanted score if scoring separately; exact stable final state.]
  [No extra next-scene flash, title/caption, extra subject or repeated utterance.]
```

Times are intentions. Preserve the returned source, select actual complete shots
and native utterances, and record actual usable ranges. Do not treat nominal
timecodes as proof that the model obeyed cuts. Check the first useful take only
for concrete dependencies; keep independent work running. Use the existing local
cached actual-cut check and one brief final check, not a paid prompt grader,
automatic per-clip ASR, repeated contact-sheet audit or review-score wait.

## Worked 30-second example — original teaching passage, not a film request

The example dramatizes a small decisive repair. Its exact scene and characters
are invented for this guide. Replace them with the authorized film's bible; do
not reuse it as an automatic plot or spend a generation to test this document.

```text
S04-C02: KEEP THE WARNING LIGHT TURNING.
Narrative change: two lighthouse technicians discover that the cracked drive
coupling will not hold. Mara chooses to hand-turn the existing crank while Ivo
goes for the spare coupling. The failed part remains broken; no instant repair.

GLOBAL: grounded coastal thriller, 16:9 landscape, natural human speed and
tactile metal. Late afternoon storm outside, cool diffuse window light from the
west, one fixed warm service lamp over the gearbox. Same light through all cuts.

REFERENCES: image A = Mara identity only; image B = Ivo identity only;
image C = this gear-room map and machine geometry. Clean voice reference A,
if supported, guides Mara's established voice; no reference soundtrack copying.
Mara wears her established wet navy work jacket, left sleeve rolled once.
Ivo wears the established gray coveralls. Exactly these two people, no reflections
or background doubles. Use the film's original faces and natural skin texture.

MAP/STATE: machine north wall, window west wall, corridor door east wall.
Camera stays south of the Mara-machine axis. Mara is screen-left at the crank;
Ivo starts screen-right beside the open gearbox. Mara holds no other object.
Gearbox cover is already open. Coupling already has one visible crack. No new
crack or extra gear appears; nobody crosses the closed corridor door offscreen.
The cracked coupling connects only the electric motor to the lamp drive. The
existing manual crank connects to the lamp shaft downstream through a one-way
clutch; it can turn the lamp without repairing or driving the broken coupling.
Keep this same simple mechanical layout in every shot and the location anchor.

00:00–00:05 SHOT1: eye-level medium-wide from south, both people and open gearbox
visible. The electric drive rattles; Mara holds the stationary manual crank and
Ivo leans toward the sound. The crank does not rotate under motor power.
Short physical camera move closer, never changing side or object positions.
The warning-lamp mechanism stalls. HARD CUT.

00:05–00:10 SHOT2: stable close view of the already exposed cracked coupling
from the same side. The motor side slips without driving the lamp shaft, then
the motor stops; no disassembly, no hand enters the gears, no shape change.
This failed transmission explains the stopped automatic drive.
Mechanical sound continues in the same room. HARD CUT.

00:10–00:16 SHOT3: medium close Mara, camera south, Ivo just offscreen right.
She looks from the gearbox to Ivo, decides, and says once, urgently but naturally:
"Get the spare. I'll keep it turning." Allow a breath and Ivo's listening reaction
offscreen. Her hands stay at the crank below frame; no prop is invented. HARD CUT.

00:16–00:22 SHOT4: return to the established medium-wide. Mara resumes a steady
manual turn with both hands on the same crank. Ivo nods, moves to the east door,
opens it and exits into the corridor, with enough time for the complete crossing.
Camera remains south; Ivo's travel is toward screen-right. HARD CUT.

00:22–00:26 SHOT5: close view of Mara's hands and the existing crank rotating
normally. One uninterrupted turn, plausible resistance and contact, no speed-up.
The damaged coupling remains unrepaired; manual action drives the mechanism.
HARD CUT.

00:26–00:30 SHOT6: medium profile of Mara and the machine from the south side.
She maintains the turn; the existing indicator resumes its regular cycle.
Door remains open after Ivo's exit. Mara is alone, tense and working, not posing.
End during steady useful action; do not cut to the next corridor scene.

AUDIO: native synchronized single Mara line and hand/crank/gear sounds,
consistent muffled storm and room tone. No narrator, extra speech, music or choir.
Score will be laid continuously in the edit. Preserve full line and natural mouth
rest. No captions or labels. End state: Mara manually turning, Ivo outside this
room, door open, coupling still cracked, same weather/light and wardrobe.
```

This prompt allocates 5+5+6+6+4+4 = 30 seconds. It demonstrates shot coverage,
state carry and speech space, not a claim that a provider will obey perfectly.
If the two-action exit shot proves too complex, simplify its coverage or use a
motivated complete doorway shot within existing work; do not default to retries.

## Variation without drift

- **Dialogue turn:** shared geography, one speaker close enough for natural face
  performance, listener reaction, decision two-shot; keep the same exact line
  and voice. Let camera size change intentionally between shots, not within one
  supposedly locked angle.
- **Pursuit:** establish escape route and obstacle, show effort/contact, reveal
  consequence, show altered route. Maintain travel direction and barrier sides;
  do not alternate unrelated running views.
- **Discovery:** establish object/location, isolate clue, show recognition, take
  consequential action. A close-up must reveal new information; do not merely
  display a prop to the lens.
- **Epic reveal:** familiar foreground scale, eyeline or sound anticipation,
  wide revelation, human reaction and changed plan. Spectacle is connected to a
  decision; the same crowd/landmark/weather state persists across coverage.

Once the rules and references are frozen, later prompts reuse them and supply
only meaningful changes. Better continuity is a production goal, not a guarantee
or permission to add exhaustive checks that delay every film.

## Directed transitions across generated passages — owner correction, 3 November 2026

Write the outgoing attention/action and incoming response as one editorial idea
before generating either side. A nominal30second boundary is not a reason to cut.
Use a story stimulus → reaction → look/turn/move → new coverage when appropriate;
keep movement phase, gaze target, screen direction, object ownership and geography
consistent. Do not cut from a keeper turning away from a tank to already leaning
on its other side without a readable movement, time ellipsis or motivated cutaway.
Hold the useful reaction/action through completion and select actual returned
source ranges rather than mechanically appending whole generations.

Plan sound bridges when they improve immersion: a real approaching wave, call,
machine change or incoming radio line can pre-lap a relevant reaction (J-cut),
and an established sound or offscreen voice can continue over the next view
(L-cut). Maintain a coherent ambient bed and useful effect tails. These are
dramatic options, not mandatory effects on every cut, and they do not repair
wrong physical state or geography. Avoid arbitrary whooshes/dissolves.

For native speech, keep the original audio-picture offset whenever the mouth is
visible. If an incoming line starts offscreen, reveal its speaker at the matching
already-elapsed native picture time; do not restart that mouth take from its
beginning. Let an outgoing voice continue under a listener/appropriate view only
when that speaker is offscreen. Do not overlap conflicting visible speech or
time-stretch words to create a bridge. Put the intended bridge in existing
sequence metadata/prompt/edit notes; add no separate review gate.
