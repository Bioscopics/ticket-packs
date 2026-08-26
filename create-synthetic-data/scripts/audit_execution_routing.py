#!/usr/bin/env python3
"""Audit dynamic lane/model routing for synthetic-data task packs."""

from __future__ import annotations

import argparse
import json
from pathlib import Path


LEVELS = {"low", "medium", "high"}
MODEL_CLASSES = {"fast", "balanced", "frontier"}
REASONING_LEVELS = {"low", "medium", "high", "xhigh"}
PARALLELISM = {"parallel", "serial"}
DECISION_ROLES = ("calibration", "architect", "domain", "label", "review")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("output_dir", type=Path)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root = args.output_dir.resolve()
    path = root / "planning" / "execution_routing_matrix.json"
    issues: list[str] = []
    if not path.exists():
        issues.append("missing planning/execution_routing_matrix.json")
        data: dict = {}
    else:
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except Exception as exc:  # noqa: BLE001
            data = {}
            issues.append(f"invalid execution routing matrix: {exc}")
    if data.get("schema_version") != 1:
        issues.append("execution_routing_matrix.schema_version must be 1")
    if not data.get("routing_goal"):
        issues.append("execution_routing_matrix.routing_goal is required")
    lanes = data.get("lanes")
    if not isinstance(lanes, list) or not lanes:
        issues.append("execution_routing_matrix.lanes must be a non-empty array")
        lanes = []
    seen: set[str] = set()
    required = (
        "lane_id",
        "role",
        "source_profile_factors",
        "uncertainty",
        "messiness",
        "stakes",
        "coupling",
        "volume",
        "validator_strength",
        "model_class",
        "reasoning",
        "parallelism",
        "escalation_triggers",
    )
    for index, lane in enumerate(lanes):
        label = f"lane {index}"
        if not isinstance(lane, dict):
            issues.append(f"{label} must be an object")
            continue
        lane_id = lane.get("lane_id")
        label = f"lane {lane_id or index}"
        for field in required:
            if lane.get(field) in (None, "", []):
                issues.append(f"{label} missing {field}")
        for field in ("source_profile_factors", "escalation_triggers"):
            if not isinstance(lane.get(field), list):
                issues.append(f"{label} {field} must be an array")
        if lane_id in seen:
            issues.append(f"duplicate lane_id: {lane_id}")
        elif lane_id:
            seen.add(lane_id)
        for field in ("uncertainty", "messiness", "stakes", "coupling", "volume"):
            if lane.get(field) not in LEVELS:
                issues.append(f"{label} {field} must be low, medium, or high")
        if lane.get("validator_strength") not in {"weak", "medium", "strong"}:
            issues.append(f"{label} validator_strength must be weak, medium, or strong")
        if lane.get("model_class") not in MODEL_CLASSES:
            issues.append(f"{label} model_class must be fast, balanced, or frontier")
        if lane.get("reasoning") not in REASONING_LEVELS:
            issues.append(f"{label} reasoning must be low, medium, high, or xhigh")
        if lane.get("parallelism") not in PARALLELISM:
            issues.append(f"{label} parallelism must be parallel or serial")
        estimated = lane.get("estimated_minutes")
        if estimated is not None and (not isinstance(estimated, (int, float)) or estimated <= 0):
            issues.append(f"{label} estimated_minutes must be positive")
        role = str(lane.get("role", "")).lower()
        model_class = lane.get("model_class")
        if model_class == "fast":
            if lane.get("uncertainty") == "high" or lane.get("stakes") == "high":
                issues.append(f"{label} cannot use fast model_class with high uncertainty or stakes")
            if lane.get("validator_strength") != "strong":
                issues.append(f"{label} fast model_class requires strong validators")
        if "review" in role and model_class == "fast":
            issues.append(f"{label} independent reviewer cannot use fast model_class")
        if any(token in role for token in DECISION_ROLES) and (
            lane.get("uncertainty") == "high" or lane.get("stakes") == "high"
        ) and model_class != "frontier":
            issues.append(f"{label} high-risk decision role requires frontier model_class")
    result = {"output_dir": str(root), "lanes": len(lanes), "blocking_issues": len(issues), "issues": issues}
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"# Execution Routing Audit: {root}")
        print(f"- Lanes: {len(lanes)}")
        print(f"- Blocking issues: {len(issues)}")
        for issue in issues:
            print(f"  - {issue}")
    return 1 if issues else 0


if __name__ == "__main__":
    raise SystemExit(main())
