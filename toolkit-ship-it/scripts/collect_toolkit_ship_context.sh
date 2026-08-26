#!/usr/bin/env bash
set -euo pipefail

echo "## Git status"
git status --short --branch

echo
echo "## Current branch"
git branch --show-current

echo
echo "## Current HEAD"
git rev-parse --short HEAD

echo
echo "## Recent commits"
git log --oneline -5

echo
echo "## Diff against origin/main"
git diff --stat origin/main...HEAD || true

echo
echo "## Changed paths against origin/main"
git diff --name-status origin/main...HEAD || true

echo
echo "## Staged paths"
git diff --cached --name-status || true

echo
echo "## Unstaged paths"
git diff --name-status || true

echo
echo "## Untracked paths"
git ls-files --others --exclude-standard || true

echo
echo "## Existing PR"
gh pr view --json number,title,url,state,headRefName,baseRefName,reviewDecision,statusCheckRollup 2>/dev/null || true
