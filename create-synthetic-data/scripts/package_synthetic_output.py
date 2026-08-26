#!/usr/bin/env python3
"""Build a deterministic, privacy-scanned synthetic dataset archive."""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import re
import zipfile
from pathlib import Path


DEFAULT_INCLUDE = [
    "README.md",
    "inventories/**",
    "source_artifacts/**",
    "scenario_packs/**",
    "eval_sets/**",
    "planning/real_example_profile.json",
    "planning/modality_execution_matrix.json",
    "planning/execution_routing_matrix.json",
    "planning/validation_exceptions.json",
    "qa_reports/**",
]
DEFAULT_EXCLUDE = [
    ".DS_Store",
    "*.zip",
    "*.zip.sha256",
    "**/.DS_Store",
    "**/__MACOSX/**",
    "**/*.zip",
    "**/*.zip.sha256",
    "planning/**/*prompt*",
    "planning/worker_prompts/**",
    "planning/ticket_pack*",
    "planning/pre_pack*",
    "planning/*lane*",
    "planning/artifact_registry*",
]
DEFAULT_PRIVATE_PATH_PATTERNS = [
    re.compile(r"/Users/[^/\s]+/"),
    re.compile(r"/home/[^/\s]+/"),
    re.compile(r"/Volumes/[^/\s]+/"),
    re.compile(r"/(?:private/)?tmp/"),
    re.compile(r"[A-Za-z]:\\Users\\[^\\\s]+\\"),
]
TEXT_SUFFIXES = {".csv", ".eml", ".html", ".json", ".jsonl", ".md", ".txt", ".xml", ".yaml", ".yml"}


def matches(path: str, patterns: list[str]) -> bool:
    return any(fnmatch.fnmatch(path, pattern) for pattern in patterns)


def load_policy(path: Path | None) -> dict:
    if path is None or not path.exists():
        return {}
    data = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1:
        raise ValueError("shareable package policy requires schema_version 1")
    return data


def inventory_entries(path: Path) -> list[dict]:
    data = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(data, list):
        return [row for row in data if isinstance(row, dict)]
    if isinstance(data, dict):
        for key in ("entries", "files", "artifacts", "items"):
            if isinstance(data.get(key), list):
                return [row for row in data[key] if isinstance(row, dict)]
    return []


def normalize_inventory_path(path_text: str, root: Path) -> str:
    candidate = Path(path_text)
    if candidate.is_absolute():
        try:
            return candidate.relative_to(root).as_posix()
        except ValueError:
            return ""
    parts = candidate.parts
    if parts and parts[0] == root.name:
        candidate = Path(*parts[1:])
    return candidate.as_posix().lstrip("./")


def collect_members(root: Path, include: list[str], exclude: list[str], zip_path: Path) -> list[Path]:
    members: list[Path] = []
    for path in root.rglob("*"):
        if not path.is_file() or path.resolve() == zip_path.resolve():
            continue
        rel = path.relative_to(root).as_posix()
        if matches(rel, include) and not matches(rel, exclude):
            members.append(path)
    return sorted(members, key=lambda item: item.relative_to(root).as_posix())


def privacy_hits(root: Path, members: list[Path], forbidden_strings: list[str], forbidden_regexes: list[str]) -> list[str]:
    hits: list[str] = []
    compiled = [re.compile(pattern) for pattern in forbidden_regexes]
    for path in members:
        rel = path.relative_to(root).as_posix()
        raw = path.read_bytes()
        for token in forbidden_strings:
            if token and (token in rel or token.encode("utf-8", errors="ignore") in raw):
                hits.append(f"{rel}: forbidden string {token!r}")
        if path.suffix.lower() in TEXT_SUFFIXES:
            text = raw.decode("utf-8", errors="ignore")
            for pattern in DEFAULT_PRIVATE_PATH_PATTERNS:
                if pattern.search(text):
                    hits.append(f"{rel}: private local path")
            for pattern in compiled:
                if pattern.search(rel) or pattern.search(text):
                    hits.append(f"{rel}: forbidden regex {pattern.pattern!r}")
    return sorted(set(hits))


