# Factory Workflow

Status: draft
Audience: migration orchestrators, agents, maintainers

## Purpose

This workflow turns a vague migration request into an auditable migration
package that preserves legacy behavior and guides implementation in a cleaner
architecture.

## Workflow Summary

```text
1. Intake
2. Legacy behavior discovery
3. Behavior parity plan
4. Change intake and classification
5. Product/spec package
6. Architecture decision
7. Implementation brief
8. Review and QA gates
9. Closeout
```

The first V0 slice covers steps 1 through 4 plus the package index.

## Gate 1 - Intake

Goal: define the migration target and non-goals before analysis begins.

Inputs:

- feature name;
- legacy system;
- target system;
- known entry points;
- stakeholders;
- constraints;
- known risks.

Output:

- `feature-intake.md`;
- initial package status;
- initial open questions.

Stop when:

- the source or target system is ambiguous;
- sensitive/private material would be needed in the public repo;
- the request is actually a new feature and not a migration.

## Gate 2 - Legacy Behavior Discovery

Goal: capture observable legacy behavior as the migration contract.

Inspect:

- APIs;
- UI flows;
- jobs;
- events;
- data writes;
- validations;
- permissions;
- errors;
- side effects;
- logs or operational signals;
- existing tests and fixtures.

Output:

- `legacy-behavior-inventory.md`;
- source evidence list;
- unknowns and gaps.

Rule:

If behavior cannot be described or evidenced, do not implement. Create a Spike
or mark the gap explicitly.

## Gate 3 - Behavior Parity Plan

Goal: define how the team will prove the target behavior stayed equivalent.

Evidence options:

- unit tests for isolated domain rules;
- contract/API tests for external behavior;
- E2E tests for full user or integration flows;
- fixture comparisons;
- golden-master examples;
- before/after database assertions;
- manual evidence only when automation is not practical.

Output:

- `behavior-parity-plan.md`;
- acceptance-to-evidence mapping;
- known validation gaps.

Rule:

Unit tests alone are not enough when the legacy contract includes API behavior,
permissions, error semantics, integrations or side effects.

## Gate 4 - Change Intake And Classification

Goal: prevent new discoveries from silently changing migration scope.

Classify every new input:

- legacy behavior clarification;
- target architecture constraint;
- behavior-preserving improvement;
- new feature;
- scope conflict;
- unknown or Spike needed.

Output:

- `change-intake.md`;
- package index update;
- affected artifacts list.

Rule:

New features do not belong inside behavior-preserving migration unless they are
split into their own approved story.

## Gate 5 - Product And Spec Package

Goal: turn the behavior contract into buildable product and technical artifacts.

Expected artifacts:

- Epic when the scope spans multiple stories;
- User Story for deliverable behavior;
- Hard Spec for implementation contract;
- Spike when uncertainty blocks design.

Rule:

The Hard Spec must satisfy the User Story without expanding scope.

## Gate 6 - Architecture Decision

Goal: choose target architecture intentionally.

Use the design ladder:

1. local cleanup;
2. module cleanup;
3. boundary cleanup;
4. domain model;
5. clean architecture.

Output:

- architecture decision artifact;
- implementation boundaries;
- explicit non-patterns.

Rule:

Use DDD, ports/adapters and patterns only when they protect real boundaries,
invariants, parity validation or independent evolution.

## Gate 7 - Implementation Brief

Goal: give the developer enough context to build without reading the whole
conversation.

Include:

- scope;
- non-goals;
- behavior contract;
- architecture boundaries;
- files likely touched;
- tests required;
- safety gates;
- evidence to return.

Rule:

Developer scope is limited by the accepted Hard Spec and implementation brief.

## Gate 8 - Review And QA

Goal: separate review responsibilities.

Review lenses:

- Peer reviewer: scope, assumptions, architecture and tradeoffs.
- Code reviewer: diff quality, bugs, maintainability and tests.
- QA reviewer: acceptance criteria, parity evidence and residual risk.

Rule:

Reviewers can challenge scope but cannot silently mutate it.

## Gate 9 - Closeout

Goal: leave a compact, auditable record.

Include:

- what changed;
- what did not change;
- validation evidence;
- residual risk;
- decisions;
- follow-up work;
- context pack for future continuation.

## Required Package Index Updates

Update the package index whenever:

- a new artifact is added;
- status changes;
- a decision is accepted;
- a blocker appears or clears;
- validation evidence changes;
- a change request is classified;
- closeout is updated.

## Decision Support

When a decision is needed, present:

- decision needed;
- option A;
- option B when useful;
- recommendation;
- decision gate.

If evidence is insufficient, recommend a Spike.

## Public-Safe Examples

Examples in this repository must use fake products, fake systems and generic
behavior. Real migration packages belong in private target repositories.
