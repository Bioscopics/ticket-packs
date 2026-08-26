#!/usr/bin/env python3
"""Summarize a synthetic output directory by top-level usage groups."""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path


def count_files(path: Path) -> int:
    return sum(1 for item in path.rglob("*") if item.is_file())


def extension_counts(path: Path) -> dict[str, int]:
    counts: Counter[str] = Counter()
    for item in path.rglob("*"):
        if item.is_file():
            counts[item.suffix.lower() or "<no_ext>"] += 1
    return dict(sorted(counts.items()))


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit a synthetic output directory.")
    parser.add_argument("output_dir", type=Path, help="Path to output directory")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of Markdown")
    args = parser.parse_args()

    root = args.output_dir
    if not root.exists() or not root.is_dir():
        raise SystemExit(f"Not a directory: {root}")

    groups = []
    for child in sorted(item for item in root.iterdir() if item.is_dir()):
        groups.append(
            {
                "path": str(child),
                "files": count_files(child),
                "extensions": extension_counts(child),
                "children": [
                    {"path": str(grand), "files": count_files(grand)}
                    for grand in sorted(item for item in child.iterdir() if item.is_dir())
                ],
            }
        )

    summary = {
        "output_dir": str(root),
        "total_files": count_files(root),
        "groups": groups,
    }

    if args.json:
        print(json.dumps(summary, indent=2, ensure_ascii=False))
        return 0

    print(f"# Synthetic Output Audit: {root}")
    print()
    print(f"- Total files: {summary['total_files']}")
    print()
    print("| Group | Files | Extensions |")
    print("|---|---:|---|")
    for group in groups:
        ext_text = ", ".join(f"{k}: {v}" for k, v in group["extensions"].items())
        print(f"| `{group['path']}` | {group['files']} | {ext_text} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
