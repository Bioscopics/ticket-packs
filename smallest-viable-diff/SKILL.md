---
name: smallest-viable-diff
description: Use when planning, implementing, reviewing, or finishing code changes in production repositories, especially with auto-planner-ticket-pack lanes. Minimize changed files and lines, preserve implementation boundaries, and report candidate merge units without deciding PR stack topology.
---

# Smallest Viable Diff

## Core Doctrine

Code change is presumed wrong until proven necessary. Added code is presumed debt. Deleted code is presumed good when behavior and stability are preserved.

Optimize for the smallest viable diff:

- change the fewest files and lines that honestly solve the problem;
- reuse existing helpers, components, routes, prompts, schemas, tests, and conventions before writing anything new;
- delete or simplify obsolete code when adding replacement behavior;
- avoid new abstractions, dependencies, fallbacks, and broad refactors unless explicitly justified;
- treat a working but unnecessarily large patch as review-failing.

Nothing is literally always or never, but the burden of proof for adding or broadening code should be high.

## PR Boundary Responsibility

Preserve minimal implementation boundaries and report candidate merge units when a completed change contains more than one independently reviewable behavior contract.

For each candidate unit, report:

- its smallest behavior contract;
- the files and accepted lane outputs it contains;
- whether it can be validated and rolled back independently;
- any observed relationship to another candidate unit.

These candidates are evidence, not topology decisions. Do not decide whether units should be stacked, partition stacks, choose merge order, retarget PR bases, or create GitHub stacks. `smallest-viable-pr` validates the proposed PR boundaries; `compose-cohesive-pr-stacks` owns topology.

## Preferred Intervention Order

Choose the highest, smallest, least rigid intervention that solves the problem:

1. no code change: clarify usage, document existing behavior, or close as already supported;
2. delete or simplify: remove dead code, stale fallbacks, duplicate branches, or unused config;
3. reuse existing surface: call or extend an existing helper, component, adapter, route, prompt, validator, or test harness;
4. change declarative behavior: config, schema, prompt, agent definition, skill, contract, or docs;
5. narrow edit to existing code: change the smallest owner file and preserve public contracts;
6. new code: only after reuse/narrow-edit options are disproven, with a deletion pass;
7. shared runtime, framework, dependency, package, or infrastructure change: last resort, explicit justification required.

For agentic repositories, prompts, agent definitions, skills, dispatch contracts, and validation gates should almost always be considered before runtime code.

## Diff Budget And Tripwires

Every plan should start with an expected diff budget:

- changed files: target 1-3;
- net new lines: as close to zero as possible;
- new files: zero unless justified;
- dependencies: zero;
- broad refactors: zero.

Stop and replan or get explicit approval when any tripwire is hit:

- more than 5 changed files;
- more than 300 net new lines;
- any package, dependency, or lockfile change;
- any shared runtime/framework/infrastructure change;
- any new abstraction/helper without reuse proof;
- any broad refactor mixed with feature work.

Tripwires do not make a change impossible. They force the agent to stop, explain why the diff is growing, and get the plan back under control before continuing.

## Required Pre-Change Passes

Before editing, complete these passes.

### 1. Contract the Problem

State the smallest actual behavior change required:

- what must change;
- what must remain unchanged;
- what proves success;
- what is out of scope;
- whether it can be solved without code.

### 2. Reuse Scan

Search for existing helpers, components, routes, services, adapters, validators, schemas, prompts, config, tests, and prior patterns.

Receipts must name what was searched and what was reused. Do not write “followed existing patterns” without naming the pattern.

### 3. Declare The Change Surface

Before editing, name the exact files expected to change and why each must change. If an undeclared file becomes necessary, stop and explain why the original plan was insufficient.

### 4. Prompt/Config/Contract Check

For agentic or configuration-driven systems, ask:

- Can a prompt, agent definition, skill, config, schema, or validation gate solve this?
- Is code compensating for vague instructions?
- Would code make variable behavior unnecessarily rigid?
- Is the issue deterministic substrate, or agent/workflow policy?

If prompt/config/contract can solve the issue, code is invalid.

### 5. Delete/Simplify Pass

When adding code, identify what can be deleted or simplified. If nothing can be deleted, explain why the addition is not duplicating or preserving obsolete surface.

### 6. Targeted Validation

Use the narrowest validation that proves the requested behavior. Compilation alone is not behavioral proof.

