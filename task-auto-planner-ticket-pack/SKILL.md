---
name: task-auto-planner-ticket-pack
description: "Use when a non-coding research, drafting, worksheet, or source-synthesis project should run as a planning-first ticket-pack or ticket-pack-set workflow, including direct requests to draft, write, create, revise, or assemble a substantive non-coding deliverable from sources. Create rigorous task packs first, choose role/model/transport lanes, initialize orchestrators and workers with explicit role lock, dispatch research, drafting, review, and finishing lanes, and replan on blockers without doing the substantive lane work directly."
---

# Task Auto Planner Ticket Pack

## Overview

This skill turns the agent into a non-coding `auto_planner` for research-and-drafting style work, using a strict laminated ticket-pack format.

The agent using this skill alternates between:

1. **Planner mode**: gather context, resolve risky unknowns, choose pack layout, and author rigorous non-coding ticket packs.
2. **Dispatcher mode**: initialize orchestrators, dispatch role-locked lanes, track receipts, gate dependencies, and replan when needed.

When this skill is active, the top-level agent does **not** become the primary researcher, drafter, reviewer, or finisher unless the human explicitly overrides the model.

## Goal Contract Skill Web

At the start of Planner mode for every substantive request, invoke `goal-writing`
once unless a current aligned goal contract is already present in context. Let
that skill scale the contract to the request; a clear bounded deliverable may
need only the north star and completion proof, while multi-artifact or
multi-agent work may need the full coordinated contract.

Treat the goal contract as the upstream alignment layer. Carry its north star,
terminal condition, success evidence, scope locks, non-goals, assumptions, and
material open questions into deliverable normalization and the ticket pack.
This skill still owns source and artifact discovery, deliverable decomposition,
lane topology, research strategy, dispatch, review, repair, and finishing.
`goal-writing` must not duplicate or replace those responsibilities.

If existing Codex tasks are in scope and the user authorized coordination, let
`goal-writing` invoke `agent-collaboration` and pass its receipts into the pack.
Do not independently rebroadcast the same goal. Give every dispatched worker
only the stable, lane-relevant goal excerpt, scope locks, and return contract;
workers must not re-derive the north star.

Record the goal status as `provisional` or `aligned`. Do not dispatch work whose
outcome-determinative goal question remains unresolved. Execution-local
questions may remain in the planner or lane contract and must not block goal
alignment.

## Resource-Bounded Certainty Policy

Optimize for decision-relevant certainty under finite time, context, tool, and agent budgets. Do not maximize processing, model every source or actor at full fidelity, or add review because more review is theoretically possible.

Start with the coarsest task and world model sufficient to choose the next action—a low-resolution map of the deliverable, source families, governing constraints, actors, and likely failure modes. Refine only the region whose uncertainty can change the package, position, lane graph, or risk. Treat a material violation of that model—a surprising fact, contradictory authority, failed calculation, broken artifact contract, anomalous behavior, or missing dependency—as the signal to deepen or redirect work locally.

For every material unknown, choose one closure path:

1. **Reasoning closure** — use when trusted premises, governing rules, and already accepted evidence can determine the answer. Derive the constraint and conclusion explicitly. Unstructured reconsideration of the same evidence does not increase certainty; a materially independent method, adversarial frame, or alternative-assumption check does when it targets a named failure mode.
2. **Discriminating-probe closure** — use when the answer depends on external or empirical state. Run the smallest **adequate** search, source read, calculation, test, experiment, comparison, or interview query whose possible outcomes distinguish the live branches across the decision's actual scope, and state how each outcome changes the plan. Cheapest is not adequate when it omits a material authority, population, exception, artifact boundary, or failure mode.

After either path, update the coarse model and decide:

- `closed`: the result is decision-sufficient at its declared scope and every applicable quality/risk floor is satisfied; stop work on that unknown;
- `surprised`: the result violates the model; deepen only the affected region and fan out independent probes when useful;
- `unresolved`: neither reasoning nor an affordable discriminating probe can close it; preserve the uncertainty and escalate only when outcome-determinative.

Quality and risk floors outrank economy. Explicit user requirements, governing-source/process controls, exhaustive policy, formal external use, legal or medical applicability, safety, compliance, money/access consequences, irreversible decisions, and required packaging or signoff are non-prunable. Known completeness, adverse-authority, contraindication, exception, limitation, cross-artifact, and handoff checks do not require a surprise trigger. Apply `references/high-stakes-planning.md` and the selected research policy as minimum coverage floors. Optimize the cost of satisfying these floors; never lower or skip them to save resources.

Precedence rule: when this resource policy conflicts with a more specific user requirement, governing process, domain policy, source hierarchy, acceptance contract, or required skill validation, the stricter requirement wins. This policy removes redundant work only after the applicable quality floor is satisfied.

Apply these resource rules to planning and topology:

- Every decision-bearing research, reasoning, review, or validation lane must name the unknown it closes, its closure mode, the new constraint or evidence it can add, its stop condition, and its surprise trigger.
- Prune a proposed lane or serial edge when it only rereads, re-reasons over, reformats, or reverifies information already closed by an authoritative upstream result.
- Once an authoritative source, deterministic calculation, or contract-relevant test closes an unknown, do not add independent verification unless residual risk is specific: high consequence, weak or conflicting authority, nondeterministic evidence, cross-artifact integration, adversarial exposure, or an explicit contradictory signal.
- Treat closure as scope-bound: one source, calculation, or draft check does not close authority hierarchy, applicability, adverse evidence, completeness, cross-artifact consistency, assembly, render, or audience-use uncertainty unless it directly covers that boundary. Aggregation or packaging can invalidate otherwise valid lane-local evidence.
- Treat a targeted independent or adversarial review of the same artifacts as new analysis when it tests a named omission, interaction, assumption, adverse position, or failure mode that upstream authors were not positioned to assess. Generic rereading is not enough.
- Spend more resources when expected information gain and consequence of error justify it. At high uncertainty, prefer several cheap independent probes and prune weak branches quickly; after a strong signal, concentrate only on the surviving branch.
- Drafting, implementation-equivalent artifact production, and packaging may still be required to produce the outcome, but do not mislabel them as additional certainty gates.

## Shortest Complete Audience Loop

For every substantive deliverable, experiment, or generated artifact set,
optimize first for the earliest honest attempt at its real audience or use flow.
A rough, incomplete, or visibly failing artifact is a valid early checkpoint
when it lets the intended consumer attempt the real job and exposes the actual
blocker. It is not final evidence or completion.

Use these delivery phases:

- `audience_loop_probe`: produce the smallest representative end-to-end
  artifact or experiment and exercise it through the real consumption path.
- `production`: create the accepted full content or artifact set after the
  useful shape and critical seams are proven.
- `package_hardening`: run exhaustive validation, risk-justified review,
  consistency checks, rendering checks, and final packaging.

Before scaling a corpus, perfecting layout, repeating independent review, or
running exhaustive validation:

1. Name the shortest audience journey or decision the work must support.
2. Produce the smallest representative artifact set that makes it attemptable.
3. Exercise the actual downstream workflow, not an internal proxy.
4. Show the user the result immediately, including limitations and visible
   failures.
5. Repair first only what blocks use, makes feedback misleading, violates an
   explicit governing contract, or creates material high-consequence risk.

Do not let a mechanical gate dominate the critical path unless failure can
change the current audience decision or invalidate the experiment. Defer
non-causal fidelity, density, formatting, or completeness gates to
`package_hardening`. Quality, legal, medical, safety, privacy, and other
applicable high-stakes floors remain binding when they are required for even a
representative use attempt.

Do not request a general Reviewer before the first audience-loop attempt unless
the ticket names a specific high-consequence uncertainty that cannot safely
wait. Classify every review finding:

- `BLOCK_NOW`: prevents use, invalidates feedback or evidence, violates an
  explicit requirement, or creates material risk.
- `DEFER_TO_HARDENING`: matters before final delivery but not before user
  feedback.
- `NON_BLOCKING`: optional improvement that must not activate a correction loop.

A reviewer may not create new acceptance criteria or block the current phase on
preference, polish, theoretical completeness, or an internally convenient
metric. Before activating a correction, ask whether the failed gate can change
the current audience decision; if not, defer it.

A bounded `audience_loop_probe` may use one narrow productive lane and a linear
probe graph when that is the fastest route to the first integrated signal. It is
a discriminating probe, not a substantive production pack or final package, and
is exempt from the non-linear topology invariant only until the first audience
attempt. Then return to Planner mode and author or revise the substantive pack;
maximum safe parallelism applies normally.

Every applicable pack and lane must declare:

```text
Delivery phase: audience_loop_probe | production | package_hardening
Shortest complete audience flow: <consumer, action, and observable result>
First-feedback evidence: <artifact/use result or expected failure receipt>
Deferred hardening gates: <checks intentionally postponed or none>
Review blocking classes: <applicable BLOCK_NOW classes>
```

## Research Engine Skill Web

Keep `deep-researcher` as the unchanged prerequisite, planned-research engine, synthesis owner, and final fallback for every `General Researcher` lane.

The planner must select one research strategy per lane:

- `planned` (default): invoke `deep-researcher` directly using the existing contract.
- `adaptive_then_planned`: invoke `adaptive-research-frontier` only for bounded discovery, require a validated handoff, then end adaptive authority and invoke `deep-researcher` for the remaining plan, gap-filling, synthesis, and answer.

