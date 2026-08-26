---
name: goal-writing
description: Write, refine, align, and propagate scalable north-star goal contracts from incomplete, conversational, or multi-step context. Use when the user asks to define, write, formalize, clarify, align, activate, or coordinate a goal; when several tasks or agents need one shared outcome; or before a substantive coding or non-coding auto-planner workflow needs an end-to-end target, terminal condition, scope locks, and completion evidence. Keep simple goals compact, expand only with task complexity or consequence, and distinguish writing a goal from activating durable goal tracking.
---

# Goal Writing

## Own the whole outcome

Infer the user-visible end state across the complete flow. Do not mistake the
latest requested piece, artifact, ticket, or lane for the goal when it is only a
means to a larger outcome.

Model the work at the lowest useful resolution:

```text
current reality -> necessary change -> integrated outcome -> durable handoff
```

Refine only the parts whose uncertainty can change the outcome, authorization,
scope, planner choice, acceptance evidence, or risk. Preserve the user's
language when it is already precise.

## Scale the goal contract

Choose the smallest contract that can keep the work aligned:

- **Compact**: Use for one obvious, reversible outcome with one owner. Write the
  goal and completion proof in two or three lines. Do not emit the full goal
  schema.
- **Standard**: Use when the work spans several steps, surfaces, artifacts, or
  assumptions. Add purpose, terminal condition, scope locks, non-goals, and
  evidence.
- **Coordinated**: Use when several existing tasks, agents, repositories,
  deliverables, stakeholders, or consequential decisions share the outcome.
  Add ownership, dependencies, reserved decisions, propagation, and final
  integration responsibility.
- **High-consequence**: Add applicable quality floors, governing constraints,
  rollback or recovery, required approvals, and durable evidence. Do not weaken
  these controls for brevity.

Do not produce a full charter for a goal that is decision-complete in one
sentence. Do not compress a consequential multi-party outcome until ownership
or completion becomes ambiguous.

## Resolve ambiguity without freezing

Separate unknowns into two classes:

1. **Outcome-determinative**: A different answer changes the north star,
   authorization, irreversible action, planner class, or acceptance standard.
   Ask one targeted clarification and write the safest useful provisional
   contract around it.
2. **Execution-local**: A planner or worker can resolve it without changing the
   goal. State a labeled assumption or leave it to the downstream owner and
   continue.

Mark a goal `provisional` when an outcome-determinative assumption remains.
Mark it `aligned` when the north star and terminal condition are stable enough
for planning. Never invent missing authority merely to avoid a question.

For a compact goal, default to exactly:

```text
Goal: <one complete end state>
Done when: <one observable proof>
Assumption: <only when a material assumption is unavoidable>
```

## Write the contract

Use only the fields needed for the selected scale. Prefer this order:

```text
Goal: <one complete end state>
Why: <value or problem resolved>
Current reality: <only facts that shape the outcome>
Terminal condition: <observable state at which the whole flow may stop>
Success evidence: <proof that the terminal condition is real>
Scope locks: <decisions downstream work may not reinterpret>
Non-goals: <nearby work intentionally excluded>
Assumptions: <labeled, consequential assumptions only>
Open questions: <outcome-determinative questions only>
Ownership and dependencies: <coordinated contracts only>
Planner handoff: <coding, non-coding, direct, or not yet ready>
Goal status: provisional | aligned | achieved | superseded
```

Write the `Goal` as an outcome, not an activity. Include the integrated finish,
not merely lane completion. Make `Success evidence` proportional to the real
boundary: unit evidence does not prove an end-to-end outcome unless it actually
exercises that outcome.

Do not invent a non-goal, scope lock, authority, or acceptance boundary merely
to fill the schema. Derive it from the user or available context, label it as a
provisional assumption, or omit it. For every standard, coordinated, or
high-consequence contract, include `Planner handoff`. If the user requested
goal writing but not execution, name the future planner and mark it `not yet
invoked`; do not activate it prematurely.

## Connect existing tasks with agent collaboration

When existing Codex tasks are part of the authorized work, read and invoke
`$agent-collaboration` at least once before concurrent mutation or independent
planning begins.

- If the user authorized coordination, send the aligned or provisional goal to
  every affected existing task once, together with its owned surface, relevant
  scope locks, dependency, and return contract.
- Use the collaboration skill's `INTRO`, `DECISION`, `CONFLICT`, `HANDOFF`, and
  `RELEASE` semantics rather than inventing another message protocol.
- Send later updates only when the goal, ownership, dependency, or acceptance
  condition materially changes. Do not broadcast routine progress.
- If the user requested only goal writing or an awareness sweep, do not message
  other tasks. Record the proposed propagation boundary instead.
- If cross-task tools are unavailable, report `coordination unavailable`; do
  not claim delivery.

Do not use `$agent-collaboration` for ephemeral subagents inside the current
task. Instead, include the stable goal, the subagent's bounded contribution,
scope locks, and return contract in each spawn or follow-up instruction.

## Hand substantive work to the auto-planner

After the goal is sufficiently aligned for decomposition, invoke exactly one
appropriate planner at least once before substantive dispatch or execution:

- Use `$auto-planner-ticket-pack` for substantive coding, repository, runtime,
  integration, or engineering work.
- Use `$task-auto-planner-ticket-pack` for substantive research, analysis,
  drafting, worksheet, evidence-synthesis, or other non-coding deliverables.
- Use neither for a simple direct answer or tiny task that does not warrant a
  planning-first workflow.
- If work truly contains independent coding and non-coding outcomes, give each
  planner its own bounded child goal, name both planner handoffs explicitly,
  and name the integration owner. A mixed coordinated contract is incomplete
  if it routes only the coding or only the non-coding child. Do not let both
  planners own the same surface.

Pass the planner the north star, terminal condition, success evidence, scope
locks, non-goals, assumptions, unresolved outcome questions, and any
collaboration receipts. Let the planner own repository or source discovery,
decomposition, maximally parallel lane topology, role/model/transport choice,
verification gates, repair routing, and packaging. Do not duplicate ticket-pack
design inside this skill.

When an auto-planner invokes this skill as its upstream goal layer, return the
goal contract to that planner instead of recursively invoking it again. Record
the selected planner in `Planner handoff`; the planner's intake satisfies this
handoff requirement.

## Preserve alignment through the lifecycle

Use this lifecycle only as far as the task requires:

```text
infer -> write -> align -> propagate -> plan -> execute -> reconcile -> close
```

- Version or supersede the goal only when the target outcome, authority, scope
  lock, or terminal condition changes. Ordinary implementation discoveries do
  not require rewriting it.
- Return a material goal change to the planner before affected work continues.
- Re-propagate only the changed contract to affected collaborators.
- At closure, compare the integrated result with the original goal and terminal
  evidence. A completed ticket, lane, review, or artifact is not automatically
  a completed goal.

## Respect the durable-goal tool boundary

Write or refine a goal in ordinary conversation by default. Call a durable
goal-creation tool only when the user explicitly asks to create, set, activate,
track, or pursue the goal. Use the whole north-star outcome as the objective,
not the next subtask. Set a token budget only when the user explicitly provides
one.

Do not claim a goal was activated when no durable goal tool succeeded.

## Avoid these failures

- Recasting the latest subtask as the entire goal.
- Blocking on execution-local ambiguity.
- Asking many questions before producing any useful provisional contract.
- Requiring planners, collaboration, or a full schema for trivial work.
- Letting every agent independently reinterpret the north star.
- Broadcasting unchanged goals or routine status to collaborators.
- Duplicating auto-planner decomposition, lane graphs, or verification logic.
- Declaring success from component completion without integrated evidence.
