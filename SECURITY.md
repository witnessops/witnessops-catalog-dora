# Security Policy

We take security issues in this repository seriously. This document describes what is in scope, how to report a suspected vulnerability, and what to expect from us in return.

## Scope

This repository contains the machine-readable DORA workflow catalog for WitnessOps:

- DORA-aligned workflow catalog rows under `catalog/`
- catalog schemas under `schemas/`
- normalized enum files under `schemas/enums/`
- deadline schema and deadline fixture behavior
- DORA mapping schema and mapping fixture behavior
- workflow-row fixture behavior
- local catalog validation through `scripts/validate_catalog.py`
- CI validation for catalog, schema, enum, fixture, validator, and workflow changes

This repository does **not** contain official ESA/EU schema authority, legal applicability decisions, official regulatory interpretation, supervisory submission packaging, source-system evidence, proof-run execution, proof-engine package generation, offline verifier implementation, public website presentation, customer evidence custody, or production compliance claims.

Reports against systems outside this repository are out of scope here and should be directed to the appropriate project or vendor.

## Supported surface

Only the current `main` branch of this repository is supported and receives security fixes. Older branches, tags, and historical releases are not patched.

## Reporting a vulnerability

Please report suspected vulnerabilities privately through one of the following channels:

- **Preferred:** GitHub Private Vulnerability Reporting —
  <https://github.com/witnessops/witnessops-catalog-dora/security/advisories/new>
- **Alternative:** email <security@witnessops.com>

When reporting, please include:

- a description of the issue and its potential impact
- steps to reproduce, or a proof of concept
- the affected catalog row, schema, enum, fixture, validator path, workflow, or documentation boundary if known
- any relevant commit SHA or environment details

> **Do not use public GitHub issues, discussions, or pull requests to report suspected vulnerabilities.** Public reports can put users at risk before a fix is available.

## Acknowledgment window

We will acknowledge receipt of your report within **5 business days**. That acknowledgment confirms the report reached us; a full triage and impact assessment will follow.

## Disclosure handling

We prefer coordinated disclosure:

- We will work with you to validate the issue, assess impact, and prepare a fix.
- We ask for a reasonable embargo period while a fix is being prepared and rolled out. The exact length depends on severity and complexity, and we will agree it with you.
- Once a fix is available, we will publish an advisory describing the issue and its resolution.
- Reporters will be credited in the advisory unless they ask to remain anonymous.

## Examples of in-scope issues

The following are examples of issues that may be security-relevant in this repository:

- invalid fixtures validate successfully
- valid fixtures stop proving intended behavior because validator coverage is weakened
- schema accepts undeclared fields that can smuggle legal, proof, evidence, or authority claims
- enum/schema drift is no longer detected
- regulatory timer fields allow ambiguous or unsupported timing claims
- DORA mapping schema allows disallowed incident surfaces under exact single-pillar incident mappings
- validator begins relying on implicit network fetches for local schemas
- catalog row includes secrets, customer evidence, confidential submission material, credentials, tokens, production targets, or private evidence paths
- docs or catalog language claims official regulatory authority, legal applicability, supervisory acceptance, or compliance proof without a named mechanism outside this repo

## Generally out of scope

The following are generally not considered reportable vulnerabilities for this repository unless a concrete security impact is demonstrated:

- missing generic web-app security headers, because this repo is not a web app
- social-engineering attacks targeting maintainers or operators
- denial-of-service via volumetric traffic flooding
- third-party dependency advisories already tracked by an automated advisory feed
- legal or compliance disagreements that do not identify a concrete schema, fixture, validator, or overclaim failure

If you believe one of the above has a concrete, demonstrable security impact in this repository, please still report it through the private channels above and explain the impact.
