---
name: create-synthetic-data
description: Create, extend, QA, repair, and package realistic synthetic datasets for any domain or product use case. Preserve supplied policies, guidelines, rubrics, schemas, and other control sources while generating the records or submissions evaluated against them; calibrate from real examples; dynamically route work by difficulty and speed; and use native subagents plus specialist image, audio, video, PDF, document, spreadsheet, and UI skills. Use for synthetic documents, records, logs, conversations, transactions, prior-authorization packets, multimedia datasets, eval sets, adversarial examples, scenario packs, inventories, and realism audits.
---

# Create Synthetic Data

## Core Rule

Treat synthetic data as a test instrument. First learn what real-world phenomenon, product workflow, model behavior, or evaluation surface the data must exercise; then generate artifacts with explicit provenance, realism constraints, intended imperfections, and holdout boundaries.

## Task Object And Control-Source Gate

Before calibration or generation, classify every important supplied artifact as one of: `control_source`, `real_shape_example`, `artifact_to_synthesize`, `output_template`, or `evaluator_only_annotation`. Write `planning/task_object_map.json` whenever the task includes a policy, guideline, rubric, schema, reference corpus, or other governing source.

- Default supplied/available controls to immutable shared inputs. Do not synthesize replacements or one variant per case unless the user explicitly asks to test control generation.
- Infer the operational task from the consumer's decision, not from the most prominent source file. A guideline plus case records usually means generate realistic case records and held-out decisions, not more guidelines.
- Calibrate each generated artifact family against real examples of that family. Never use a short policy, prompt, or prior failed synthetic record as the length/format reference for a faxed chart, filing, claim packet, or other operational record.
- State exactly what the tested system receives, what it must produce, and what remains held out. Block generation if those roles are still ambiguous.
- Resolve ambiguity from the user packet, existing corpus, product contract, and real-workflow research before asking. Proceed with a recorded, evidence-backed assumption when formats or scale are inferable; ask only when the unresolved choice would materially change the consumer interface, label semantics, or safety boundary.
- When the supplied corpus and later SME feedback disagree about the target, treat the feedback as a task-contract correction and repair the dataset architecture before generating more of the old artifact class.

Read [control-source-decision-packets.md](references/control-source-decision-packets.md) for governed decision workflows such as prior authorization, claims, grading, compliance, underwriting, and eligibility review.

## Evidence-Stage Integrity

Match the information state of the target workflow, not only the final subject-matter answer. When a reference bundle mixes original material with SME annotations, later analyst conclusions, proposed designs, or other enrichment that would not have existed at the target stage:

- build source-like artifacts from the pre-enrichment baseline only;
- keep expert-added material in a separate, explicitly labeled `expert_delta`, eval, or review layer unless the user says the target system receives it as input;
- classify planning and QA assertions as `observed`, `supported_inference`, `proposal`, or `expert_annotation`; do not present one class as another;
- require source-derived claims in raw artifacts to trace to `observed` material, while using expert annotations only as held-out evaluation or post-processing targets;
- record the stripping/filtering rule, excluded marker, and intended source/eval boundary in the calibration profile or local QA record.

Do not treat provenance, a human selection, an annotation, or a downstream validation result as proof that an upstream source contained the associated fact. A reviewer may accept or reject an artifact, but that decision does not retroactively change the source-like data.

Three universal gates and one conditional framework gate apply before substantive generation:

