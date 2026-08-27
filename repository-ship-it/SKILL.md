---
name: repository-ship-it
description: Ship scoped repository changes as review-ready pull requests. Use when the user asks to package a worktree, create or update a PR, add BLUF copy and useful inline self-review, handle checks or review feedback, or prepare a concise colleague review message.
---

# Repository Ship It

## Purpose

Turn a scoped repository change into a review-ready PR with:

- repository-native branch and base conventions,
- a BLUF PR body,
- targeted inline self-comments on risky or important lines,
- automated and human review comments assessed and fixed when sensible,
- relevant tests and required checks passing,
- a short human message the user can paste to colleagues asking for review.

This is a shipment coordinator, not just a PR-description generator.

## Core Rules

- Do not stage, commit, push, create PRs, post comments, or alter review threads unless the user explicitly asks.
- Before side effects, inspect the actual diff against the intended PR base; never rely on memory.
- Infer repository identity, remote, default base, branch convention, and validation commands from the target repository. Explicit user instructions and repository guidance take precedence.
- Preserve an existing PR's base unless the user asks to retarget it. For a new PR, use the repository's default branch unless another base is explicit.
- Preserve unrelated local work. Never use `git add .`, `git reset --hard`, or `git checkout -- .`.
- If the worktree is mixed or dirty with unrelated files, use a clean disposable worktree or ask before staging.
- For a new branch, infer the prefix from explicit instructions, repository guidance, and recent PR heads authored by `@me`. If none is reliable, follow the active coding environment's documented default or use a short kebab-case summary.
- Do not rename a current branch silently when it differs from the inferred convention. Call it out and follow the user's direction.
- Integrate the current base branch using the repository's established merge or rebase convention. Resolve conflicts file-by-file; never use blanket “ours” or “theirs” resolution.
- Fix review comments that are correct and in scope. Defer comments that broaden scope, weaken intentional behavior, or conflict with the PR goal, and explain why.
- Use plain language in PR descriptions, inline comments, code comments, docstrings, and colleague messages. State what changes, what can fail, and what the reviewer should check.
- Start every PR description with one unheaded sentence: `<what it does>, so <problem it fixes>.` Put it before headings, stack notes, implementation details, and validation.
- When reporting a PR or drafting colleague copy, default to one direct sentence: `<PR link> <what it does>, so <problem it fixes>.` Add a blocker only when it changes the next action.
- When shipping several PRs or changing a PR train, require an accepted `compose-cohesive-pr-stacks` plan before creating, retargeting, or ordering branches. Ship each PR with `pr-create-bluf-review`.

## Workflow

### 1. Inspect Repository And Shipment State

Run from the candidate repository or worktree:

```bash
git status --short --branch
git branch --show-current
git rev-parse --short HEAD
git remote -v
gh repo view --json nameWithOwner,defaultBranchRef 2>/dev/null || true
gh pr view --json number,title,url,state,headRefName,baseRefName,reviewDecision,statusCheckRollup 2>/dev/null || true
```

Determine:

- `REMOTE`: the remote that owns the intended PR, normally inferred from the branch upstream or repository guidance;
- `REPO`: `owner/name` from `gh repo view`, not a hardcoded organization or repository;
- `BASE`: an existing PR's `baseRefName`, an explicit user choice, or the repository's default branch;
- branch convention: explicit instruction, repository guidance, recent authored PR heads, then the coding environment default.

Fetch and inspect against those derived values:

```bash
git fetch "$REMOTE" "$BASE" --prune
git diff --name-status "$REMOTE/$BASE"...HEAD
git diff --stat "$REMOTE/$BASE"...HEAD
git diff --cached --name-status
git ls-files --others --exclude-standard
```

For a compact bundle, run:

```bash
~/.codex/skills/repository-ship-it/scripts/collect_repository_ship_context.sh
```

The helper infers the PR remote and base. Override them only when necessary:

```bash
REMOTE=upstream BASE=release/v2 ~/.codex/skills/repository-ship-it/scripts/collect_repository_ship_context.sh
```

### 2. Define Scope

Before staging or committing, state:

- what the PR is about,
- which files are included,
- which dirty or untracked files are excluded,
- whether any file is unclear,
- the derived repository, remote, base, and branch convention,
- what validation matches the changed surface.

If scope is ambiguous, ask. If unrelated work is present, prefer a clean disposable worktree.

If several PRs are in scope, run `compose-cohesive-pr-stacks` here and record the approved topology before making GitHub changes.

### 3. Sync With The PR Base

Before calling the PR ready, fetch the derived base again and confirm any existing PR still targets the expected base:

```bash
git fetch "$REMOTE" "$BASE" --prune
gh pr view --json baseRefName,headRefName,url 2>/dev/null || true
```

