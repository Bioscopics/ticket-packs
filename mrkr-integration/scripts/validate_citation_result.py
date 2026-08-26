#!/usr/bin/env python3
"""Validate a sanitized MRKR result and citation bundle JSON file."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

ASSET_DIRECTORY = Path(__file__).resolve().parents[1] / "assets" / "python"
sys.path.insert(0, str(ASSET_DIRECTORY))

from mrkr_reference import CitationContractError, validate_persisted_result  # noqa: E402


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("result", type=Path, help="JSON with text and citationBundle")
    parser.add_argument("--require-citation", action="store_true")
    return parser.parse_args()


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text())
    if not isinstance(value, dict):
        raise CitationContractError("result JSON must be an object")
    return value


def main() -> int:
    arguments = _arguments()
    try:
        result = _load(arguments.result)
        text = result.get("text")
        bundle = result.get("citationBundle")
        if not isinstance(text, str) or not isinstance(bundle, dict):
            raise CitationContractError("result requires string text and object citationBundle")
        validate_persisted_result(
            text,
            bundle,
            require_citation=arguments.require_citation,
        )
    except (CitationContractError, OSError, json.JSONDecodeError) as error:
        print(f"FAIL: {error}", file=sys.stderr)
        return 1
    print("PASS: citation result is internally consistent")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
