---
name: button-prd
description: Draft copy-pastable Button Build a System PRDs from rough use-case notes, transcripts, examples, local file packets, or product ideas. Use when the user asks for a "button-prd", BAS request, filled PRD template, Build a System prompt, or wants a raw Markdown PRD with Use Case Definition, Constraints, Evaluations, and optional References.
---

# Button PRD

## Purpose

Turn loose Button Build a System ideas into a copy-pastable Markdown PRD that gives the BAS planner enough product, input/output, behavior, constraint, and evaluation detail to preserve the intended system shape.

## Output Rule

Default to one copy-pastable Markdown artifact. If the user is likely pasting into Button, wrap the whole PRD in a four-backtick Markdown fence:

````text
````markdown
<PRD>
````
````

Use inner fenced blocks normally for JSON and Mermaid. Do not add explanatory prose before or after the PRD unless the user asks for rationale.

## Required PRD Shape

Use this exact top-level structure:

```markdown
# Use Case Definition

## Customer Context

### Goal

<1-2 sentences describing the goal of the system.>

### Use Case Summary

<No more than two paragraphs describing what the system does and who it is for.>

## Inputs and Outputs

<A table with input/output name, type/direction, and description. Include a sample JSON payload.>

## System Behaviour

<Describe how the system behaves. Include Mermaid flowcharts and tables only when they clarify the workflow, edge cases, or state model.>

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
   - primary UI or runtime shape
   - core loop or workflow
   - what must not be reduced away

2. Normalize inputs and outputs:
   - separate user-provided files/data from intermediate artifacts and final outputs
   - include representative file categories, formats, and failure modes
   - inspect local example files when paths are provided, but do not mutate them
   - use sample files as input-shape evidence, not as the full product definition

3. Make behavior operational:
   - describe the end-to-end flow
   - include the important state transitions
   - call out deterministic checks, agentic reasoning, tool use, retrieval, vision, citations, memory, or interactive controls when they matter
   - list common edge cases in a table when the system has meaningful failure modes

4. Make constraints concrete:
   - include UX shape, modality, data handling, evidence/citation expectations, runtime, cost, latency, model/tool requirements, and non-goals
   - state when accuracy, traceability, or human review matters more than speed

5. Make evaluations testable:
   - create H2 subsections by capability, not generic "quality"
   - include minimum targets or pass/fail standards
   - cover product-fit quality, not just pipeline success

## Button-Specific Guidance

- Preserve the intended app, game, tool, or workflow. Do not reduce an interactive app into a generic dashboard or one-shot form unless the user explicitly asks for that.
- For folder-upload systems, describe the directory structure and file categories clearly.
- For multimodal or scanned documents, say whether vision-based parsing, page-level indexing, OCR fallback, or citation coordinates are expected.
- For agentic systems, describe what the agent observes, remembers, decides, and how it uses feedback.
- For games and simulations, describe the core loop, world state, controls, progression, win/quality conditions, and AI-agent observation/action interface if relevant.
- For evidence-heavy workflows, require source references in the final output and define what a valid citation contains.
- For generated-app validation, include evaluations that catch reduced or generic implementations.

## Style

- Use clear product language, not implementation-ticket language.
- Prefer concise paragraphs plus tables.
- Use Mermaid only when it clarifies a flow or state machine.
- Keep sample JSON realistic but small.
- Avoid placeholders like "etc." when a concrete category is known.
- Avoid asking follow-up questions unless a missing decision would materially change the PRD.
