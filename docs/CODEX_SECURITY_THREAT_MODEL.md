# Codex Security Threat Model — witnessops-catalog-dora

Status: `repo_prep_seed_for_codex_security`

This document is a repository-specific seed for Codex Security review and GitHub PR review. It is not a vulnerability report, not a scan result, not legal advice, not an official regulatory interpretation, and not proof of DORA compliance.

## Scope

This repository is the machine-readable DORA workflow catalog for WitnessOps.

It owns:

- DORA-aligned workflow catalog rows under `catalog/`
- catalog schemas under `schemas/`
- normalized enum files under `schemas/enums/`
- deadline schema and deadline fixture behavior
- DORA mapping schema and mapping fixture behavior
- workflow-row fixture behavior
- local catalog validation through `scripts/validate_catalog.py`
- CI validation for catalog, schema, enum, fixture, validator, and workflow changes

## Out of scope

This repository does not own:

- official ESA/EU schema authority
- legal applicability decisions
- official regulatory interpretation
- supervisory submission packaging
- source-system evidence
- proof-run execution
- proof-engine package generation
- offline verifier implementation
- public website presentation
- customer evidence custody
- production compliance claims

Do not infer that a passing Codex Security review verifies any out-of-scope system.

## Authority boundaries

- `main` in `witnessops/witnessops-catalog-dora` is the code/content authority for this catalog repo.
- `schemas/enums/` files are authoritative vocabulary surfaces for normalized enums.
- The local validator checks schema enum values against enum files.
- Valid fixtures must pass validation.
- Invalid fixtures must fail validation.
- Catalog validity is structural/catalog validity only; it is not legal applicability, supervisory acceptance, operational proof, or compliance proof.
- Codex Security may identify findings and suggest patches.
- Codex Security findings do not authorize merge, release, catalog-semantic changes, schema-semantic changes, fixture truth changes, legal interpretation, compliance claims, execution behavior, proof claims, deploy, or customer-impacting changes.
- Human maintainer review remains required for changes that affect catalog rows, schema acceptance, enum vocabulary, deadline semantics, DORA mapping semantics, fixture truth, validator behavior, or compliance-language boundaries.

## Primary review surfaces

Treat the following as first-class review surfaces:

1. `catalog/dora-workflows.v1.json`
   - workflow IDs and names
   - triggers and owners
   - deadlines
   - required evidence
   - status states
   - DORA mapping
   - no overclaim that catalog row equals legal applicability

2. `schemas/workflow-catalog.schema.json`
   - top-level workflow row contract
   - required fields
   - `additionalProperties` boundaries
   - schema references

3. `schemas/deadline.schema.json`
   - deadline type handling
   - regulatory multi-stage structure
   - concrete timer boundaries

4. `schemas/dora-mapping.schema.json`
   - pillar vocabulary
   - official surface constraints
   - exact incident-surface narrowing

5. `schemas/enums/`
   - owner enum
   - deadline type enum
   - DORA pillar enum
   - normalized vocabulary authority

6. `tests/fixtures/`
   - valid deadline fixtures
   - invalid deadline fixtures
   - valid DORA mapping fixtures
   - invalid DORA mapping fixtures
   - valid workflow-row fixtures
   - invalid workflow-row fixtures

7. `scripts/validate_catalog.py`
   - local schema resolution
   - enum/schema alignment checks
   - fixture corpus behavior
   - no implicit network fetch reliance

8. `.github/workflows/validate-catalog.yml`
   - deterministic validation for catalog/schema/fixture/validator changes
   - no secrets or external system dependency

## Untrusted inputs

Review all handling of:

- catalog row JSON
- schema JSON
- enum JSON
- fixture JSON
- deadline values
- official surface strings
- owner values
- DORA pillar values
- validator path resolution
- schema `$ref` resolution
- any value that resembles real customer evidence, confidential regulatory submissions, secrets, credentials, tokens, production system names, private evidence paths, or private client data

## Security invariants

The following must remain true unless an explicit design change is reviewed and approved:

- This repo must not be described as an official ESA/EU schema.
- This repo must not make legal applicability decisions.
- Catalog validity must not be presented as DORA compliance proof.
- Regulatory timers must only be encoded where the source material provides a concrete timing rule.
- Enum files must remain authoritative vocabulary surfaces.
- Schema enum values must stay aligned with enum files.
- Valid fixtures must pass and invalid fixtures must fail.
- Invalid fixture coverage must not be weakened to make catalog changes pass.
- Dedicated deadline and DORA mapping schemas must resolve locally, not through implicit network fetches.
- Catalog rows must not include production customer data, private evidence, confidential submission material, secrets, credentials, tokens, or private system details.
- Authority, execution, proof, and presentation must remain separate.

## High-priority finding classes

Treat the following as P1 for review purposes:

- invalid fixtures validate successfully
- valid fixtures stop proving intended behavior because validator coverage is weakened
- schema accepts undeclared fields that can smuggle legal, proof, evidence, or authority claims
- enum/schema drift is no longer detected
- regulatory timer fields allow ambiguous or unsupported timing claims
- DORA mapping schema allows disallowed incident surfaces under exact single-pillar incident mappings
- validator begins relying on implicit network fetches for local schemas
- catalog row includes secrets, customer evidence, confidential submission material, credentials, tokens, production targets, or private evidence paths
- docs or catalog language claims official regulatory authority, legal applicability, supervisory acceptance, or compliance proof without a named mechanism outside this repo

## Lower-priority but relevant finding classes

Review but do not automatically treat as P1 without demonstrated impact:

- cosmetic README wording that preserves boundaries
- missing web-app security headers, because this repo is not a web app
- dependency advisories not reachable through local validation behavior
- broad performance concerns without a concrete schema-validation amplification path

## Review instructions for Codex

When reviewing this repository:

- prefer small, surgical findings over broad refactors
- name the affected catalog row, schema, enum, fixture, validator path, workflow, or documentation boundary
- include a concrete schema-bypass, fixture-drift, enum-drift, overclaim, or local-resolution failure path where possible
- do not weaken schemas, enum checks, or negative fixtures to make catalog rows pass
- do not add legal interpretation, official-regulator claims, compliance proof claims, execution logic, proof-engine behavior, verifier behavior, or customer evidence
- do not add production credentials, customer data, confidential submission material, or private proof bundles as fixtures
- preserve `python scripts/validate_catalog.py` as the baseline validation command unless a separate tooling lane changes it

## Suggested Codex Security scan configuration

Initial scan seed:

- repository: `witnessops/witnessops-catalog-dora`
- branch: `main`
- history window: `180 days`
- environment family: `Python / JSON Schema catalog`
- setup command: `python -m pip install jsonschema==4.22.0`
- validation command for proposed catalog/schema patches: `python scripts/validate_catalog.py`
- agent secrets: none
- production credentials: prohibited
- customer data fixtures: prohibited
- private evidence fixtures: prohibited
- legal applicability rewrites without maintainer authority: prohibited
- compliance proof claims: prohibited

## Closure condition for this prep artifact

This prep artifact is sufficient when:

- Codex Security scan context can be seeded from this file.
- `AGENTS.md` points reviewers to this file.
- A private-reporting `SECURITY.md` exists for the repo.
- No catalog rows, schemas, enum files, fixtures, validator behavior, workflow behavior, production settings, secrets, customer evidence, legal interpretation, compliance claims, or proof claims were changed by this prep pass.
