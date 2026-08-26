# Native Document Artifacts

Use this reference when generating synthetic files that must exercise real document ingestion, extraction, OCR, layout parsing, or file-upload behavior. Produce real native files, not text stand-ins with misleading extensions.

Treat the exact container as part of the calibration contract. Before substituting `.xlsx` for `.xls`, `.eml` for `.msg`, or another nearby format, check the specialist writer and sanctioned conversion paths. If the exact container remains unavailable, record a matrix downgrade with reason, consumer impact, and approval; never rename a different container to the requested extension.

## Required Variant Classes

For apps that claim document support, generate a mix of these classes when relevant:

| Class | Purpose | Examples |
|---|---|---|
| Clean digital | Prove the happy path works with easy extraction. | Text-layer PDF, well-structured DOCX, simple XLSX, valid XML. |
| Scanned/image-only | Force OCR or image handling; text extraction should be empty or weak. | PDF pages that are embedded raster images, fax-like scan, skew/noise/low DPI. |
| Partially corrupt or malformed | Exercise graceful failure and partial recovery. | PDF with one damaged page/object, truncated xref, corrupted embedded image, DOCX with one broken relationship, XLSX with corrupt sheet XML. |
| Extraction-hostile formatting | Expose weird artifacts from naive extraction. | Multi-column PDF, footnotes, hyphenated line breaks, tables rendered as positioned text, rotated text, overlapping headers/footers, ligatures, hidden text. |
| Semantically messy | Test reasoning over realistic imperfections after extraction succeeds. | Contradictory clauses, stale terms, missing page, duplicate invoice line, wrong date format, inconsistent IDs. |

When a case references photos, scans, screenshots, voice clips, or videos, include the actual native media files when those modalities matter. A photo index, transcript, or media manifest is not enough by itself. See `modality-helper-skills.md` for routing to image/audio/video helpers.

## PDF Requirements

Generate PDFs across at least these shapes when PDF support matters:

- **Clean text-layer PDF:** selectable text, normal reading order, stable page numbers, realistic length.
- **PII/financial/legal style clean PDF:** easy to transcribe but contains planted facts that downstream output must preserve.
- **Scanned embedded-image PDF:** pages are images, not selectable text; include noise, skew, compression artifacts, stamps, handwriting-like notes, or poor contrast.
- **Partial corruption PDF:** enough pages open to test partial extraction, but at least one page/object/image is damaged or unreadable.
- **Extraction-hostile PDF:** multi-column layout, table grid, wrapped cells, repeated headers/footers, footnotes, rotated labels, ligatures, odd whitespace, and line-break artifacts.

Long PDFs must earn their length. Do not create a long PDF by repeating generic paragraphs, mechanically numbered sections, tiny type, forced page breaks, or by placing normal content in only the top or bottom fraction of each page. Use document-specific structures such as summaries, schedules, clauses, forms, appendices, exhibit logs, signatures, statements, email printouts, scanned pages, or table runs.

Render a pilot before bulk generation. For the finished batch, run low-resolution every-page density checks, then visually inspect early/middle/late pages, evidence-anchor pages, and every distinct page family. A naturally short signature or closing page is acceptable. Repeated continuation pages with a large unexplained top or bottom void are a layout defect even when extraction, word count, and page-count ranges pass.

Document expected behavior separately from the uploaded/source file. Example: keep `eval_sets/labels_or_answer_keys/pdf_case_03_expected.json` separate from `source_artifacts/pdf_case_03.pdf`.

## DOCX Requirements

Use real `.docx` containers with structure that matters:

- headings, sections, tables, comments, footnotes/endnotes, headers/footers;
- tracked-change-like content if the product claims review/redline support;
- embedded images or screenshots when OCR/image handling should be tested;
- weird formatting: nested tables, page breaks, text boxes, lists with custom numbering, mixed fonts/styles;
- malformed path when needed: broken image relationship, missing media file, corrupt document XML, or unreadable package member.

## XLSX Requirements

Use real `.xlsx` workbooks when spreadsheet support matters:

- multiple sheets with meaningful names;
- formulas, merged cells, hidden rows/columns, filters, frozen panes;
- inconsistent date/currency formats and blank/missing fields;
- realistic row counts for the app's promise, not toy 3-row sheets;
- corrupt/error variant: broken sheet XML, formula errors, missing referenced sheet, or invalid shared string entry.

## XML/CSV Requirements

- XML should include namespaces, nested elements, attributes, comments, optional missing nodes, and invalid variants when testing parser errors.
- CSV should include quoted commas/newlines, BOM/encoding edge cases, duplicate headers, empty rows, and inconsistent delimiters when relevant.

## Metadata

For each native artifact, include metadata outside the source file:

- native file path and MIME type;
- variant class (`clean_digital`, `scanned_image`, `partial_corrupt`, `extraction_hostile`, `semantic_messy`);
- planted facts to verify;
- intended extraction difficulty;
- expected app behavior;
- rendered-preview paths for long or layout-sensitive PDFs;
- labels/answers location, never embedded in raw/source artifacts.

## QA

Before delivery:

- verify the file opens or fails in the intended way;
- confirm file extension and MIME/container are real;
- run a basic extraction attempt and record expected artifacts such as empty OCR text, bad line breaks, or table flattening;
- confirm labels/answers do not leak through filenames, metadata, comments, hidden sheets, alt text, or document properties unless intentionally testing leakage.
