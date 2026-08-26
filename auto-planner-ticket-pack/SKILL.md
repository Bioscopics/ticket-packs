---
name: auto-planner-ticket-pack
description: "Use when a coding task should be executed as a planning-first ticket-pack or ticket-pack-set workflow, including direct requests to implement, fix, patch, refactor, add, or wire up substantive engineering changes. Create rigorous packs, dispatch and track worker lanes, identify proposed PR units, and invoke cohesive stack composition before multiple PRs are packaged. Optional child orchestrators are reserved for truly independent pack sets."
---

# Auto Planner Ticket Pack

## Overview

This skill turns the agent into a coding `auto_planner` that alternates between two modes:

1. **Planner mode**: gather context, understand the ask and problem, normalize any PRD or spec into an aligned implementation problem statement, decide single-pack vs multi-pack layout, and author rigorous ticket packs.
2. **Dispatcher mode**: the same top-level agent becomes the direct orchestrator for the ticket pack by default, dispatches worker lanes, monitors receipts and dependencies, and keeps execution aligned with the agreed plan. Optional child orchestrators are used only for truly independent pack sets.

If execution drifts, blocks, or reveals a design gap, switch back to **Planner mode**, produce a corrected or follow-up ticket pack, then return to **Dispatcher mode**.

The agent using this skill does **not** directly implement code unless the human explicitly overrides that operating model.

## Goal Contract Skill Web

At the start of Planner mode for every substantive request, invoke `goal-writing`
once unless a current aligned goal contract is already present in context. Let
that skill scale the contract to the request; a clear small change may need only
the north star and completion proof, while multi-stage or multi-agent work may
need the full coordinated contract.

Treat the goal contract as the upstream alignment layer. Carry its north star,
terminal condition, success evidence, scope locks, non-goals, assumptions, and
material open questions into problem normalization and the ticket pack. This
skill still owns repository discovery, implementation-problem normalization,
ticket decomposition, lane topology, dispatch, verification, repair, and PR
packaging. `goal-writing` must not duplicate or replace those responsibilities.

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

Optimize for decision-relevant certainty under finite time, context, tool, and agent budgets. Do not maximize processing, model every component at full fidelity, or add review because more review is theoretically possible.

Start with the coarsest system model that is sufficient to choose the next action. Refine only the part of that model whose uncertainty can change scope, architecture, dispatch, acceptance, or risk. Treat a material violation of the coarse model—a surprising runtime result, contradictory source, broken invariant, unexpected dependency, or behavior outside the predicted contract—as the signal to deepen or redirect work locally.

For every material unknown, choose one closure path:

1. **Reasoning closure** — use when trusted premises, contracts, and already accepted evidence can determine the answer. Derive the constraint and conclusion explicitly. Unstructured reconsideration of the same evidence does not increase certainty; a materially independent method, adversarial frame, or alternative-assumption check does when it targets a named failure mode.
2. **Discriminating-probe closure** — use when the answer depends on external or empirical state. Run the smallest **adequate** search, read, test, experiment, runtime check, or comparison whose possible outcomes distinguish the live branches across the decision's actual scope, and state how each outcome changes the plan. Cheapest is not adequate when it omits a material boundary or failure mode.

After either path, update the coarse model and decide:

- `closed`: the result is decision-sufficient at its declared scope and every applicable quality/risk floor is satisfied; stop work on that unknown;
- `surprised`: the result violates the model; deepen only the affected region and fan out independent probes when useful;
- `unresolved`: neither reasoning nor an affordable discriminating probe can close it; preserve the uncertainty and escalate only when outcome-determinative.

Quality and risk floors outrank economy. Explicit user requirements, repository/contract gates, security or privacy boundaries, migrations, irreversible operations, externally consumed interfaces, high-consequence behavior, and exhaustive or regulated policies are non-prunable. Known completeness, adverse-case, exception, integration, and rollback checks do not require a surprise trigger. Optimize the cost of satisfying these floors; never lower or skip them to save resources.

Precedence rule: when this resource policy conflicts with a more specific user requirement, repository instruction, domain policy, acceptance contract, or required skill validation, the stricter requirement wins. This policy removes redundant work only after the applicable quality floor is satisfied.

Apply these resource rules to planning and topology:

- Every decision-bearing research, reasoning, review, or validation lane must name the unknown it closes, its closure mode, the new constraint or evidence it can add, its stop condition, and its surprise trigger.
- Prune a proposed lane or serial edge when it only rereads, re-reasons over, or reverifies information already closed by an authoritative upstream result.
- Once a deterministic, contract-relevant test closes an empirical unknown, do not add an independent verification lane unless residual risk is specific: high consequence, weak or nondeterministic evidence, cross-boundary integration, adversarial exposure, or an explicit contradictory signal.
- Treat closure as scope-bound: a unit test does not close integration, runtime, migration, accessibility, visual, rollback, or end-to-end user-outcome uncertainty unless it directly exercises that boundary. Integration or assembly can invalidate otherwise valid lane-local evidence.
- Treat a targeted independent or adversarial review of the same artifacts as new analysis when it tests a named omission, interaction, assumption, or failure mode that upstream authors were not positioned to assess. Generic rereading is not enough.
- Spend more resources when expected information gain and consequence of error justify it. At high uncertainty, prefer several cheap independent probes and prune weak branches quickly; after a strong signal, concentrate only on the surviving branch.
- Implementation and packaging lanes may still be required to produce the outcome, but do not mislabel them as additional certainty gates.

## Shortest Complete User Loop

For every user-facing or externally consumed build, optimize first for time to
the earliest honest attempt of the shortest end-to-end user journey. A rough,
incomplete, or visibly failing version is a valid early checkpoint when it
reaches the real surface and exposes the actual blocker. It is not completion
and must be labeled honestly.

Use these delivery phases:

- `user_flow_probe`: make the smallest real journey attemptable through the UI
  or other public entrypoint and return the first high-signal result.
- `implementation`: repair the journey blockers and build the accepted behavior
  after the integration seam is proven.
- `pr_hardening`: protect only the final surviving behavior with tests, required
  review, full validation, and PR packaging.

Before new unit tests, broad suites, general independent review, coverage work,
or polish:

1. Name the shortest journey that crosses every changed system boundary.
2. Build the smallest honest version through which a user can attempt it.
3. Start or attach to the real app and exercise that journey from its visible
   surface with realistic minimal input. For a non-visual product, use its real
   public CLI, API, or other user entrypoint.
4. Inspect the visible result plus relevant console, network, and runtime errors.
5. Return the URL or entrypoint, input, screenshot or observable result, and the
   first blocking failure to the user immediately.
6. Repair first only what blocks the journey, makes feedback misleading, breaks
   an explicit contract, or creates material security, privacy, data-loss,
   migration, or irreversible-action risk.

During `user_flow_probe` and `implementation`, do **not author new unit tests**.
Do not write tests for exploratory code that may be deleted. Existing targeted
tests may be run only when they are the fastest discriminating probe for a named
blocker or a mandatory safety/repository gate; do not run broad suites by ritual.
At `pr_hardening`, add only the tests needed to protect the accepted surviving
behavior, then run the required final suites.

Use `test-from-ui` in `early_smoke` mode for the first rendered journey and in
`final_proof` mode during hardening. Do not request a general reviewer before
the first user-flow attempt unless the ticket names a specific high-consequence
risk that cannot safely wait.

Every review finding must be classified:

- `BLOCK_NOW`: prevents the user journey, invalidates feedback, violates an
  explicit requirement, or creates material risk.
- `DEFER_TO_HARDENING`: matters before PR submission but not before user
  feedback.
- `NON_BLOCKING`: optional improvement that must not activate a repair loop.

A reviewer may not create new acceptance criteria or block the current phase on
preference, polish, theoretical completeness, or coverage percentage. Before
activating any repair, ask whether the failed gate can change the current user
decision. If not, defer it to the appropriate later phase.

A bounded `user_flow_probe` may use one narrow implementer lane and a linear
probe graph when that is the fastest route to the first integrated signal. This
is a discriminating probe, not a substantive implementation pack or PR-ready
claim, and is exempt from the non-linear productive-work invariant only until
the first journey attempt. After the probe, return to Planner mode and author or
revise the substantive pack; maximum safe parallelism then applies normally.

Every applicable pack and lane must declare:

```text
Delivery phase: user_flow_probe | implementation | pr_hardening
Shortest complete user flow: <real entrypoint, action, and observable result>
First-feedback evidence: <URL/input/screenshot/result or expected failure receipt>
Test-writing policy: prohibited_until_pr_hardening | pr_hardening_required
Review blocking classes: <applicable BLOCK_NOW classes>
```

## Research Engine Skill Web

Keep `deep-researcher` as the unchanged prerequisite, planned-research engine, synthesis owner, and final fallback for every planning-support `general_researcher` lane.

The planner must select one research strategy per lane:

- `planned` (default): invoke `deep-researcher` directly using the existing contract.
- `adaptive_then_planned`: invoke `adaptive-research-frontier` only for bounded discovery, require a validated handoff, then end adaptive authority and invoke `deep-researcher` for the remaining plan, gap-filling, synthesis, and answer.

