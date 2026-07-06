# Behavior Parity Reference

Use this reference when defining or reviewing migration equivalence.

## Behavior Contract

A legacy behavior is observable when a user, client, integration, job, database
state, event stream, permission check, error response or operational signal can
notice it.

Give each behavior a stable ID such as `LB-01`. Keep the ID consistent across:

- legacy behavior inventory;
- behavior parity plan;
- User Story acceptance criteria;
- Hard Spec requirements;
- implementation brief;
- review/QA evidence;
- closeout.

## Evidence Levels

| Evidence | Use When |
| --- | --- |
| Unit test | Isolated domain rule or pure transformation. |
| Integration test | Behavior depends on persistence, framework wiring or internal services. |
| Contract/API test | Request/response shape, status codes, headers or error semantics matter. |
| E2E/workflow test | User or system flow spans multiple boundaries. |
| Golden-master or fixture comparison | Legacy output can be captured and replayed safely. |
| Data assertion | State changes are part of the contract. |
| Manual evidence | Automation is impractical and the residual risk is accepted. |

Unit tests alone are not enough when the contract includes API behavior,
permissions, integrations, error semantics, events, jobs, logs or side effects.

## Parity Mapping

Every behavior in the inventory should map to:

- at least one acceptance criterion or documented non-goal;
- at least one Hard Spec requirement;
- at least one validation evidence item or an explicit gap;
- a review/QA status.

If a behavior is intentionally not migrated, document the decision and approval.

## Allowed Differences

Internal differences are acceptable when observable behavior is unchanged:

- clearer module boundaries;
- improved naming and guard clauses;
- target-framework idioms;
- clearer test boundaries;
- cleaner domain rules;
- stronger observability that does not alter public behavior.

Observable differences require separate approval:

- new user-visible capability;
- changed response payload, status, text or error semantics;
- changed permission behavior;
- changed side effect;
- changed timing or retry behavior that callers depend on.

## Validation Recommendation

Recommend the lowest validation level that proves the risky behavior. Escalate
from unit to integration, contract or E2E evidence when behavior crosses a
boundary.