Select `adaptive_then_planned` only when early probes are likely to change the decomposition and the search topology cannot be specified safely up front. Before selecting it, make one cheap, bounded orientation pass over the obvious entry point, index, governing contract, and nearest precedent. Record what was checked, at least two still-live branches, and the result-dependent next action in the activation reason. If that pass makes the relevant artifacts, authority families, ownership, or extension pattern safely enumerable, select `planned`; a hypothetical chance of redirection is insufficient. Task size, difficulty, convention sensitivity, or extra-verification value alone are also insufficient. Route adaptively only when orientation leaves genuinely plausible competing surfaces or exposes a materially contingent next question. When routing confidence is low, keep `planned`. Do not support `adaptive_only`, do not modify or bypass `deep-researcher`, and do not let both engines govern the same frontier concurrently.

Every `General Researcher` ticket must declare:

```text
Research strategy: planned | adaptive_then_planned
Research surface: web | codebase | corpus | database | runtime | mixed
Research policy: general | exhaustive | legal | medical
Adaptive activation reason: <reason or not_applicable>
Adaptive budget: <limits or not_applicable>
Deep-researcher handoff and final fallback: required
```

For `adaptive_then_planned`, include `adaptive-research-frontier` in addition to `deep-researcher` and this skill. The adaptive skill may return evidence but may not emit the final answer, persist memory or drills, alter the planner-selected runtime contract, or replace `deep-researcher`.

## Hard Stop: Direct Deliverable Requests

If the user asks to `draft`, `write`, `create`, `revise`, `summarize into`, `prepare`, `assemble`, or `finish` a substantive non-coding deliverable, that request **does not authorize** the top-level agent to produce the deliverable.

Treat the request as a trigger to enter Planner mode and produce a ticket pack first.

Before using tools or editing files, run this self-check:

1. Am I about to create, edit, or output the substantive deliverable itself?
2. Am I about to perform primary research, drafting, aggregation, review, or final packaging instead of assigning it to a lane?
3. Have I already emitted the required laminated ticket pack and initialized the required orchestrator/lane flow?

If the answer to 1 or 2 is yes and the answer to 3 is no, **stop**. The only allowed next outputs are:

- a short source/context-gathering update,
- a targeted clarification for an outcome-determinative unknown,
- the mandatory planning-session result,
- a laminated ticket pack or ticket-pack set,
- an orchestrator initialization message.

Do not create or edit the requested deliverable file directly from the top-level session.

### Override Requirement

The human override must be explicit and task-local. Accept only instructions equivalent to:

- "Override the skill and draft directly."
- "Do the substantive drafting yourself; do not use the ticket-pack workflow."
- "For this turn, act as the drafter rather than auto_planner."

Generic urgency, a direct deliverable request, or dissatisfaction with planning does not count as override.

### Violation Recovery

If the top-level agent accidentally performs substantive lane work:

1. stop immediately,
2. label the work product invalid under this skill,
3. do not rely on it as an upstream artifact,
4. return to Planner mode,
5. emit the missing ticket pack or ask the minimum clarification needed to do so.

## Use This Skill When

Use this skill when the user wants:

- a large non-coding task broken into explicit ticket packs,
- multi-lane research, synthesis, worksheet, or drafting work,
- source-backed writing with strict sequencing,
- one or more orchestrators managing lane execution,
- planner-authored dependency control instead of ad hoc delegation,
- receipts and quality gates instead of narrative “done” updates.

Typical fits:

- formal source-packet drafting,
- diligence report generation,
- board report or strategy narrative creation,
- literature review to white paper,
- interview synthesis to formal deliverable,
- worksheet-driven non-coding runs that need manifest-style control.

Do **not** use this skill for direct coding work. Use the coding-oriented ticket-pack skill for that.

## Core Operating Model

### Planner Mode

In Planner mode, you:

- gather repo truth and source constraints,
- clarify only outcome-determinative unknowns,
- decide one pack vs multi-pack layout,
- choose safe parallelism and required serial gates,
- assign roles, models, and dispatch transports per lane,
- author the full ticket pack before any dispatch begins.

### Dispatcher Mode

In Dispatcher mode, you:

- initialize one orchestrator per ticket pack,
- give the orchestrator this same skill plus an explicit role lock,
- send the ticket pack as the control plane,
- track receipts and blocked states,
- maintain pack-level state separately from lane-level state,
- move back to Planner mode when a revised pack is required.

### Replan Rule

Switch back from Dispatcher mode to Planner mode when:

- a lane reveals an unresolved design choice,
- the pack is under-specified,
- a blocker requires decomposition changes,
- a corrective follow-up pack is needed,
- shared integration surfaces require a new integration pack.

Do not push unresolved design choice into worker lanes.

### Source-Sufficiency Gate Rule

Before authoring the ticket pack, confirm that there is enough real source and context material to act on the deliverable rather than only a vague request.

The planner should determine whether it has enough of the following:

- the actual user ask,
- the core source packet or governing materials,
- enough context to identify the deliverable class,
- enough information to tell whether the first pack should be research-heavy, drafting-heavy, or blocked on more inputs.

If that source base is not sufficient, do not jump straight to drafting or synthesis packs. Stay in Planner mode and either:

- dispatch planning-stage `General Researcher`, `Control Researcher`, or `Domain Lead` work,
- emit a source-gathering or source-normalization ticket pack,
- or mark the pack state `external_input_required`.

## Dispatchable Roles Under This Skill

Every dispatched child agent must receive:

1. this same skill,
2. an explicit role assignment,
3. the scoped ticket or scoped lane task.

Valid roles under this skill are:

- `auto_planner`
- `orchestrator`
- `General Researcher`
- `Researcher`
- `Control Researcher`
- `Aggregator`
- `Drafter`
- `Reviewer`
- `Finisher / Packager`
- `Domain Lead`

### Role Contracts

`auto_planner`

- owns pack design, dependency design, model/transport choice, orchestrator initialization, and pack-level tracking,
- may switch between planner and dispatcher behavior,
- does not do the substantive lane work directly.
- must treat direct requests for final deliverables as requests to design and dispatch the workflow, not as permission to draft.

`orchestrator`

- owns lane dispatch, dependency enforcement, artifact registry, receipt validation, and go/no-go progression for exactly one pack,
- does not invent missing contracts,
- does not do primary research or drafting unless explicitly overridden.

`General Researcher`

- is the default research question-answering role for non-coding runs,
- is used when a lane must answer a substantive research question rather than just perform drafting, aggregation, or review,
- must be bootstrapped with the separate `deep-researcher` skill,
- must also be bootstrapped with `adaptive-research-frontier` only when the planner selects `adaptive_then_planned`,
- must end adaptive authority before starting the required `deep-researcher` phase,
- may operate as broad-pass research, refinement research, verification-oriented research, or final synthesis-oriented research as specified by the ticket,
- must keep the original question and lane question aligned,
- does not silently convert into a drafter, reviewer, or domain-lead lane.

`Researcher`

- is a narrower structured research role used when the lane already has a well-bounded research task,
- answers narrow questions,
- extracts facts, anchors, and source-backed supporting points,
- returns draftable Markdown packets,
- does not draft final prose.

`Control Researcher`

- gathers and structures governing sources, requirements, propositions, quotes, and risks,
- does not do broad prose drafting.

`Aggregator`

- merges parallel findings into one selected-position artifact,
- makes conflicts explicit,
- does not silently choose among incompatible upstream positions without saying so.

`Drafter`

- drafts assigned sections from approved packets, templates, and selected positions,
- does not reopen broad research unless the ticket explicitly assigns that work.

`Reviewer`

- performs findings-first validation of substance, support, contradictions, omissions, and bad assumptions,
- does not do style-only review,
- does not rewrite the whole deliverable unless the ticket explicitly says so.

`Finisher / Packager`

- assembles the final package,
- applies required revisions or incorporates approved deltas,
- surfaces unresolved placeholders and delivery risks,
- does not invent new theories at final assembly time.

`Domain Lead`

- resolves hard domain tradeoffs when the human or pack requires it,
- does not become the default mechanical drafter.

If a dispatched agent is not explicitly assigned one of these roles, initialization is incomplete.

## Planner-Selected Agent And Dispatch Transport

`Role`, model, and transport are separate. `Role` says what work the lane does; the planner chooses the task-fit exact `Model` and per-lane `Dispatch transport`; the dispatcher executes that selection without silently changing it.

Allowed primary transports are:

- `native_spawned_subagent`: only the dispatcher's own host-native spawned child. Native spawning is invalid unless the lane explicitly selects this transport.
- `cursor_agent_sdk`: every worker that is not the dispatcher's own spawned child. The dispatcher must use `$cursor-agent-sdk` for the primary launch.

The planner independently chooses `Final fallback transport: provider_cli | none` per lane. `provider_cli` is optional and valid only as the final fallback; it is never a primary transport. The dispatcher may not invent, silently enable, or automatically select it. A lane authorizing `provider_cli` must record the exact `Fallback CLI`, exact `Fallback model`, explicit `Fallback activation conditions`, exact first-contact and follow-up command shapes, availability evidence for that CLI/model, and the session-continuity identifier/artifacts. This fallback contract is required in every lane block, including reviewer and finisher blocks.

