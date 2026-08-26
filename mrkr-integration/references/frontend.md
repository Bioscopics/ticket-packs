# Clickable Citation Frontend

Extend the existing answer renderer. Do not replace the page or import another
product's design system.

When the host has no citation renderer, adapt the tested fallback under
`assets/react/` as described in
[reference-assets.md](reference-assets.md). Preserve its parser and resolver
rules while replacing its visual primitives with the host design system.

## Rendering contract

- Receive sanitized MRKR-bearing content plus the backend-built citation
  bundle in the normal API response.
- Parse only the exact canonical marker form. Prefer a shared parser supplied
  by the target codebase; otherwise mirror the package's canonical pattern in a
  small tested client parser.
- Replace each resolved marker with an inline accessible citation control.
- Use only the citation bundle for labels, snippets, and resolver targets.
- Never create a clickable target from model text.
- Remove or render a neutral unavailable state for unresolved tokens; raw MRKR
  syntax must not leak into normal UI.

## Host-native interaction

Reuse existing rich-text/Markdown components, buttons, popovers, dialogs,
drawers, document viewers, routing, and theme tokens. A citation control should:

- be keyboard reachable and have an accessible name such as "Open citation:
  Service manual";
- visually read as a source reference, not a warning or primary command;
- open the source detail in the application's established modal/drawer pattern;
- show source title, directly supporting excerpt/anchor, and source location;
- offer "open source" only when an authorized resolver exists;
- preserve focus and work on narrow/mobile layouts.

Reserve warning/error colors for actual warning/error states. Citation bubbles
or badges should use neutral or informational tokens unless the citation is
invalid or unavailable.

## Streaming and structured output

During streaming, avoid treating an incomplete marker token as final content.
Buffer or defer parsing until a complete token is available. Final rendering
must use the sanitized server result, not an optimistic client interpretation.

For structured results, render citations only in fields declared MRKR-bearing.
Do not recursively rewrite arbitrary object keys, identifiers, code, or binary
artifact references.

## Documents and exports

If the product exports DOCX/PDF/HTML, preserve the existing export workflow.
Choose one explicit behavior:

- convert verified MRKRs to the export format's native footnotes/endnotes or
  source links; or
- retain canonical MRKRs in the stored text and render them only in the app.

Do not silently drop citations from an executive-facing export when citations
are part of the product contract.

## UI acceptance

Test through the real UI:

1. submit representative evidence;
2. receive a grounded response with at least two distinct citations;
3. open each citation by mouse and keyboard;
4. verify source title/excerpt and authorized source navigation;
5. verify malformed/unknown markers are not clickable or exposed raw;
6. verify loading, no-source, provider-error, and revoked-source states;
7. verify follow-up output resolves only current-turn citations.
