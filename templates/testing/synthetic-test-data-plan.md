# Synthetic Test Data Plan - <Feature Or Foundation>

Status: draft
Sensitivity: public-safe-example | internal | confidential
Related package index: `<path>`
Related behavior inventory: `<path>`
Related parity plan: `<path>`

## Purpose

Define deterministic synthetic data for behavior-preserving migration tests.

Synthetic data is not a copy of production data. It is a curated set of small
fixtures that prove accepted behavior, edge cases, error handling and model
mapping.

## Data Principles

- Use fake values only.
- Keep fixture size small.
- Name fixtures by scenario and behavior purpose.
- Pair valid and invalid variants.
- Record the reason each fixture exists.
- Link fixtures to `LB-*`, `AC-*`, `HS-*` and `EV-*` IDs.

## Fixture Catalog

| Fixture ID | Profile | Purpose | Related IDs | Owner | Status |
| --- | --- | --- | --- | --- | --- |
| FX-001 | happy-minimal | baseline valid behavior | LB-<id>, EV-<id> | QA reviewer | draft |
| FX-002 | happy-complete | full enrichment behavior | LB-<id>, EV-<id> | QA reviewer | draft |
| FX-003 | edge-empty | empty or missing optional data | LB-<id>, EV-<id> | QA reviewer | draft |
| FX-004 | edge-boundary-values | limits, dates, identifiers and enums | LB-<id>, EV-<id> | QA reviewer | draft |
| FX-005 | bad-invalid-schema | invalid payload shape | LB-<id>, EV-<id> | QA reviewer | draft |
| FX-006 | bad-upstream-error | external failure behavior | LB-<id>, EV-<id> | QA reviewer | draft |
| FX-007 | security-denied | permission behavior | LB-<id>, EV-<id> | QA reviewer | draft |

## Golden-Master Snapshots

| Snapshot | Observable Contract | Source Fixture | Target Fixture | Acceptance Gate |
| --- | --- | --- | --- | --- |
| GM-001 | <API response / event / output> | FX-<id> | FX-<id> | QA review |

Rules:

- Snapshot only externally observable behavior.
- Do not snapshot private generated DTO internals unless they are the public
  contract.
- Update snapshots only through a classified change request.

## Negative Cases

| Case | Expected Behavior | Evidence |
| --- | --- | --- |
| invalid input | <error code/message contract> | EV-<id> |
| missing source record | <not found behavior> | EV-<id> |
| upstream timeout | <timeout/retry/fallback behavior> | EV-<id> |
| malformed upstream payload | <defensive parsing behavior> | EV-<id> |

## Review Gate

Before closeout:

- every accepted fixture has an owner and evidence ID;
- every changed fixture is linked to a change request;
- every unsupported fixture is listed as residual risk.

## Search Anchors

- synthetic test data
- parity fixtures
- golden master snapshots
- happy edge bad cases
