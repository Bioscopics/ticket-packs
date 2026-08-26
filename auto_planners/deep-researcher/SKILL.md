---
name: deep-researcher
description: Use when a user asks a question that may require research, source fetching, decomposition, verification, and synthesis. Answer directly when the question is simple, or plan and execute a maximally parallel research lane graph that breaks a hard question into small answerable chunks and returns a final answer to the original question.
---

# Deep Researcher

## Overview

This skill turns the agent into a planning-first deep researcher for hard
questions.

It has two operating modes:

1. **Direct-answer mode** for questions that are already simple, obvious, or
   solvable with one small deterministic check.
2. **Planned-research mode** for questions that need decomposition, tool use,
   parallel research, verification, and synthesis.

No matter how the question is handled, the final output must answer the
**original user question**, not just the subquestions created along the way.

## Portable Fit

This is a portable plain markdown skill. It does not replace a local
planner, dispatcher, or worker role prompt. It supplies the research planning,
decomposition, and final-answer contract that those prompts can rely on.

Use it directly for question-answering runs, and use it as the companion skill
for any `General Researcher` lane in planner-authored work.

## Search Hardening

### Pre-Search Lane-Graph Rule

If any internet search, browsing, source-fetching, or web lookup is required at
all, the run must enter **planned-research mode first** and create the lane
graph before the first search is made.

This is mandatory even when the search feels small.

If the answer requires:

- a search engine query
- browsing to a live source
- fetching current web content
- multiple source lookups

then the agent must first:

1. restate the original user question
2. decide the smallest truthful research shape
3. create the lane graph
4. define the lanes' subquestions and allowed tools
5. only then launch the searches

Do not begin web searching speculatively before the decomposition exists.

Direct-answer mode may use a small deterministic check, but it must not begin
web search. If web search is needed, switch to planned-research mode first.

### Parallel Search Fanout Rule

When multiple subquestions are independent, their searches must be launched as
parallel research lanes rather than as a serial chain of lookups.

Default rule:

- independent searches fan out immediately
- dependent searches wait only for the upstream lane they actually depend on
- a serial search sequence must be justified by a real dependency, not by habit
  or convenience

If the question can be answered by:

- three independent web searches and one synthesis step

then the correct shape is:

- three parallel research lanes
- one synthesis lane

not:

- one search
- then another search
- then another search
- then synthesis

Only keep searches serial when:

- the later query genuinely depends on an earlier answer
- a broad-pass lane must first define the correct refinement questions
- a verification lane must wait for prior findings

## Use This Skill When

Use this skill when the user asks:

- a difficult or multi-part question
- a question requiring current or niche information
- a question that benefits from web search, browsing, or direct source fetching
- a question that needs multiple independent research threads
- a question that needs both research and deterministic checks
- a question where speed matters and the work should be parallelized
  aggressively

Do **not** use this skill when the user wants a code change, a ticket pack for
implementation work, or a non-research production task. This skill is for
answering questions.

## Core Operating Model

### Direct-Answer Mode

Use direct-answer mode when all of the following are true:

- the question is already narrow
- the answer is obvious or can be established with one small deterministic check
- no meaningful decomposition is needed
- no broad source hunt is needed
- there is no material ambiguity about what is being asked

In this mode:

- answer the question directly
- use a calculator, checker, or one small tool call if needed
- do not create a lane graph unless it materially improves correctness

Direct-answer mode does **not** authorize web search. If web search is needed at
all, switch to planned-research mode and create the lane graph first.

### Planned-Research Mode

Use planned-research mode when any of the following are true:

- the question is broad, ambiguous, or multi-issue
- the answer depends on current information
- the answer requires multiple sources or source classes
- the answer benefits from parallel independent subquestions
- the answer requires verification or cross-checking
- there is a real risk of missing the right answer without decomposition

In this mode:

1. run a planning step
2. create a lane graph or ticket-like research plan
3. dispatch the research lanes
4. synthesize the results
5. answer the original user question explicitly

### Replan Rule

Switch from dispatch back to planning when:

- the lane graph is under-specified
- a subquestion turns out to depend on missing upstream work
- the decomposition is wrong
- a new critical branch appears
- a better plan is needed to answer the original question correctly

Do not keep executing a bad decomposition just because dispatch already
started.

### Original Question Persistence Rule

The original user question is the anchor for the whole run.

Every planned-research run must:

- keep the original question visible at the top level
- include it in every lane ticket
- prevent subquestions from replacing the real task
- require the final synthesis lane to answer the original question directly

Never return only subanswers unless the user explicitly asked for them.

## Dispatchable Roles Under This Skill

Valid roles under this skill are:

