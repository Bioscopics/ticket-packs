# Example: Policy and Procedure Corpus

This is an example pattern, not the default use case.

## User Goal

Create synthetic data for a product that ingests policy/procedure-style documents, creates a knowledge graph or task-specific ontology, identifies contradictions, asks targeted SME questions, and supports downstream applications such as Q&A, conversation review, and regulatory-change impact analysis.

## Useful Artifact Groups

- Source artifacts: global policies, local procedures, desk manuals, process maps, operating routines, FAQs, templates, calculators, exception records.
- Planned imperfections: global/local conflicts, policy/procedure lag, stale quick references, exception records that override internal standards, outdated operating routines, ambiguous local applicability.
- Eval sets: Q&A challenges, email/chat conversations to classify, regulatory-change notices to run through impact analysis.
- Inventories: title, path, jurisdiction, owner, version, status, effective date, authority tier, source role, eval-holdout flag.

## Packaging Shape

```text
output/
  README.md
  inventories/
  knowledge_sources/
    policies_and_procedures/
    operating_artifacts/
  scenario_packs/
  eval_and_test_data/
    conversations/
    qna_challenges/
    regulatory_changes/
```

## QA Lessons

- Formal documents need realistic metadata and varied owners/statuses.
- Do not make every jurisdiction use the same exact topic matrix unless that is a deliberate test condition.
- Use authority tiers so policies, desk manuals, FAQs, and case notes do not collapse into one truth source.
- Keep eval labels and answer keys out of source ingestion.
- Current legal/regulatory details need research or cautious wording.
- Repair passes should preserve useful contradictions while removing accidental hallucinations, unsafe instructions, placeholders, and template fingerprints.
