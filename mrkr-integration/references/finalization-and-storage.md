# Finalization and Storage

Finalization is a deterministic trust boundary after the model call and before
persistence/API return.

## Finalization sequence

1. Select only the contract-designated MRKR-bearing text fields.
2. Obtain valid IDs from the current provider packet, not from model output.
3. Use `scrub_unverified_markers` to remove or flag unknown markers according
   to the product's explicit policy.
4. Parse each surviving full marker with `MRKR_PATTERN`. Require the displayed
   label to equal the provider-owned hint label for that ID; remove or reject a
   valid ID paired with an altered label.
5. Extract referenced IDs from the sanitized fields.
6. Resolve each referenced ID to current match hints and exactly one authorized
   source record. Reject duplicate, missing, or ambiguous resolution.
7. Apply the surface's citation policy:
   - optional: valid citations may be absent;
   - required-if-evidence-used: evidence-backed claims require valid citations;
   - required: the designated output must contain at least one valid citation.
8. Persist/return sanitized content and a backend-built citation bundle.

ID membership proves provenance linkage, not semantic support. For high-stakes
flows, add a bounded verifier or existing evaluator that compares the nearby
claim with provider-owned anchors. Do not ask the model to self-certify support.

## Additive bundle shape

Adapt names to existing API conventions, but preserve these semantics:

```json
{
  "version": 1,
  "citations": {
    "deadbeef": {
      "label": "Service manual",
      "anchors": ["direct supporting source excerpt"],
      "sourceId": "authorized-source-id"
    }
  },
  "sources": [
    {
      "sourceId": "authorized-source-id",
      "title": "Service manual",
      "resolver": "/existing/authorized/source/route"
    }
  ]
}
```

Do not force URL fields for private documents. The resolver may be an existing
authorized route, object ID, document viewer state, or external URL.

## Persistence

Reuse the existing response, message, memo, case, or artifact record. Store
citation metadata additively where the existing schema allows it. Retain enough
to reproduce resolution and audit the response:

- sanitized model output;
- current citation bundle and packet/version identifier;
- source IDs, labels, checksums, and retrieval/extraction timestamps;
- match hints/anchors or a stable reference to them;
- extraction/search diagnostics and finalization statistics;
- raw model output only when existing retention and sensitive-data policy allow.

Do not migrate storage merely for citations. Context Mesh is one possible
existing store, not a requirement.

## Authorization and immutability

- Resolve citations under the requesting user's current tenant/document ACL.
- Never let a model-provided URL, label, or object ID become the resolver.
- Prevent cross-tenant marker/source collisions by scoping bundles to the
  invocation/result record.
- Preserve source version/checksum so later document changes do not silently
  alter what an old citation represented.
- If a source is deleted or access is revoked, retain an auditable tombstone or
  show an unavailable state according to policy; do not expose stale content.

## Failure behavior

Fail closed when the contract requires citations and provider artifacts,
verification, or secure source resolution is unavailable. Return an explicit
bounded product error or existing repair state. Do not return citation-looking
unverified output as success.
