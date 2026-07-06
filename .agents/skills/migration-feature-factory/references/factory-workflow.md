# Skill Workflow Reference

Use this reference when running the factory from Codex.

## Request Classification

Classify first:

| Classification | Meaning | Next Action |
| --- | --- | --- |
| Migration | Existing behavior moves to a new implementation. | Run the migration gates. |
| Migration plus constraint | Migration must use a company library, platform rule or architecture constraint. | Record the constraint and use decision support if adoption is not obvious. |
| Behavior-preserving improvement | Internal quality improves without observable behavior change. | Keep inside migration if evidence proves behavior parity. |
| New feature | Behavior does not exist in the legacy system. | Split into product discovery or a separate story. |
| Scope conflict | Requested behavior changes the legacy contract. | Create a decision request before proceeding. |
| Unknown | Evidence is missing. | Create a Spike. |

## Minimum Package

Do not treat a migration package as implementation-ready until it has:

- package index;
- feature intake;
- legacy behavior inventory;
- behavior parity plan;
- User Story or Epic;
- Hard Spec;
- architecture decision when design choices are material;
- implementation brief.

Use the smallest valid artifact set for the request. A narrow migration may not
need an Epic, but it still needs intake, behavior inventory, parity plan, spec
and review evidence.

## Gate Order

1. Intake: define target, non-goals, systems, stakeholders and risks.
2. Legacy behavior discovery: list observable behaviors and evidence.
3. Behavior parity plan: map behaviors and acceptance criteria to validation.
4. Change intake: classify new input before mutating scope.
5. Product/spec package: create Epic, User Story, Hard Spec or Spike as needed.
6. Architecture decision: document target boundaries and tradeoffs.
7. Implementation brief: give developers bounded build instructions.
8. Review/QA: separate peer, code and QA review.
9. Closeout: summarize changes, validation, risk and future context.

## Template Map

| Need | Template |
| --- | --- |
| Package index | `../../../templates/core/migration-package-index.md` |
| Initial scope | `../../../templates/migration/feature-intake.md` |
| Legacy contract | `../../../templates/migration/legacy-behavior-inventory.md` |
| Validation plan | `../../../templates/migration/behavior-parity-plan.md` |
| New input | `../../../templates/migration/change-intake.md` |
| Epic | `../../../templates/product/epic.md` |
| User Story | `../../../templates/product/user-story.md` |
| Hard Spec | `../../../templates/product/hard-spec.md` |
| Spike | `../../../templates/product/spike.md` |
| Architecture decision | `../../../templates/migration/architecture-decision.md` |
| Implementation brief | `../../../templates/migration/implementation-brief.md` |
| Review and QA | `../../../templates/review/review-qa.md` |
| Closeout | `../../../templates/migration/closeout.md` |

## Stop Conditions

Stop and ask for a decision, or create a Spike, when:

- the source or target system is unclear;
- legacy behavior cannot be evidenced;
- a requested change alters observable behavior;
- private material would need to be written into the public repo;
- validation cannot prove the risky part of the migration;
- architecture constraints conflict with the target repository.
