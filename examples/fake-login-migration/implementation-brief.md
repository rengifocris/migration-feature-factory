# Implementation Brief - Fake Login Migration

Status: approved-for-implementation
Message type: implementation_brief
Target role: developer
Related package index: `migration-package-index.md`
Sensitivity: public-safe-example
Context budget: small

## User Spec

- Original ask: provide a public fake example of a complete migration package.
- Desired outcome: demonstrate behavior-preserving migration into a cleaner architecture.
- Business/user value: maintainers and users can inspect a working factory package.
- Non-goals: real code, real accounts, registration, passphrase reset and multi-factor login.

## Product And Spec Inputs

- Epic: `epic.md`.
- User Story: `user-story.md`.
- Hard Spec: `hard-spec.md`.
- Spike outcome: `spike.md`.
- Architecture decision: `architecture-decision.md`.
- Behavior inventory: `legacy-behavior-inventory.md`.
- Parity plan: `behavior-parity-plan.md`.
- Acceptance criteria source: `user-story.md#acceptance-criteria`.
- Definition of Done source: `user-story.md#definition-of-done`.

## Scope Contract

### In Scope

- Implement the target design for LB-01 through LB-05 in a hypothetical target repo.
- Add unit, contract, integration and E2E checks described in the parity plan.
- Preserve response result codes and session side effects.

### Out Of Scope

- Real target implementation in this public repo.
- New login capabilities.
- Real external integrations.

### Assumptions

- Target repo has a web endpoint layer - Confidence: high.
- Target repo supports dependency injection or equivalent composition - Confidence: high.

## Behavior Contract

| Behavior ID | Legacy Behavior | Target Requirement | Evidence Expected |
| --- | --- | --- | --- |
| LB-01 | active account login succeeds | HS-01 | EV-01, EV-05 |
| LB-02 | invalid login returns stable 401 | HS-02 | EV-02 |
| LB-03 | locked account returns 423 | HS-03 | EV-03 |
| LB-04 | every attempt writes audit row | HS-04 | EV-04 |
| LB-05 | failed-attempt throttle returns 429 | HS-05 | EV-05 |

## Implementation Boundaries

- Components/files likely touched: login controller, login policy service, account port, session port, audit port and tests.
- Repo-local commands/conventions to follow: target repo commands, not defined in this public example.
- APIs/events/contracts: `POST /demo/login` and `demo.login.attempted`.
- Data/model changes: session row, failed-attempt counter and audit row.
- UX/process behavior: demo login form receives unchanged results.
- Company/platform libraries: none in this fake example.
- Reuse existing patterns: thin controller, explicit adapters and focused tests.
- Explicitly avoid: direct persistence calls from controller and hidden behavior changes.
- Design level: boundary cleanup.

## Inputs To Inspect

| Input | Why It Matters |
| --- | --- |
| `legacy-behavior-inventory.md` | Source of behavior contract. |
| `behavior-parity-plan.md` | Source of validation evidence. |
| `hard-spec.md` | Source of technical requirements. |
| `architecture-decision.md` | Source of target boundary decision. |

## Safety And Human Gates

- Sensitive data: use fake fixtures only.
- Destructive operations: none.
- Migrations/deploys: none.
- External sends: none.
- Approval required: product and QA acceptance before closeout.

## Validation Requirements

- Unit tests: login policy outcomes for LB-01 through LB-05.
- Integration/contract tests: API responses, session writer and audit writer.
- E2E/regression: failed-attempt throttling.
- Manual/artifact inspection: public-safety scan and package check.

## Evidence To Return

- Test command names and results.
- Files changed in target repo.
- Any behavior difference found.
- Residual risk and follow-up work.
