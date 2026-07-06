# User Story - Fake Login Migration

Status: completed
Related package index: `migration-package-index.md`
Related Epic: `epic.md`
Related Hard Spec: `hard-spec.md`
Language policy: English only
Sensitivity: public-safe-example

## Summary

Preserve the fake login behavior in Target Identity Service so demo clients see
the same outcomes as Legacy Portal Auth.

## Business Context

- Legacy behavior being preserved: LB-01 through LB-05.
- User, system or stakeholder affected: demo portal user and demo API client.
- Target capability: login through Target Identity Service.
- Value of migration: demonstrates behavior parity through a complete package.

## User Story

As a demo API client,
I want login outcomes to stay the same after the migration,
so that callers can move to Target Identity Service without changing their behavior.

## Scope

### In Scope

- Successful login for active account.
- Invalid login response.
- Locked account response.
- Audit side effect.
- Failed-attempt throttling.

### Out Of Scope

- New login factors.
- Registration.
- Passphrase reset.
- Real account data.

## Legacy Behavior Contract

| Behavior ID | Legacy Behavior | Source Evidence | Must Preserve |
| --- | --- | --- | --- |
| LB-01 | active account login succeeds | `legacy-behavior-inventory.md` | yes |
| LB-02 | invalid login returns stable 401 | `legacy-behavior-inventory.md` | yes |
| LB-03 | locked account returns 423 | `legacy-behavior-inventory.md` | yes |
| LB-04 | every attempt writes audit row | `legacy-behavior-inventory.md` | yes |
| LB-05 | failed-attempt throttle returns 429 | `legacy-behavior-inventory.md` | yes |

## Acceptance Criteria

### Scenario 1: Active Account Login

Given an active demo account
When the client submits the matching passphrase to `POST /demo/login`
Then Target Identity Service returns 200 with `LOGIN_OK` and a session cookie.

### Scenario 2: Invalid Login

Given an unknown account handle or wrong passphrase
When the client submits the login request
Then Target Identity Service returns 401 with `INVALID_CREDENTIALS` and no session cookie.

### Scenario 3: Locked Account

Given a locked demo account
When the client submits the login request
Then Target Identity Service returns 423 with `ACCOUNT_LOCKED` and no session cookie.

### Scenario 4: Audit Record

Given any login attempt
When Target Identity Service finishes the attempt
Then it records an audit row with account handle, outcome and correlation ID.

### Scenario 5: Failed-Attempt Throttle

Given five failed attempts for the same account within fifteen minutes
When the client submits another login request
Then Target Identity Service returns 429 with `LOGIN_THROTTLED` and no session cookie.

## Behavior Changes

- Approved behavior changes: none.
- Behavior changes explicitly not approved: status code changes, result code changes, audit omission and session side-effect changes.
- New-feature candidates to split: registration, passphrase reset and multi-factor login.

## INVEST Check

- Independent: yes, one login migration slice.
- Negotiable: no behavior changes without approval.
- Valuable: yes, shows a complete factory example.
- Estimable: yes, five behavior IDs.
- Small: yes, one endpoint and one UI flow.
- Testable: yes, contract and integration evidence are defined.

## Definition Of Ready

- [x] Legacy behavior inventory exists or required gaps are explicit.
- [x] Behavior parity plan exists.
- [x] Acceptance criteria are written in testable form.
- [x] Architecture constraints are known or a Spike is created.
- [x] Dependencies and non-goals are explicit.

## Definition Of Done

- [x] Acceptance criteria map to HS-01 through HS-05.
- [x] Behavior parity plan maps each behavior to evidence.
- [x] Review/QA brief records validation status.
- [x] Closeout records residual risk.
