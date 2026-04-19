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
- `schemas/workflow-catalog.schema.json` — JSON Schema for the catalog shape and normalized vocabularies
- `schemas/enums/owner.enum.json` — authoritative allowed values for `owner`
- `schemas/enums/deadline-type.enum.json` — authoritative allowed values for `deadline.type`
- `schemas/enums/dora-pillar.enum.json` — authoritative allowed values for `dora_mapping.pillars`
- `scripts/validate_catalog.py` — local validator for all catalog JSON files plus enum/schema alignment checks
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

The schema now enforces normalized enums for:
- `owner`
- `deadline.type`
- `dora_mapping.pillars`

The enum files under `schemas/enums/` are treated as authoritative vocabulary surfaces.
The local validator checks that the schema's embedded enum values remain identical to those enum files.

## Deadline policy

Most workflow deadlines are represented as:
- `null` when no universal timer is encoded in the source-backed surface
- structured objects when the workflow is timer-bearing
- `internal_policy` when the workflow should exist but the timing must be defined by operator policy or supervisory instruction

`DORA-009` contains the explicit staged reporting timing structure because that surface has concrete external timing.

## Validation

Local validation:

```bash
python -m pip install jsonschema==4.22.0
python scripts/validate_catalog.py
```

CI validation:
- runs on pushes to `main`
- runs on pull requests affecting catalog, schema, enum files, validator, or workflow files
- fails the build if any catalog JSON file no longer conforms to the schema
- fails the build if schema enums and normalized enum files diverge

## Design notes

The catalog intentionally separates:
- authority
- execution
- proof
- presentation

This repository currently stores the workflow catalog only. It does not yet contain execution logic, control evidence, or supervisory submission packaging.

## Next useful additions

- separate schema for `deadline`
- issue templates for workflow changes
- versioned changelog for catalog mutations
- CSV/JSONL export generation
- workflow examples or golden fixtures for validator tests
