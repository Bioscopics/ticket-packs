# Codebase Audit and Smallest Viable Diff

Do not start by adding a citation component. First trace how evidence actually
reaches the model and how its answer reaches the user.

## Discovery probes

Adapt commands to the repository; use its native search tools and conventions.

```bash
rg -n "(chat|completion|responses|generate|invoke|agent|llm|model)" .
rg -n "(prompt|messages|system_prompt|context|retriev|upload|document|search)" .
rg -n "(result|response|artifact|history|conversation|memo|decision)" .
rg -n "(markdown|rich.?text|modal|drawer|tooltip|citation|source)" .
rg -n "(tenant|workspace|organization|acl|permission|authorize)" .
rg -n "(pyproject.toml|requirements|package.json|lock)" .
```

Inspect schemas, route handlers, services, prompt builders, model clients,
storage records, and the exact frontend component that renders the answer.
Prefer structured call graphs or framework metadata when available.

## Produce an integration map

Document one real path before planning:

| Stage | Existing owner | Input/output | Reuse decision |
| --- | --- | --- | --- |
| Evidence intake | path/symbol | raw file/search/result | retain/adapt |
| Context assembly | path/symbol | evidence -> model messages | insertion point |
| Model invocation | path/symbol | messages -> raw output | unchanged |
| Response parsing | path/symbol | raw -> domain output | finalizer point |
| Persistence | path/symbol | record/artifact | additive metadata |
| API | path/symbol | backend -> client | additive bundle |
| UI renderer | path/symbol | content -> view | citation extension |

Also record:

- selected evidence-bearing output fields;
- follow-up/history behavior;
- source authorization and tenant boundary;
- file-size/type limits and extraction behavior;
- existing error, loading, empty, and retry states;
- whether public egress or external model providers are permitted.

## Scope lock

Write the smallest behavior delta:

```text
Add verified MRKR citations to <specific evidence-backed output> by adapting
<existing context boundary>, finalizing at <existing response boundary>, and
rendering through <existing UI surface>. Preserve <workflow/model/rules/state>.
```

Expected change surface should normally be:

- one backend provider/context adapter;
- one response finalizer or narrow extension of an existing parser;
- additive persistence/API schema fields if needed;
- one existing frontend renderer plus focused tests;
- dependency declarations only in packages that directly import `mrkr`.

## Reuse proof

Before adding a helper, name the existing upload/retrieval adapter, model client,
storage abstraction, auth guard, rich-text component, modal/drawer, and test
harness considered. New infrastructure is justified only when no existing owner
can express the citation lifecycle safely.

## Archetype-specific preservation

- Memo/drafting: preserve draft stages, approval, export, and document format.
- Chat: preserve message transport, streaming, memory, and tool routing.
- Decision/workbench: preserve deterministic rules, statuses, and audit events.
- Batch/extraction: preserve row identity, ordering, partial-failure semantics,
  and artifact contracts.

Citation work must not silently convert one archetype into another.