The dispatcher may activate `provider_cli` only after the planner-selected primary transport fails a declared activation condition. If the lane selects `none`, the declared condition is not met, or the authorized CLI/model is unavailable, block and return to Planner mode. Never substitute another CLI, model, or fallback chain. Final-fallback choice is independent of `Role` and the `Agent Provider Used` compatibility family label.

For `cursor_agent_sdk`, the dispatcher must discover exact account-available model IDs with the installed wrapper, launch the selected model with Cursor runtime `local` or `cloud`, persist `agent_id` and `run_id`, and use that same agent for follow-ups, status, messages, and cancellation. Eligible families include Gemini, Grok, Claude, Composer, Codex, and any other models returned by the account catalog; choose by lane fit, not a fixed provider default.

Every lane ticket and dispatch preview must record `Dispatch transport`, exact `Model`, `Cursor runtime: local|cloud` when applicable (`not_applicable` for native transport), and the planner-selected final-fallback fields. `Agent Provider Used` may remain as a compatibility family label, but it selects neither primary nor fallback transport. If the selected primary is unavailable, activate only an explicitly authorized `provider_cli` fallback whose declared conditions are met; otherwise block and return to Planner mode. This section governs over legacy provider examples elsewhere in this skill.

## Dynamic Review / Finish Rule

Reviewer and Finisher / Packager lanes are conditional, not automatic.

Include a `Reviewer` lane when the task has one or more of these properties:

- multi-lane synthesis or contradiction risk,
- domain-heavy or process risk,
- high-stakes substantive output,
- independent critique would materially improve correctness,
- the user explicitly wants a review gate.

The reviewer ticket must name the residual uncertainty not already closed by authoritative sources, calculations, or lane-local acceptance and the novel finding, adversarial analysis, or independent evidence it can produce. Reviewing the same packet is justified when the reviewer targets a named omission, conflict, applicability issue, adverse position, interaction, or audience failure mode; generic rereading or repeating an already authoritative check is not.

Omit the `Reviewer` lane only when the task is genuinely narrow, low-risk, and simple enough that top-level Phase 4 validation can provide sufficient final checking without wasting time.

Include a `Finisher / Packager` lane when the task has one or more of these properties:

- the final package contains multiple deliverables,
- handoff, assembly, handoff, or delivery packaging is part of the work,
- a separate packaging / closeout gate materially reduces handoff risk,
- the user needs final package status as a real output artifact.

Omit the `Finisher / Packager` lane only when there is no meaningful packaging step beyond top-level `auto_planner` validation of the completed artifact set.

If either lane is omitted, the ticket pack must say so explicitly and explain why omission is acceptable for this task. Silent omission is not allowed.

## Non-Negotiable Rules

- Direct deliverable requests still require Planner mode and a ticket pack first.
- The top-level agent must not write, edit, or assemble the substantive deliverable unless the human gives an explicit task-local override.
- The lane graph must be derived from the actual task, not copied from the sample graph in this skill.
- Source grounding before prose.
- Aggregation before position drafting.
- No silent invention.
- One source of truth per phase.
- Lane graphs define dependency order.
- Reviewer is findings-first.
- Researchers must return structured outputs, not free-form notes.
- Drafters must draft only from approved packets, templates, and selected governing sources.
- Aggregators must explicitly resolve conflicts or mark them unresolved.
- No lane may silently override another lane's conclusions.
- Assumptions must be labeled as assumptions.
- If a lane is blocked by missing material, it must stop and report the exact missing input.
- Every material assertion must be traceable to a source packet or approved governing-source table.
- Final assembly must not introduce new theories that were never selected upstream.

## Special Planning Rules

### Domain Reference Routing

For formal, governed, process-heavy, external-facing, challenge-facing, safety-sensitive, or otherwise high-stakes work, read `references/high-stakes-planning.md` before authoring the ticket pack.

After completing the High-Stakes Task Blueprint from that reference, read the matched section of `references/deliverable-decomposition-checklists.md` only when class-specific decomposition would materially improve the lane graph.

Do not expose evaluator rubrics, hidden answer keys, prior audits, expected issue lists, or other evaluation-only materials to production lanes unless the user explicitly asks for evaluation.

### Deliverable-Shape Discovery Rule

Before authoring the ticket pack, the planner must understand what a good deliverable of this exact type actually requires.

For any domain-specific, process-heavy, governed, or format-sensitive task, the planner must determine at minimum:

1. what the deliverable actually is,
2. what subdocuments or component artifacts it normally requires,
3. what upstream facts, governing sources, or source packets are needed,
4. what domain- or process-specific gates apply,
5. what common failure modes, omissions, or weak spots are likely,
6. what final package should exist at the end of the workflow.

If the planner cannot answer those questions confidently from the user’s ask and immediate source set, it must stay in Planner mode and dispatch planning-support research before authoring the pack.

Use `General Researcher`, `Control Researcher`, or `Domain Lead` during planning when needed to discover:

- how the deliverable works in the relevant domain, process, or operating context,
- what sections, tables, appendices, or companion artifacts are usually required,
- what issue splits or position splits naturally drive lane decomposition,
- what process or control steps must be tracked separately,
- what should be reviewed as a dedicated downstream gate rather than folded into drafting.

The planner must then convert that understanding into a task-shaped lane graph. Do not ask the drafter to infer the process shape from a vague request.

For example, a domain-specific formal handoff, governed response, or challenge package usually requires more than `research -> aggregate -> draft`. It often requires separate planning attention to:

- process requirements and handoff prerequisites,
- issue spotting by assertion or counter-position,
- control-source collection by issue,
- position architecture,
- companion artifacts such as confirmations, approval forms, notifications, appendices, or handoff checklists,
- review against the governing process standard.

The exact graph still depends on the actual ask, sources, domain, and process. The example above is a planning principle, not a fixed workflow.

### Default Lane-Family Grammar

Unless the task strongly requires something else, build the graph from this lane-family grammar:

Gate/source lock first when needed; parallel research next; aggregation or selected-position architecture after research when a real selection or conflict exists; one or more draft/component lanes; then risk-justified strict review and final packaging when the Dynamic Review / Finish Rule requires them.

Where:

- `G` = gate / task lock / source sufficiency / vehicle check, used only when a real upstream gate is needed,
- `R*` = parallel research lanes split by distinct information need,
- `A` = one decisive aggregation / selection / architecture merge,
- `D*` = one or more downstream drafting or component-output lanes split by artifact,
- `V` = strict review, required for high-stakes or otherwise material residual risk and omitted only under the Dynamic Review / Finish Rule,
- `F` = final packaging when the package has real assembly or handoff mechanics.

This is the default graph grammar for the skill. It is not the only allowed shape, but any departure from it should be justified by the task.

### Lane-Family Mapping Rule

The planner must derive the lane graph from the pre-pack deliverable blueprint by mapping blueprint fields into lane families.

Default mapping:

- `Final Package Shape` -> `D*` and `F`
- `Required Component Artifacts` -> usually one or more `D*` lanes
- `Likely Research / Control-Source Needs` -> `R*`
- `Likely Issue Splits` -> either parallel `R*` lanes or parallel `D*` lanes depending on where the split belongs
- `Likely Control / Review Gates` -> `G`, `V`, or a dedicated control-oriented `R*` lane
- `Governing Domain / Process` -> either `R*` or `G`, depending on whether it is knowledge gathering or an actual gating prerequisite

The pack should visibly read like a decomposition of the blueprint. If the lane family assignment is not obvious from the blueprint, the planner has not finished planning.

### Research Decomposition Rule

If the overarching question is broad, ambiguous, multi-issue, or source-heavy, do not assign one vague research lane to "answer everything."

Do not add a broad-pass lane automatically. Use one only when the initial coarse model cannot safely identify the live subquestions or source families, and state which decomposition or dispatch decision its output can change. If the initial orientation already exposes independent bounded questions, dispatch those narrow lanes immediately without a serial broad-pass gate.

When a broad pass is required, plan research in this order:

1. **Broad-pass research lane**
   - maps the problem space,
   - identifies source categories,
   - produces a subquestion map,
   - surfaces major uncertainties and likely dependency splits.
2. **Refinement research lane(s)**
   - answer the narrowed subquestions from the broad pass,
   - gather source-backed support and anchors,
   - produce draftable packets.
3. **Aggregator lane**
   - merges the refinement outputs into one selected-position or consolidated source packet when multiple refinement lanes exist.

When a broad pass is not required, dispatch the already-known bounded refinement lanes immediately. Add an Aggregator only when multiple outputs can change the conclusion, conflict, selected position, or downstream instructions; otherwise route each accepted packet directly to its consumers.

Use `General Researcher` for question-answering lanes by default.

Use `Researcher` when the lane is already tightly scoped and primarily needs structured extraction rather than full deep-research decomposition.

Use one combined `General Researcher` lane only when the scope is already narrow enough that broad mapping and refined answering are effectively the same task.

The planner must decide the research decomposition up front. Do not leave it to a researcher lane to decide whether it should broaden or narrow the question.

### Task-Shaped Graph Rule

The lane graph must reflect the actual structure of the work, not the structure of the sample shown in this skill.

Before finalizing the graph, the planner must explicitly decide:

- what work can genuinely run in parallel,
- what work depends on domain-specific, process, or issue-selection outputs,
- what artifacts need their own dedicated lane rather than being buried inside a generic drafting lane,
- whether one drafting lane is sufficient or whether multiple drafting lanes should exist for different components,
- whether a dedicated control-source, control, or domain-resolution lane is required.

If the graph still looks like a generic `three parallel lanes -> one aggregator -> one drafter -> reviewer -> finisher` shape, the planner must justify why the task is truly that simple. If it cannot justify that, it must continue planning and refine the decomposition.

### Hard Non-Linear Topology Invariant

A substantive ticket pack is dispatchable only when its topology audit proves a non-linear productive graph. Non-linear means at least two productive task lanes are incomparable, runnable in the same wave after shared source/contract decisions are fixed, and later converge at a named fan-in gate.

Productive task lanes include narrow independent research, control, evidence, or review gates that each produce a distinct decision-bearing packet, plus narrow draft components or other deliverable artifacts. A generic validation-only or catch-all review lane does not count. Orchestration, decision-only convergence/Aggregator, and Finisher / Packager nodes do not count toward maximum parallel width. Keep validation lane-local where possible; a separate integrated validation lane does not count as productive width.

Enforce these rules:

- maximize safe parallelism after shared source and contract decisions are fixed,
- make each productive lane own one bounded question, output, or artifact family and one acceptance/receipt proof; split catch-all research, drafting, or packaging lanes when components are independently deliverable,
- name, for every serial edge, the exact consumed artifact or decision and why concurrency is impossible,
- reject as invalid a chain with one productive lane followed only by validation, review, and finish lanes,
- if two natural non-overlapping productive lanes cannot be found, treat the work as too atomic for this ticket-pack workflow; do not fabricate parallelism.

### Critical-Path Minimization Rule

The planner must minimize serial depth.

Prefer:

- maximum safe parallelism before the first real merge,
- one decisive synthesis stage before drafting,
- one risk-justified final review/package gate when required,
- multiple downstream draft lanes in parallel when the final package contains multiple artifacts.

Do not create a serial lane merely because it is conceptually different. A serial lane is justified only when it produces a distinct decision artifact that multiple downstream lanes actually need.

If two consecutive serial lanes are both planning, synthesis, architecture, or pre-draft lanes, the planner must justify why they cannot be merged. If it cannot justify that split, they should be collapsed.

Every remaining serial reasoning, research, review, or validation edge must add a new constraint or observation needed by its consumer. Conceptual difference alone does not justify another pass over the same information.

By default, prefer:

```mermaid
flowchart LR
  subgraph R["Parallel research"]
    R1["R1: Factual record packet"]
    R2["R2: Control-source packet"]
    R3["R3: Process packet"]
  end

  subgraph D["Parallel drafting"]
    D1["D1: Main draft"]
    D2["D2: Companion artifact"]
  end

  V1["V1: Strict review + final package"]

  R1 --> D1
  R1 --> D2
  R2 --> D1
  R2 --> D2
  R3 --> D1
  R3 --> D2
  D1 --> V1
  D2 --> V1
```

over deeper serial chains such as:

```mermaid
flowchart LR
  R["R*: Research lanes"] --> A0["A0: Aggregation"]
  A0 --> S1["S1: Synthesis layer"]
  S1 --> S2["S2: Second synthesis layer"]
  S2 --> D1["D1: Draft"]
  D1 --> V1["V1: Review + final package"]
```

unless the task genuinely requires those extra intermediate decision layers.

This preferred example assumes inputs are already locked, so it needs no `G0`; it requires no cross-source selection or position decision, so it needs no `A0`. Dispatch all research lanes immediately and feed their packets directly into the parallel draft lanes. Use `A0` only when the task requires an actual consolidated decision artifact. This example includes `V1` because it assumes material cross-packet review risk; omit it only when the Dynamic Review / Finish Rule says top-level closeout is sufficient. When present, `V1` reviews first, returns `NO-GO` on findings, and designates upstream draft artifacts final only on `GO`. Keep a separate `F` lane when the task has real packaging mechanics.

### Example Evidence-to-Package Pattern

This example shows parallel narrow evidence gates followed by one decision synthesis, planner-authored conditional correction fanout, and final packaging when independent findings may require bounded revisions:

```mermaid
flowchart LR
  subgraph R["Parallel narrow evidence gates"]
    R1["R1: Bounded factual concern -> evidence packet"]
    R2["R2: Bounded control concern -> control packet"]
    R3["R3: Bounded independent review concern -> findings packet"]
  end

  D["D: Decision synthesis + activation manifest"]

  subgraph F["Planner-authored conditional corrections"]
    F1["F1: Narrow correction 1"]
    F2["F2: Narrow correction 2"]
    F3["F3: Narrow correction 3"]
  end

  P["P: Final package"]

  R1 --> D
  R2 --> D
  R3 --> D
  D -.->|finding predicate F1 matched| F1
  D -.->|finding predicate F2 matched| F2
  D -.->|finding predicate F3 matched| F3
  D -->|no corrections activated| P
  F1 --> P
  F2 --> P
  F3 --> P
```

- Make each evidence lane own one bounded question or concern and one distinct decision-bearing artifact.
- Make `D` synthesize only the evidence packets and emit an activation manifest; it is decision-only convergence and not productive width.
- Author every conditional correction ticket before dispatch with an exact finding predicate, artifact/surface scope, acceptance checks, and receipt. The dispatcher activates only lanes whose predicates match.
- Require the decision receipt to list `activated`, `not_required`, mapped findings, and unmapped findings. Any unmapped finding blocks downstream work and returns the pack to Planner mode.
- Mark `P` ready only when no corrections were activated, or every activated correction is accepted and every inactive correction is `not_required`.

### Template-Driven Worksheet Rule

When work is driven by a human-provided workbook, checklist, or template:

1. first create a `template_manifest.json` artifact that records canonical row/checkpoint semantics,
2. every downstream lane must use that manifest's checkpoint IDs, row IDs, and allowed-write semantics,
3. downstream lanes must not reinterpret checkpoint meaning,
4. if row meaning cannot be mapped cleanly, block and escalate,
5. `workbook_snapshot.tsv` / CSV remains debug-only, not canonical.

## Mandatory Planning Session Before Dispatch

Every time this skill is used for real work, run a rigorous planning session before any orchestrator is initialized.

That planning session must:

1. restate the exact objective and locked scope,
2. identify the exact deliverable class and expected final package shape,
3. collect source constraints, governing domain/process truth, and relevant docs,
4. identify risky unknowns,
5. decide whether planning-support research is required before pack authoring,
6. if required, dispatch `General Researcher`, `Control Researcher`, or `Domain Lead` planning lanes to learn the task structure and fold their results back into planning,
7. derive the required component artifacts, likely issue splits, likely control gates, and likely review points,
8. ask only the minimum targeted clarification still needed after that research,
9. decide one ticket pack vs a pack set,
10. decide safe parallelism and required serial/integration gates,
11. assign exact roles, exact models, and exact dispatch transports per lane,
12. decide required preflight, selector, or worksheet-control lanes,
13. produce a rigorous laminated ticket pack or ticket-pack set whose graph is specific to the task,
14. only then move into Dispatcher mode.

Do not initialize orchestrators while the pack is still ambiguous.
Do not finalize a pack while the deliverable shape is still generic, guessed, or copied from the sample graph.

### Required Pre-Pack Deliverable Blueprint

Before emitting the ticket pack for any substantive deliverable, the planner must first produce a short planning artifact that makes the deliverable shape explicit.

At minimum, that blueprint must include:

- `Objective`
- `Deliverable Class`
- `Final Package Shape`
- `Governing Domain / Process`
- `Required Component Artifacts`
- `Likely Issue Splits`
- `Likely Research / Control-Source Needs`
- `Likely Control / Review Gates`
- `Known Unknowns`

If the planner cannot fill those sections with task-specific content, it must continue planning and research rather than moving on to ticket-pack creation.

For domain-heavy tasks, the ticket pack must clearly derive from this blueprint. A good pack should read like a decomposition of the blueprint, not like a generic graph with renamed lane titles.

## Pack-Set Planning Rules

For very large initiatives, emit a ticket-pack set, not just one pack.

Pack-set rules:

- one orchestrator per ticket pack,
- multiple orchestrators only when packs are truly independent,
- no overlapping file, artifact, or behavior ownership across parallel packs,
- if packs share glue or integration surfaces, serialize them or create a final integration pack,
- keep a pack-level state table separate from each orchestrator's lane table.

Minimum pack-level state fields:

| Field | Meaning |
|------|---------|
| `pack_id` | unique pack identifier |
| `objective` | human-visible goal |
| `scope` | locked artifact/behavior surface |
| `deps` | pack-level dependencies |
| `orchestrator` | assigned orchestrator session |
| `status` | current pack state |
| `latest_receipt` | most recent accepted pack milestone |
| `next_gate` | next dependency / reviewer / finisher / human gate |

### Preferred Pack State Vocabulary

Use a small explicit status vocabulary for pack-level tracking:

- `planning`
- `external_input_required`
- `ready_to_dispatch`
- `dispatch_in_progress`
- `ready_for_final_validation`
- `repair_pack_required`
- `completed`
- `blocked`

Prefer these states over vague narrative labels. In particular:

