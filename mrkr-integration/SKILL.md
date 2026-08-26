---
name: mrkr-integration
description: Integrate DistylAI MRKR citations into an existing LLM or agent workflow using a codebase-first audit, the smallest viable diff, verified provider metadata, and host-native clickable citations. Use for hosted or on-prem applications that need traceable document, web, or internal-source claims without redesigning the underlying workflow.
---

# MRKR Integration

Add MRKR as a thin citation overlay around the existing product. Preserve the
workflow, agent, model, business rules, state machine, storage model, and user
journey unless the user separately asks to change them.

The required lifecycle is:

```text
existing evidence -> distylai-mrkr preprocessing -> existing model/agent
                  -> verified finalization -> existing persistence/API
                  -> host-native clickable citations
```

## Non-negotiable contract

- Use the `distylai-mrkr` distribution (`import mrkr`) for marker creation,
  parsing, and scrubbing. Do not clone its algorithms or mint marker IDs.
- A model may copy only exact markers from its current provider context. Marker
  IDs, match hints, source locators, and resolver metadata are provider-owned
  and model-external.
- Verify and sanitize every designated MRKR-bearing output field before it is
  persisted or returned. Never trust citation-looking model text by itself.
- Render only backend-verified citations. Clicking a citation must resolve to
  the source information authorized for that user.
- Keep source acquisition pluggable. Public web search, internal search, RAG,
  uploaded files, and air-gapped document stores may differ; all converge on
  the same citable packet and finalization boundary.
- Do not require Toolkit, Weave, OpenCode, Context Mesh, or a specific frontend
  framework. Reuse them only when the target codebase already does.
- Do not turn a memo workflow into chat, replace a prior-authorization rules
  engine, add a new agent, or otherwise broaden the product to add citations.

## Work sequence

1. Read [references/codebase-audit.md](references/codebase-audit.md). Trace one
   complete evidence-to-model-to-user path before proposing changes.
2. Freeze the integration contract and smallest viable diff. Name the exact
   evidence-bearing fields, provider, prompt boundary, finalizer, persistence
   owner, API shape, and renderer. Preserve all other behavior.
3. Read [references/architecture.md](references/architecture.md) and choose one
   narrow insertion point before the existing model call and one verification
   point after it.
4. Use the public package APIs in
   [references/distylai-mrkr.md](references/distylai-mrkr.md). Feature-detect
   the API actually installed in the target environment; do not assume a
   Toolkit-local wrapper.
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
depend on supplied/retrieved evidence. In mixed outputs, designate only the
evidence-bearing text fields as MRKR-bearing.

Examples:

- Bench memo: cite evidence-backed memo claims and exported narrative; leave
  deterministic document assembly unchanged.
- Chatbot: create a fresh citable context for each turn and preserve normal
  conversation state without reusing stale marker IDs.
- Prior authorization: cite evidence and rationale; do not change policy
  evaluation, eligibility rules, or deterministic decision logic.

## Scope and diff controls

Start with a target of one adapter at the existing context boundary, one
finalizer at the existing response boundary, additive persistence/API fields,
and one renderer adaptation. Reuse existing upload, retrieval, prompt, storage,
authorization, and UI infrastructure.

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
- model-visible text versus model-external metadata;
- finalization, persistence, ACL, and UI behavior;
- exact tests, browser evidence, and residual limitations;
- on-prem dependencies, egress behavior, and secret requirements.
