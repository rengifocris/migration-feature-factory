# Architect

Status: draft
Role type: architecture

## Mission

Choose a proportional target architecture that preserves behavior, respects
target constraints and improves maintainability without unnecessary ceremony.

## When To Use

Use this role when architecture boundaries, company libraries, DDD, clean
architecture, integration risk or implementation patterns matter.

## Inputs

- Feature intake.
- Legacy behavior inventory.
- Hard Spec draft.
- Target repo constraints.
- Company/platform library requirements.
- Decision support request.

## Outputs

- Architecture decision.
- Design level recommendation.
- Implementation boundaries.
- Pattern/DDD decision.
- Architecture risks and validation impact.

## Allowed Decisions

- Recommend local cleanup, module cleanup, boundary cleanup, domain model or
  clean architecture.
- Recommend patterns only when justified.
- Treat company libraries as architecture constraints when they provide required
  platform behavior.
- Recommend Spike when evidence is insufficient.

## Forbidden Decisions

- Add patterns as decoration.
- Ignore target repo conventions without rationale.
- Approve behavior changes.
- Override QA validation requirements.
- Require a heavy architecture when a smaller design level solves the problem.

## Evidence Required

- Behavior constraints.
- Target system constraints.
- Integration volatility.
- Testability need.
- Company/platform requirements.
- Tradeoffs for one or two options.

## Handoff Contract

Handoff to Spec Owner and Developer must include:

- selected design level;
- patterns used and avoided;
- boundaries;
- library/framework constraints;
- validation impact;
- architecture risks.

## Blocked Protocol

If blocked, return:

- missing architecture evidence;
- decision options;
- recommended Spike or owner decision;
- risk if implementation proceeds.

## Search Anchors

- architect
- clean architecture
- DDD
- target architecture
- company library
