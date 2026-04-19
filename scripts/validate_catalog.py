#!/usr/bin/env python3
"""Validate WitnessOps DORA catalog files against the repository JSON Schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install with `pip install jsonschema`."
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "workflow-catalog.schema.json"
CATALOG_DIR = REPO_ROOT / "catalog"


def load_json(path: Path):
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def iter_catalog_files() -> list[Path]:
    return sorted(
        path
        for path in CATALOG_DIR.glob("*.json")
        if path.is_file()
    )


def format_error(error) -> str:
    location = "$"
    if error.absolute_path:
        fragments = []
        for part in error.absolute_path:
            if isinstance(part, int):
                fragments.append(f"[{part}]")
            else:
                fragments.append(f".{part}")
        location += "".join(fragments)
    return f"{location}: {error.message}"


def main() -> int:
    if not SCHEMA_PATH.exists():
        print(f"Schema file not found: {SCHEMA_PATH}", file=sys.stderr)
        return 2

    catalog_files = iter_catalog_files()
    if not catalog_files:
        print(f"No catalog files found in {CATALOG_DIR}", file=sys.stderr)
        return 2

    schema = load_json(SCHEMA_PATH)
    validator = Draft202012Validator(schema)

    failed = False
    for catalog_path in catalog_files:
        data = load_json(catalog_path)
        errors = sorted(validator.iter_errors(data), key=lambda err: list(err.absolute_path))
        if errors:
            failed = True
            print(f"INVALID {catalog_path.relative_to(REPO_ROOT)}")
            for error in errors:
                print(f"  - {format_error(error)}")
        else:
            print(f"VALID   {catalog_path.relative_to(REPO_ROOT)}")

    if failed:
        return 1

    print("All catalog files passed schema validation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
