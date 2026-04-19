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
- `schemas/dora-mapping.schema.json` — dedicated DORA mapping schema for pillars and official surfaces
- `schemas/enums/owner.enum.json` — authoritative allowed values for `owner`
- `schemas/enums/deadline-type.enum.json` — authoritative allowed values for `deadline.type`
- `schemas/enums/dora-pillar.enum.json` — authoritative allowed values for `dora_mapping.pillars`
- `tests/fixtures/deadline/` — golden deadline fixtures for expected pass/fail behavior
- `tests/fixtures/dora-mapping/` — golden DORA mapping fixtures for expected pass/fail behavior
- `tests/fixtures/workflow/` — golden full-row workflow fixtures for expected pass/fail behavior
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

`deadline` is split into a dedicated schema.

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

## DORA mapping contract

`dora_mapping` is now split into a dedicated schema.

Rules today:
- `pillars` must use normalized allowed values
- `official_surface` remains a bounded non-empty string array
- the top-level workflow schema resolves `dora_mapping` through `schemas/dora-mapping.schema.json`
- exact single-pillar `ict_related_incidents` mappings are currently narrowed to:
  - `incident_management`
  - `major_incident_reporting`

Reason for the split:
- pillar vocabulary now has a single authority surface
- future per-pillar restrictions on `official_surface` can be added in one place without modifying the whole workflow schema

Implementation note:
- to preserve catalog validity under the narrow exact-incident branch, incident-adjacent rows that use other incident surfaces are currently modeled as mixed-pillar mappings rather than exact single-pillar incident mappings

## Golden fixtures

Current deadline fixtures:
- `tests/fixtures/deadline/valid-simple-deadline.json`
- `tests/fixtures/deadline/valid-regulatory-multi-stage.json`
- `tests/fixtures/deadline/invalid-regulatory-multi-stage-missing-final-report.json`
- `tests/fixtures/deadline/invalid-simple-deadline-extra-key.json`

Current DORA mapping fixtures:
- `tests/fixtures/dora-mapping/valid-major-incident-mapping.json`
- `tests/fixtures/dora-mapping/valid-incident-management-mapping.json`
- `tests/fixtures/dora-mapping/invalid-bad-pillar.json`
- `tests/fixtures/dora-mapping/invalid-empty-official-surface.json`
- `tests/fixtures/dora-mapping/invalid-ict-related-incidents-disallowed-surface.json`

Current workflow-row fixtures:
- `tests/fixtures/workflow/valid-dora-009-row.json`
- `tests/fixtures/workflow/invalid-workflow-row-bad-owner.json`
- `tests/fixtures/workflow/invalid-workflow-row-bad-pillar.json`

The validator treats these as an expected pass/fail corpus:
- valid fixtures must validate successfully
- invalid fixtures must fail validation

Deadline fixtures are validated against the dedicated deadline schema.
DORA mapping fixtures are validated against the dedicated DORA mapping schema.
Workflow-row fixtures are wrapped into a one-element catalog array and validated against the full top-level catalog schema.

This gives the repository a replayable behavior check for:
- deadline contract behavior
- dora_mapping contract behavior
- full workflow row contract behavior

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
- resolves the dedicated DORA mapping schema during validation rather than relying on implicit network fetches
- runs the golden deadline fixture corpus
- runs the golden DORA mapping fixture corpus
- runs the golden workflow-row fixture corpus

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
- expand per-pillar `official_surface` rules inside `schemas/dora-mapping.schema.json` one pillar at a time
