---
name: toolkit-ship-it
description: Use when the user asks to ship changes, create or update a Toolkit PR, package a scoped worktree into a convention-matching branch, add BLUF PR copy and inline self-review comments, wait for Claude/CodeRabbit/GitHub checks, fix sensible review comments, and prepare a high-level colleague review message.
---

# Toolkit Ship It

## Purpose

Turn a scoped Toolkit change into a review-ready PR with:

- a branch that matches the user's established naming convention,
- a BLUF PR body,
- targeted inline self-comments on risky or important lines,
- Claude / CodeRabbit / reviewer comments assessed and fixed when sensible,
- relevant tests and required GitHub checks passing,
- a short human message the user can paste to colleagues asking for review.

This is a shipment coordinator, not just a PR-description generator.

## Core Rules

- Do not stage, commit, push, create PRs, post GitHub comments, or alter review threads unless the user explicitly asks.
- Before side effects, inspect the actual diff against `origin/main`; never rely on memory.
- Treat `main` as the PR base unless the user explicitly says otherwise. Before calling a PR ready, fetch and integrate current `origin/main`.
- Preserve unrelated local work. Never use `git add .`, `git reset --hard`, or `git checkout -- .`.
- If the worktree is mixed or dirty with unrelated files, use a clean disposable worktree or ask before staging.
- For a new branch, infer the user's usual prefix from explicit instructions, repository guidance, and recent PR heads authored by `@me`. If there is no reliable prefix, use an unprefixed short kebab-case summary. Never create or push a branch beginning with `codex/`.
- If the current branch does not match the inferred convention, do not rename it silently. Call it out and ask or follow the user's explicit instruction.
- During a merge from `origin/main`, do not silently override recently approved work on shared `main`. Preserve the PR's intended behavior by reconciling it onto current main, not by blindly taking the PR text. Do not use blanket `-X ours`; resolve conflicts file-by-file and hunk-by-hunk.
- Fix review comments that are correct and in scope. Defer comments that broaden scope, destabilize Button/BAS/OAA, or conflict with the PR goal, and explain why.
- Use plain language in PR descriptions, inline comments, code comments, docstrings, and Slack messages. State what changes, what can fail, and what the reviewer should check. Avoid jargon and abstract shorthand when concrete wording is available.
- Start every PR description with one unheaded sentence in the user's tone: `<what it does>, so <problem it fixes>.` Put it before every heading, stack note, implementation detail, or validation section. Preserve the detailed body below it and do not duplicate an existing correct first line.
- When reporting a PR to the user or drafting Slack copy, default to one direct sentence: `<PR link> <what it does>, so <problem it fixes>.` Leave out code, file, diff, and test details unless the user asks. Add a real blocker in the same sentence only when it changes the next action.
- When shipping several PRs or changing a PR train, require an accepted `compose-cohesive-pr-stacks` plan before creating, retargeting, or ordering branches. Ship each PR with `pr-create-bluf-review`; do not turn a thematic list into a stack.

## Workflow

### 1. Inspect Shipment State

Run from the candidate repo/worktree:

```bash
git status --short --branch
git branch --show-current
git rev-parse --short HEAD
git fetch origin main --prune
git diff --name-status origin/main...HEAD
git diff --stat origin/main...HEAD
git diff --cached --name-status
git ls-files --others --exclude-standard
```

For a compact bundle, run:

```bash
~/.codex/skills/toolkit-ship-it/scripts/collect_toolkit_ship_context.sh
```

If a PR may already exist:

```bash
gh pr view --json number,title,url,state,headRefName,baseRefName,reviewDecision,statusCheckRollup 2>/dev/null
```

### 2. Define Scope

Before staging or committing, state:

- what the PR is about,
- which files are included,
- which dirty/untracked files are excluded,
- whether any file is unclear,
- whether the branch needs current `origin/main`,
- what validation matches the changed surface.

If scope is ambiguous, ask. If unrelated work is present, prefer a clean disposable worktree.

If several PRs are in scope, run `compose-cohesive-pr-stacks` here and record the approved bottom-to-top branch topology before making GitHub changes.

### 3. Sync With Main Before Shipping

Before the PR is marked ready, make sure the branch is based on current `main`:

```bash
git fetch origin main --prune
gh pr view --json baseRefName,headRefName,url 2>/dev/null || true
```

If a PR exists, confirm `baseRefName` is `main`. If it is not, stop and call it out.

Default to merging current main into the PR branch unless the user asked for a different history shape:

```bash
git merge --no-edit origin/main
```

Conflict policy:

- In `git merge origin/main`, `ours` is the current PR branch and `theirs` is `origin/main`.
- Treat current `origin/main` as shared, recently approved work. Avoid overwriting it unless the PR explicitly and intentionally supersedes that behavior.
- Preserve PR intent, not necessarily PR text. When main changed the same area, start from the current main shape and re-apply the PR behavior as a minimal reconciliation.
- Prefer `theirs` for unrelated mainline cleanup, dependency churn, generated artifacts, or work outside the PR's intended scope.
- Use `ours` only when the exact branch-side code is the deliberate feature/fix under review and keeping main would remove that PR's purpose.
- If both sides intentionally changed the same behavior, do not guess. Summarize the conflict and ask the user or leave a clear reviewer note.
- For Button/BAS/OAA conflicts, preserve stabilized planner, dispatcher, gate, OpenCode runner, generated-app runtime, recovery, and reviewed frontend run UX unless main has an explicitly compatible fix.
- Never resolve with a blanket `git merge -X ours`, `git checkout --ours .`, or `git checkout --theirs .`.

