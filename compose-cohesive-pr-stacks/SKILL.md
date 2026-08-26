---
name: compose-cohesive-pr-stacks
description: Use when validated PR units must be partitioned and ordered into cohesive GitHub stacks or left standalone. Produces the approved topology, then hands execution to the externally maintained gh-stack skill.
---

# Compose Cohesive PR Stacks

## Skill Web

- Receive candidate PR units from `auto-planner-ticket-pack` and boundary evidence from `smallest-viable-diff`.
- Use `smallest-viable-pr` first when PR boundaries are still uncertain or a large change may need splitting.
- Use `pr-review-deep-dive` when the task is a read-only audit of the PRs in a proposed train.
- Use `pr-create-bluf-review` for each PR's reviewer-facing body and inline self-review notes.
- After the user approves the topology, invoke the externally maintained `gh-stack` skill to create or update the native GitHub stack.
- Use `toolkit-ship-it` for individual Toolkit PR content and review readiness when needed; it does not replace `gh-stack` execution.

This skill partitions units and decides topology and merge order. It does not replace boundary validation, PR writing, or GitHub stack execution. Reference `gh-stack`; do not copy, modify, or reimplement its instructions here.

## Purpose

Turn a set of small PRs into the smallest sensible collection of cohesive stacks.

Do not maximize stack size or minimize stack count. A stack exists only when its PRs form one ordered, reviewable delivery chain.

Valid outcomes include:

- one cohesive stack;
- several independent stacks;
- a mixture of stacks and standalone PRs;
- no stack, when the PRs are independently mergeable.

## Inputs

Gather:

- each proposed PR's contract;
- files and subsystems changed;
- behavioral and code dependencies;
- required merge order;
- validation performed by each PR;
- whether each PR can merge, deploy, or roll back independently;
- intended trunk branch;
- whether GitHub Stacked PRs is enabled for the repository.

If PR contracts do not exist, define them using the `smallest-viable-pr` standard before composing stacks.

## Core Model

Treat the proposed PRs as a dependency graph.

An edge `A → B` means B cannot be correctly reviewed or merged without A.

A GitHub stack must be a linear chain:

```text
trunk ← PR A ← PR B ← PR C
```

Relatedness alone does not create a dependency. Two PRs touching the same feature, ticket, or subsystem may still belong in separate stacks if neither depends on the other.

## Workflow

### 1. Preserve PR Boundaries

Start from the smallest viable PR boundaries already established.

Do not enlarge PRs merely to make the stack topology simpler. Merge two PRs only when one of them is not independently reviewable or its boundary creates more review overhead than clarity.

### 2. Map Hard Dependencies

For every PR pair, classify the relationship:

- **hard dependency** — the upper PR cannot work or be reviewed correctly without the lower PR;
- **ordering preference** — landing one first is convenient but not required;
- **contextual relationship** — the PRs contribute to the same initiative but remain independent;
- **unrelated** — no meaningful delivery relationship.

Only hard dependencies justify stack edges.

Examples of hard dependencies:

- schema before its consumer;
- shared primitive before its use;
- backend contract before generated client integration;
- mechanical extraction before a behavior change that relies on it.

Examples that are not sufficient:

- same ticket or milestone;
- same directory or code owner;
- expected to ship around the same time;
- similar naming or implementation;
- reduced administrative overhead.

### 3. Partition Into Cohesive Units

Create separate candidate stacks when PRs differ materially in:

- user or system outcome;
- subsystem ownership;
- reviewer audience;
- deployment or rollback boundary;
- risk profile;
- release timing;
- dependency root.

Prefer two short coherent stacks over one long stack joined by a weak thematic relationship.

Leave independently mergeable PRs standalone unless stacking provides necessary review context or ordering.

### 4. Linearize Each Candidate

Confirm every candidate stack can be expressed as one chain.

If the graph branches:

```text
       PR B
      /
PR A
      \
       PR C
```

do not pretend it is a single linear stack.

Choose the smallest honest structure:

- make the shared foundation PR standalone, then create separate stacks after it merges;
- split the candidate into independent stacks;
- reconsider the PR boundaries if they created an artificial shared dependency.

