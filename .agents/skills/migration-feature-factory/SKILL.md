---
name: migration-feature-factory
description: Create and run behavior-preserving feature migration packages. Use when migrating legacy features into a new app, service or architecture; preserving observable behavior while improving internals; producing migration intake, legacy behavior inventory, parity plan, change intake, Epic, User Story, Hard Spec, Spike, architecture decision, implementation brief, review/QA or closeout artifacts; classifying migration scope versus new-feature work; or choosing validation and architecture options with a recommendation.
---

# Migration Feature Factory

## Core Rule

Legacy behavior is the contract. Architecture may improve internally.
Observable behavior changes require a separate approved story.

## Load Only What The Task Needs

- Read `../../../docs/workflow/factory-workflow.md` for the full gate model.
- Read `../../../docs/workflow/automated-discovery.md` when the user wants the
  factory to discover many features or generate packages from source code.
- Read `references/factory-workflow.md` to run the skill operating loop.
- Read `references/behavior-parity.md` when behavior equivalence or validation
  evidence is involved.
- Read `references/change-intake.md` when new requirements, company libraries,
  architecture constraints or scope changes appear.
- Read `references/traceability-harness.md` when package links, status,
  context compaction or closeout continuity matter.
- Read `../../../docs/workflow/traceability-harness.md` when hook mapping or
  package-wide traceability rules matter.
- Read `../../../docs/architecture/decision-support.md` when a decision needs
  options and a recommendation.
- Read `../../../docs/agents/README.md` plus the relevant role file when a role
  handoff or review lens is needed.
- Use templates from `../../../templates/` as the artifact contracts.

## Workflow

1. Classify the request as migration, migration plus constraint, new feature,
   improvement or Spike.
2. If the user asks for automatic preparation across many features, run
   discovery and generate draft packages before selecting implementation scope.
3. Create or update the migration package index before adding standalone
   artifacts.
4. Capture intake, legacy behavior and parity evidence before implementation
   planning.
5. Convert the validated behavior contract into product/spec artifacts.
6. Choose architecture proportionally: local cleanup, module cleanup, boundary
   cleanup, domain model or clean architecture.
7. Produce an implementation brief only after scope, non-goals, behavior
   contract, architecture boundaries and validation evidence are clear.
8. Keep peer review, code review and QA review separate.
9. Close with validation evidence, residual risk, decisions and a compact
   continuation context.

## Decision Discipline

When validation, architecture or scope needs user confirmation, offer one or two
serious options plus a recommendation. If evidence is insufficient, recommend a
Spike instead of implementation.

## Do Not Use This Skill For

- Greenfield feature design with no legacy behavior to preserve, except to
  classify and route it out of the migration flow.
- General code refactoring without a feature migration package.
- Private migration details that should not be written into this public repo.
- Tooling, persistence or search implementation unless the request is about the
  factory itself.