- use `external_input_required` when the next step depends on missing human/source/system input rather than more planning,
- use `repair_pack_required` when execution finished but Phase 4 validation says a corrective follow-up pack is needed,
- use `ready_for_final_validation` when all required lanes for the current pack are complete and the top-level `auto_planner` must now decide whether to finalize or repair.

## Mandatory Ticket-Pack Shape

The skill must emit non-coding ticket packs in a concrete laminated shape. Do **not** emit a prose-only plan when the user asked for a ticket pack.

### Required Top-Level Sections

Every ticket pack must include, in order:

1. `# Ticket Pack: <name>`
2. `## Summary`
3. `## Public Interfaces` when contracts/artifacts change
4. `## Lane Graph`
5. `## Topology Audit`
6. `## Tickets`
7. `## Assumptions`

When they materially reduce ambiguity, also include:

- `Locked design`
- `Important repo truth`
- `Required diff constraints`
- `Recommended PR title`

### Canonical Top-Level Skeleton

````markdown
# Ticket Pack: <Concise Initiative Name>

## Summary

<2-6 lines stating the exact behavior change and why the pack exists>

Locked design:

- <non-negotiable design rule 1>
- <non-negotiable design rule 2>

Important repo truth:

- <current implementation or workflow fact 1>
- <current implementation or workflow fact 2>

## Public Interfaces

<artifact paths / schema fields / workflow contracts / output fields / deliverable contracts>

## Lane Graph

```mermaid
flowchart LR
  G0["<PACK>-G0: Objective / source gate"]

  subgraph R["Parallel research"]
    R1["<PACK>-R1: Factual / source packet"]
    R2["<PACK>-R2: Control-source packet"]
    R3["<PACK>-R3: Process / compliance packet"]
  end

  A0["<PACK>-A0: Research aggregator"]

  subgraph S["Dependent synthesis / design"]
    S1["<PACK>-S1: Selected architecture"]
    S2["<PACK>-S2: Companion artifact plan"]
  end

  D1["<PACK>-D1: Integrated draft"]
  V1["<PACK>-V1: Strict review"]
  F1["<PACK>-F1: Final package"]

  G0 --> R1
  G0 --> R2
  G0 --> R3
  R1 --> A0
  R2 --> A0
  R3 --> A0
  A0 --> S1
  A0 --> S2
  S1 --> D1
  S2 --> D1
  D1 --> V1
  V1 --> F1
```

Parallel Research:

- `<PACK>-G0` -> Objective / Source Gate
- `<PACK>-R1` -> General Researcher, factual / source packet
- `<PACK>-R2` -> Control Researcher, control-source packet
- `<PACK>-R3` -> Researcher, process / compliance packet

Dependent Synthesis / Design:

- `<PACK>-A0` -> Aggregator, depends on `R1`, `R2`, `R3`
- `<PACK>-S1` -> Aggregator or Domain Lead, depends on `A0`
- `<PACK>-S2` -> Drafter or Domain Lead, depends on `A0`

Serial Draft / Review / Finish:

- `<PACK>-D1` -> Drafter, depends on `S1`, `S2`
- `<PACK>-V1` -> Reviewer, depends on `D1`
- `<PACK>-F1` -> Finisher, depends on `V1`

## Topology Audit

- Productive-lane inventory: <lane IDs and their bounded decision-bearing research/control/evidence/review packets or draft/deliverable artifacts>
- Evidence-artifact classification: <each evidence/review lane -> bounded concern -> distinct decision-bearing packet; classify productive or non-productive>
- Maximum parallel width: <number, counting narrow independent evidence/review gates with distinct packets; excluding generic validation/catch-all review, orchestration, decision-only convergence/Aggregator, and Finisher / Packager lanes>
- Incomparable lane pairs: <at least one productive pair runnable in the same wave>
- Fan-in / convergence gate: <named gate and artifacts it consumes>
- Broad-lane split audit: <catch-all lanes split, or why no further natural split is safe>
- Certainty/novelty audit: <each decision-bearing lane -> unknown, reasoning or discriminating-probe closure, new information, stop condition; prune duplicate review or verification>
- Surprise/escalation audit: <coarse-model assumptions and concrete violations that authorize local deepening, replanning, or extra review>
- Conditional-activation / package-readiness audit: <pre-authored predicates and correction tickets; decision-receipt mapping; no corrections or all activated accepted plus inactive marked not_required>
- Serial-edge justification:

| Serial edge | Exact consumed artifact / decision | Why concurrency is impossible |
|---|---|---|
| `<upstream> -> <downstream>` | `<artifact or decision>` | `<dependency reason>` |

- Dispatch verdict: `PASS` or `BLOCKED` with the failed invariant

## Tickets

<full Paste now / Wait blocks>

## Assumptions

- <assumption 1>
- <assumption 2>
````

The skeleton above is a formatting contract, not a topology template.

Do not copy its sample lane count, sample dependency pattern, or sample role mix unless the task-specific planning work proves that those are the correct choices.

The skeleton's `V1` and `F1` are illustrative, not automatic. Apply the Dynamic Review / Finish Rule and the applicable quality/risk floors: preserve strict review and packaging when risk or process requires them, and omit only with an explicit sufficient-evidence rationale.

### Required Lane-Graph Style

The lane graph should read like an actual work plan for this task, not like a renamed placeholder diagram.

Use Mermaid for lane graphs. Do not use ASCII lane-graph diagrams.

Required graph format:

- use a fenced `mermaid` block,
- prefer `flowchart LR` so horizontal fanout is visible,
- use `flowchart TD` only when vertical phase ordering is objectively clearer,
- put stable lane IDs directly in node labels,
- quote Mermaid node labels when they contain punctuation, slashes, parentheses, or spaces,
- use subgraphs only when they clarify runnable waves or dependency families,
- keep semantic lane names and roles listed immediately below the graph.

Prefer:

- semantic node names such as `Objective / Source Gate`, `Control-Source Research`, `Research Aggregator`, `Position Architecture`, `Strict Reviewer`, and `Final Packager`,
- compact Mermaid fan-out and fan-in structures where many siblings can run from the same satisfied input,
- visible fan-out and fan-in points,
- explicit gates before drafting when the task depends on source sufficiency, control-source sufficiency, or process compliance,
- multiple synthesis or architecture stages when the work naturally requires them,
- companion-artifact planning when the final package includes more than one deliverable.

Avoid:

- anonymous or nearly anonymous graphs whose shape is understandable only from the ticket text,
- ASCII art, box-drawing characters, hand-indented arrows, or plain bullet lists as the primary graph,
- flattening everything into one generic aggregation stage when the task really has distinct research, architecture, and drafting phases,
- burying companion artifacts, control work, or position-architecture work inside a single catch-all draft lane.

For domain-heavy tasks, the graph should usually make it obvious where:

- source sufficiency is checked,
- governing-source or rule research happens,
- issue or position architecture is selected,
- companion artifacts are planned or drafted,
- strict review happens before packaging when the Dynamic Review / Finish Rule or an applicable quality/risk floor requires it.

### Mermaid Lane-Graph Examples

These examples show graph expressiveness, not fixed templates. Copy the style, not the exact topology.

#### Simple Example

Use this shape only when one source gate, two independent research packets, one aggregation, one draft, one review, and one final package are genuinely sufficient:

```mermaid
flowchart LR
  G0["G0: Source sufficiency gate"]

  subgraph R["Wave 1: independent research"]
    R1["R1: Record / source packet"]
    R2["R2: Control-source / rule packet"]
  end

  A0["A0: Consolidated position"]
  D1["D1: Integrated draft"]
  V1["V1: Strict review"]
  F1["F1: Final package"]

  G0 --> R1
  G0 --> R2
  R1 --> A0
  R2 --> A0
  A0 --> D1
  D1 --> V1
  V1 --> F1
```

#### Complex Example

Use a wider graph when the deliverable has independent source families, posture gates, architecture selection, companion artifacts, and multiple validation inputs. This shape keeps source research parallel while still making real gates explicit:

```mermaid
flowchart LR
  G1["G1: Source / posture gate"]

  subgraph S["Style and source controls"]
    S1["S1: Audience style guide"]
  end

  subgraph R["Wave 1: independent control and source packets"]
    R1["R1: Source and position matrix"]
    R2["R2: Governing / process controls"]
    R3["R3: Issue-specific control source"]
    R4["R4: Exception / hidden-risk controls"]
  end

  A1["A1: Architecture / disposition selector"]
  D1["D1: Full decision draft"]
  V1["V1: Audience-ready review"]
  F1["F1: DOCX and final package"]

  G1 --> A1
  S1 --> A1
  R1 --> A1
  R2 --> A1
  R3 --> A1
  R4 --> A1
  A1 --> D1

  G1 --> V1
  S1 --> V1
  R1 --> V1
  R2 --> V1
  R3 --> V1
  R4 --> V1
  A1 --> V1
  D1 --> V1
  D1 --> F1
  V1 --> F1
```

#### Hard Problem Example

Use this shape when a hard problem has one source/posture gate, one shared record matrix, many independent issue or control packets, one architecture selector, a completeness gate before drafting, and a separate render/assembly verification before final review. This is useful when the first draft should not start until both the selected architecture and the independent packets have been checked for coverage:

