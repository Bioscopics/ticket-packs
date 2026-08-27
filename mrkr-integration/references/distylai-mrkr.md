# `distylai-mrkr` Public API

The distribution is `distylai-mrkr`; the Python import is `mrkr`. Use the
version approved by the target environment and verify the public symbols at
implementation time. The examples below match the 0.1.7 public API.

## Availability

`distylai-mrkr==0.1.7` is not published on public PyPI. Current users need an
approved private wheel or registry, or an authorized source checkout.

## Packet from existing text

```python
from mrkr import build_citable_packet

packet = build_citable_packet(
    [
        {
            "text": source_text,
            "label": short_source_label,
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

When the application already owns uploaded content in memory or object storage,
extract it first and then pass the codebase-owned compact label into packet
construction. This preserves the package's faithful extraction while avoiding
filename-derived marker noise:

```python
from mrkr import build_citable_packet, document_bytes_to_faithful_markdown

document = await document_bytes_to_faithful_markdown(
    upload_bytes,
    filename=safe_full_filename,
    mime_type=detected_mime_type,
)
packet = build_citable_packet(
    [
        {
            "text": page.markdown,
            "label": f"{short_source_reference}:p{page.page_number}",
            "title": full_display_title,
            "path": authorized_source_locator,
        }
        for page in document.pages
    ]
)
```

Convenience document-byte packet builders in some package versions derive the
visible label from the filename and do not accept a caller label. Do not use
that convenience path when it would expose a long filename. Feature-detect the
installed API; either pass an explicit label when supported or use the
extract-then-build sequence above.

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
            "label": assign_short_source_label(document),
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

## Source-label contract

The provider adapter, never the model, assigns the display label passed to
packet construction. Use the shortest human-readable label that remains unique
within the invocation:

1. Prefer an existing short document, record, exhibit, or source reference.
2. Otherwise normalize the filename stem or title, removing `.pdf` and other
   extensions, long paths, UUIDs, and redundant words.
3. Collision-check the result within the packet and add only the shortest
   stable disambiguator needed.
4. For page-based sources, use a compact page form such as `lf_001:p12` when the
   package/provider boundary supports page-specific labels.

The private source index retains the full filename/title, stable document ID,
page, version/checksum, anchors, resolver, and authorization data. Do not repeat
that metadata in the label. Finalization must require the returned label to
exactly match the provider-owned hint for its opaque ID.

## Dependency and distribution

- Declare `distylai-mrkr` in every package that imports `mrkr` directly.
- Follow the target repository's pin and lockfile policy.
- For private/on-prem delivery, mirror the approved wheel and transitive wheels
  to the customer's package registry or deliver an integrity-checked offline
  wheel set. Do not add a runtime download path.
- Fail startup/build clearly when required public symbols are absent; do not
  silently fall back to home-grown markers.
