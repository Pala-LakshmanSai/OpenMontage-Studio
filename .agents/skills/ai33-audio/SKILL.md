---
name: ai33-audio
description: Generate fixed-voice speech, sound effects and instrumental music through the AI33 audio adapter; safely resume paid tasks.
---

# AI33 audio

Use the registry tool `ai33_audio`; read the assets director skill first. Official API source: https://ai33.pro/app/api-document, verified 2026-10-10.

Credentials: local `AI33_API_KEY` only. The adapter sends `xi-api-key`; never put credentials in inputs, prompts, receipts, logs or Pages.

Input: `operation` (`tts`, `sfx`, `music`) and explicit `output_path` under the production project. Each output also has a durable `.ai33-job.json` receipt. Set `job_path` to override it. `poll_timeout` defaults 900 seconds, `poll_interval` 3 seconds.

- TTS: `text`, provider-prefixed `voice_id`, optional `speed` 0.5–1.5 (default 1), `with_transcript` (default false). Multipart `/v3/text-to-speech`. Keep one voice per character. Voice descriptions were verified through read-only `GET /v3/voices?provider=elevenlabs&language=English&accent=American`. Restrained American dialogue candidates: Sarah `elevenlabs_EXAVITQu4vr4xnSDxMaL`, Eric `elevenlabs_cjVigY5qzO86Huf0OWal`, Chris `elevenlabs_iP95p4xoKVk53GoZ742B`. Audition actual output; catalog labels are not performance proof.
- SFX: `text` <=450 characters, optional `duration_seconds` null or 0.5–30, `prompt_influence` 0–1 (default 0.3), `loop` (default false). JSON `/v1/task/sound-effect`, model `eleven_text_to_sound_v2`. Auto duration costs 200 credits; specified duration costs 50 credits per second, minimum 50. Ask for clean isolated stems, no music/no speech where appropriate. Looping ambience supports continuous edits; Foley needs clean tails. One 30-second bed costs 1500 credits.
- Music: `prompt` <=500 characters, `instrumental` true by default, optional `track_index` default 0. Simple-mode Suno `/v1s/task/music-generation`. Provider chooses model version; do not claim specific Suno version before result evidence. May return two longer tracks; choose one and edit locally. There is no verified fixed USD or credit tariff in the public audio API documentation.

All submissions return task ids; `GET /v1/task/{id}` uses `doing`, `done`, `error`. Polls and downloads can resume. Call with `job_id`, same `operation` and `output_path` to resume without generation fields, or repeat original inputs with the same receipt path. Never change the payload against an accepted receipt.

A timeout/crash while submitting leaves `status: submitting` without a task id. **Do not delete this receipt or replay the POST**. Reconcile provider task history first. Known task ids always poll; no paid submission retries exist. Errors retain receipt/job metadata, not raw provider error bodies. `cost_usd` is unknown (`None`); actual credit cost is retained when returned by polling. Do not record credits as USD.

Finish with a continuous sound scene: consistent voice EQ/acoustics, ambience bridging picture cuts, effects beginning before appropriate visual reveals, music shaped around dialogue and action. These APIs generate stems; the audio mixer owns timing, crossfades, levels and final loudness. The adapter does not perform lip-sync.
