---
name: test-from-ui
description: Validate web apps through realistic browser UI journeys, either as a fast early smoke test that exposes the first real user-flow blocker or as final acceptance proof with screenshots and console/network evidence. Use when asked to run an e2e, test an app from the UI, verify a generated app, check a multimodal/file/citation workflow, or prove a frontend works beyond API-level checks.
---

# Test From UI

## Core Rule

Prove behavior from the visible product surface. API calls, logs, database reads, and direct backend requests are useful for setup and diagnosis, but they do not replace a real browser journey through the UI.

Load references only as needed:

- [generic-ui-e2e.md](references/generic-ui-e2e.md): default repo-agnostic UI validation workflow.
- [toolkit-build-a-system.md](references/toolkit-build-a-system.md): Toolkit / Build-a-System / Weave generated-app validation.
- [native-file-inputs.md](references/native-file-inputs.md): native PDF/DOCX/XLSX/media test-data rules.

If realistic native files are missing, use the sibling `create-synthetic-data` skill to create them. Keep expected labels/answer keys out of files uploaded to the app.

## Validation Modes

Choose one mode before testing:

- `early_smoke`: obtain the fastest high-signal result from the shortest complete
  user journey. Incomplete behavior and an honest failure are acceptable
  outcomes. Start the real app, use realistic minimal input, stop after the
  first decision-bearing blocker is captured, and report it immediately. Do not
  wait for unit tests, broad suites, polish, or general independent review.
- `final_proof`: validate the accepted complete journey for delivery or PR
  readiness. Exercise required paths, inspect output and browser health, capture
  final evidence, and return an explicit pass/fail verdict.

Under an auto-planner, use `early_smoke` during `user_flow_probe` and
`final_proof` during `pr_hardening`. Early-smoke evidence is a feedback artifact,
not acceptance proof, and must be labeled as such.

## Workflow

1. **Discover the app contract.** Identify start commands, target URL, auth needs, primary user journey, claimed modalities, expected outputs, and success criteria.
2. **Start or attach to the app.** Prefer existing dev servers when present. If starting services, record commands, ports, env assumptions, and logs.
3. **Prepare realistic inputs.** Use native files for claimed file modalities. Do not replace PDFs/DOCX/XLSX/images/audio/video with pasted text unless the app explicitly only supports text.
4. **Drive the visible UI.** Click, type, upload, submit, wait for progress, inspect rendered output, and exercise the intended user journey.
5. **Inspect browser health.** Capture console errors, failed network requests, stuck loading states, disabled controls, fallback banners, and missing expected UI affordances.
6. **Verify the actual output.** Confirm rendered output satisfies the product promise: correct fields, citations, artifacts, downloads, media playback, inline markers, tables, charts, or whatever the app claims to produce.
7. **Test at least one fresh input.** If demo scenarios exist, use one for a sanity path, then test one non-demo/non-benchmark input when practical.
8. **Capture evidence.** Save screenshots for initial state, input setup, running/progress state, final rendered output, and any failure.
9. **Report pass/fail.** State exact URLs, inputs used, screenshots, observed output, console/network issues, and whether each requirement passed, failed, or is blocked.

In `early_smoke`, perform only the smallest subset needed to reach the first
real result or blocker: discover the shortest journey, start the app, use one
representative input, drive the visible UI, inspect console/network health, and
capture the result. Do not expand into exhaustive variants after the decision is
clear. In `final_proof`, complete all applicable workflow steps.

## Hard Failures

Treat these as failures or blockers, not soft passes:

- expected modality missing from the UI;
- app claims native file support but only accepts pasted text;
- file upload succeeds visually but output does not use file contents;
- voice/realtime/image/citation/document features are replaced by preview/fallback mode without explicit user acceptance;
- final state is raw JSON when the user journey requires a rendered human UI;
- citations/markers are present as text but not clickable/rendered as required;
- generated artifacts are named but not downloadable/openable;
- console/runtime errors affect the journey;
- only API/backend tests pass while the visible UI cannot complete the journey.

## Synthetic Data Use

When the app needs realistic files or records, call `create-synthetic-data` from the adjacent skills directory. Require:

- real native file formats for the UI upload path;
- realistic length and structure, not one-paragraph toy content;
- planted facts that the UI output can be checked against;
- separate tester-only expectations/labels that are never uploaded to the app;
- validation with `create-synthetic-data/scripts/validate_synthetic_output.py` when packaging a corpus.

## Final Response Shape

Keep the final report concise:

- **Verdict:** pass, fail, or blocked.
- **URL / App:** page tested and runtime ports if relevant.
- **Inputs:** files/scenarios used, noting native formats.
- **Evidence:** screenshots and key observations.
- **Failures:** exact missing controls, console/network errors, output mismatches.
- **Next step:** smallest fix or retest action.