1. **Real-example calibration:** find and inspect representative real examples whenever access and licensing permit. Measure the artifact shape, not just its subject matter: file families, native formats, lengths, structure, layout/register, metadata, complexity, distributions, relationships, and normal imperfections. Write `planning/real_example_profile.json` and use it as a generation and QA contract. Read [real-example-calibration.md](references/real-example-calibration.md).
2. **Specialist-helper routing:** discover the available modality skills, select the best owner for every claimed output modality, read each selected `SKILL.md` completely, and write `planning/modality_execution_matrix.json`. The parent skill coordinates; image/audio/video/document helpers execute and validate their modality. Read [modality-helper-skills.md](references/modality-helper-skills.md).
3. **Native pilot acceptance:** for a repeated native-document or media family, generate one representative pilot before fanout. Require a fresh reviewer to accept real shape, chronology, content density, modality behavior, and label/reference separation. Freeze the accepted renderer only after `GO`; route findings back to the smallest owner and rerun the pilot.
4. **Open-source generator reuse:** for simulation-heavy, population, lifecycle, or computed-label tasks, research credible existing generators before designing a new engine. Prefer cloning and running a pinned, licensed framework through its documented configuration/CLI when it fits; write custom generator code only for a demonstrated gap or a minimal adapter. Record the decision in `planning/generator_framework_decision.json`, inspect cloned code before execution, and preserve a reproducibility/safety receipt. Read [open-source-generator-reuse.md](references/open-source-generator-reuse.md).

Do not begin bulk generation while either applicable gate is unresolved. If no usable real example or helper exists, record the blocked/proxy decision and downgrade the claim rather than silently inventing a substitute.

For substantive generation, use the `task-auto-planner-ticket-pack` method. The top-level agent should plan and dispatch the work; it should not directly author a multi-artifact corpus, native document suite, eval set, or QA package unless the user explicitly overrides the planner workflow.

For self-contained skill runs where the current agent is the only available worker and the user asked to create artifacts in a local/temp output directory, the ticket pack is a control artifact, not the final deliverable. Create a compact pack, then execute it in-process if child dispatch is unavailable or would only produce a plan. Do not stop after writing planning artifacts unless the task is explicitly planning-only.

Route speed and reasoning per lane/case from [execution-modes.md](references/execution-modes.md). Let the measured real-example difficulty decide where work should be fast, balanced, or frontier-heavy while preserving every quality gate. When native subagent tools are available and delegation is authorized, use native spawned subagents first; an explicit user request for a subagent must not be silently replaced by an external CLI session or user-owned thread.

Load references only as needed:

- [intake-questions.md](references/intake-questions.md): questions for unclear tasks.
- [output-taxonomy.md](references/output-taxonomy.md): general packaging and source-vs-eval routing.
- [realism-rubric.md](references/realism-rubric.md): QA checks for plausibility, artifacts, contradictions, leakage, and metadata.
- [native-document-artifacts.md](references/native-document-artifacts.md): generate realistic native PDF/DOCX/XLSX/XML and corrupted/scanned/extraction-hostile document variants.
- [synthetic-data-scale.md](references/synthetic-data-scale.md): use e2e stories, scale classes, and shallow/wide case-packet fanout for realistic corpus generation.
- [population-generation-modes.md](references/population-generation-modes.md): choose authored-case, deterministic-population, or hybrid generation; use whenever scale, base rates, longitudinal state, or computed labels matter.
- [open-source-generator-reuse.md](references/open-source-generator-reuse.md): discover, assess, clone, pin, configure, run, validate, and receipt existing open-source generators before writing a custom simulation engine.
- [real-example-calibration.md](references/real-example-calibration.md): mandatory real-example research, measurement, target-profile, privacy, and conformance contract for every dataset.
- [realistic-case-packet-calibration.md](references/realistic-case-packet-calibration.md): calibrate document-family realism from unrelated examples; avoid padded PDFs and template-looking packets.
- [conversation-dataset-regressions.md](references/conversation-dataset-regressions.md): for multi-session chats, semantic-language labels, or controlled time expressions, use hidden label-first planning and validate natural evidence, fresh-session openers, full-utterance label meaning, contextual temporal-expression variation, and blind adjudication.
- [modality-helper-skills.md](references/modality-helper-skills.md): route images, PDFs, DOCX, spreadsheets, audio, video, and UI tests to modality-specific helper skills/tools instead of faking them.
- [generated-app-media-contracts.md](references/generated-app-media-contracts.md): discover repository-native generated-app media contracts, route to available specialist helpers, and keep fixture files separate from held-out labels.
- [agent-prompts.md](references/agent-prompts.md): prompts for research, planning, generation, QA, repair, and packaging agents.
- [execution-modes.md](references/execution-modes.md): choose fast vs full lanes, native subagents, and model routing without weakening QA.
- [evidence-reference-contract.md](references/evidence-reference-contract.md): preserve host schemas while validating PDF/workbook evidence through held-out reference manifests.
- [control-source-decision-packets.md](references/control-source-decision-packets.md): distinguish immutable controls from generated submissions and build realistic criterion-scored decision packets, including prior-authorization fax/OCR cases.
- [shareable-packaging.md](references/shareable-packaging.md): build privacy-scanned allowlisted archives instead of zipping internal work areas.
- [example-hsbc-knowledge-corpus.md](references/example-hsbc-knowledge-corpus.md): example pattern from a policy/procedure corpus with eval sets.