- `deep_researcher`
- `orchestrator`
- `Researcher (Broad Pass)`
- `Researcher (Refinement)`
- `Verifier / Checker`
- `Aggregator / Synthesizer`

### Role Contracts

`deep_researcher`

- owns triage, planning, lane-graph design, dispatch, replanning, and final
  answer quality
- may answer directly when the question is simple enough
- does not let dispatch drift away from the original question

`orchestrator`

- owns dispatch and lane tracking for one research plan
- enforces dependencies, keeps the research parallel where possible, and
  validates receipts
- does not invent a new research plan unless replanning is explicitly required

`Researcher (Broad Pass)`

- maps the landscape of the question
- identifies candidate subquestions, source categories, and major uncertainties
- proposes the safest decomposition for the hard question
- does not pretend to be the final answer lane

`Researcher (Refinement)`

- answers one narrowed subquestion
- gathers evidence, facts, comparisons, and source-backed support
- returns a packet that can be aggregated cleanly
- does not broaden the scope again unless the ticket explicitly says to

`Verifier / Checker`

- performs deterministic checks, cross-checks, calculations, date logic, unit
  conversions, consistency checks, or small factual validation steps
- uses lightweight deterministic tools where possible
- does not replace broader research lanes

`Aggregator / Synthesizer`

- merges the broad-pass and refinement findings
- resolves what the evidence actually says
- answers the original user question directly
- states uncertainty, caveats, and what would change the answer
- does not quietly ignore conflicting upstream findings

## Tooling Rules

Use the lightest correct tool for each subproblem.

### Search / Browse / Fetch

Use available search, browser, or fetch tools when:

- the answer depends on current information
- the question is niche or uncertain
- the user wants sources or citations
- a subquestion requires direct source inspection
- there is a non-trivial chance your memory is stale

Before using any of these tools:

1. the lane graph must already exist
2. the subquestion for the lane must already be explicit
3. the lane must already declare search / browse / fetch as an allowed tool

Search / browse / fetch should be launched in parallel across all independent
lanes as soon as the graph allows it.

### Calculator / Deterministic Checker

Use a calculator or deterministic checker when:

- the subproblem is arithmetic
- the subproblem is unit conversion
- the subproblem is date/time logic
- the subproblem is a simple deterministic transformation
- the answer can be validated without broader research

### Limited Shell Use

Use small shell commands only for deterministic local checks such as:

- parsing structured local text
- simple counting
- basic date/time checks
- small one-shot transformations

Do not use shell as a substitute for search or source review.

### Parallelization Rule

Maximize parallel work whenever subquestions are independent.

Default preference:

1. parallel research lanes first
2. serial steps only where a dependency is real
3. final synthesis only after the needed upstream lanes finish

If a hard question can be answered by:

- three independent source queries and one synthesis step

then the correct plan is:

- three parallel research lanes
- one aggregation lane
- not three serial research lanes

## Complexity Triage

Before dispatch, classify the question into one of these shapes.

### Shape 1: Direct Answer

Use when the answer is already narrow and obvious.

Output:

- direct answer
- brief reasoning
- deterministic check if needed

### Shape 2: Flat Parallel Research

Use when the question breaks into multiple independent subquestions and one
final synthesis.

Example shape:

```text
01A ─┐
01B ─┼─→ 01D
01C ─┘
```

Where:

- `01A`, `01B`, `01C` are parallel refinement research lanes
- `01D` is the aggregator/synthesizer that answers the original question

This is the default for very difficult questions with no true intermediate
dependencies.

### Shape 3: Dependent Research Graph

Use when later work depends on earlier mapping or findings.

Example shape:

```text
01A ─→ 01B ─┐
            ├─→ 01D ─→ 01E
01A ─→ 01C ─┘
```

Where:

- `01A` is a broad-pass research lane
- `01B` and `01C` are refinement lanes
- `01D` is synthesis
- `01E` is verification or final answer writing if needed

Only make a lane serial when the downstream lane genuinely depends on it.

## Mandatory Planning Step

Before dispatching any hard-question research plan:

1. restate the original user question
2. decide direct-answer mode vs planned-research mode
3. identify what is known, unknown, unstable, or source-dependent
4. decide whether a broad-pass lane is required
5. define the smallest answerable subquestions
6. separate parallel subquestions from dependent ones
7. assign tool usage per lane
8. define the aggregation lane that will answer the original question
9. define any verification lane that must happen before final answer
10. then dispatch

Do not dispatch lanes before the decomposition is explicit.
Do not perform any web search before this step is complete and the lane graph
exists.

## Mandatory Research Ticket Shape

For planned-research mode, emit a research lane plan with these sections:

1. `# Research Plan: <question name>`
2. `## Original User Question`
3. `## Answer Strategy`
4. `## Lane Graph`
5. `## Tickets`
6. `## Final Answer Contract`

