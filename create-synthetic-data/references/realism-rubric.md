# Realism Rubric

Use this rubric for QA and repair of synthetic data in any domain.

## Blocking Issues

Fix before delivery:

- missing or unusable `planning/real_example_profile.json` for a dataset claiming real-world representativeness, unless an explicit user-authorized blocked/proxy exception is documented;
- native/media artifacts generated without `planning/modality_execution_matrix.json`, the selected specialist helper, or an existing helper receipt;
- claimed image/audio/video/document/spreadsheet coverage represented only by captions, transcripts, storyboards, indexes, renamed text files, or metadata sidecars;
- visible placeholders: `TBD`, `TBC`, `xxx`, lorem text, fake IDs that should have been realistic;
- labels, answer keys, expected outputs, or scoring rationales mixed into raw eval inputs;
- SME annotations, later analyst conclusions, or proposed remedies mixed into a pre-SME raw/source-like corpus without an explicit target-workflow justification and evidence-stage record;
- synthetic/eval provenance leaked inside raw source inputs, such as "synthetic case packet", "fictional test data", "upload/eval testing", "QA note for evaluators", "expected outputs", or "held-out labels";
- broken files, invalid JSON/CSV/XLSX/DOCX/HTML, malformed logs, or inventory paths that do not exist;
- schemas that do not match the declared format or consumer expectations;
- held-out source citations with missing files, wrong PDF pages, non-contiguous quoted text, or workbook references lacking deterministic sheet/row/cell anchors;
- long or layout-sensitive documents with visible header overlap, clipped text, blank filler pages, repeated generic prose, forced page breaks, tiny type, or repeated continuation pages whose content occupies only a narrow top/bottom band to inflate page count;
- unsafe or harmful instructions presented as real guidance;
- current factual claims that are stale, impossible, fabricated, or unverified in high-stakes domains;
- all artifacts sharing identical template language, timestamps, IDs, or metadata unless intentionally testing duplicates.
- later-session chat openers that only answer an absent earlier turn, or semantic labels that conflict with the full labeled utterance.

## High-Severity Realism Issues

Usually repair:

- data distributions are too uniform or too perfect;
- generated file families, native formats, lengths, durations, resolutions, row/page/turn counts, structure, register/layout, complexity, metadata, or relationships materially diverge from the measured real-example target profile without a justified explanation; measured ranges are soft unless a sourced external rule makes them hard;
- a generic worker bypassed an available specialist helper and produced a lower-fidelity modality artifact;
- every actor, record, or scenario has the same fields, wording, or sequence;
- timestamps, versions, lifecycle states, and ownership are implausibly synchronized;
- controlled time expressions use one surface construction despite differing contexts, or relative expressions conflict with the recorded timeline;
- artifacts lack the messiness expected in the target system: revisions, exceptions, abbreviations, partial records, attachments, informal notes, or handoffs;
- document packets lack family coherence: filenames, IDs, dates, parties, page counts, formats, and cross-document references do not look like one accumulated case file;
- contradictions are accidental and undocumented rather than intentional and useful;
- stale data lacks a plausible reason to still exist;
- edge cases are present but do not connect to the target product/model task;
- raw test inputs leak labels through filenames, metadata, or text.
- raw source artifacts look like QA/control documents instead of domain artifacts because they explain that they are synthetic, generated for testing, fictional, or evaluation-only.
- source-like artifacts claim or imply a certainty level that exceeds the intended workflow stage, for example treating an expert annotation as an observed source fact.

## Useful Synthetic Imperfections

Keep or create these when they serve the goal:

- contradictions across sources, records, or versions;
- stale guidance or outdated field values;
- missing optional and required fields;
- duplicate or near-duplicate entities;
- inconsistent casing, formats, units, currencies, locales, or timestamp conventions;
- noisy OCR/transcription/chat text;
- ambiguous labels with adjudication notes;
- adversarial inputs;
- rare edge cases and boundary values;
- temporal drift and version-history conflicts;
- false positives and false negatives.

Each planned imperfection should be documented in metadata or a QA report so evaluators can distinguish intentional challenge data from generation defects.

## Domain Plausibility

Check:

- terminology matches the domain and audience;
- workflows have plausible roles, handoffs, tools, states, and timing;
- structured fields have realistic ranges and correlations;
- document types look like their real-world analogues;
- actors have consistent but not identical styles;
- locale, time period, organization size, maturity, and industry constraints are reflected;
- examples are varied enough to test generalization, not just memorization.

## Research Posture

For low-risk fictional domains, light research can be enough. For current or high-stakes domains:

- verify facts against primary or authoritative sources;
- cite or record research notes where useful;
- avoid invented exact citations, standards, product behavior, prices, laws, medical facts, or security guidance;
- use configurable or fictionalized labels when exact current facts are unnecessary;
- mark uncertain details as synthetic assumptions.

## Eval-Set Quality

Eval sets should include:

- clear task definition;
- raw inputs separate from labels;
- where reference material has mixed authority, a documented evidence-stage boundary that keeps expert deltas separate from the raw source stage;
- label schema and allowed values;
- enough examples per class or scenario;
- easy, medium, hard, ambiguous, adversarial, and out-of-scope cases when useful;
- rationales or citations only in answer-key files;
- leakage checks across filenames, metadata, and raw text.

## Final Validation Checklist

- `planning/real_example_profile.json` parses, sources resolve or have documented access notes, and generated artifacts conform to its target ranges;
- `planning/modality_execution_matrix.json` parses, selected helper paths are resolvable, and every required modality has a completed/blocked/downgraded receipt;
- `scripts/audit_calibration_contract.py <output_dir>` passes, or blocked exceptions are explicit and user-authorized;
- `scripts/audit_reference_integrity.py <output_dir> --require` passes whenever labels cite source artifacts;
- `scripts/audit_pdf_layout.py <output_dir> --strict` passes for generated clean/layout-sensitive PDF batches, with any calibrated short page family documented in the helper receipt;
- inventories parse and all paths exist;
- output README explains source vs eval usage;
- placeholder scan is clean or documented;
- eval labels are held out;
- synthetic provenance is documented in README, inventories, and QA reports, not burned into raw upload/source files;
- metadata is sufficient for downstream use;
- planned imperfections are documented;
- for applicable conversation datasets, fresh-session opener, full-utterance semantic-label, and temporal-expression regressions are recorded;
- QA/repair reports list residual caveats;
- manifests are rebuilt after moves or edits.
- shareable archives come from an explicit allowlist, pass privacy/integrity scans, exclude internal prompts/control paths, and have a matching SHA-256 sidecar.