Do not duplicate the foundation change across stacks.

### 5. Test Stack Cohesion

A candidate stack passes only when all answers are yes:

1. Does every upper PR require the PR immediately below it?
2. Can each PR be reviewed as one focused layer?
3. Does the ordered stack tell one coherent implementation story?
4. Would merging a prefix of the stack leave the repository valid?
5. Can the entire stack be validated against its final trunk?
6. Would reviewers benefit from seeing these PRs together?
7. Can the stack be merged and rolled back without coupling an unrelated outcome?

If the chain needs explanatory language such as "while we are here," "also," or "same initiative," split it.

### 6. Choose Bottom-to-Top Order

Order each stack from foundation to outcome:

1. prerequisites and contracts;
2. shared or lower-level implementation;
3. consumers and integrations;
4. user-facing behavior;
5. follow-up validation or documentation only when genuinely dependent.

Every PR must keep a narrow contract and include the tests appropriate to its layer. Do not postpone all meaningful validation to the top PR.

### 7. Check Operational Readiness

Before creating stacks, verify:

- all branches are in the same repository;
- the bottom PR targets the intended trunk;
- every higher PR targets the branch immediately below it;
- branch protection and CI will evaluate every layer appropriately;
- branch names, PR titles, and descriptions identify stack and position;
- each PR description starts with the `pr-create-bluf-review` one-sentence outcome line before any heading or stack note, then explains its dependency on the PR below;
- GitHub's native stack feature is enabled.

If native GitHub stacks or the external `gh-stack` skill are unavailable, stop before publishing and report the approved topology. Do not silently substitute manual base retargeting or a third-party workflow.

### 8. Hand Off Approved Topology

After the user approves the plan:

1. Pass the trunk, ordered PR units, branch names, PR metadata, and dependency edges to `gh-stack`.
2. Let `gh-stack` execute the topology and return the native GitHub stack receipt.
3. Verify the returned stack order matches this plan.

Do not create branches, retarget bases, open multiple PRs, or register a native stack directly from this skill.

## Tripwires

Repartition or request review when:

- a stack contains PRs with no hard dependency between adjacent layers;
- one PR could move between stacks without changing correctness;
- a stack crosses unrelated deployment or rollback boundaries;
- a stack exists only because all PRs share one ticket;
- an independent PR is buried in a stack;
- the dependency graph branches;
- a "foundation" PR becomes a dumping ground for multiple stacks;
- a PR cannot be validated until several later PRs exist;
- reordering PRs would not matter, suggesting the stack is only a grouping mechanism;
- combining PRs would be easier to review than maintaining their artificial boundaries.

## Output

Produce this plan before creating branches or PRs:

```markdown
## Cohesive PR Stack Plan

### Stack 1: <cohesive outcome>

Purpose: <single delivery outcome>
Trunk: <branch>

1. <PR title>
   - Contract: <smallest behavior delta>
   - Depends on: trunk
   - Why stacked: <reason>
   - Validation: <proof>

2. <PR title>
   - Contract: <smallest behavior delta>
   - Depends on: PR 1
   - Hard dependency: <specific dependency>
   - Validation: <proof>

Cohesion proof: <why this is one chain>
Prefix safety: <what remains valid after each partial merge>

### Stack 2: <cohesive outcome>

...

### Standalone PRs

- <PR title>: <why it should not be stacked>

### Rejected Groupings

- <proposed grouping>: <why it was split or left standalone>

### Execution Readiness

- Native GitHub stacks enabled: yes | no | unknown
- External `gh-stack` skill available: yes | no
- Branch topology verified: yes | no
- CI and protection implications checked: yes | no
- Topology approved by user: yes | no
- Ready to publish: yes | no
```

## Decision Rule

Choose the topology with the fewest unjustified dependency edges—not the fewest stacks.

A stack is cohesive when each PR is both:

- independently reviewable as one focused layer; and
- genuinely dependent on the ordered work below it.

When those properties conflict, fix the PR boundaries or create separate stacks. Never force unrelated small PRs into one stack merely to reduce PR administration.
