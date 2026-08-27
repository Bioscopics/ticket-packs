# Modality Helper Skills

Use this reference when synthetic data needs real modality artifacts: images, PDFs, DOCX, spreadsheets, audio, video, screenshots, citations, or UI upload tests.

## Core Rule

Do not fake a modality with a description of that modality.

If the target app claims image support, create actual image files. If it claims audio or video support, create actual media files. If it claims document or spreadsheet support, create real native containers. Indexes, captions, transcripts, JSON metadata, and file manifests are useful sidecars, but they do not replace the uploadable artifact.

The parent synthetic-data skill is the orchestrator, not the default renderer. When a specialist helper exists, that helper owns generation and modality-specific validation.

## Capability Discovery Gate

Before planning native/media artifacts:

1. Inspect the available skill catalog.
2. Search local product/runtime skill roots, including the current workspace, `$CODEX_HOME/skills`, and any user-provided repositories. Prefer portable paths such as:
   - `<workspace>/.agents/skills/`
   - `<workspace>/.opencode/skills/`
   - `<workspace>/template/.opencode/skills/`
   - `<workspace>/apps/*/.opencode/skills/`
   - `$CODEX_HOME/plugins/cache/*/skills/`
3. Select one execution owner and any supporting contract skills for each modality.
4. Read every selected helper `SKILL.md` completely before generation.
5. Write `planning/modality_execution_matrix.json` before dispatching generators.

Selection order:

1. user-specified or target-runtime contract skill;
2. canonical local product skill (`rendering-*`, `multimodal`, `playground-*`);
3. installed system helper (`imagegen`, `pdf`, `documents`, `Spreadsheets`, `Presentations`, `test-from-ui`);
4. a documented generic tool only when no specialist skill exists and the downgrade is explicit.

For PDFs, prefer the active primary-runtime `handle_pdfs/SKILL.md` under `$CODEX_HOME/plugins/cache/openai-primary-runtime/pdf/<active-version>/skills/` when present. It is coupled to the bundled ReportLab, pypdf/pdfplumber, and Poppler runtime and requires render-and-recheck validation. Use the personal `$CODEX_HOME/skills/pdf/SKILL.md` only as a fallback or supporting contract when the primary-runtime helper is unavailable. Resolve the active version at runtime; do not hard-code a stale cache version into the parent skill.

Do not copy stale helper instructions into the parent skill. Record a portable selected-helper path (`$CODEX_HOME/...`, `$WORKSPACE/...`, or repository-relative) and source commit when available so the worker reads current source-of-truth instructions. Put fully resolved local paths in local-only receipts, not a shareable matrix.

A helper does not need to be registered in the current session's skill catalog to be usable. If its filesystem-backed `SKILL.md` exists within the user-provided workspace or local product repos, read it directly and follow it. Resolve referenced scripts/imports from the helper's owning repo. Do not ask for permission merely to read or use an in-scope local skill. Distinguish:

- `available`: helper and required runtime are usable;
- `available_runtime_blocked`: helper exists, but a required executable, service, credential, or model endpoint is unavailable;
- `unavailable`: no suitable helper skill exists after catalog and filesystem discovery.

Store this as `availability`. Keep `status: "planned"` during planning; change `status` to `complete`, `blocked`, or `downgraded` at delivery. Only the second and third availability states justify a blocked/downgraded modality. A missing catalog registration by itself does not.

Use the canonical detector keys for `modality`: `image`, `audio`, `video`, `pdf`, `document`, `spreadsheet`, or `presentation`. Put subtypes such as digital PDF, scanned PDF, AP ledger, or payment-history workbook in `applies_to_families`; do not invent subtype modality keys that the contract auditor cannot match.

Minimum matrix shape:

```json
{
  "schema_version": 1,
  "modalities": [
    {
      "modality": "image",
      "required": true,
      "execution_owner": "imagegen",
      "supporting_skills": ["rendering-images", "test-from-ui"],
      "skill_paths": ["$CODEX_HOME/skills/.system/imagegen/SKILL.md"],
      "availability": "available",
      "calibration_source_ids": ["SRC-001"],
      "generation_method": "<method>",
      "runtime_dependencies": ["<executable, import, service, or credential>"],
      "validation": ["file signature", "dimensions", "visual inspection"],
      "receipt_path": "qa_reports/helper_receipts/image.md",
      "status": "planned"
    }
  ]
}
```

After writing the planning matrix and before dispatching generators, run:

```bash
set -o pipefail
python3 scripts/audit_calibration_contract.py <output_dir> --phase planning \
  | tee <output_dir>/qa_reports/helper_receipts/calibration_planning.md
```

Before delivery, update statuses and receipts, then run the default delivery audit:

```bash
python3 scripts/audit_calibration_contract.py <output_dir>
```

For `status: "downgraded"`, include a `deviation` object with non-empty `reason`, `impact`, and `approval`. Record original and emitted containers when the downgrade changes file type. A downgrade is never an implicit convenience choice.

