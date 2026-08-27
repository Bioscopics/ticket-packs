# Review Readiness And Colleague Message

Use this reference after a PR exists.

## Review Readiness Gate

A PR is not ready to hand to colleagues until the review loop has been checked.

Derive `REPO` as `owner/name` with `gh repo view`, then check:

```bash
gh pr checks --repo "$REPO" --watch
gh pr view --repo "$REPO" --json reviewDecision,statusCheckRollup,comments,reviews,url,title,number
gh api "repos/$REPO/pulls/$PR_NUMBER/comments" --paginate
gh api "repos/$REPO/issues/$PR_NUMBER/comments" --paginate
```

If an expected automated reviewer is still running, wait unless Ben asks to stop early.

Treat as blockers until assessed:

- security, authentication, authorization, or tenancy issues,
- required test or build failures,
- application runtime, persistence, publishing, or deployment regressions,
- changes to important planner, dispatcher, recovery, state, or user-flow behavior,
- comments that identify stale code, missing cleanup, or hidden compatibility breaks,
- a reviewer saying not to merge.

## Review Comment Handling

For each actionable automated or human review comment:

1. Verify it against the code and tests. Do not guess.
2. Categorize it:
   - `fix`: correct, scoped, and improves stability or correctness;
   - `defer`: valid but broader than the PR;
   - `decline`: incorrect, risky, or conflicting with the intended architecture.
3. Fix `fix` comments and push a new commit.
4. Rerun affected validation.
5. Prepare short defer or decline wording for Ben when needed.

Default stance: preserve intentional, working behavior. Do not accept suggestions that simplify away important contracts, recovery behavior, runtime hardening, or reviewed user flows without explicit user approval.

## Inline Self-Comment Style

Inline self-comments should help reviewers review faster:

```text
Please check how this handles older saved records after the app directory is recreated. It preserves the prior behavior so existing links continue to work.
```

```text
This timeout is intentionally longer than the old default because parent work can wait on subagents that are still making progress. The retry path below prevents that from becoming an indefinite hang.
```

Avoid implementation narration:

```text
This function validates the form.
```

## Paste-Ready Colleague Message

Default to one direct sentence:

```text
<PR link> <what it does>, so <problem it fixes>.
```

If the user asks for more context, use:

```text
Hey all, could I get an extra set of eyes on <PR link>?

High level:
- <What changed in product or user terms>
- <Why this matters or what failure it fixes>
- <Specific area where a closer look would help>

I’ve handled the review comments that made sense, left notes where something was intentionally deferred, and the relevant checks are passing.
```

Make it sound like Ben:

- direct,
- practical,
- high level,
- not too formal,
- uses “all” rather than “folks”,
- asks for “an extra set of eyes” or “a closer look” instead of sounding like a formal review request,
- no long implementation inventory,
- no CI mechanics unless there is a review caveat.

Use plain language:

- Say what changed, why it matters, and exactly what should be checked.
- Prefer short sentences and common words.
- Keep exact product or code names when useful, but explain uncommon terms.
- Avoid phrases such as “review the boundary,” “contract shape,” “compatibility edge,” or “runtime surface.”
- Read the message once as a teammate who has not followed the implementation. Rewrite anything that needs translation.

Example:

```text
Hey all, could I get an extra set of eyes on https://github.com/example/project/pull/1234?

High level:
- Restores run progress and logs that were lost during a larger merge.
- Keeps the newer execution path intact; this is additive, not a rollback.
- I’d especially like a closer look at whether details still load for older saved runs.

I’ve handled the review comments that made sense, left notes where something was intentionally deferred, and the relevant checks are passing.
```