Select `adaptive_then_planned` only when early probes are likely to change the decomposition and the search topology cannot be specified safely up front. Before selecting it, make one cheap, bounded orientation pass over the obvious entry point, contract, component index, and nearest precedent. Record what was checked, at least two still-live branches, and the result-dependent next action in the activation reason. If that pass maps the ownership boundary and extension pattern, select `planned`; a hypothetical chance of redirection is insufficient. Task size, difficulty, convention sensitivity, or extra-verification value alone are also insufficient. Prefer `planned` for enumerable artifacts, fixed calculations, and code changes whose component ownership and extension pattern can be mapped safely before dispatch. A codebase task qualifies only when orientation leaves genuinely plausible competing shared, domain-local, host, runtime, or API boundaries, or exposes a materially contingent next question. When routing confidence is low, keep `planned`. Do not support `adaptive_only`, do not modify or bypass `deep-researcher`, and do not let both engines govern the same frontier concurrently.

Every `general_researcher` task must declare:

```text
Research strategy: planned | adaptive_then_planned
Research surface: web | codebase | corpus | database | runtime | mixed
Research policy: general | exhaustive | legal | medical
Adaptive activation reason: <reason or not_applicable>
Adaptive budget: <limits or not_applicable>
Deep-researcher handoff and final fallback: required
```

For `adaptive_then_planned`, include `adaptive-research-frontier` in addition to `deep-researcher` and this skill. The adaptive skill may return evidence but may not emit the final answer, persist memory or drills, alter the planner-selected runtime contract, or replace `deep-researcher`.

## Agent Behavior Contract Probe Skill Web

Use `agent-behavior-contract-probe` only as a conditional discriminating-probe technique when the live unknown is an agent's observable prompt ownership, tool choice or sequence, permission handling, delegation, or recovery behavior and deterministic tests cannot prove it. Do not require it globally, use it for deterministic substrate, or replace final cross-system E2E with it.

Use this validation ladder at its applicable scopes:

1. deterministic unit/integration tests prove deterministic substrate;
2. a faithful real-agent behavioral contract probe proves one controlled runtime choice when that uncertainty remains;
3. E2E remains the final proof of the complete cross-system user outcome.

When the planner selects this technique, add `agent-behavior-contract-probe` to that lane's required skills and choose the target repository's faithful production agent runtime and adapter. OpenCode may be preferred when it faithfully runs a Weave agent, but it is never a prerequisite or dependency. For other repositories, use their production runtime or another faithful real-agent runtime carrying the production prompt, tools, permissions, configuration, and topology. If none is available, classify the probe `unavailable`, record the missing fidelity, and continue all other proof; never block solely because OpenCode is absent.

Author these fields before dispatching a selected probe:

```text
Behavior-contract target: <one observable contract>
Production artifacts: <agent definition, prompt layers, tools, permissions, configuration, topology>
Faithful runtime / alternate: <production runtime, faithful alternate, or unavailable condition>
Controlled stimulus: <one realistic uncoached input>
Required actions: <externally observable sequence>
Prohibited actions: <bypasses, leaks, unsupported claims, or other forbidden outcomes>
Evidence to retain: <session/trace, transcript, tool calls, configuration and fixture snapshot, report>
Stop condition: <pass, unresolved, or unavailable evidence sufficient to route the next step>
Surprise trigger: <observation that contradicts the model and stops blind patching>
```

A selected probe receipt must report its classification (`pass | surprised | unresolved | unavailable`), runtime fidelity and deliberate deviations, observed required sequence, prohibited-action checks, durable evidence locations, and next action (`none | revised probe | E2E | broader workflow continues unavailable`). A `surprised` result stops the affected lane for local replanning or E2E escalation; an unavailable faithful runtime does not stop unrelated deterministic or E2E proof.

## PR Packaging Skill Handoff

When completed work may produce multiple pull requests:

1. Identify the proposed PR units from the accepted lane outputs and their smallest behavior contracts.
2. Use `smallest-viable-pr` to validate each proposed boundary. If a split is recommended, preserve its relationship evidence.
3. Invoke `compose-cohesive-pr-stacks` before any of those PRs are packaged. That skill owns partitioning, dependency classification, and merge order.
4. After the topology is approved, invoke the externally maintained `gh-stack` skill to create the GitHub stack.

This skill identifies proposed PR units and initiates the handoff. It does not decide stack topology or implement GitHub stack operations. Do not reproduce or modify `gh-stack` instructions here. If `gh-stack` is unavailable, stop after the approved topology and report that packaging is blocked.

For one proposed PR, skip stack composition and use the normal PR creation workflow.

## Hard Stop: Direct Implementation Requests

If the user asks to `implement`, `fix`, `patch`, `refactor`, `add`, `wire up`, `update`, `ship`, or `build` a substantive coding change, that request **does not authorize** the top-level agent to implement the code itself.

Treat the request as a trigger to enter Planner mode and produce a ticket pack first.

Before using tools or editing files, run this self-check:

1. Am I about to create or edit production code, tests, config, or integration logic myself?
2. Am I about to perform implementer, bugfixer, reviewer, or finisher work instead of assigning it to a lane?
3. Have I already emitted the required laminated ticket pack and entered the required direct-orchestrator/lane flow?

If the answer to 1 or 2 is yes and the answer to 3 is no, **stop**. The only allowed next outputs are:

- a short source/context-gathering update,
- a targeted clarification for an outcome-determinative unknown,
- the mandatory planning-session result,
- a laminated ticket pack or ticket-pack set,
- a direct-orchestrator state snapshot or optional child-orchestrator initialization message for independent pack sets.

Do not create or edit the requested code directly from the top-level session.

### Override Requirement

The human override must be explicit and task-local. Accept only instructions equivalent to:

- "Override the skill and implement directly."
- "Do the coding yourself; do not use the ticket-pack workflow."
- "For this turn, act as the implementer rather than auto_planner."

Generic urgency, a direct request to fix/build something, or dissatisfaction with planning does not count as override.

### Violation Recovery

If the top-level agent accidentally performs substantive coding-lane work:

1. stop immediately,
2. label the work product invalid under this skill,
3. do not rely on it as an upstream artifact,
4. return to Planner mode,
5. emit the missing ticket pack or ask the minimum clarification needed to do so.

## Use This Skill When

Use this skill when the user wants any of the following:

- a large or ambiguous engineering task broken into rigorous ticket packs,
- a large or ambiguous engineering ask, with or without a PRD/spec/requirements doc, converted into an implementation-ready ticket pack,
- parallelizable implementation lanes with explicit dependency control,
- direct-orchestrator management of worker lanes, with optional child orchestrators only for independent pack sets,
- planner-authored execution rather than ad hoc direct coding,
- receipt-driven coordination with reviewer/finisher gates,
- replanning when execution uncovers new blockers or scope drift.

Do **not** use this skill for a simple one-file edit, a casual code question, or a task the user wants implemented directly without orchestration.

## Core Role Model

### Planner Mode

In Planner mode, you act like `Planner` plus the planning parts of `Senior Agent`:

- gather codebase and workflow context,
- treat the user's ask as the primary planning input,
- ingest any PRD/spec/requirements artifact as optional supporting context,
- build an aligned understanding of the actual problem before lane design,
- optionally dispatch one or more `general_researcher` lanes in parallel during planning when the problem still needs clarification,
- ask only the minimum clarifying questions needed for risky unknowns,
- define the objective, scope locks, non-goals, acceptance criteria, and receipt contracts,
- decide whether the work is:
  - one ticket pack handled by direct orchestrator mode, or
  - a ticket-pack set where truly independent packs may receive optional child orchestrators,
- design the lane graph and pack graph,
- choose where parallelism is safe and where serialization is required,
- author the ticket pack(s) completely before dispatch.

### Dispatcher Mode

In Dispatcher mode, the same top-level agent becomes the direct orchestrator by default. Do not create a child orchestrator for the normal single-pack case.

Direct orchestrator mode means:

- treat the ticket pack as the source of truth,
- emit runnable worker-lane `Paste now` blocks directly,
- spawn or continue worker sessions with the exact role locks required by the lane tickets,
- monitor worker receipts and approvals,
- track pack-level state separately from lane-level state,
- decide when another pack may start,
- escalate only real blockers or approval needs,
- switch back to Planner mode when the pack is under-specified, execution reveals a decomposition problem, or a repair pack is required.

Optional child orchestrators may be initialized only for truly independent ticket-pack sets where separate orchestration materially reduces coordination risk.

### Mode-Switch Rule

Switch **from Planner mode to Dispatcher mode** only after the ticket pack is decision-complete.

Switch **from Dispatcher mode back to Planner mode** when:

- the current pack is under-specified,
- a blocker requires architectural or decomposition changes,
- a follow-up bugfix/fixup pack is needed,
- integration risk between packs requires a new pack or revised dependency ordering.

### Problem-Evidence Gate Rule

Before authoring the ticket pack, confirm that there is enough concrete evidence to act on the problem rather than only a vague symptom report.

For bug, incident, regression, or failure-style asks, the planner should determine whether it has enough of the following:

- the triggering ask or ticket,
- reproducible symptoms, or a clear statement that the issue is not yet reproducible,
- relevant logs, traces, screenshots, failing tests, or code-path evidence when available,
- enough context to tell whether the first pack should be diagnosis-heavy, fix-heavy, or blocked on more inputs.

If that evidence is not sufficient, do not jump straight to implementation packs. Stay in Planner mode and either:

- dispatch planning-stage `general_researcher` work to clarify the problem shape,
- emit a diagnosis-oriented ticket pack,
- or mark the pack state `external_input_required`.

## Dispatchable Roles Under This Skill

This skill is the shared operating contract for the top-level `auto_planner`, for any dispatched orchestrator, and for any worker lane agent.

Every dispatched agent must receive:

1. this same skill,
2. an explicit role assignment,
3. the scoped task or lane ticket for that role.

Coding-lane agents (`implementer`, `bugfixer`, `reviewer`, `pr_finisher`) must also receive and follow the `smallest-viable-diff` skill. Its smallest-diff, reuse-first, deletion/simplification, tripwire, and reviewer-veto requirements are part of this skill's lane contract.

Valid roles under this skill are:

- `auto_planner`
- `orchestrator`
- `general_researcher`
- `implementer`
- `bugfixer`
- `reviewer`
- `pr_finisher`

### Role Contracts

`auto_planner`

- owns planning, pack-set design, pack authorship, direct-orchestrator mode switching, optional child-orchestrator initialization for independent pack sets, and pack-level tracking,
- may switch between planner and dispatcher behavior,
- does not directly code unless the human explicitly overrides the operating model,
- must treat direct implementation requests as requests to design and dispatch the workflow, not as permission to code.

`orchestrator`

- coordinates lane execution for exactly one ticket pack,
- enforces dependency order, scope locks, acceptance criteria, and receipt quality,
- does not invent architecture, code changes, or review findings.

`general_researcher`

- is an optional planning-support role used before ticket-pack authoring when the problem still needs clarification,
- helps the planner understand the ask, product/problem space, repo implications, edge cases, or external context,
- may run in parallel with other `general_researcher` lanes when those clarification questions are independent,
- must be bootstrapped with the separate `deep-researcher` skill,
- must also be bootstrapped with `adaptive-research-frontier` only when the planner selects `adaptive_then_planned`,
- must end adaptive authority before starting the required `deep-researcher` phase,
- does not become an implementer, reviewer, or finisher lane,
- returns research artifacts that the planner uses to author the actual coding ticket pack.

`implementer`

- executes a scoped coding lane,
- changes only the allowed files/behavior surface,
- runs the lane acceptance commands,
- for an applicable rendered or user-facing change, completes the real UI journey and captures a final working-state screenshot,
- returns a full implementer receipt with runtime proof.

`bugfixer`

- executes a narrow corrective coding lane,
- fixes the specific defect or regression identified by upstream review/integration,
- does not widen into a fresh feature implementation.

`reviewer`

- performs read-only findings-first review on the integrated branch,
- reports severity-ordered findings, pass/fail against required review points, residual risks, and testing gaps,
- does not make code changes.

`pr_finisher`

- reruns only accepted validation commands whose evidence was invalidated by integration, repair, branch movement, or packaging; otherwise confirms and reuses current accepted receipts,
- confirms reviewer status,
- packages one approved PR to the correct base branch, or follows the approved multi-PR topology through the external `gh-stack` skill,
- does not make unrelated code changes.

If a dispatched agent is not explicitly assigned one of these roles, initialization is incomplete.

## Mandatory Role Initialization For Dispatched Agents

Whenever `auto_planner` initializes an orchestrator, or whenever an orchestrator initializes a worker lane, the child agent must be bootstrapped with this same skill and an explicit role lock.

### Canonical Child-Agent Role Initialization Template

Use this template before the lane-specific ticket content:

```text
You are now operating under the `auto-planner-ticket-pack` skill.

Your role is "<role>" ONLY.

Role lock:
- Follow only the responsibilities and boundaries for the "<role>" role from the skill.
- Do not assume planner, orchestrator, reviewer, or implementer authority outside that role.
- Do not widen scope beyond the ticket or scoped task you are given.
- If the task is ambiguous relative to your role, ask one targeted clarification instead of inventing missing scope.

Startup behavior:
- First acknowledge your role lock.
- Then restate your role-specific limitations and responsibilities.
- Then confirm the runtime/session contract required by the ticket.
- Then request the scoped task if it has not yet been provided.
```

### Child-Agent Initialization Rules

- The same skill must be included in every first-contact child-agent prompt.
- `general_researcher` child prompts must include both:
  - `auto-planner-ticket-pack`
  - `deep-researcher`
- `general_researcher` child prompts using `Research strategy: adaptive_then_planned` must additionally include `adaptive-research-frontier`; prompts using `planned` must not activate it.
- The role assignment must be explicit, using the exact form:
  - `Your role is "<role>" ONLY.`
- The lane ticket or scoped task must come after the role lock.
- Follow-up turns may omit the full role template only when the child session is already active and has previously acknowledged the same role.
- If a child agent starts acting outside its assigned role, treat that as role drift and reinitialize or replace the lane.

### General Researcher Initialization Rule

For `general_researcher` first-contact prompts using `Research strategy: planned`, include this instruction block:

```text
You must also operate under the `deep-researcher` skill for this lane.

Use the `deep-researcher` skill to:
- clarify the lane's planning question,
- break the question down if needed,
- use parallel research where appropriate,
- return a concise research artifact that helps the planner understand the problem,
- avoid drifting into implementation or final ticket-pack authoring.
```

If a planning-support research lane does not intake the `deep-researcher` skill, the lane contract is incomplete.

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

## Hard Boundaries

When this skill is active:

- direct implementation requests still require Planner mode and a ticket pack first,
- you are **not** an implementer,
- you do **not** directly code,
- you do **not** silently replace orchestrated execution with direct edits,
- you do **not** let the orchestrator invent the graph,
- you do **not** let workers add code without `smallest-viable-diff` proof,
- you do **not** parallelize overlapping file or behavior ownership,
- you do **not** treat narrative updates as completion,
- you do **not** consider a lane complete without its required receipt.

`Reviewer`, `Implementer`, `Bugfixer`, and `Finisher` may not spawn orchestrators.

`auto_planner` is a **mode**, not a separate permanent role. `Planner` may operate in it. `Senior Agent` may operate in it only when explicitly acting in planner scope.

## Pack-Set Planning Rules

### Single Pack vs Multiple Packs

Decide whether the initiative should run as:

- **one ticket pack handled by direct orchestrator mode**, or
- **multiple independent packs that may use optional child orchestrators**.

Use optional child orchestrators only when packs are truly independent.

If packs share glue, integration surfaces, or overlapping file/behavior ownership:

- serialize them, or
- create a final integration pack.

### Pack-Level State Table

Track pack-level state separately from each orchestrator's lane table.

Minimum fields:

| Field | Meaning |
|------|---------|
| `pack_id` | Unique pack identifier |
| `objective` | Human-visible goal |
| `scope` | Locked file/behavior surface |
| `deps` | Pack-level dependencies |
| `orchestrator` | Assigned orchestrator session |
| `status` | Current pack state |
| `latest_receipt` | Most recent accepted pack-level milestone |
| `next_gate` | Next reviewer/finisher/dependency/human gate |

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

- use `external_input_required` when the next step depends on missing human/system input rather than more planning,
- use `repair_pack_required` when execution finished but Phase 4 validation says a corrective follow-up pack is needed,
- use `ready_for_final_validation` when all required lanes for the current pack are complete and the top-level `auto_planner` must now decide whether to finalize or repair.

### Ticket-Pack Requirements

Every ticket pack must be decision-complete before dispatch. It must define:

- the aligned problem statement the pack is solving,
- scope locks,
- acceptance criteria,
- receipt contract,
- reviewer and finisher requirements, or an explicit rationale for omitting either lane,
- any approval gates,
- exact commands when command execution matters,
- coding conventions source for coding lanes,
- a `Smallest Viable Diff` section for every coding lane or an explicit statement that the lane is read-only.

The orchestrator executes a planner-authored graph. It does **not** invent one.

## Dynamic Review / Finish Rule

Reviewer and PR finisher lanes are conditional, not automatic.

Include a `reviewer` lane when the task has one or more of these properties:

- multi-lane implementation or integration risk,
- meaningful regression risk,
- contradiction risk across outputs,
- high-stakes behavior change,
- significant ambiguity in correctness,
- explicit request for independent review.

The reviewer ticket must name the residual uncertainty not already closed by lane-local acceptance tests and the novel finding, adversarial analysis, or independent evidence it can produce. Reviewing the same diff is justified when the reviewer targets a named omission, interaction, assumption, or failure mode; generic rereading or rerunning an already authoritative deterministic test is not.

Omit the `reviewer` lane only when the task is genuinely narrow, low-risk, and simple enough that top-level Phase 4 validation can provide sufficient final checking without wasting time.

Include a `pr_finisher` lane when the task has one or more of these properties:

- PR creation is part of the requested workflow,
- multiple artifacts or validations need final packaging,
- branch / base / validation / PR metadata need explicit closeout,
- a separate packaging / closeout gate materially reduces handoff risk.

When the finisher would package more than one PR, the pack must include the PR-unit validation and stack-composition handoff defined above. The finisher must not invent topology, manually approximate a native stack, or package multiple PRs before `compose-cohesive-pr-stacks` has produced an approved plan.

Omit the `pr_finisher` lane only when there is no real packaging step beyond the top-level `auto_planner` validating the completed result.

If either lane is omitted, the ticket pack must say so explicitly and explain why omission is acceptable for this task. Silent omission is not allowed.

## Ask-First Intake and Alignment Rule

