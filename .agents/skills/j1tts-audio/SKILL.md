---
name: j1tts-audio
description: Generate fixed-voice narration through J1TTS with durable acceptance and safe import/resume.
---

# J1TTS audio

Use registered `j1tts_audio` after the pipeline assets director. API contract is
grounded in VideoForge's published `apps/web/src/server/hosted/j1tts.ts`, source
49f0267f, and live readback. Host `https://api.j1tts.com`; authenticate with
`Authorization: Bearer <J1TTS_API_KEY>` loaded from private .env. Never log auth.

- `operation=voices`: GET /v1/voices and /v1/my-voices, each returns a list or
  {voices:[...]}. Use exact voice_id, name, tags, languages and preview_url.
- `operation=import`, voice_id and job_path: first check exact-ID availability;
  if missing, POST /v1/voices/import JSON {"voice_ids":"<ElevenLabs voice ID>"}.
  Re-read both catalogs. An already-imported or uncertain response can still mean
  success; reconcile exact ID rather than blindly importing again. Availability
  is provider/account-dependent; do not promise every ElevenLabs voice.
- `operation=tts`, text, voice_id, output_path, optional file_name: POST /v1/tts
  JSON {"text":"...","voice_id":"...","file_name":"unique-name"}. Persist
  the returned id before polling GET /v1/tts/{id}. When status=completed,
  authenticated GET /v1/tts/{id}/download writes the MP3. Failed is terminal.
  Do not invent model/speed/stability parameters absent the current contract.

Use job_path (default output_path.j1tts-job.json). Accepted IDs poll/download
without resubmission; timeout/crash without confirmed ID retains a no-replay
receipt. Resume original inputs or job_id plus original output/receipt paths.
Never mutate the payload of accepted work. Redirects are rejected; credentials
must not follow external URLs. Inspect actual audio with ffprobe/full decode,
transcription, playback and listening when supported. J1TTS is TTS, not a music,
SFX, lip-sync or video engine. This user reports an unlimited plan with $0
incremental narration cost; do not generalize that to another account.
