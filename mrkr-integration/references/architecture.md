# Portable MRKR Architecture

MRKR is a citation lifecycle, not a workflow engine. Add it around the existing
model boundary.

```text
Source intake/retrieval and evidence selection
  |  uploaded files, internal search, RAG, public web, records
  v
Provider adapter
  |  normalizes selected source text + compact provider-owned label
  v
mrkr-provenance packet construction
  |-- model-visible: citable text with exact MRKRs + mandatory instructions
  `-- model-external: marker IDs, match hints, source index/registry, checksums
  v
Existing model or agent call
  |-- existing tool/business JSON remains marker-free
  `-- ordinary assistant text copies exact inline MRKRs
  v
Finalizer
  |-- scrub unknown/malformed markers
  |-- resolve valid marker IDs to current provider metadata
  |-- associate verified claims with native field/result IDs
  |-- derive legacy compatibility fields when still consumed
  `-- return sanitized content + citation bundle
  v
Existing persistence/API
  |  additive citation metadata, normal tenant/auth boundaries
  v
Existing frontend
     exact marker parser -> accessible citation control
                         -> existing source modal/viewer/page highlight
```

## Integration contract

Freeze these decisions before editing:

| Concern | Required decision |
| --- | --- |
| Evidence selection | Exact retrieved/selected source items supplied to the model |
| Evidence-bearing output | Ordinary raw text/Markdown channel that may contain MRKRs |
| Provider | Document, web, internal retrieval, or hybrid owner |
| Source label | Short provider-assigned reference, uniqueness, and page form |
| Model boundary | Existing function that assembles context and invokes the model |
| Current context | Packet or provider result for this invocation only |
| Finalizer | Existing response boundary that verifies designated fields |
| Native association | Deterministic claim-to-field/result/record binding |
| Legacy replacement | Model-authored quote/page/citation inputs to remove or derive |
| Citation policy | Optional, required-if-evidence-used, or required for the surface |
| Metadata store | Existing record/object/file store with tenant ACLs |
| API | Additive sanitized content plus provider-owned citation bundle |
| Renderer | Existing rich-text surface plus source viewer/highlight extension point |

## Data separation

Model-visible data:

- selected source content with exact canonical markers and compact labels;
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

Keep structured business output, tool calls, and response-schema objects
marker-free. An API transport may serialize ordinary assistant text as a JSON
string; that does not make the model's business JSON the MRKR channel. When the
product is field- or row-oriented, associate verified nearby claims with stable
native IDs after finalization. Do not fuzzy-match citations back to results or
ask another model to perform the join.

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
