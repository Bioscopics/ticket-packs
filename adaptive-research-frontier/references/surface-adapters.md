# Surface Adapters

Select only planner-authorized surfaces and tools. Every adapter must emit the common probe receipt; adapter-specific output is not a substitute.

## Web

Use search, direct source opening, citation traversal, and bounded page inspection.

Prefer signals such as source authority, directness, freshness, corroboration, and whether a source exposes a new causal or dependency branch. Do not equate search rank with evidence quality.

## Codebase

Use repository search, symbol and reference navigation, dependency inspection, tests, configuration, history, logs, or runtime traces as allowed.

Anchor evidence to files, symbols, lines, commits, tests, or trace identifiers. Treat runtime reproduction and direct code paths as stronger signals than name similarity. Keep diagnosis separate from implementation; return findings to the coding planner rather than editing code.

## Private Corpus

Use approved keyword, semantic, metadata, relationship, or record retrieval interfaces.

Preserve document or record identifiers, access scope, version, date, authorship, and applicable business context. Never copy a corpus into a new index or persistent memory unless the planner explicitly authorizes that separate operation.

## Database

Use approved schema inspection, bounded queries, aggregates, samples, joins, or anomaly checks.

Record the query or reproducible transformation, dataset/version, filters, time range, and missingness limitations. Do not infer causal claims from correlation or incomplete samples.

## Runtime Or Experiment

Use approved logs, traces, deterministic tests, controlled experiments, or simulations.

Record environment, inputs, version, observation, and reproducibility. Prefer the least disruptive probe. Do not mutate production state, contact people, or launch external experiments without explicit authority.

## Mixed Surfaces

Allow a receipt from one surface to open a narrow probe on another when the evidence creates a real dependency or contradiction. Preserve cross-surface provenance and avoid repeating the same question through every adapter by default.

## Adapter Availability Failure

If a selected adapter is unavailable:

1. mark affected frontier nodes `blocked`;
2. continue only if other authorized surfaces can still produce a valid handoff;
3. otherwise fall back to `deep-researcher` with the original question and list the unavailable surface;
4. never silently substitute an unauthorized corpus, account, tool, or data source.
