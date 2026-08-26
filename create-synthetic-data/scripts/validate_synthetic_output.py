#!/usr/bin/env python3
"""Validate common synthetic corpus packaging issues."""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path


PLACEHOLDER_RE = re.compile(r"\b(TBD|TBC|PLACEHOLDER|LOREM|XX/XX|20XX|2024/xxx|xxx)\b", re.I)
EVAL_HINT_RE = re.compile(
    r"(?:^|[/\\_. -])(?:answer[_ -]?keys?|labels?|expected[_ -]?answers?|evaluation[_ -]?only)(?=$|[/\\_. -])",
    re.I,
)


def load_exceptions(path: Path | None, root: Path) -> tuple[set[tuple[str, str]], list[str]]:
    if path is None or not path.exists():
        return set(), []
    invalid: list[str] = []
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report invalid control file
        return set(), [f"could not parse {path}: {exc}"]
    rows = data.get("exceptions") if isinstance(data, dict) else None
    if not isinstance(rows, list):
        return set(), [f"{path} must contain an exceptions array"]
    accepted: set[tuple[str, str]] = set()
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            invalid.append(f"exception {index} must be an object")
            continue
        rule = row.get("rule")
        path_text = row.get("path")
        reason = row.get("reason")
        if rule != "eval_leakage_path" or not path_text or not reason:
            invalid.append(f"exception {index} requires rule=eval_leakage_path, exact path, and reason")
            continue
        candidate = Path(path_text)
        if candidate.is_absolute() or any(char in path_text for char in "*?[]"):
            invalid.append(f"exception {index} path must be exact and output-relative: {path_text}")
            continue
        normalized = candidate.as_posix().lstrip("./")
        if not (root / normalized).is_file():
            invalid.append(f"exception {index} path does not exist: {normalized}")
            continue
        accepted.add((rule, normalized))
    return accepted, invalid


def load_inventory(path: Path):
    if path.suffix.lower() == ".csv":
        with path.open(newline="", encoding="utf-8-sig", errors="ignore") as handle:
            return list(csv.DictReader(handle))
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, dict) and isinstance(data.get("entries"), list):
        return data["entries"]
    if isinstance(data, dict) and isinstance(data.get("files"), list):
        return data["files"]
    if isinstance(data, dict) and isinstance(data.get("artifacts"), list):
        return data["artifacts"]
    if isinstance(data, list):
        return data
    return []


def relative_or_raw(path_text: str, root: Path) -> Path:
    candidate = Path(path_text)
    if candidate.is_absolute():
        return candidate
    root_candidate = root / candidate
    if root_candidate.exists():
        return root_candidate
    if candidate.exists():
        return candidate
    return root.parent / candidate


def scan_text_file(path: Path) -> list[str]:
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return []
    return sorted(set(match.group(0) for match in PLACEHOLDER_RE.finditer(text)))


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate synthetic output packaging.")
    parser.add_argument("output_dir", type=Path, help="Path to output directory")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    parser.add_argument("--exceptions", type=Path, help="Exact-path validation exception JSON")
    args = parser.parse_args()

    root = args.output_dir
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    exception_path = args.exceptions
    if exception_path is None:
        default_exceptions = root / "planning" / "validation_exceptions.json"
        exception_path = default_exceptions if default_exceptions.exists() else None
    exceptions, invalid_exceptions = load_exceptions(exception_path, root)

    findings = {
        "inventory_files": [],
        "missing_inventory_paths": [],
        "placeholder_hits": [],
        "eval_leakage_risks": [],
        "applied_exceptions": [],
        "invalid_exceptions": invalid_exceptions,
    }

    inventory_paths = {
        *root.rglob("*inventory*.json"),
        *root.rglob("*inventory*.csv"),
        *root.rglob("*manifest*.json"),
    }
    for inv in sorted(inventory_paths):
        entries = load_inventory(inv)
        findings["inventory_files"].append({"path": str(inv), "entries": len(entries)})
        for entry in entries:
            path_text = entry.get("path") if isinstance(entry, dict) else None
            if not path_text:
                continue
            candidate = relative_or_raw(path_text, root)
            if not candidate.exists():
                findings["missing_inventory_paths"].append({"inventory": str(inv), "path": path_text})

    source_roots = [root / "knowledge_sources", root / "scenario_packs"]
    text_suffixes = {".md", ".txt", ".csv", ".json", ".html", ".mmd", ".eml"}
    for source_root in source_roots:
        if not source_root.exists():
            continue
        for path in source_root.rglob("*"):
            if not path.is_file():
                continue
            rel = path.relative_to(root)
            if "expected" in rel.parts:
                continue
            rel_text = rel.as_posix()
            if EVAL_HINT_RE.search(rel_text):
                if ("eval_leakage_path", rel_text) in exceptions:
                    findings["applied_exceptions"].append({"rule": "eval_leakage_path", "path": rel_text})
                else:
                    findings["eval_leakage_risks"].append(str(path))
            if path.suffix.lower() in text_suffixes:
                hits = scan_text_file(path)
                if hits:
                    findings["placeholder_hits"].append({"path": str(path), "matches": hits})

    blocking = (
        len(findings["missing_inventory_paths"])
        + len(findings["eval_leakage_risks"])
        + len(findings["invalid_exceptions"])
    )
    result = {
        "output_dir": str(root),
        "exception_file": str(exception_path) if exception_path else None,
        "blocking_issues": blocking,
        **findings,
    }

    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(f"# Synthetic Output Validation: {root}")
        print()
        print(f"- Blocking issues: {blocking}")
        print(f"- Inventory files: {len(findings['inventory_files'])}")
        print(f"- Missing inventory paths: {len(findings['missing_inventory_paths'])}")
        print(f"- Placeholder hits: {len(findings['placeholder_hits'])}")
        print(f"- Eval leakage risks: {len(findings['eval_leakage_risks'])}")
        print(f"- Applied exceptions: {len(findings['applied_exceptions'])}")
        print(f"- Invalid exceptions: {len(findings['invalid_exceptions'])}")

    return 1 if blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
