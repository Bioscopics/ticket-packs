# High-Stakes Planning Reference

Use this reference before authoring a ticket pack for formal, governed, process-heavy, external-facing, challenge-facing, safety-sensitive, or otherwise high-stakes non-coding work.

The goal is not to add domain jargon. The goal is to force the planner to understand the work vehicle, source posture, control-source surface, decomposition, review gates, and packaging contract before dispatch.

## High-Stakes Task Blueprint

Before writing the ticket pack, produce a short blueprint with these fields:

- `Objective`: the exact outcome the user wants.
- `Deliverable Class`: the type of artifact or decision package being produced.
- `Audience / Consumer`: who will rely on the output and what they need from it.
- `Source Packet`: the actual input materials available now.
- `Source Gaps`: missing materials that could change the outcome.
- `Control Surface`: rules, processes, standards, policies, schemas, templates, or acceptance criteria that govern the work.
- `Risk Triggers`: why mistakes would matter.
- `Decision Points`: choices that must be selected before drafting or synthesis.
- `Component Artifacts`: sections, tables, appendices, summaries, worksheets, or companion outputs that may need separate lanes.
- `Review Gates`: checks that must occur before final packaging.
- `Final Package Shape`: exact files or outputs expected at completion.

If any required field is unknown and outcome-determinative, stay in Planner mode and dispatch planning-support research or ask one targeted clarification.

## Risk Triggers

Treat the task as high-stakes when any of these are present:

- a formal audience will rely on the output;
- the result affects money, access, safety, compliance, reputation, or an irreversible decision;
- multiple source packets conflict;
- the deliverable must satisfy an external rule, template, standard, or process;
- the task involves critical review, audit, escalation, challenge, negotiation, or signoff;
- the output must be packaged for handoff, approval, or external-facing use;
- a hidden evaluator, benchmark, or rubric exists and must not contaminate production lanes.

## Planning Control Matrix

Use this matrix to convert the blueprint into lanes:

| Planning Need | Usually Maps To | Notes |
|---|---|---|
| source sufficiency or source normalization | `G` gate | Run first when source posture controls the rest of the work. |
| rule, standard, policy, template, or process discovery | `R*` or `G` | Use `G` only when it blocks all later work. |
| independent source families | parallel `R*` lanes | Split by source family when each lane can produce a draftable packet. |
| conflicting facts or conflicting inputs | `R*` then `A` | Require explicit conflict handling before drafting. |
| issue selection or decision architecture | `A` or Domain Lead | Do not ask drafters to choose the theory or position implicitly. |
| component artifacts | parallel `D*` lanes | Split when artifacts can draft independently from the same selected inputs. |
| quality, completeness, or skeptical check | `V` reviewer | Make findings-first review a hard gate when risk is material. |
| final assembly or handoff package | `F` finisher | Use when package shape matters beyond a single Markdown answer. |

## Governing-Source Controls

For any governing rule, policy, standard, template, or acceptance criterion:

1. identify the controlling source;
2. state whether it is binding, advisory, inferred, or user-provided;
3. attach the exact downstream lane that consumes it;
4. do not allow drafting lanes to invent missing controls;
5. make unresolved conflicts visible to the aggregator or reviewer.

## Pre-Draft Gates

Before any drafting or final synthesis lane starts, verify:

- source sufficiency is resolved or explicitly scoped;
- the control surface is known or marked unavailable;
- major decision points have an owner;
- parallel research outputs have a common output shape;
- the aggregator is required when more than one lane can affect the conclusion;
- drafters consume selected positions, not raw conflicting notes.

## Review / Repair Routing

Reviewer findings must route back to the smallest responsible owner:

- source defect -> source/gate or research lane;
- control-surface defect -> control-source lane;
- unresolved conflict -> aggregator;
- wrong selected position -> aggregator or Domain Lead;
- prose or packaging defect -> drafter or finisher;
- global decomposition failure -> planner repair pack.

Do not create a generic recovery lane when the owning lane can be continued with a scoped follow-up.

## Packaging Checks

Before final completion:

- list every promised artifact;
- confirm each artifact has a producing lane and final status;
- surface missing inputs and assumptions;
- confirm no evaluator-only material leaked into production work;
- confirm the final package matches the original user ask, not just the last lane receipt.
