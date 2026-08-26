# Intake Questions

Use these questions to collect a synthetic-data brief. Ask only what is needed; for small requests, ask a compact subset and state assumptions.

## Minimum Brief

- What domain, process, or real-world artifact family should this simulate?
- Who or what will consume the data?
- What should the data help test, train, demo, or evaluate?
- What artifact types and formats are required?
- How many artifacts or records are needed?
- Should there be held-out eval/test sets with labels or answer keys?
- What imperfections should be intentionally present?

## Product or AI-System Context

Ask these when the user mentions a product, model, agent, RAG system, classifier, workflow engine, analytics product, or benchmark:

- What are the key user journeys or model tasks?
- What inputs will the system receive at inference/query time?
- What outputs should be judged correct?
- What failure modes should the eval set expose?
- Should the dataset include easy, hard, ambiguous, adversarial, and out-of-scope cases?
- Should labels include rationales, citations, expected tool calls, scoring rubrics, or only final answers?
- What data must be withheld from source ingestion to avoid eval leakage?

## Intended Imperfections

Common synthetic artifacts to request or confirm:

- contradictions across records or documents;
- stale records and outdated guidance;
- missing required fields;
- duplicate or near-duplicate entities;
- noisy OCR/text extraction;
- inconsistent formatting;
- ambiguous labels;
- rare edge cases;
- distribution shifts by time, geography, persona, or product line;
- adversarial examples and prompt-injection attempts;
- benign false positives and false negatives;
- chain-of-custody or version-history conflicts.

## Constraints

- Any real entities, brands, jurisdictions, dates, standards, APIs, or schemas that must be represented?
- Any domains requiring current research or primary-source verification?
- Any content that must be fictionalized, anonymized, or avoided?
- Any file naming, directory, schema, or metadata conventions?
- Any target token/size limits?
- Any validation tools that must pass?

## Default Assumptions

When the user does not specify, assume:

- create a small pilot corpus before scaling;
- separate source artifacts from eval labels;
- include metadata and inventory files;
- include a README explaining directory roles;
- include a realism QA pass and a repair loop;
- use parallel workers for large independent batches only when authorized.
