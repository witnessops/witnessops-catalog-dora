# witnessops-catalog-dora

Machine-readable DORA workflow catalog for WitnessOps.

## Purpose

This repository holds a structured catalog of workflows aligned to the Digital Operational Resilience Act (DORA) operating surfaces.

Boundary:
- this is an implementation catalog, not an official ESA/EU schema
- legal applicability depends on entity scope and operating context
- explicit regulatory timers are only encoded where the source material provides a concrete timing rule

## Current files

- `catalog/dora-workflows.v1.json` — initial machine-readable workflow catalog
- `schemas/workflow-catalog.schema.json` — top-level catalog schema
- `schemas/deadline.schema.json` — dedicated deadline schema with per-type structural rules
- `schemas/enums/owner.enum.json` — authoritative allowed values for `owner`
- `schemas/enums/deadline-type.enum.json` — authoritative allowed values for `deadline.type`
- `schemas/enums/dora-pillar.enum.json` — authoritative allowed values for `dora_mapping.pillars`
- `tests/fixtures/deadline/` — golden deadline fixtures for expected pass/fail behavior
- `scripts/validate_catalog.py` — local validator for catalog JSON files, enum/schema alignment checks, external schema resolution, and fixture validation
- `.github/workflows/validate-catalog.yml` — CI gate enforcing schema validation on push and pull request

## Data contract

Each workflow row contains:

- `workflow_id`
- `workflow_name`
- `trigger`
- `owner`
- `deadline`
- `required_evidence`
- `status_states`
- `dora_mapping`

## Vocabulary discipline

The schema enforces normalized enums for:
- `owner`
- `deadline.type`
- `dora_mapping.pillars`

The enum files under `schemas/enums/` are treated as authoritative vocabulary surfaces.
The local validator checks that schema enum values remain identical to those enum files.

## Deadline contract

`deadline` is now split into a dedicated schema.

Rules:
- `deadline` may still be `null`
- non-null deadlines must conform to `schemas/deadline.schema.json`
- `regulatory_multi_stage` must include:
  - `initial_notification`
  - `intermediate_report`
  - `final_report`
- simpler deadline types use a smaller bounded object with:
  - `type`
  - `value`

This split keeps timer-bearing workflows structurally explicit without forcing the same shape onto simpler internal-policy deadlines.

## Golden fixtures

Current deadline fixtures:
- `tests/fixtures/deadline/valid-simple-deadline.json`
- `tests/fixtures/deadline/valid-regulatory-multi-stage.json`
- `tests/fixtures/deadline/invalid-regulatory-multi-stage-missing-final-report.json`
- `tests/fixtures/deadline/invalid-simple-deadline-extra-key.json`

The validator treats these as an expected pass/fail corpus:
- valid fixtures must validate successfully
- invalid fixtures must fail validation

This gives the repository a replayable behavior check for the deadline schema, not just a shape check against production data.

## Validation

Local validation:

```bash
python -m pip install jsonschema==4.22.0
python scripts/validate_catalog.py
```

CI validation:
- runs on pushes to `main`
- runs on pull requests affecting catalog, schema, enum files, validator, fixture files, or workflow files
- fails the build if any catalog JSON file no longer conforms to the schema
- fails the build if schema enums and normalized enum files diverge
- resolves the dedicated deadline schema during validation rather than relying on implicit network fetches
- runs the golden deadline fixture corpus

## Design notes

The catalog intentionally separates:
- authority
- execution
- proof
- presentation

This repository currently stores the workflow catalog only. It does not yet contain execution logic, control evidence, or supervisory submission packaging.

## Next useful additions

- issue templates for workflow changes
- versioned changelog for catalog mutations
- CSV/JSONL export generation
- golden fixtures for full workflow rows
- dedicated schema for `dora_mapping` if official-surface discipline needs tightening later
