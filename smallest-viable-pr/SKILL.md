---
name: smallest-viable-pr
description: Use when reviewing pull requests for unnecessary scope, validating proposed PR boundaries, or recommending splits. Defines each resulting PR contract and classifies relationships among split units, then hands topology decisions to compose-cohesive-pr-stacks.
---

# Smallest Viable PR

## Core Doctrine

A PR is presumed too large until the diff proves it is the smallest honest mergeable unit.

Review for merge shape, not just correctness:

- the PR should change the fewest files and lines that solve the stated problem;
- every changed file should have a clear reason tied to the PR goal;
- existing helpers, components, routes, schemas, prompts, config, tests, and conventions should be reused before new surfaces are added;
- obsolete or duplicate code should be deleted when replacement behavior is added;
- broad refactors, new dependencies, framework/runtime changes, and unrelated cleanup should be split unless they are strictly required.

A working PR can still be review-failing if it is larger, more rigid, or harder to maintain than necessary.

## Boundary And Handoff Responsibility

Validate one proposed PR boundary at a time. Decide whether that boundary is the smallest honest, independently reviewable merge unit.

When recommending a split, define each resulting PR contract and classify every relevant relationship between the resulting units as:

- `hard dependency`;
- `ordering preference`;
- `contextual relationship`;
- `unrelated`.

Do not turn those relationships into a stack plan. Hand the validated units and relationship evidence to `compose-cohesive-pr-stacks`, which owns partitioning and order.

## Review Inputs

Base conclusions on evidence from the PR, not intent:

```bash
git status --short --branch
git diff --name-status <base>...HEAD
git diff --stat <base>...HEAD
git diff --check <base>...HEAD
git diff --unified=80 <base>...HEAD -- <important files>
```

Use the PR title/body only to understand the claimed goal. The actual diff decides whether the PR is smallest viable.

## Smallest Viable PR Checks

### 1. State The PR Contract

Summarize the smallest behavior delta in one or two sentences:

- what user-visible or system-visible behavior changes;
- what must remain unchanged;
- what proof would make the PR safe to merge.

If the contract cannot be stated narrowly, the PR likely needs splitting or replanning.

### 2. Map The Changed Surface

Classify changed files by purpose:

- required behavior change;
- tests or validation;
- docs/config/prompt/schema;
- generated/lock/package artifact;
- refactor-only;
- unrelated cleanup;
- suspicious or unexplained.

Every file outside the required behavior/test/doc surface needs an explicit reason.

### 3. Check Reuse Before New Code

Look for duplicate or parallel implementation:

- new helper/component/service similar to an existing one;
- copied parsing, validation, API, filesystem, queue, retry, or rendering logic;
- new fallback path instead of fixing the source contract;
- new abstraction with one caller;
- new config or env surface when an existing one already exists.

If reuse was possible and not used, return `NO-GO` unless the PR explains why reuse would be worse.

### 4. Separate Behavior From Refactor

Treat mixed refactor + behavior change as suspicious.

Accept only when:

- the behavior change cannot be made safely without the refactor;
- the refactor is narrow and mechanically reviewable;
- tests prove the affected behavior before and after.

Otherwise ask to split: first pure refactor, then behavior change, or shrink the PR to behavior only.

### 5. Challenge New Dependencies And Runtime Surface

Return `NO-GO` or require explicit approval for:

- package, lockfile, build, Docker, CI, or install changes;
- shared runtime/framework/infrastructure changes;
- new long-lived processes, queues, background jobs, caches, or persistence paths;
- new auth, filesystem, network, sandbox, or env-var boundaries.

These may be valid, but they carry a higher burden of proof and should not ride along with a narrow fix.

### 6. Confirm Deletion And Simplification

When the PR adds replacement behavior, check whether it removes:

- dead branches;
- obsolete fallbacks;
- duplicate helpers;
- stale tests or fixtures;
- unused config/prompt/schema paths.

If nothing was deleted, ask whether the PR is layering new behavior over old debt.

## Tripwires

Treat these as review escalation triggers:

- more than 5 changed files for a narrow bugfix;
- more than 300 net new lines;
- any new dependency or lockfile churn;
- any shared runtime/framework/infrastructure change;
- any broad rename, move, or refactor mixed with behavior;
- new helper/abstraction with no reuse proof;
- generated-looking boilerplate not clearly required;
- tests that mostly lock implementation details rather than behavior;
- PR body claims a small fix while diff shows architectural change.

Tripwires do not automatically block merge. They require explicit evidence that this is still the smallest viable PR.

## Review Output

Include this section in the PR review when the PR changes code or runtime-relevant config:

```markdown
**Smallest Viable PR**
- Verdict: PASS | NO-GO | PASS WITH SHRINK REQUESTS
- PR contract: <smallest behavior delta>
- Changed surface: <files/subsystems and why they are required>
- Reuse proof: <existing surfaces reused or missing proof>
- Refactor/dependency/runtime tripwires: <none or listed>
- Deletion/simplification: <what was removed, or what should be removed>
- Required shrink requests:
  - <specific file/surface to remove, split, reuse, or justify>
- Resulting PR units when split:
  - <unit name and smallest behavior contract>
- Relationships among resulting units:
  - <unit A -> unit B: hard dependency | ordering preference | contextual relationship | unrelated, with evidence>
```

If there are no shrink issues, say so directly. Do not invent nitpicks.

## Comment Guidance

For inline review comments:

- comment on the smallest changed line that demonstrates unnecessary scope;
- ask for a shrink, split, reuse proof, or targeted test;
- do not redesign the implementation unless the user asks.

Useful wording:

```markdown
I’d push to shrink this before merge. The PR goal appears to be <goal>, but this hunk also changes <extra surface>. Can we either split that out or show why this file must change for the stated behavior?
```

```markdown
This looks like a parallel implementation of <existing surface>. Can we reuse <existing file/helper/component> instead, or add a short note explaining why reuse would break the new behavior?
```

## Decision Rule

Prefer `NO-GO` for unnecessary size, duplication, or unrelated surface even if tests pass. Prefer `PASS WITH SHRINK REQUESTS` when the core fix is sound but a small amount of removable scope remains.

When the result is two or more independently reviewable PR contracts, hand those contracts and their classified relationships to `compose-cohesive-pr-stacks`. Splitting defines and validates the boundaries; the stack skill decides whether any hard dependency justifies a train and what stays standalone.
