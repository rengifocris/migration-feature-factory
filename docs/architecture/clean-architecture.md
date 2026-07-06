# Clean Architecture For The Factory

Status: draft
Audience: maintainers, architects, contributors

## Purpose

This document defines how Migration Feature Factory applies clean architecture,
SOLID and screaming architecture without becoming overbuilt.

The factory should be simple to use, but strict about behavior preservation,
traceability and decision quality.

## Core Position

The factory is not a code framework first. It is a workflow and artifact system
with optional adapters.

The architecture must make the purpose obvious:

```text
migration-feature-factory/
  docs/
    architecture/
    workflow/
    setup/
  templates/
    core/
    migration/
    product/
    review/
  .agents/
    skills/
  .codex/
  scripts/
  examples/
```

This is screaming architecture: the repository structure should say
"migration factory" before it says "scripts" or "utilities".

## Layers

```text
Core domain:
  behavior preservation
  migration package contract
  traceability rules
  decision support
  agent responsibilities

Application workflow:
  intake
  legacy discovery
  behavior parity planning
  change intake
  spec generation
  architecture decision
  implementation handoff
  review and closeout

Adapters:
  Codex skill
  Markdown templates
  optional hooks
  minimal scripts
  future persistence/search
  future external tracker integrations

Delivery:
  README
  docs
  fake examples
  public repository
```

The core domain must not depend on adapters. For example, the behavior parity
rules should make sense even if a team does not use Codex hooks, Supabase or a
future CLI.

## SOLID Application

### Single Responsibility

Each artifact should have one primary reason to change.

- Intake changes when scope inputs change.
- Legacy behavior inventory changes when legacy behavior evidence changes.
- Parity plan changes when validation strategy changes.
- Change intake changes when new information appears.
- Package index changes when relationships, status or traceability changes.

### Open / Closed

The factory should allow extension through new templates, scripts or adapters
without rewriting the core workflow.

Examples:

- add a Jira adapter later;
- add a Supabase index later;
- add company-specific templates later;
- add frontend-specific parity checks later.

### Liskov Substitution

Team-specific templates can replace public templates only if they preserve the
required contract:

- status;
- scope;
- non-goals;
- evidence;
- traceability links;
- risks and open questions;
- validation expectations.

### Interface Segregation

Agents should receive focused inputs.

- Developers receive implementation briefs.
- QA reviewers receive parity plans and evidence.
- Architects receive behavior constraints, target constraints and decision
  options.
- Product/spec owners receive scope and acceptance criteria.

Avoid one huge prompt or document that asks every agent to infer its role.

### Dependency Inversion

High-level migration rules should not depend on low-level tools.

Good:

```text
Behavior parity must be validated.
```

Avoid:

```text
Behavior parity must be validated by one specific test framework.
```

Target repositories choose concrete testing tools according to their stack.

## Design Ladder

Use the smallest design level that protects the work.

| Level | Use When | Output |
| --- | --- | --- |
| Local cleanup | Naming, small extraction or guard clauses clarify intent. | Implementation note. |
| Module cleanup | A cohesive module can own behavior. | Hard Spec boundary. |
| Boundary cleanup | Integration or framework details must be isolated. | ADR and implementation brief. |
| Domain model | Business rules, policies or invariants are meaningful. | Domain terms and model boundaries. |
| Clean architecture | Independent evolution, testability or volatility justifies the cost. | Ports/adapters or equivalent target pattern. |

Stop at the lowest level that solves the real problem.

## DDD Use

Use DDD only when the migration has real domain language or invariants.

Good DDD signals:

- business terms are stable and repeated;
- rules are more important than framework plumbing;
- behavior has meaningful invariants;
- policy must be tested without external systems.

Weak DDD signals:

- simple CRUD;
- purely technical mapping;
- no recurring business language;
- no policy beyond data transport.

## Pattern Rules

Use patterns only when they remove real complexity.

- Adapter: isolate legacy, company library or external platform details.
- Strategy: select behavior from a real runtime or domain variation.
- Repository: keep persistence details out of core behavior when needed.
- Facade: simplify a volatile or broad integration.
- Pipeline: compose ordered processing steps with clear validation.

If the pattern does not protect behavior, testability or change isolation, do
not add it.

## Company Architecture Libraries

Company-provided libraries can be architecture constraints.

Use them when they provide:

- required platform contracts;
- security, observability or governance;
- built-in behavior the target system must follow;
- consistency with the target repo architecture.

Do not wrap a company library behind a custom abstraction unless replacement,
testing or boundary protection is a real need.

## Decision Discipline

When architecture is not obvious, use the decision support contract:

- one or two serious options;
- recommendation;
- evidence;
- validation impact;
- artifacts to update.

If evidence is missing, create a Spike.

## Public Safety

Architecture examples must be generic. Do not include private class names,
private repo paths or proprietary implementation details from real projects.
