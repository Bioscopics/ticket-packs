# Dynamic Execution Routing

Optimize each lane for the fastest execution that still clears the realism and correctness floor. Do not classify an entire dataset as simply fast or heavy unless every lane is genuinely similar.

## Quality Invariants

Every route keeps:

- real-example calibration and copy boundaries;
- specialist helper routing and planning-phase matrix validation;
- native file/container checks;
- source-vs-eval separation;
- schema, chronology, internal-consistency, reference, leakage, and realism QA;
- independent review before packaging;
- delivery-phase calibration audit and sanitized packaging.

Speed changes who performs a lane, how much reasoning it receives, and how much can run in parallel. It does not remove gates.

## Route From The Real Example

Complete enough of `real_example_profile.json` to expose actual difficulty before choosing workers. Route each lane or case using:

| Dimension | Low | High |
|---|---|---|
| Source uncertainty | stable schema, clear examples | sparse/conflicting sources, unclear semantics |
| Real-world messiness | clean, independent records | contradictions, revisions, OCR/noise, missing data |
| Cross-artifact coupling | isolated artifact | dates, IDs, calculations, and facts must tie across files |
| Domain consequence | low-risk fictional workflow | legal, medical, financial, regulated, safety-critical |
| Native modality difficulty | plain text/JSON | long PDFs, scans, media, complex spreadsheets, corruption |
| Volume/repetition | one-off reasoning | many locked variations or mechanical rows |
| Validator strength | weak/manual judgment | deterministic schema, tie-out, reference, render, and leakage checks |

Use heavier reasoning when uncertainty, messiness, coupling, modality difficulty, or consequence is high. Use faster workers when variation is bounded, facts are locked, repetition is high, and validators are strong.

## Required Routing Matrix

For substantive multi-lane work, write `planning/execution_routing_matrix.json` after calibration and before dispatch:

```json
{
  "schema_version": 1,
  "routing_goal": "minimize elapsed time subject to the locked quality floor",
  "lanes": [
    {
      "lane_id": "CASE-01",
      "role": "complete-case builder",
      "source_profile_factors": ["clean digital packet", "locked arithmetic"],
      "uncertainty": "low",
      "messiness": "medium",
      "stakes": "medium",
      "coupling": "high",
      "volume": "high",
      "validator_strength": "strong",
      "model_class": "fast",
      "reasoning": "low",
      "parallelism": "parallel",
      "estimated_minutes": 12,
      "escalation_triggers": ["tie-out failure", "unresolved source ambiguity", "two repair attempts"]
    }
  ]
}
```

Use available model names at runtime; the matrix records capability classes, not a permanently hardcoded model ID.

## Model Classes

| Class | Use |
|---|---|
| `fast` | locked drafting, bulk variations, rows/manifests, deterministic transforms, scoped repairs, packaging |
| `balanced` | moderate ambiguity, mixed documents, case integration, ordinary independent review |
| `frontier` | source calibration, difficult architecture, high-stakes labels, conflicting evidence, complex cross-document reasoning, skeptical final review |

Do not use `fast` for a lane with high uncertainty or high stakes unless a frontier/balanced lane has already locked its decisions and deterministic validators cover execution. A builder never serves as its own only reviewer.

## Dynamic Shape

Route per case:

- simple clean cases may use fast workers;
- messy OCR, contradictory, very-large, or high-coupling cases may use balanced/frontier workers in the same batch;
- calibration and final review may be frontier while inventory, packaging, and bounded repairs are fast;
- a small but ambiguous dataset may be heavy; a large repetitive dataset with locked facts may use many fast parallel workers.

Use shallow/wide fanout after shared decisions are locked. Keep serial depth only for decisions that downstream lanes truly need.

## Processing-Time Optimization

1. Run cheap deterministic gates first: file set, signatures, counts, schemas, chronology, arithmetic, references, and leakage.
2. Render a representative pilot artifact before bulk generation to catch style/layout errors early.
3. For long PDFs, use the active `handle_pdfs` helper, render a pilot before fanout, and automate every-page blank/overflow/similarity/body-density checks. Then visually inspect early/middle/late pages, evidence-anchor pages, and every distinct page family. Escalate to all-page visual review after any repeated whitespace/density defect, weak automation, or high-risk layout.
4. Inspect every spreadsheet sheet, but render targeted used ranges rather than empty areas.
5. Parallelize disjoint case folders and modality work; serialize only shared architecture, final review, and packaging.
6. Stop source sampling when the measured profile stabilizes, while still covering known classes, edge cases, and high-risk variants.
7. Reuse the owning worker for a scoped repair; use a fresh reviewer for acceptance.

## Escalation

Automatically move a lane to more reasoning or a stronger model when:

- source meaning remains ambiguous;
- generated facts fail chronology, schema, or financial tie-outs;
- native artifacts need repeated layout repair;
- a fast worker reaches two unsuccessful repair attempts;
- reviewer findings reveal architectural rather than local defects;
- new evidence raises domain risk or contradicts the locked plan.

Record the reroute in the matrix or receipt. Never keep retrying a cheap lane when the failure is reasoning-bound.

## Native Subagents

When native multi-agent tools are available and delegation is authorized, use native spawned subagents first. If the user explicitly asks for a subagent, do not substitute an external CLI process or a new user-owned thread while native `spawn_agent` is available.

Use `worker` for bounded generation, repair, and packaging; use `explorer` for narrow read-only questions; use a fresh reviewer-role agent for independent QA. External CLI sessions are fallbacks only when native spawning is unavailable or the user explicitly requests that provider. Disclose the fallback.
