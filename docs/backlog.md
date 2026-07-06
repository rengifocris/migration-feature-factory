# Migration Feature Factory Backlog

Status: V0.2 automation layer implemented
Language policy: English only
Owner: local maintainer

## Current Objective

Build a public-safe Migration Feature Factory:

- Markdown-first;
- clean architecture and SOLID principles;
- agents, skills and optional hooks;
- minimal scripts plus safe automation;
- fake example only;
- no private data;
- no Supabase dependency in the current core.

## Delivery Order

| Order | ID | Type | Title | Status | Notes |
| --- | --- | --- | --- | --- | --- |
| 0 | INIT-00 | Setup | Vision and backlog packet | completed | Created this planning baseline. |
| 1 | EPIC-01 | Epic | Public repo foundation | completed | Repo shape, safety, contribution docs. |
| 2 | EPIC-02 | Epic | Core migration workflow and templates | completed | Factory gates and artifact contracts. |
| 3 | EPIC-03 | Epic | Agent role system | completed | Responsibility boundaries and handoff contracts. |
| 4 | EPIC-04 | Epic | Codex skill package | completed | Reusable skill and references. |
| 5 | EPIC-05 | Epic | Traceability harness and hooks | completed | Package index, checks and hook examples. |
| 6 | EPIC-06 | Epic | Minimal scripts | completed | Scaffold, check and context summary. |
| 7 | EPIC-07 | Epic | Public fake example | completed | Demonstrates end-to-end migration package. |
| 8 | EPIC-08 | Epic | Release readiness | completed | License, README polish, checks and public safety review. |
| 9 | EPIC-09 | Epic | Automated discovery and package generation | completed | Source feature inventory, generated packages and roadmap. |

## EPIC-01 - Public Repo Foundation

Status: completed

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
| US-01.4 | As a Codex Desktop user, I want setup guidance so I can use the factory from the app without guessing where skills, hooks and instructions live. | Adoption. |

### Definition of Done

- README links to vision, backlog and future docs.
- Public/private boundary is explicit.
- Codex Desktop setup guidance exists.
- No real customer data is present.

### Progress

- [x] Root README exists.
- [x] Repository `AGENTS.md` exists.
- [x] Clean architecture guidance exists.
- [x] Codex Desktop setup guidance exists.
- [x] Contribution guide exists.
- [x] Release/public-safety checklist exists.

## EPIC-02 - Core Migration Workflow And Templates

Status: completed

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
| US-02.7 | As a decision maker, I want one or two viable options plus a recommendation so validation, architecture and scope decisions are clear. | Decision quality. |

### Definition of Done

- All V0 templates exist.
- Required sections are consistent.
- Templates include status, sensitivity, scope, evidence and Search Anchors or
  terminology sections where useful.

### Progress

- [x] Factory workflow exists.
- [x] Migration package index template exists.
- [x] Feature intake template exists.
- [x] Legacy behavior inventory template exists.
- [x] Behavior parity plan template exists.
- [x] Change intake template exists.
- [x] Migration-ready Epic template exists.
- [x] Migration-ready User Story template exists.
- [x] Migration-ready Hard Spec template exists.
- [x] Migration-ready Spike template exists.
- [x] Architecture decision template exists.
- [x] Implementation brief template exists.
- [x] Review / QA template exists.
- [x] Closeout template exists.

## EPIC-03 - Agent Role System

Status: completed

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

### Progress

- [x] Agent role index exists.
- [x] Migration orchestrator role exists.
- [x] Legacy analyst role exists.
- [x] Product Owner / Business Analyst role exists.
- [x] Spec owner role exists.
- [x] Architect role exists.
- [x] Developer role exists.
- [x] Peer reviewer role exists.
- [x] Code reviewer role exists.
- [x] QA reviewer role exists.
- [x] Technical writer role exists.

## EPIC-04 - Codex Skill Package

Status: completed

### Business Outcome

Make the factory reusable from Codex through a focused skill that routes work to
the migration workflow and references.

### Scope

In scope:

- `.agents/skills/migration-feature-factory/SKILL.md`;
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

### Progress

- [x] Repo-scoped Codex skill exists.
- [x] Skill references are split from `SKILL.md`.
- [x] Skill classifies migration, constraints, improvements, new features,
      conflicts and Spikes.
- [x] Skill states when not to use the factory.

## EPIC-05 - Traceability Harness And Hooks

Status: completed

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

### Progress

- [x] Traceability harness documentation exists.
- [x] Package index template includes ID, matrix, decision, change and risk
      traceability rules.
- [x] Change intake template includes a stable change ID.
- [x] Optional `.codex/hooks.json.example` exists and is inert by default.
- [x] Hook-to-script mapping is documented for EPIC-06 scripts.

