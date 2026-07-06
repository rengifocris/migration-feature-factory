# Decision Support Contract

Status: draft
Audience: orchestrators, architects, spec owners, reviewers

## Purpose

The factory should help users make good decisions without creating unnecessary
ceremony. When a validation, architecture, scope or implementation choice is
needed, the factory presents a small set of viable options and a recommendation.

The goal is not to generate many alternatives. The goal is to make the best next
move clear and evidence-backed.

## Core Rule

Offer one or two serious options plus a recommendation.

If there is not enough evidence to recommend responsibly, recommend a Spike.

## Decision Shape

```markdown
## Decision Needed

- Question:
- Why now:
- Impacted artifacts:
- Evidence available:
- Evidence missing:

## Option A - <name>

- Summary:
- Benefits:
- Costs:
- Risks:
- Validation impact:
- Architecture impact:

## Option B - <name>

- Summary:
- Benefits:
- Costs:
- Risks:
- Validation impact:
- Architecture impact:

## Recommendation

Choose <option>.

Rationale:

- <reason>

## Decision Gate

- Approver:
- Required evidence:
- Artifacts to update:
- Next action:
```

## When To Use

Use the decision support contract for:

- choosing validation strategy;
- choosing migration slice boundaries;
- deciding whether discovered behavior belongs in migration or a new feature;
- accepting company-provided libraries or platform frameworks as architecture
  constraints;
- choosing between local cleanup, module cleanup, boundary cleanup, DDD or
  clean architecture;
- deciding whether a Spike is needed;
- deciding rollout or compatibility strategy.

Do not use it for:

- obvious template filling;
- minor wording choices;
- formatting decisions;
- choices already decided by the target repository or company standards.

## Minimalist But Not Simplistic

The factory should choose the smallest design level that protects the work.

| Design Level | Use When | Avoid When |
| --- | --- | --- |
| Local cleanup | Names, guard clauses or small extraction improve clarity. | The feature needs cross-boundary behavior control. |
| Module cleanup | A cohesive module or service can own behavior. | The module still leaks infrastructure or legacy details. |
| Boundary cleanup | Adapters, DTOs, ports or services isolate integration risk. | The feature is simple CRUD with stable framework conventions. |
| Domain model | Business terms, invariants or policies are real and recurring. | There is no meaningful domain behavior. |
| Clean architecture | Independent evolution, testability or integration volatility matters. | The cost exceeds the risk being reduced. |

## Recommendation Rules

- Prefer the option that preserves behavior with the least accidental
  complexity.
- Prefer target-repo conventions unless they violate behavior parity,
  maintainability or explicit architecture constraints.
- Treat company-provided libraries as architecture constraints when they provide
  required behavior, governance, security, observability or platform contracts.
- Do not recommend DDD, ports/adapters or clean architecture as decoration.
- If a lower design level solves the problem, stop there.
- If behavior evidence is missing, recommend a Spike before implementation.

## Required Updates After A Decision

When a decision is accepted, update:

- migration package index;
- change log;
- affected User Story or Hard Spec;
- architecture decision artifact when architecture is affected;
- implementation brief;
- review/QA brief;
- validation plan.

## Examples

### Company Architecture Library

Decision needed: Should the migration use a company-provided library as the
main architecture provider?

Recommendation: use it if it provides required platform contracts or prevents
architecture drift. Document the constraint in the ADR and implementation brief.
Do not wrap it behind an abstraction unless the target repo has a real need to
replace it independently.

### New Feature Found During Migration

Decision needed: Should the discovered request be folded into the migration?

Recommendation: split it into the new-feature design flow unless it is already
legacy behavior or a behavior-preserving internal improvement.

### Validation Strategy

Decision needed: Is unit testing enough for this migrated behavior?

Recommendation: use contract or E2E parity tests when external behavior,
integrations, permissions, error codes or side effects are part of the legacy
contract. Unit tests alone are enough only for isolated domain rules.
