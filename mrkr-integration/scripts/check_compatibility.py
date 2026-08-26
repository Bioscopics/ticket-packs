#!/usr/bin/env python3
"""Verify the runtime and optional wheel against the packet compatibility manifest."""

from __future__ import annotations

import argparse
import hashlib
import importlib
import json
import sys
from importlib.metadata import version
from pathlib import Path
from typing import Any

MANIFEST_PATH = Path(__file__).resolve().parents[1] / "assets" / "compatibility.json"


def _arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--wheel", type=Path, help="Optional wheel to verify by SHA-256")
    return parser.parse_args()


def _manifest() -> dict[str, Any]:
    value = json.loads(MANIFEST_PATH.read_text())
    if not isinstance(value, dict):
        raise ValueError("compatibility manifest must be an object")
    return value


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    arguments = _arguments()
    manifest = _manifest()
    minimum = tuple(int(part) for part in manifest["python"].removeprefix(">=").split("."))
    if sys.version_info[: len(minimum)] < minimum:
        raise SystemExit(f"FAIL: Python {manifest['python']} is required")

    distribution = manifest["distribution"]
    installed = version(distribution)
    if installed != manifest["version"]:
        raise SystemExit(f"FAIL: expected {distribution} {manifest['version']}, found {installed}")

    module = importlib.import_module("mrkr")
    missing = [name for name in manifest["requiredPublicSymbols"] if not hasattr(module, name)]
    if missing:
        raise SystemExit(f"FAIL: missing public mrkr symbols: {', '.join(missing)}")

    if arguments.wheel is not None:
        actual = _sha256(arguments.wheel)
        if actual != manifest["wheelSha256"]:
            raise SystemExit("FAIL: wheel SHA-256 does not match compatibility manifest")

    print(f"PASS: Python {sys.version_info.major}.{sys.version_info.minor}")
    print(f"PASS: {distribution} {installed} public API")
    if arguments.wheel is not None:
        print("PASS: wheel SHA-256")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