Scripts:

- `scripts/audit_output_tree.py <output_dir>`: summarize directory groups and file counts.
- `scripts/validate_synthetic_output.py <output_dir> [--exceptions <path>]`: validate inventory paths, placeholders, and token-boundary eval-leakage risks with exact-path reasoned exceptions only.
- `scripts/audit_case_packet_realism.py <output_dir> [--render]`: audit case-packet file families, PDF lengths/extraction behavior, missing native modalities, and optional rendered previews for long PDFs.
- `scripts/audit_pdf_layout.py <path> [--strict] [--allow-sparse-final] [--json-out <path>]`: render every PDF page at low resolution and flag blank or under-filled pages. Generated clean/layout-sensitive PDFs must pass the canonical script with `--strict`; use `--allow-sparse-final` only for a documented terminal signature, certification, or exhibit page.
- `scripts/audit_calibration_contract.py <output_dir> [--phase planning|delivery] [--allow-blocked]`: validate the real-example profile and canonical modality matrix before generation, then require final helper receipts at delivery.
- `scripts/audit_reference_integrity.py <output_dir> [--require]`: validate claim JSON Pointers and source file/page/sheet/row/cell anchors without changing host schemas.
- `scripts/audit_execution_routing.py <output_dir>`: validate lane-by-lane speed/reasoning/model routing and escalation triggers from the real-example difficulty profile.
- `scripts/package_synthetic_output.py <output_dir> --zip <path> [--policy <path>]`: create a deterministic allowlisted archive, privacy-scan it, test integrity, and write a SHA-256 sidecar.

## Task-Pack Requirement

Use `task-auto-planner-ticket-pack` for any request that creates or materially revises:

- multiple artifacts or files;
- a native document suite such as PDF/DOCX/XLSX/XML inputs;
- an eval/test corpus with held-out labels;
- a realistic scenario pack;
- a dataset that needs research, QA, repair, or packaging.

The synthetic-data pack should usually include these lanes:

1. **Intake / Calibration Research:** find real examples and relevant established generators; produce the measured `real_example_profile.json` contract and any `generator_framework_decision.json` required by the task.
2. **Generator Framework Runner:** when reuse is selected, inspect, clone, pin, configure, smoke-test, and run the framework in an isolated task-local environment; return immutable source/runtime/seed receipts. Omit this lane when the decision is `not_applicable`.
3. **Capability Router:** discover installed helper skills and produce `modality_execution_matrix.json` with one execution owner and receipt path per modality.
4. **Coverage Planner:** produce a coverage matrix with artifact classes, target distributions, labels, planted facts, source-vs-eval routing, and QA gates.
5. **Artifact Generators:** create disjoint artifact families from the calibration profile; selected frameworks own simulated state, and specialist helpers own native/media generation.
6. **Eval / Labels Worker:** create tester-only expected answers, labels, rubrics, and planted-fact manifests outside uploaded/source files.
7. **Realism QA:** compare outputs to the real-example profile and audit plausibility, native validity, framework/helper receipts, leakage, imperfections, inventories, and distributions.
8. **Repair Worker:** fix QA findings while preserving intended imperfections and framework truth.
9. **Packager:** write README, inventories, validation report, and final handoff.