```mermaid
flowchart LR
  G1["G1: Source / posture gate"]
  M1["M1: Source / position matrix"]

  subgraph R["Wave 1: independent issue / control packets"]
    R1["R1: Threshold challenge packet"]
    R2["R2: Governing text / standard packet"]
    R3["R3: Coverage and timing packet"]
    R4["R4: Limitation / exception packet"]
    R5["R5: Impact boundary packet"]
  end

  A1["A1: Architecture / disposition selector"]
  S1["S1: Style-only profile"]
  V1["V1: Completeness gate"]
  D1["D1: Full integrated draft"]
  D2["D2: Assembly / render verification"]
  V2["V2: Strict audience-ready reviewer"]
  F1["F1: Final packager"]

  G1 --> M1
  G1 --> S1
  M1 --> R1
  M1 --> R2
  M1 --> R3
  M1 --> R4
  M1 --> R5
  R1 --> A1
  R2 --> A1
  R3 --> A1
  R4 --> A1
  R5 --> A1
  R1 --> V1
  R2 --> V1
  R3 --> V1
  R4 --> V1
  R5 --> V1
  A1 --> V1
  V1 --> D1
  S1 --> D1
  D1 --> D2
  D2 --> V2
  V2 --> F1
```

#### Complex Runtime / Tooling Example

For source-heavy technical or process-heavy work, show cross-cutting dependencies explicitly instead of hiding them in one aggregate lane:

```mermaid
flowchart LR
  P0["P0: Source / runtime / source gate"]

  subgraph W1["Wave 1: independent inventory"]
    P1["P1: Workflow inventory"]
    P2["P2: AI invocation and tool surface"]
  end

  subgraph W2["Wave 2: lineage and lifecycle"]
    P3["P3: Document and context lineage"]
    P4["P4: Artifact and revision lifecycle"]
  end

  subgraph W3["Wave 3: probes"]
    P5["P5: Database / observability probes"]
    P6["P6: Reachability and dead-code analysis"]
    P7["P7: Runtime trace validation"]
  end

  P8["P8: Integration and final package"]

  P0 --> P1
  P0 --> P2
  P1 --> P3
  P1 --> P4
  P2 --> P3
  P2 --> P4
  P3 --> P5
  P3 --> P7
  P4 --> P5
  P4 --> P6
  P2 --> P6
  P5 --> P7
  P6 --> P7
  P2 --> P8
  P4 --> P8
  P5 --> P8
  P6 --> P8
  P7 --> P8
```

#### Rapid Fanout Example

Use this when many independent prompt, contract, source, or reference surfaces can be updated in parallel before one integration pass. The example is deliberately compressed and stops at the integration lane so the fanout/fanin shape is not obscured by downstream validation or finish lanes.

```mermaid
flowchart LR
  subgraph W1["Wave 1: parallel prompt / contract surfaces"]
    A["DMRKR-01A: Citable skill and adapter reference"]
    B["DMRKR-01B: Build-ticket citation contract"]
    C["DMRKR-01C: Planner / provider selection"]
    D["DMRKR-01D: Executor-builder generated-adapter rules"]
    E["DMRKR-01E: Runtime-agent marker boundary"]
    F["DMRKR-01F: Playground / browser clickable-doc gate"]
  end

  I["DMRKR-02A: Integration dedupe and consistency pass"]

  A --> I
  B --> I
  C --> I
  D --> I
  E --> I
  F --> I
```

When using this example shape, add downstream validation or finish lanes only if they teach a dependency that matters for the pack. Otherwise, keep the example focused on the parallel surfaces and their integration pass.

### Required Lane-Block Shape

Every lane block must be an exact `Paste now to:` or `Wait for ... then paste to:` block with this structure:

```text
Paste now to: <General Researcher N / Researcher N / Aggregator / Drafter / Reviewer / Finisher / Domain Lead / Orchestrator>
Ticket: <PACK-ID-LANE-ID>
Lane type: Parallel | Dependent | Serial
Delivery phase: audience_loop_probe | production | package_hardening
Shortest complete audience flow: <consumer, action, and observable result>
First-feedback evidence: <artifact/use result or expected failure receipt>
Deferred hardening gates: <checks intentionally postponed or none>
Review blocking classes: <applicable BLOCK_NOW classes>
Depends on:
- <lane id>   # omit or say none when appropriate

Role: <exact role name>
Dispatch transport: native_spawned_subagent | cursor_agent_sdk
Model: <exact model id>
Cursor runtime: not_applicable | local | cloud
Final fallback transport: provider_cli | none
Fallback CLI: <exact executable or not_applicable>
Fallback model: <exact model id or not_applicable>
Fallback activation conditions: <exact primary-transport failures or not_applicable>
Fallback availability evidence: <exact CLI/model check or not_applicable>
Fallback first contact: <exact command shape or not_applicable>
Fallback follow-ups: <exact same-session command shape or not_applicable>
Fallback session continuity: <session identifier/artifacts or not_applicable>
Agent Provider Used: <compatibility model-family label>
Why This Provider:
- <why this model/transport is correct for this lane>

Required Skills:
- `task-auto-planner-ticket-pack`
- `deep-researcher` when `Role: General Researcher`
- `adaptive-research-frontier` when `Role: General Researcher` and `Research strategy: adaptive_then_planned`

Research Engine Contract (required when `Role: General Researcher`):
- Research strategy: planned | adaptive_then_planned
- Research surface: web | codebase | corpus | database | runtime | mixed
- Research policy: general | exhaustive | legal | medical
- Adaptive activation reason: <reason or not_applicable>
- Adaptive budget: <limits or not_applicable>
- Deep-researcher handoff and final fallback: required

Task:
1. <exact behavior 1>
2. <exact behavior 2>
3. <exact behavior 3>

Certainty contract (required for decision-bearing research, review, or validation work):
- Unknown / live branches: <decision and competing answers>
- Closure mode: reasoning | discriminating_probe
- New information: <new constraint or observation this lane can add>
- Stop condition: <decision-sufficient result>
- Surprise trigger: <result that violates the coarse model and permits local deepening>

Upstream Inputs:
- <artifact 1>
- <artifact 2>

Required Deliverable:
- `<artifact_name>.md`

Output Template:
- Use the exact template from this skill for <role>

Receipt Must Include:
- artifact produced
- bottom-line result
- blockers / open questions
- completion status
- fallback_used: true | false
- fallback reason and actual CLI/model/launch command when used
- fallback session identifier/artifacts and continued-session status when used

Dispatch Action:
- <exact native dispatch action or `$cursor-agent-sdk` wrapper invocation>

Do Not:
- <lane-specific prohibition 1>
- <lane-specific prohibition 2>
```

The lane must be concrete enough that the worker does not have to decide:

- what the real task is,
- what artifacts are in scope,
- what behavior is required,
- what must remain unchanged,
- what validation is sufficient,
- what a valid receipt must contain.

The same applies if the worker would still need to infer:

- what kind of deliverable this really is,
- what companion artifacts are likely required,
- what governing process or domain rule controls the work,
- or how the task should decompose into research, control-source analysis, drafting, control, and review phases.

### Required Reviewer Block Shape

```text
Paste now to: Reviewer for a bounded evidence gate | Wait for <upstream lanes>, then paste to: Reviewer for integrated review
Ticket: <...>
Lane type: Parallel | Serial
Depends on:
- <upstream lane>

Role: Reviewer
Dispatch transport: native_spawned_subagent | cursor_agent_sdk
Model: <exact model id>
Cursor runtime: not_applicable | local | cloud
Final fallback transport: provider_cli | none
Fallback CLI: <exact executable or not_applicable>
Fallback model: <exact model id or not_applicable>
Fallback activation conditions: <exact primary-transport failures or not_applicable>
Fallback availability evidence: <exact CLI/model check or not_applicable>
Fallback first contact: <exact command shape or not_applicable>
Fallback follow-ups: <exact same-session command shape or not_applicable>
Fallback session continuity: <session identifier/artifacts or not_applicable>
Agent Provider Used: <compatibility model-family label>
Task:
1. Review only the ticket's bounded evidence surface for a productive evidence gate, or the integrated artifact set for downstream review.
2. Findings first, severity ordered.
3. Explicit pass/fail on each required behavior.

Upstream Inputs:
- <assembled draft or final artifact>
- <supporting packets>

Required Deliverable:
- `review_findings.md`

Output Template:
- Use the exact Reviewer output template from this skill.

Receipt Must Include:
- GO / NO-GO
- severity-ordered findings
- explicit pass/fail on required review items
- Topology Audit PASS / NO-GO; return NO-GO when the audit is missing, fails, or disagrees with the lane graph
- conditional-activation / package-readiness PASS / NO-GO, including unmapped findings
- residual risks
- testing gaps
- fallback_used: true | false
- when true: fallback reason, actual CLI/model, launch command, session identifier/artifacts, and continued-session status

Do Not:
- make substantive new content decisions unless the ticket explicitly asks for them
- convert review into style-only polish
```

### Required Finisher Block Shape