## Planner Requirements

Any ticket pack or implementation plan that permits code changes must include:

```markdown
## Smallest Viable Diff

Behavior delta:
- <smallest user-visible or system-visible change>

Expected diff budget:
- files:
- net lines:
- new files:
- dependencies:

Expected changed files:
- <path> — <why this file must change>

Forbidden files/surfaces:
- <path or area>

Reuse scan requirements:
- <helpers/components/routes/prompts/tests to inspect first>

Prompt/config/contract alternative:
- <sufficient path, or why insufficient>

Deletion/simplification target:
- <obsolete code/config/prompt to remove or simplify>

Validation:
- <targeted command or manual gate>

Tripwire policy:
- <what requires replan/approval>
```

If this section is missing, the pack is not ready to dispatch.

## Worker Receipt Requirements

Every worker that touched files must report:

```json
{
  "changed_files": [],
  "net_line_change": { "added": 0, "deleted": 0 },
  "smallest_viable_diff_rationale": "why this is the smallest honest change",
  "reuse_scan": ["existing surfaces inspected and reused or rejected with reason"],
  "prompt_config_contract_check": "why non-code or higher-layer change was sufficient, or why code was unavoidable",
  "deleted_or_simplified": ["obsolete code/config/prompt removed or simplified"],
  "new_abstractions_added": ["name and justification, or empty"],
  "tripwires_hit": ["large diff / dependency / new file / shared runtime change, or empty"],
  "out_of_scope_files_touched": [],
  "candidate_merge_units": ["smallest independently reviewable behavior units, or one unit for the whole lane"],
  "candidate_relationship_evidence": ["observed dependency or independence evidence without choosing topology"],
  "validation": "exact command/output or reason not run"
}
```

A receipt is incomplete without reuse proof, smallest-diff rationale, deletion/simplification accounting, and targeted validation.

Candidate merge units must remain narrow and evidence-based. Their presence does not authorize the worker, reviewer, or finisher to package multiple PRs or call them a stack.

## Reviewer Requirements

Reviewers must actively resist unnecessary code. Return `NO-GO` when a diff works but is larger, more duplicative, or more rigid than necessary.

Required review questions:

1. Could this have been solved with no code?
2. Could config, prompt, schema, contract, or docs solve it?
3. Did the worker reuse existing surfaces?
4. Did the worker duplicate an abstraction?
5. Did the worker touch more files than necessary?
6. Did added code replace and delete obsolete code where possible?
7. Did the diff add a fallback chain instead of fixing the source behavior?
8. Did the diff mix refactor with feature work?
9. Did it hit a tripwire without explicit approval?
10. Did validation prove the motivating behavior?

Reviewer output must include:

```text
Smallest viable diff: PASS | NO-GO
Reuse proof: PASS | NO-GO
Deletion/simplification pass: PASS | NO-GO
Tripwires: none | listed
Required shrink requests:
- ...
```

## Finisher Requirements

Before packaging or PR creation, confirm:

- final diff matches approved scope;
- tripwires are approved or absent;
- no undeclared files were touched;
- new files and dependencies are justified;
- obsolete code was removed where possible;
- reviewer left no unresolved minimal-diff objections.

## Slop Detectors

Treat these as warning signs:

- 10+ files changed for narrow behavior;
- large generated-looking boilerplate;
- new helper with a name similar to an existing helper;
- new abstraction with only one caller;
- new fallback path rather than fixing an upstream contract;
- copied parsing/validation code;
- package/dependency change for a local issue;
- broad rename/refactor mixed with behavior change;
- future-proof extension point not used now;
- parallel implementation of an existing route/component/service;
- tests that assert implementation details but not behavior;
- runtime code compensating for vague agent/workflow instructions.

## Escalation Template

If a larger or lower-layer change appears unavoidable, stop and report:

```text
I believe a larger/lower-layer code change is necessary.

Smallest behavior delta:
Higher-layer alternatives tried:
Why they are insufficient:
Existing helpers/components inspected:
Proposed changed files:
Expected added/deleted lines:
New files/dependencies:
Code to delete or simplify:
Validation:
Risk of not doing this:
```

Until this is accepted, the large/lower-layer change is not authorized.

## Default Decision Rule

If unsure, do not add code. Delete less, reuse more, and ask for a smaller plan.