For small one-file demos, the planner may use a tiny single-pack flow. For anything intended to test a product UI, prefer the full lane set.

For case-based corpus generation, prefer the compact shallow/wide pattern in `synthetic-data-scale.md`: one research-and-case-architecture lane, then one parallel worker per complete case folder, then one parent aggregate/QA/package pass. Do not default to deeply serial research → design → generation → labels → review → repair unless the task genuinely needs that depth.

For fast-routed lanes, use native fast workers only after calibration and architecture lock their decisions, then use a fresh balanced/frontier reviewer. Never collapse the reviewer into the builder.

## Workflow

1. **Collect the data brief.** Ask enough to define domain, target users, product/AI-system use case, artifact types, realism level, scale, formats, privacy constraints, and required imperfections such as contradictions, stale data, noisy data, missing fields, label ambiguity, or adversarial cases. If the user names a specific AI/product use case, offer to create eval sets and answer keys/labels as held-out artifacts.
2. **Lock task objects and inspect existing artifacts.** Classify controls, shape examples, generated targets, templates, and evaluator-only annotations; write `planning/task_object_map.json` when controls are present. If there is an existing corpus, map its output tree, formats, inventories, schemas, coverage, duplicates, and obvious gaps before planning. Use `rg`, `find`, manifests, and the audit script.
3. **Calibrate from real examples and generator ecosystems.** Search for the actual target dataset or representative public/user-provided examples. Inspect enough samples to measure file types, length distributions, schemas, structure, style/register/layout, metadata, complexity, noise, lifecycle relationships, and internal consistency. For simulation-heavy or population tasks, also search official repositories, papers, registries, and documentation for established generators that model the phenomenon. Write `planning/real_example_profile.json`; cite or record every source and copy/privacy boundary.
4. **Discover and lock specialist helpers.** Inspect the available skill catalog and local product/runtime skill roots. A filesystem-backed helper is usable even when it is not registered/injected in the current session: read its `SKILL.md` directly and resolve its runtime from the owning repo. For each claimed modality, write the canonical `planning/modality_execution_matrix.json` with coarse modality key, owner, path, generation method, runtime dependencies, validation, receipt path, and fallback/block status. Run `audit_calibration_contract.py <output_dir> --phase planning` and repair every issue before generation.
5. **Choose the generation mode and implementation origin, then build coverage and dynamic execution routing.** Write `planning/generation_mode_decision.json` for any benchmark or multi-record corpus. Choose `authored_cases` for a small intentionally distinct case set; `deterministic_population` when base rates, longitudinal state, eligibility, dependencies, or labels must emerge over a population; and `hybrid` when deterministic state/labels need realistic LLM-rendered surfaces. Separately decide whether the state engine comes from a selected open-source framework, a framework plus minimal adapter, or custom code. For simulation-heavy/population tasks, write `planning/generator_framework_decision.json` even when the result is `custom_generator`; do not write a new engine until the candidate search and fit/gap analysis show why reuse is insufficient. Do not apply case-signature uniqueness or hand-authored minimum-case logic to a population. Read [population-generation-modes.md](references/population-generation-modes.md) and [open-source-generator-reuse.md](references/open-source-generator-reuse.md). Convert the measured profile into target ranges and variation, then track domain/topic, persona/role, jurisdiction/locale if relevant, time period, artifact type, source-vs-eval role, labels, required edge cases, expected contradictions, and quality checks. For realistic case packets, map the full related document family. For multi-session chats, semantic-language labels, or controlled time expressions, add the applicable checks from [conversation-dataset-regressions.md](references/conversation-dataset-regressions.md) to the coverage and QA plan. Write `planning/execution_routing_matrix.json` so each lane/case receives the fastest model/reasoning level justified by source uncertainty, messiness, stakes, coupling, volume, modality difficulty, and validator strength. Run `audit_execution_routing.py` before dispatch.
   Treat measured page, word, row, duration, and file-size bands as soft calibration targets by default. A hard minimum or maximum requires an external constraint from the user, product, schema, statute, court rule, or other authoritative source recorded in the plan. Do not trim useful content, abbreviate natural document furniture, or add padding merely to land inside an internal range.