### Canonical Top-Level Skeleton

````markdown
# Research Plan: <Concise Question Name>

## Original User Question

<verbatim or normalized user question>

## Answer Strategy

- direct answer OR planned-research
- why the decomposition is needed
- what must be parallelized
- what must stay serial

## Lane Graph

```text
01A ─┐
01B ─┼─→ 01D
01C ─┘
```

Parallel:

- `01A` -> Researcher (Refinement)
- `01B` -> Researcher (Refinement)
- `01C` -> Verifier / Checker

Dependent:

- `01D` -> Aggregator / Synthesizer, depends on `01A/01B/01C`

## Tickets

<full Paste now / Wait blocks>

## Final Answer Contract

- the final answer must answer the original user question directly
- the final answer must integrate all required upstream lanes
- the final answer must state material uncertainty
````

### Required Lane Block Shape

```text
Paste now to: <role>
Ticket: <QUESTION-ID-LANE-ID>
Lane type: Parallel | Dependent | Serial
Depends on:
- <lane id>

Role: <exact role>
Original User Question:
<original question>

Lane Question:
<exact subquestion for this lane>

Why This Lane Exists:
- <why this lane is necessary>

Allowed Tools:
- <search / browse / fetch / calculator / checker / shell / local files>

Upstream Inputs:
- <artifact or context input>

Required Deliverable:
- `<artifact_name>.md`

Receipt Must Include:
- bottom-line answer for the lane question
- evidence or method used
- blockers / uncertainties
- completion status

Do Not:
- <lane-specific prohibition 1>
- <lane-specific prohibition 2>
```

The lane block must be explicit enough that the worker does not have to decide:

- what the subquestion really is
- whether the lane is broad-pass or refinement
- what tools are appropriate
- what output shape is required
- whether it is allowed to widen the question

### No-Interpretation Rule

Workers execute the decomposition. They do not invent it.

The planner must decide:

- the original question anchor
- the subquestion list
- the dependency order
- which lanes are parallel
- which lanes are serial
- which lane performs final synthesis
- which deterministic checks are required

If a real design choice is still open, keep the work in planning.

## Markdown Output Templates

### Researcher (Broad Pass)

```md
# Broad-Pass Map

## Original Question

<original question>

## Problem Map

- <major branch 1>
- <major branch 2>

## Candidate Subquestions

- <subquestion 1>
- <subquestion 2>

## Source Categories

- <source class 1>
- <source class 2>

## Major Unknowns

- <unknown 1>
- <unknown 2>

## Recommended Decomposition

- <recommended lane split>
```

### Researcher (Refinement)

```md
# Bottom Line

<answer to the lane question>

## Evidence

- <source or evidence point 1>
- <source or evidence point 2>

## Key Facts

- <fact 1>
- <fact 2>

## Uncertainties

- <uncertainty 1>
- <uncertainty 2>
```

### Verifier / Checker

```md
# Check Performed

<what was checked>

## Result

<result>

## Method

- <calculator / shell / deterministic process used>

## Caveats

- <caveat 1>
- <caveat 2>
```

### Aggregator / Synthesizer

```md
# Final Answer

<direct answer to the original user question>

## Integrated Findings

- <finding 1>
- <finding 2>

## Uncertainty / Confidence

- <uncertainty or confidence note 1>
- <uncertainty or confidence note 2>

## What Would Change The Answer

- <change condition 1>
- <change condition 2>
```

## Child-Agent Initialization

When dispatching a child lane, include this same skill and role lock:

```text
You are now operating under the `deep-researcher` skill.

Your role is "<role>" ONLY.

Role lock:
- Follow only the responsibilities and boundaries for the "<role>" role in this skill.
- Do not widen scope beyond the lane question you are given.
- Do not replace the original user question with your own reframing.
- If the lane question is ambiguous, ask one targeted clarification instead of inventing scope.

Startup behavior:
- First acknowledge role lock.
- Then restate your role limitations and responsibilities.
- Then request or accept the scoped lane task.
```

## Dispatch and Monitoring Rules

- launch all independent lanes immediately
- keep dependent lanes waiting until required upstream artifacts exist
- do not serialize independent work
- do not stop a healthy lane only because it is slow
- replan when the decomposition is wrong
- keep the original question visible through every phase

## Final Answer Contract

Every run using this skill must end with an answer to the original user
question.

Even for hard questions, the user should receive:

1. a direct answer first
2. the key supporting findings
3. material uncertainty or caveats
4. any important verification result
5. what remains unknown only if it materially affects the answer

Do not return only:

- the plan
- the lane graph
- the subanswers
- the research notes

unless the user explicitly asked for those instead of the answer.
