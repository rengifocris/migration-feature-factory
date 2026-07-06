# Behavior Parity Plan - Fake Login Migration

Status: completed
Feature ID: FAKE-LOGIN-001
Related package index: `migration-package-index.md`
Related behavior inventory: `legacy-behavior-inventory.md`
Sensitivity: public-safe-example

## Purpose

Define how a target implementation would prove it preserves the fake legacy
login behavior.

## Parity Strategy

- Primary validation approach: contract/API tests for request and response parity.
- Secondary validation approach: integration test for audit and session side effects.
- Manual evidence needed: public example review only.
- Automation not practical because: no real target application exists in this repository.

## Behavior-To-Evidence Matrix

| Behavior ID | Legacy Behavior | Target Evidence | Test Type | Status |
| --- | --- | --- | --- | --- |
| LB-01 | active account login succeeds | EV-01 contract test and EV-05 E2E flow | contract | planned |
| LB-02 | unknown account or wrong passphrase returns stable 401 | EV-02 contract test | contract | planned |
| LB-03 | locked account returns 423 | EV-03 contract test | contract | planned |
| LB-04 | every attempt writes audit row | EV-04 integration test | integration | planned |
| LB-05 | five failures in fifteen minutes return 429 | EV-05 E2E flow | E2E | planned |

## Test Levels

### Unit Tests

- Scope: login policy decisions for success, invalid login, locked account and throttling.
- What they prove: domain rules are isolated from HTTP and persistence.
- What they do not prove: API response shape, cookie behavior or audit persistence.

### Integration Tests

- Scope: account repository, session writer and audit writer adapters.
- Systems involved: target service and fake in-memory persistence.
- Required test data: active, locked and throttled demo accounts.

### Contract / API Tests

- Endpoint or contract: `POST /demo/login`.
- Request fixtures: active account, unknown account, wrong passphrase and locked account.
- Response assertions: status code, result code and session cookie presence.
- Error assertions: 401, 423 and 429 responses preserve legacy result codes.

### E2E / Workflow Tests

- User or system flow: five failed attempts followed by a throttled attempt.
- Preconditions: active demo account and clean failed-attempt count.
- Expected result: sixth attempt returns 429 and writes audit row.

### Golden-Master Or Fixture Tests

- Fixture source: fake legacy request and response examples.
- Comparison rule: compare status code, result code, cookie presence and audit outcome.
- Allowed differences: internal module names and target service log format.

## Non-Functional Parity

- Performance: no slower than legacy p95 target for this fake flow.
- Reliability: login attempt audit is not skipped on handled errors.
- Security/permissions: invalid login does not reveal whether account handle exists.
- Observability/logs: correlation ID remains available.
- Backward compatibility: request and response contract stays stable.

## Data Assertions

- Before state: no session row for the request correlation ID.
- Action: submit login request.
- After state: session row exists only for LB-01; audit row exists for every behavior.
- Rollback/cleanup: delete fake session and audit rows after test.

## Known Gaps

| Gap | Risk | Mitigation | Decision Needed |
| --- | --- | --- | --- |
| No executable target app in this public repo | low | treat evidence as planned example evidence | no |

## Validation Gate

- Minimum evidence before implementation: behavior inventory and parity plan accepted.
- Minimum evidence before review: contract and integration test results.
- Minimum evidence before closeout: package check and public-safety scan.
- Owner: qa-reviewer.

## Recommendation

Recommended validation path:

- Option A: unit tests only.
- Option B: contract tests plus integration side-effect checks.
- Recommendation: choose Option B.
- Rationale: login behavior crosses API, session and audit boundaries.

## Search Anchors

Terms people might search for:

- behavior parity
- fake login
- audit evidence
- throttling flow
- session behavior
