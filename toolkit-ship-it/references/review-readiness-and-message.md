# Review Readiness And Colleague Message

Use this reference after a Toolkit PR exists.

## Review Readiness Gate

A PR is not ready to hand to colleagues until the review loop has been checked.

Check:

```bash
gh pr checks --watch
gh pr view --json reviewDecision,statusCheckRollup,comments,reviews,url,title,number
gh api repos/DistylAI/toolkit/pulls/<PR_NUMBER>/comments --paginate
gh api repos/DistylAI/toolkit/issues/<PR_NUMBER>/comments --paginate
```

If Claude or CodeRabbit is still running, wait unless Ben asks to stop early.

Treat as blockers until assessed:

- security/auth/tenancy issues,
- backend/frontend/engine test failures,
- generated app runtime or publishing regressions,
- Button/BAS/OAA planner, dispatcher, gate, OpenCode runner, or checkpoint behavior changes,
- comments that identify stale code, missing cleanup, or hidden compatibility breaks,
- reviewer says not to merge.

## Bot Comment Handling

For each actionable Claude / CodeRabbit / review comment:

1. Verify against the code and tests. Do not guess.
2. Categorize:
   - `fix`: correct, scoped, improves stability or correctness.
   - `defer`: valid but broader than the PR.
   - `decline`: incorrect, risky, or conflicts with the intended architecture.
3. Fix `fix` comments and push a new commit.
4. Re-run affected validation.
5. Prepare short defer/decline wording for Ben when needed.

Default stance for Button/BAS/OAA: stability beats broad cleanup. Do not accept suggestions that simplify away planner/dispatcher contracts, checkpoint recovery, generated-app runtime hardening, or reviewed frontend run UX without explicit user approval.

## Inline Self-Comment Style

Inline self-comments should help reviewers review faster:

```text
Please check how this handles old runs after the app directory is recreated. It keeps the old behavior so existing run links continue to work.
```

```text
This timeout is intentionally longer than the old default because parent runs can wait on OpenCode subagents that are still making progress. The retry path below is what prevents this from becoming an indefinite hang.
```

Avoid implementation narration:

```text
This function validates the form.
```

## Paste-Ready Colleague Message

Use this shape:

```text
Hey all, could I get an extra set of eyes on <PR link>?

High level:
- <What changed in product/user terms>
- <Why this matters / what failure it fixes>
- <Specific area where a closer look would help>

I’ve handled the bot comments that made sense, left notes where something was intentionally deferred, and the relevant checks are passing.
```

Make it sound like Ben:

- direct,
- practical,
- high level,
- not too formal,
- uses "all" rather than "folks",
- asks for "an extra set of eyes" or "a closer look" instead of sounding like a formal review request,
- no long implementation inventory,
- no CI mechanics unless there is a review caveat.

Use plain language:

- Say what changed, why it matters, and exactly what should be checked.
- Prefer short sentences and common words.
- Keep exact product or code names when useful, but explain uncommon terms.
- Avoid phrases such as “review the boundary,” “contract shape,” “compatibility edge,” “runtime surface,” “monotone,” or “hysteresis.”
- Read the message once as a teammate who has not followed the implementation. Rewrite anything that needs translation.

Examples:

```text
Hey all, could I get an extra set of eyes on https://github.com/DistylAI/toolkit/pull/1234?

High level:
- Restores the Button run progress/log UX that got dropped during the larger merge.
- Keeps the newer OpenCode execution path intact; this is meant to be additive, not a rollback.
- I’d especially like a closer look at whether run details still load for older saved runs.

I’ve handled the bot comments that made sense, left notes where something was intentionally deferred, and the relevant checks are passing.
```

```text
Hey all, could I get an extra set of eyes on https://github.com/DistylAI/toolkit/pull/1234?

High level:
- Adds the generated-system execution API path Button needs for downstream integrations.
- I’d love a closer look at three things: starting work immediately or in the background, retrieving a past result, and the error shown by older generated apps.
- I left inline notes on the older-app cases that are easiest to miss.

Relevant checks are passing and I handled the review comments that looked in-scope.
```