The user's ask is always the primary planning input.

If a PRD, spec, product brief, or requirements document is available, it is supporting input to planning, not a substitute for planning.

Do **not** translate the ask or a PRD directly into lanes.

Before an ask, PRD, or combined ask+PRD input can become a ticket pack, the planner must:

1. read the original user ask first,
2. read any PRD/spec/requirements artifact if one exists,
3. restate the actual problem in plain implementation terms,
4. extract:
   - goals,
   - constraints,
   - success criteria,
   - non-goals,
   - implied assumptions,
   - open questions,
5. compare the ask and any supporting spec material to repo truth and current implementation reality,
6. identify gaps, contradictions, and underspecified areas,
7. ask only the minimum targeted clarifications needed to remove outcome-determinative ambiguity,
8. produce an aligned implementation problem statement,
9. only then convert that aligned understanding into a ticket pack.

If a PRD/spec is vague, contradictory, aspirational, or disconnected from repo reality, the planner must normalize it first. It must not push that ambiguity into implementer lanes.

If no PRD/spec exists, the planner must still normalize the user's ask into an aligned implementation problem statement before creating the pack.

### Required Ask / Spec Understanding Artifact

Create a short planning artifact before the ticket pack with at least:

- `Original Ask`
- `Input PRD / Spec` when one exists
- `Aligned Problem Statement`
- `Goals`
- `Non-Goals`
- `Constraints`
- `Success Criteria`
- `Open Questions`
- `Implementation Risks`

The ticket pack must trace back to this understanding artifact. If the pack does not clearly solve the aligned problem statement, it is not ready.

### Optional Planning-Support Research Fanout

If the ask is still materially unclear after initial repo reading, the planner may dispatch one or more `general_researcher` lanes **during planning** before ticket-pack authoring.

Use this when the planner needs help answering questions like:

- what problem the user is really trying to solve,
- what the current system actually does,
- what product or external context matters,
- what edge cases or constraints are likely to matter,
- what decomposition is safest.

Rules:

- these are planning-stage clarification lanes, not implementation lanes,
- they may run in parallel when the clarification questions are independent,
- their outputs must fold back into the ask/spec understanding artifact,
- the final coding ticket pack must still be authored by the planner after those lanes complete,
- do not dispatch implementation lanes until this clarification work is complete when it is required.

## Mandatory Planning Session Before Dispatch

Every time this skill is used for real work, perform a rigorous planning session **before** any orchestrator is initialized.

That planning session must:

1. restate the original ask and locked scope,
2. ingest any PRD, spec, or requirements artifact if one exists,
3. collect repo truth, system constraints, and relevant docs,
4. build an aligned understanding of the actual implementation problem,
5. identify risky unknowns, contradictions, and underspecified areas,
6. decide whether optional `general_researcher` clarification lanes are needed,
7. if needed, dispatch those clarification lanes in parallel where safe and fold their outputs back into the understanding artifact,
8. ask only the minimum targeted human clarifications still needed after that research,
9. decide whether the work is:
   - one ticket pack, or
   - a ticket-pack set,
10. decide where work can safely parallelize, maximizing horizontal fanout before adding serial depth,
11. define serial/integration gates only where a lane consumes a concrete upstream artifact, decision, receipt, or validation result,
12. produce a rigorous, laminated ticket pack or ticket-pack set that is aligned with the normalized problem statement,
13. only then move into Dispatcher mode.

Do not enter Dispatcher mode while the pack is still ambiguous.
Do not initialize optional child orchestrators directly from an unread, unnormalized, or unvalidated PRD.
Do not use optional child orchestrators for a normal single-pack workflow.
Do not treat the absence of a PRD as permission to skip the understanding and normalization step.

## Mandatory Ticket-Pack Shape

The skill must emit ticket packs in a concrete, laminated shape like the strong example pattern the user provided. Do **not** emit a vague plan, outline, or prose-only decomposition when a ticket pack is requested.

### Required Top-Level Sections

Every ticket pack must include these sections in order:

1. `# Ticket Pack: <name>`
2. `## Summary`
3. `## Proposed Flow` when the pack changes behavior across multiple surfaces
4. `## Public Interfaces` when interfaces/contracts are changing
5. `## Lane Graph`
6. `## Topology Audit` immediately after `## Lane Graph`
7. `## Tickets`
8. `## Assumptions`

Include `Locked design`, `Important repo truth`, `Required diff constraints`, and `Recommended PR title/body` whenever they materially reduce ambiguity.

### Proposed Flow Section

Include a `## Proposed Flow` section whenever the pack changes system behavior
across two or more surfaces (for example build-time contracts plus runtime plus
UI), or when a shared end-to-end picture materially reduces lane
misinterpretation. Omit it for narrow single-surface packs.

Rules:

- It is a **behavioral alignment artifact**: a Mermaid flowchart of the target
  end-to-end behavior after the pack lands, ideally walked through with one
  concrete example journey (a realistic user prompt or input case).
- Group the flow into phase subgraphs that match the system's real seams (for
  example build time, runtime, UI).
- Mark future/out-of-scope paths with dashed edges and label them explicitly so
  no lane implements them by accident.
- The Proposed Flow is **not** a dependency map and does not replace or
  override the `## Lane Graph`. Lane dependencies, scope locks, and receipts
  remain governed by the Lane Graph and Tickets. If the two conflict, the Lane
  Graph and lane tickets win and the pack must be corrected.
- Reviewer and e2e/browser-gate lanes should treat the Proposed Flow as the
  expected observable behavior to validate against.

### Topology Rule: Maximize X, Justify Y

The lane graph is a dependency map, not a decorative Mermaid template.

- **X axis = safe parallelism.** Put every lane that can start from the same satisfied inputs in the same runnable wave, even when that produces many sibling lanes.
- **Y axis = true dependency depth.** Add vertical/dependent layers only when a lane consumes a concrete upstream artifact, decision, receipt, runtime handle, or validation result.
- Do not default to memorized shapes like `2 -> 1 -> 1 -> 1`, `3 -> 1 -> reviewer`, or the example skeleton below. Lane count and wave count must scale with task complexity, file ownership, artifact interfaces, and validation needs.
- If two lanes touch disjoint files/behavior and consume only already-fixed contracts, they should normally be parallel.

#### Hard Invariant: Non-Linear Productive Work

- A substantive ticket pack must be non-linear: at least two productive lanes must be incomparable, runnable in the same wave, and later converge at an integration, review, decision, or finish gate.
- A productive lane is either (a) a narrow implementation/artifact lane that creates or changes one bounded behavior or artifact surface, or (b) a narrow independent evidence gate that owns one concern and produces one distinct findings/verification artifact consumed by a later decision node.
- A generic validation-only lane or catch-all `Independent review` does not count merely because it is separate. Orchestration, decision-only convergence, and PR-finisher nodes do not count toward maximum parallel width.
- A single productive lane followed by validation, review, and finish is invalid. The chain `Implement -> UI/runtime validation -> Independent review -> PR finish` does not satisfy this invariant.
- After contracts are fixed, require maximum safe parallelism. Every serial edge must name the exact artifact or decision consumed and explain why concurrent execution is impossible.
- Keep each productive implementation/artifact lane narrow: one bounded outcome, one bounded ownership surface or file family, and one lane-local acceptance proof. Keep each productive evidence lane to one concern and one decision-bearing artifact/receipt. Split independently deliverable concerns instead of combining them in a broad lane.
- Put implementation validation inside implementation/artifact lanes whenever possible. A separate generic validation lane is valid only for genuinely integrated behavior and does not count toward productive width.
- If two natural, non-overlapping productive lanes cannot be found, state that the work is too atomic for this ticket-pack workflow and do not fabricate parallelism.
- Treat omitted safe parallelism or a failing topology audit as a planner defect that blocks dispatch.

### Example Review / PR-Hardening Topology

```mermaid
flowchart LR
  subgraph "Parallel narrow evidence gates"
    R1["R1 Evidence: concern A"]
    R2["R2 Evidence: concern B"]
    R3["R3 Evidence: concern C"]
  end
  D["D Decision synthesis + repair activation manifest"]
  subgraph "Conditional narrow repairs"
    F1["F1 Repair A"]
    F2["F2 Repair B"]
    F3["F3 Repair C"]
  end
  P["P PR finisher"]
  R1 --> D
  R2 --> D
  R3 --> D
  D -.->|"activate only on mapped F1 predicate"| F1
  D -.->|"activate only on mapped F2 predicate"| F2
  D -.->|"activate only on mapped F3 predicate"| F3
  D -->|"no activated repairs"| P
  F1 --> P
  F2 --> P
  F3 --> P
```

- Limit `D` to synthesizing upstream evidence and emitting a repair activation manifest; it must not repeat all reviews or edit files.
- Require the `D` receipt to list `activated_repairs`, `not_required_repairs`, `finding_to_ticket_mapping`, and `unmapped_findings`.
- If `unmapped_findings` is non-empty, return to Planner mode; the dispatcher must not invent a repair.

### Canonical Top-Level Skeleton

Use this as the default section shape, not as a default lane topology. The graph
below is illustrative only. Replace the lane count, waves, labels, and edges
with the widest safe dependency graph for the actual task:

