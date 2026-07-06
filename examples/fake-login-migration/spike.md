# Spike - Fake Login Architecture Level

Status: completed
Time-box: one documentation pass
Related package index: `migration-package-index.md`
Related Epic/User Story: `user-story.md`
Sensitivity: public-safe-example

## Question To Answer

- What uncertainty are we reducing? Whether the fake login migration needs full clean architecture or a smaller boundary cleanup.
- Why does it matter now? The public example should be minimalist but not simplistic.
- Which decision will this unblock? ADR-01 target design level.

## Context

- Legacy behavior involved: LB-01 through LB-05.
- Target architecture involved: controller, login policy, account lookup, session writing and audit recording.
- Validation concern: API and side effects cross boundaries.
- Known evidence: behavior inventory and parity plan.
- Missing evidence: no real target code exists in this public example.

## Hypotheses / Options

| Option | Hypothesis | Evidence Needed |
| --- | --- | --- |
| A | Local controller rewrite is enough. | Behavior has no side-effect boundaries. |
| B | Boundary cleanup is enough. | Behavior crosses HTTP, policy, session and audit boundaries. |

## Evaluation Criteria

- Behavior parity: Option B protects more behavior boundaries.
- Feasibility: Option B is still small.
- Complexity: Option B adds meaningful ports only.
- Risk: Option A risks mixing HTTP and side effects.
- Performance/security/operations: Option B keeps correlation and audit handling explicit.
- Fit with target architecture: Option B fits a target service.
- Maintenance cost: Option B is acceptable for five behaviors.

## Activities

- [x] Inspect legacy behavior evidence.
- [x] Inspect target architecture constraints.
- [x] Prototype only if needed.
- [x] Compare options.
- [x] Recommend next action.
- [x] Update affected artifacts.

## Out Of Scope

- Production implementation.
- Broad refactor not needed for the decision.
- New feature delivery.
- Private data capture in public examples.

## Expected Output

- Recommendation: use boundary cleanup.
- Evidence: login crosses API, session and audit boundaries.
- Decision needed: ADR-01.
- Follow-up story/spec updates: align Hard Spec and implementation brief.
- Risks: avoid overbuilding the fake example.

## Definition Of Done

- [x] Evidence collected.
- [x] Options compared.
- [x] Recommendation written.
- [x] Follow-up artifacts identified.
- [x] Package index updated.

## Result

- Decision: boundary cleanup is the right level.
- Evidence: `legacy-behavior-inventory.md` and `behavior-parity-plan.md`.
- Follow-up: ADR-01 accepted.
- Artifacts updated: package index, ADR, Hard Spec and implementation brief.

## Search Anchors

- architecture spike
- boundary cleanup
- fake login
- decision support
