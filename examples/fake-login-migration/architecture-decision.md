# Architecture Decision - Fake Login Boundary Cleanup

Status: completed
Related package index: `migration-package-index.md`
Related Hard Spec: `hard-spec.md`
Sensitivity: public-safe-example

## Summary

Use boundary cleanup for the fake login migration: keep HTTP handling thin,
place login policy in a small domain service, and use ports for account lookup,
session writing and audit recording.

## Context

- Problem: fake legacy login behavior crosses API response, session and audit boundaries.
- Goal: preserve behavior while improving internal structure.
- Legacy behavior constraint: LB-01 through LB-05 must stay observable.
- Target architecture constraint: Target Identity Service should isolate policy from adapters.
- Non-goals: no full platform rewrite and no real code migration in this public example.

## Facts

- Login has five behavior IDs - Evidence: `legacy-behavior-inventory.md`.
- Audit side effect is part of the contract - Evidence: LB-04.
- Throttling requires stateful policy - Evidence: LB-05.

## Assumptions

- Target service can use dependency-injected ports - Confidence: high.
- Fake repository adapters are enough for example validation - Confidence: high.

## Constraints

- Technical: preserve request and response contract.
- Business: keep example small and readable.
- Security/privacy: no real account data.
- Operational: no deployment.
- Timeline/cost: one public example package.
- Company/platform libraries: none.

## Options Considered

### Option A - Local Controller Rewrite

- Description: implement behavior directly in the endpoint handler.
- Benefits: smallest number of files.
- Costs: mixes HTTP, policy and side effects.
- Risks: harder to validate audit and throttling parity.
- Validation impact: contract tests only may miss side-effect rules.
- Reversibility: easy, but risks learning the wrong pattern.

### Option B - Boundary Cleanup

- Description: thin controller, login policy service, account/session/audit ports.
- Benefits: protects behavior boundaries and supports focused tests.
- Costs: a few more names and interfaces.
- Risks: can become overbuilt if expanded beyond the login slice.
- Validation impact: supports unit, contract and integration evidence.
- Reversibility: straightforward because boundaries are small.

## Recommendation

Choose Option B.

Rationale:

- Login behavior crosses API, session and audit boundaries.
- The extra structure maps directly to parity evidence.
- It demonstrates clean architecture principles without a full architecture framework.

## Decision

We will model the target slice as boundary cleanup with a login policy service
and three ports: account lookup, session writer and audit writer.

## Design Level

- Selected level: boundary cleanup.
- Why this level is sufficient: it isolates the risky boundaries in this migration.
- Why a heavier level is not needed: the fake example has one endpoint and five behaviors.

## Pattern / DDD Decision

- Patterns used: ports and adapters for account, session and audit dependencies.
- DDD concepts used: login policy and account status as domain language.
- Patterns explicitly avoided: full layered platform, generic repository framework and broad event architecture.
- Rationale: use only the structure that protects behavior parity.

## Consequences

- Controller stays thin.
- Policy can be unit tested without HTTP or persistence.
- Side-effect adapters can be integration tested.
- Public example remains small enough to inspect.

## Validation Impact

- Unit evidence covers login policy.
- Contract evidence covers API parity.
- Integration evidence covers session and audit side effects.
- E2E evidence covers failed-attempt throttling.

## Search Anchors

- ADR-01
- boundary cleanup
- login policy
- ports and adapters
