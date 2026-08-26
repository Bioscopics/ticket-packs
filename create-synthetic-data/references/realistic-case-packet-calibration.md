# Realistic Case Packet Calibration

## Length Policy

Use observed page and word ranges as soft document-family calibration bands. Do not turn them into hard ceilings unless the jurisdiction, filing rule, product, or user imposes a sourced limit. When a rule limits pages or words, measure the rule-defined material separately from captions, tables, certificates, exhibits, or other exclusions instead of applying a raw whole-PDF count. Prefer a natural, fully supported filing just outside a soft band over content deletion, padding, forced pagination, or compressed typography.

Use this reference when creating synthetic case folders meant to look like real messy document packets, especially legal, healthcare, finance, insurance, real-estate, municipal, procurement, or claims files.

Complete the global `real-example-calibration.md` gate first. This reference adds case-packet-specific calibration rules; it does not replace the required `planning/real_example_profile.json`.

## Core Principle

Generate document families, not isolated files.

A realistic case packet usually contains related artifacts with a shared lifecycle: a primary governing or source record, later amendments or updates, statements or reconciliations, structured exports, emails/messages, scans, attachments, and index-like files. The files should look like they accumulated over time rather than being produced by one template in one sitting.

Do not satisfy "large" or "very large" by padding one generic PDF. Length only counts when the document has realistic internal structure, varied sections, stable visual layout, and a reason to exist in the case.

## Use Unrelated Examples Safely

When inspecting real examples for quality calibration:

- inspect only generalized traits: file mix, naming style, page counts, layout families, extraction behavior, date/version patterns, and artifact relationships;
- do not copy names, addresses, IDs, proprietary terms, clauses, exact language, signatures, or visible private facts;
- record a short `calibration_notes.md` describing abstracted patterns used and private details intentionally excluded;
- compare generated output against the generalized pattern, not against verbatim source content.

## Packet Family Map

Before generating files, write a packet family map with:

- shared fictional case ID and optional legacy IDs;
- stable fictional parties, organizations, locations, matter dates, and lifecycle events;
- artifact families and why each exists;
- cross-document references such as amendment numbers, invoice IDs, exhibit IDs, claim IDs, email attachment names, payment rows, inspection IDs, or Bates-like ranges;
- expected source-vs-holdout boundaries.

For each case, include a mix appropriate to the domain:

- **Primary long record:** contract, policy, claim file, medical record packet, lease, engineering report, litigation production, public-records production, or similar.
- **Short updates:** amendments, notices, letters, denials, addenda, approvals, summaries, signed forms.
- **Structured data:** `.xlsx`, `.xls`, CSV, XML, JSON, EDI/FHIR-like payloads, exports, ledger/payment histories.
- **Messages:** `.eml`, `.msg`, chat transcript, forwarded email thread, portal message, fax cover sheet.
- **Image/scanned artifacts:** image-only PDFs, standalone photos/screenshots, faxed forms, low-contrast scans, stamps, handwritten notes.
- **Messy extras:** duplicate files, stale versions, missing attachment references, unusual filenames, inconsistent dates, partially corrupt or unreadable artifacts.

## Scale Quality Bar

Scale should be visible across both file count and individual-file realism:

- `small`: a few coherent artifacts; at least one file has real layout, not plain text.
- `medium`: several files with at least two formats and one cross-document dependency.
- `large`: a realistic packet with one substantial primary record plus several short updates/exports/messages.
- `very_large`: multiple substantial records or one very long primary record plus many shorter related files, structured exports, and noisy attachments.

When the domain plausibly has long documents, large/very-large cases should include at least one long individual source document. But a long PDF must not be repeated filler. It should contain varied document sections, page numbers, tables/forms where plausible, signatures/footers when plausible, and document-specific internal references.

If a file is named, inventoried, or described as `long`, `production binder`, `record`, `lease`, `chart`, `claim file`, `policy packet`, or another long-form artifact, make it at least 30 pages. If the artifact is shorter, name and inventory it honestly as a brief, letter, memo, excerpt, note, summary, or short packet.

For bounded one-shot packets, a 30-40 page long record is acceptable only if it has visibly different page types. Do not make most pages the same appendix table, numbered extract table, or repeated source-fact grid. Mix at least four relevant page families, such as narrative summaries, scanned/form-like pages, correspondence printouts, estimates, logs, maps/diagrams, signature/certification pages, exhibit dividers, dense prose, and table runs.

## PDF Realism Rules

For legal or record-production style PDFs:

- Prefer document-specific layouts: form-heavy summaries, dense prose pages, amendments/addenda, statements, schedules, tables, email printouts, scanned forms, signature pages, exhibits, and appendices.
- Keep headers and footers constrained so they never overlap body text or each other.
- Avoid generic repeated paragraphs across pages. Repetition is allowed only when it matches the document type, such as form rows, table pages, boilerplate clauses, or scanned copies.
- Avoid a long PDF that is mostly one repeated table or appendix-page template. Tables and appendices are useful, but they should be one page family among several, not the document's dominant visual identity.
- Put synthetic disclosure in README/metadata by default, not stamped on every source page, unless the test intentionally needs watermark handling.
- Use plausible page artifacts: page numbers, scan borders, skew, light noise, stamps, signatures, checkboxes, handwritten annotations, attachment labels, and file IDs.
- For scanned/image-only PDFs, confirm text extraction is empty or weak by design.
- Treat page density as a document-design constraint, not a request to add filler. Reflow natural content, eliminate unnecessary page breaks, combine short adjacent sections, resize oversized tables, or use a shorter document form when the available evidence does not justify another page.
- A continuation page with only a heading and a few paragraphs above a large empty field is a layout defect. Do not create it merely to meet a page target.
- A sparse final page is allowed only for a genuine signature, certification, exhibit divider, or similarly document-native terminal page. Record that exception in the helper receipt and pass `--allow-sparse-final` only for that intentional case.

## Visual And Extraction QA

For every long or layout-sensitive PDF:

- render at least page 1, one middle page, and one late page to PNG;
- visually reject overlap, clipping, unreadable text, giant blank regions unless intentional, uniform filler pages, and synthetic-looking repeated templates;
- run the canonical `scripts/audit_pdf_layout.py` from the installed synthetic-data skill, not a copied or temporary script. For generated clean PDFs, `--strict` must exit zero with no issues; a nonzero result requires a layout repair before delivery.
- do not waive an under-filled continuation page. The only permitted density waiver is an intentional sparse terminal page, documented in the receipt and invoked with `--allow-sparse-final`.
- record preview paths in QA notes;
- record page count and text extraction character count;
- verify clean PDFs have substantial text, scanned PDFs have little/no extractable text, corrupt PDFs fail in the intended way, and extraction-hostile PDFs produce awkward but nonempty text.

Use `scripts/audit_case_packet_realism.py <output_dir> --render` when the output is a case-packet folder. Treat blocking issues from this script as repair-required. Treat warnings as review-required; either repair them or document why the packet intentionally omits that modality.

## Package-Level QA

Reject or repair packets when:

- files do not look related to the same case lifecycle;
- all files were created with one visible template or one timestamp pattern;
- every PDF has the same header/body style;
- long documents are padded with repeated prose;
- a file claims to be long-form but has fewer than 30 pages;
- a long document is dominated by one repeated table/appendix template instead of mixed page families;
- structured files are toy-sized when the scenario requires real operational scale;
- image references exist only as indexes without actual image files when image ingestion is part of the test;
- image/photo evidence is a rough drawing, deterministic sketch, cartoon, or clip-art-style placeholder but is inventoried as realistic photo evidence;
- labels or expected outcomes leak into uploadable inputs.
