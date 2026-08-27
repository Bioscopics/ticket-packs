# Verification Matrix

Compilation and a visible marker are not sufficient. Prove the complete
evidence-to-click lifecycle.

## Backend unit tests

- packet construction uses `distylai-mrkr` and produces canonical 8-hex MRKRs;
- only current packet IDs survive finalization;
- invented, malformed, altered, stale, and duplicate/ambiguous IDs fail or are
  scrubbed according to the contract;
- a valid ID paired with the wrong source label is removed or rejected;
- ordinary marker-bearing text is sanitized while tool arguments and business
  JSON remain marker-free and unchanged;
- source bundle entries derive from provider metadata, not model output;
- compact labels are provider-assigned, unique within the packet, extension-
  free, and resolve to full source metadata;
- verified claims join deterministically to native field/result/record IDs;
- any required legacy quote/page/source fields are derived from the verified
  registry rather than model-authored provenance;
- required-citation surfaces fail closed when no valid citation remains;
- document extraction warnings and provider errors remain observable;
- tenant/source authorization applies to resolver routes;
- follow-up prompt projection removes old markers without mutating history.

## Provider tests

- documents: text PDF, scanned PDF policy path, Office document, CSV/TSV if
  supported, multiple files, folder limits, empty/unsupported/oversize input;
- web: authoritative result, rate limit, no result, timeout, revoked URL,
  provider credential absence, and source content checksum;
- internal/RAG: allowed and denied records, stale index result, deleted source,
  and tenant isolation;
- hybrid: document and web markers coexist, resolve uniquely, and neither
  provider's finalization removes the other's valid citations.

## Behavioral probes

Run the real model/agent with production prompts and tools on at least:

1. a supported factual claim that should be cited;
2. an unsupported requested claim that must be omitted or qualified;
3. a numeric/date/quote claim requiring precise support;
4. a malicious source instruction asking the model to invent or alter markers;
5. a follow-up turn where prior marker IDs are no longer current.

Inspect the raw model output, sanitized output, valid ID set, final bundle, and
source resolution. Do not pass a probe solely because the final text contains
the substring `mrkr`.

For structured workflows, also inspect tool/business JSON and the final native
record association. The model must emit exact MRKRs in ordinary text, never in
tool arguments, and no second model may reconstruct the source quote or join.

## Product archetypes

- Memo: citations survive draft, edit, approval, persistence, reload, and
  export according to the declared export policy.
- Chat: streaming does not expose partial markers; follow-ups cite current
  context; restored conversations retain clickable old responses.
- Prior authorization/decision: deterministic decision outcome is unchanged;
  evidence/rationale citations are valid; missing citation infrastructure does
  not silently alter the decision.

## Browser acceptance

Use representative inputs in the real UI. Verify content, distinct clickable
citations, source modal/drawer, authorized navigation, keyboard behavior,
responsive layout, loading/error/empty states, reload, and revoked-source state.
Capture console/network errors and screenshots when the normal test process
does so.

## Regression proof

Compare pre- and post-change behavior for the same non-citation inputs:

- same workflow stages and tool routing;
- same deterministic outputs and state transitions;
- same model/provider selection unless explicitly changed;
- same structured business values while redundant model-authored citation
  inputs are removed or ignored for new MRKR-enabled runs;
- no additional network egress outside the approved provider calls;
- no unrelated UI or storage migration.

## Completion thresholds

The integration is not complete when any of these remain:

- model-authored resolver metadata is trusted;
- raw unverified markers reach persistence or UI;
- the integration stops at backend markerization or trace storage;
- MRKRs are required inside tool arguments, response-schema objects, or
  business JSON;
- new results retain a parallel model-authored quote/page/citation provenance
  path when verified MRKR metadata can replace it;
- structured results have no deterministic association between their native ID
  and the verified marker-bearing claim;
- marker labels repeat full filenames, paths, UUID noise, or other source
  metadata already retained in the private registry;
- citations are visible but not clickable;
- clickable citations do not reach the existing source viewer, page, excerpt,
  anchor, or highlight behavior promised by the product;
- clicking bypasses current authorization;
- only a mocked package path was tested;
- on-prem mode silently calls an external extraction/search service;
- citation work changed the product workflow without explicit scope.
