# Shareable Packaging

Keep the full local work area for auditability, but build external archives from an explicit allowlist. Internal prompts, ticket packs, source paths, user names, and private calibration identifiers must not ship accidentally.

## Required Policy

For user-provided or private calibration sources, write `planning/shareable_package_policy.json`:

```json
{
  "schema_version": 1,
  "include": [
    "README.md",
    "inventories/**",
    "scenario_packs/**",
    "eval_sets/**",
    "planning/real_example_profile.json",
    "planning/modality_execution_matrix.json",
    "planning/execution_routing_matrix.json",
    "planning/validation_exceptions.json",
    "qa_reports/**"
  ],
  "exclude": [
    "qa_reports/private_source_notes/**"
  ],
  "forbidden_strings": [
    "<private source identifier>",
    "<absolute private source path>"
  ],
  "forbidden_regexes": []
}
```

Use exact forbidden identifiers/paths from the calibration copy boundary. The policy normally stays local because it contains the strings being blocked. Include it only when its contents are non-sensitive.

## Default Exclusions

The packager always excludes:

- worker prompts and prompt files;
- ticket packs, pre-pack blueprints, lane controls, and artifact registries;
- existing ZIP/SHA files, OS metadata, and temporary files.

Shareable planning contracts must use portable path aliases such as `$CODEX_HOME/...`, `$WORKSPACE/...`, or repository-relative paths. Put fully resolved local helper/runtime paths in local-only receipts excluded from the archive. The packager rejects included `/Users/...`, `/home/...`, `/Volumes/...`, temp-directory, and Windows user-home paths.

The default allowlist retains the two mandatory calibration JSON contracts, inventories, scenario/eval data, README, and QA evidence. Add other planning artifacts only after a privacy scan.

## Required Command

Write final package status before archiving, then run:

```bash
python3 scripts/package_synthetic_output.py <output_dir> \
  --zip <output_dir>/<dataset_name>.zip \
  --policy <output_dir>/planning/shareable_package_policy.json
```

The script:

- builds a sorted deterministic archive under one output-root directory;
- verifies inventory and modality-receipt paths are included;
- scans included paths and bytes for forbidden strings and private Downloads/Desktop/Documents paths;
- writes a SHA-256 sidecar;
- tests ZIP integrity.

After any file included by the allowlist changes, rebuild the archive and recompute the hash. Never edit a packaged file after the final hash without rebuilding.

## Delivery Gate

Before linking the archive, independently confirm:

- archive hash equals the sidecar;
- ZIP integrity passes;
- source/eval counts match inventories;
- no archive member is the archive itself;
- internal prompt/control exclusions have zero hits;
- privacy scan has zero hits;
- calibration, reference, leakage, and realism audits pass or have explicit approved exceptions.
