#!/usr/bin/env python3
"""Validate WitnessOps DORA catalog files against the repository JSON Schema."""

from __future__ import annotations

import json
import sys
from pathlib import Path

try:
    from jsonschema import Draft202012Validator
    from referencing import Registry, Resource
except ImportError as exc:  # pragma: no cover
    raise SystemExit(
        "Missing dependency: jsonschema. Install with `pip install jsonschema`."
    ) from exc


REPO_ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = REPO_ROOT / "schemas" / "workflow-catalog.schema.json"
DEADLINE_SCHEMA_PATH = REPO_ROOT / "schemas" / "deadline.schema.json"
DORA_MAPPING_SCHEMA_PATH = REPO_ROOT / "schemas" / "dora-mapping.schema.json"
CATALOG_DIR = REPO_ROOT / "catalog"
DEADLINE_FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "deadline"
DORA_MAPPING_FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "dora-mapping"
WORKFLOW_FIXTURE_DIR = REPO_ROOT / "tests" / "fixtures" / "workflow"
VALID_DEADLINE_FIXTURES = [
    DEADLINE_FIXTURE_DIR / "valid-simple-deadline.json",
    DEADLINE_FIXTURE_DIR / "valid-regulatory-multi-stage.json",
]
INVALID_DEADLINE_FIXTURES = [
    DEADLINE_FIXTURE_DIR / "invalid-regulatory-multi-stage-missing-final-report.json",
    DEADLINE_FIXTURE_DIR / "invalid-simple-deadline-extra-key.json",
]
VALID_DORA_MAPPING_FIXTURES = [
    DORA_MAPPING_FIXTURE_DIR / "valid-major-incident-mapping.json",
]
INVALID_DORA_MAPPING_FIXTURES = [
    DORA_MAPPING_FIXTURE_DIR / "invalid-bad-pillar.json",
    DORA_MAPPING_FIXTURE_DIR / "invalid-empty-official-surface.json",
]
VALID_WORKFLOW_FIXTURES = [
    WORKFLOW_FIXTURE_DIR / "valid-dora-009-row.json",
]
INVALID_WORKFLOW_FIXTURES = [
    WORKFLOW_FIXTURE_DIR / "invalid-workflow-row-bad-owner.json",
    WORKFLOW_FIXTURE_DIR / "invalid-workflow-row-bad-pillar.json",
]
ENUM_SPECS = {
    "owner": {
        "path": REPO_ROOT / "schemas" / "enums" / "owner.enum.json",
        "schema_file": SCHEMA_PATH,
        "schema_path": ("$defs", "ownerEnum", "enum"),
    },
    "deadline.type": {
        "path": REPO_ROOT / "schemas" / "enums" / "deadline-type.enum.json",
        "schema_file": DEADLINE_SCHEMA_PATH,
        "schema_path": ("$defs", "deadlineTypeEnum", "enum"),
    },
    "dora_mapping.pillars": {
        "path": REPO_ROOT / "schemas" / "enums" / "dora-pillar.enum.json",
        "schema_file": DORA_MAPPING_SCHEMA_PATH,
        "schema_path": ("$defs", "doraPillarEnum", "enum"),
    },
}


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


def get_nested(document, path_parts):
    current = document
    for part in path_parts:
        current = current[part]
    return current


def build_registry(schema_docs: dict[Path, dict]) -> Registry:
    registry = Registry()
    for _, document in schema_docs.items():
        schema_id = document.get("$id")
        if not schema_id:
            raise ValueError("Schema document missing $id")
        registry = registry.with_resource(schema_id, Resource.from_contents(document))
    return registry


def validate_enum_alignment(schema_docs: dict[Path, dict]) -> bool:
    ok = True
    for name, spec in ENUM_SPECS.items():
        enum_path = spec["path"]
        schema_file = spec["schema_file"]
        if not enum_path.exists():
            print(f"Missing enum file: {enum_path}", file=sys.stderr)
            ok = False
            continue
        if schema_file not in schema_docs:
            print(f"Missing loaded schema for enum check: {schema_file}", file=sys.stderr)
            ok = False
            continue

        enum_doc = load_json(enum_path)
        file_enum = enum_doc.get("enum")
        schema_enum = get_nested(schema_docs[schema_file], spec["schema_path"])

        if file_enum != schema_enum:
            ok = False
            print(f"ENUM MISMATCH {name}", file=sys.stderr)
            print(f"  file:   {enum_path.relative_to(REPO_ROOT)}", file=sys.stderr)
            print(f"  schema: {schema_file.relative_to(REPO_ROOT)} -> {'/'.join(spec['schema_path'])}", file=sys.stderr)

    return ok


