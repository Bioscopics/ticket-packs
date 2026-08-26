# Provider Adapters and Model Injection

## Provider-neutral adapter result

Each provider adapter should return the same logical envelope:

```text
citable_text        model-visible source text with exact MRKRs and instructions
valid_marker_ids    current invocation's allowed opaque IDs
match_hints         provider/package-owned anchors and labels
source_registry     authorized source records/locators/checksums
diagnostics         extraction/search quality, warnings, and failures
```

Keep this envelope behind the application's existing service boundary. Do not
make the model author it.

## Document and file sources

Resolve user-selected file IDs through the current authorization layer, then
pass authorized bytes or staged paths to `distylai-mrkr`. Retain extraction
quality warnings and source checksums. Preserve the target application's file
limits, malware scanning, MIME detection, tenant isolation, and deletion rules.

Folders are a selection convenience, not permission to recurse through an
unbounded filesystem. Apply existing scope, hidden-file, size, count, and type
limits before extraction.

## Web sources

The search provider remains replaceable. It must return actual source content
and stable source locators, not model-invented citations. Normalize selected
results into citable documents, build the packet with `distylai-mrkr`, and map
each marker label to a retained authorized source record.

For public web search:

- use the customer's approved provider and egress path;
- assign a human-readable label that is unique within the invocation and bind
  it to exactly one retained source record;
- retain query, retrieval time, source URL/title, and content checksum where
  policy permits;
- prefer authoritative sources and record provider errors/rate limits;
- never expose search credentials to the model or frontend;
- do not treat a URL alone as evidence without retrieved source text.

For internal search/RAG, use object IDs or signed resolver routes rather than
leaking storage paths.

## Hybrid sources

Build one packet from the selected document, web, and internal source texts
when practical. Otherwise merge provider registries before model invocation and
validate all active marker IDs in one finalizer. Detect duplicate IDs and fail
closed rather than allowing ambiguous resolution. Reject duplicate labels that
would map one displayed source name to different records in the same packet.

## Injection into an existing model call

Add the citable packet at the narrowest existing context assembly boundary:

```text
existing system/product instructions
existing user task and state
citable packet text for this invocation
```

`packet.text` already contains mandatory MRKR requirements. If an adapter
produces markerized context without `packet.text`, use the package's
`MRKR_PINCITE_REQUIREMENTS` once. Use
`FILE_WEB_SEARCH_CITATION_REQUIREMENTS` only when the actual agent has the file
and web search tools described by that add-on.

Do not replace the product prompt. Add only the minimum citation-specific rules
needed at the owner boundary:

- copy exact current markers immediately after supported claims;
- never invent IDs or resolver metadata;
- omit or qualify unsupported claims according to product policy;
- preserve the required output schema and domain behavior.

## Agent and tool workflows

If an existing agent retrieves evidence through tools, return markerized text
from the tool or inject the resulting packet before the reasoning/model call.
Do not add a parallel citation agent. Limit tool permissions and secrets using
the host agent framework's existing controls.

For follow-ups, strip old markers from the prompt-only history projection with
the package API and provide a fresh current packet. Do not mutate persisted
history merely to prepare a new prompt.
