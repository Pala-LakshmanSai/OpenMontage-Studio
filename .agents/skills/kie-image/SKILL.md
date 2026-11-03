---
name: kie-image
description: Generate or edit Nano Banana 2.1 images through Kie, with fixed model identity and safe task resume.
---

# Kie Nano Banana 2.1

Use registered `kie_image` after the pipeline assets director. Read `KIE_API_KEY`
from private .env. Use exact Kie model `nano-banana-2-1`, never Nano Banana 2 or Pro
as a silent substitute. Default 16:9, 1K, PNG for 720p/768P films. Use 2K only
for substantial crops or detail-critical shots; 4K only when justified. One
request produces one image. Check actual downloaded dimensions.

- `operation=credits` checks GET https://api.kie.ai/api/v1/chat/credit.
- `operation=generate`, prompt, output_path, optional reference_images (local
  paths or HTTPS URLs), resolution (1K/2K/4K), aspect_ratio and output_format.
  Local references must be JPEG/PNG/WebP and at most 30MB. Use a conservative
  maximum of 10: Kie's English market page says 10 while localized pages say 14.
  Do not assume the Google/fal limit applies to Kie.
- Local references upload via multipart POST
  https://kieai.redpandaai.co/api/file-stream-upload with file, uploadPath and a
  unique fileName. Preserve source files; uploads are temporary. Use returned
  data.downloadUrl in input.image_input, not filesystem paths.
- Authenticated requests use Bearer auth and reject redirects. Check JSON code
  equals 200 even when HTTP is 200. POST https://api.kie.ai/api/v1/jobs/createTask
  with {model:"nano-banana-2-1",input:{prompt,image_input,aspect_ratio,resolution,
  output_format}}. callBackUrl is optional; do not invent a callback service.
- Persist submitting marker/input hash before POST and taskId immediately on
  acceptance. GET /api/v1/jobs/recordInfo?taskId=... returns data.state:
  waiting/queuing/generating/success/fail. Verify task ID and model. On success,
  parse data.resultJson, download resultUrls without sending the key to the CDN,
  validate the image and save dimensions/SHA256. Retain all receipts locally.
- job_path defaults to output_path.kie-job.json. Resume accepted tasks with the
  same inputs/paths or task_id plus output_path/job_path. Unknown POST acceptance
  must reconcile Kie task history before any new generation; no automatic replay.
  For read-only status timeouts/429, wait as instructed and resume the same task;
  changing reference contents or accepted inputs is rejected.

Published 10 October 2026 quotes: 1K 4 credits/$0.02, 2K 6/$0.03, 4K 9/$0.045.
Recheck before spending. quoted_usd is an estimate; reported_credits is provider
task metadata when supplied. Balance differences may include concurrent use.

Use locked masters/state ledgers and compare adjoining anchors before animation.
Keep pose/contact/framing intact when editing; identity alone does not ensure
continuity. Extract the exact final usable video frame for same-shot extensions
instead of unnecessarily regenerating it. Review full image detail and references;
do not infer consistent faces/hands from a successful request.

Official sources:
- https://kie.ai/nano-banana-2-1
- https://docs.kie.ai/market/google/nanobanana-2-1
- https://docs.kie.ai/market/common/get-task-detail
- https://docs.kie.ai/cn/file-upload-api/upload-file-stream
- https://docs.kie.ai/common-api/get-account-credits