def validate_deadline_golden_fixtures(deadline_validator: Draft202012Validator) -> bool:
    ok = True

    for fixture_path in VALID_DEADLINE_FIXTURES:
        if not fixture_path.exists():
            print(f"Missing valid fixture: {fixture_path}", file=sys.stderr)
            ok = False
            continue
        data = load_json(fixture_path)
        errors = sorted(deadline_validator.iter_errors(data), key=lambda err: list(err.absolute_path))
        if errors:
            ok = False
            print(f"EXPECTED VALID BUT FAILED {fixture_path.relative_to(REPO_ROOT)}", file=sys.stderr)
            for error in errors:
                print(f"  - {format_error(error)}", file=sys.stderr)
        else:
            print(f"FIXTURE VALID   {fixture_path.relative_to(REPO_ROOT)}")

    for fixture_path in INVALID_DEADLINE_FIXTURES:
        if not fixture_path.exists():
            print(f"Missing invalid fixture: {fixture_path}", file=sys.stderr)
            ok = False
            continue
        data = load_json(fixture_path)
        errors = sorted(deadline_validator.iter_errors(data), key=lambda err: list(err.absolute_path))
        if not errors:
            ok = False
            print(f"EXPECTED INVALID BUT PASSED {fixture_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        else:
            print(f"FIXTURE INVALID {fixture_path.relative_to(REPO_ROOT)}")

    return ok


def validate_dora_mapping_golden_fixtures(dora_mapping_validator: Draft202012Validator) -> bool:
    ok = True

    for fixture_path in VALID_DORA_MAPPING_FIXTURES:
        if not fixture_path.exists():
            print(f"Missing valid dora_mapping fixture: {fixture_path}", file=sys.stderr)
            ok = False
            continue
        data = load_json(fixture_path)
        errors = sorted(dora_mapping_validator.iter_errors(data), key=lambda err: list(err.absolute_path))
        if errors:
            ok = False
            print(f"EXPECTED VALID BUT FAILED {fixture_path.relative_to(REPO_ROOT)}", file=sys.stderr)
            for error in errors:
                print(f"  - {format_error(error)}", file=sys.stderr)
        else:
            print(f"FIXTURE VALID   {fixture_path.relative_to(REPO_ROOT)}")

    for fixture_path in INVALID_DORA_MAPPING_FIXTURES:
        if not fixture_path.exists():
            print(f"Missing invalid dora_mapping fixture: {fixture_path}", file=sys.stderr)
            ok = False
            continue
        data = load_json(fixture_path)
        errors = sorted(dora_mapping_validator.iter_errors(data), key=lambda err: list(err.absolute_path))
        if not errors:
            ok = False
            print(f"EXPECTED INVALID BUT PASSED {fixture_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        else:
            print(f"FIXTURE INVALID {fixture_path.relative_to(REPO_ROOT)}")

    return ok


def validate_workflow_row_golden_fixtures(catalog_validator: Draft202012Validator) -> bool:
    ok = True

    for fixture_path in VALID_WORKFLOW_FIXTURES:
        if not fixture_path.exists():
            print(f"Missing valid workflow fixture: {fixture_path}", file=sys.stderr)
            ok = False
            continue
        data = load_json(fixture_path)
        errors = sorted(catalog_validator.iter_errors([data]), key=lambda err: list(err.absolute_path))
        if errors:
            ok = False
            print(f"EXPECTED VALID BUT FAILED {fixture_path.relative_to(REPO_ROOT)}", file=sys.stderr)
            for error in errors:
                print(f"  - {format_error(error)}", file=sys.stderr)
        else:
            print(f"FIXTURE VALID   {fixture_path.relative_to(REPO_ROOT)}")

    for fixture_path in INVALID_WORKFLOW_FIXTURES:
        if not fixture_path.exists():
            print(f"Missing invalid workflow fixture: {fixture_path}", file=sys.stderr)
            ok = False
            continue
        data = load_json(fixture_path)
        errors = sorted(catalog_validator.iter_errors([data]), key=lambda err: list(err.absolute_path))
        if not errors:
            ok = False
            print(f"EXPECTED INVALID BUT PASSED {fixture_path.relative_to(REPO_ROOT)}", file=sys.stderr)
        else:
            print(f"FIXTURE INVALID {fixture_path.relative_to(REPO_ROOT)}")

    return ok


def main() -> int:
    for required_path in (SCHEMA_PATH, DEADLINE_SCHEMA_PATH, DORA_MAPPING_SCHEMA_PATH):
        if not required_path.exists():
            print(f"Schema file not found: {required_path}", file=sys.stderr)
            return 2

    catalog_files = iter_catalog_files()
    if not catalog_files:
        print(f"No catalog files found in {CATALOG_DIR}", file=sys.stderr)
        return 2

    schema_docs = {
        SCHEMA_PATH: load_json(SCHEMA_PATH),
        DEADLINE_SCHEMA_PATH: load_json(DEADLINE_SCHEMA_PATH),
        DORA_MAPPING_SCHEMA_PATH: load_json(DORA_MAPPING_SCHEMA_PATH),
    }
    if not validate_enum_alignment(schema_docs):
        return 1

    registry = build_registry(schema_docs)
    catalog_validator = Draft202012Validator(schema_docs[SCHEMA_PATH], registry=registry)
    deadline_validator = Draft202012Validator(schema_docs[DEADLINE_SCHEMA_PATH], registry=registry)
    dora_mapping_validator = Draft202012Validator(schema_docs[DORA_MAPPING_SCHEMA_PATH], registry=registry)

    if not validate_deadline_golden_fixtures(deadline_validator):
        return 1
    if not validate_dora_mapping_golden_fixtures(dora_mapping_validator):
        return 1
    if not validate_workflow_row_golden_fixtures(catalog_validator):
        return 1

    failed = False
    for catalog_path in catalog_files:
        data = load_json(catalog_path)
        errors = sorted(catalog_validator.iter_errors(data), key=lambda err: list(err.absolute_path))
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
