# Probe And Handoff Contract

## Contents

- [Probe Receipt](#probe-receipt)
- [Adaptive Handoff Artifact](#adaptive-handoff-artifact)
- [Handoff Validation](#handoff-validation)

## Probe Receipt

Require one receipt per frontier node:

```markdown
# Adaptive Probe Receipt

- Probe ID: <stable id>
- Parent Node: <id or root>
- Original User Question: <question>
- Lane Question: <question>
- Probe Question: <small answerable question or hypothesis>
- Evidence Surface: web | codebase | corpus | database | runtime | mixed
- Action And Tools: <what was performed>
- Budget Consumed: <time, calls, tokens, or other available measure>
- Status: accepted | negative_signal | blocked | malformed

## Bottom Line

<answer to the probe question, not the final user answer>

## Evidence And Provenance

- <stable URL, file/symbol/line, record/query id, trace/test id, or other anchor>

## Evidence Quality

- Authority/applicability: <assessment>
- Freshness/version: <assessment>
- Directness: <primary, secondary, inferred, or experimental>

## Signal

- Relevance: high | medium | low
- Information gain: high | medium | low
- Novelty: high | medium | low
- Contradiction/safety/completeness value: high | medium | low
- Expected value of another nearby probe: high | medium | low

## New Unknowns Or Contradictions

- <new question, conflict, or none>

## Suggested Frontier Action

expand | deepen | competing_probe | fuse | prune | block | handoff_candidate

## Suggested Next Probes

- <narrow probe with reason and expected information gain>
```

Accept a receipt only when its evidence anchors can be inspected by the next phase. Preserve useful negative results because they can prune the frontier.

## Adaptive Handoff Artifact

Write `adaptive_research_handoff.md` with this exact structure:

```markdown
# Adaptive Research Handoff

## Phase Contract

- Adaptive status: HANDOFF_READY | FALLBACK_TO_DEEP_RESEARCHER | BLOCKED
- Deep-researcher required: true
- Adaptive authority ended: true
- Final answer emitted: false
- Persistent memory or drill written: false

## Original User Question

<original question>

## Lane Question

<scoped lane question>

## Strategy And Constraints

- Research strategy: adaptive_then_planned
- Research surface: <surface list>
- Research policy: <profile>
- Allowed tools/access: <contract>
- Budget consumed / limit: <values>

## Stabilized Problem Map

- <branch or dependency and why it matters>

## Accepted Evidence Ledger

| Receipt ID | Finding | Provenance | Evidence quality | Supports | Reuse status |
|---|---|---|---|---|---|
| <id> | <finding> | <anchor> | <assessment> | <branch/claim> | accepted_no_repeat |

## Material Contradictions

- <contradiction, competing evidence, and affected branch>

## Unresolved High-Priority Questions

- <question and why the planned phase must resolve it>

## Pruned And Fused Branches

- <branch> — pruned | fused — <reason and receipt IDs>

## Untrusted Partial Evidence

- <partial receipt and why it was not accepted>

## Recommended Deep-Research Topology

- <candidate parallel questions, real dependencies, and synthesis needs>

## Selective Verification Needs

- <claim requiring a new check and why an accepted receipt is insufficient>

## Stop Reason

<why the frontier stabilized, fell back, or blocked>
```

## Handoff Validation

Mark the handoff invalid unless:

- both questions are present;
- `Deep-researcher required` and `Adaptive authority ended` are true;
- every accepted finding has inspectable provenance;
- unresolved material questions and contradictions are explicit;
- pruned branches include reasons;
- the artifact distinguishes accepted evidence from untrusted partial evidence;
- the artifact contains no final answer and no claim that adaptive discovery replaced deep-researcher.

On invalid handoff, use the original question to start the normal `deep-researcher` path and treat all adaptive evidence as untrusted.
