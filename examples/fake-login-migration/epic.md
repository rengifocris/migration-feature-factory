# Epic - Fake Login Migration

Status: completed
Related package index: `migration-package-index.md`
Language policy: English only
Sensitivity: public-safe-example

## Summary

Move the fake login capability from Legacy Portal Auth to Target Identity
Service while preserving observable behavior and showing the full factory flow.

## Business Outcome

- Target outcome: demonstrate an end-to-end migration package.
- Why now: EPIC-07 needs a public-safe example before release readiness.
- Expected value: new users can inspect a complete package without private context.
- Success evidence: `factory_check.py` passes and all artifacts are linked.

## Problem Statement

- Current pain or opportunity: the factory is abstract without an example.
- Affected users, systems or stakeholders: maintainers and first-time users.
- Legacy process/domain: fake user login.
- Target process/domain: fake identity service login.

## Migration Scope

### In Scope

- Successful login.
- Invalid login.
- Locked account.
- Audit record.
- Failed-attempt throttling.

### Out Of Scope

- Real code migration.
- Real account data.
- Registration and passphrase reset.
- Multi-factor login.

## Behavior Preservation Principle

- Legacy behavior source: `legacy-behavior-inventory.md`.
- Behavior that must remain observable: LB-01 through LB-05.
- Behavior changes that require separate approval: any new login result, changed status code or changed side effect.

## Architecture Direction

- Target architecture intent: boundary cleanup around login policy.
- Known target constraints: preserve API contract and audit side effect.
- Company/platform libraries or frameworks: none in this fake example.
- Explicitly avoid: full platform rewrite and decorative abstractions.

## Candidate Child Stories

| ID | Story Candidate | Migration Value | Notes |
| --- | --- | --- | --- |
| US-FAKE-LOGIN-01 | Preserve fake login behavior in Target Identity Service. | Shows product-facing migration story. | Implemented in `user-story.md`. |

## Candidate Spikes

| ID | Uncertainty | Why It Matters | Expected Decision |
| --- | --- | --- | --- |
| SP-FAKE-LOGIN-01 | Is full clean architecture needed? | Avoid overbuilding the example. | Boundary cleanup is enough. |

## Dependencies

- Legacy system access: fake behavior inventory only.
- Target system access: not required.
- Test data: fake fixtures only.
- Product or architecture approvals: ADR-01 accepted.
- External integrations: none.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Example becomes too large. | Medium | Keep one migration slice with five behaviors. |
| Example looks like a real system. | Low | Use fake names and generic behavior. |

## Definition Of Ready

- [x] Migration outcome is clear.
- [x] Scope and non-goals are explicit.
- [x] Candidate child story exists.
- [x] Legacy behavior discovery path is known.

## Definition Of Done

- [x] All required package artifacts exist.
- [x] Behavior IDs map to validation evidence.
- [x] Architecture decision is linked.
- [x] Package passes factory check.
