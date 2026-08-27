---
name: prd-generation
description: Draft copy-pastable product requirements documents from rough notes, transcripts, examples, local file packets, or product ideas. Use when the user asks for a PRD, use-case definition, product specification, or structured requirements with constraints and evaluations.
---

# PRD Generation

## Purpose

Turn loose product ideas into a copy-pastable Markdown PRD that preserves the intended product, input/output, behavior, constraint, and evaluation shape.

## Output Rule

Default to one copy-pastable Markdown artifact. If the user is likely pasting the PRD into another tool, wrap the whole PRD in a four-backtick Markdown fence:

````text
````markdown
<PRD>
````
````

Use inner fenced blocks normally for JSON and Mermaid. Do not add explanatory prose before or after the PRD unless the user asks for rationale.

## Required PRD Shape

Use this top-level structure unless the user or target system supplies a required template:

```markdown
# Use Case Definition

## Customer Context

### Goal

<1-2 sentences describing the goal of the product or system.>

### Use Case Summary

<No more than two paragraphs describing what the product does and who it is for.>

## Inputs and Outputs

<A table with input/output name, type/direction, and description. Include a sample JSON payload when useful.>

## Product Behaviour

<Describe the end-to-end behavior. Include Mermaid flowcharts and tables only when they clarify the workflow, edge cases, or state model.>

# Constraints

<Bulleted list of non-evaluation constraints such as latency, cost, model/tool restrictions, data handling, UI shape, interaction style, traceability, or runtime requirements.>

# Evaluations

<Evaluation methodology with H2 subsections for each evaluation area and minimum performance targets.>

# References

<Optional. Include supplied files, examples, recordings, or resources used to assemble the PRD. Omit if none are relevant.>
```

## Drafting Workflow

1. Extract the intended product shape before details:
   - target user
   - primary job-to-be-done
   - primary interface or runtime shape
   - core loop or workflow
   - what must not be reduced away

2. Normalize inputs and outputs:
   - separate user-provided files or data from intermediate artifacts and final outputs
   - include representative file categories, formats, and failure modes
   - inspect local example files when paths are provided, but do not mutate them
   - use sample files as input-shape evidence, not as the full product definition

3. Make behavior operational:
   - describe the end-to-end flow
   - include important state transitions
   - call out deterministic checks, agentic reasoning, tool use, retrieval, vision, citations, memory, or interactive controls when they matter
   - list common edge cases in a table when the product has meaningful failure modes

4. Make constraints concrete:
   - include UX shape, modality, data handling, evidence or citation expectations, runtime, cost, latency, model or tool requirements, and non-goals
   - state when accuracy, traceability, or human review matters more than speed

5. Make evaluations testable:
   - create H2 subsections by capability, not generic "quality"
   - include minimum targets or pass/fail standards
   - cover product-fit quality, not just pipeline success

## Product-Shape Guidance

- Preserve the intended app, game, tool, or workflow. Do not reduce an interactive product into a generic dashboard or one-shot form unless the user explicitly asks for that.
- For folder-upload systems, describe the directory structure and file categories clearly.
- For multimodal or scanned documents, say whether vision-based parsing, page-level indexing, OCR fallback, or citation coordinates are expected.
- For agentic systems, describe what the agent observes, remembers, decides, and how it uses feedback.
- For games and simulations, describe the core loop, world state, controls, progression, win or quality conditions, and AI-agent observation/action interface if relevant.
- For evidence-heavy workflows, require source references in the final output and define what a valid citation contains.
- For generated-product validation, include evaluations that catch reduced or generic implementations.

## Style

- Use clear product language, not implementation-ticket language.
- Prefer concise paragraphs plus tables.
- Use Mermaid only when it clarifies a flow or state machine.
- Keep sample JSON realistic but small.
- Avoid placeholders like "etc." when a concrete category is known.
- Avoid asking follow-up questions unless a missing decision would materially change the PRD.
