# Generic UI E2E Workflow

## Discovery

- Find the app start command from package scripts, README, Procfile, Docker compose, Makefile, or existing terminal state.
- Identify the user journey from product copy, issue/PR text, routes, screenshots, or acceptance criteria.
- Identify expected outputs and modalities before testing.

## Browser Journey

1. Open the app URL.
2. Authenticate only through supported local/dev auth paths.
3. Confirm the expected landing page and primary controls are visible.
4. Enter realistic data through visible fields.
5. Upload real files through file inputs/dropzones when supported.
6. Submit through the UI.
7. Wait for progress/completion using visible state, not arbitrary sleeps.
8. Inspect final rendered output and artifacts.
9. Capture screenshots for initial, input, running, result, and failure states.

## Health Checks

- Check console errors and failed network requests.
- Check no fatal overlays, hydration errors, or infinite loading states.
- Check keyboard/mouse-visible controls are usable.
- Check output can be copied/downloaded/opened when promised.

## Evidence Standard

A valid pass needs a visible UI journey plus evidence. Backend `200`, API success, or logs alone are not enough.