For exact-container requirements such as legacy `.xls` or Outlook `.msg`, first check the specialist helper, a sanctioned conversion path, and the target consumer's accepted formats. If exact output remains unavailable, record the downgrade and obtain user or locked-contract approval before generation; otherwise mark the modality blocked.

## Helper Skill Routing

Load and use helper skills when available:

- `imagegen`: create or refine realistic raster image evidence, screenshots, product photos, site photos, document photos, or visual variants.
- primary-runtime `handle_pdfs` / `pdf`: create and visually verify PDFs, render pages, inspect layout-sensitive PDFs, and re-render after every meaningful layout repair.
- `documents`: create and visually verify DOCX/Word-style artifacts with realistic formatting.
- `Spreadsheets`: create and visually verify native XLSX/XLS workbooks, plus CSV exports when the domain uses exports.
- `test-from-ui`: validate that generated files actually work through a visible app upload/UI journey.
- Repository-local media skills, when present: use applicable `rendering-*`, document-reading, playground, voice, or multimodal skills before inventing ad hoc media-generation rules for generated-app evaluations.
- `Presentations`: create and render-check PPTX/slide artifacts when the real-example profile includes presentations.

For realistic benchmark media, use paired ownership:

- **Images:** `imagegen` owns bitmap generation/editing; a repository-native image contract may add evaluation dimensions, variance, prompt, and artifact quality gates.
- **Audio files:** `rendering-audio` owns speech/audio generation, duration, sidecars, and waveform/container checks.
- **Video files:** `rendering-video` owns realistic motion generation, duration/size, prompts, transcripts/keyframes, and playback checks.
- **PDF/DOCX/XLSX/PPTX:** the matching native artifact skill owns container creation and render/visual QA; product `rendering-*` skills add benchmark-specific requirements.
- **Generated-app runtime/UI:** repository-native multimodal, playground, and voice skills own fixture, payload, upload, preview, realtime, and E2E contracts when present.

Prefer the target repository's canonical shared helpers over copies embedded in generated app folders. Record the selected repository-relative path and source commit when available.

If a needed helper skill or media generator is unavailable, say so in the QA report and either generate the best real container available or mark that modality as blocked. Do not silently ship a text stand-in while claiming modality coverage.

Record a helper receipt for every claimed modality: selected skill name/path, source commit when available, calibration source IDs, generation prompt/method, final artifact paths, validation commands/results, visual/playback findings, and any blocked or downgraded capability. Put receipts under `qa_reports/helper_receipts/` or the case-level held-out metadata.

When using `imagegen`, follow the `imagegen` skill's execution policy. Use its built-in path when exposed. If the built-in path is unavailable, use the CLI/API fallback only when the current user request explicitly authorizes image-model/API fallback or when the operator has provided that permission in the task. If fallback is not authorized, mark realistic image generation blocked/downgraded; do not substitute a deterministic sketch and call it final photo evidence.

When CLI/API fallback is authorized, use the installed imagegen script rather than writing a one-off API runner:

```bash
export CODEX_HOME="${CODEX_HOME:-$HOME/.codex}"
export IMAGE_GEN="$CODEX_HOME/skills/.system/imagegen/scripts/image_gen.py"
PYTHON_BIN="$(command -v python3 || command -v python)"
"$PYTHON_BIN" "$IMAGE_GEN" generate \
  --prompt "<realistic documentary/photo evidence prompt>" \
  --use-case photorealistic-natural \
  --style "realistic documentary field photo" \
  --constraints "no labels, no arrows, no watermark, no text overlay; fictional/synthetic scene only" \
  --quality medium \
  --size 1536x1024 \
  --out "<case inputs path>/<photo_id>.png"
```

Record the exact command or prompt, model path, output path, and `file` validation result in a helper receipt. If the command fails, keep the failure in QA and mark realistic image generation blocked; do not replace it with a cartoon final.

## Generated-App Contract

When the synthetic data is for a generated app, also read `generated-app-media-contracts.md`. If repository-native contract skills exist, load them as source-of-truth:

- `playground-media` for upload previews, runtime input payloads, output rendering, and UI smoke expectations;
- `playground-voice` for realtime voice app contracts and mic-free validation boundaries;
- `multimodal` references for media benchmark fixture shape, PDF/image runtime behavior, and media-grounding checks.
- applicable repository-native render skills for image/audio/video/PDF/document artifact quality bars and validation commands.

For generated-app evaluations, follow the target repository's current fixture
loader exactly. If it uses case-local sibling files and bare filenames, preserve
that shape; if it uses another representation, do not replace it with a
remembered product contract. Never copy a live runtime payload shape into an
evaluation fixture without repository evidence that both contracts are the same.

## Image Evidence

For realistic photo/image artifacts:

- Use `imagegen` when a drawn, diagrammatic, or synthetic-looking image should become a realistic photo-like asset.
- A rough sketch, map, diagram, synthetic render, or low-quality generated image can be a seed/reference. Prompt the image model to make it look like a realistic documentary/site/photo artifact while preserving the scene facts.
- Treat rough visuals as intermediate references, not final evidence, unless the test explicitly targets hand-drawn/sketch input. If the user expects realistic evidence, run a seed-to-realism pass through `imagegen` and save the realistic output as the uploadable file.
- If `imagegen` or an equivalent realistic-image generator is unavailable, mark realistic photo generation as blocked or downgraded in QA. You may include a rough visual as `rough_reference`, but do not count deterministic drawings, PIL/canvas renderings, clip art, or sketches as final realistic photo evidence.
- If public or third-party source imagery is used instead of generated imagery, use only material with explicit compatible licensing or permission, record source/license/provenance, and do not imply it depicts the fictional case. Prefer generated or synthetic images for privacy-sensitive case packets.
- Save the final `.jpg`/`.png` in `inputs/`, not just a workbook row or photo index.
- Keep labels, expected findings, and scoring facts in sidecar metadata or held-out expected files, not burned into the image unless the app is meant to read visual annotations.
- Use filenames and sidecars that match the case lifecycle: photo IDs, dates, source actor, location, and relationship to estimates/reports.

Useful imagegen prompt shape:

```text
Use the attached rough/synthetic scene only as factual composition reference.
Create a realistic documentary evidence photo of the same scene: <domain-specific scene>.
Preserve: <critical facts to keep>.
Remove: cartoon styling, labels, arrows, UI chrome, and synthetic annotation overlays unless requested.
Style: natural lighting, realistic camera perspective, plausible lens, normal field-photo imperfections.
Output should look like an uploadable case/photo artifact, not concept art.
```

For damage, inspection, medical, insurance, legal, real-estate, or field-work cases, reject images that look like cartoons, MS Paint diagrams, clip art, iconography, or presentation illustrations unless that exact artifact type is part of the case packet. A photo-index spreadsheet is not enough; include the corresponding image files.

## Audio And Video

For voice, call, meeting, dashcam, inspection, walkthrough, or realtime-agent outputs:

- Use real media containers such as `.wav`, `.mp3`, `.m4a`, `.mp4`, or `.mov` when the product will ingest media.
- Use realistic media when the modality is load-bearing: audio waveform or playable video first, transcript/summary second. A realtime voice transcript, call log, or storyboard can seed the media plan, but it does not satisfy audio/video coverage without a playable file.
- Include transcripts, speaker labels, timestamps, and metadata as sidecars, but do not substitute them for media.
- Validate with `file`, `ffprobe`/`ffmpeg` when available, duration checks, and a small playback/extraction smoke test when practical.
- For noisy media, document the intended imperfection: background noise, crosstalk, clipping, codec artifacts, partial recording, off-camera speech, or dropped frames.
- If media generation is outside available tools, write a blocked QA note instead of claiming audio/video coverage.

Examples of acceptable sidecar-plus-media pairs:

- `inputs/claim_call_2026-04-18.m4a` plus `inputs/claim_call_2026-04-18.transcript.json`;
- `inputs/site_walkthrough_2026-05-02.mov` plus `inputs/site_walkthrough_2026-05-02.scene_notes.md`;
- `inputs/realtime_agent_session_001.wav` plus `inputs/realtime_agent_session_001.events.jsonl`.

## Native Documents And Spreadsheets

Use helper skills for native documents when quality matters:

- Use the active primary-runtime `handle_pdfs` skill for generated PDFs when available, with `pdf` as fallback/support. Render a representative pilot before bulk generation, then run every-page density/blank checks and visually inspect the required page families.
- Use `documents` for DOCX when formatting, comments, headers/footers, tables, or review artifacts matter.
- Use `Spreadsheets` for XLSX/XLS when the task says spreadsheet, workbook, Excel, sheet, formulas, multiple sheets, hidden rows, formatting, or visual workbook fidelity. CSV is an export/log format, not a substitute for a native spreadsheet claim. Include CSV only as an additional export when useful.

Do not produce `.docx`, `.xlsx`, `.pdf`, `.mov`, `.mp4`, `.mp3`, or image extensions that are renamed text files.

## Modality QA

Before shipping a multimodal dataset:

- run `file` or equivalent signature checks for every native/media artifact;
- render or visually inspect representative images/PDF/DOCX/spreadsheet pages;
- for generated clean or layout-sensitive PDFs, run `scripts/audit_pdf_layout.py <output_dir> --strict`; repair repeated under-filled continuation pages even when page count and text extraction pass;
- record media duration/codec for audio/video;
- include helper receipts for image/PDF/DOCX/spreadsheet/audio/video generation or blocked status;
- confirm sidecars point to existing files;
- confirm source artifacts are separate from held-out labels and expected outputs;
- test at least one app upload path with `test-from-ui` when a UI is available.
