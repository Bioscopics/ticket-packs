# `distylai-mrkr` Public API

The distribution is `distylai-mrkr`; the Python import is `mrkr`. Use the
version approved by the target environment and verify the public symbols at
implementation time. The examples below match the 0.1.7 public API.

## Packet from existing text

```python
from mrkr import build_citable_packet

packet = build_citable_packet(
    [
        {
            "text": source_text,
            "label": display_label,
            "source": authorized_source_locator,
        }
    ]
)

model_visible_context = packet.text
valid_marker_ids = set(packet.marker_ids)
match_hints = packet.citation_match_hints
source_index = packet.source_index
```

`packet.text` includes markerized context and the package's mandatory citation
requirements. Do not append a second conflicting copy.

## Packet from uploaded bytes

Use bytes APIs when the application already owns uploaded content in memory or
object storage:

```python
from mrkr import async_build_citable_packet_from_documents

packet = await async_build_citable_packet_from_documents(
    [
        {
            "content": upload_bytes,
            "filename": safe_display_name,
            "mime_type": detected_mime_type,
        }
    ]
)
```

## Packet from existing paths or folders

```python
from mrkr import async_faithful_markdown_from_paths, build_citable_packet

documents = await async_faithful_markdown_from_paths(
    selected_paths,
    vision="auto",
)
packet = build_citable_packet(
    [
        {
            "text": document.markdown,
            "label": document.filename,
            "path": document.filename,
        }
        for document in documents
    ]
)
```

Do not expose arbitrary server paths. Resolve user selections through the
application's existing authorized file/object layer first.

`vision="auto"` can use provider-backed extraction when supported credentials
are exported. In on-prem or restricted environments, make that egress decision
explicit; deterministic extraction must remain the default when external calls
are not allowed.

## Verification

```python
from mrkr import extract_citation_ids_from_context, scrub_unverified_markers

valid_ids = set(packet.marker_ids)
sanitized_text, stats = scrub_unverified_markers(
    model_output,
    valid_ids,
    mode="remove",
)
referenced_ids = extract_citation_ids_from_context(sanitized_text)
```

Apply scrubbing only to designated MRKR-bearing text fields. Do not run regex
replacement over arbitrary serialized JSON or binary content.

`scrub_unverified_markers` validates the ID set. A production finalizer must
also parse each surviving marker with `MRKR_PATTERN` and require its label to
equal the provider-owned hint label for that ID. Remove or reject markers that
reuse a valid ID with an altered label.

Use package exports such as `MRKR_PATTERN`, `MRKR_ID_PATTERN`,
`scrub_all_markers`, `extract_citation_ids_from_hints`, and
`rollup_from_answer` instead of duplicating parser behavior.

## Marker contract

Canonical marker:

```text
【mrkr: ||<source label>|| <8 lowercase hexadecimal characters>】
```

IDs are opaque. Neither application code nor the model may derive an ID from a
URL, filename, page, hash, or counter. Tests may inject the package's private
ID factory hook only for deterministic package-level fixtures; product code
must not.

## Dependency and distribution

- Declare `distylai-mrkr` in every package that imports `mrkr` directly.
- Follow the target repository's pin and lockfile policy.
- For private/on-prem delivery, mirror the approved wheel and transitive wheels
  to the customer's package registry or deliver an integrity-checked offline
  wheel set. Do not add a runtime download path.
- Fail startup/build clearly when required public symbols are absent; do not
  silently fall back to home-grown markers.