Useful conflict inspection commands:

```bash
git diff --name-only --diff-filter=U
git diff --ours -- path/to/file
git diff --theirs -- path/to/file
git show origin/main:path/to/file
```

After resolving merge conflicts, rerun the changed-surface validation before pushing.

### 4. Branch / Stage / Commit / Push

Branch naming for new branches:

```text
<inferred-user-prefix>/<short-kebab-summary>
```

Omit the prefix when no reliable user convention can be inferred. Check recent PR heads with `gh pr list --author @me --state all --limit 30 --json headRefName` when repository guidance is absent.

Stage explicitly:

```bash
git add path1 path2 path3
```

After staging:

```bash
git diff --cached --stat
git status --short
```

Commit with a concise conventional title when possible:

```text
fix(button): restore run detail log loading
feat(button): expose generated execution contracts
docs(button): document BAS architecture flow
```

Push only after the user asks:

```bash
git push -u origin "$(git branch --show-current)"
```

### 5. Create Or Update PR

Use the `pr-create-bluf-review` skill's PR body structure. The body must be high signal:

- First line: one unheaded sentence saying what the PR does and what problem it fixes.
- BLUF: what changed and why it matters.
- Why: user-visible gap or failure mode.
- What changed: grouped by subsystem, not raw file dump.
- Stability / risk notes: especially Button/BAS/OAA planner, dispatcher, OpenCode, generated-app runtime, publishing, API contracts, or frontend run UX.
- How tested: exact commands and manual UI checks.
- Visual proof: for applicable Toolkit UI, generated-app, or other rendered changes, reuse the implementation receipt's current working-state screenshot, follow `pr-create-bluf-review`, and embed it in the PR body before calling the PR ready. Rerun the UI journey only if that evidence is missing, stale, or no longer matches the final diff.
- Reviewer notes: what to look at.
- Security/compliance: logs, secrets, PII/PHI if applicable.

Create/update with `gh`:

```bash
gh pr create --base main --head "$(git branch --show-current)" --title "<title>" --body-file /tmp/pr-body.md
gh pr edit --body-file /tmp/pr-body.md
```

After creating or updating the PR, read back the first nonblank body line. Do not call the description ready if a heading, stack position, implementation detail, or test note appears before the outcome sentence.

### 6. Add Inline Self-Comments

Add self-comments where reviewers need context:

- risky behavior changes,
- recovery/fallback paths,
- timeouts/retries,
- env/config/auth/filesystem boundaries,
- state-machine or concurrency decisions,
- compatibility shims,
- unusual choices a reviewer may otherwise simplify away.

Do not comment obvious code. Keep comments short and human.

Example tone:

```text
Please check this fallback for older runs. If it misses an older saved format, the PR can work locally while existing run links stop loading.
```

Post comments only after the PR exists and only when requested or included in the shipment instruction.

### 7. Wait For Reviews And Checks

After PR creation, monitor:

```bash
gh pr checks --watch
gh pr view --json reviewDecision,statusCheckRollup,comments,reviews,url,title,number
gh api repos/DistylAI/toolkit/pulls/<PR_NUMBER>/comments --paginate
gh api repos/DistylAI/toolkit/issues/<PR_NUMBER>/comments --paginate
```

For this workflow, Claude and CodeRabbit are active review inputs:

- Wait for Claude / CodeRabbit when they are expected and currently running.
- Inspect their actual comments, not just status labels.
- Fix comments that are correct, scoped, and improve stability.
- Do not blindly accept comments that broaden the PR, remove hard-won Button/BAS/OAA behavior, or destabilize the pipeline.
- If deferring a comment, prepare a concise rationale the user can post.

Do not announce the PR as ready until:

- relevant local validation has passed or a clear non-run reason is documented,
- required GitHub checks are green,
- Claude/CodeRabbit/actionable review comments have been handled,
- the branch is current enough for review expectations.

### 8. Colleague Review Message

When the PR is ready, default to one paste-ready sentence in the user's tone. Say only what it does and what problem it fixes:

```text
<PR link> <what it does>, so <problem it fixes>.
```

Keep it to one statement unless the user asks for more. Do not mention implementation, files, diff size, tests, CI, Claude, or CodeRabbit unless one of those is the actual blocker the colleague needs to know.

Before sending, remove wording that requires the reviewer to translate it. For example, replace “review the private-wheel resolution boundary” with “check that published apps can download private packages without exposing credentials.” Apply this same check to the PR body and inline comments.

## Validation

Choose validation based on changed surface:

- Button frontend: typecheck/build and relevant UI smoke.
- Button backend/API: focused pytest + API schema checks.
- Button engine/OpenCode: focused Bun tests under `apps/button/engine/opencode-workflow`.
- App publishing/supervisor: publisher/supervisor tests and a targeted packaging run.
- BAS/OAA pipeline behavior: one UI-started run when practical, plus checkpoint/recovery proof when the PR affects recovery.

If the user says “all tests,” treat that as required GitHub checks plus all practical changed-surface local tests. If a full suite is too expensive or blocked, say exactly what did and did not run.

## Final Response

After shipping:

- branch,
- commit hash,
- PR URL,
- validation/check status,
- inline self-comment count and focus areas,
- Claude/CodeRabbit comments handled or deferred,
- paste-ready colleague review message,
- any remaining blockers or excluded dirty files.

## References

- `references/review-readiness-and-message.md` - review loop, bot comments, checks, and colleague message style.