```markdown
# Ticket Pack: <Concise Initiative Name>

## Summary

<2-6 lines stating the exact behavior change and the point of the pack>

Locked design:

- <non-negotiable design rule 1>
- <non-negotiable design rule 2>

Important repo truth:

- <current implementation fact 1>
- <current implementation fact 2>

## Public Interfaces

<new workflows / contracts / API / artifact paths / metadata fields / response fields>

## Lane Graph

```mermaid
flowchart LR
  subgraph "Wave 1: all independent lanes dispatch immediately"
    A["<PACK>-01A Independent implementation lane"]
    B["<PACK>-01B Independent implementation lane"]
    C["<PACK>-01C Independent implementation lane"]
  end
  V["<PACK>-V1 Integrated review + PR finish"]
  A --> V
  B --> V
  C --> V
```

Runnable wave 1:

- `<PACK>-01A` -> independent implementation lane with disjoint ownership under fixed contracts
- `<PACK>-01B` -> independent implementation lane with disjoint ownership under fixed contracts
- `<PACK>-01C` -> independent implementation lane with disjoint ownership under fixed contracts

Dependent waves:

- This example has no dependent implementation wave. Add one only when it consumes a real upstream artifact or decision.

Combined closeout gate:

- `<PACK>-V1` -> review the integrated state first, return `NO-GO` on findings, and perform PR closeout only on `GO`

This example assumes public contracts, the base branch, and ownership are already locked. It has no synthetic preflight, aggregation, or dependent lane: the direct orchestrator mechanically integrates accepted, conflict-free disjoint heads. Add a real integration lane or separate PR Finisher when glue, conflicts, or packaging mechanics require it.

## Topology Audit

- Productive-lane inventory: `<lane id> -> <implementation/artifact or evidence type, bounded concern, artifact, and ownership surface>`
- Maximum parallel width: `<number of simultaneously runnable productive lanes>`
- Incomparable lane pairs: `<lane A> || <lane B> -> <why neither consumes the other>`
- Fan-in/convergence gate: `<integration, review, decision, or finish gate consuming the productive lanes>`
- Broad-lane split audit: `<confirm one outcome/ownership surface/acceptance proof per lane; list required splits or none>`
- Evidence/decision artifact classification: `<evidence receipts, decision inputs, and repair activation manifest; identify non-productive nodes>`
- Certainty/novelty audit: `<each decision-bearing lane -> unknown, reasoning or discriminating-probe closure, new information, stop condition; prune duplicate review or verification>`
- Surprise/escalation audit: `<coarse model assumptions and the concrete violations that authorize local deepening, replanning, or extra review>`
- Conditional-activation/finisher-readiness audit: `<predicate coverage, inactive not_required repairs, accepted activated repairs, and no-repair path>`

Serial-edge justification table:

| Serial edge | Exact consumed artifact/decision | Why concurrent execution is impossible |
|---|---|---|
| `<upstream> -> <downstream>` | `<artifact or decision>` | `<concrete reason>` |

- Dispatch verdict: `PASS | BLOCKED` — block unless the graph is non-linear, maximally parallel, narrow, and fully justified.

## Tickets

<full Paste now / Wait blocks>

## Assumptions

- <assumption 1>
- <assumption 2>
```

If the project is complex enough that a weak pack could create churn, include both `Locked design` and `Important repo truth`. Do not omit them just to save space.

### Required Ticket-Pack Graph Shape

- Use a Mermaid lane graph in a fenced `mermaid` block.
- Prefer `flowchart LR` when horizontal fanout is important; use `flowchart TD` only when vertical phase ordering is objectively clearer.
- Use node labels that include the stable lane ID and match the ticket blocks.
- Quote Mermaid node labels when they contain punctuation, parentheses, slashes, or spaces beyond a simple lane ID.
- Label runnable waves and gates clearly. Acceptable labels include `Wave 1`, `Wave 2`, `Parallel`, `Dependent`, `Review`, `Finish`, or more specific phase names. Do not force the graph into a fixed `Parallel` / `Dependent` / `Serial` trio if that obscures the real dependency structure.

### Required Per-Lane Block Shape

Infer the user's branch prefix from explicit instructions, repository guidance, and recent PR heads authored by `@me`. If no reliable prefix exists, use an unprefixed branch name. Never emit a branch beginning with `codex/`.

Every lane block must be emitted as an exact `Paste now to:` or `Wait for ... then paste to:` block with this structure:

```text
Paste now to: <Role / Implementer N / Reviewer / PR Finisher>
Ticket: <PACK-ID-LANE-ID>
Lane type: Parallel | Dependent | Serial
Delivery phase: user_flow_probe | implementation | pr_hardening
Shortest complete user flow: <real entrypoint, action, and observable result>
First-feedback evidence: <URL/input/screenshot/result or expected failure receipt>
Test-writing policy: prohibited_until_pr_hardening | pr_hardening_required
Review blocking classes: <applicable BLOCK_NOW classes>
Depends on:
- <lane id>   # omit or say none when appropriate
Branch: <inferred branch name>
Worktree: /tmp/<worktree-name>
Base branch: <base branch>

Lane role: Implementer | Bugfixer | Reviewer | PR Finisher
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
Runtime selection rationale: <why this available runtime/model fits this lane>
Agent spec: <exact persona/runtime description>
Required skills:
- auto-planner-ticket-pack
- smallest-viable-diff
- test-from-ui  # required when visual proof applicability is `required`
Session policy:
- First contact: <exact command shape>
- Follow-ups in same session: <exact command shape>
- Do not create nested workers or change the planner-selected transport/model.
Worker agent: <compatibility alias>

Required behavior:
1. <behavior 1>
2. <behavior 2>
3. <behavior 3>

Certainty contract (required for decision-bearing research, review, or validation work):
- Unknown / live branches: <decision and competing answers>
- Closure mode: reasoning | discriminating_probe
- New information: <new constraint or observation this lane can add>
- Stop condition: <decision-sufficient result>
- Surprise trigger: <result that violates the coarse model and permits local deepening>

Required files to add:
- <path>

Required files to update:
- <path>

Required tests to add or update:
- none — prohibited in this phase  # required for user_flow_probe and implementation
- <path>  # pr_hardening only

Smallest viable diff:
- behavior delta: <smallest required change>
- expected diff budget: <files/net lines/new files/dependencies>
- reuse scan: <existing helpers/components/routes/prompts/tests to inspect first>
- prompt/config/contract alternative: <sufficient path, or why insufficient>
- deletion/simplification target: <obsolete code/config/prompt to remove or simplify>
- tripwire policy: <what requires replan/approval>

Keep this lane narrow:
- <out-of-scope area 1>
- <out-of-scope area 2>

Acceptance commands:
- <exact command>

Required coverage:
- <required assertion 1>
- <required assertion 2>

Visual proof:
- applicability: required | not_applicable
- rationale: <why this lane does or does not have a meaningful rendered state>
- UI journey: <exact real user flow when required>
- required evidence: <final working-state screenshot, inputs used, and console/network status>

Return receipt:
- branch name
- head commit
- exact files changed
- net line change (added/deleted)
- smallest viable diff rationale
- reuse scan result
- deleted or simplified code/config/prompt
- tripwires hit or none
- one example of <artifact / behavior / assertion>
- test output
- visual proof applicability and rationale
- screenshot path, tested UI journey and inputs, and console/network status when visual proof is required
```

The lane block must be concrete enough that the worker does not have to decide:

- what the real task is,
- what files are in scope,
- what behavior is required,
- what behavior must remain unchanged,
- what validation is sufficient,
- what a valid receipt must contain.

If the worker would still need to choose architecture, contract shape, scope boundary, validation strategy, or artifact shape, the ticket is under-specified and must be rewritten before dispatch.

### Implementation-Time Visual Proof

The planner must decide visual-proof applicability before dispatch. Mark it `required` whenever the lane adds or changes a meaningful rendered state, including frontend features, generated-app UI, interaction flows, styling/layout fixes, charts, documents, or other reviewer-inspectable output. Mark it `not_applicable` only for work with no meaningful visual surface and record why.

For `Delivery phase: user_flow_probe`, use `test-from-ui` in `early_smoke`
mode: the evidence may show an honest failure and should return the first
journey blocker quickly. For `pr_hardening`, use `final_proof`; that evidence
must exercise the accepted complete journey. Do not withhold early-smoke
evidence merely because the implementation is incomplete.

When required, visual proof is part of implementation acceptance, not deferred PR-authoring work:

- load and follow `test-from-ui`,
- exercise the real user journey against the final implementation,
- capture a high-signal screenshot of the completed working state after validation,
- record the exact journey and inputs plus relevant console/network status,
- keep secrets, tokens, PII/PHI, customer data, private logs, and unrelated desktop content out of the image,
- return the screenshot as a receipt artifact for reviewers, finishers, and PR authors to consume.

An applicable implementer-family lane is incomplete without current visual proof. Downstream lanes must reject evidence that is stale or no longer matches the integrated diff. PR authoring should reuse a current implementation artifact and rerun the UI journey only when the artifact is missing, stale, or invalidated by later changes.

### Required Reviewer Block Shape

Reviewer lanes must be findings-first and must explicitly list pass/fail against the required review points:

```text
Wait for <upstream lanes>, then paste to: Reviewer
Ticket: <...>
Lane type: Serial
Depends on:
- <upstream lane>

Lane role: Reviewer
Dispatch transport: native_spawned_subagent | cursor_agent_sdk
Model: <exact planner-selected model id>
Cursor runtime: not_applicable | local | cloud
Final fallback transport: provider_cli | none
Fallback CLI: <exact executable or not_applicable>
Fallback model: <exact model id or not_applicable>
Fallback activation conditions: <exact primary-transport failures or not_applicable>
Fallback availability evidence: <exact CLI/model check or not_applicable>
Fallback first contact: <exact command shape or not_applicable>
Fallback follow-ups: <exact same-session command shape or not_applicable>
Fallback session continuity: <session identifier/artifacts or not_applicable>
Runtime selection rationale: <why this model fits independent review>
Agent spec: <review persona>
Required skills:
- auto-planner-ticket-pack
- smallest-viable-diff
Session policy:
- Review only the integrated branch.
- Do not make code changes.
- Findings first, severity ordered.
Worker agent: Codex Reviewer

Required review:
1. <one bounded review concern and its decision-bearing artifact; do not use a catch-all scope>
2. <topology and conditional-repair semantics when applicable>

Required output:
- GO / NO-GO
- severity-ordered findings
- explicit pass/fail on each required review item
- topology audit PASS / NO-GO
- explicit Smallest Viable Diff PASS / NO-GO
- reuse proof PASS / NO-GO
- deletion/simplification pass PASS / NO-GO
- tripwires: none or listed
- residual risks
- testing gaps
- fallback_used: true | false
- when true: fallback reason, actual CLI/model, launch command, session identifier/artifacts, and continued-session status
```

The reviewer must return `NO-GO` when the topology audit is missing, misplaced, incomplete, inconsistent with the graph/tickets, or fails the non-linear productive-work invariant. For a conditional repair graph, also return `NO-GO` if evidence concerns/artifacts overlap, the decision node repeats review or edits files, repair tickets/predicates are incomplete, findings are unmapped, or finisher readiness is not proven.

### Required Finisher Block Shape

Finisher lanes must confirm or refresh accepted evidence as required, open the PR, and produce a constrained human-validation target:

```text
Wait for <review lane>, then paste to: PR Finisher
Ticket: <...>
Lane type: Serial
Depends on:
- <review lane>

Lane role: PR Finisher
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
Runtime selection rationale: <why this runtime/model fits the finish lane>
Agent spec: <finisher persona>
Session policy:
- First contact: <exact command for the selected runtime/model>
- Follow-ups in same session: <exact continuation command for the selected runtime/model>
- Do not create nested workers or change the planner-selected transport/model.
Worker agent: <compatibility alias for the selected runtime/model>

Required validation:
1. Run accepted targeted commands only when integration, repairs, branch movement, or packaging invalidated the upstream evidence; otherwise confirm the accepted receipt still names the current head and reuse it.
2. Confirm reviewer is GO and, for conditional graphs, the decision receipt declares no repairs or every activated repair has an accepted receipt while every inactive repair is `not_required`.
3. If there is one approved PR unit, open it to the correct base branch. If there are multiple approved PR units, use the approved `compose-cohesive-pr-stacks` topology and invoke the external `gh-stack` skill to package them.
4. Do not inspect or modify unrelated files.

Required output:
- GO_AUTOMATED_PENDING_HUMAN_VALIDATION or NO-GO
- exact automated commands run
- PR number/url, or GitHub stack number and ordered PR URLs
- concise human validation target
- fallback_used: true | false
- when true: fallback reason, actual CLI/model, launch command, session identifier/artifacts, and continued-session status
```

### Ticket-Pack Set Shape

For very large projects, emit a **pack set**, not just one pack.

In that case:

- start with a pack-set summary,
- include the pack-level state table,
- define dependencies between packs before any lane blocks,
- then emit one full ticket pack per pack,
- use the direct orchestrator for the overall pack-set controller,
- assign optional child orchestrators only to truly independent packs,
- keep parallel packs file/behavior independent,
- add a final integration pack whenever parallel packs converge on shared glue.

### Ticket-Pack Quality Bar

A valid ticket pack from this skill must be:

- rigorous,
- explicit,
- narrow per lane,
- aggressively parallel where safe,
- serialized only where glue/integration or artifact dependencies require it,
- acceptance-driven,
- receipt-driven,
- runtime-declared,
- resistant to scope creep.

If the pack does not have this shape and depth, it is not ready to dispatch.

### Depth Requirements

The pack must be deep enough that each lane can execute without inventing missing structure.

That means:

- top-level summary states the exact behavioral delta, not just the area of the codebase,
- when a PRD or spec exists, the pack reflects the normalized implementation problem rather than blindly mirroring the document structure,
- when no PRD or spec exists, the pack still reflects a normalized implementation problem statement derived from the user's ask and repo truth,
- `Locked design` captures what must not change,
- `Important repo truth` captures existing implementation facts that shape the plan,
- `Public Interfaces` enumerates concrete paths, artifact names, schema fields, APIs, metadata, or workflow contracts,
- every lane names exact files or exact code areas,
- every lane has lane-local scope locks and explicit non-goals,
- every lane includes exact acceptance commands, not generic "run tests",
- every lane includes receipt artifacts specific to its output,
- reviewer lanes enumerate explicit pass/fail checkpoints,
- finisher lanes enumerate exact validation targets and PR base.

If a ticket pack could still be answered with "I wasn't sure what you wanted me to change," the pack is not rigorous enough.

### Toolkit Button Testing Convention

When a pack touches Button or the Button engine, route tests into the CI lanes established by `DistylAI/toolkit#1680`:

- Backend unit tests live under `apps/button/backend/tests/unit` and should cover deterministic helpers, guards, parsing, path safety, upload caps, state loading, and other pure behavior.
- Backend integration tests live under `apps/button/backend/tests/integration` and should use the real FastAPI `TestClient` / assembled router to prove endpoint wiring, status codes, file guards, and response contracts.
- Engine Python unit tests live under `apps/button/engine/tests/unit` and must be deterministic and CI-safe.
- Engine workflow TypeScript tests live beside workflow source as `apps/button/engine/opencode-workflow/src/*.test.ts` and run with Bun.
- Live LLM, network, Exa, model-provider, or other non-deterministic checks belong under `apps/button/engine/tests/integration` and must not be used as required CI proof unless explicitly requested.

Prefer real temporary files, real zip archives, real git repos, and real router wiring over mocks. Mock only process boundaries that would make the test non-deterministic, such as clocks, env vars, external services, or live model calls.

Tests should assert the actual behavioral contract, not weak proxies. Examples:

- assert file paths inside a returned file tree, not just that a parent folder exists,
- assert exact API response shape when that shape is the contract,
- assert nested excluded files are absent, not only that top-level excluded folders are absent,
- avoid low-value pins to hard-coded literals unless the literal is the behavior under test.

For Button lanes, choose targeted acceptance commands from:

```bash
uv run pytest apps/button/backend/tests/unit -v --tb=short
uv run pytest apps/button/backend/tests/integration -v --tb=short
uv run pytest apps/button/engine/tests/unit -v --tb=short
cd apps/button/engine/opencode-workflow && bun test ./src/*.test.ts
```

Use the narrowest subset that proves the lane. When multiple heads or behavior surfaces are integrated, treat that assembly as invalidating lane-local proof for the combined behavior and require the integration or finisher lane to rerun the relevant full command(s). For an unchanged single head, reuse a current accepted receipt instead of rerunning by ritual. Include top-level test module docstrings when adding substantial test modules, and keep imports at module scope.

### No-Interpretation Rule

Tickets must be authored so workers execute decisions rather than make them.

That means the ticket author, not the worker, must decide:

- the intended behavior change,
- the exact or bounded file surface,
- the contract shape,
- the allowed fallbacks,
- the required tests,
- the exact acceptance commands,
- the receipt format,
- what is explicitly out of scope.

Do not dispatch tickets that rely on phrases like:

- "wire this up as needed"
- "update whatever is necessary"
- "fix the related tests"
- "handle edge cases"
- "keep it narrow" without naming what narrow means
- "follow existing patterns" when multiple materially different patterns exist
- "use the best approach"

Replace them with explicit instructions such as:

- exact files to add or update,
- exact fallback order,
- exact schema fields,
- exact artifact filenames,
- exact tests to add or update,
- exact unchanged surfaces,
- exact acceptance commands,
- exact receipt artifacts to return.

If a genuine design decision is still open, keep the work in Planner mode and resolve it there. Do not push unresolved design choice into an implementer lane.

### Ticket Authoring Checklist

Complete and verify every field in `## Topology Audit` against the lane graph and ticket blocks before treating authorship as complete. For conditional graphs, verify evidence artifacts, the decision receipt schema, every pre-authored repair predicate/ticket, and finisher readiness. A missing, misplaced, incomplete, or non-`PASS` audit blocks dispatch.

Before dispatching any lane, verify that the ticket answers all of these questions explicitly:

1. What exact aligned problem statement is this pack solving?
2. What exact behavior changes?
3. What exact behavior must remain unchanged?
4. What exact files or code areas are in scope?
5. What exact files or code areas are out of scope?
6. What exact interfaces, schema fields, artifact names, or metadata fields are affected?
7. What exact tests must be added or updated?
8. What exact commands prove acceptance?
9. What exact receipt artifacts prove completion?
10. What exact dependency must complete before this lane starts?
11. What exact decisions are already fixed so the worker should not reinterpret them?

If any answer is missing, the lane is not ready.

