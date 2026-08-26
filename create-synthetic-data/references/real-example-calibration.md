# Real-Example Calibration

## Length Bands Are Usually Soft

Measured page, word, row, duration, and file-size ranges describe the observed distribution; they are not automatic acceptance ceilings. Record them as soft targets unless an external consumer, schema, court rule, statute, product limit, or explicit user requirement creates a hard bound. For each hard bound, record the source, the exact counting method, and what content is excluded. A small organic deviation from a soft band is preferable to padding, tiny type, forced page breaks, abbreviated furniture, or deleting useful complexity.

Use this reference for every synthetic dataset. Content plausibility alone is insufficient: calibrate the physical and structural shape of the data before generation.

## Mandatory Gate

Before bulk generation, find and inspect representative real examples whenever access, privacy, and licensing permit. Prefer, in order:

1. user-provided examples or an existing target corpus;
2. the actual public benchmark, dataset, repository, schema, or product export being emulated;
3. authoritative forms, manuals, sample packets, standards, or public records from the real workflow;
4. unrelated examples of the same artifact class and lifecycle;
5. the nearest documented proxy when no direct example is accessible.

For a public benchmark or host dataset, download or query the actual records and verify IDs, locators, dates, speakers, schemas, and application semantics end to end. A plausible invented reference is not a host reference.

If no usable example exists, set the profile status to `proxy` or `blocked`, explain why, and obtain an explicit downgrade in the ticket pack. Do not silently generate from intuition while claiming real-world fidelity.

## Mixed-Authority References

Some reference packets combine a raw source with later SME annotations, analyst synthesis, or proposed future-state material. Calibrate the target information stage deliberately:

- **observed**: source text, records, layout, structure, and metadata available at the target stage;
- **supported_inference**: a bounded interpretation supported by observed material, but not directly stated in it;
- **proposal**: a recommended design, disposition, or next step that does not yet exist in the source state;
- **expert_annotation**: SME-added context or correction not available before the expert review.

For a pre-SME synthetic source corpus, strip or exclude `expert_annotation` lines using a documented, reproducible marker rule. Keep the raw baseline as the uploadable/source layer. Put expert deltas in a separate held-out evaluation, review, or enrichment layer unless the product being tested receives expert annotations as an input.

Record the boundary in `planning/real_example_profile.json`, for example:

```json
{
  "evidence_stage_boundary": {
    "target_stage": "pre_sme_review",
    "included_classes": ["observed"],
    "excluded_classes": ["expert_annotation", "proposal"],
    "filter_rule": "remove lines containing <known expert marker>",
    "expert_delta_destination": "eval_sets/expert_review/"
  }
}
```

Do not let an SME correction silently become a raw fact, a label, or a source citation. Provenance records association and review history; it does not make a claim true or demonstrate that the earlier source included it.

## What To Measure

Inspect enough examples to estimate variation, not just one canonical file. For large corpora, sample across classes, time periods, sources, and obvious edge cases.

Measure:

- artifact families, native extensions, MIME types, and common companion files;
- length/scale distributions: pages, rows, fields, turns, tokens, duration, resolution, frame rate, or file size;
- internal structure: sections, forms, sheets, tables, message threads, event sequences, scene/turn boundaries;
- visual or conversational style: layout density, typography, headers/footers, scan quality, register, punctuation, speaker behavior;
- schema behavior: required/optional fields, nulls, repeated groups, value ranges, correlations, identifiers, timestamps;
- complexity and content density: nesting, cross-references, calculations, citations, medical/legal/technical detail, exception handling;
- lifecycle relationships: attachments, amendments, replies, corrected versions, prior-event anchors, duplicate/stale records;
- normal imperfections: OCR errors, compression, background noise, crosstalk, missing fields, skew, inconsistent casing, stale values;
- internal consistency rules and realistic contradiction patterns;
- privacy, licensing, and copy boundaries.

For user-provided/private examples, also identify source IDs, filenames, and absolute paths that must not enter a shareable archive. Put those exact tokens in the local-only shareable package policy, not in generated source artifacts.

## Required Profile

Write `planning/real_example_profile.json` with this minimum shape:

```json
{
  "status": "complete",
  "domain": "<domain>",
  "target_use_case": "<consumer and task>",
  "sources": [
    {
      "source_id": "SRC-001",
      "kind": "public_dataset",
      "title": "<title>",
      "url_or_path": "<URL or local path>",
      "accessed_at": "<ISO date>",
      "license_or_permission": "<license, permission, or inspection-only note>",
      "artifact_types": ["<type>"]
    }
  ],
  "observed_profile": {
    "artifact_families": [
      {
        "family": "<family>",
        "formats": ["<extension or MIME>"],
        "sample_count": 5,
        "length_or_scale": {"metric": "pages", "min": 2, "typical": 8, "max": 31},
        "structure": ["<observed structure>"],
        "style_or_register": ["<observed style>"],
        "complexity": ["<observed complexity>"],
        "metadata": ["<observed metadata>"],
        "imperfections": ["<observed imperfections>"],
        "relationships": ["<observed cross-artifact relationship>"]
      }
    ]
  },
  "target_profile": {
    "artifact_families": [
      {
        "family": "<family>",
        "count": 10,
        "formats": ["<format>"],
        "length_or_scale": {"metric": "pages", "min": 2, "typical": 8, "max": 31},
        "required_variation": ["<variation>"],
        "required_relationships": ["<relationship>"]
      }
    ]
  },
  "copy_boundary": ["Abstract structure and distributions; do not copy names, IDs, prose, signatures, or private facts."],
  "known_gaps": []
}
```

Use `status: "proxy"` only with `known_gaps` and a source that explains the proxy. Use `status: "blocked"` only when generation cannot honestly claim the requested realism.

## Generation Contract

- Generate to distributions and ranges, not one average template.
- Preserve correlations: longer records should have more sections/attachments; noisy scans should affect extraction; longer calls should have more turns and topic transitions.
- Match the artifact family and lifecycle, not surface wording alone.
- Keep synthetic content original. Examples calibrate shape, not text to copy.
- Record source IDs used by each artifact family in planning metadata or inventories.

## QA Contract

Compare generated vs target profile and report:

- file-family/count conformance;
- length/scale distribution conformance;
- structure, layout/register, and complexity conformance;
- metadata and relationship conformance;
- intended-imperfection conformance;
- justified deviations and blocked capabilities.

Reject a corpus that has good prose but the wrong file type, implausible length, toy-sized structured data, uniform templates, unresolved host references, or media sidecars without the media itself.
