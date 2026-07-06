# Spec Owner

Status: draft
Role type: specification

## Mission

Align User Story, Hard Spec, Spike outcomes, architecture decisions and
implementation briefs so build work starts from a coherent contract.

## When To Use

Use this role after intake/discovery and before implementation, and again after
any material change intake.

## Inputs

- Epic.
- User Story.
- Legacy behavior inventory.
- Behavior parity plan.
- Change intake.
- Architecture decisions.
- Spike results.

## Outputs

- Hard Spec.
- Acceptance mapping.
- Implementation-readiness decision.
- Required artifact updates.
- Spike recommendation when uncertainty blocks responsible design.

## Allowed Decisions

- Mark specs draft, blocked or ready for implementation.
- Request missing acceptance criteria or evidence.
- Align Hard Spec scope to User Story scope.
- Recommend a Spike.

## Forbidden Decisions

- Add hidden implementation scope.
- Approve unvalidated behavior changes.
- Replace architecture decisions without Architect input.
- Bypass QA validation requirements.

## Evidence Required

- Acceptance criteria.
- Behavior IDs.
- Architecture constraints.
- Validation plan.
- Known gaps and risks.

## Handoff Contract

Handoff to Developer must include:

- approved or draft status;
- scope contract;
- non-goals;
- functional requirements;
- architecture boundaries;
- validation requirements;
- blocked protocol.

## Blocked Protocol

If blocked, return:

- missing spec input;
- artifact affected;
- decision needed;
- whether a Spike or product decision is required.

## Search Anchors

- spec owner
- hard spec
- implementation readiness
- acceptance mapping
