# Evidence And Reference Contract

Use this contract whenever held-out labels, expected answers, findings, or rationales cite generated source artifacts.

## Preserve Host Schemas

Treat the user-provided prediction/output schema as controlling. Do not add `sheet`, `row`, `cell`, `reference_id`, or other keys when `additionalProperties: false` forbids them.

Put richer locators in a separate `expected/reference_manifest.json`. This keeps host answers valid while making every source claim independently resolvable.

## Manifest Shape

```json
{
  "schema_version": 1,
  "references": [
    {
      "reference_id": "REF-001",
      "claim_file": "prediction.json",
      "claim_path": "/findings/0/citations/0",
      "source_file": "reconciliation.pdf",
      "anchor": {"kind": "pdf", "page": 4},
      "expected_text": "year label (2025) agrees with the reconciliation contents",
      "match_mode": "contiguous"
    },
    {
      "reference_id": "REF-002",
      "claim_file": "planted_facts.json",
      "claim_path": "/facts/8",
      "source_file": "Payment History.xlsx",
      "anchor": {
        "kind": "xlsx",
        "sheet": "Payment History",
        "rows": [46, 49, 52],
        "cell_range": "A46:J52"
      },
      "expected_text": "CAM",
      "match_mode": "contiguous"
    }
  ]
}
```

`claim_path` is a JSON Pointer into the held-out claim file. `source_file` resolves under the same case's `inputs/` directory.

## Anchor Rules

- PDF: require `kind: pdf`, a real page number, and a short exact contiguous extracted substring.
- XLSX: require `kind: xlsx`, sheet, and at least one of `row`, `rows`, `cell`, `cells`, or `cell_range`.
- CSV: require `kind: csv` and row/rows.
- Text/JSON/EML: use `kind: text`, `json`, or `email` and an exact substring when text evidence is claimed.
- Image/audio/video or non-text evidence: use `kind: file` for existence and pair it with modality-specific visual/playback QA.

Use `match_mode: contiguous` by default. Use `normalized_whitespace` only when extraction necessarily changes whitespace, and include `normalization_reason`. Do not let normalization hide merged words, wrong cells, wrong pages, or invalid locators.

## Structured Evidence

For sums or multi-row facts, record every contributing row/cell range in the manifest or planted-fact map. Validate the rows against the actual workbook and recompute the tie-out. A workbook citation with only `page: 1` is not a deterministic structured-data anchor.

If the host prediction schema cannot encode workbook coordinates, cite schema-valid PDF/text evidence in the prediction and map the load-bearing workbook rows through `reference_manifest.json`.

## Required Audit

When labels cite source artifacts, run:

```bash
python3 scripts/audit_reference_integrity.py <output_dir> --require
```

Treat unresolved claim paths, missing files, wrong PDF pages, missing workbook coordinates, and absent exact text as blocking. The reviewer must rerun this auditor after every reference repair.
