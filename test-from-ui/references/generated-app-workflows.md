# Generated-App UI Validation

## Scope

Use this reference for generated apps and app-playground validation.

## Flow

1. Inspect the target repository's documented start command, app entry point, input contract, and runtime dependencies.
2. Start the existing documented environment or attach to an already running instance.
3. Open the generated-app page through the visible product entry point.
4. Select the target generated app when the product hosts more than one.
5. Read the app summary, evaluation status, and promised user journey.
6. Open the generated playground/runtime UI.
7. Confirm domain-specific controls exist; generic JSON/chat UI is not enough unless that is the intended product.
8. Use one built-in scenario/demo case to verify the happy path.
9. Use one fresh input, preferably generated with `create-synthetic-data`, to verify non-evaluation behavior.
10. Watch live progress/pipeline state and final rendered output.
11. Verify screenshots, console/network health, downloadable artifacts, citations/markers, and native file handling.

## Generated-App Failures

- Claimed modality missing from the generated UI.
- App falls back to transcript-first/preview mode when the PRD required live voice/realtime.
- Generated executor works via API but playground cannot drive it.
- UI posts a payload that does not match the target repository's current execution contract.
- Built-in evaluation cases pass but a fresh human-representative input fails.
- Output contains citations/markers but does not render them inline/clickable when required.

## Report

Include app id, tested URL and ports, scenario used, fresh input used, evaluation result if available, screenshots, and explicit pass/fail for the promised user journey.
