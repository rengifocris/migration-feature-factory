# Migration Feature Factory Vision

Status: draft
Audience: maintainers, contributors, migration agents, reviewers

## Purpose

Migration Feature Factory helps teams migrate legacy features into newer
applications, services or architectures without accidentally changing observable
behavior.

The factory provides a repeatable workflow, artifact templates, agent role
contracts, hooks and minimal validation scripts. It is designed to be public on
GitHub while allowing private teams to apply it to real customer or company
work in their own repositories.

## Product Principle

Be minimalist, not simplistic.

The factory should do more with less: fewer moving parts, clearer contracts,
clean boundaries and stronger evidence. Minimalism means removing accidental
complexity. It does not mean avoiding architecture when the work has real
domain rules, integration risk, behavior-parity needs or long-term maintenance
pressure.

## Product Thesis

Most migrations fail because teams mix several concerns into one effort:

- discovering legacy behavior;
- redesigning architecture;
- fixing old problems;
- adding new features;
- writing implementation specs;
- proving behavior parity;
- explaining decisions after the fact.

This factory separates those concerns. Legacy behavior is captured first,
architecture decisions are explicit, changes are classified, and every
implementation slice must connect to validation evidence.

## Core Rule

Legacy behavior is the contract.

Architecture may improve internally, but user-visible behavior, API behavior,
data behavior, permissions, errors, side effects and integrations must remain
equivalent unless a separate new-feature story approves the change.

## Goals

- Preserve behavior while improving architecture.
- Make migration work explainable to engineers, customers and reviewers.
- Offer one or two viable options plus a recommendation when a decision is
  required.
- Produce Epic, User Story, Hard Spec and review-ready implementation packets.
- Keep decisions, evidence and progress linked.
- Provide agent roles with clear responsibilities and blocked protocols.
- Add optional hooks and scripts that enforce traceability and automate safe
  discovery without building a heavy platform.
- Generate mock-server, synthetic-data and model-governance strategies when
  migrations depend on clients, enrichment, DTO boundaries, mappers or
  canonical records.
- Stay public-safe by avoiding real customer data.

## Non-Goals

- V0 is not a full web app.
- V0 is not a Supabase memory platform.
- V0 does not perform automatic code migration.
- V0 does not replace target-repo tests, CI or architecture conventions.
- V0 does not hide new features inside behavior-preserving migration work.

## Clean Architecture Model

The factory itself follows clean architecture at the documentation and tooling
level.

```text
Core domain:
  migration principles
  behavior parity rules
  artifact contracts
  traceability requirements
  agent role responsibilities

Application layer:
  factory workflow
  change-intake routing
  migration package lifecycle
  review and QA gates

Adapters:
  Codex skill
  Markdown templates
  optional hooks
  optional scripts
  optional future Supabase/search adapter
  optional future GitHub/Jira adapter

Delivery:
  README
  docs
  examples
  public repository packaging
```

## SOLID Interpretation

- Single Responsibility: each template and agent role has one clear job.
- Open/Closed: new adapters can be added without changing the core migration
  contract.
- Liskov Substitution: company-specific templates may replace public templates
  if they preserve required fields and gates.
- Interface Segregation: agents receive focused briefs instead of one giant
  prompt.
- Dependency Inversion: core workflow does not depend on Codex, Supabase, Jira,
  GitHub or a programming language.

## Decision Support Contract

When the factory reaches a validation, architecture, scope or implementation
decision, it should not just ask an open-ended question. It should present a
small decision set.

Default decision shape:

```text
Decision needed:
  What must be decided and why now.

Option A:
  Description, benefits, cost, risk, validation impact.

Option B:
  Description, benefits, cost, risk, validation impact.

Recommendation:
  The option the factory recommends and why.

Decision gate:
  Who must approve, what evidence is required and what happens next.
```

Rules:

