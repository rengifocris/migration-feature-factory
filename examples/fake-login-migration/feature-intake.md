# Feature Intake - Fake Login Migration

Status: completed
Feature ID: FAKE-LOGIN-001
Related package index: `migration-package-index.md`
Sensitivity: public-safe-example

## Summary

Move a fake legacy login flow from Legacy Portal Auth into Target Identity
Service while preserving all observable responses, session behavior, audit
records and throttling rules.

## Migration Request

- Original ask: migrate the fake login behavior into a cleaner service boundary.
- Desired outcome: target service preserves login results while internal design improves.
- Legacy system: Legacy Portal Auth.
- Target system: Target Identity Service.
- Primary users or consumers: demo portal users and demo API clients.
- Business/domain process: authenticate a returning demo user and start a session.

## Scope

### In Scope

- Active account successful login.
- Unknown account and wrong passphrase failure behavior.
- Locked account behavior.
- Audit record for every login attempt.
- Failed-attempt throttling after five failures in fifteen minutes.

### Out Of Scope

- Registration.
- Passphrase reset.
- Multi-factor login.
- Real account data.
- Real product names or client context.

## Known Entry Points

| Type | Name / Path | Notes |
| --- | --- | --- |
| API | `POST /demo/login` | Primary login endpoint. |
| UI | Demo login form | Submits the same fields as the API. |
| Job | none | Login has no scheduled job. |
| Event | `demo.login.attempted` | Internal audit event after each attempt. |

## Known Data And Integrations

- Data read: demo account status, passphrase verifier and failed-attempt count.
- Data written: demo session row, failed-attempt count and audit row.
- External integrations: none.
- Internal libraries/frameworks: target service web framework and repository layer.
- Configuration or feature flags: fifteen-minute failed-attempt window.

## Constraints

- Behavior constraints: preserve status codes, error codes, session creation and audit side effects.
- Architecture constraints: isolate login policy from HTTP handling and persistence.
- Company/platform constraints: none in this fake example.
- Security/privacy constraints: public-safe fake data only.
- Operational constraints: no real deployment or production migration.

## Initial Classification

- [x] Behavior-preserving migration
- [ ] Migration plus architecture constraint
- [ ] Migration plus possible new feature
- [ ] New feature, not migration
- [ ] Unknown / Spike needed

## Assumptions

- Legacy response examples are represented by fake fixtures in this package - Confidence: high.
- Target service can support a small domain service and ports - Confidence: high.
- No real account data is needed for this public example - Confidence: high.

## Risks

| Risk | Impact | Mitigation |
| --- | --- | --- |
| Fake behavior may look too generic. | Medium | Keep behavior IDs, evidence IDs and traceability explicit. |
| Readers may infer a real system. | Low | Use fake system names and public-safe wording throughout. |

## Open Questions

| Question | Owner | Blocks | Status |
| --- | --- | --- | --- |
| Is any real system context needed? | migration-orchestrator | none | closed: no |

## Next Gate

Legacy behavior discovery is complete in `legacy-behavior-inventory.md`.
