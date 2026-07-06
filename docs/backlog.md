# Migration Feature Factory Backlog

Status: draft
Language policy: English only
Owner: local maintainer

## Current Objective

Build a public-safe V0 of Migration Feature Factory:

- Markdown-first;
- clean architecture and SOLID principles;
- agents, skills and optional hooks;
- minimal scripts;
- fake example only;
- no private data;
- no Supabase dependency in V0.

## Delivery Order

| Order | ID | Type | Title | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 0 | INIT-00 | Setup | Vision and backlog packet | completed | Created this planning baseline. |
| 1 | EPIC-01 | Epic | Public repo foundation | draft | Repo shape, safety, contribution docs. |
| 2 | EPIC-02 | Epic | Core migration workflow and templates | draft | Factory gates and artifact contracts. |
| 3 | EPIC-03 | Epic | Agent role system | draft | Responsibility boundaries and handoff contracts. |
| 4 | EPIC-04 | Epic | Codex skill package | draft | Reusable skill and references. |
| 5 | EPIC-05 | Epic | Traceability harness and hooks | draft | Package index, checks and hook examples. |
| 6 | EPIC-06 | Epic | Minimal scripts | draft | Scaffold, check and context summary. |
| 7 | EPIC-07 | Epic | Public fake example | draft | Demonstrates end-to-end migration package. |
| 8 | EPIC-08 | Epic | Release readiness | draft | License, README polish, checks and public safety review. |

## EPIC-01 - Public Repo Foundation

Status: draft

### Business Outcome

Create a clean public repository structure that explains the factory and avoids
leaking private implementation or customer context.

### Scope

In scope:

- root README;
- public/private boundary doc;
- docs folder structure;
- contribution and safety expectations;
- initial architecture notes.

Out of scope:

- publishing to GitHub;
- packaging as a Codex plugin;
- real migration examples.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-01.1 | As a maintainer, I want a clear README so newcomers understand the factory purpose and V0 scope. | Public clarity. |
| US-01.2 | As a contributor, I want public-safety rules so no private data is added by mistake. | Safety. |
| US-01.3 | As an architect, I want clean architecture and SOLID docs so the repo has design discipline from the start. | Maintainability. |

### Definition of Done

- README links to vision, backlog and future docs.
- Public/private boundary is explicit.
- No real customer data is present.

## EPIC-02 - Core Migration Workflow And Templates

Status: draft

### Business Outcome

Provide the reusable migration package structure that turns ambiguous migration
requests into inspectable artifacts.

### Scope

In scope:

- factory workflow;
- feature intake template;
- legacy behavior inventory template;
- behavior parity plan template;
- change intake template;
- Epic/User Story/Hard Spec/Spike templates adapted for migration;
- architecture decision template;
- implementation brief template;
- review/QA template;
- closeout template.

Out of scope:

- target repo code changes;
- automated code analysis.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-02.1 | As a migration orchestrator, I want a feature intake template so migration scope and non-goals are explicit. | Scope control. |
| US-02.2 | As a legacy analyst, I want a behavior inventory template so current behavior becomes the migration contract. | Behavior preservation. |
| US-02.3 | As a QA reviewer, I want a behavior parity plan so equivalence evidence is defined before implementation. | Regression control. |
| US-02.4 | As a spec owner, I want migration-ready User Story and Hard Spec templates so implementation does not expand hidden scope. | Build readiness. |
| US-02.5 | As an architect, I want an ADR template so target architecture constraints and patterns are explicit. | Design clarity. |
| US-02.6 | As an orchestrator, I want a closeout template so validation, risks and follow-ups are not lost. | Continuity. |

### Definition of Done

- All V0 templates exist.
- Required sections are consistent.
- Templates include status, sensitivity, scope, evidence and Search Anchors or
  terminology sections where useful.

## EPIC-03 - Agent Role System

Status: draft

### Business Outcome

Define the specialist responsibilities needed to run migrations safely without
mixing architecture, implementation and QA decisions.

### Scope

In scope:

- migration orchestrator;
- legacy analyst;
- product owner / business analyst;
- spec owner;
- architect;
- developer;
- peer reviewer;
- code reviewer;
- QA reviewer;
- technical writer.

Out of scope:

- character/personality agents;
- real subagent runtime setup;
- external tool integrations.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-03.1 | As an orchestrator, I want role contracts so each agent has a clear mission and output. | Coordination. |
| US-03.2 | As a reviewer, I want forbidden decisions listed so reviewers do not silently change scope. | Governance. |
| US-03.3 | As a blocked agent, I want a blocked protocol so missing context becomes a decision request instead of guessing. | Safety. |

### Definition of Done

- Each role has mission, inputs, outputs, allowed decisions, forbidden
  decisions, evidence and blocked protocol.
- Review roles are distinct: peer review, code review and QA review.

## EPIC-04 - Codex Skill Package

Status: draft

### Business Outcome

Make the factory reusable from Codex through a focused skill that routes work to
the migration workflow and references.

### Scope

In scope:

- `skills/migration-feature-factory/SKILL.md`;
- reference docs for workflow, behavior parity, change intake and traceability;
- trigger description with clear boundaries.

