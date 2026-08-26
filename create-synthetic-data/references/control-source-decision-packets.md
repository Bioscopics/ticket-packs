# Control Sources And Decision Packets

Use this reference when a dataset combines a governing source with records or submissions that a system must evaluate against it. Common controls include policies, clinical guidelines, rubrics, statutes, schemas, eligibility rules, underwriting rules, and compliance checklists.

## Task-Object Contract

Write `planning/task_object_map.json` before substantive generation:

```json
{
  "schema_version": 1,
  "consumer_task": "apply a shared control to each generated submission",
  "model_visible_inputs": [
    {"role": "control_source", "path": "guideline/raw_policy.md", "mutation": "forbidden"},
    {"role": "artifact_to_synthesize", "path_pattern": "scenario_packs/*/inputs/*"}
  ],
  "system_output": ["criterion findings", "final decision", "rationale"],
  "held_out": ["expected decisions", "evidence anchors", "expert annotations"],
  "real_shape_examples": ["same-class operational packets"],
  "explicit_non_targets": ["new control documents", "policy rewrites"]
}
```

The map must answer:

- What stays shared and unchanged?
- What is generated per case?
- What does the tested system receive?
- What output is scored?
- What is evaluator-only?
- Which artifact class supplies length, format, and messiness calibration?

If the answers are ambiguous, stop before coverage planning.

## Default Control Handling

- Preserve a supplied or publicly available control byte-for-byte when possible.
- Store one shared control once unless the consumer requires per-case bundling.
- Do not infer that a prominent control document is the thing to synthesize.
- Do not generate multiple policies, guidelines, rubrics, or schemas merely to create variation. Put variation in the submissions, evidence, chronology, and outcomes.
- Treat later SME glosses as evaluator-only unless the tested system receives them. Use them to design difficult gold cases only when the evidence-stage contract permits it.
- Record the extraction/filter rule and control hash. Fail closed if excluded expert markers remain in the model-visible control.

## Submission-Packet Shape

Generate the operational record family, not a short answer-shaped summary. A governed decision packet may include:

- cover/request/intake forms;
- independently authored source records;
- dated updates, corrections, addenda, and resubmissions;
- results, logs, tables, images, or structured exports;
- missing or referenced-but-absent attachments where planned;
- source-native signatures, authors, status timestamps, and page furniture.

Length must be earned by distinct source documents and evidence. Do not repeat facts, timelines, generic grids, metadata rows, or continuation templates to hit a target. If the available evidence only supports fewer pages, repaginate within the soft range or revise the case architecture.

## Decision Labels

Keep labels outside uploadable inputs. For criterion-driven decisions, each case should usually include:

```json
{
  "criteria": [
    {
      "criterion_id": "C1",
      "status": "met | not_met | unclear | not_applicable",
      "rationale": "source-grounded explanation",
      "anchors": ["A-001"]
    }
  ],
  "final_decision": "approve | deny",
  "final_rationale": "decision rule applied to criterion findings"
}
```

- Use the control's actual Boolean structure; preserve `ALL`, `ANY`, thresholds, exclusions, and temporal conditions.
- Make every material rationale claim resolve to actual source evidence or a documented absence.
- Freeze pagination before generating PDF anchors.
- Make finality explicit. A denial for insufficient evidence must not read as a still-pending request unless `pending` is an intended label.
- Run a mutation check when feasible: removing decisive evidence should alter the affected criterion or final decision.

## Prior-Authorization And Utilization Review

When a user provides a clinical utilization guideline and asks for synthetic data, default to:

- one shared raw guideline;
- synthetic prior-authorization or concurrent-review record packets;
- held-out per-criterion findings and final approve/deny decisions;
- realistic clinical chronology and page-level evidence anchors.

Do not default to synthetic guideline generation. Guidelines are often already available; the evaluation surface is whether the system can apply them to messy submitted records.

If the input modality is not stated, inspect the product contract and representative current workflows before asking. Choose the observed representative channel or a measured channel mix, record the assumption, and build a native pilot. Ask only when the consumer accepts one hard format and that choice cannot be discovered.

### Realistic Input Families

Calibrate from actual prior-authorization forms, medical-record submissions, or the nearest official proxy. A packet may include:

- fax cover and authorization request;
- attachment index or resubmission/addendum cover;
- ED/triage note, H&P, orders, and progress notes;
- serial vitals, nursing flowsheets, intake/output, and medication administration;
- laboratory, microbiology, imaging, consultation, and procedure reports;
- discharge/transfer documentation;
- referenced but absent records for planned insufficiency cases.

Do not reduce these to a few hundred words of clean Markdown when the target workflow receives a multi-page record packet.

### Fax/OCR Requirements

When the workflow is fax/OCR-like:

- create an actual PDF whose pages are rasterized source documents with a searchable OCR layer;
- vary degradation by source system, document family, fax batch, and seeded transport conditions, not `page_index % N` cadence;
- preserve legibility of decisive evidence while allowing realistic skew, contrast, scan borders, OCR line breaks, and occasional character errors;
- keep authored/signed/verified timestamps later than every observed fact on that source page;
- distinguish prospective plans from later observed events;
- ensure consolidated/resubmitted fax dates follow the latest included record;
- scan input text, filenames, and metadata for decision, criterion, evaluator, synthetic/test, policy-answer, and expert-marker leakage.

### Pilot Gate

Before case fanout, independently review one representative packet:

1. Inspect every pilot page and every distinct family at original resolution.
2. Check chronology at the source-page level, not only the fax cover.
3. Confirm page count is content-driven and each page is independently useful.
4. Check actual OCR searchability and frozen evidence anchors.
5. Reject generic fill tables, repeated facts, deterministic degradation cadence, fake density from borders, large unexplained voids, clipped tables, and stale QA renders.
6. Freeze the renderer only after a fresh reviewer returns `GO`.

## QA And Packaging

- Require parseable, non-vacuous saved QA. A `.json` file cannot contain Markdown, and an audit that reports zero cases is not evidence.
- Tie every hash-bearing QA report and helper receipt to the current artifact hash; regenerate receipts after any case changes.
- Run delivery calibration only after modality status is `complete` and its declared helper receipt exists.
- Package with a narrow allowlist. Include shared controls, uploadable submissions, held-out labels/manifests, portable calibration contracts, inventories, required helper receipts, and public QA. Exclude case specs, generators, prompts, work images, renders, internal reviews, private paths, and superseded receipts.
