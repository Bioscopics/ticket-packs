# MRKR Integration Review Checklist

## 1. Workflow preservation

- The original user journey, state machine, model/agent, tools, business rules,
  deterministic decisions, and artifacts remain unchanged except for additive
  citation behavior.
- The implementation did not add a parallel agent, orchestration path, storage
  system, or UI architecture without explicit scope.
- Memo, chat, decision, batch, and workbench archetypes retain their native
  interaction pattern.

## 2. Package ownership

- Direct importers declare the `distylai-mrkr` distribution.
- Product code imports public `mrkr` APIs rather than cloning marker creation,
  extraction, or scrubbing.
- Canonical syntax is exact: `【mrkr: ||label|| deadbeef】`.
- IDs are package-generated opaque tokens, never URL/file hashes, counters, or
  model-created values.
- Installed API/version is feature-checked and deployment uses approved package
  distribution/pinning.
- The compatibility receipt matches the tested Python/package version and the
  delivered wheel hash when an offline/private wheel is claimed.
- If the host is not Python, the implementation uses an already approved
  boundary or has explicit approval for the new service/process architecture;
  it does not reimplement MRKR in another language.

## 3. Provider and prompt boundary

- Evidence is authorized before extraction/retrieval.
- Provider output includes markerized text plus model-external valid IDs, match
  hints, source registry/index, and diagnostics.
- The model sees package-generated citable text and mandatory instructions once.
- The model does not see secrets, ACL metadata, signed URLs, or resolver internals.
- Only current-turn marker IDs are valid; prompt-only history projection removes
  stale markers without mutating persisted history.
- Web, document, internal, and hybrid providers have explicit ownership and do
  not scrub each other's valid markers.

## 4. Finalization

- Verification occurs after every model path and before persistence/API return.
- Only designated MRKR-bearing text fields are scrubbed.
- Valid IDs originate from current provider state, not the response.
- Each surviving marker label matches the provider-owned label for its valid ID;
  ID-only scrubbing is not treated as complete verification.
- Unknown, malformed, stale, duplicate, and ambiguous markers are handled
  deterministically.
- Citation bundle metadata is built by backend/provider code.
- Required-citation policy fails closed when no valid support remains.
- High-stakes implementations test semantic support, not ID membership alone.

## 5. Storage and authorization

- Existing storage is reused with additive citation metadata.
- Bundle/source records retain stable source identity/version/checksum and
  enough anchors for audit.
- Tenant isolation applies to packet, result, and source resolution.
- Citation opening rechecks current authorization.
- Deleted/revoked sources do not leak stale content.
- Raw prompts/source/model output follow existing sensitive-data retention rules.

## 6. Frontend

- UI renders only sanitized content plus verified bundle.
- Exact markers become keyboard-accessible inline controls.
- Source detail uses host-native components and current auth routes.
- Unresolved markers are not raw/clickable.
- Streaming handles partial tokens; reload preserves old verified responses.
- Warning colors are reserved for real warnings/errors.
- Export behavior is explicit and tested when citations are contractually part
  of the exported result.

## 7. On-prem

- Wheel/dependencies come from an approved private registry or offline bundle.
- No runtime package/model download is introduced.
- External search, model, OCR/vision, and telemetry egress are explicit and
  disable cleanly.
- Air-gapped document flow works without external credentials.
- Secrets use the host secret manager and never enter prompts/client bundles.
- Resource limits, path safety, malware/MIME handling, residency, retention,
  encryption, and audit controls are inherited or explicitly implemented.

## 8. Behavioral evidence

Require tests for:

- valid and invented marker outputs;
- unsupported claims;
- numeric/date/quote support;
- stale follow-up IDs;
- provider timeout/no-result/credential failure;
- cross-tenant and revoked-source access;
- hybrid provider coexistence when applicable;
- real package import, not only mocks;
- browser click-through and accessibility when a frontend exists;
- unchanged non-citation workflow behavior;
- offline/no-egress operation when on-prem is claimed.
- executable adapter/finalizer tests or equivalent product-native tests, not
  only prompt prose and a review checklist.
