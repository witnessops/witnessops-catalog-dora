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
- `schemas/workflow-catalog.schema.json` — JSON Schema for the catalog shape

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

## Deadline policy

Most workflow deadlines are represented as:
- `null` when no universal timer is encoded in the source-backed surface
- structured objects when the workflow is timer-bearing
- `internal_policy` when the workflow should exist but the timing must be defined by operator policy or supervisory instruction

`DORA-009` contains the explicit staged reporting timing structure because that surface has concrete external timing.

## Design notes

The catalog intentionally separates:
- authority
- execution
- proof
- presentation

This repository currently stores the workflow catalog only. It does not yet contain execution logic, control evidence, or supervisory submission packaging.

## Next useful additions

- normalized enums for `owner`
- separate schema for `deadline`
- issue templates for workflow changes
- versioned changelog for catalog mutations
- CSV/JSONL export generation