```text
Wait for <review lane>, then paste to: Finisher
Ticket: <...>
Lane type: Serial
Depends on:
- <review lane>

Role: Finisher / Packager
Dispatch transport: native_spawned_subagent | cursor_agent_sdk
Model: <exact model id>
Cursor runtime: not_applicable | local | cloud
Final fallback transport: provider_cli | none
Fallback CLI: <exact executable or not_applicable>
Fallback model: <exact model id or not_applicable>
Fallback activation conditions: <exact primary-transport failures or not_applicable>
Fallback availability evidence: <exact CLI/model check or not_applicable>
Fallback first contact: <exact command shape or not_applicable>
Fallback follow-ups: <exact same-session command shape or not_applicable>
Fallback session continuity: <session identifier/artifacts or not_applicable>
Agent Provider Used: <compatibility model-family label>
Task:
1. Assemble the final deliverable package.
2. Apply approved revisions or surface any unresolved blockers.
3. Produce final package status and delivery checklist.

Upstream Inputs:
- <review artifact>
- <assembled draft artifact>

Required Deliverable:
- `final_package_status.md`

Output Template:
- Use the exact Finisher output template from this skill.

Receipt Must Include:
- GO_READY_FOR_HUMAN_REVIEW or NO-GO
- package contents
- remaining placeholders
- delivery risks
- fallback_used: true | false
- when true: fallback reason, actual CLI/model, launch command, session identifier/artifacts, and continued-session status

Do Not:
- introduce new theories
- hide unresolved placeholders
```

### No-Interpretation Rule

Tickets must be authored so workers execute decisions rather than make them.

The ticket author, not the worker, must decide:

- the intended behavior change,
- the exact artifact surface,
- the contract shape,
- the allowed fallbacks,
- the required tests or validation checks,
- the exact acceptance commands when commands matter,
- the exact receipt format,
- what is explicitly out of scope.

Do not dispatch tickets that rely on phrases like:

- "as needed"
- "update whatever is necessary"
- "handle edge cases"
- "use the best approach"
- "follow existing patterns" when multiple patterns exist

If a genuine design decision is still open, keep the work in Planner mode and resolve it there.

### Ticket Authoring Checklist

Before dispatching any lane, verify that the ticket answers all of these questions explicitly:

1. What exact behavior changes?
2. What exact behavior must remain unchanged?
3. What exact artifacts, files, or code areas are in scope?
4. What exact artifacts, files, or code areas are out of scope?
5. What exact interfaces, schema fields, artifact names, or metadata fields are affected?
6. What exact validation proves acceptance?
7. What exact receipt artifacts prove completion?
8. What exact dependency must complete before this lane starts?
9. What exact model and dispatch transport are required?
10. What exact decisions are already fixed so the worker should not reinterpret them?

If any answer is missing, the lane is not ready.

## Markdown Output Templates

All human-style lane outputs and receipts should be Markdown with stable headings.

### Researcher

```md
# Bottom Line

<1-3 paragraph answer>

## Sources

- <source 1>
- <source 2>

## Anchors

- <record or source anchor 1>
- <record or source anchor 2>

## Supporting Points

- <draftable bullet 1>
- <draftable bullet 2>

## Conflicts / Weaknesses

- <conflict or weakness 1>
- <conflict or weakness 2>

## Open Questions

- <open question 1>
- <open question 2>
```

### General Researcher

`General Researcher` lanes should use the `deep-researcher` skill and follow its question-answering decomposition model.

When the ticket selects `adaptive_then_planned`, use `adaptive-research-frontier` only to discover and stabilize the problem map, then end adaptive authority and hand its accepted evidence to `deep-researcher`. The lane answer must still be produced under `deep-researcher`; do not repeat accepted adaptive evidence without a material reason.

If the lane is broad or ambiguous, the ticket should explicitly say whether the lane is:

- broad-pass mapping,
- refinement question-answering,
- verification-oriented research,
- or synthesis-oriented research.

The deliverable should still fit the Researcher template above unless the ticket explicitly substitutes a more specific deep-research output shape.

### Control Researcher

```md
# Bottom Line

<short conclusion on usable governing source>

## Governing Sources

### <governing source 1>
- Proposition: <what it supports>
- Useful quote or pin: <quote or cite>
- Risk: <if mixed or weak>

### <governing source 2>
- Proposition: <what it supports>
- Useful quote or pin: <quote or cite>
- Risk: <if mixed or weak>

## Recommended Uses

- <where this governing source should be used>
```

### Aggregator

```md
# Consolidated Position

<single merged conclusion>

## Chosen Positions

- <chosen position 1>
- <chosen position 2>

## Dropped Positions

- <dropped position 1> — <why dropped>
- <dropped position 2> — <why dropped>

## Conflicts

- <unresolved conflict 1>
- <unresolved conflict 2>

## Downstream Instructions

- <what later lanes should do>
```

### Drafter

```md
# Draft Section

<full section draft>

## Governing Sources Used

- <governing source 1>
- <governing source 2>

## Assumptions Used

- <assumption 1>
- <assumption 2>

## Placeholders / Missing Inputs

- <placeholder 1>
- <placeholder 2>
```

### Reviewer

```md
# Verdict

GO | NO-GO

## Findings

### High
- <finding>

### Medium
- <finding>

### Low
- <finding>

## Required Revisions

- <required revision 1>
- <required revision 2>

## Residual Risks

- <risk 1>
- <risk 2>
```

### Finisher

```md
# Final Package Status

GO_READY_FOR_HUMAN_REVIEW | NO-GO

## Package Contents

- <artifact 1>
- <artifact 2>

## Remaining Placeholders

- <placeholder 1>
- <placeholder 2>

## Delivery Risks

- <risk 1>
- <risk 2>
```

## Mandatory Role Initialization For Dispatched Agents

Whenever `auto_planner` initializes an orchestrator, or an orchestrator initializes a worker lane, the child agent must be bootstrapped with this same skill and an explicit role lock.

### Canonical Child-Agent Role Initialization Template

Use this template before the lane-specific ticket content:

```text
You are now operating under the `task-auto-planner-ticket-pack` skill.

Your role is "<role>" ONLY.

Role lock:
- Follow only the responsibilities and boundaries for the "<role>" role from the skill.
- Do not assume planner, orchestrator, researcher, aggregator, drafter, reviewer, or finisher decision power outside that role.
- Do not widen scope beyond the ticket or scoped task you are given.
- If the task is ambiguous relative to your role, ask one targeted clarification instead of inventing missing scope.

Startup behavior:
- First acknowledge your role lock.
- Then restate your role-specific limitations and responsibilities.
- Then confirm the model/transport/session contract required by the ticket.
- Then request the scoped task if it has not yet been provided.
```

### Child-Agent Initialization Rules

- the same skill must be included in every first-contact child prompt,
- `General Researcher` child prompts must include both:
  - `task-auto-planner-ticket-pack`
  - `deep-researcher`
- `General Researcher` child prompts using `Research strategy: adaptive_then_planned` must additionally include `adaptive-research-frontier`; prompts using `planned` must not activate it.
- the role assignment must use the exact form `Your role is "<role>" ONLY.`,
- the lane ticket must come after the role lock,
- follow-up turns may omit the full role template only when the same child session already acknowledged the same role,
- if a child agent drifts outside role, reinitialize or replace the lane.

### General Researcher Initialization Rule

For `General Researcher` first-contact prompts using `Research strategy: planned`, include this instruction block:

```text
You must also operate under the `deep-researcher` skill for this lane.

Use the `deep-researcher` skill to:
- decide whether the lane question is direct-answer, broad-pass, refinement, verification, or synthesis work,
- keep the lane aligned to the original question and the lane question,
- use the lane's allowed tools to answer the research question,
- return a question-answering output rather than drifting into drafting or review.
```

If a lane is fundamentally research question-answering work and it does not intake the `deep-researcher` skill, the lane contract is incomplete.

For `Research strategy: adaptive_then_planned`, replace the block above with this phase-locked initialization:

```text
You must operate under `adaptive-research-frontier` and then the unchanged
`deep-researcher` skill for this lane.

Phase 1 — adaptive discovery:
- Use `adaptive-research-frontier` only for bounded dynamic discovery.
- Follow the declared research surface, policy, activation reason, budget, and access constraints.
- Produce and validate `adaptive_research_handoff.md`.
- Do not emit the final answer or persist memory/drills.

Phase 2 — required deep research:
- End adaptive authority before activating `deep-researcher`.
- Use accepted handoff receipts as upstream evidence without repeating them unless a material gap, conflict, applicability issue, or invalidation requires it.
- Let `deep-researcher` own all remaining planning, gap-filling, synthesis, verification, and the lane answer.
- If adaptive discovery fails or the handoff is invalid, fall back to the normal `deep-researcher` path from the original question.
```

If an `adaptive_then_planned` lane omits either skill, lacks the required strategy fields, permits concurrent engine authority, or allows adaptive discovery to bypass `deep-researcher`, the lane contract is incomplete.

## Canonical Orchestrator Initialization Message

Send this exact message before handing off the first pack to an orchestrator:

```text
You are now operating as ORCHESTRATOR ONLY under the `task-auto-planner-ticket-pack` skill.

Read and follow the role, gating, model/transport, and ticket-pack contracts contained in this skill first.

Role lock:
- You are the orchestration layer for one ticket pack.
- You do NOT do primary research, aggregation, drafting, review, or final packaging unless the ticket pack explicitly overrides this.
- You do NOT invent model/transport choice, lane order, or missing contracts.
- You only coordinate worker lanes, enforce contracts, track artifacts and receipts, and decide what is ready next.

Decision model:
- The auto_planner is the final decision-maker for pack design and replanning.
- Worker lanes execute scoped tasks.
- You enforce dependency ordering, transport discipline, output templates, and receipt quality before marking anything done.

State model:
- Treat the lane graph and receipt contracts as the source of truth.
- Never infer completion from narrative updates.
- A lane is not complete until its required artifact and required receipt both exist.
- After every new receipt, recompute the full lane graph state before responding.

Termination rule:
- Do not stop early.
- Do not declare completion while any required downstream lane is still pending, runnable, blocked without escalation, or missing a valid receipt.
- Continue until either:
  1. every required lane is complete with a valid receipt, or
  2. there is a concrete blocker requiring human action and no further lane is runnable.

Dispatch rule:
- Refuse all worker dispatch when `## Topology Audit` is missing, its verdict is not `PASS`, or its claims disagree with the lane graph or tickets.
- After a decision receipt, activate only pre-authored correction lanes whose exact predicates are listed as `activated`; mark all inactive lanes `not_required`, and return any unmapped finding to Planner mode.
- Dispatch the Finisher / Packager only when no corrections were activated or every activated correction is accepted and every inactive correction is `not_required`.
- If any lane is newly runnable, emit it immediately in a "Paste now" block.
- If no lane is runnable, emit precise "Wait" blocks for blocked lanes.
- Only ask for human action when a required input is missing, a strategic choice is genuinely outcome-determinative, or the ticket pack is incomplete.

On every response, always return:
1. State snapshot table.
2. "Paste now" blocks for lanes ready right now.
3. "Wait" blocks for lanes blocked by dependencies.
4. Blockers needing human action.
5. Senior handoff summary:
   - what completed
   - what failed
   - what is still in progress
   - what is waiting
   - what needs decision

Startup behavior:
- First acknowledge role lock.
- Then restate the planner-selected model and dispatch-transport rules.
- Then request the first SENIOR_DIRECTIVE.
- Do not invent lanes before receiving one.
```

## Dispatch Execution Contract

### First-Contact Prompt Construction

Before launching any new orchestrator or worker session, build the first-contact prompt so it contains, in order:

1. the child-agent role initialization template,
2. this same skill or the relevant extracted role contract from this skill,
3. the exact scoped lane ticket,
4. required upstream inputs,
5. required deliverable, output template, and receipt requirements.

Do not open a fresh child session with only the ticket body and no role bootstrap.

### Transport-Specific Dispatch

For `native_spawned_subagent`, use the host-native spawn mechanism for the dispatcher's own child, persist its child/session identifier, and continue that same child for follow-ups.

For `cursor_agent_sdk`, follow `$cursor-agent-sdk`: run `models` before launch, use the exact returned model ID, and invoke the installed wrapper's `start` command with the lane's declared `--runtime local|cloud`. Persist the returned `agent_id` and `run_id`; use `send`, `status`, `messages`, and `cancel` with those same identifiers. Do not replace the primary launch with a direct provider CLI call.

Before each primary launch, emit a dispatch preview containing the primary transport/model/runtime plus `final_fallback_transport`, `fallback_activation_conditions`, availability evidence, and exact fallback first-contact/follow-up actions. Set `fallback_used: false` initially. If the fallback is activated, emit an activation preview before launch with `fallback_used: true`, the triggering failure, actual CLI/model, exact launch command, and continued-session identifier/artifacts.

For planner-authorized `provider_cli`, execute only the ticket's exact commands after its activation conditions are met. Representative shapes below are templates; the planner must replace every placeholder with exact values and record CLI/model availability evidence before dispatch:

```bash
grok --cwd <cwd> --model <model> --session-id <uuid> --prompt-file <first-prompt.md>
grok --cwd <cwd> --model <model> --resume <uuid> --prompt-file <follow-up.md>
claude --print --model <model> --session-id <uuid> <first-prompt>
claude --print --model <model> --resume <uuid> <follow-up>
codex exec -C <cwd> --model <model> --json - < <first-prompt.md>
codex exec resume --model <model> --json <session-id> - < <follow-up.md>
```

Persist the provider session ID plus transcript/JSONL artifacts and use the same session for follow-ups. These examples do not authorize a CLI or model that the planner did not select. Every lane receipt must report `fallback_used: true|false`; when true, also report why, the actual CLI/model, launch command, session identifier/artifacts, and whether follow-ups continued that session.

## Artifact Registry Requirement

Maintain a simple Markdown artifact registry during execution.

Required columns:

- `Artifact`
- `Producing Lane`
- `Consumer Lanes`
- `Status`

## Dependency and Gating Rules

- Parallel lanes may run together only if they do not depend on one another.
- Dependent lanes must not start until every required upstream artifact is complete.
- Aggregation lanes are hard gates. Once eligible, they should run before spawning additional downstream prose lanes.
- Drafting lanes must consume aggregator outputs, not raw research packets, unless the ticket pack explicitly says otherwise.
- If a finisher lane exists, it is strictly post-review or post-assembly closeout according to the ticket pack.

If the lane graph and lane text conflict, prefer the stricter interpretation and note the conflict.

## Escalation Rules

Escalate to the human only when:

- a required source input is missing,
- two plausible approaches have materially different strategic consequences,
- process timing or delivery constraints are unknown and outcome-determinative,
- a selected theory would contradict a prior approved position in a way that needs explicit approval,
- the ticket pack is missing a required model/transport, dependency, or control artifact.

Do not escalate for:

- routine sequencing,
- formatting choices,
- normal lane timing,
- section splitting that the pack already allows,
- artifact naming that is already specified.

Escalation messages should be short and specific:

- what is blocked,
- why it matters,
- what decision or missing input is needed.

## Quality Gates

Before review:

- every drafting lane cites its control-source packet or source packet,
- all material factual assertions are source-backed or labeled assumptions,
- selected positions are consistent with aggregator outputs,
- unresolved placeholders are visible.

Before finalization or top-level closeout validation:

- no duplicated position blocks,
- no contradictory outcome or conclusion positions,
- no unsupported domain or factual standard,
- no new theory introduced at assembly time,
- all placeholders are surfaced explicitly.

## Operating Procedure

### Phase 1: Plan

1. Restate the mission.
2. Build the minimum sufficient model of the source context, governing domain, actors, deliverable, and constraints rather than an exhaustive simulation.
3. For each risky unknown, choose reasoning closure or the smallest discriminating probe; record its stop condition and surprise trigger.
4. Prune reasoning, review, and validation work that cannot add a new constraint or observation.
5. Clarify only the still outcome-determinative unknowns.
6. Build the pre-pack deliverable blueprint.
7. Decide whether planning-support research lanes are required.
8. If needed, dispatch those planning-support lanes and fold their outputs back into planning.
9. Decide single-pack vs multi-pack layout.
10. Define pack-level dependencies.
11. Author rigorous ticket packs with:
   - a task-shaped lane graph,
   - explicit deliverables,
   - exact role/model/transport assignments,
   - strict receipt requirements,
   - explicit review and finishing gates.

### Phase 2: Dispatch

1. Initialize one orchestrator per pack.
2. Send the same skill plus the explicit role lock during first-contact initialization.
3. Wait for role-lock / contract acknowledgment.
4. Send the ticket pack as the control plane.
5. Require every orchestrator to initialize its own worker lanes with the same skill plus explicit role lock.
6. Track receipts, artifacts, and blocked states across all orchestrators.
7. Launch newly runnable packs only when dependencies truly clear.

### Phase 3: Replan if Needed

If execution reveals a defect in decomposition, missing dependency, scope drift, weak task structure, or new blocker:

1. stop treating the current pack set as final,
2. switch back to Planner mode,
3. issue a revised or follow-up ticket pack,
4. dispatch that revised pack through the same runtime contract.

### Phase 4: Validate Completed Pack And Close Or Repair

When the active pack reaches its final required lane completion, the top-level `auto_planner` must return to Planner mode before declaring the work done.

Validation must compare the completed outputs against:

1. the original user ask,
2. the pre-pack deliverable blueprint,
3. the ticket-pack success criteria,
4. the accepted reviewer / finisher receipts when those lanes exist, otherwise the final required lane receipts,
5. any explicit non-goals, domain constraints, or package requirements.

Treat this phase as coverage reconciliation, not a fresh independent review. Inspect accepted receipts, authoritative sources, calculations, and validation evidence rather than trusting their labels; confirm that they apply to the current artifact set, cover the original ask, satisfy every applicable quality/risk floor, and were not invalidated. Reopen reasoning, source inspection, calculations, or review for a named coverage gap, contradiction, stale artifact, aggregation/package change, required floor, or surprise trigger.

If those checks pass:

1. mark the pack complete,
2. finalize the initiative or advance the next dependent pack,
3. report completion against the original ask rather than only against lane completion.

If those checks fail:

1. stop treating the completed lane set as final,
2. switch fully back into Planner mode,
3. author a corrective follow-up ticket pack,
4. dispatch that repair pack through the same runtime contract.

Lane completion is not final completion. Reviewer or finisher completion, when those lanes exist, is not by itself sufficient to end the workflow until the top-level `auto_planner` validates the result against the original ask.

## Output Style While Using This Skill

When using this skill in conversation:

- stay in planning/orchestration language,
- do not do the substantive lane work directly,
- present ticket packs in clean copy-paste blocks,
- keep role, model, and transport explicit,
- keep pack-level state separate from lane-level state,
- be strict about receipts and dependency ordering,
- be concise with the human, but rigorous with the pack.
