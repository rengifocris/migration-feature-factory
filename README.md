# Migration Feature Factory

Status: draft planning scaffold

Migration Feature Factory is a public-safe system for moving legacy features into
new applications or services while preserving observable behavior and improving
internal architecture.

The core rule:

> Legacy behavior is the contract. Architecture may improve internally.
> Observable behavior changes require a separate approved story.

## Start Here

- [Repository Rules](AGENTS.md): durable working agreements for contributors
  and Codex agents.
- [Vision](docs/vision.md): product direction, architecture principles, agents,
  skills, hooks, scripts and public/private boundaries.
- [Backlog](docs/backlog.md): ordered implementation backlog for building the
  factory.
- [Clean Architecture](docs/architecture/clean-architecture.md): how the
  factory applies clean architecture, SOLID and screaming architecture.
- [Decision Support](docs/architecture/decision-support.md): how the factory
  presents options, tradeoffs and recommendations.
- [Factory Workflow](docs/workflow/factory-workflow.md): migration gates from
  intake through closeout.
- [Traceability Harness](docs/workflow/traceability-harness.md): package index,
  traceability rules, change log discipline and optional hook mapping.
- [Minimal Scripts](docs/workflow/minimal-scripts.md): standard-library
  scaffold, check and context-summary helpers.
- [Agent Roles](docs/agents/README.md): responsibility contracts for
  orchestrator, discovery, product/spec, architecture, implementation, review
  and writing roles.
- [Codex Skill](.agents/skills/migration-feature-factory/SKILL.md): reusable
  Codex workflow for running the factory from this repo.
- [Codex Desktop Setup](docs/setup/codex-desktop.md): recommended local setup
  for using the factory in Codex Desktop.

## V0 Templates

- [Migration Package Index](templates/core/migration-package-index.md)
- [Feature Intake](templates/migration/feature-intake.md)
- [Legacy Behavior Inventory](templates/migration/legacy-behavior-inventory.md)
- [Behavior Parity Plan](templates/migration/behavior-parity-plan.md)
- [Change Intake](templates/migration/change-intake.md)
- [Epic](templates/product/epic.md)
- [User Story](templates/product/user-story.md)
- [Hard Spec](templates/product/hard-spec.md)
- [Spike](templates/product/spike.md)
- [Architecture Decision](templates/migration/architecture-decision.md)
- [Implementation Brief](templates/migration/implementation-brief.md)
- [Review And QA Brief](templates/review/review-qa.md)
- [Closeout](templates/migration/closeout.md)

## Minimal Scripts

```sh
python3 scripts/scaffold_feature.py --help
python3 scripts/factory_check.py --help
python3 scripts/summarize_context.py --help
```

See [Minimal Scripts](docs/workflow/minimal-scripts.md) for command examples.

## Scope

V0 is Markdown-first:

- reusable workflow documentation;
- migration templates;
- agent role contracts;
- a Codex skill;
- optional Codex hook examples;
- minimal scripts for scaffold, checks and context summaries;
- a fake public example with no real customer data.

Supabase, semantic search, dashboards and external integrations are future
adapters, not V0 dependencies.

## Operating Principle

Be minimalist, not simplistic.

Use the smallest solution that preserves behavior, clarifies intent and keeps
future change safe. Add structure only when it protects a real boundary,
decision, invariant or validation need.

## Public Safety

This repository must not contain:

- real client/customer migration data;
- secrets, credentials, keys or connection strings;
- private repo paths that identify sensitive work;
- raw chat logs, raw exports or unnecessary personal data.

Use fake examples and generic terminology in public documentation.
