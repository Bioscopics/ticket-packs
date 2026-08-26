---
name: adaptive-research-frontier
description: "Use only when auto-planner-ticket-pack or task-auto-planner-ticket-pack explicitly selects adaptive_then_planned for a General Researcher lane whose search topology cannot be specified safely up front. Run bounded, tool-neutral adaptive discovery over web, codebase, private-corpus, database, runtime, or mixed evidence surfaces; then hand a validated evidence packet to the unchanged deep-researcher skill. Do not use as a standalone user entry point, an adaptive-only answer engine, or a replacement for deep-researcher."
---

# Adaptive Research Frontier

## Purpose

Discover the shape of an uncertain research problem through small parallel probes, dynamically allocate effort toward useful signals, and stop once the evidence frontier is stable enough for `deep-researcher` to perform the proven planning, gap-filling, synthesis, and final-answer work.

Treat this skill as an optional upstream accelerator. Keep `deep-researcher` unchanged and mandatory after adaptive discovery.

## Skill Web Contract

Accept invocation only from:

- `auto-planner-ticket-pack`, for a planning-support `general_researcher` lane;
- `task-auto-planner-ticket-pack`, for a `General Researcher` lane.

Require the planner-selected strategy `adaptive_then_planned`. Otherwise, do not run this skill. Use the existing `deep-researcher` path directly.

Keep the two research engines phase-locked:

1. Run `adaptive-research-frontier` during discovery.
2. End adaptive authority after emitting a valid handoff packet.
3. Start `deep-researcher` with that packet as upstream evidence.
4. Let `deep-researcher` own the remaining research plan, synthesis, and answer.

Never let both skills independently dispatch or replan the same frontier at the same time.

## Required Planner Inputs

Require the lane ticket to declare:

```text
Research strategy: adaptive_then_planned
Research surface: web | codebase | corpus | database | runtime | mixed
Research policy: general | exhaustive | legal | medical
Adaptive activation reason: <why the topology cannot be fixed safely up front>
Adaptive budget: <time, probe, concurrency, tool, or cost limits>
Deep-researcher handoff and final fallback: required
```

Also require:

- the original user question;
- the scoped lane question;
- allowed tools and evidence sources;
- access, confidentiality, and data-handling constraints;
- any source hierarchy or governing authority requirements;
- the expected research deliverable and receipt.

If the strategy, original question, lane question, allowed surfaces, or deep-researcher handoff is missing, stop adaptive discovery and request a corrected ticket. Do not invent the missing contract.

## Activation Gate

Validate the planner's activation reason before launching a probe. Use adaptive discovery only when the ticket names a concrete branching decision that early evidence can change, such as:

- which evidence family, subsystem, authority, hypothesis, or surface should receive the next probe;
- whether an existing convention should be extended, composed locally, or left unchanged because ownership boundaries are not yet known;
- whether an adverse, contradictory, or newly discovered dependency invalidates the initial decomposition.

Require an orientation receipt in the ticket before activating the frontier. The planner may make one cheap, bounded pass over the obvious entry point, index, contract, or nearest precedent to test whether the topology is actually unknown. The receipt must state what was checked, identify at least two still-live branches, and explain which later probe or lane would change based on the first result. A merely hypothetical possibility of redirection is not enough.

Difficulty, repository size, source count, convention sensitivity, or a desire for extra verification are not sufficient activation reasons. Prefer `planned` when the relevant files, artifacts, questions, calculations, authority families, ownership boundary, or extension pattern become enumerable after that orientation pass and independent work can be specified safely up front. A bounded codebase task qualifies only when the pass leaves genuinely plausible competing boundaries—such as shared, domain-local, host, runtime, or API ownership—or exposes a result-dependent next question. Finding the existing component, hook, contract, and nearest precedent in one pass is evidence for `planned`, not for activating adaptive discovery.

If the activation gate fails, launch no adaptive probes. Return `FALLBACK_TO_DEEP_RESEARCHER` with the routing reason and let the normal planned path own the work.

## Read Conditional References

- Read [references/probe-and-handoff-contract.md](references/probe-and-handoff-contract.md) before launching the first probe or emitting the handoff.
- Read [references/surface-adapters.md](references/surface-adapters.md) for every selected research surface.
- Read the selected profile in [references/policy-profiles.md](references/policy-profiles.md) before scoring or pruning branches. For `mixed`, read every applicable adapter section but only one policy profile unless the ticket supplies stricter combined constraints.

## Core State

Maintain one frontier rooted in the original question. A frontier node represents a question, hypothesis, evidence gap, or candidate causal path—not merely a file, URL, or search result.

Record for every node:

- stable node and parent identifiers;
- the exact question or hypothesis;
- selected evidence surface and probe action;
- expected information gain and decision relevance;
- status: `queued`, `running`, `accepted`, `pruned`, `fused`, `blocked`, or `unresolved`;
- evidence receipt identifiers;
- next-probe candidates and remaining uncertainty;
- cost consumed.

Keep state run-local. Do not promote memories or drills in v1.

## Adaptive Control Loop

### 1. Anchor The North Star

Restate the original question and lane question. Define what evidence would make the frontier stable enough to hand off. Preserve both questions in every probe ticket.

### 2. Seed Minimal Independent Probes

Launch the smallest useful set of narrow probes across distinct hypotheses, evidence families, or search regions.

- Use more shallow independent probes when uncertainty is high.
- Keep initial probes cheap and bounded.
- Do not create a complete lane graph before probing.
- Do not send multiple probes to the same region without a stated differentiation.
- Prefer parallel probes whenever they do not consume one another's results.

### 3. Normalize Receipts Immediately

Convert every result, including useful negative results, into the receipt contract. Reject narrative-only updates, unsupported conclusions, missing provenance, or receipts that cannot be tied to a frontier node.