6. **Author the ticket pack.** Make the calibration profile and modality matrix explicit upstream inputs. Route native/media lanes to their selected helper skills instead of giving a generic generator ownership of those files.
7. **Dispatch or execute lanes.** Prefer native spawned workers with disjoint write scopes for framework execution, helper-owned generation, eval labels, QA, repair, and packaging. A framework runner clones into a task-local temporary/generator-work directory, resolves the selected release to a full commit SHA, inspects its license/build/entrypoint, runs a smoke population, then runs the pinned configuration with fixed seeds. It must not expose production credentials, install into system runtimes, or mutate unrelated repositories. Use faster workers only for locked bounded tasks and a separate high-capability reviewer for uncertain/high-stakes work. If native dispatch is unavailable, execute in-process or use a disclosed external fallback.
8. **Pilot before fanout.** Generate one representative native/media artifact, run modality-native validation, and obtain independent reviewer `GO`. Treat page/word/duration ranges as soft; repair by improving document-native content or pagination, never by repeated filler or mechanical density.
9. **Generate in batches.** Match the target profile's distributions rather than one average template. Use high-capability models for plans and QA when quality is critical; use cheaper/faster workers for bulk drafting and scoped repairs when appropriate. Keep labels and answer keys separate from raw/source artifacts.
10. **Attach metadata and evidence.** Include enough provenance for downstream use: title/id, path, format, synthetic role, source/eval status, generator batch, domain, owner/persona, locale/time period, version/status, labels, intended imperfections, related artifacts, calibration source IDs, and helper receipt IDs. Record evidence stage (`observed`, `supported_inference`, `proposal`, or `expert_annotation`) whenever the source bundle includes mixed-authority material. Preserve host prediction schemas; when held-out claims cite source artifacts, write `expected/reference_manifest.json` with deterministic PDF/workbook anchors.
11. **QA for realism and utility.** Compare generated file mix, lengths, structure, style, complexity, metadata, relationships, and imperfections against `real_example_profile.json`. Check helper receipts, schemas, leakage, duplicates, distributions, and domain plausibility. For the applicable conversational factors, run the fresh-session, semantic-label, and temporal-expression regressions before delivery.
12. **Repair and revalidate.** Fix unsafe, impossible, overly templated, under-length, wrong-format, helper-bypassing, mislabeled, leaking, unresolved-reference, or low-realism artifacts. Preserve useful planned imperfections. Rerun schema, reference, leakage, calibration, and realism validation after repairs.
13. **Package for use.** Organize outputs by role and include calibration, generator, and helper contracts in planning/QA, never in evaluator-visible source artifacts. Preserve selected-framework URL, license, full commit SHA, runtime versions, configuration, seeds, minimal adapters/patches, exact commands, and validation receipts. Do not redistribute a cloned upstream repository unless its license and package policy permit it. Write a directory-level README explaining what to ingest, what to hold out, and how to evaluate. For shareable delivery, write a package policy and use `package_synthetic_output.py`; do not zip prompts, ticket controls, private source paths, or prior archives.
14. **Report evidence.** State which real examples calibrated the corpus, which specialist helpers generated each modality, what was validated, where the README/inventories/eval sets live, and any blocked or downgraded capabilities.

## One-Shot Execution Rule

If the request says to create or generate a dataset and gives a local destination path, completion requires actual artifacts at that path. A planning-only output is blocked/incomplete.

