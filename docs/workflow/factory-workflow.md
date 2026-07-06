# Factory Workflow

Status: draft
Audience: migration orchestrators, agents, maintainers

## Purpose

This workflow turns a vague migration request into an auditable migration
package that preserves legacy behavior and guides implementation in a cleaner
architecture.

## Workflow Summary

```text
0. Optional automated discovery and package generation
1. Intake
2. Legacy behavior discovery
3. Behavior parity plan
4. Change intake and classification
5. Technical foundation and architecture blueprint
6. Mock server, synthetic data and model governance
7. Product/spec package
8. Architecture decision
9. Implementation brief
10. Review and QA gates
11. Closeout
```

V0.2 can create discovery inventories, draft packages and a roadmap
automatically. These generated artifacts still enter Gate 1 as drafts.

## Gate 0 - Optional Automated Discovery

Goal: create a starting inventory and package set from source repository entry
points.

Inputs:

- source repository path;
- source system name;
- target system name;
- output root for generated packages.

Output:

- source feature inventory;
- one draft migration package per discovered candidate;
- migration roadmap.

Rule:

Generated packages are discovery drafts. They do not approve implementation and
do not prove behavior parity.

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

## Gate 5 - Technical Foundation And Architecture Blueprint

Goal: decide the target architecture rules before generating code or packages
at scale.

Expected artifacts:

- technical foundation spec;
- architecture blueprint;
- package/module slicing decision;
- DTO/model/ACL generation policy;
- code style and defensive-programming rules;
- diagrams;
- validation gates.

Rule:

Generated DTOs and API delegates are allowed at boundaries. Domain models,
ACLs, mappers, validation behavior and error semantics require engineering
review because they affect behavior parity and maintainability.

## Gate 6 - Mock Server, Synthetic Data And Model Governance

Goal: define test doubles, synthetic fixtures and model/client boundaries before
implementation begins.

Expected artifacts:

- mock-server strategy;
- synthetic scenario matrix for happy, edge and bad cases;
- fixture governance rules;
- raw/non-enriched, canonical and enriched model policy;
- client, adapter/ACL, mapper and validator governance;
- code-context signal table when source roots are scanned.

Rule:

Mock servers and synthetic data support parity evidence. They do not replace
legacy behavior discovery, approved specs or target platform review.

## Gate 7 - Product And Spec Package

Goal: turn the behavior contract into buildable product and technical artifacts.

Expected artifacts:

- Epic when the scope spans multiple stories;
- User Story for deliverable behavior;
- Hard Spec for implementation contract;
- Spike when uncertainty blocks design.

Rule:

The Hard Spec must satisfy the User Story without expanding scope.

## Gate 8 - Architecture Decision

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

## Gate 9 - Implementation Brief

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

## Gate 10 - Review And QA

Goal: separate review responsibilities.

Review lenses:

- Peer reviewer: scope, assumptions, architecture and tradeoffs.
- Code reviewer: diff quality, bugs, maintainability and tests.
- QA reviewer: acceptance criteria, parity evidence and residual risk.

Rule:

Reviewers can challenge scope but cannot silently mutate it.

## Gate 11 - Closeout

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
