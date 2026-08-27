# Generated-App Media Contracts

Use this reference when synthetic data is meant to exercise a generated app or app bundle with image, PDF, audio, video, realtime voice, or other file-like media.

## Prefer Local Contract Skills When Present

Load the target repository's current contract skills before generating media fixtures. Treat repository-native contracts as source-of-truth over this summary.

Search the current workspace and user-provided repository paths. Do not assume a product name, checkout location, route, schema, or runtime exists.

### Generated-App Contracts

Load these from either:

- the target repository's documented shared skill root; or
- an app template's repository-relative skill root.

Relevant files:

- `playground-media/SKILL.md`
- `playground-media/references/input-contracts.md`
- `playground-media/references/output-contracts.md`
- `playground-voice/SKILL.md`
- `multimodal/SKILL.md`
- `multimodal/references/core-media-contract.md`
- `multimodal/references/image-pdf.md`
- `multimodal/references/synthetic-media-benchmarks.md`

### Render Skills

Load the equivalent repository-native skills when available:

- `rendering-images/SKILL.md` — realistic image artifacts, dimensions, variance, prompt patterns, and generated-image preference over PIL/canvas for photo-like evidence.
- `rendering-audio/SKILL.md` — real WAV/MP3 speech artifacts, duration requirements, TTS patterns, sidecars, and audio validation.
- `rendering-video/SKILL.md` — real MP4/WebM artifacts, duration/size requirements, video-generation patterns, and when OpenCV/slides are acceptable.
- `rendering-pdfs/SKILL.md` — PDF generation/rendering expectations for the target evaluation environment.
- `reading-documents/SKILL.md` and `reading-documents/references/playground_upload_contract.md` — document upload contract and document-ingestion expectations.
- `playground-media/SKILL.md` and `playground-voice/SKILL.md` — generated-app UI/media behavior.

These render skills should be used as generation guidance, not copied into final source artifacts. If a worker lane will not have access to the target repository, copy only the needed `SKILL.md` or reference snippets into a task-local planning reference folder and record the source path and commit SHA in `qa_reports/helper_receipts.md`. Do not copy those references into `scenario_packs/*/inputs/` or evaluator-visible labels.

## Media Generation Routing

For generated-app synthetic case packets:

- **Images:** use a repository-native image contract when available and `imagegen` or another selected image helper for realistic photo-like content. Do not let deterministic sketches, drawings, charts, or photo-index rows count as final evidence photos unless the task explicitly tests them.
- **Audio:** use the selected audio helper for speech generation, duration, sidecars, and validation. A transcript JSONL is only a sidecar; include a playable `.wav`, `.mp3`, `.m4a`, or equivalent source file when audio is load-bearing.
- **Video:** use the selected video helper for duration, container, size, and prompt requirements. A storyboard or scene list is not video coverage; include playable video unless the modality is blocked and recorded as blocked.
- **PDF/documents:** use repository-native multimodal and playground contracts when present, and use PDF/DOCX/XLSX helper skills for native containers and render checks.
- **Realtime voice:** use `playground-voice`. Do not substitute passive audio-file tests for live/realtime voice behavior; if live relay/mic is unavailable, mark that portion blocked or covered only by a mic-free bridge.

## Fixture Shape

First read the target repository's evaluation loader and existing fixtures. Match
its filenames, directories, and reference shape exactly. When that contract uses
case-local sibling files, a fixture may look like:

```text
cases/case_1/
  input.json
  output.json
  metadata.json
  request_form.pdf
  clinical_record.pdf
  site_photo_001.jpg
  call_recording.m4a
```

In that kind of repository, `input.json` may refer to media by bare filename
values:

```json
{
  "request_pdf": "request_form.pdf",
  "site_photo": "site_photo_001.jpg",
  "call_recording": "call_recording.m4a"
}
```

This is an example, not a portable schema requirement. Do not impose sibling
files, these field names, or this directory layout on a repository with a
different native contract.

Keep gold answers, expected evidence, labels, human E2E prompts, and
failure-owner routing out of source media and source-facing metadata. Store them
only in the target repository's held-out evaluation surface.

## Live Runtime Payload Shape

Read the current frontend serializer, backend input schema, and a working live
request before constructing runtime inputs. Preserve the repository's native
file object, URI, upload, and metadata conventions. Do not infer the live
payload from an evaluation fixture, invent upload endpoints or URI schemes, or
reuse a path-like fixture value unless the runtime contract explicitly accepts
it.

## Media Grounding Requirements

When a benchmark is meant to test media perception, the answer must be derivable from the actual media, not from filenames, prompt text, surrounding metadata, or labels.

Use these design checks:

- The decisive fact is visible/audible/readable only inside the uploaded media.
- At least one distractor or contradiction case separates media-grounded reasoning from text-only guessing when useful.
- The output schema or held-out expected answer contains resolvable evidence: source file, page/frame/timestamp/section, and the perceived fact.
- For PDFs/documents, prefer extraction-first plus rendered-page/vision fallback behavior; do not require raw PDF SDK file parts.
- For policy/governing-document apps, require section/page citations when answers derive from governing text.

## UI / E2E Implications

When a generated app accepts media:

- Inputs should preserve MIME, filename, size/representation, and common subtype variance.
- Browser UI should render the repository's supported previews or players inline rather than hiding accepted media after upload.
- Outputs should be schema-visible and rendered inline, not only download links.
- Large inline uploads must respect the generated-app request-content budget and surface a pre-submit warning rather than silently truncating or faking progress.
- Progress must distinguish local browser work from backend/executor work.

## Realtime Voice Boundary

Passive audio-file playback is a media fixture. Live speak-and-listen app behavior is a realtime voice contract:

- Use the local `playground-voice` skill when present.
- Validate mic-free voice through the text/tool bridge and transcript artifacts when microphone capture is unavailable.
- Do not claim microphone or audio-in e2e coverage if only transcript or typed-tool testing ran.
- A synthetic voice dataset should include real playable audio when the product ingests recordings; transcript/event JSONL is a sidecar, not the modality itself.