### Style Requirements For Ticket Packs

When emitting a ticket pack:

- prefer full absolute paths when file paths matter,
- prefer exact artifact filenames and schema field names over paraphrase,
- prefer concrete branch/worktree names over placeholders,
- prefer lane-local acceptance commands over suite-wide commands unless the wider suite is required,
- prefer explicit `Keep this lane narrow` bullets to prevent scope creep,
- never collapse the plan into a prose summary when the user asked for a ticket pack,
- never substitute an outline or checklist for the laminated `Paste now` / `Wait for` structure.

## Runtime Contract

### Planner-Selected Agent And Dispatch Transport

The planner chooses the task-fit agent/model and `Dispatch transport` for every lane. The dispatcher executes that choice; it does not make or silently revise it.

Allowed primary transports are:

- `native_spawned_subagent`: only the dispatcher's own host-native spawned child. Native spawning is invalid unless the lane explicitly selects this transport.
- `cursor_agent_sdk`: every worker that is not the dispatcher's own spawned child. The dispatcher must use `$cursor-agent-sdk` for the primary launch.

The planner independently chooses `Final fallback transport: provider_cli | none` per lane. `provider_cli` is optional and valid only as the final fallback; it is never a primary transport. The dispatcher may not invent, silently enable, or automatically select it. A lane authorizing `provider_cli` must record the exact `Fallback CLI`, exact `Fallback model`, explicit `Fallback activation conditions`, exact first-contact and follow-up command shapes, availability evidence for that CLI/model, and the session-continuity identifier/artifacts. This fallback contract is required in every lane block, including reviewer and finisher blocks.

The dispatcher may activate `provider_cli` only after the planner-selected primary transport fails a declared activation condition. If the lane selects `none`, the declared condition is not met, or the authorized CLI/model is unavailable, halt dispatch and return to Planner mode. Never substitute another CLI, model, or fallback chain.

For `cursor_agent_sdk`, the dispatcher must discover exact account-available model IDs with the installed wrapper, launch the selected model with Cursor runtime `local` or `cloud`, persist `agent_id` and `run_id`, and use that same agent for follow-ups, status, messages, and cancellation. Cursor-exposed Gemini, Grok, Claude, Composer, Codex, or other returned models are eligible when task-fit.

Every lane ticket and pre-dispatch preview must record `Dispatch transport`, exact `Model`, `Cursor runtime: local|cloud` when applicable (`not_applicable` for native transport), and the planner-selected final-fallback fields. If the selected primary is unavailable, activate only an explicitly authorized `provider_cli` fallback whose declared conditions are met; otherwise halt dispatch and return to Planner mode. This section governs over legacy runtime examples elsewhere in this skill.

### Required Per-Ticket Runtime Fields

`Worker agent` alone is never sufficient. Each worker ticket must specify:

- `Lane role`
- `Dispatch transport`
- `Model`
- `Cursor runtime`
- `Runtime selection rationale`
- `Agent spec`
- `Session policy`
- `Worker agent`
- `Final fallback transport` and all required `Fallback ...` fields

Meanings:

- `Agent spec`: repo-local prompt/persona surface.
- `Dispatch transport`: exact allowed lane transport.
- `Model`: exact model identifier passed to that runtime.
- `Cursor runtime`: `local` or `cloud` for `cursor_agent_sdk`; otherwise `not_applicable`.
- `Runtime selection rationale`: task-fit and availability justification covering scope clarity, difficulty, state/recovery hazards, correctness and maintainability risk, validation strength, and throughput/cost needs; never a generic model ranking.
- `Worker agent`: compatibility alias only; it does not replace the transport declaration.
- `Session policy`: default is `initialize_once_then_continue` unless the human explicitly overrides it.
- `Final fallback transport`: `provider_cli` or `none`, selected by the planner independently of the primary transport.

### Planner-Selected Runtime Policy

- Choose each exact model based on scope clarity, reasoning difficulty, repository/tool fit, risk, required verification, and throughput/cost needs rather than role-name defaults.
- For `cursor_agent_sdk`, use `$cursor-agent-sdk` model discovery as the availability source and record the exact returned model ID.
- Reviewer choices must preserve independent findings-first review.
- If a ticket lacks transport/model fields, Cursor runtime when applicable, availability evidence, session actions, or a lane-specific rationale, the pack is incomplete and must not be dispatched.

## Runtime-Aware Dispatch Contract

### Initialization-Complete Gate

In the normal single-pack case, the top-level agent enters direct orchestrator mode after Planner mode finishes the pack. No child orchestrator acknowledgment is required.

Before launching the first worker lane, the direct orchestrator must explicitly confirm:

- each lane's selected transport/model is available and matches the planner's task-fit rationale,
- each first-contact and follow-up action matches the declared transport/model,
- reviewer choices preserve independent findings-first review,
- host-native spawning is used only for lanes declaring `native_spawned_subagent`; every other worker uses `cursor_agent_sdk`,
- the direct orchestrator itself will not implement code.
- optional child orchestrators are not being used unless the pack set is truly independent.

If any of those acknowledgments are missing, initialization is incomplete and the pack must not be dispatched yet.

### Pre-Dispatch Proof Requirement

Before the direct orchestrator launches the first worker lane, it must recompute the topology audit from the laminated graph and tickets. For a conditional graph, confirm every possible repair is already authored in `## Tickets` with its exact predicate, scope, acceptance, and receipt contract. If the audit is missing or fails, halt before emitting a preview or launching any lane. Otherwise, emit a dispatch preview containing:

- `topology_audit_verdict: PASS`
- `lane_id`
- `lane_role`
- `dispatch_transport`
- `model`
- `cursor_runtime`
- `runtime_selection_rationale`
- `availability_check`
- `agent_spec`
- `cwd`
- `first_contact_action`
- `follow_up_action`
- `final_fallback_transport`
- `fallback_activation_conditions`
- `fallback_availability_check`
- `fallback_first_contact_action`
- `fallback_follow_up_action`
- `fallback_used: false`

If the preview's transport, model, Cursor runtime, actions, or availability evidence disagree with the laminated ticket, dispatch must halt as a contract violation.

Before activating a conditional repair, require the decision receipt's complete activation manifest and an exact predicate-to-ticket match; any unmapped finding returns to Planner mode. Before launching the finisher, require either no activated repairs or accepted receipts for every activated repair plus `not_required_repairs` entries for every inactive repair.

If the fallback is activated, emit an activation preview before launch with `fallback_used: true`, the triggering failure, actual CLI/model, exact launch command, and continued-session identifier/artifacts.

### Forbidden Runtime Patterns

These are invalid for implementer-family lanes:

- host-native spawning when the lane does not declare `native_spawned_subagent`
- direct Gemini, Grok, Claude, Codex, Composer, or other provider CLI launch as a primary transport
- any provider CLI launch not explicitly planner-authorized as the lane's final fallback
- a non-native launch that bypasses `$cursor-agent-sdk`
- any hidden handoff transport instead of the ticket's declared transport/model
- silently substituting a transport, model, or Cursor runtime

## Direct Orchestrator Mode Contract

Use this contract when switching from Planner mode into Dispatcher mode for the normal single-pack case:

```text
I am now operating in direct orchestrator mode.

Role lock:
- I coordinate worker lanes, enforce contracts, track state, and decide what is ready next.
- I do NOT implement code changes directly.
- I do NOT invent a new lane graph outside the ticket pack.

State model:
- The ticket pack lane graph and receipt contracts are the source of truth.
- A lane is not complete until its required receipt is complete.
- I will emit Paste now blocks for runnable lanes and Wait blocks for blocked lanes.
```

## Optional Child-Orchestrator Initialization Message

Only use this for truly independent ticket-pack sets where separate orchestration materially reduces coordination risk. Do not use it for the normal single-pack case. Send this exact message before handing off the child pack:

```text
You are now operating as ORCHESTRATOR ONLY.

Read and follow this file first:
ORCHESTRATOR_MASTER_AGENT.md inside of button_modules/

Role lock:
- You are the orchestration layer.
- You do NOT do senior planning or architecture decisions.
- You do NOT implement code changes.
- You do NOT review style-only issues.
- You only coordinate Senior <-> worker lanes, enforce contracts, track state, and decide what is ready next.

Authority model:
- Senior Agent is the final decision-maker.
- Worker lanes (Implementer / Bugfixer / Reviewer / Finisher) execute scoped tasks.
- You enforce scope locks, acceptance criteria, dependency ordering, and receipt quality before marking anything done.

State model:
- Treat the lane graph and receipt contracts as the source of truth.
- Never infer completion from narrative progress updates.
- A lane is NOT complete until it has the exact receipt artifacts required by its ticket.
- If a lane reports partial progress without a valid receipt, it remains incomplete.
- After every new receipt or approval update, recompute the full graph state before responding.

Termination rule:
- Do NOT stop early.
- Do NOT conclude the orchestration because one or more implementation lanes finished.
- Do NOT declare overall completion while any required downstream lane is still pending, waiting, runnable, or missing a valid receipt.
- Continue orchestrating until exactly one of these is true:
  1. every required lane is completed with a valid receipt, OR
  2. there is a concrete blocker that requires human action and no further lane is runnable.
- Reviewer and Finisher lanes are conditional. If omitted, the ticket pack must explicitly say why, and the top-level `auto_planner` Phase 4 validation becomes the closing gate for that pack.
- “Waiting on reviewer” or “waiting on finisher” is NOT completion.
- “Most of the work is done” is NOT completion.

Dispatch rule:
- If any lane is newly runnable, emit it immediately in a "Paste now" block.
- If no lane is runnable, emit precise "Wait" blocks for blocked lanes.
- Only ask for human action when:
  - an approval is actually required,
  - a dependency cannot be resolved by the existing lane graph,
  - or the `SENIOR_DIRECTIVE` is ambiguous.

Receipt rule:
- A receipt must satisfy the lane’s required output contract.
- If required receipt fields or artifacts are missing, the lane remains incomplete.
- If a lane claims success but its receipt is incomplete, mark it blocked/incomplete and say what is missing.
- Never upgrade a lane to completed from a summary alone.

On every response, always return:
1. State snapshot table (lane_id, role, status, deps, scope, approvals, receipt).
2. "Paste now" blocks for any lane that is ready right now.
3. "Wait" blocks for lanes blocked by dependencies.
4. Blockers needing human action, batched.
5. Senior handoff summary:
   - what completed
   - what failed
   - what is still in progress
   - what is waiting
   - what needs decision

Input protocol I will use with you:
- SENIOR_DIRECTIVE: <new plan / lane graph / criteria>
- WORKER_RECEIPT: <lane result from implementer / reviewer / finisher / etc>
- APPROVAL_UPDATE: <approved / denied + command>
- STATUS: <ask for current orchestration state>

Behavior on ambiguous input:
- If a directive is ambiguous, ask one targeted clarification before dispatch.
- Otherwise, dispatch immediately according to the lane graph.

Startup behavior:
- First acknowledge role lock.
- Then explicitly repeat back the runtime contract for implementer-family lanes, reviewer lanes, and forbidden delegation mechanisms.
- Then request the first SENIOR_DIRECTIVE.
- Do not invent lanes before receiving one.
```

## Lane Spin-Up Commands

### First-Contact Prompt Construction

Before launching any new orchestrator or worker session, build the first-contact prompt so it contains, in order:

1. the child-agent role initialization template,
2. this same skill or the relevant extracted role contract from this skill,
3. the `smallest-viable-diff` skill or its extracted contract for coding-lane agents,
4. any coding-conventions source required by the lane,
5. the exact scoped ticket block or scoped task,
6. acceptance commands and receipt requirements.

For Toolkit frontend/UI lanes, include `references/toolkit-fe-ui.md` as a coding-conventions source, especially for styling, portal, popout, or sidebar work.

Do not open a fresh child session with only the ticket body and no role bootstrap.

### Baseline

Before any lane:

```bash
git -C /Volumes/git/button-modules status --short --branch
git -C /Volumes/git/button-modules rev-parse --abbrev-ref HEAD
```

### Transport-Specific Dispatch

For `native_spawned_subagent`, use the host-native spawn mechanism for the dispatcher's own child, persist its child/session identifier, and continue that same child for follow-ups.

For `cursor_agent_sdk`, follow `$cursor-agent-sdk`: run `models` before launch, use the exact returned model ID, and invoke the installed wrapper's `start` command with the lane's declared `--runtime local|cloud`. Persist the returned `agent_id` and `run_id`; use `send`, `status`, `messages`, and `cancel` with those same identifiers. Do not replace the primary launch with a direct provider CLI call.

For planner-authorized `provider_cli`, execute only the ticket's exact commands after its activation conditions are met. Representative shapes below are templates; the planner must replace every placeholder with exact values and record CLI/model availability evidence before dispatch:

```bash
grok --cwd <cwd> --model <model> --session-id <uuid> --prompt-file <first-prompt.md>
grok --cwd <cwd> --model <model> --resume <uuid> --prompt-file <follow-up.md>
claude --print --model <model> --session-id <uuid> <first-prompt>
claude --print --model <model> --resume <uuid> <follow-up>
codex exec -C <cwd> --model <model> --json - < <first-prompt.md>
codex exec resume --model <model> --json <session-id> - < <follow-up.md>
```

Persist the provider session ID plus transcript/JSONL artifacts, and use the same session for follow-ups. These examples do not authorize a CLI or model that the planner did not select.

Persist a lane session registry and reuse it across turns.

## Receipt Contract

Every implementer-family receipt must include:

- concise summary,
- changed file list,
- net line change (`added`, `deleted`),
- smallest viable diff rationale,
- reuse scan proof,
- prompt/config/contract alternative analysis when applicable,
- deletion/simplification pass result,
- tripwires hit or explicit `none`,
- key diff excerpt,
- exact outputs for acceptance commands,
- explicit note on whether any out-of-scope files were touched,
- `dispatch_transport`,
- `model_used`,
- `cursor_runtime: local|cloud|not_applicable`,
- `agent_id` and `run_id` when `cursor_agent_sdk` is used,
- `launch_command`,
- `continued_session: true|false`,
- `fallback_used: true|false`,
- `fallback_reason`, actual `fallback_cli` / `fallback_model`, and `fallback_launch_command` when used,
- `fallback_session_id` / transcript artifacts and `fallback_continued_session: true|false` when used,
- `lane_transcript_artifact`,
- `visual_proof_applicable: true|false` with rationale,
- when visual proof applies: `screenshot_artifact`, exact UI journey and inputs, and console/network status.

Every reviewer receipt must include:

- findings ordered by severity with file/line references,
- explicit pass/fail on required behaviors,
- explicit pass/fail on Smallest Viable Diff requirements,
- required shrink requests when the diff is larger than necessary,
- residual risks,
- testing gaps.

If runtime proof fields, Smallest Viable Diff proof fields, or required visual-proof fields are missing for an implementer-family lane, that lane is not validly completed even if the code result looks good.

## Operating Procedure

### Phase 1: Plan

1. Restate the mission.
2. Build the minimum sufficient codebase/workflow model rather than an exhaustive simulation.
3. For each risky unknown, choose reasoning closure or the smallest discriminating probe; record its stop condition and surprise trigger.
4. Prune reasoning, review, and validation work that cannot add a new constraint or observation.
5. Clarify only the still outcome-determinative unknowns.
6. Decide single-pack vs multi-pack layout.
7. Define pack-level dependencies.
8. Identify proposed PR units when the expected result may require more than one PR; leave topology undecided.
9. Author rigorous ticket packs with:
   - lane graph,
   - scope-locked files,
   - exact behavior,
   - acceptance commands,
   - strict receipt requirements.

### Phase 2: Dispatch

1. Enter direct orchestrator mode for the normal single-pack case.
2. Emit the direct orchestrator mode contract before launching workers.
3. Emit a pre-dispatch preview for each runnable worker lane.
4. Dispatch each worker lane through its planner-selected transport with the same skill plus the explicit role lock.
5. Continue existing worker sessions for follow-ups unless unrecoverable.
6. Track receipts and blocked states across all lanes.
7. Launch newly runnable lanes only when dependencies truly clear.
8. Use optional child orchestrators only for truly independent ticket-pack sets; when used, initialize each child with the optional child-orchestrator message and send its pack as `SENIOR_DIRECTIVE`.

### Phase 3: Replan if Needed

If execution reveals a defect in decomposition, missing dependency, scope drift, or new blocker:

1. stop treating the current pack set as final,
2. switch back to Planner mode,
3. issue a revised or follow-up ticket pack,
4. dispatch that revised pack through the same runtime contract.

### Phase 4: Validate Completed Pack And Close Or Repair

When the active pack reaches reviewer / finisher completion, the top-level `auto_planner` must return to Planner mode before declaring the work done.

Validation must compare the completed outputs against:

1. the original user ask,
2. the aligned implementation problem statement,
3. the ticket-pack success criteria,
4. the accepted reviewer / finisher receipts when those lanes exist, otherwise the final required lane receipts,
5. any explicit non-goals or locked constraints.

Treat this phase as coverage reconciliation, not a fresh independent review. Inspect the accepted receipts and authoritative test evidence rather than trusting their labels; confirm that they apply to the current head, cover the original ask, satisfy every applicable quality/risk floor, and were not invalidated. Reopen reasoning, source inspection, or tests for a named coverage gap, contradiction, stale artifact, branch/integration change, required floor, or surprise trigger.

If those checks pass:

1. identify the final proposed PR units from the accepted outputs,
2. validate every proposed PR boundary with `smallest-viable-pr`,
3. when more than one PR remains, invoke `compose-cohesive-pr-stacks` and obtain an approved topology before packaging,
4. invoke the external `gh-stack` skill to execute an approved multi-PR topology,
5. mark the pack complete,
6. finalize the initiative or advance the next dependent pack,
7. report completion against the original ask rather than only against lane completion.

If those checks fail:

1. stop treating the completed lane set as final,
2. switch fully back into Planner mode,
3. author a corrective follow-up ticket pack,
4. dispatch that repair pack through the same runtime contract.

Lane completion is not final completion. Reviewer and finisher completion are not, by themselves, sufficient to end the workflow until the top-level `auto_planner` validates the result against the original ask.

## Output Style While Using This Skill

When using this skill in conversation:

- stay in planning/orchestration language,
- do not code unless explicitly overridden,
- present ticket packs in clean copy-paste blocks,
- separate pack-level state from lane-level state,
- be rigorous about receipts and dependency ordering,
- be concise with the human, but strict with the pack.
