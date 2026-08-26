# Portable MRKR Architecture

MRKR is a citation lifecycle, not a workflow engine. Add it around the existing
model boundary.

```text
Source intake/retrieval
  |  uploaded files, internal search, RAG, public web, records
  v
Provider adapter
  |  normalizes source text + stable authorized source locator
  v
distylai-mrkr packet construction
  |-- model-visible: citable text with exact MRKRs + mandatory instructions
  `-- model-external: marker IDs, match hints, source index/registry, checksums
  v
Existing model or agent call
  |  may copy exact markers; may not create IDs or resolver metadata
  v
Finalizer
  |-- scrub unknown/malformed markers
  |-- resolve valid marker IDs to current provider metadata
  |-- apply citation-required policy to designated fields
  `-- return sanitized content + citation bundle
  v
Existing persistence/API
  |  additive citation metadata, normal tenant/auth boundaries
  v
Existing frontend
     exact marker parser -> accessible citation control -> source modal/drawer
```

## Integration contract

Freeze these decisions before editing:

| Concern | Required decision |
| --- | --- |
| Evidence-bearing output | Exact text/Markdown fields that may contain MRKRs |
| Provider | Document, web, internal retrieval, or hybrid owner |
| Model boundary | Existing function that assembles context and invokes the model |
| Current context | Packet or provider result for this invocation only |
| Finalizer | Existing response boundary that verifies designated fields |
| Citation policy | Optional, required-if-evidence-used, or required for the surface |
| Metadata store | Existing record/object/file store with tenant ACLs |
| API | Additive sanitized content plus provider-owned citation bundle |
| Renderer | Existing rich-text/chat/document viewer extension point |

## Data separation

Model-visible data:

- source content with exact canonical markers;
- the package-supplied mandatory citation requirements;
- the user's task and existing application instructions.

Model-external data:

- valid marker ID set;
- citation match hints and source registry/index;
- source URLs, object IDs, access-control facts, checksums, and extraction
  diagnostics;
- the final citation bundle.

Never ask the model to emit the model-external fields. Build them from the
provider packet and verified output.

## Current-turn rule

Treat marker IDs as invocation-local opaque tokens. If prior assistant output
is included in a follow-up prompt, create a prompt-only projection with prior
markers and citation bundles removed. Preserve authoritative history in
storage, but require current claims to cite markers from current context.

## Hybrid providers

Prefer constructing one packet from all selected sources so one ID namespace
and one finalizer own the turn. If providers must remain separate, maintain a
disjoint marker registry and use a finalizer that validates all active
providers together. Never let a web-only scrubber erase valid document markers
or vice versa.
