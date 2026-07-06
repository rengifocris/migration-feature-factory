# User Story - <Migration Slice>

Status: draft
Related package index: `../core/migration-package-index.md`
Related Epic: `<path-or-none>`
Related Hard Spec: `<path-or-none>`
Language policy: English only | match target project
Sensitivity: public-safe-example | internal | confidential

## Summary

<Short description of the migrated behavior and expected value.>

## Business Context

- Legacy behavior being preserved:
- User, system or stakeholder affected:
- Target capability:
- Value of migration:

## User Story

As a <role/persona/system>,
I want <legacy behavior or capability preserved in the target>,
so that <business or operational value>.

## Scope

### In Scope

- <behavior or capability>

### Out Of Scope

- <explicit non-goal>

## Legacy Behavior Contract

| Behavior ID | Legacy Behavior | Source Evidence | Must Preserve |
| --- | --- | --- | --- |
| LB-01 | <behavior> | `<path/reference>` | yes |

## Acceptance Criteria

### Scenario 1: <preserved behavior>

Given <legacy-equivalent context>
When <action/event>
Then <target system preserves expected result>

### Scenario 2: <error or alternate behavior>

Given <legacy-equivalent context>
When <action/event>
Then <target system preserves expected result>

## Behavior Changes

- Approved behavior changes:
- Behavior changes explicitly not approved:
- New-feature candidates to split:

## INVEST Check

- Independent:
- Negotiable:
- Valuable:
- Estimable:
- Small:
- Testable:

## Definition Of Ready

- [ ] Legacy behavior inventory exists or required gaps are explicit.
- [ ] Behavior parity plan exists.
- [ ] Acceptance criteria are written in testable form.
- [ ] Architecture constraints are known or a Spike is created.
- [ ] Dependencies and non-goals are explicit.

## Definition Of Done

- [ ] Hard Spec covers every acceptance criterion.
- [ ] Parity evidence exists or gaps are accepted.
- [ ] Review/QA gate is completed.
- [ ] Package index traceability is updated.
- [ ] No unapproved observable behavior change is included.

## Technical Notes

- Affected components:
- API/contracts:
- Data behavior:
- Permissions/security:
- Observability:
- Compatibility:

## Testing Suggestions

- Unit tests:
- Integration tests:
- Contract/API tests:
- E2E/regression tests:
- Negative/error scenarios:
- Evidence to capture:

## Risks / Open Questions

| Item | Owner | Impact | Status |
| --- | --- | --- | --- |
| <risk/question> | <role> | <impact> | open |

## Related Artifacts

- Package index:
- Legacy behavior inventory:
- Behavior parity plan:
- Hard Spec:
- Architecture decision:

## Search Anchors

Terms people might search for:

- migration user story
- behavior parity
- acceptance criteria
- <feature-name>
