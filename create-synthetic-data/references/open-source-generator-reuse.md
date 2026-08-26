# Open-Source Generator Reuse

Use this reference when a task could benefit from an existing simulator, population generator, benchmark builder, scenario engine, or domain-specific synthetic-data framework.

## Core Rule

During research, look for a credible existing generator before asking an agent to design or write a new simulation engine. When an established framework fits the state model and output needs, prefer cloning a pinned release, configuring it, running it, and validating its output. Write custom code only for a minimal adapter, deterministic post-processing, unsupported requirement, or demonstrated framework gap.

Framework reuse is an implementation-origin decision, not a replacement for generation-mode selection. An external framework may power a `deterministic_population` run or the state/label layer of a `hybrid` run.

## Required Planning Artifact

For simulation-heavy or population tasks, write `planning/generator_framework_decision.json`:

```json
{
  "schema_version": 1,
  "decision": "reuse_existing | reuse_plus_adapter | custom_generator | not_applicable",
  "search_scope": ["domain generator registries", "official repositories", "relevant papers"],
  "candidates": [
    {
      "name": "Synthea",
      "repository": "https://github.com/synthetichealth/synthea",
      "release_or_commit": "pinned tag or full commit SHA",
      "license": "Apache-2.0",
      "fit": ["longitudinal patient state", "export formats"],
      "gaps": ["client-specific prevalence requires calibration"],
      "status": "selected | rejected | blocked"
    }
  ],
  "selected_framework": {
    "name": "framework name",
    "repository": "canonical URL",
    "commit": "full immutable commit SHA",
    "license": "SPDX identifier or exact license",
    "runtime": "runtime and version",
    "entrypoint": "documented CLI or build target",
    "seed": "fixed seed or seed manifest",
    "configuration_paths": ["generator_configs/..."],
    "expected_outputs": ["materialized output paths"]
  },
  "reason": "why this origin is safer and more faithful than alternatives",
  "validation": ["smoke run", "seed replay", "schema checks", "distribution checks", "label recomputation"]
}
```

Use `not_applicable` for small authored case sets, document-only rendering, or tasks with no meaningful generator engine. Do not invent candidates merely to fill the file.

## Research And Selection

1. Search official repositories, project documentation, papers, package registries, and active community references for generators that model the target phenomenon.
2. Prefer maintained projects with a documented domain model, deterministic controls, clear exports, usable licenses, tests, and releases or immutable commits.
3. Inspect the actual repository and documentation. Do not select a framework from a search snippet, name match, star count, or broad subject similarity.
4. Compare candidates against the required state, dependencies, lifecycle, labels, scale, output schema, locale, chronology, prevalence controls, and realism surface.
5. Record both fit and gaps. A framework's domain label does not prove that its assumptions match the target task.
6. Select the smallest credible framework or combination that owns the difficult simulation logic. Do not combine multiple generators unless their state boundary and reconciliation rules are explicit.

Examples include Synthea for longitudinal synthetic patient records, SUMO for traffic simulation, Faker only for surface fields rather than causal state, and domain-specific benchmark generators discovered for the task. These examples are not a fixed allowlist.

## Clone And Run Contract

- Clone into a task-local temporary or generator-work directory, never over the user's repository.
- Pin a release tag and resolve it to a full commit SHA. Do not depend on a moving default branch.
- Record repository URL, commit, license, runtime/toolchain versions, documented build/run commands, configuration, seed, environment variables, output paths, elapsed time, and exit codes.
- Prefer the framework's documented CLI, configuration, modules, plugins, and export options. Do not rewrite its core engine merely to make the agent look productive.
- Run the smallest smoke population first. Inspect schemas and state transitions before a full run.
- Prove seed replay: the same pinned code, configuration, and seed must reproduce deterministic state/label summaries, or the receipt must document the framework's nondeterminism and tolerance.
- Keep generated outputs, task-owned configurations, minimal adapters, patches, and receipts. Do not redistribute the cloned repository in a shareable package unless its license and the package policy permit it.

## Supply-Chain And Execution Safety

Treat cloned code as untrusted until inspected.

- Read the license, installation steps, build scripts, container files, dependency manifests, and execution entrypoint before running.
- Prefer an isolated container, virtual environment, or task-local runtime. Do not install into the system runtime or mutate unrelated repositories.
- Do not expose production credentials, cloud tokens, private datasets, home-directory secrets, SSH agents, or broad host mounts.
- Disable or restrict outbound network access during generation when the framework does not require it. Never allow a generator to call production services.
- Reject unexpected post-install scripts, telemetry, destructive filesystem operations, privileged execution, or opaque downloaded binaries until explicitly reviewed.
- Record downloaded artifacts and container image digests when practical. Preserve any security downgrade or blocked dependency in the receipt.

## Adaptation Boundary

Prefer configuration over code. When adaptation is necessary:

- write the smallest auditable adapter around stable framework outputs;
- keep upstream framework state immutable and derive downstream labels from explicit rules;
- version mappings between framework concepts and target schemas;
- test row counts, identities, timestamps, units, relationships, and lossless round trips;
- keep LLM rendering downstream of locked facts and labels;
- do not patch the simulator to force a desired result without documenting the changed assumption.

If a candidate fails a material requirement, reject it explicitly and continue the search or choose a custom generator. Do not distort the task to fit the tool.

## Validation

Framework-generated data still requires calibration. Validate:

- schema and native export validity;
- entity and referential integrity;
- lifecycle and temporal consistency;
- state-to-label recomputation;
- requested base rates and decision-bearing strata;
- parameter sensitivity and support boundaries;
- output distributions against public or real calibration sources;
- seed replay and bounded/full-run equivalence;
- known framework artifacts, defaults, impossible states, and template fingerprints;
- realism of any LLM- or specialist-rendered surface artifacts.

Do not claim that framework provenance makes the output production-representative. Open-source defaults often model a generic or academic population. Client-specific prevalence, workflow noise, coding behavior, and production accuracy still require calibration against a real extract.

## Receipt

Write `qa_reports/generator_receipts/<framework>.json` or `.md` containing:

- selected project, canonical URL, license, release/tag, and full commit SHA;
- inspection and safety findings;
- exact clone/build/run commands and exit codes;
- runtime versions, configuration paths, seeds, and output paths;
- smoke-run and target-run counts;
- determinism, schema, integrity, distribution, and label-check results;
- minimal adapters or patches with reasons;
- known assumptions, unsupported strata, and calibration limits.

Stop and report `blocked` rather than silently replacing a failed framework run with hand-authored rows while claiming framework-backed generation.
