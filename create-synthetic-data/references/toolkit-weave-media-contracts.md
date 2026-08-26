# Toolkit / Weave Media Contracts

Use this reference when synthetic data is meant to exercise Toolkit Button, Weave, Build-a-System, generated apps, or OpenCode app bundles with image, PDF, audio, video, realtime voice, or other file-like media.

## Prefer Local Contract Skills When Present

If the local machine has Toolkit or Weave sources, load the current contract skills before generating media fixtures. Treat local skill files as source-of-truth over this summary.

Search likely roots such as `/Volumes/git/toolkit`, `/Volumes/git/weave-agents`, the current repo, or a user-provided repo path. Do not assume the absolute path exists.

### Weave Generated-App Contracts

Load these from either:

- `template/.opencode/skills/...` in a Weave repo; or
- `apps/weave/backend/src/weave/template/.opencode/skills/...` in Toolkit.

Relevant files:

- `playground-media/SKILL.md`
- `playground-media/references/input-contracts.md`
- `playground-media/references/output-contracts.md`
- `playground-voice/SKILL.md`
- `multimodal/SKILL.md`
- `multimodal/references/core-media-contract.md`
- `multimodal/references/image-pdf.md`
- `multimodal/references/synthetic-media-benchmarks.md`

### Toolkit Button Render Skills

Load these from `apps/button/engine/opencode-workflow/.opencode/skills/...` when available:

- `rendering-images/SKILL.md` — realistic image artifacts, dimensions, variance, prompt patterns, and generated-image preference over PIL/canvas for photo-like evidence.
- `rendering-audio/SKILL.md` — real WAV/MP3 speech artifacts, duration requirements, TTS patterns, sidecars, and audio validation.
- `rendering-video/SKILL.md` — real MP4/WebM artifacts, duration/size requirements, video-generation patterns, and when OpenCV/slides are acceptable.
- `rendering-pdfs/SKILL.md` — PDF generation/rendering expectations when local Toolkit owns the benchmark environment.
- `reading-documents/SKILL.md` and `reading-documents/references/playground_upload_contract.md` — document upload contract and document-ingestion expectations.
- `playground-media/SKILL.md` and `playground-voice/SKILL.md` — Button-side generated-app UI/media behavior.

These render skills should be used as generation guidance, not copied into final source artifacts. If a worker lane will not have access to the Toolkit/Weave repo, copy only the needed `SKILL.md` or reference snippets into `planning/references/toolkit_weave_media_skills/` and record the source path and commit SHA in `qa_reports/helper_receipts.md`. Do not copy those references into `scenario_packs/*/inputs/` or evaluator-visible labels.

## Media Generation Routing

For Toolkit/Weave synthetic case packets:

- **Images:** use Toolkit `rendering-images` for benchmark quality requirements and Codex `imagegen` or the app-build `generate_image()` helper for realistic photo-like content. Do not let deterministic sketches, PIL drawings, charts, or photo-index rows count as final evidence photos unless the task explicitly tests sketches/charts.
- **Audio:** use Toolkit `rendering-audio` for TTS, duration, sidecars, and validation. A transcript JSONL is only a sidecar; include a playable `.wav`, `.mp3`, `.m4a`, or equivalent source file when audio is load-bearing.
- **Video:** use Toolkit `rendering-video` for MP4/WebM duration/size and prompt design. A storyboard or scene list is not video coverage; include playable video unless the modality is blocked and recorded as blocked.
- **PDF/documents:** use Weave `multimodal` + `playground-media` for upload/runtime contract, and use PDF/DOCX/XLSX helper skills for native containers and render checks.
- **Realtime voice:** use `playground-voice`. Do not substitute passive audio-file tests for live/realtime voice behavior; if live relay/mic is unavailable, mark that portion blocked or covered only by a mic-free bridge.

## Benchmark Fixture Shape

For generated-app benchmarks, media files are case-local sibling files:

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

`input.json` should refer to media by bare filename values, not paths and not runtime URI objects:

```json
{
  "request_pdf": "request_form.pdf",
  "site_photo": "site_photo_001.jpg",
  "call_recording": "call_recording.m4a"
}
```

Keep gold answers, expected evidence, labels, human E2E prompts, and failure-owner routing out of `metadata.json` and source media. Put them in `output.json`, `expected/`, `eval_sets/`, or other held-out reviewer artifacts.

## Live Runtime Payload Shape

For live generated app/API runs, file inputs use an object:

```json
{
  "inputs": {
    "media_file": {
      "uri": "data:image/png;base64,...",
      "fileName": "site_photo_001.png"
    }
  }
}
```

Supported URI schemes are only:

- `data:`
- `http://`
- `https://`
- `cm://`

Do not invent custom upload endpoints, multipart upload, custom media routes, or path-like fixture values for live runtime payloads.

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
- Browser UI should render upload previews inline: image via `<img>`, audio via `<audio controls>`, video via `<video controls>`, PDF via native `<iframe>`.
- Outputs should be schema-visible and rendered inline, not only download links.
- Large inline uploads must respect the generated-app request-content budget and surface a pre-submit warning rather than silently truncating or faking progress.
- Progress must distinguish local browser work from backend/executor work.

## Realtime Voice Boundary

Passive audio-file playback is a media fixture. Live speak-and-listen app behavior is a realtime voice contract:

- Use the local `playground-voice` skill when present.
- Validate mic-free voice through the text/tool bridge and transcript artifacts when microphone capture is unavailable.
- Do not claim microphone or audio-in e2e coverage if only transcript or typed-tool testing ran.
- A synthetic voice dataset should include real playable audio when the product ingests recordings; transcript/event JSONL is a sidecar, not the modality itself.
