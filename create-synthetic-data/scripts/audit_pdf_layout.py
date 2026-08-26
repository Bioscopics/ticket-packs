#!/usr/bin/env python3
"""Detect blank and under-filled pages in generated PDFs."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import tempfile
from pathlib import Path


def find_pdfs(target: Path) -> list[Path]:
    if target.is_file():
        return [target] if target.suffix.lower() == ".pdf" else []
    return sorted(path for path in target.rglob("*.pdf") if path.is_file())


def pgm_payload(path: Path) -> tuple[int, int, bytes]:
    raw = path.read_bytes()
    index = 0

    def token() -> bytes:
        nonlocal index
        while index < len(raw):
            if raw[index] in b" \t\r\n":
                index += 1
                continue
            if raw[index] == ord("#"):
                while index < len(raw) and raw[index] not in b"\r\n":
                    index += 1
                continue
            break
        start = index
        while index < len(raw) and raw[index] not in b" \t\r\n#":
            index += 1
        return raw[start:index]

    if token() != b"P5":
        raise ValueError(f"unsupported PGM format: {path}")
    width = int(token())
    height = int(token())
    maximum = int(token())
    if maximum != 255:
        raise ValueError(f"unsupported PGM maximum {maximum}: {path}")
    while index < len(raw) and raw[index] in b" \t\r\n":
        index += 1
    payload = raw[index : index + width * height]
    if len(payload) != width * height:
        raise ValueError(f"truncated PGM payload: {path}")
    return width, height, payload


def page_density(path: Path) -> dict:
    width, height, pixels = pgm_payload(path)
    body_top = int(height * 0.10)
    body_bottom = int(height * 0.90)
    body_height = max(1, body_bottom - body_top)
    active_threshold = max(2, int(width * 0.004))
    active_rows: list[int] = []
    dark_pixels = 0
    for row_index in range(body_top, body_bottom):
        row = pixels[row_index * width : (row_index + 1) * width]
        dark = sum(value < 245 for value in row)
        dark_pixels += dark
        if dark >= active_threshold:
            active_rows.append(row_index)
    if not active_rows:
        return {
            "occupancy": 0.0,
            "top_gap": 1.0,
            "bottom_gap": 1.0,
            "ink_ratio": 0.0,
            "blank": True,
        }
    first = active_rows[0]
    last = active_rows[-1]
    return {
        "occupancy": round((last - first + 1) / body_height, 4),
        "top_gap": round((first - body_top) / body_height, 4),
        "bottom_gap": round((body_bottom - last - 1) / body_height, 4),
        "ink_ratio": round(dark_pixels / (body_height * width), 6),
        "blank": False,
    }


def is_underfilled(metric: dict, *, page_number: int, page_count: int) -> bool:
    """Flag pages whose body text stops implausibly early for their page role."""
    if metric["blank"]:
        return True

    # A real caption page can be less dense than a continuation page, but it
    # should still use most of the available body space after the caption.
    if page_number == 1:
        return metric["occupancy"] < 0.48 and metric["bottom_gap"] > 0.42

    # Continuations should not look like a few paragraphs stranded above an
    # otherwise empty sheet. A terminal signature or exhibit page may be
    # sparse, but strict callers must explicitly allow that exception.
    if page_number == page_count:
        return metric["occupancy"] < 0.42 and metric["bottom_gap"] > 0.50

    return metric["occupancy"] < 0.68 and (
        metric["bottom_gap"] > 0.28 or metric["top_gap"] > 0.32
    )


def audit_pdf(pdf: Path, strict: bool, allow_sparse_final: bool) -> dict:
    if shutil.which("pdftoppm") is None:
        return {"path": str(pdf), "pages": 0, "issues": ["pdftoppm is unavailable"], "warnings": [], "page_metrics": []}
    with tempfile.TemporaryDirectory(prefix="pdf-layout-audit-") as temp_dir:
        prefix = Path(temp_dir) / "page"
        process = subprocess.run(
            ["pdftoppm", "-gray", "-r", "30", str(pdf), str(prefix)],
            text=True,
            capture_output=True,
            timeout=180,
        )
        if process.returncode != 0:
            detail = process.stderr.strip() or "render failed"
            return {"path": str(pdf), "pages": 0, "issues": [detail], "warnings": [], "page_metrics": []}
        rendered = sorted(
            Path(temp_dir).glob("page-*.pgm"),
            key=lambda item: int(item.stem.rsplit("-", 1)[1]),
        )
        metrics = []
        underfilled_pages: list[int] = []
        blank_pages: list[int] = []
        border_span_risk_pages: list[int] = []
        for page_number, rendered_page in enumerate(rendered, 1):
            metric = page_density(rendered_page)
            metric["page"] = page_number
            metric["border_span_risk"] = (
                metric["occupancy"] >= 0.97 and metric["ink_ratio"] < 0.24
            )
            metrics.append(metric)
            if metric["blank"]:
                blank_pages.append(page_number)
            if metric["border_span_risk"]:
                border_span_risk_pages.append(page_number)
            if is_underfilled(metric, page_number=page_number, page_count=len(rendered)):
                if page_number != len(rendered) or not allow_sparse_final:
                    underfilled_pages.append(page_number)

    issues: list[str] = []
    warnings: list[str] = []
    if blank_pages:
        issues.append(f"blank pages: {blank_pages}")
    if underfilled_pages:
        detail = (
            f"under-filled pages: {underfilled_pages} "
            f"({len(underfilled_pages)}/{max(1, len(metrics))} pages)"
        )
        if strict:
            issues.append(detail)
        else:
            warnings.append(detail)
    if border_span_risk_pages:
        warnings.append(
            "border-span density may mask sparse content on pages: "
            f"{border_span_risk_pages}; run border-independent body-text/OCR-box "
            "density checks and visual review"
        )
    return {
        "path": str(pdf),
        "pages": len(metrics),
        "issues": issues,
        "warnings": warnings,
        "page_metrics": metrics,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("path", type=Path)
    parser.add_argument("--strict", action="store_true")
    parser.add_argument(
        "--allow-sparse-final",
        action="store_true",
        help="Allow a documented sparse final signature or exhibit page.",
    )
    parser.add_argument("--json-out", type=Path)
    args = parser.parse_args()

    target = args.path.resolve()
    results = [audit_pdf(pdf, args.strict, args.allow_sparse_final) for pdf in find_pdfs(target)]
    issue_count = sum(len(result["issues"]) for result in results)
    warning_count = sum(len(result["warnings"]) for result in results)
    report = {
        "path": str(target),
        "pdfs": len(results),
        "blocking_issues": issue_count,
        "warnings": warning_count,
        "results": results,
    }
    if args.json_out:
        args.json_out.parent.mkdir(parents=True, exist_ok=True)
        args.json_out.write_text(json.dumps(report, indent=2) + "\n")

    print(f"# PDF Layout Audit: {target}")
    print(f"- PDFs: {len(results)}")
    print(f"- Blocking issues: {issue_count}")
    print(f"- Warnings: {warning_count}")
    for result in results:
        for issue in result["issues"]:
            print(f"- BLOCK {result['path']}: {issue}")
        for warning in result["warnings"]:
            print(f"- WARN {result['path']}: {warning}")
    return 1 if issue_count else 0


if __name__ == "__main__":
    raise SystemExit(main())
