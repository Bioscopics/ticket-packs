#!/usr/bin/env python3
"""Audit required real-example calibration and modality-helper contracts."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path


MEDIA_EXTENSIONS = {
    "image": {".png", ".jpg", ".jpeg", ".webp", ".gif", ".tif", ".tiff"},
    "audio": {".wav", ".mp3", ".m4a", ".aac", ".ogg", ".flac"},
    "video": {".mp4", ".mov", ".webm", ".avi", ".mkv"},
    "pdf": {".pdf"},
    "document": {".docx", ".odt", ".rtf"},
    "spreadsheet": {".xlsx", ".xls", ".ods"},
    "presentation": {".pptx", ".ppt", ".odp"},
}

EXCLUDED_ROOTS = {"planning", "control", "qa_reports", "inventories"}
PROFILE_FIELDS = (
    "family",
    "formats",
    "length_or_scale",
    "structure",
    "style_or_register",
    "complexity",
    "metadata",
    "imperfections",
    "relationships",
)


def load_json(path: Path, issues: list[str]) -> dict:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:  # noqa: BLE001 - report malformed control artifacts
        issues.append(f"invalid JSON: {path}: {exc}")
        return {}
    if not isinstance(value, dict):
        issues.append(f"expected JSON object: {path}")
        return {}
    return value


def detect_modalities(root: Path) -> dict[str, list[str]]:
    detected: dict[str, list[str]] = {name: [] for name in MEDIA_EXTENSIONS}
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        relative = path.relative_to(root)
        if relative.parts and relative.parts[0] in EXCLUDED_ROOTS:
            continue
        if relative.parts[:2] == ("eval_sets", "labels_or_answer_keys"):
            continue
        for modality, extensions in MEDIA_EXTENSIONS.items():
            if path.suffix.lower() in extensions:
                detected[modality].append(str(relative))
    return {key: value for key, value in detected.items() if value}


def audit_profile(root: Path, allow_blocked: bool, issues: list[str]) -> dict:
    path = root / "planning" / "real_example_profile.json"
    if not path.exists():
        issues.append("missing planning/real_example_profile.json")
        return {}
    profile = load_json(path, issues)
    status = profile.get("status")
    if status not in {"complete", "proxy", "blocked"}:
        issues.append("real_example_profile.status must be complete, proxy, or blocked")
    if status == "blocked" and not allow_blocked:
        issues.append("real-example calibration is blocked; rerun with --allow-blocked only for an explicit downgrade")
    sources = profile.get("sources")
    if not isinstance(sources, list) or not sources:
        issues.append("real_example_profile.sources must contain at least one source or documented proxy")
    else:
        for index, source in enumerate(sources):
            if not isinstance(source, dict):
                issues.append(f"source {index} must be an object")
                continue
            for field in ("source_id", "kind", "title", "url_or_path", "accessed_at", "license_or_permission", "artifact_types"):
                if not source.get(field):
                    issues.append(f"source {index} missing {field}")
    families = profile.get("observed_profile", {}).get("artifact_families", [])
    if not isinstance(families, list) or not families:
        issues.append("observed_profile.artifact_families must be non-empty")
    else:
        for index, family in enumerate(families):
            if not isinstance(family, dict):
                issues.append(f"observed family {index} must be an object")
                continue
            for field in PROFILE_FIELDS:
                if field not in family or family[field] in (None, "", []):
                    issues.append(f"observed family {index} missing {field}")
    targets = profile.get("target_profile", {}).get("artifact_families", [])
    if not isinstance(targets, list) or not targets:
        issues.append("target_profile.artifact_families must be non-empty")
    if not profile.get("copy_boundary"):
        issues.append("real_example_profile.copy_boundary must be non-empty")
    if status in {"proxy", "blocked"} and not profile.get("known_gaps"):
        issues.append(f"status {status} requires known_gaps")
    return profile


def audit_matrix(root: Path, detected: dict[str, list[str]], issues: list[str], phase: str) -> None:
    path = root / "planning" / "modality_execution_matrix.json"
    if not path.exists():
        if detected:
            issues.append("missing planning/modality_execution_matrix.json for native/media source artifacts")
        return
    matrix = load_json(path, issues)
    schema_version = matrix.get("schema_version")
    if schema_version is not None and schema_version != 1:
        issues.append("modality_execution_matrix.schema_version must be 1 when present")
    rows = matrix.get("modalities")
    if not isinstance(rows, list):
        issues.append("modality_execution_matrix.modalities must be an array")
        return
    by_modality: dict[str, dict] = {}
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            issues.append(f"modality row {index} must be an object")
            continue
        modality = row.get("modality") or f"row-{index}"
        if modality in by_modality:
            issues.append(f"duplicate modality row: {modality}")
        else:
            by_modality[modality] = row
        for field in ("execution_owner", "availability", "calibration_source_ids", "generation_method", "runtime_dependencies", "validation", "receipt_path", "status"):
            if not row.get(field):
                issues.append(f"modality {modality} missing {field}")
        if row.get("availability") not in {"available", "available_runtime_blocked", "unavailable"}:
            issues.append(f"modality {modality} availability must be available, available_runtime_blocked, or unavailable")
        status = row.get("status")
        allowed_statuses = {"planned", "blocked", "downgraded"} if phase == "planning" else {"complete", "blocked", "downgraded"}
        if status not in allowed_statuses:
            issues.append(
                f"modality {modality} status must be {', '.join(sorted(allowed_statuses))} during {phase}"
            )
        if status in {"planned", "complete", "downgraded"} and not row.get("skill_paths"):
            issues.append(f"modality {modality} missing skill_paths")
        skill_paths = row.get("skill_paths")
        if isinstance(skill_paths, list):
            for skill_path in skill_paths:
                if not isinstance(skill_path, str) or not skill_path:
                    issues.append(f"modality {modality} skill_paths must contain non-empty strings")
                elif skill_path.startswith("/") or re.match(r"^[A-Za-z]:[\\/]", skill_path):
                    issues.append(f"modality {modality} skill path must be portable, not absolute: {skill_path}")
        if status == "blocked" and not row.get("blocked_reason"):
            issues.append(f"blocked modality {modality} missing blocked_reason")
        if status == "downgraded":
            if row.get("availability") == "available":
                issues.append(f"downgraded modality {modality} availability must explain the capability limitation")
            deviation = row.get("deviation")
            if not isinstance(deviation, dict):
                issues.append(f"downgraded modality {modality} missing deviation object")
            else:
                for field in ("reason", "impact"):
                    if not deviation.get(field):
                        issues.append(f"downgraded modality {modality} deviation missing {field}")
                if not (deviation.get("approval") or deviation.get("status")):
                    issues.append(f"downgraded modality {modality} deviation missing approval")
        if status == "planned" and row.get("availability") == "unavailable":
            issues.append(f"planned modality {modality} cannot have unavailable capability")
        receipt = row.get("receipt_path")
        if phase == "delivery" and status in {"complete", "downgraded"} and receipt and not (root / receipt).is_file():
            issues.append(f"modality {modality} helper receipt does not exist: {receipt}")
    for modality, paths in detected.items():
        row = by_modality.get(modality)
        if not row:
            issues.append(f"detected {modality} artifacts but no modality matrix row: {paths[0]}")
            continue
        if phase == "delivery" and row.get("status") == "blocked":
            issues.append(f"detected {modality} artifacts but modality matrix status is blocked: {paths[0]}")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--allow-blocked", action="store_true")
    parser.add_argument("--phase", choices=("planning", "delivery"), default="delivery")
    args = parser.parse_args()
    root = args.output_dir.resolve()
    issues: list[str] = []
    audit_profile(root, args.allow_blocked, issues)
    detected = detect_modalities(root)
    audit_matrix(root, detected, issues, args.phase)

    print(f"# Calibration Contract Audit: {root}")
    print(f"- Phase: {args.phase}")
    print(f"- Detected native/media modalities: {', '.join(sorted(detected)) or 'none'}")
    print(f"- Blocking issues: {len(issues)}")
    for issue in issues:
        print(f"  - {issue}")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
