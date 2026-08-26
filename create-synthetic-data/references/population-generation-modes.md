# Population Generation Modes

Use this reference whenever a dataset is larger than an intentionally small case set, must preserve a base rate, represents longitudinal entities, or needs labels that can be recomputed from state.

## Planner Decision

Generation mode and execution power are separate decisions. A deterministic generator may require frontier reasoning to design but fast compute to run; a small authored case may require deep domain reasoning. Write `planning/generation_mode_decision.json` before coverage planning:

```json
{
  "mode": "authored_cases | deterministic_population | hybrid",
  "engine_origin": "not_applicable | existing_open_source | existing_plus_adapter | custom",
  "unit": "patient | account | conversation | claim | case",
  "estimand": "what the dataset is intended to measure",
  "population_size": 100000,
  "base_rate_is_part_of_task": true,
  "state_owner": "generator | author",
  "label_owner": "deterministic_rule | author | adjudicator",
  "renderer_owner": "none | llm | specialist_helper",
  "framework_decision_path": "planning/generator_framework_decision.json",
  "framework_receipt_path": "qa_reports/generator_receipts/<framework>.json",
  "reason": "evidence-backed selection rationale",
  "validation": ["recomputation", "seed determinism", "distribution checks"]
}
```

## Engine Origin

Generation mode describes the dataset architecture; engine origin describes how the state simulator is implemented. Keep them separate.

For `deterministic_population` and simulation-backed `hybrid` runs, research credible existing generators before writing custom code. Prefer a pinned, licensed open-source framework when its documented state model and exports fit the task. The agent should usually clone, configure, run, and validate that framework rather than reimplementing its engine. Use `existing_plus_adapter` only for a minimal, auditable mapping or export layer. Choose `custom` only after `planning/generator_framework_decision.json` records the candidate search and material gaps. Read [open-source-generator-reuse.md](open-source-generator-reuse.md).

## Modes

### `authored_cases`

Use for a small set of deliberately distinct scenarios where each case is a test story and population prevalence is not an estimand. An agent may author inputs and held-out answers case by case. Require semantic diversity and independent review.

Do not use merely because the current case builder only supports this mode. A uniqueness rule over case signatures is not a population realism check.

### `deterministic_population`

Use when the task depends on prevalence, incidence, longitudinal state, eligibility, correlated events, lifecycle transitions, or labels at scale. The primary reproducibility surface is either a pinned external framework plus task-owned configuration/minimal adapters, or custom executable generator code after a documented reuse search. In both cases preserve immutable versions, parameters, seeds, manifests, commands, and validation receipts. Compute labels from simulated state; do not ask an LLM to author them row by row.

Require:

- explicit population and dependency model;
- deterministic seeds and versioned parameter files;
- conservation and reconciliation checks;
- label recomputation from state;
- distribution, base-rate, support, and effective-sample-size checks;
- a materialized pilot that matches a bounded or streaming production run;
- clear separation between enriched generation proportions and target-population estimates;
- retention modes such as full materialization, summary plus sampled panel, or summary only when storage is material.

### `hybrid`

Use when deterministic state and labels are necessary but free text, documents, images, audio, or video need realistic variation. The generator owns entities, dates, relationships, events, eligibility, and labels. The LLM or modality specialist receives only an allowed fact bundle and renders the surface artifact.

The renderer must not create or change state, labels, dates, identifiers, tests, treatments, results, or outcomes. Validate entailment, forbidden-fact rate, chronology, identity consistency, label leakage, template similarity, length distribution, and cross-artifact consistency. Repair renderer failures without changing generator truth.

## Scale And Calibration

Do not infer a client-specific prevalence or production-accuracy point estimate from synthetic data alone. Synthetic populations can support conditional estimates, robustness envelopes, rare-event power, and pipeline testing. Calibrate client-specific claims against a real extract when available; otherwise report source-backed public ranges, stress assumptions, unsupported strata, and identifiability limits.

For a population benchmark, scale must follow the estimand and rare-event support rather than the generic minimum case count. Predeclare minimum positive and negative counts per decision-bearing stratum, retention probabilities, weighting, and precision targets. Generate additional independent population draws only when those rules require them.

## Hybrid Workflow

1. Calibrate population marginals, dependencies, lifecycle transitions, artifact shapes, and known noise from real examples.
2. Research existing generator frameworks. Clone, inspect, pin, configure, and smoke-test the selected framework, or document why its gaps require a custom state machine. Implement only the missing adapter or custom layer and test the deterministic labeler.
3. Prove a small materialized run and bounded run produce identical state/label summaries.
4. Generate the target population and retain auditable summaries plus the required evaluation panel.
5. Sample fact bundles by label, near-miss, divergence, sparsity, identity, and lifecycle strata.
6. Render sampled artifacts with fast workers after facts are locked.
7. Use a fresh balanced or frontier reviewer for factual entailment and realism.
8. Package generator code, parameters, manifests, observed inputs, held-out truth, weights, and limitations separately.

## Failure Signals

Stop and redesign when:

- a requested base rate is represented by a handful of unique cases;
- labels are independently authored instead of recomputed from state;
- an agent writes a new simulator before checking whether a credible maintained framework already owns the hard domain model;
- a framework is selected by name or popularity without inspecting its actual assumptions, license, export behavior, or pinned source;
- a moving branch, unrecorded seed, host-global install, or unreceipted framework run makes the population irreproducible;
- the generator creates labels but no auditable causal state;
- a pure simulator emits obviously templated artifacts and no realism layer exists;
- an LLM renderer can see labels or invent facts;
- balancing or enrichment is reported as natural prevalence;
- every row is forced to be unique even though repetition is a real population property;
- full materialization is required only because no bounded retention mode was designed.