- Prefer one clear recommendation with at most two serious alternatives.
- Do not include weak options just to look balanced.
- Separate facts, assumptions and judgment.
- If evidence is insufficient, recommend a Spike instead of guessing.
- Record accepted decisions in the package index and the architecture decision
  artifact when they affect implementation.
- Keep recommendations proportional: clean architecture, DDD, ports/adapters or
  patterns are justified only when they protect real boundaries, invariants,
  behavior parity or independent evolution.

See [Decision Support](architecture/decision-support.md) for the detailed
contract.

## Factory Lifecycle

Each migrated feature moves through these gates:

1. Intake: identify feature, source, target, owners, scope and non-goals.
2. Legacy behavior discovery: inventory entry points, flows, data, errors,
   permissions, side effects and integrations.
3. Behavior parity plan: define tests and evidence that prove behavior stayed
   equivalent.
4. Mock/data/model governance: define mock-server boundaries, synthetic happy,
   edge and bad cases, raw/enriched model rules and client/mapper governance.
5. Spec package: create or update Epic, User Story, Hard Spec and Spikes where
   needed.
6. Architecture decision: document target boundaries, company constraints,
   patterns and explicit non-patterns.
7. Implementation brief: hand developers a scoped packet with boundaries and
   validation requirements.
8. Review gates: peer review, code review and QA review.
9. Closeout: summarize changed files, unchanged behavior, validation evidence,
   residual risk and follow-up work.

## Change Intake Router

Any new information found during migration must be classified before it changes
scope.

| Classification | Example | Action |
| --- | --- | --- |
| Legacy behavior clarification | A hidden legacy edge case is discovered. | Update behavior inventory, parity plan, Hard Spec and tests. |
| Target architecture constraint | Company requires an internal library or platform framework. | Update architecture decision, Hard Spec and implementation brief. |
| Behavior-preserving improvement | Internal code structure improves without visible behavior change. | Allow if parity evidence remains valid. |
| New feature | The desired behavior does not exist in legacy. | Route to new-feature design flow. |
| Scope conflict | Requested change alters behavior without approval. | Stop, split, or ask for decision. |
| Unknown | Evidence is insufficient. | Create a Spike. |

## Traceability Harness

Every feature package needs a central package index that links artifacts and
keeps the work auditable.

Required traceability:

- every legacy behavior maps to a parity test or documented gap;
- every acceptance criterion maps to Hard Spec coverage;
- every Hard Spec requirement maps to validation evidence;
- every architecture constraint maps to an ADR or implementation boundary;
- every change request is classified;
- every blocker has an owner, status and next action;
- closeout states what changed, what did not change and what remains risky.

## Agents

Agents are responsibility boundaries, not personalities.

Recommended roles:

- Migration Orchestrator: owns lifecycle, gates, scope and synthesis.
- Legacy Analyst: extracts current behavior and evidence.
- Product Owner / Business Analyst: converts behavior and goals into product
  scope.
- Spec Owner: aligns User Story, Hard Spec, Spike and implementation brief.
- Architect: chooses target boundaries and justified patterns.
- Developer: implements only the approved scope.
- Peer Reviewer: challenges scope, architecture and assumptions.
- Code Reviewer: reviews diff quality, bugs, maintainability and tests.
- QA Reviewer: validates acceptance criteria and behavior parity evidence.
- Technical Writer: keeps docs, closeout and public-safe wording clear.

Each agent contract should define:

- mission;
- inputs;
- outputs;
- allowed decisions;
- forbidden decisions;
- evidence required;
- blocked protocol.

## Skills

The main reusable workflow should be a Codex skill:

```text
skills/migration-feature-factory/
  SKILL.md
  references/
    factory-workflow.md
    behavior-parity.md
    change-intake.md
    traceability-harness.md
```

The skill teaches Codex when and how to run the factory. It should activate for
requests such as:

- migrate a legacy feature;
- preserve behavior while improving architecture;
- build migration specs;
- create a behavior parity plan;
- classify migration vs new feature;
- run migration review gates.

