# AGENTS.md

## Identity

This repository is the machine-readable DORA workflow catalog for WitnessOps. It is a catalog and schema repo, not an official ESA/EU schema, not a legal opinion, not an execution engine, and not a proof package producer.

## Ownership

This repo owns:

- DORA-aligned workflow catalog rows under `catalog/`
- catalog schemas under `schemas/`
- normalized enum files under `schemas/enums/`
- golden pass/fail fixtures under `tests/fixtures/`
- local catalog validation through `scripts/validate_catalog.py`
- CI validation for catalog, schema, enum, fixture, and validator changes

This repo does not own:

- legal applicability decisions
- official regulatory interpretation
- source-system evidence
- supervisory submission packaging
- proof-run execution
- proof-engine package generation
- offline verifier implementation
- public website presentation
- customer evidence custody

## Non-Negotiable Rules

- Do not describe this repository as an official DORA schema or legal determination.
- Do not encode regulatory timers unless the source material provides a concrete timing rule.
- Do not weaken normalized enum discipline to make a row pass.
- Do not remove negative fixtures unless replacing them with equal or stronger failure coverage.
- Do not let catalog coherence imply legal applicability, compliance, or operational proof.
- Do not add execution logic, control evidence, supervisory submission packaging, production customer data, secrets, credentials, tokens, or private evidence.
- Keep authority, execution, proof, and presentation separate.

## Codex Security review

Use [`docs/CODEX_SECURITY_THREAT_MODEL.md`](./docs/CODEX_SECURITY_THREAT_MODEL.md) as the seed context for Codex Security review.

Codex Security may identify findings and propose patches, but it does not authorize merge, release, catalog-semantic changes, schema-semantic changes, fixture truth changes, legal interpretation, compliance claims, execution behavior, proof claims, deploy, or customer-impacting changes.

For security-sensitive changes, preserve these boundaries:

- the catalog is implementation support, not official law
- schemas define catalog structure only
- valid fixtures must pass and invalid fixtures must fail
- enum files remain authoritative vocabulary surfaces
- catalog validity is not proof that an entity is compliant or in scope

## Validation

Install validator dependency:

```bash
python -m pip install jsonschema==4.22.0
```

Run catalog validation:

```bash
python scripts/validate_catalog.py
```

GitHub Actions runs the same validator for catalog, schema, fixture, validator, and workflow changes.
