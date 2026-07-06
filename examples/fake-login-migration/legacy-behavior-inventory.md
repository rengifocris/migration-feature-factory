# Legacy Behavior Inventory - Fake Login Migration

Status: completed
Feature ID: FAKE-LOGIN-001
Related package index: `migration-package-index.md`
Sensitivity: public-safe-example

## Purpose

Capture observable fake legacy login behavior as the migration contract.

## Source Systems Inspected

| Source | Type | What Was Inspected | Evidence |
| --- | --- | --- | --- |
| Legacy Portal Auth fixture | docs | Fake request and response examples | EV-01, EV-02, EV-03 |
| Legacy audit fixture | docs | Fake audit row shape | EV-04 |
| Legacy login journey fixture | docs | Fake failed-attempt journey | EV-05 |

## Entry Points

| Type | Entry Point | Request / Trigger | Response / Result |
| --- | --- | --- | --- |
| API | `POST /demo/login` | account handle and passphrase | session result or stable error response |
| UI | Demo login form | submit account handle and passphrase | same result as API, rendered in demo UI |
| Job | none | none | none |
| Event | `demo.login.attempted` | every login attempt | audit row is recorded |

## Main Flow

1. User submits account handle and passphrase.
2. Legacy system checks account existence and active status.
3. Legacy system checks passphrase verifier.
4. Legacy system creates a session row when the account is active and the passphrase matches.
5. Legacy system writes an audit row with outcome and correlation ID.
6. API returns 200 with result code `LOGIN_OK` and a session cookie.

## Alternate Flows

| Flow | Trigger | Legacy Behavior | Notes |
| --- | --- | --- | --- |
| Unknown account | account handle is not found | returns 401 with `INVALID_CREDENTIALS` | same response as wrong passphrase |
| Wrong passphrase | verifier does not match | returns 401 with `INVALID_CREDENTIALS` | no session row |
| Locked account | account status is locked | returns 423 with `ACCOUNT_LOCKED` | no session row |
| Failed-attempt throttle | five failures in fifteen minutes | returns 429 with `LOGIN_THROTTLED` | no session row |

## Validation Rules

| Rule | Input / Condition | Legacy Result | Evidence |
| --- | --- | --- | --- |
| LB-01 | active account and matching passphrase | 200, `LOGIN_OK`, session cookie | EV-01 |
| LB-02 | unknown account or wrong passphrase | 401, `INVALID_CREDENTIALS`, no session cookie | EV-02 |
| LB-03 | locked account | 423, `ACCOUNT_LOCKED`, no session cookie | EV-03 |
| LB-04 | any login attempt | audit row with account handle, outcome and correlation ID | EV-04 |
| LB-05 | five failures in fifteen minutes | 429, `LOGIN_THROTTLED`, no session cookie | EV-05 |

## Permissions And Roles

| Actor / Role | Allowed Behavior | Denied Behavior | Evidence |
| --- | --- | --- | --- |
| Demo user | submit login request for own account handle | inspect another account state | EV-02 |
| Demo API client | submit login request | bypass throttling rule | EV-05 |

## Data Behavior

- Reads: account handle, account status, passphrase verifier and failed-attempt count.
- Writes: session row for successful login, failed-attempt count for failed login, audit row for every attempt.
- Updates: failed-attempt count resets after successful login.
- Deletes: none.
- Transactions: session creation and audit recording are committed together for success.
- Idempotency: repeated failed attempts are recorded separately.
- Concurrency: failed-attempt count uses atomic increment semantics.

## Error Behavior

| Scenario | Status / Error | Body / Message | Side Effect | Evidence |
| --- | --- | --- | --- | --- |
| Unknown account | 401 | `INVALID_CREDENTIALS` | audit row | EV-02 |
| Wrong passphrase | 401 | `INVALID_CREDENTIALS` | failed-attempt count and audit row | EV-02 |
| Locked account | 423 | `ACCOUNT_LOCKED` | audit row | EV-03 |
| Throttled account | 429 | `LOGIN_THROTTLED` | audit row | EV-05 |

## Side Effects

- Events emitted: `demo.login.attempted`.
- Notifications: none.
- Logs: correlation ID and outcome only.
- Metrics: success, failure, locked and throttled counts.
- External calls: none.
- Persistence side effects: session, failed-attempt and audit rows.

## Existing Tests Or Fixtures

| Test / Fixture | What It Proves | Reuse For Parity |
| --- | --- | --- |
| EV-01 | successful login contract | yes |
| EV-02 | invalid login contract | yes |
| EV-03 | locked account contract | yes |
| EV-04 | audit side effect | yes |
| EV-05 | throttling flow | yes |

## Known Gaps

No behavior gaps are open for this public fake example.
