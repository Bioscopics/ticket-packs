---
name: mrkr-integration
description: Integrate MRKR as a complete marker-native provenance path from selected model context through verified raw-text output, native persistence/API, and host-native clickable citations. Use for hosted or on-prem LLM or agent workflows that need traceable document, web, or internal-source claims, including replacing redundant model-authored quote, page, or citation-JSON paths without redesigning the product.
---

# MRKR Integration

Add MRKR as a thin but complete provenance layer around the existing product.
Preserve the workflow, agent, model, business rules, state machine, storage
model, and user journey unless the user separately asks to change them. Do not
stop at backend markerization or trace storage: carry the verified relationship
through the product's native result, API, renderer, and source-opening behavior.

The required lifecycle is:

```text
existing retrieval/selection -> mrkr-provenance preprocessing
                             -> existing model/agent
                             -> raw text with inline MRKRs
                             -> deterministic finalization and native association
                             -> existing persistence/API
                             -> host-native clickable source highlighting
```

## Non-negotiable contract

- Use the `mrkr-provenance` distribution (`import mrkr`) for marker creation,
  parsing, and scrubbing. Do not clone its algorithms or mint marker IDs.
- Retrieve or select the useful evidence first, then markerize every
  evidence-bearing source item actually supplied to the model. Do not
  indiscriminately markerize an entire corpus merely because it is available.
- Carry MRKRs in ordinary assistant text or Markdown. The surrounding API may
  serialize that text, but never require MRKRs inside tool/function arguments,
  response-schema objects, or business JSON. Keep existing structured domain
  output marker-free.
- A model may copy only exact markers from its current provider context. Marker
  IDs, match hints, source locators, and resolver metadata are provider-owned
  and model-external.
- The provider adapter must assign a short, stable, collision-checked source
  label before markerization. Prefer an existing short document/reference ID;
  otherwise derive the shortest useful name without extensions, full paths,
  UUID noise, or long filenames. Keep complete source identity and page data in
  the private registry, not in the marker label.
- Verify and sanitize every designated MRKR-bearing output field before it is
  persisted or returned. Never trust citation-looking model text by itself.
- When structured native results need citations, deterministically associate
  verified marker-bearing claims with existing result, record, claim, or field
  IDs. Do not use fuzzy reconstruction or a second model call for this join.
- If the existing workflow asks the model to repeat a verbatim quotation, page,
  source identifier, or citation object for provenance, replace that model
  responsibility for new MRKR-enabled runs. Derive any still-required legacy
  compatibility fields from the verified MRKR registry. Historical records may
  retain their old rendering path; do not run two competing provenance systems
  for new results.
- Render only backend-verified citations. Clicking a citation must resolve to
  the source information authorized for that user.
- Keep source acquisition pluggable. Public web search, internal search, RAG,
  uploaded files, and air-gapped document stores may differ; all converge on
  the same citable packet and finalization boundary.
- Do not require a particular application framework, agent framework, storage
  layer, or frontend stack. Reuse the target codebase's existing surfaces.
- Do not turn a memo workflow into chat, replace a prior-authorization rules
  engine, add a new agent, or otherwise broaden the product to add citations.

## Work sequence

1. Read [references/codebase-audit.md](references/codebase-audit.md). Trace one
   complete evidence-to-model-to-user path before proposing changes, including
   any existing model-authored quote/page/citation path and every downstream
   consumer of it.
2. Freeze the integration contract and smallest viable diff. Name the exact
   selected model context, raw marker-bearing response channel, deterministic
   native association, provider label policy, finalizer, persistence owner, API
   shape, renderer, and legacy replacement. Preserve all other behavior.
3. Read [references/architecture.md](references/architecture.md) and choose one
   narrow insertion point before the existing model call and one verification
   point after it.
4. Use the public package APIs in
   [references/mrkr-provenance.md](references/mrkr-provenance.md). Feature-detect
   the API actually installed in the target environment; do not assume an
   application-local wrapper.
   When implementation code is needed, adapt the tested assets described in
   [references/reference-assets.md](references/reference-assets.md) instead of
   rewriting the package lifecycle.
5. Read [references/providers-and-injection.md](references/providers-and-injection.md)
   for the selected evidence providers and agent/prompt shape. Inject the
   package's mandatory requirements once at the existing model boundary.
6. Implement finalization and persistence using
   [references/finalization-and-storage.md](references/finalization-and-storage.md).
7. Add host-native clickable rendering using
   [references/frontend.md](references/frontend.md). Prefer existing design
   system components over a copied citation UI.
8. For customer-hosted, private, or air-gapped deployments, apply
   [references/on-prem-and-security.md](references/on-prem-and-security.md).
   If the host has no approved Python boundary, follow
   [references/non-python-boundary.md](references/non-python-boundary.md) and
   stop before introducing a sidecar or service without explicit approval.
9. Run the behavioral matrix in
   [references/verification.md](references/verification.md), including a real
   browser journey when a frontend exists.

## Activation decisions

Add the citation path to a surface when source evidence materially influences
what the model says or decides, even if the user did not literally ask for
"citations." Do not activate it for deterministic fields or prose that does not
depend on supplied/retrieved evidence. In mixed outputs, keep business JSON and
tool payloads marker-free; designate the ordinary evidence-bearing assistant
text as the MRKR channel and bind it deterministically to native results when
the UI is field- or record-oriented.

Examples:

- Bench memo: cite evidence-backed memo claims and exported narrative; leave
  deterministic document assembly unchanged.
- Chatbot: create a fresh citable context for each turn and preserve normal
  conversation state without reusing stale marker IDs.
- Prior authorization: cite evidence and rationale; do not change policy
  evaluation, eligibility rules, or deterministic decision logic.

## Scope and diff controls

Start with a target of one adapter at the existing selected-context boundary,
one finalizer and deterministic native association at the existing response
boundary, additive persistence/API fields, removal or bypass of redundant
model-authored citation inputs, and one renderer adaptation. Reuse existing
upload, retrieval, prompt, storage, authorization, source viewer, bounding-box,
and UI infrastructure.

Stop and replan before:

- replacing the model or agent framework;
- introducing a second orchestration path;
- migrating storage or auth;
- adding an external service when local package APIs suffice;
- changing unrelated prompts, schemas, or screens;
- accepting a provider whose resolver metadata cannot be retained securely.

## Completion receipt

Report:

- the traced pre-change path and exact insertion points;
- preserved workflow behavior;
- changed files and why each was necessary;
- package API and provider adapters used;
- selected evidence markerized and short-label policy;
- model-visible text versus model-external metadata;
- marker-free structured output and deterministic native association;
- legacy model-authored citation path replaced or proven absent;
- finalization, persistence, ACL, API, clickable UI, and source-highlight behavior;
- exact tests, browser evidence, and residual limitations;
- on-prem dependencies, egress behavior, and secret requirements.
