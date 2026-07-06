# Migration Feature Factory

Status: V0.2 automation layer implemented

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
- [Release Checklist](docs/release/release-checklist.md): V0 release scope,
  smoke checks and next release decision.
- [Public Safety Review](docs/release/public-safety-review.md): V0 public-safety
  evidence and residual risks.
- [Contributing](CONTRIBUTING.md): public-safe contribution workflow.
- [Clean Architecture](docs/architecture/clean-architecture.md): how the
  factory applies clean architecture, SOLID and screaming architecture.
- [Decision Support](docs/architecture/decision-support.md): how the factory
  presents options, tradeoffs and recommendations.
- [Factory Workflow](docs/workflow/factory-workflow.md): migration gates from
  intake through closeout.
- [Automated Discovery](docs/workflow/automated-discovery.md): source scanning,
  package generation and roadmap creation.
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

## Public Example

- [Fake Login Migration](examples/fake-login-migration/migration-package-index.md):
  complete public-safe package showing intake, behavior inventory, parity plan,
  spec artifacts, architecture decision, review and closeout.

## Minimal Scripts

```sh
python3 scripts/scaffold_feature.py --help
python3 scripts/discover_features.py --help
python3 scripts/generate_migration_packages.py --help
python3 scripts/build_migration_roadmap.py --help
python3 scripts/factory_check.py --help
python3 scripts/summarize_context.py --help
```

See [Minimal Scripts](docs/workflow/minimal-scripts.md) for command examples.

## Release Readiness

V0.1 is released for public GitHub use. V0.2 adds the first automation layer:
source feature discovery, package generation and roadmap creation.

Evidence:

- [V0 Release Checklist](docs/release/release-checklist.md)
- [Public Safety Review](docs/release/public-safety-review.md)
- [License Decision](docs/release/license-decision.md)
- [MIT License](LICENSE)

## License

This repository is available under the [MIT License](LICENSE).

## Scope

V0 is Markdown-first:

- reusable workflow documentation;
- migration templates;
- agent role contracts;
- a Codex skill;
- optional Codex hook examples;
- minimal scripts for scaffold, checks and context summaries;
- automated discovery scripts for source inventory, package generation and
  roadmap creation;
- a fake public example with no real customer data.

Supabase, semantic search, dashboards and external integrations remain future
adapters, not current dependencies.

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