Use the repository's documented merge or rebase convention. If none exists and changing history would be consequential, ask rather than guessing.

Conflict policy:

- Treat the fetched base as shared, recently approved work.
- Preserve PR intent, not necessarily the branch's exact text. When both sides changed the same area, start from the current base shape and reapply the PR behavior minimally.
- Keep unrelated base cleanup, dependency churn, or generated artifacts unless the PR deliberately supersedes them.
- If both sides intentionally changed the same behavior, summarize the conflict and ask the user or leave a clear reviewer note.
- Never resolve with blanket `-X ours`, `git checkout --ours .`, or `git checkout --theirs .`.

Useful inspection commands:

```bash
git diff --name-only --diff-filter=U
git diff --ours -- path/to/file
git diff --theirs -- path/to/file
git show "$REMOTE/$BASE":path/to/file
```

After resolving conflicts, rerun changed-surface validation before pushing.

### 4. Branch, Stage, Commit, And Push

Use the inferred branch convention. Stage only explicit paths:

```bash
git add path1 path2 path3
git diff --cached --stat
git status --short
```

Use a concise repository-native commit title, following local guidance or recent commit style. Push only after the user asks:

```bash
git push -u "$REMOTE" "$(git branch --show-current)"
```

### 5. Create Or Update The PR

Use the `pr-create-bluf-review` skill's PR body structure:

- First line: one unheaded sentence saying what the PR does and what problem it fixes.
- BLUF: what changed and why it matters.
- Why: user-visible gap or failure mode.
- What changed: grouped by subsystem, not a raw file dump.
- Stability and risk: important behavior, persistence, runtime, compatibility, API, security, and UI implications.
- How tested: exact commands and manual user-flow checks.
- Visual proof: for rendered changes, reuse current implementation evidence when it still matches the final diff; rerun only when missing or stale.
- Reviewer notes: what deserves a closer look.
- Security and compliance: logs, secrets, PII, or PHI when applicable.

Create or update with derived values:

```bash
gh pr create --repo "$REPO" --base "$BASE" --head "$(git branch --show-current)" --title "<title>" --body-file /tmp/pr-body.md
gh pr edit --repo "$REPO" --body-file /tmp/pr-body.md
```

Read back the first nonblank body line. The description is not ready if a heading, stack position, implementation detail, or test note appears before the outcome sentence.

### 6. Add Inline Self-Comments

Add self-comments where reviewers need context:

- risky behavior changes,
- recovery or fallback paths,
- timeouts and retries,
- environment, config, auth, or filesystem boundaries,
- state-machine or concurrency decisions,
- compatibility shims,
- unusual choices a reviewer may otherwise simplify away.

Do not comment obvious code. Keep comments short and human. Post them only after the PR exists and only when the shipment request authorizes it.

### 7. Wait For Reviews And Checks

Monitor the actual repository and PR:

```bash
gh pr checks --repo "$REPO" --watch
gh pr view --repo "$REPO" --json reviewDecision,statusCheckRollup,comments,reviews,url,title,number
gh api "repos/$REPO/pulls/$PR_NUMBER/comments" --paginate
gh api "repos/$REPO/issues/$PR_NUMBER/comments" --paginate
```

- Determine expected automated reviewers from existing checks, repository guidance, or prior PRs; do not assume particular bots exist.
- Inspect actual comments, not just status labels.
- Fix comments that are correct, scoped, and improve stability.
- Do not accept comments that broaden the PR or remove intentional behavior merely to simplify the diff.
- If deferring a comment, prepare a concise rationale the user can post.

Do not announce the PR as ready until relevant local validation has passed or has a precise non-run reason, required checks are green, and actionable review comments have been handled.

### 8. Colleague Review Message

When the PR is ready, default to one paste-ready sentence:

```text
<PR link> <what it does>, so <problem it fixes>.
```

Do not mention implementation, files, diff size, tests, CI, or review bots unless one is the actual blocker the colleague needs to know. Rewrite jargon into the concrete product or operational effect.

## Validation

Infer validation from repository guidance, changed paths, package scripts, CI configuration, and nearby tests. Prefer the smallest checks that prove the changed behavior, including a realistic user flow for user-facing changes. If the user requests every test or required check, run all practical checks and state exactly what did and did not run.

## Final Response

After shipping, report:

- branch and commit hash,
- PR URL and base,
- validation and check status,
- inline self-comment count and focus areas,
- review comments handled or deferred,
- paste-ready colleague review message,
- remaining blockers or excluded dirty files.

## References

- `references/review-readiness-and-message.md` — review loop, automated comments, checks, and colleague message style.
