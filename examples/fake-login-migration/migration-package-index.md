# Migration Package Index - Fake Login Migration

Status: completed
Sensitivity: public-safe-example
Feature ID: FAKE-LOGIN-001
Legacy system: Legacy Portal Auth
Target system: Target Identity Service
Owner: migration-orchestrator
Last updated: 2026-07-06

## Purpose

Demonstrate how the factory preserves a fake legacy login flow while moving it
into a cleaner target service boundary.

## Current Status

- Lifecycle state: validated
- Current gate: closeout
- Last completed gate: review-and-qa
- Next action: use this example as the baseline package for EPIC-08 release checks
- Blocked by: none

## Package Artifacts

| Artifact | Status | Path | Owner | Last Updated |
| --- | --- | --- | --- | --- |
| Feature Intake | completed | `feature-intake.md` | migration-orchestrator | 2026-07-06 |
| Legacy Behavior Inventory | completed | `legacy-behavior-inventory.md` | legacy-analyst | 2026-07-06 |
| Behavior Parity Plan | completed | `behavior-parity-plan.md` | qa-reviewer | 2026-07-06 |
| Change Intake | completed | `change-intake.md` | migration-orchestrator | 2026-07-06 |
| Epic | completed | `epic.md` | product-owner-business-analyst | 2026-07-06 |
| User Story | completed | `user-story.md` | product-owner-business-analyst | 2026-07-06 |
| Hard Spec | completed | `hard-spec.md` | spec-owner | 2026-07-06 |
| Spike | completed | `spike.md` | spec-owner | 2026-07-06 |
| Architecture Decision | completed | `architecture-decision.md` | architect | 2026-07-06 |
| Implementation Brief | completed | `implementation-brief.md` | developer | 2026-07-06 |
| Review / QA | completed | `review-qa.md` | qa-reviewer | 2026-07-06 |
| Closeout | completed | `closeout.md` | migration-orchestrator | 2026-07-06 |

## Traceability Matrix

| Source | ID | Requirement / Behavior | Target Artifact | Validation Evidence | Status |
| --- | --- | --- | --- | --- | --- |
| Legacy behavior inventory | LB-01 | Active account login returns a successful session result. | `user-story.md#acceptance-criteria`, `hard-spec.md#functional-requirements` | EV-01 contract test and EV-05 E2E test | validated |
| Legacy behavior inventory | LB-02 | Unknown account or wrong passphrase returns the same 401 response without revealing which field failed. | `user-story.md#acceptance-criteria`, `hard-spec.md#functional-requirements` | EV-02 contract test | validated |
| Legacy behavior inventory | LB-03 | Locked account returns 423 and no session result. | `hard-spec.md#functional-requirements` | EV-03 contract test | validated |
| Legacy behavior inventory | LB-04 | Every login attempt writes an audit record with outcome and correlation ID. | `hard-spec.md#data-and-contracts` | EV-04 integration test | validated |
| Legacy behavior inventory | LB-05 | Five failed attempts for the same account within fifteen minutes return 429. | `hard-spec.md#process-behavior` | EV-05 E2E test | validated |

Status values: `pending`, `planned`, `validated`, `gap`, `accepted-risk`,
`superseded`.

## Decision Log

| Date | ID | Decision | Options Considered | Recommendation | Artifact Updated |
| --- | --- | --- | --- | --- | --- |
| 2026-07-06 | ADR-01 | Use boundary cleanup with a small login domain service and ports for account lookup, session writing and audit recording. | Local controller rewrite; boundary cleanup | Boundary cleanup | `architecture-decision.md` |

## Change Log

| Date | ID | Change | Classification | Artifacts Updated | Decision |
| --- | --- | --- | --- | --- | --- |
| 2026-07-06 | CHG-01 | Keep the example fully fake and public-safe. | Target architecture constraint | all artifacts | accepted |
| 2026-07-06 | CHG-02 | Include a completed spike artifact that documents why no uncertainty blocks implementation. | Behavior-preserving improvement | `spike.md`, `implementation-brief.md` | accepted |

## Open Questions

| Question | Owner | Blocks | Status | Needed By |
| --- | --- | --- | --- | --- |
| None | migration-orchestrator | none | closed | 2026-07-06 |

## Risks

| ID | Risk | Impact | Mitigation | Status |
| --- | --- | --- | --- | --- |
| R-01 | Readers may treat fake endpoint names as product guidance. | Low | State that all systems and examples are fake. | mitigated |

## Validation Summary

- Unit tests: EV-01 login policy examples planned in target repo.
- Integration tests: EV-04 audit persistence contract planned in target repo.
- Contract/API tests: EV-01, EV-02 and EV-03 define request and response parity.
- E2E tests: EV-05 defines failed-attempt throttling parity.
- Manual evidence: artifacts reviewed for public-safe fake names.
- Not validated: no real application code exists in this public example.

## Context Pack

- Short summary: fake login migration package demonstrating all V0 factory artifacts.
- Key decisions: ADR-01 boundary cleanup; no full platform rewrite.
- Current blockers: none.
- Files/artifacts to inspect first: `feature-intake.md`, `legacy-behavior-inventory.md`, `behavior-parity-plan.md`, `hard-spec.md`, `closeout.md`.
- Next prompt: continue with EPIC-08 release readiness and public-safety checklist.

## Traceability Rules

- Every discovered legacy behavior maps to validation evidence or a documented gap.
- Every acceptance criterion maps to Hard Spec coverage.
- Every Hard Spec requirement maps to validation evidence or accepted risk.
- Every architecture constraint maps to a decision or implementation boundary.
- Every change request is classified and recorded in the change log.
- Superseded IDs are not reused.

## Consistency Checklist

- [x] Every discovered legacy behavior maps to validation evidence or a documented gap.
- [x] Every acceptance criterion maps to Hard Spec coverage.
- [x] Every Hard Spec requirement maps to validation evidence.
- [x] Every architecture constraint maps to a decision or implementation boundary.
- [x] Every change request is classified.
- [x] Every blocker has an owner and next action.
- [x] Closeout states what changed, what did not change and residual risk.

## Search Anchors

Terms people might search for:

- fake login migration
- demo login flow
- Legacy Portal Auth
- Target Identity Service
- behavior parity example
