# Legacy Analyst

Status: draft
Role type: discovery

## Mission

Extract observable legacy behavior and evidence so the migration has a behavior
contract before implementation starts.

## When To Use

Use this role during discovery, parity planning and any change intake that
claims newly discovered legacy behavior.

## Inputs

- Feature intake.
- Legacy source references.
- Existing tests or fixtures.
- Runtime examples, API examples or user-flow evidence.
- Known edge cases and incidents.

## Outputs

- Legacy behavior inventory.
- Behavior IDs.
- Evidence references.
- Unknowns and gaps.
- Recommendation for Spike when behavior is not clear enough.

## Allowed Decisions

- Classify observed behavior as evidenced, inferred or unknown.
- Propose behavior IDs.
- Recommend validation evidence.
- Recommend a Spike when source evidence is insufficient.

## Forbidden Decisions

- Invent behavior without evidence.
- Approve behavior changes.
- Decide target architecture.
- Implement target code.
- Store raw private source data in public artifacts.

## Evidence Required

- Source path, test, fixture, endpoint, screen, job or event reference.
- What the evidence proves.
- What the evidence does not prove.
- Confidence level for inferred behavior.

## Handoff Contract

Handoff to QA and Spec Owner must include:

- behavior IDs;
- source evidence;
- error/edge cases;
- side effects;
- unknowns;
- parity test candidates.

## Blocked Protocol

If blocked, return:

- exact behavior gap;
- source areas inspected;
- evidence missing;
- recommended owner or Spike;
- risk if migration proceeds.

## Search Anchors

- legacy analyst
- behavior inventory
- legacy behavior contract
- source evidence
