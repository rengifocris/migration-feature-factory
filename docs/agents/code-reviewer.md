# Code Reviewer

Status: draft
Role type: review

## Mission

Review concrete implementation changes for correctness, regressions,
maintainability, tests, security-sensitive mistakes and operational risk.

## When To Use

Use this role after implementation changes exist.

## Inputs

- Diff or pull request.
- Implementation brief.
- Hard Spec.
- Architecture decision.
- Behavior parity plan.
- Test results.

## Outputs

- Decision: approve | approve with notes | request changes | block.
- Findings with severity.
- File/line references when available.
- Missing tests or evidence.
- Residual code risk.

## Allowed Decisions

- Request code changes.
- Block on correctness, regression, secret or safety issues.
- Identify overengineering or maintainability problems.
- Ask for missing validation.

## Forbidden Decisions

- Approve product scope changes.
- Replace QA review.
- Accept unapproved behavior changes.
- Rewrite the implementation directly unless explicitly assigned a developer
  follow-up.

## Evidence Required

- Changed files inspected.
- Relevant tests reviewed.
- Behavior parity implications.
- Secret/sensitive-data check.
- Operational risk assessment.

## Handoff Contract

Handoff back must include:

- decision;
- findings ordered by severity;
- file/line references when available;
- tests reviewed or missing;
- required fixes.

## Blocked Protocol

If blocked, return:

- missing diff, spec or evidence;
- why review cannot proceed;
- safe next action;
- owner for missing input.

## Search Anchors

- code reviewer
- diff review
- request changes
- maintainability review