Do not wait for an entire wave when an early receipt already creates, kills, or materially redirects a branch.

### 4. Evaluate Signal

Evaluate each branch using:

- relevance to the original and lane questions;
- expected uncertainty reduction;
- evidence quality and provenance;
- novelty versus accepted receipts;
- actionability for the next decision;
- contradiction, safety, or completeness value;
- expected cost of the next probe.

Treat these as decision dimensions, not a false-precision formula. Never equate result count, semantic similarity, or agent confidence alone with strong signal.

### 5. Reallocate The Frontier

After each meaningful receipt:

- deepen or add nearby sibling probes around strong, decision-relevant signal;
- launch a competing hypothesis when one plausible explanation is becoming dominant too early;
- fuse branches that now ask the same question from equivalent evidence;
- prune branches that are irrelevant, duplicative, disproven, inaccessible, or too costly for their expected information gain;
- retain low-frequency branches when they carry material safety, authority, contradiction, or completeness risk;
- reorient from a dead end using the new unknowns in its receipt rather than repeating the failed query.

Scale width and depth dynamically. High uncertainty favors broad shallow fanout; strong localized signal earns depth; weak signal loses budget.

### 6. Verify Selectively

Reuse an accepted verification receipt. Do not repeat a check merely to create an independent verification stage.

Add or repeat verification only when at least one condition holds:

- the claim is material to the answer and remains weakly supported;
- evidence conflicts;
- provenance, date, jurisdiction, population, version, or applicability is uncertain;
- the selected policy requires independent support;
- later evidence materially invalidates an earlier receipt;
- a deterministic test can cheaply resolve an important uncertainty.

### 7. Stop, Hand Off, Or Fall Back

Emit a validated handoff when:

- the likely answer topology is stable enough to plan;
- critical evidence families and material contradictions are represented;
- high-priority unresolved nodes are explicit;
- accepted receipts have usable provenance;
- remaining probes have low expected value relative to cost or belong in the planned phase.

Stop and fall back directly to `deep-researcher` when:

- the adaptive strategy or ticket is malformed;
- required tools, permissions, or surfaces are unavailable;
- the frontier produces weak or non-actionable signal;
- the budget is exhausted before a valid handoff;
- receipts are malformed or cannot establish provenance;
- policy constraints make continued adaptive pruning unsafe.

Pass usable partial receipts as `untrusted_partial_evidence`; do not represent them as accepted findings.

Treat `HANDOFF_READY` as an execution barrier. Once emitted, launch no more adaptive probes and do not reopen adaptive authority. The planned phase may check only the handoff's explicit unresolved questions, selective-verification needs, or a newly discovered material contradiction.

When the ticket supplies a total lane wall-clock budget, reserve at least 25% for planned gap-filling, synthesis, validation, and artifact writing. At half of the adaptive budget, check whether the frontier is already stable. At 80%, stop launching ordinary probes; spend the remainder only on a safety-critical/adverse branch required by the selected policy or emit the best valid handoff/fallback available. Never consume the whole lane budget before synthesis by silently treating the probe ceiling as a target.

## Deep-Researcher Handoff

Use the exact handoff template in [references/probe-and-handoff-contract.md](references/probe-and-handoff-contract.md). Then initialize or continue the next phase with this phase lock:

```text
Adaptive discovery is complete. You are now operating under the unchanged
`deep-researcher` skill.

Use `adaptive_research_handoff.md` as upstream evidence. Reuse accepted receipts
and do not repeat their searches or checks unless you identify a material gap,
conflict, applicability problem, or invalidation. Own all remaining planning,
gap-filling, synthesis, verification, and final-answer responsibilities under
`deep-researcher`.
```

If `deep-researcher` cannot be invoked, return `DEEP_RESEARCHER_REQUIRED` with the handoff artifact. Do not answer the original question from this skill alone.

## Probe Dispatch Contract

When agents are available, dispatch independent probes concurrently. Keep every probe narrow and include:

```text
Role: Adaptive Probe Worker ONLY
Original User Question: <root question>
Lane Question: <scoped research question>
Frontier Node: <node id and exact probe question>
Evidence Surface: <adapter>
Allowed Tools: <exact tools>
Budget: <probe-local limit>
Required Receipt: use the adaptive probe receipt contract
Do Not: synthesize the final answer, widen scope, spawn workers, or persist memory
```

If independent agents are unavailable, use parallel tool calls where possible and preserve the same receipt boundaries. Do not change the planner-selected transport, model, access scope, or fallback chain.

## V1 Quality And Complexity Guardrails

- Keep `planned` as the default strategy in both planner entry points.
- Support only `adaptive_then_planned`; prohibit `adaptive_only`.
- Keep the current `deep-researcher` files unchanged.
- Keep adaptive state ephemeral and scoped to the current lane.
- Do not create global memory, drills, indexes, or corpus copies.
- Do not bypass source permissions, repository boundaries, or data controls.
- Do not persist private source content outside planner-approved artifacts.
- Do not let adaptive exploration change the ticket pack's role, model, transport, or final-fallback contracts.
- Prefer the existing deep-researcher path whenever routing confidence is low.
- Do not activate adaptive discovery merely because a task is large, difficult, or convention-sensitive; require a topology-changing uncertainty.

## Required Adaptive Receipt

Return:

- `adaptive_status: HANDOFF_READY | FALLBACK_TO_DEEP_RESEARCHER | BLOCKED`;
- `adaptive_research_handoff.md` when any usable evidence exists;
- accepted, pruned, fused, blocked, and unresolved node counts;
- budget consumed;
- selected surface adapters and policy;
- why adaptive discovery stopped;
- `deep_researcher_required: true`;
- confirmation that no final answer was emitted and no memory or drill was persisted.
