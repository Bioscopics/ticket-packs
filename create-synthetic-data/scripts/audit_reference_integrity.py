#!/usr/bin/env python3
"""Validate held-out claim references without changing host prediction schemas."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import subprocess
import zipfile
from pathlib import Path
from xml.etree import ElementTree as ET


CELL_RE = re.compile(r"^([A-Z]+)([1-9][0-9]*)$")


def json_pointer(value, pointer: str):
    if pointer in {"", "/"}:
        return value
    current = value
    for raw in pointer.lstrip("/").split("/"):
        token = raw.replace("~1", "/").replace("~0", "~")
        current = current[int(token)] if isinstance(current, list) else current[token]
    return current


def find_source(inputs: Path, source_file: str) -> Path | None:
    candidate = Path(source_file)
    if candidate.is_absolute() or ".." in candidate.parts:
        return None
    direct = inputs / candidate
    if direct.is_file():
        return direct
    matches = [path for path in inputs.rglob(candidate.name) if path.is_file()]
    return matches[0] if len(matches) == 1 else None


def normalize_whitespace(text: str) -> str:
    return " ".join(text.split())


def text_matches(haystack: str, expected: str, mode: str) -> bool:
    if mode == "contiguous":
        return expected in haystack
    if mode == "normalized_whitespace":
        return normalize_whitespace(expected) in normalize_whitespace(haystack)
    return False


def pdf_page_text(path: Path, page: int) -> tuple[str, str | None]:
    executable = shutil.which("pdftotext")
    if not executable:
        return "", "pdftotext is unavailable"
    proc = subprocess.run(
        [executable, "-f", str(page), "-l", str(page), str(path), "-"],
        text=True,
        capture_output=True,
        timeout=60,
    )
    return (proc.stdout, None) if proc.returncode == 0 else ("", proc.stderr.strip() or "PDF extraction failed")


def column_number(label: str) -> int:
    value = 0
    for char in label:
        value = value * 26 + ord(char) - 64
    return value


def parse_cell(cell: str) -> tuple[int, int]:
    match = CELL_RE.match(cell.upper())
    if not match:
        raise ValueError(f"invalid A1 cell: {cell}")
    return int(match.group(2)), column_number(match.group(1))


def cells_in_range(cell_range: str) -> tuple[int, int, int, int]:
    parts = cell_range.split(":")
    start = parse_cell(parts[0])
    end = parse_cell(parts[-1])
    return min(start[0], end[0]), max(start[0], end[0]), min(start[1], end[1]), max(start[1], end[1])


def xlsx_sheet_values(path: Path, sheet_name: str) -> dict[str, str]:
    ns = {"m": "http://schemas.openxmlformats.org/spreadsheetml/2006/main"}
    rel_ns = {"r": "http://schemas.openxmlformats.org/package/2006/relationships"}
    office_rel = "{http://schemas.openxmlformats.org/officeDocument/2006/relationships}id"
    with zipfile.ZipFile(path) as archive:
        shared: list[str] = []
        if "xl/sharedStrings.xml" in archive.namelist():
            root = ET.fromstring(archive.read("xl/sharedStrings.xml"))
            for item in root.findall("m:si", ns):
                shared.append("".join(node.text or "" for node in item.findall(".//m:t", ns)))
        workbook = ET.fromstring(archive.read("xl/workbook.xml"))
        rels = ET.fromstring(archive.read("xl/_rels/workbook.xml.rels"))
        targets = {rel.attrib["Id"]: rel.attrib["Target"] for rel in rels.findall("r:Relationship", rel_ns)}
        target = None
        for sheet in workbook.findall(".//m:sheet", ns):
            if sheet.attrib.get("name") == sheet_name:
                target = targets.get(sheet.attrib.get(office_rel, ""))
                break
        if not target:
            raise ValueError(f"sheet not found: {sheet_name}")
        member = target.lstrip("/")
        if not member.startswith("xl/"):
            member = "xl/" + member
        sheet_root = ET.fromstring(archive.read(member))
        values: dict[str, str] = {}
        for cell in sheet_root.findall(".//m:c", ns):
            ref = cell.attrib.get("r", "")
            cell_type = cell.attrib.get("t")
            if cell_type == "inlineStr":
                value = "".join(node.text or "" for node in cell.findall(".//m:t", ns))
            else:
                node = cell.find("m:v", ns)
                value = node.text if node is not None and node.text is not None else ""
                if cell_type == "s" and value:
                    value = shared[int(value)]
            values[ref.upper()] = value
        return values


def xlsx_anchor_text(path: Path, anchor: dict) -> str:
    sheet = anchor.get("sheet")
    if not sheet:
        raise ValueError("xlsx anchor requires sheet")
    values = xlsx_sheet_values(path, sheet)
    selected: list[tuple[int, int, str]] = []
    if anchor.get("cell"):
        cells = [anchor["cell"]]
    else:
        cells = list(anchor.get("cells") or [])
    for cell in cells:
        row, col = parse_cell(cell)
        selected.append((row, col, values.get(cell.upper(), "")))
    if anchor.get("cell_range"):
        row_min, row_max, col_min, col_max = cells_in_range(anchor["cell_range"])
        for ref, value in values.items():
            row, col = parse_cell(ref)
            if row_min <= row <= row_max and col_min <= col <= col_max:
                selected.append((row, col, value))
    rows = anchor.get("rows") or ([] if anchor.get("row") is None else [anchor["row"]])
    if rows:
        wanted = {int(row) for row in rows}
        for ref, value in values.items():
            row, col = parse_cell(ref)
            if row in wanted:
                selected.append((row, col, value))
    if not selected:
        raise ValueError("xlsx anchor requires cell, cells, cell_range, row, or rows")
    deduped = sorted(set(selected))
    return " | ".join(value for _, _, value in deduped if value != "")


def csv_anchor_text(path: Path, anchor: dict) -> str:
    rows = anchor.get("rows") or ([] if anchor.get("row") is None else [anchor["row"]])
    if not rows:
        raise ValueError("csv anchor requires row or rows")
    with path.open(newline="", encoding="utf-8-sig", errors="ignore") as handle:
        data = list(csv.reader(handle))
    selected = [data[int(row) - 1] for row in rows if 1 <= int(row) <= len(data)]
    if len(selected) != len(rows):
        raise ValueError("csv anchor row is out of range")
    return "\n".join(" | ".join(row) for row in selected)


def source_text(path: Path, anchor: dict) -> tuple[str, str | None]:
    kind = anchor.get("kind") or path.suffix.lower().lstrip(".") or "file"
    try:
        if kind == "pdf":
            page = anchor.get("page")
            if not isinstance(page, int) or page < 1:
                return "", "pdf anchor requires a positive page"
            return pdf_page_text(path, page)
        if kind in {"xlsx", "spreadsheet"}:
            return xlsx_anchor_text(path, anchor), None
        if kind == "csv":
            return csv_anchor_text(path, anchor), None
        if kind in {"text", "email", "json", "file"}:
            return path.read_text(encoding="utf-8", errors="ignore"), None
        return "", f"unsupported anchor kind: {kind}"
    except Exception as exc:  # noqa: BLE001 - report malformed source/anchor
        return "", str(exc)


def audit_case(case_dir: Path, require: bool) -> tuple[int, list[str]]:
    expected_dir = case_dir / "expected"
    manifest_path = expected_dir / "reference_manifest.json"
    if not manifest_path.exists():
        if require and expected_dir.exists() and any(expected_dir.iterdir()):
            return 0, [f"{case_dir.name}: missing expected/reference_manifest.json"]
        return 0, []
    issues: list[str] = []
    try:
        manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001
        return 0, [f"{case_dir.name}: invalid reference manifest: {exc}"]
    if manifest.get("schema_version") != 1 or not isinstance(manifest.get("references"), list):
        return 0, [f"{case_dir.name}: reference manifest requires schema_version 1 and references array"]
    checks = 0
    seen: set[str] = set()
    for index, row in enumerate(manifest["references"]):
        label = f"{case_dir.name}: reference {index}"
        if not isinstance(row, dict):
            issues.append(f"{label} must be an object")
            continue
        reference_id = row.get("reference_id")
        if not reference_id or reference_id in seen:
            issues.append(f"{label} has missing or duplicate reference_id")
        else:
            seen.add(reference_id)
        claim_file = row.get("claim_file")
        claim_path = row.get("claim_path")
        if not claim_file or claim_path is None:
            issues.append(f"{label} requires claim_file and claim_path")
        else:
            claim = expected_dir / claim_file
            try:
                claim_data = json.loads(claim.read_text(encoding="utf-8"))
                json_pointer(claim_data, claim_path)
            except Exception as exc:  # noqa: BLE001
                issues.append(f"{label} claim does not resolve: {exc}")
        source = find_source(case_dir / "inputs", row.get("source_file", ""))
        if source is None:
            issues.append(f"{label} source_file does not resolve uniquely")
            continue
        anchor = row.get("anchor")
        if not isinstance(anchor, dict):
            issues.append(f"{label} requires anchor object")
            continue
        extracted, error = source_text(source, anchor)
        if error:
            issues.append(f"{label} anchor failed: {error}")
            continue
        expected_text = row.get("expected_text")
        mode = row.get("match_mode", "contiguous")
        if mode not in {"contiguous", "normalized_whitespace"}:
            issues.append(f"{label} has unsupported match_mode: {mode}")
            continue
        if mode == "normalized_whitespace" and not row.get("normalization_reason"):
            issues.append(f"{label} normalized_whitespace requires normalization_reason")
            continue
        if expected_text is not None and (not isinstance(expected_text, str) or not text_matches(extracted, expected_text, mode)):
            issues.append(f"{label} expected_text not found at anchor")
            continue
        checks += 1
    return checks, issues


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--require", action="store_true", help="Require a manifest for each non-empty expected directory")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.output_dir.resolve()
    scenario_root = root / "scenario_packs"
    cases = sorted(path for path in scenario_root.iterdir() if path.is_dir()) if scenario_root.exists() else []
    checks = 0
    issues: list[str] = []
    for case in cases:
        case_checks, case_issues = audit_case(case, args.require)
        checks += case_checks
        issues.extend(case_issues)
    result = {"output_dir": str(root), "case_count": len(cases), "checks": checks, "blocking_issues": len(issues), "issues": issues}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"# Reference Integrity Audit: {root}")
        print(f"- Cases: {len(cases)}")
        print(f"- References checked: {checks}")
        print(f"- Blocking issues: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