## EPIC-06 - Minimal Scripts

Status: completed

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

### Progress

- [x] `scripts/scaffold_feature.py` exists.
- [x] `scripts/factory_check.py` exists.
- [x] `scripts/summarize_context.py` exists.
- [x] Minimal scripts documentation exists with command and smoke examples.
- [x] Optional hook example maps to real scripts.

## EPIC-07 - Public Fake Example

Status: completed

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

### Progress

- [x] Fake login migration package exists under `examples/fake-login-migration`.
- [x] Package index links all artifacts.
- [x] Behavior inventory, parity plan, User Story, Hard Spec, ADR,
      implementation brief, review/QA and closeout exist.
- [x] Example passes `factory_check.py`.

## EPIC-08 - Release Readiness

Status: completed

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

### Progress

- [x] MIT License exists.
- [x] License decision exists.
- [x] Contribution guide exists.
- [x] README has release-readiness links.
- [x] Public-safety review exists.
- [x] Release checklist exists.
- [x] Local smoke checks pass.
- [x] Next release steps are documented.

## EPIC-09 - Automated Discovery And Package Generation

Status: completed

### Business Outcome

Turn "migrate all features from this source repo" into an actionable migration
roadmap with one draft package per discovered source feature.

### Scope

In scope:

- source feature discovery for common API, job and listener entry points;
- source feature inventory output;
- draft package generation for every discovered candidate;
- generated discovery seed sections;
- migration roadmap with recommended ordering;
- fake public source fixture for smoke validation.

Out of scope:

- automatic behavior proof;
- automatic code migration;
- target architecture selection without review;
- production readiness claims;
- storing private source excerpts in public artifacts.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-09.1 | As a migration orchestrator, I want source feature discovery so a large legacy repo can be converted into migration candidates quickly. | Speed. |
| US-09.2 | As a spec owner, I want one draft package per discovered feature so each slice has a place for behavior, parity and decisions. | Traceability. |
| US-09.3 | As a reviewer, I want a generated roadmap so migration order starts with lower-risk, easier-to-validate slices. | Risk control. |
| US-09.4 | As a maintainer, I want generated artifacts to avoid source excerpts so the public factory remains safe. | Public safety. |

### Definition of Done

- Discovery script exists and supports Markdown and JSON output.
- Package generation script creates draft packages from discovery output.
- Roadmap script creates a recommended migration order.
- Automation workflow is documented.
- README, vision, skill and minimal script docs reference the automation layer.
- Fake source fixture validates the workflow without private data.

### Progress

- [x] `scripts/discover_features.py` exists.
- [x] `scripts/generate_migration_packages.py` exists.
- [x] `scripts/build_migration_roadmap.py` exists.
- [x] `docs/workflow/automated-discovery.md` exists.
- [x] README and vision describe the automation boundary.
- [x] Fake source fixture exists.
- [x] Generated packages remain discovery drafts.

## Spike Candidates

| ID | Question | Timing | Output |
| --- | --- | --- | --- |
| SP-01 | Should the factory be packaged as a Codex plugin after V0? | After skill works locally. | Plugin packaging decision. |
| SP-02 | Should Supabase persistence/search be part of this repo or a separate adapter repo? | After V0 publication. | Adapter architecture decision. |
| SP-03 | Should hooks be repo-local examples only or also user-level examples? | Before release readiness. | Hook distribution decision. |
| SP-04 | Should automated discovery move from regex heuristics to language-specific AST adapters? | After V0.2 usage on real repos. | Analyzer adapter decision. |

## Immediate Next Work Queue

1. [x] Create repository folder structure.
2. [x] Create `docs/architecture/clean-architecture.md`.
3. [x] Create `docs/architecture/decision-support.md`.
4. [x] Create `docs/setup/codex-desktop.md`.
5. [x] Create `docs/workflow/factory-workflow.md`.
6. [x] Create `templates/core/migration-package-index.md`.
7. [x] Create remaining V0 migration/product/review templates.
8. [x] Create agent role docs.
9. [x] Create the Codex skill.
10. [x] Create traceability harness and hook examples.
11. [x] Create minimal scripts.
12. [x] Create fake login migration example.
13. [x] Run local checks and public-safety review.
14. [x] Create automated discovery scripts.
15. [x] Document automated discovery and package generation.
16. [ ] Run automation against the first private source repo and review the generated packages.

## Global Definition Of Done

- Core artifacts exist and are internally linked.
- Factory check passes on the fake example.
- README explains usage and boundaries.
- No private or customer-specific data is present.
- Public GitHub publication only contains reviewed public-safe content.
