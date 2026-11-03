# Reliable, efficient AI vlog production

## Latest production speed and review preference — 2 November 2026

Apply [fast production for every video style](video-fast-production-preferences.md). The owner now prioritizes much faster completion with good-enough quality. This supersedes older exhaustive/repeated review instructions below: no default per-clip ASR, paid audiovisual review, every-join or frame-by-frame inspection, duplicate audits or cosmetic reroll loops. Use quick obvious-defect checks where a continuation depends on actual state, parallel independent sequences and one brief final batch check. Preserve the selected cast, story, meaningful continuity, style-specific sound/source rules, budget and accepted-job safeguards.

Saved at the owner's request on 1 November 2026. Aim for a substantially shorter production without increasing cost, weakening the creative or technical quality, or sacrificing reliability. Apply with `vlog-style-preferences.md`, `ai-style-first-pass-sop.md`, `ai-video-global-realism-preferences.md`, the cinematic pipeline and current user instructions. No method guarantees a speedup or a usable generation.

## Reduce repeated work

- Finish the complete causal script and one authoritative shot/state ledger, including camera ownership, prop continuity, time, weather, light and sound. Treat shorter summaries and prompts as views of that source; reconcile stale counts or assumptions rather than maintaining divergent copies.
- Identify reusable **scene-state anchor families**: identity, initial/final work stages, locations, practical props and essential reverse angles. Review each distinct state and neighboring required composition together. Reuse a genuinely matching, reviewed master or an accepted take's exact outgoing frame only when action phase, camera, light, weather, cast and physical state match. A shared master never proves that multiple generated takes are continuous.
- A fresh sample or scratch rebuild retains the owner's already selected character identity unless the owner explicitly changes the cast. Use the selected identity reference while creating fresh scene and footage assets; a workflow restart does not authorize silent recasting. Verify the resulting face and performance in motion.
- Avoid creating near-duplicate stills, speculative variants or an independent reference for every shot by default. Create a new image when the required subject, pose, geography or changed state is not already established; never reuse the wrong state merely to save time. Follow the current Kie-first image policy and actual production authorization. Keep original and rejected images for diagnosis.
- Prepare prompts, budget estimates, source research, image review, sound cues, technical render setup and QA templates concurrently when inputs are independent. Do not proceed with an unresolved safety, quality, cost or authorization gate.

## Qualify, then overlap independent work

- Complete first-pass readiness and make the hardest planned reusable production take first. Inspect actual full motion, performance, identity, physical action, camera turn, sound and the exact usable end frame before using it or creating dependent shots. An unreliable first take is a defect, not permission to skip quality or hide it.
- After prerequisites pass, submit already-planned, separately validated **independent** first-pass roots in small bounded parallel waves; two to four at a time is an initial operational range, not a proven fal concurrency limit. Inspect results promptly and adjust concurrency to actual queue, failures and review capacity. Do not initiate an unscreened batch of descendants. Output only from real footage, no still/freeze/repeat padding.
- Keep dependent generation serial: next-frame continuations, changed physical state, camera geography and same-host voice conditioning wait for the accepted predecessor and applicable review. The actual accepted take overrides the ideal plan. Review joins at normal speed and frame by frame as required.
- Overlap local conform, metadata, state checks and nonpaid QA with independent provider waits, without leaving audible playback running. Finish the brief essential story/audio/export check before delivery; inspect particular joins further only for a concrete fault or a required continuation dependency.

## Sequence-based preparation — owner direction, 2 November 2026

Freeze each sequence's dialogue, camera actions, voice/accent, environmental state
and cost envelope once. Reuse that reviewed direction for its production chunks;
do not repeatedly rewrite or research an unchanged shot. Keep actual returned
words and physical state authoritative. Assign independent sequences to separate
agents when delegation is authorized, and continue ready work without routine
approval waits already covered by the owner's scope.

