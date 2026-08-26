#!/usr/bin/env python3
"""Audit synthetic case packets for document-family realism.

This intentionally does not prove legal/domain correctness. It catches common
synthetic-data failure modes: toy file mixes, padded long PDFs, no real images
despite photo indexes, no structured/message artifacts, weak scanned/corrupt
coverage, and missing rendered previews for long PDFs.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import zipfile
from collections import Counter
from dataclasses import dataclass, asdict
from pathlib import Path


LONG_PDF_MIN_PAGES = 30
SUBSTANTIAL_TEXT_PER_PAGE = 350
SCANNED_TEXT_PER_PAGE_MAX = 25
STRUCTURED_EXTS = {".csv", ".json", ".xml", ".xls", ".xlsx"}
MESSAGE_EXTS = {".eml", ".msg"}
IMAGE_EXTS = {".jpg", ".jpeg", ".png", ".tif", ".tiff", ".heic"}
MEDIA_EXTS = {".wav", ".mp3", ".m4a", ".mp4", ".mov"}
DOC_EXTS = {".pdf", ".docx", ".doc", ".rtf", ".txt"}
TEXT_LIKE_EXTS = {
    ".csv",
    ".eml",
    ".html",
    ".json",
    ".jsonl",
    ".md",
    ".rtf",
    ".txt",
    ".xml",
    ".yaml",
    ".yml",
}
ZIP_TEXT_EXTS = {".docx", ".xlsx"}
RAW_INPUT_PROVENANCE_MARKERS = [
    r"\bsynthetic case packet\b",
    r"\bfictional test data\b",
    r"\bgenerated for upload/eval testing\b",
    r"\bupload/eval testing\b",
    r"\bqa note for evaluators\b",
    r"\bexpected outputs?\b",
    r"\bheld[- ]out labels?\b",
    r"\bsynthetic use notice\b",
    r"\bthis (?:pdf|document|file|record) is wholly synthetic\b",
    r"\bno one should treat .* as real\b",
    r"\bexists only as test data\b",
    r"\bsynthetic records coordinator\b",
    r"\bimagegen cli fallback\b",
    r"\bno real property depicted\b",
    r"\bfictional scene only\b",
    r"\b\\(fictional\\)\b",
]
RAW_INPUT_PROVENANCE_RE = re.compile("|".join(RAW_INPUT_PROVENANCE_MARKERS), re.IGNORECASE)


@dataclass
class PdfInfo:
    path: str
    pages: int | None
    text_chars: int
    text_chars_per_page: float | None
    extraction_class: str
    rendered_previews: list[str]


def run_text(cmd: list[str]) -> tuple[int, str, str]:
    try:
        proc = subprocess.run(cmd, text=True, capture_output=True, timeout=60)
        return proc.returncode, proc.stdout, proc.stderr
    except Exception as exc:  # noqa: BLE001
        return 999, "", str(exc)


def file_type(path: Path) -> str:
    if shutil.which("file") is None:
        return ""
    code, stdout, _ = run_text(["file", "-b", str(path)])
    if code != 0:
        return ""
    return stdout.strip()


def looks_like_valid_image(path: Path) -> bool:
    description = file_type(path).lower()
    return any(token in description for token in ["jpeg image", "png image", "tiff image", "heif", "heic"])


def looks_like_valid_media(path: Path) -> bool:
    description = file_type(path).lower()
    return any(
        token in description
        for token in [
            "audio",
            "mpeg",
            "mp4",
            "quicktime",
            "wave audio",
            "iso media",
            "apple quicktime",
        ]
    )


def pdf_pages(path: Path) -> int | None:
    if shutil.which("pdfinfo") is None:
        return None
    code, stdout, _ = run_text(["pdfinfo", str(path)])
    if code != 0:
        return None
    for line in stdout.splitlines():
        if line.startswith("Pages:"):
            try:
                return int(line.split(":", 1)[1].strip())
            except ValueError:
                return None
    return None


def pdf_text_chars(path: Path) -> int:
    if shutil.which("pdftotext") is None:
        return 0
    code, stdout, _ = run_text(["pdftotext", str(path), "-"])
    if code != 0:
        return 0
    return len(stdout)


def searchable_text(path: Path) -> str:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        if shutil.which("pdftotext") is None:
            return ""
        code, stdout, _ = run_text(["pdftotext", str(path), "-"])
        return stdout if code == 0 else ""
    if suffix in TEXT_LIKE_EXTS or suffix == "":
        try:
            return path.read_text(errors="ignore")
        except Exception:  # noqa: BLE001
            return ""
    if suffix in ZIP_TEXT_EXTS:
        chunks: list[str] = []
        try:
            with zipfile.ZipFile(path) as archive:
                for name in archive.namelist():
                    lower = name.lower()
                    if lower.endswith((".xml", ".txt", ".rels", ".csv")):
                        data = archive.read(name)
                        chunks.append(data.decode("utf-8", errors="ignore"))
        except Exception:  # noqa: BLE001
            return ""
        return "\n".join(chunks)
    return ""


def raw_input_provenance_hits(files: list[Path]) -> list[str]:
    hits: list[str] = []
    for path in files:
        text = searchable_text(path)
        if not text:
            continue
        match = RAW_INPUT_PROVENANCE_RE.search(text)
        if match:
            hits.append(f"{path.name}: {match.group(0)[:80]}")
    return hits


def pdf_page_heading_counts(path: Path) -> Counter[str]:
    if shutil.which("pdftotext") is None:
        return Counter()
    code, stdout, _ = run_text(["pdftotext", "-layout", str(path), "-"])
    if code != 0:
        return Counter()
    headings: list[str] = []
    for page in stdout.split("\f"):
        lines = [line.strip() for line in page.splitlines() if line.strip()]
        if not lines:
            continue
        heading = re.sub(r"\d+", "#", lines[0].lower())
        heading = re.sub(r"\s+", " ", heading).strip()
        if "appendix" in heading or "source extract" in heading:
            headings.append("appendix/source-extract")
        elif "table" in heading or "log" in heading or "schedule" in heading:
            headings.append("table/log/schedule")
        else:
            headings.append(heading[:40])
    return Counter(headings)


def render_pdf_samples(path: Path, pages: int | None, preview_dir: Path) -> list[str]:
    if pages is None or pages <= 0 or shutil.which("pdftoppm") is None:
        return []
    sample_pages = sorted({1, max(1, pages // 2), pages})
    preview_dir.mkdir(parents=True, exist_ok=True)
    rendered: list[str] = []
    for page in sample_pages:
        prefix = preview_dir / f"{path.stem}_p{page}"
        code, _, _ = run_text(["pdftoppm", "-png", "-f", str(page), "-l", str(page), str(path), str(prefix)])
        if code == 0:
            rendered.extend(str(p) for p in sorted(preview_dir.glob(f"{prefix.name}-*.png")))
    return rendered


def classify_pdf(pages: int | None, chars: int) -> tuple[float | None, str]:
    if not pages:
        return None, "unreadable_or_corrupt"
    per_page = chars / pages
    if per_page <= SCANNED_TEXT_PER_PAGE_MAX:
        return per_page, "scanned_or_image_like"
    if per_page >= SUBSTANTIAL_TEXT_PER_PAGE:
        return per_page, "text_layer"
    return per_page, "weak_text_layer"


def find_case_dirs(root: Path) -> list[Path]:
    scenario_root = root / "scenario_packs"
    if scenario_root.exists():
        return sorted(p for p in scenario_root.iterdir() if p.is_dir())
    case_dirs = sorted(p for p in root.iterdir() if p.is_dir() and (p / "inputs").exists())
    if case_dirs:
        return case_dirs
    if any(p.is_file() for p in root.iterdir()):
        return [root]
    return []


def audit_case(case_dir: Path, render: bool, preview_root: Path) -> dict:
    inputs = case_dir / "inputs"
    input_root = inputs if inputs.exists() else case_dir
    files = sorted(p for p in input_root.rglob("*") if p.is_file())
    exts = Counter(p.suffix.lower() or "<no_ext>" for p in files)
    images = [p for p in files if p.suffix.lower() in IMAGE_EXTS]
    media = [p for p in files if p.suffix.lower() in MEDIA_EXTS]
    pdfs: list[PdfInfo] = []
    issues: list[str] = []
    warnings: list[str] = []

    for pdf in [p for p in files if p.suffix.lower() == ".pdf"]:
        pages = pdf_pages(pdf)
        chars = pdf_text_chars(pdf)
        per_page, extraction_class = classify_pdf(pages, chars)
        previews = render_pdf_samples(pdf, pages, preview_root / case_dir.name) if render and pages and pages >= LONG_PDF_MIN_PAGES else []
        pdfs.append(PdfInfo(str(pdf), pages, chars, per_page, extraction_class, previews))
        if "long" in pdf.name.lower() and (pages or 0) < LONG_PDF_MIN_PAGES:
            issues.append(
                f"PDF named as long-form artifact has fewer than {LONG_PDF_MIN_PAGES} pages: "
                f"{pdf.name} ({pages or 'unknown'} pages)"
            )
        if pages and pages >= LONG_PDF_MIN_PAGES:
            heading_counts = pdf_page_heading_counts(pdf)
            dominant_heading, dominant_count = heading_counts.most_common(1)[0] if heading_counts else ("", 0)
            if dominant_heading in {"appendix/source-extract", "table/log/schedule"} and dominant_count / pages > 0.25:
                warnings.append(
                    f"long PDF appears dominated by repeated {dominant_heading} page family: "
                    f"{pdf.name} ({dominant_count}/{pages} pages)"
                )

    scale_class = None
    metadata_path = case_dir / "metadata.json"
    if metadata_path.exists():
        try:
            scale_class = json.loads(metadata_path.read_text()).get("scale_class")
        except Exception:  # noqa: BLE001
            warnings.append("metadata.json did not parse")

    if not files:
        issues.append("case has no uploadable input files")
    provenance_hits = raw_input_provenance_hits(files)
    if provenance_hits:
        issues.append(
            "raw input files leak synthetic/eval provenance; keep this in README/inventories/QA instead: "
            + "; ".join(provenance_hits[:8])
        )
    if not any(p.suffix.lower() in DOC_EXTS for p in files):
        issues.append("case has no document-like input")
    if scale_class in {"large", "very_large"}:
        if not any((info.pages or 0) >= LONG_PDF_MIN_PAGES for info in pdfs):
            issues.append("large/very_large case has no individual PDF with 30+ pages")
        if not any(p.suffix.lower() in STRUCTURED_EXTS for p in files):
            warnings.append("large/very_large case has no structured export")
        if not any(p.suffix.lower() in MESSAGE_EXTS for p in files):
            warnings.append("large/very_large case has no email/message artifact")
    if scale_class == "very_large" and len(files) < 10:
        issues.append("very_large case has fewer than 10 uploadable files")
    if any("photo" in p.name.lower() for p in files) and not any(p.suffix.lower() in IMAGE_EXTS for p in files):
        warnings.append("photo-related filenames exist but no standalone image files are present")
    invalid_images = [str(p) for p in images if not looks_like_valid_image(p)]
    if invalid_images:
        issues.append(f"image-extension files are not valid image containers: {', '.join(invalid_images[:5])}")
    invalid_media = [str(p) for p in media if not looks_like_valid_media(p)]
    if invalid_media:
        issues.append(f"media-extension files are not valid media containers: {', '.join(invalid_media[:5])}")
    if any(word in p.name.lower() for p in files for word in ["call", "voice", "audio", "video", "walkthrough", "recording"]) and not media:
        warnings.append("media-related filenames exist but no standalone audio/video files are present")
    if pdfs and all(info.extraction_class == "text_layer" for info in pdfs):
        warnings.append("all PDFs have text layers; consider scanned/image-only or extraction-hostile variants")
    if pdfs and all((info.pages or 0) < 10 for info in pdfs) and scale_class in {"large", "very_large"}:
        issues.append("all PDFs are short in a large/very_large case")

    return {
        "case": case_dir.name,
        "scale_class": scale_class,
        "input_file_count": len(files),
        "extension_counts": dict(sorted(exts.items())),
        "pdfs": [asdict(info) for info in pdfs],
        "issues": issues,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--render", action="store_true", help="Render early/middle/late pages for long PDFs")
    parser.add_argument("--json-out", type=Path)
    parser.add_argument("--md-out", type=Path)
    args = parser.parse_args()

    root = args.output_dir.resolve()
    preview_root = root / "qa_reports" / "render_previews"
    case_dirs = find_case_dirs(root)
    cases = [audit_case(case, args.render, preview_root) for case in case_dirs]
    package_issues: list[str] = []
    package_warnings: list[str] = []

    qa_text = ""
    qa_root = root / "qa_reports"
    if qa_root.exists():
        for report in sorted(qa_root.rglob("*.md")):
            try:
                qa_text += "\n" + report.read_text(errors="ignore")
            except Exception:  # noqa: BLE001
                continue

    has_image = any(".jpg" in case["extension_counts"] or ".jpeg" in case["extension_counts"] or ".png" in case["extension_counts"] for case in cases)
    downgraded_image_markers = [
        "imagegen caveat",
        "deterministic pil",
        "image_gen was not exposed",
        "imagegen was not exposed",
        "programmatic jpg",
        "programmatic image",
        "photo-like synthetic",
        "not a real photograph",
        "cartoon",
        "clip art",
    ]
    if has_image and any(marker in qa_text.lower() for marker in downgraded_image_markers):
        package_issues.append(
            "realistic image evidence appears downgraded or generated without imagegen/equivalent realistic-image support"
        )

    total_issues = sum(len(case["issues"]) for case in cases) + len(package_issues)
    total_warnings = sum(len(case["warnings"]) for case in cases) + len(package_warnings)
    result = {
        "output_dir": str(root),
        "case_count": len(cases),
        "blocking_issues": total_issues,
        "warnings": total_warnings,
        "package_issues": package_issues,
        "package_warnings": package_warnings,
        "cases": cases,
    }

    json_text = json.dumps(result, indent=2)
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json_text + "\n")

    lines = [
        f"# Case Packet Realism Audit: {root}",
        "",
        f"- Cases: {len(cases)}",
        f"- Blocking issues: {total_issues}",
        f"- Warnings: {total_warnings}",
        "",
    ]
    if package_issues:
        lines.extend(["## Package Issues", ""])
        lines.extend(f"- {issue}" for issue in package_issues)
        lines.append("")
    if package_warnings:
        lines.extend(["## Package Warnings", ""])
        lines.extend(f"- {warning}" for warning in package_warnings)
        lines.append("")
    lines.extend([
        "| Case | Scale | Inputs | Extensions | PDF pages | Issues | Warnings |",
        "|---|---|---:|---|---|---|---|",
    ])
    for case in cases:
        pdf_pages_summary = ", ".join(str(pdf["pages"] or "?") for pdf in case["pdfs"]) or "-"
        lines.append(
            "| {case} | {scale} | {count} | {exts} | {pages} | {issues} | {warnings} |".format(
                case=case["case"],
                scale=case["scale_class"] or "-",
                count=case["input_file_count"],
                exts=", ".join(f"{k}:{v}" for k, v in case["extension_counts"].items()),
                pages=pdf_pages_summary,
                issues="<br>".join(case["issues"]) or "-",
                warnings="<br>".join(case["warnings"]) or "-",
            )
        )
    md_text = "\n".join(lines) + "\n"
    if args.md_out:
        args.md_out.parent.mkdir(parents=True, exist_ok=True)
        args.md_out.write_text(md_text)

    print(md_text)
    return 1 if total_issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
