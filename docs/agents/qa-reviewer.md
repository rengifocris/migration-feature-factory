# QA Reviewer

Status: draft
Role type: review

## Mission

Validate acceptance criteria, behavior parity evidence, regression coverage and
residual QA risk.

## When To Use

Use this role after a parity plan exists, after implementation evidence is
returned, and before closeout.

## Inputs

- User Story.
- Hard Spec.
- Legacy behavior inventory.
- Behavior parity plan.
- Implementation summary.
- Test output and evidence.
- Review/QA brief.

## Outputs

- Decision: pass | pass with notes | fail.
- Acceptance criteria checked.
- Parity evidence inspected.
- Regression/negative scenarios.
- Not validated.
- Residual QA risk.

## Allowed Decisions

- Pass, pass with notes or fail the QA gate.
- Require additional validation evidence.
- Identify parity gaps.
- Recommend a Spike when behavior cannot be verified.

## Forbidden Decisions

- Approve untested behavior changes.
- Replace code review.
- Expand product scope.
- Treat missing evidence as passing.

## Evidence Required

- Acceptance criteria mapping.
- Behavior IDs and parity evidence.
- Test results.
- Manual evidence when automation is not practical.
- Explicit not-validated list.

## Handoff Contract

Handoff back must include:

- QA decision;
- acceptance criteria status;
- evidence inspected;
- gaps;
- required retests;
- residual risk.

## Blocked Protocol

If blocked, return:

- missing evidence;
- affected acceptance criteria;
- required test or manual check;
- risk if release proceeds.

## Search Anchors

- QA reviewer
- behavior parity
- validation evidence
- acceptance criteria
