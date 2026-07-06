# Migration Package Index - <Feature Name>

Status: draft
Sensitivity: public-safe-example | internal | confidential
Feature ID: <feature-id>
Legacy system: <legacy-system>
Target system: <target-system>
Owner: <owner-or-role>
Last updated: YYYY-MM-DD

## Purpose

<Short statement of what this migration package preserves and enables.>

## Current Status

- Lifecycle state: draft | discovery | parity-planning | spec-ready |
  implementation-ready | in-progress | blocked | validated | closed
- Current gate:
- Last completed gate:
- Next action:
- Blocked by:

## Package Artifacts

| Artifact | Status | Path | Owner | Last Updated |
| --- | --- | --- | --- | --- |
| Feature Intake | draft | `feature-intake.md` | <role> | YYYY-MM-DD |
| Legacy Behavior Inventory | draft | `legacy-behavior-inventory.md` | <role> | YYYY-MM-DD |
| Behavior Parity Plan | draft | `behavior-parity-plan.md` | <role> | YYYY-MM-DD |
| Change Intake | draft | `change-intake.md` | <role> | YYYY-MM-DD |
| User Story | not-started | `<path>` | <role> | YYYY-MM-DD |
| Hard Spec | not-started | `<path>` | <role> | YYYY-MM-DD |
| Architecture Decision | not-started | `<path>` | <role> | YYYY-MM-DD |
| Implementation Brief | not-started | `<path>` | <role> | YYYY-MM-DD |
| Review / QA | not-started | `<path>` | <role> | YYYY-MM-DD |
| Closeout | not-started | `<path>` | <role> | YYYY-MM-DD |

## Traceability Matrix

Use stable IDs such as `LB-01`, `AC-01`, `HS-01`, `ADR-01`, `EV-01`, `CHG-01`
and `R-01`.

| Source | ID | Requirement / Behavior | Target Artifact | Validation Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| `<legacy source>` | LB-01 | <behavior> | `<artifact section>` | EV-01 | pending |

Status values: `pending`, `planned`, `validated`, `gap`, `accepted-risk`,
`superseded`.

## Decision Log

| Date | ID | Decision | Options Considered | Recommendation | Artifact Updated |
| --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | ADR-01 | <decision> | <options> | <recommendation> | `<path>` |

## Change Log

| Date | ID | Change | Classification | Artifacts Updated | Decision |
| --- | --- | --- | --- | --- | --- |
| YYYY-MM-DD | CHG-01 | <change> | <classification> | `<paths>` | <decision> |

## Open Questions

| Question | Owner | Blocks | Status | Needed By |
| --- | --- | --- | --- | --- |
| <question> | <role> | <artifact/gate> | open | YYYY-MM-DD |

## Risks

| ID | Risk | Impact | Mitigation | Status |
| --- | --- | --- | --- | --- |
| R-01 | <risk> | <impact> | <mitigation> | open |

## Validation Summary

- Unit tests:
- Integration tests:
- Contract/API tests:
- E2E tests:
- Manual evidence:
- Not validated:

## Context Pack

- Short summary:
- Key decisions:
- Current blockers:
- Files/artifacts to inspect first:
- Next prompt:

## Traceability Rules

- Every discovered legacy behavior maps to validation evidence or a documented
  gap.
- Every acceptance criterion maps to Hard Spec coverage.
- Every Hard Spec requirement maps to validation evidence or accepted risk.
- Every architecture constraint maps to a decision or implementation boundary.
- Every change request is classified and recorded in the change log.
- Superseded IDs are not reused.

## Consistency Checklist

- [ ] Every discovered legacy behavior maps to validation evidence or a
      documented gap.
- [ ] Every acceptance criterion maps to Hard Spec coverage.
- [ ] Every Hard Spec requirement maps to validation evidence.
- [ ] Every architecture constraint maps to a decision or implementation
      boundary.
- [ ] Every change request is classified.
- [ ] Every blocker has an owner and next action.
- [ ] Closeout states what changed, what did not change and residual risk.

## Search Anchors

Terms people might search for:

- <feature-name>
- <legacy-name>
- <target-name>
- <ticket-id>
- <domain-term>
