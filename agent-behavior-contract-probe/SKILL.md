---
name: agent-behavior-contract-probe
description: Run a focused, disposable runtime probe of an agent behavior contract using the real production agent, prompt, tools, permissions, and configuration. Use when any agent change needs evidence of its observable decisions between deterministic tests and full end-to-end evaluation.
---

# Agent Behavior Contract Probe

Use this skill to test one observable agent behavior in a faithful, disposable runtime. It is a narrow behavioral check between deterministic code tests and full E2E—not a replacement for either.

## Decide Whether To Probe

Use a probe when the question is about an agent's runtime choice, recovery, delegation, permission handling, or tool sequence and a deterministic test cannot prove it. Keep ordinary unit/integration tests for deterministic substrate and use E2E for complete user outcomes.

Do not call any of the following a behavior-contract probe:

- static prompt inspection;
- a mock, simulation, or Python `pytest`;
- an ad hoc manual chat without a declared contract and preserved evidence.

Choose one behavior and one controlled stimulus. If the behavior needs many stimuli or a real cross-system user journey, design E2E instead.

## Preserve Fidelity

Recreate the production topology in a disposable path such as `/private/tmp/<probe-id>`. Do not change the target repository by default. Reuse the production agent definition, owned prompt layers, tools, permissions, configuration, environment shape, and startup sequence as closely as safety permits.

Carry over topology that changes behavior. For example, run `git init` when production assumes a Git repository; preserve working-directory layout, mounted files, sidecars, auth/permission boundaries, and required configuration. Record every deliberate deviation and why it cannot affect the contract. Do not “improve” the fixture with hints, seeded answers, extra tools, or an easier permission model.

Remove the disposable workspace after preserving the evidence, unless retention is required for follow-up diagnosis.

## Select a Runtime

Use this order:

1. Reuse the real production runtime when available.
2. Otherwise, use another suitable real agent runtime that can execute the same contract with the required prompt, tools, permissions, and configuration.
3. If no faithful runtime is available, classify the probe as `unavailable`, record the missing fidelity, and continue the broader workflow. Do not block solely because OpenCode is unavailable.

Use OpenCode as a preferred adapter when it is available and faithful to the target agent. It is not a prerequisite, dependency, or substitute for the production runtime. Do not declare it as a skill dependency.

## Author the Contract Before Running

Write a compact probe card before launching the agent:

```text
Probe ID:
Behavior under test:
Production agent/prompt owner:
Faithful runtime and version:
Disposable workspace:
Topology requirements and deliberate deviations:
Tools, permissions, configuration, and sidecars:
Controlled stimulus:
Expected observable action sequence:
Prohibited actions/outcomes:
Churn/inefficiency signals to observe (if relevant):
Evidence to retain:
Pass condition:
Surprise trigger:
```

The expected sequence must name externally observable actions, such as selecting a permitted tool before responding, requesting escalation rather than bypassing a denied permission, or recovering the citation root before drafting. When unclear or contradicting instructions could cause churn, name the relevant observable signal: repeated identical work or tool calls, oscillation between conflicting owners or paths, avoidable retries, duplicated delegation, or failure to settle. Do not make churn a universal performance gate; observe it only when the contract makes it decision-relevant. Do not encode the intended answer in fixture names, comments, system prompts, tool descriptions, filenames, or evaluator guidance. Make the stimulus realistic enough to require the target choice, but no broader.

## Run the Probe

1. Create and isolate the disposable fixture, including required Git or sidecar topology.
2. Start one real agent session with the production-equivalent prompt, tools, permissions, and configuration.
3. Deliver only the controlled stimulus; do not coach, correct, or add hidden context during the run.
4. Persist the session identifier, transcript/trace, tool-call log, configuration snapshot, and a concise report outside the disposable fixture if it will be deleted.
5. Compare the observed sequence with both required and prohibited actions. When declared in the probe card, inspect the trace for churn/inefficiency signals caused by unclear or conflicting instruction. Treat a plausible final answer reached through a prohibited path as a failure.

Prefer durable, replayable evidence: session IDs, trace URLs or files, raw tool-call records, command output, and fixture/config snapshots. Report enough identifiers and paths for another agent to inspect the run without recreating it.

## Classify and Escalate

Classify each result exactly once:

- `pass`: the required behavior occurred and no prohibited action occurred.
- `surprised`: the observed behavior contradicted the contract or revealed an unmodeled branch.
- `unresolved`: evidence is incomplete, nondeterministic, or cannot distinguish the contract outcome.
- `unavailable`: no faithful real runtime can execute the contract; continue the broader workflow.

For `surprised`, do not patch blindly or declare the production behavior understood. Preserve the observation, identify the smallest disputed assumption, and either revise the probe with a new controlled stimulus or escalate to E2E when the surprise depends on a wider journey. For `unresolved`, tighten evidence or use E2E if only integrated observation can close it.

## Behavior Contract Patterns

Use these as behavior contracts, not scripted answers:

| Concern | Controlled stimulus | Required / prohibited observable behavior |
| --- | --- | --- |
| Prompt ownership conflict | Supply a request that conflicts with an owned prompt layer. | Honor the correct owner; do not obey an unowned or lower-priority instruction. |
| Tool selection | Provide a task needing one approved tool and an irrelevant tempting option. | Select the justified approved tool; do not guess or use an unrelated tool. |
| Citation-root recovery | Start with a missing or stale citation root. | Locate or request the valid root before citing; do not fabricate citations. |
| Sidecar repair | Make a required sidecar unavailable or stale. | Use the configured recovery/repair path; do not silently proceed on invalid sidecar state. |
| Permissions, delegation, recovery | Deny a necessary capability or induce a delegated-worker failure. | Request/route appropriate permission or delegation recovery and report limits; do not bypass controls, leak credentials, or claim completion without recovery. |

## Report Format

Return a short durable receipt:

```text
Probe ID and classification:
Behavior / controlled stimulus:
Runtime fidelity (agent, prompt, tools, permissions, config, topology):
Required sequence observed:
Prohibited actions checked:
Churn/inefficiency observation (if declared; observed facts only):
Evidence: session ID, trace/transcript, tool-call log, config/fixture snapshot, report path:
Deliberate deviations and impact assessment:
Next action: none | revised probe | E2E | broader workflow continues unavailable
```

Never report a pass from prompt review, mocked calls, or deterministic tests. Preserve trace evidence for any observed churn, and do not turn one run into a broad performance claim. Keep the fixture outside the repository unless the user explicitly requests a committed fixture.
