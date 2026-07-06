# Change Intake - Fake Login Migration

Status: completed
Feature ID: FAKE-LOGIN-001
Change ID: CHG-01
Related package index: `migration-package-index.md`
Sensitivity: public-safe-example

## New Input

- Date: 2026-07-06
- Source: EPIC-07 backlog scope.
- Summary: example must be fake, public-safe and complete enough to pass the factory check.
- Evidence: `docs/backlog.md`.

## Classification

Choose one primary classification.

- [ ] Legacy behavior clarification
- [x] Target architecture constraint
- [ ] Behavior-preserving improvement
- [ ] New feature
- [ ] Scope conflict
- [ ] Unknown / Spike needed

## Impact Analysis

| Area | Impact | Artifact To Update |
| --- | --- | --- |
| Legacy behavior | use fake behavior only | `legacy-behavior-inventory.md` |
| Parity plan | planned evidence only, no real app tests | `behavior-parity-plan.md` |
| User Story | state public-safe fake scope | `user-story.md` |
| Hard Spec | avoid real system details | `hard-spec.md` |
| Architecture | use generic target service boundaries | `architecture-decision.md` |
| Implementation brief | describe hypothetical target files only | `implementation-brief.md` |
| Review / QA | include public-safety review | `review-qa.md` |

## Decision Needed

- Question: should the example include any real implementation detail?
- Why now: EPIC-07 is a public repository example.
- Evidence available: backlog states fake example only.
- Evidence missing: none.

## Options

### Option A - Fold Into Current Migration

- When valid: the change keeps the package fake and behavior-preserving.
- Benefits: example remains complete and public-safe.
- Risks: none material.
- Required updates: all package artifacts.

### Option B - Split Into Separate Work

- When valid: the change asks for a real app, client context or new behavior.
- Benefits: protects public repository.
- Risks: delays example.
- Required updates: create a separate private package.

## Recommendation

Recommended decision: choose Option A.

Rationale:

- Fake public scope is required by EPIC-07.
- No observable behavior change is introduced.

## Required Updates

- [x] Package index
- [x] Legacy behavior inventory
- [x] Behavior parity plan
- [x] User Story
- [x] Hard Spec
- [x] Architecture decision
- [x] Implementation brief
- [x] Review / QA brief
- [x] Closeout

## Approval / Gate

- Approver: migration-orchestrator.
- Approval needed before: package closeout.
- If not approved: block public example publication.

## Search Anchors

Terms people might search for:

- change intake
- public fake example
- scope classification
- fake login