## Hooks

Hooks are optional enforcement, not the workflow itself.

Useful Codex hook examples:

- Stop: run the factory check before the turn ends.
- PreCompact: verify or update a compact context pack.
- PostToolUse: detect changed migration artifacts and remind/update the package
  index.
- PreToolUse: block risky implementation commands when Hard Spec or parity plan
  is missing.

Public hook files should be examples only. Users must explicitly review and
trust hooks in their own Codex environment.

## Automation Layer

The factory should automate the repetitive parts of migration preparation:

- discover source entry points;
- create a source feature inventory;
- generate one migration package per candidate;
- recommend an initial migration order;
- keep generated artifacts marked as discovery drafts.
- generate technical foundation specs before code generation.
- generate mock-server, synthetic-data and model-governance strategy before
  implementation when clients, enrichment or model boundaries matter.

The factory should not automatically implement all features. Code migration
requires reviewed behavior evidence, target architecture boundaries, parity
strategy and an implementation brief.

This keeps the factory useful for large repos without turning it into a blind
rewrite tool.

## Minimal Scripts

V0.1 needed only three scripts:

```text
scripts/
  scaffold_feature.py
  factory_check.py
  summarize_context.py
```

V0.2 adds the first automation scripts:

```text
scripts/
  discover_features.py
  generate_migration_packages.py
  build_migration_roadmap.py
```

V0.3 adds technical foundation generation:

```text
scripts/
  generate_technical_foundation.py
```

V0.4 adds mock-server, synthetic-data and model-governance generation:

```text
scripts/
  generate_mock_and_model_governance.py
```

Responsibilities:

- scaffold_feature.py: creates a feature package from templates.
- discover_features.py: scans source entry points and writes an inventory.
- generate_migration_packages.py: creates draft packages for discovered
  features.
- build_migration_roadmap.py: recommends migration order from inventory risk.
- generate_technical_foundation.py: creates architecture blueprint, generation
  policy, design-pattern guidance, code-style rules and diagrams.
- generate_mock_and_model_governance.py: creates mock-server strategy,
  synthetic scenario matrix, model-governance policy and code-context signal
  table without copying source excerpts.
- factory_check.py: validates required files, headings, statuses, links and
  traceability expectations.
- summarize_context.py: creates or updates a compact context pack for long
  work and compaction-safe continuation.

Scripts should be deterministic, readable and dependency-light.

## Public / Private Boundary

The public repository contains the factory pattern:

- templates;
- fake examples;
- docs;
- scripts;
- optional hook examples;
- optional future adapter designs.

Private repos contain real work:

- client/customer data;
- real issue context;
- private code references;
- proprietary architecture constraints;
- credentials and environment details;
- real validation evidence.

## Roadmap

V0.1: Markdown-first factory with skills, agents, hook examples and minimal
scripts.

V0.2: automated source discovery, package generation and roadmap creation.

V0.3: technical foundation and architecture blueprint generation.

V0.4: mock-server, synthetic-data and model-governance generation.

V1: CLI quality improvements, richer checks, plugin packaging and more examples.

V2: optional persistence/search adapter such as Supabase, lexical search,
artifact indexing and context-pack retrieval.

V3: optional UI or dashboard for migration status and traceability.

## Success Criteria

The factory is successful when a developer can:

- create a feature migration package from templates;
- classify new input without corrupting migration scope;
- preserve behavior with explicit parity evidence;
- explain why architecture choices were made;
- resume work from a compact context pack;
- pass review gates without relying on raw chat history;
- publish the factory publicly without leaking private data.

## Open Questions

- Should V0 include a license immediately?
- Should the default examples use a backend API migration, frontend flow
  migration or both?
- Should hook examples be disabled by default under `.codex/hooks.json.example`
  only?
- Should the first CLI be plain Python scripts or a packaged command later?
- Should plugin packaging be V1 or V2?
