# Executable Reference Assets

Use these only after the codebase audit identifies the existing owners. Copy or
adapt the smallest relevant part; do not install a parallel framework.

## Python adapter and finalizer

`assets/python/mrkr_reference.py` supplies:

- `build_text_envelope` for approved web, RAG, and internal-search text;
- `build_document_envelope` for authorized document bytes, explicit compact
  caller-owned labels, and page-specific marker labels;
- source-marker injection stripping and unregistered-marker fail-closed checks;
- current-invocation ID and provider-label validation;
- `finalize_text` for one declared MRKR-bearing field;
- backend-built citation bundles and prompt-only history projection;
- `validate_persisted_result` for API/storage consistency checks.

It intentionally does not own retrieval, model calls, persistence,
authorization, routes, or UI. Adapt its dataclasses to existing domain models
instead of creating duplicate models when equivalent types already exist.

Run the reference tests with the target environment's Python:

```bash
PYTHONPATH=assets/python python -m unittest discover -s assets/python -p 'test_*.py' -v
```

## Result conformance CLI

Validate an emitted result shaped as `{ "text": ..., "citationBundle": ... }`:

```bash
python scripts/validate_citation_result.py result.json --require-citation
```

This proves internal bundle/marker consistency. It does not prove that the
source semantically supports the claim or that provider metadata was honestly
created; retain provider and behavioral tests for those properties.

## Frontend fallback

`assets/react/citation-model.ts`, `CitableText.tsx`, and
`citation-fallback.css` provide a dependency-light React fallback. Prefer the
host's rich-text parser, dialog/drawer, button, and theme components. Keep the
pure parser and security rules when adapting the visual component. Import the
CSS once at the host application's existing style entry point; the component
does not impose a bundler-specific CSS import.

## Compatibility

`assets/compatibility.json` records the exact package/runtime combination used
to validate this packet. It is not a universal dependency lock. For delivery,
freeze the approved wheel plus all transitive wheels in the customer's normal
lockfile or offline bundle and update the manifest only after rerunning all
reference and product tests.

Check the installed runtime and optionally an approved wheel:

```bash
python scripts/check_compatibility.py
python scripts/check_compatibility.py --wheel /approved/distylai_mrkr.whl
```