Required minimum for one-shot runs:

- `planning/` or `control/` contains the compact ticket pack and packet-family map;
- `planning/task_object_map.json` exists when the task includes a governing control source and identifies the shared input, generated target, system output, and held-out layer;
- `planning/real_example_profile.json` records measured real-example sources and target ranges;
- `planning/generator_framework_decision.json` exists for simulation-heavy/population runs and records selected/rejected frameworks, immutable version, license, fit/gaps, runtime, seed/configuration, and validation, or a reasoned `not_applicable`/custom decision;
- `planning/modality_execution_matrix.json` records helper ownership for every claimed native/media modality, or explicitly records that no such modality is required;
- substantive multi-lane runs include a validated `planning/execution_routing_matrix.json`;
- `scenario_packs/*/inputs/` contains real native uploadable files;
- `scenario_packs/*/expected/` or `eval_sets/labels_or_answer_keys/` contains held-out labels;
- source-citing held-out claims include `expected/reference_manifest.json` and pass the reference auditor;
- `inventories/` lists generated files and paths;
- `qa_reports/` records validation, leakage, native-file, packet-realism, visual/render checks, and helper-skill receipts for claimed image/audio/video/native modalities when applicable;
- final response links concrete output paths and states whether dispatch was real or in-process fallback.
- framework-backed runs include a generator receipt with the canonical repository, full commit SHA, license, inspected entrypoint, exact run commands, fixed seeds/configuration, smoke and target counts, determinism checks, and calibration limits.

## Intake Defaults

If the user asks broadly, do not stall on a long questionnaire. Ask one compact set of questions or proceed with explicit assumptions:

- What domain or real-world process should this simulate?
- What will consume the data: a product, AI model, agent, search index, dashboard, training pipeline, or human workflow?
- Should I create only source-like synthetic artifacts, or also held-out eval/test inputs with labels?
- What imperfections should be present: contradictions, stale records, missing fields, noise, duplicates, biased distributions, adversarial prompts, edge cases?
- What scale and formats are needed?

## Deep Research Requirements

Always include a research phase in the plan and complete the real-example profile before generation. Scale the source depth to the risk:

- **Light research:** terminology, artifact examples, common schemas, and public samples.
- **Standard research:** source examples, workflows, realistic distributions, edge cases, and validation criteria.
- **Deep research:** primary sources, current rules/standards, recent examples, SME-like plausibility checks, and citation/provenance notes.

For simulation-heavy or population tasks, research also includes credible open-source generator candidates, their actual repositories/documentation, licenses, maintenance state, assumptions, export formats, deterministic controls, and fit gaps. Framework discovery is part of calibration, not a post hoc implementation convenience.

For domains such as law, medicine, finance, cybersecurity, regulation, public policy, or current product APIs, verify current facts before relying on them.

## Parallelization Pattern

When authorized, prefer this shape and native `spawn_agent` workers when available:

- **Research agents:** collect source examples, schemas, terminology, edge cases.
- **Planner agents:** turn research into artifact plans and coverage matrices.
- **Generation workers:** draft artifacts in disjoint slices.
- **QA agents:** audit realism, schema validity, coverage, leakage, and planned imperfections.
- **Repair workers:** apply scoped fixes from QA.
- **Coordinator:** maintains manifests, inventories, README, and final validation.

For large batches, split recursively. Example: one agent assigned 50 artifacts can spawn or be replaced by 5 workers handling 10 artifacts each, provided write scopes do not overlap.

## Quality Gates

Before delivery, run applicable checks:

- output tree summary and file counts;
- schema/format validation for JSON, CSV, DOCX, XLSX, HTML, logs, or custom records;
- native-document validation for real file containers, OCR/scanned variants, corruption/error variants, and extraction-hostile formatting where relevant;
- visual render checks for long or layout-sensitive PDFs: run the canonical installed `audit_pdf_layout.py --strict` and preserve its command/exit code in the helper receipt; sample early, middle, and late pages plus every distinct page family, and reject overlap, clipping, repeated filler pages, unrealistic headers, tiny text forced into a narrow band, or unexplained top/bottom whitespace. Repair by reflowing real content or changing the document form, never by padding. A sparse final page needs a document-native reason, an explicit receipt note, and `--allow-sparse-final`; no continuation-page waiver exists;
- for fax/OCR, form-heavy, ruled, or table-heavy PDFs, never treat first-to-last pixel occupancy as proof of substantive density: full-width rules, borders, footers, and scan marks can create a false pass. Run a border-independent body-text or OCR-box density check and visually inspect every pilot page; every border-span warning is review-required;
- packet-family realism checks: case files share plausible IDs, dates, parties, filenames, lifecycle states, and cross-document references without copying private examples verbatim;
- modality checks: if the task claims image/audio/video/native-doc support, generated inputs must include actual usable media/native containers, not only indexes, captions, or transcript stand-ins;
- calibration conformance: generated file families, lengths, structures, register/layout, complexity, metadata, relationships, and planned imperfections stay within the measured target profile or document a justified deviation;
- generator provenance: simulation-heavy/population runs have a reasoned framework decision; selected frameworks are pinned to immutable commits, license-checked, executed from task-local isolated environments, seed/configuration reproducible, and covered by generator receipts;
- framework validity: smoke and target runs pass schema, state/label recomputation, lifecycle, distribution, base-rate, support-boundary, and seed-replay checks; framework defaults are not presented as client-specific prevalence or production realism without real-extract calibration;
- helper ownership: every claimed native/media modality has a selected specialist helper, generated artifact, validation evidence, and helper receipt; no generic worker silently bypasses an available helper;
- inventory/catalog paths exist;
- source artifacts are separated from held-out eval inputs and labels;
- source-stage integrity: expert annotations, late conclusions, or proposed remedies are absent from raw/source-like artifacts unless the target workflow actually exposes them; excluded enrichment is separately inventoried as an expert or eval layer;
- placeholder scan: `TBD`, `TBC`, `xxx`, `lorem`, fake IDs that should have been realistic;
- metadata scan: id/title/path/format/source role/eval role/version/time period/domain/labels;
- realism QA: terminology, workflows, distributions, contradiction plausibility, stale-data plausibility, and non-template variation;
- conversation QA when applicable: every later session opener works as a fresh start, semantic labels match the full labeled utterance, and controlled time expressions are timeline-consistent and varied by context rather than mechanically uniform;
- leakage QA: answer keys, expected outputs, labels, or solution hints do not appear in raw inputs;
- validation exceptions are exact-path, reasoned, and reported; broad wildcard suppression is prohibited;
- reference integrity: host schemas remain valid and source-citing claims resolve through exact PDF text or deterministic workbook coordinates;
- provenance QA: raw upload/source files do not contain evaluator-facing synthetic/test notices such as "synthetic case packet", "fictional test data", "upload/eval testing", "expected outputs", or "held-out labels"; put synthetic provenance in README, inventories, and QA reports instead;
- final README explains directory-level usage.
- `scripts/audit_calibration_contract.py <output_dir>` passes, or every blocked/proxy exception is explicit and user-authorized.
- planning-phase calibration audit passes before generation, delivery-phase calibration audit passes before packaging, and the shareable archive passes allowlist/privacy/integrity/hash checks.
- execution routing is derived from measured difficulty, fast lanes have strong validators and escalation triggers, and independent reviewers are balanced/frontier rather than fast.

## Packaging Recommendation

Adapt names to the domain, but default to:

```text
output/
  README.md
  inventories/
  source_artifacts/
  scenario_packs/
  eval_sets/
    raw_inputs/
    labels_or_answer_keys/
  qa_reports/
```

Use source-like artifacts for ingestion/training/context, scenario packs for end-to-end workflows, and eval sets as held-out query/test inputs.
