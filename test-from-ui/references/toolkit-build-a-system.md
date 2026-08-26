# Toolkit / Build-a-System / Weave UI Validation

## Scope

Use this reference for Toolkit Button Build-a-System, Weave generated apps, and app playground validation.

## Flow

1. Start Toolkit/Weave or attach to the running devbox/local stack.
2. Open `/weave` or the generated app page.
3. Select the target generated app.
4. Read the app summary, benchmark status, and user journey.
5. Open the generated playground/runtime UI.
6. Confirm domain-specific controls exist; generic JSON/chat UI is not enough unless that is the intended product.
7. Use one built-in scenario/demo case to verify the happy path.
8. Use one fresh input, preferably generated with `create-synthetic-data`, to verify non-benchmark behavior.
9. Watch live progress/pipeline state and final rendered output.
10. Verify screenshots, console/network health, downloadable artifacts, citations/markers, and native file handling.

## BAS-Specific Failures

- Claimed modality missing from the generated UI.
- App falls back to transcript-first/preview mode when the PRD required live voice/realtime.
- Generated executor works via API but playground cannot drive it.
- UI posts the wrong schema shape to `/v1/executions` or `/v1/executions-sync`.
- Benchmark cases pass but a fresh human-representative input fails.
- Output contains citations/markers but does not render them inline/clickable when required.

## Report

Include app id, frontend/backend ports, scenario used, fresh input used, benchmark score if available, screenshots, and explicit pass/fail for the promised user journey.