Batch local transcription, source hashing, probes and frame sheets as takes
return; inspect actual performances and boundaries before dependent generation.
Batch audio comparison across takes rather than buying a separate assessment for
every clip. Overlap conform of selected footage with remaining independent work.
Use atomic append/locking for shared shot inputs as well as the budget, preserving
frozen job identities. These changes reduce repeated setup; they do not waive
reviews or establish a measured whole-film speed or reliability improvement.

## Spend and recovery controls

Use the user's actual budget and scope for each run. Diagnose defects and make justified targeted repairs within that authority; don't conceal faults, rerun blindly, exceed the cap or buy credits. Use a single shared reservation ledger with atomic locking, distinct take IDs, distinct output paths and duplicate-payload detection. Persist a pre-submit marker, accepted request identity and exact payload binding. Never replay unknown acceptance; reconcile first. Preserve accepted outputs. Bound concurrency to prevent budget races and stop new submissions if review falls behind, a prerequisite fails, pricing changes or an outcome is uncertain. A local ledger is not a provider-side hard spending limit and cannot see external account activity.

Record phase timestamps, queue/acceptance/completion, provider inference timings when available, review, corrections and final delivery. A local fake-provider simulation of 24 jobs with 0.1-second waits showed correct 1/4/8-worker bookkeeping in the glacier project, but did not measure real provider latency, audiovisual quality, end-to-end production or a live speedup. Compare only equivalent actual work and never promise speed or quality based on simulated timing.

## Measured opening-sample lessons — 2 November 2026

The first 15-second JFK turn take contained an unplanned foreground person and did not perform the case release or camera turn; its ASR-estimated dialogue occupied most of the take. The corrected 02A produced a roughly 9.7-second candidate with an initially held lead-in, so time the actual returned speech and action rather than assuming the prompt's nominal 15 seconds is fully usable. ASR and frame checks do not prove audible voice quality or lip sync.

A separate planned 02B continuation used the exact reviewed 02A outgoing frame, but still remained in selfie orientation and added unrequested speech. An exact-frame input and a split prompt are useful continuity controls, not proof that a model will perform a complex turn. Preserve both take receipts; do not spend on repeated blind prompt rerolls or represent a cut as a completed camera rotation. For an independently authorized sample, a motivated time/location cut may replace that particular attempted transition when the actual selected sample does not claim it occurred; it does not waive a requested physical turn in the full film.

Prepare unrelated valid requests and cue/QA plans while a prerequisite take is running, then submit only dependency-ready roots in guarded, budgeted waves after review and authorization. The project used a private input-upload helper and local timing/frame-sheet checks; reuse the verified helper where its exact input and provider contract match, keep access-bearing URLs and keys private, and preserve unique receipts. Batch cheap local technical checks and inspect output state before descendants. These observations are from a small number of takes, not an end-to-end speed benchmark or evidence that any full-film workflow is fastest.

For exact-frame H3 Turbo continuations, preserve the provider's native output
canvas through generation handoffs. In the glacier run, H3 768P returned
1344×768; a project guard's overly strict near-16:9 input check had forced a
1344×756 crop before each continuation. That changes framing and can contribute
to visible handoff differences. The project guard now accepts exactly the
observed 1344×768 Turbo canvas without changing its conservative reservation;
39 offline checks pass, including unchanged input bytes and continued rejection
of other unsupported ratios/Max inputs. This is input-preservation proof, not
proof that the model's next moving take remains stable. Perform final
aspect-preserving cover crop once consistently in the output conform, and
continue checking actual joins. Do not generalize an observed native canvas to
unverified providers or widen reference-pricing assumptions.

A 2 November 2026 native Turbo voice comparison found that the vague prompt “conversational English male voice” produced a higher-pitched, non-rhotic British-sounding take compared with the established American host. A targeted take explicitly specifying the selected accent and delivery was judged closer by an AI audio comparison; this is limited evidence, not human listening or a voice-clone guarantee. State and maintain the chosen character’s accent, articulation and delivery consistently in the dialogue direction; do not interpret this case as a universal preference for American accents. Inspect actual paired speech, voice and lip motion before propagating a take to descendants.
