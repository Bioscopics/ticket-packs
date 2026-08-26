# Native File Input Rules

## Rule

If the product claims support for `PDF`, `DOCX`, `XLSX`, image, audio, video, ZIP, XML, or another file modality, test that modality with a real native file passed through the visible UI file input or dropzone.

Do not substitute extracted text, pasted markdown, JSON fixtures, or renamed `.txt` files unless the product explicitly only supports text input.

## Required Checks

- The UI accepts the native file type.
- The filename/upload state is visible where expected.
- The app output uses facts from the uploaded file.
- File-specific behavior appears: citations/page references, sheet/table parsing, image rendering, audio playback/transcription, PDF artifact output, etc.
- Tester-only labels or expected answers are not uploaded.

## Edge Files

Use real problematic native files for failure paths:

- clean text-layer PDF for the happy path, including realistic PII/financial/legal-style planted facts when relevant;
- scanned/image-only PDF with embedded raster pages, poor contrast, skew, stamps, or compression artifacts;
- partially corrupt PDF where some pages open but one page/object/image is damaged or unreadable;
- extraction-hostile PDF with multi-column layout, footnotes, tables rendered as positioned text, weird whitespace, repeated headers/footers, ligatures, rotated labels, or hyphenated line breaks;
- DOCX with tables/comments/headers/footers/footnotes, embedded images, nested tables, text boxes, page breaks, and malformed relationship variants when testing failures;
- XLSX with multiple sheets, merged cells, formulas, hidden rows/columns, mixed date/currency formats, formula errors, corrupt sheet XML, and missing values;
- XML with namespaces, nested structures, optional missing nodes, and invalid variants;
- CSV with quoting/encoding edge cases;
- image with text, low contrast, or annotations;
- audio with pauses/noise/speaker changes.

When the needed native files do not exist, use the sibling `create-synthetic-data` skill and its `native-document-artifacts.md` reference to generate them. Keep tester-only expected answers separate from uploaded files.

If a native upload cannot be exercised from the UI, report blocked/fail.
