#!/usr/bin/env bash
set -euo pipefail

remote="${REMOTE:-}"
if [[ -z "$remote" ]]; then
  upstream="$(git rev-parse --abbrev-ref --symbolic-full-name '@{upstream}' 2>/dev/null || true)"
  if [[ "$upstream" == */* ]]; then
    remote="${upstream%%/*}"
  elif git remote get-url origin >/dev/null 2>&1; then
    remote="origin"
  else
    remote="$(git remote | head -n 1)"
  fi
fi

repo="$(gh repo view --json nameWithOwner --jq .nameWithOwner 2>/dev/null || true)"
base="${BASE:-$(gh pr view --json baseRefName --jq .baseRefName 2>/dev/null || true)}"
if [[ -z "$base" ]]; then
  base="$(gh repo view --json defaultBranchRef --jq .defaultBranchRef.name 2>/dev/null || true)"
fi
if [[ -z "$base" && -n "$remote" ]]; then
  remote_head="$(git symbolic-ref --short "refs/remotes/$remote/HEAD" 2>/dev/null || true)"
  base="${remote_head#"$remote/"}"
fi

echo "## Repository"
printf 'repo=%s\nremote=%s\nbase=%s\n' "${repo:-unknown}" "${remote:-unknown}" "${base:-unknown}"

echo
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

if [[ -n "$remote" && -n "$base" ]]; then
  comparison="$remote/$base"

  echo
  echo "## Diff against $comparison"
  git diff --stat "$comparison"...HEAD || true

  echo
  echo "## Changed paths against $comparison"
  git diff --name-status "$comparison"...HEAD || true
else
  echo
  echo "## Base comparison unavailable"
  echo "Set REMOTE and BASE to compare this branch with its intended PR base."
fi

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
