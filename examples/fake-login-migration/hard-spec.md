# Hard Spec - Fake Login Migration

Status: completed
Related package index: `migration-package-index.md`
Related Epic/User Story: `user-story.md`
Related behavior inventory: `legacy-behavior-inventory.md`
Related parity plan: `behavior-parity-plan.md`
Language policy: English only
Sensitivity: public-safe-example

## Objective

- Build or modify: Target Identity Service login endpoint and supporting domain service.
- Business outcome supported: preserve fake legacy login behavior.
- Legacy behavior preserved: LB-01 through LB-05.
- Non-goal summary: no new login features and no real system integration.

## Scope

### In Scope

- `POST /demo/login` behavior.
- Login policy decisions.
- Session creation on success.
- Audit row for every attempt.
- Failed-attempt throttling.

### Out Of Scope

- UI redesign.
- Registration.
- Passphrase reset.
- Multi-factor login.
- Real data migration.

## Functional Requirements

| ID | Requirement | Legacy Behavior Mapping | Notes |
| --- | --- | --- | --- |
| HS-01 | Return 200, `LOGIN_OK` and session cookie for active account with matching passphrase. | LB-01 | Preserve response shape. |
| HS-02 | Return 401 and `INVALID_CREDENTIALS` for unknown account or wrong passphrase. | LB-02 | Do not reveal which field failed. |
| HS-03 | Return 423 and `ACCOUNT_LOCKED` for locked account. | LB-03 | No session cookie. |
| HS-04 | Record an audit row for every login attempt. | LB-04 | Include outcome and correlation ID. |
| HS-05 | Return 429 and `LOGIN_THROTTLED` after five failures in fifteen minutes. | LB-05 | No session cookie. |

## Non-Functional Requirements

- Security/privacy: public-safe fake data only; invalid login does not reveal account existence.
- Performance: preserve fake p95 target from legacy fixtures.
- Reliability: audit row must be written for handled outcomes.
- Observability: keep correlation ID through policy and adapter calls.
- Compatibility: request and response contract stays stable.
- Operability: throttling window is configurable.

## Data And Contracts

- Inputs: account handle, passphrase and correlation ID.
- Outputs: result code, HTTP status and optional session cookie.
- APIs/events: `POST /demo/login`, `demo.login.attempted`.
- Data model: account record, session record, failed-attempt counter and audit row.
- Validation rules: account handle and passphrase are required.
- Error cases: invalid login, locked account and throttled login.
- Backward compatibility: status code and result code match fake legacy contract.

## Process Behavior

- Main flow: validate request, load account, evaluate policy, write side effects and return response.
- Alternate flows: invalid login, locked account and throttled login.
- Empty/error states: missing fields use the same invalid login response for this fake example.
- Permissions/roles: demo user and demo API client only.
- Side effects: session row on success, audit row always, failed-attempt count on failure.

## Architecture / Implementation Boundaries

- Components likely touched: login controller, login domain service, account port, session port and audit port.
- Integration points: account repository, session repository and audit writer.
- Company/platform libraries: none in this fake example.
- Reuse existing target patterns: thin controller and dependency-injected adapters.
- Explicitly avoid: direct persistence calls from controller and full platform rewrite.
- Design level: boundary cleanup.

## Decision Support

| Decision | Option A | Option B | Recommendation | Artifact |
| --- | --- | --- | --- | --- |
| Target design level | local controller rewrite | boundary cleanup | boundary cleanup | `architecture-decision.md` |

## Edge Cases

| Edge Case | Expected Behavior | Evidence |
| --- | --- | --- |
| Unknown account | 401 `INVALID_CREDENTIALS` | EV-02 |
| Wrong passphrase | 401 `INVALID_CREDENTIALS` | EV-02 |
| Locked account | 423 `ACCOUNT_LOCKED` | EV-03 |
| Sixth failed attempt | 429 `LOGIN_THROTTLED` | EV-05 |

## Validation Contract

| Requirement | Evidence |
| --- | --- |
| HS-01 | EV-01 and EV-05 |
| HS-02 | EV-02 |
| HS-03 | EV-03 |
| HS-04 | EV-04 |
| HS-05 | EV-05 |