Out of scope:

- plugin packaging;
- app connector setup;
- external MCP tools.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-04.1 | As a Codex user, I want a migration skill so Codex can run the factory consistently. | Reuse. |
| US-04.2 | As a maintainer, I want references split from `SKILL.md` so context loads progressively. | Context efficiency. |
| US-04.3 | As a user, I want the skill to classify migration vs new feature so scope stays clean. | Delivery control. |

### Definition of Done

- Skill has name, description and workflow instructions.
- Skill references only public-safe docs.
- Skill states when not to use the factory.

## EPIC-05 - Traceability Harness And Hooks

Status: draft

### Business Outcome

Keep migration artifacts linked and updated across iterations, context
compaction and review cycles.

### Scope

In scope:

- migration package index template;
- traceability matrix rules;
- change log rules;
- hook documentation;
- `.codex/hooks.json.example`;
- hook-to-script mapping.

Out of scope:

- enabling hooks automatically;
- managed/admin hooks;
- hard blocking in user environments by default.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-05.1 | As an orchestrator, I want a package index so all artifacts, statuses and owners are visible. | Traceability. |
| US-05.2 | As a QA reviewer, I want acceptance criteria mapped to validation evidence so parity is auditable. | Quality. |
| US-05.3 | As a Codex user, I want hook examples so checks can run at Stop, PreCompact and PostToolUse. | Discipline. |

### Definition of Done

- Package index template exists.
- Traceability rules are documented.
- Hook examples are public-safe and disabled unless users copy/trust them.

## EPIC-06 - Minimal Scripts

Status: draft

### Business Outcome

Provide lightweight deterministic enforcement without turning the factory into a
large application.

### Scope

In scope:

- `scaffold_feature.py`;
- `factory_check.py`;
- `summarize_context.py`;
- simple command examples;
- no third-party dependencies unless clearly justified.

Out of scope:

- full CLI framework;
- database access;
- embedding generation;
- target repo code analysis.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-06.1 | As a maintainer, I want `scaffold_feature.py` so a new feature package can be created from templates. | Speed. |
| US-06.2 | As a reviewer, I want `factory_check.py` so required artifacts and traceability expectations can be validated. | Quality. |
| US-06.3 | As a long-running task owner, I want `summarize_context.py` so work can resume after context compaction. | Continuity. |

### Definition of Done

- Scripts run with standard Python.
- Scripts have help output.
- Scripts avoid private assumptions.
- Scripts are covered by basic smoke examples.

## EPIC-07 - Public Fake Example

Status: draft

### Business Outcome

Show how the factory works end-to-end without exposing real customer or private
project data.

### Scope

In scope:

- fake login migration example;
- package index;
- behavior inventory;
- parity plan;
- User Story;
- Hard Spec;
- ADR;
- implementation brief;
- review/QA;
- closeout.

Out of scope:

- real code migration;
- real customer names;
- real issue IDs.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-07.1 | As a new user, I want a fake example so I can understand the factory without private context. | Adoption. |
| US-07.2 | As a maintainer, I want the example to pass `factory_check.py` so it proves the scripts and templates align. | Validation. |

### Definition of Done

- Example includes all required artifacts.
- Example contains no real private data.
- Example passes the factory check.

## EPIC-08 - Release Readiness

Status: draft

### Business Outcome

Prepare the V0 repository for public GitHub publication after explicit approval.

### Scope

In scope:

- license decision;
- contribution guide;
- public safety review;
- README polish;
- local smoke checks;
- release checklist.

Out of scope:

- pushing to GitHub without explicit approval;
- publishing packages;
- enabling integrations.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-08.1 | As a maintainer, I want a license and contribution guide so public usage expectations are clear. | Public readiness. |
| US-08.2 | As a maintainer, I want a public-safety review so no private data is shipped. | Safety. |
| US-08.3 | As a maintainer, I want a release checklist so publication is deliberate. | Governance. |

### Definition of Done

- User explicitly approves publication scope.
- Repo contains no private data.
- Smoke checks pass.
- Next release step is clear.

## Spike Candidates

| ID | Question | Timing | Output |
| --- | --- | --- | --- |
| SP-01 | Should the factory be packaged as a Codex plugin after V0? | After skill works locally. | Plugin packaging decision. |
| SP-02 | Should Supabase persistence/search be part of this repo or a separate adapter repo? | After V0 publication. | Adapter architecture decision. |
| SP-03 | Should hooks be repo-local examples only or also user-level examples? | Before release readiness. | Hook distribution decision. |

## Immediate Next Work Queue

1. Create repository folder structure.
2. Create `docs/architecture/clean-architecture.md`.
3. Create `docs/workflow/factory-workflow.md`.
4. Create `templates/core/migration-package-index.md`.
5. Create all V0 migration templates.
6. Create agent role docs.
7. Create the Codex skill.
8. Create minimal scripts.
9. Create fake login migration example.
10. Run local checks and public-safety review.

## Global Definition Of Done

- V0 artifacts exist and are internally linked.
- Factory check passes on the fake example.
- README explains usage and boundaries.
- No private or customer-specific data is present.
- No GitHub publication occurs without explicit user approval.
