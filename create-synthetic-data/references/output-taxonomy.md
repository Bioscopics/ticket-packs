# Output Taxonomy

Use this taxonomy when packaging a synthetic dataset. Rename directories to match the project if needed, but preserve the source-vs-eval separation.

## General Layout

```text
output/
  README.md
  inventories/
    source_inventory.json
    eval_inventory.json
  source_artifacts/
  scenario_packs/
  eval_sets/
    raw_inputs/
    labels_or_answer_keys/
  qa_reports/
```

## Directory Roles

| Group | Use | Do Not Use For |
|---|---|---|
| `source_artifacts/` | Synthetic artifacts that can be ingested, indexed, used as context, used as training examples, or shown to users. | Held-out answer keys or labels. |
| `scenario_packs/` | End-to-end bundles with multiple related artifacts, personas, events, and expected workflows. | Blind ingestion without deciding which files are source vs held-out inputs. |
| `eval_sets/raw_inputs/` | Query-time or inference-time inputs for tests and benchmarks. | Source ingestion when that would leak the benchmark. |
| `eval_sets/labels_or_answer_keys/` | Ground truth labels, expected answers, rubrics, scoring metadata, or rationales. | Model/source context except during scoring. |
| `inventories/` | Provenance, schema, metadata, and relationship catalogs. | Replacing artifact content. |
| `qa_reports/` | Coverage, realism, validation, and repair evidence. | Training or source truth unless explicitly intended. |

## Possible Source Artifact Families

Choose families that fit the domain:

- documents, manuals, policies, specifications, contracts, tickets, notes;
- structured records, CSVs, JSON events, logs, transactions, API payloads;
- conversations, emails, chats, transcripts, call summaries;
- time-series, metrics snapshots, alerts, telemetry;
- forms, templates, examples, reports, dashboards exports;
- images/audio/video metadata or captions when media itself is not needed.

## Inventory Fields

Prefer these fields when they apply:

- `id`
- `title`
- `path`
- `format`
- `artifact_family`
- `source_role`
- `eval_role`
- `domain`
- `subdomain`
- `persona_or_actor`
- `locale_or_segment`
- `time_period`
- `version`
- `status`
- `synthetic_intent`
- `intended_imperfections`
- `labels`
- `related_artifacts`
- `graph_ingest` or `source_ingest`
- `eval_holdout`
- `notes`

## README Requirements

The output README should explain directory groups, not every file. It must make clear:

- what should be ingested, indexed, trained on, or used as context;
- what should be held out for evaluation;
- where labels and answer keys live;
- what imperfections were intentionally included;
- what research or realism QA was done;
- where inventories and validation reports live.

## Synthetic Provenance Placement

Document that the corpus is synthetic in `README.md`, `inventories/`, and `qa_reports/`. Do not burn synthetic provenance or evaluator instructions into uploadable/source files unless the explicit task is to test recognition of such notices.

Raw source files should look like plausible domain artifacts. Avoid source-file text such as:

- `SYNTHETIC CASE PACKET`
- `FICTIONAL TEST DATA`
- `Generated for upload/eval testing`
- `QA note for evaluators`
- `expected outputs`
- `held-out labels`

If a raw source artifact must contain a disclaimer for safety, make it domain-plausible and non-evaluator-specific, and record the tradeoff in QA.

## Shareable Archive Boundary

The local output tree may retain ticket packs, worker prompts, source calibration paths, and internal receipts for auditability. Do not include those automatically in an external archive.

Build shareable archives from an allowlist using `package_synthetic_output.py`. Include the README, inventories, source/scenario/eval artifacts, mandatory calibration JSON contracts, and safe QA evidence. Exclude prompts, ticket/lane controls, private source notes, absolute calibration paths, source identifiers prohibited by the copy boundary, existing archives, and temporary/OS files. See `shareable-packaging.md`.

## Validation Exceptions

If a source-like filename legitimately contains a validator token, write `planning/validation_exceptions.json` with an exact output-relative path, `rule: "eval_leakage_path"`, and a concrete reason. Wildcards, regex path suppression, nonexistent paths, and reasonless exceptions are invalid. Keep applied exceptions visible in validator output and reviewer receipts.