def contract_hits(root: Path, members: list[Path]) -> list[str]:
    included = {path.relative_to(root).as_posix() for path in members}
    issues: list[str] = []
    matrix_path = root / "planning" / "modality_execution_matrix.json"
    if matrix_path.exists() and "planning/modality_execution_matrix.json" in included:
        matrix = json.loads(matrix_path.read_text(encoding="utf-8"))
        for row in matrix.get("modalities", []):
            receipt = row.get("receipt_path") if isinstance(row, dict) else None
            if receipt and receipt not in included:
                issues.append(f"matrix receipt omitted from archive: {receipt}")
    inventories = sorted((root / "inventories").glob("*.json")) if (root / "inventories").exists() else []
    for inventory in inventories:
        for row in inventory_entries(inventory):
            path_text = row.get("path")
            if not path_text:
                continue
            normalized = normalize_inventory_path(path_text, root)
            if not normalized or normalized not in included:
                issues.append(f"inventory path omitted from archive: {path_text}")
    for required in (
        "README.md",
        "planning/real_example_profile.json",
        "planning/modality_execution_matrix.json",
        "planning/execution_routing_matrix.json",
    ):
        if (root / required).exists() and required not in included:
            issues.append(f"required package artifact omitted: {required}")
    return sorted(set(issues))


def write_zip(root: Path, members: list[Path], zip_path: Path) -> None:
    zip_path.parent.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in members:
            rel = path.relative_to(root).as_posix()
            info = zipfile.ZipInfo(f"{root.name}/{rel}", date_time=(1980, 1, 1, 0, 0, 0))
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (path.stat().st_mode & 0xFFFF) << 16
            archive.writestr(info, path.read_bytes())


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--zip", dest="zip_path", type=Path, required=True)
    parser.add_argument("--policy", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.output_dir.resolve()
    zip_path = args.zip_path.resolve()
    policy_path = args.policy
    if policy_path is None:
        default_policy = root / "planning" / "shareable_package_policy.json"
        policy_path = default_policy if default_policy.exists() else None
    try:
        policy = load_policy(policy_path)
    except Exception as exc:  # noqa: BLE001
        print(f"Invalid package policy: {exc}")
        return 1
    include = list(policy.get("include") or DEFAULT_INCLUDE)
    exclude = sorted(set(DEFAULT_EXCLUDE + list(policy.get("exclude") or [])))
    forbidden_strings = [str(value) for value in policy.get("forbidden_strings") or []]
    forbidden_regexes = [str(value) for value in policy.get("forbidden_regexes") or []]
    members = collect_members(root, include, exclude, zip_path)
    issues = privacy_hits(root, members, forbidden_strings, forbidden_regexes) + contract_hits(root, members)
    if issues:
        result = {"status": "blocked", "members": len(members), "issues": issues}
        print(json.dumps(result, indent=2) if args.json else "\n".join(["# Package blocked", *[f"- {issue}" for issue in issues]]))
        return 1
    write_zip(root, members, zip_path)
    digest = hashlib.sha256(zip_path.read_bytes()).hexdigest()
    sidecar = zip_path.with_suffix(zip_path.suffix + ".sha256")
    sidecar.write_text(f"{digest}  {zip_path.name}\n", encoding="ascii")
    with zipfile.ZipFile(zip_path) as archive:
        bad_member = archive.testzip()
    result = {
        "status": "complete" if bad_member is None else "blocked",
        "archive": str(zip_path),
        "sidecar": str(sidecar),
        "members": len(members),
        "bytes": zip_path.stat().st_size,
        "sha256": digest,
        "integrity": "pass" if bad_member is None else f"failed: {bad_member}",
        "privacy_hits": 0,
    }
    print(json.dumps(result, indent=2) if args.json else "\n".join(f"- {key}: {value}" for key, value in result.items()))
    return 0 if bad_member is None else 1


if __name__ == "__main__":
    raise SystemExit(main())
