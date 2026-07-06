# Behavior Parity Plan - <Feature Name>

Status: draft
Feature ID: <feature-id>
Related package index: `migration-package-index.md`
Related behavior inventory: `legacy-behavior-inventory.md`
Sensitivity: public-safe-example | internal | confidential

## Purpose

Define how the team will prove the migrated feature preserves observable legacy
behavior.

## Parity Strategy

- Primary validation approach:
- Secondary validation approach:
- Manual evidence needed:
- Automation not practical because:

## Behavior-To-Evidence Matrix

| Behavior ID | Legacy Behavior | Target Evidence | Test Type | Status |
| --- | --- | --- | --- | --- |
| LB-01 | <behavior> | <test/check/evidence> | unit | pending |

## Test Levels

### Unit Tests

- Scope:
- What they prove:
- What they do not prove:

### Integration Tests

- Scope:
- Systems involved:
- Required test data:

### Contract / API Tests

- Endpoint or contract:
- Request fixtures:
- Response assertions:
- Error assertions:

### E2E / Workflow Tests

- User or system flow:
- Preconditions:
- Expected result:

### Golden-Master Or Fixture Tests

- Fixture source:
- Comparison rule:
- Allowed differences:

## Non-Functional Parity

- Performance:
- Reliability:
- Security/permissions:
- Observability/logs:
- Backward compatibility:

## Data Assertions

- Before state:
- Action:
- After state:
- Rollback/cleanup:

## Known Gaps

| Gap | Risk | Mitigation | Decision Needed |
| --- | --- | --- | --- |
| <gap> | <risk> | <mitigation> | yes / no |

## Validation Gate

- Minimum evidence before implementation:
- Minimum evidence before review:
- Minimum evidence before closeout:
- Owner:

## Recommendation

Recommended validation path:

- Option A:
- Option B:
- Recommendation:
- Rationale:

## Search Anchors

Terms people might search for:

- behavior parity
- golden master
- legacy behavior
- validation evidence
- <feature-name>
