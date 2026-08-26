---
name: mrkr-integration-review
description: Perform a findings-first, read-only audit of an MRKR citation integration for package correctness, workflow preservation, provider provenance, finalization, storage, clickable UI, and on-prem safety. Use when reviewing an implementation or deciding whether it is production-ready; do not use as the primary implementation workflow.
---

# MRKR Integration Review

Review the actual evidence-to-model-to-user path, not just files named
"citation." Default to read-only unless the user separately asks for fixes.

## Review order

1. Identify the exact code version and requested citation-bearing surface.
2. Trace source intake/retrieval, packet construction, model injection, raw
   output, finalization, persistence/API, and frontend rendering.
3. Compare the implementation with
   [references/review-checklist.md](references/review-checklist.md).
4. Run or inspect the narrowest behavioral tests that prove the lifecycle. Do
   not infer correctness from prompt text, typechecking, or visible markers.
5. Report findings first, ordered by severity, with tight file/line references.

## Release blockers

Return `NO-GO` for any of these:

- markers are minted outside `distylai-mrkr` or accepted from model output;
- valid IDs/metadata are not scoped to the current invocation;
- designated outputs bypass verification before persistence/API return;
- source URLs/object IDs are trusted from model text;
- citations appear in UI without a verified bundle or current authorization;
- the implementation changes the underlying workflow/decision logic without
  explicit scope;
- on-prem mode has undeclared external egress or runtime package downloads;
- required-citation flows silently succeed without valid citations.

## Minimality review

Require proof that existing evidence adapters, model clients, storage, auth,
API schemas, and UI primitives were reused. Flag copied Toolkit/Weave
orchestration, a new citation agent, storage migration, duplicated marker
parsers/finalizers, and broad prompt rewrites when a narrow adapter suffices.

## Output format

```text
Findings
- [severity] <issue> - <file:line and behavioral impact>

Decision: GO | NO-GO
Workflow preservation: PASS | NO-GO
Package/lifecycle correctness: PASS | NO-GO
Provider and metadata provenance: PASS | NO-GO
Finalization/storage/auth: PASS | NO-GO
Clickable UI: PASS | NO-GO | N/A
On-prem safety: PASS | NO-GO | N/A
Smallest viable diff: PASS | NO-GO
Test evidence: <commands/results or missing proof>
Smallest correction: <only the minimum release-blocking change>
Residual risks: <bounded list>
```

If there are no findings, say so explicitly and identify any unexecuted
provider, model, browser, or on-prem test as residual risk.
