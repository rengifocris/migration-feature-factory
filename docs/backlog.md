# Migration Feature Factory Backlog

Status: V0.5 autonomous gated migration defined
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
| 10 | EPIC-10 | Epic | Technical foundation generation | completed | Architecture blueprint, generation policy, patterns and diagrams. |
| 11 | EPIC-11 | Epic | Mock server, synthetic data and model governance | completed | Mock strategy, happy/edge/bad synthetic data and raw/enriched model governance. |
| 12 | EPIC-12 | Epic | Autonomous gated migration mode | completed | Automatic behavior proof, candidate-final specs, code patches and architecture-tool decisions with human gates. |
| 13 | EPIC-13 | Epic | Capability grouping guardrail | completed | Raw endpoint discovery can be grouped into capability-level package candidates before roadmap and package generation. |

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

## EPIC-10 - Technical Foundation Generation

Status: completed

### Business Outcome

Generate architecture and technical foundation specs before package-scale code
generation or implementation begins.

### Scope

In scope:

- technical foundation template;
- architecture blueprint generation;
- stack and company-library detection from target build metadata where
  available;
- DTO/model/ACL generation policy;
- vertical slice and design-pattern recommendations;
- code style and defensive-programming rules;
- Mermaid architecture and slice diagrams;
- validation gates.

Out of scope:

- automatic production code generation;
- behavior proof without legacy evidence;
- target architecture decisions without review;
- replacing company standards or target repo rules.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-10.1 | As an architect, I want a generated technical foundation so stack, slicing and pattern decisions are explicit before implementation. | Architecture clarity. |
| US-10.2 | As a developer, I want DTO/model/ACL generation rules so generated code does not leak into domain logic. | Maintainability. |
| US-10.3 | As a reviewer, I want diagrams and validation gates so design intent and quality checks are reviewable. | Review quality. |
| US-10.4 | As a migration orchestrator, I want foundation decisions linked to packages so every feature follows the same rules. | Consistency. |

### Definition of Done

- Technical foundation template exists.
- Generator script exists.
- Workflow docs explain the boundary and review gate.
- Skill and README reference the generator.
- Generated output includes recommendation, decisions, generation policy, code
  style, validation gates and diagrams.

### Progress

- [x] `templates/architecture/technical-foundation.md` exists.
- [x] `scripts/generate_technical_foundation.py` exists.
- [x] `docs/workflow/technical-foundation-generation.md` exists.
- [x] README and skill reference the new capability.
- [x] Generator supports English and Spanish-first output.

## EPIC-11 - Mock Server, Synthetic Data And Model Governance

Status: completed

### Business Outcome

Generate the testing and model-governance foundation needed before migrating
features that depend on external clients, enrichment flows, generated DTOs,
mappers, validators or canonical records.

### Scope

In scope:

- mock-server strategy template;
- synthetic test data plan template;
- model-governance template;
- generator for mock-server, synthetic-data and model-governance docs;
- optional code-context signal scanning that stores terms and anchors, not code
  excerpts;
- Spanish-first and English output support;
- workflow docs and skill/README references.

Out of scope:

- automatic production code generation;
- choosing a company-specific mock-server tool without platform approval;
- storing production or private payloads;
- claiming parity without tests and review evidence;
- making the public factory specific to one company or domain.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-11.1 | As a QA reviewer, I want a mock-server strategy so integration and parity tests can simulate happy, edge and bad upstream behavior. | Regression control. |
| US-11.2 | As a developer, I want synthetic fixture governance so tests are deterministic, fake and traceable. | Maintainability. |
| US-11.3 | As an architect, I want model governance so generated DTOs, raw records, enriched records, clients, ACLs and mappers have explicit boundaries. | Architecture clarity. |
| US-11.4 | As a migration orchestrator, I want code-context signals so source terms and anchors can seed model decisions without copying private source code. | Safe automation. |

### Definition of Done

- Templates exist for mock strategy, synthetic data and model governance.
- Generator script exists and supports inventory JSON plus optional code-root
  scanning.
- Workflow docs explain boundaries, defaults, commands and review gates.
- README, backlog, vision, factory workflow, minimal scripts and skill reference
  the capability.
- Generated artifacts remain drafts until platform, architecture and QA review
  accept them.

### Progress

- [x] `templates/testing/mock-server-strategy.md` exists.
- [x] `templates/testing/synthetic-test-data-plan.md` exists.
- [x] `templates/architecture/model-governance.md` exists.
- [x] `scripts/generate_mock_and_model_governance.py` exists.
- [x] `docs/workflow/mock-server-and-model-governance.md` exists.
- [x] README, vision, skill and minimal script docs reference the new capability.

## EPIC-12 - Autonomous Gated Migration Mode

Status: completed

### Business Outcome

Define the target factory mode where automation performs the full migration
loop while human gates approve final behavior baselines, specs, architecture
decisions, code application, merge and release.

### Scope

In scope:

- automatic behavior proof target capability;
- final-candidate Epic/User Story/Hard Spec generation rules;
- automatic code migration patch flow;
- company-specific architecture tool recommendation flow;
- status vocabulary for generated, candidate-final, approved, applied and
  rejected artifacts;
- human gate rules for approval, merge, deployment and architecture adoption;
- public-safe workflow documentation.

Out of scope:

- implementing unattended production migration;
- bypassing target repo CI, tests or architecture rules;
- committing, pushing, opening PRs, merging or deploying without explicit
  approval;
- storing private behavior evidence in the public repository.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-12.1 | As a QA reviewer, I want the factory to generate and run behavior proof automatically so parity evidence is produced before implementation. | Regression control. |
| US-12.2 | As a product/spec owner, I want generated Epics and User Stories to become candidate-final automatically when traceability is complete. | Throughput. |
| US-12.3 | As a developer, I want the factory to generate and apply code patches after gates are approved so migration execution becomes repeatable. | Delivery speed. |
| US-12.4 | As an architect, I want company-specific tools and libraries detected and recommended automatically so platform fit is explicit. | Architecture governance. |
| US-12.5 | As an approver, I want human gates before approval, merge, deployment and architecture adoption so automation remains controlled. | Safety. |

### Definition of Done

- Autonomous gated migration workflow doc exists.
- README, vision, factory workflow, automated discovery and skill reference the
  capability.
- Status vocabulary distinguishes generated output from approved output.
- Human gates are explicit for behavior baseline, specs, code patches,
  architecture-tool decisions, merge and deployment.

### Progress

- [x] `docs/workflow/autonomous-gated-migration.md` exists.
- [x] README references autonomous gated migration.
- [x] Vision and factory workflow describe the target mode.
- [x] Backlog captures follow-up implementation stories.

## EPIC-13 - Capability Grouping Guardrail

Status: completed

### Business Outcome

Prevent raw endpoint discovery from becoming an inflated implementation backlog
when the real migration scope is a smaller set of capabilities.

### Scope

In scope:

- capability backlog generation from discovery JSON;
- optional project rules for known capability names and match terms;
- Markdown and JSON capability backlog output;
- workflow documentation that treats endpoints as behavior evidence;
- package generation from capability backlog JSON.

Out of scope:

- deciding private project capability names in the public repository;
- proving behavior automatically;
- generating or applying code patches.

### Candidate Stories

| ID | Story | Value |
| --- | --- | --- |
| US-13.1 | As a migration orchestrator, I want endpoint discoveries grouped into capabilities so the roadmap reflects the real migration plan. | Scope control. |
| US-13.2 | As an architect, I want optional grouping rules so company or product boundaries can guide package generation without hardcoding private context. | Architecture fit. |
| US-13.3 | As a reviewer, I want endpoint membership preserved as evidence so traceability is not lost when packages are merged. | Auditability. |

### Definition of Done

- `scripts/group_inventory_capabilities.py` exists.
- Automated discovery docs recommend capability grouping for non-trivial
  services.
- Minimal script docs include grouping in the smoke flow.
- Package generation can consume capability backlog JSON.

### Progress

- [x] Capability grouping script exists.
- [x] Workflow docs explain endpoint evidence versus implementation packages.
- [x] README and minimal scripts reference the guardrail.

## Spike Candidates

| ID | Question | Timing | Output |
| --- | --- | --- | --- |
| SP-01 | Should the factory be packaged as a Codex plugin after V0? | After skill works locally. | Plugin packaging decision. |
| SP-02 | Should Supabase persistence/search be part of this repo or a separate adapter repo? | After V0 publication. | Adapter architecture decision. |
| SP-03 | Should hooks be repo-local examples only or also user-level examples? | Before release readiness. | Hook distribution decision. |
| SP-04 | Should automated discovery move from regex heuristics to language-specific AST adapters? | After V0.2 usage on real repos. | Analyzer adapter decision. |
| SP-05 | Should the factory generate code scaffolds after technical foundation approval? | After V0.3 target validation. | Code generation boundary decision. |
| SP-06 | Should the mock/model generator emit tool-specific fixtures for approved stacks? | After V0.4 target validation. | Mock adapter generation decision. |
| SP-07 | Which behavior-proof runner should be implemented first: API contract comparison, existing test mining or golden-master capture? | Before behavior-proof implementation. | Behavior proof runner decision. |
| SP-08 | Should code migration generate patches only or also manage branches/PR drafts? | Before code-patch implementation. | Code execution boundary decision. |

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
16. [x] Create technical foundation generator.
17. [x] Create mock-server, synthetic-data and model-governance generator.
18. [x] Define autonomous gated migration mode.
19. [x] Add capability grouping guardrail.
20. [ ] Run automation against the first private source repo and review the generated packages.
21. [ ] Implement behavior proof runner.
22. [ ] Implement candidate-final spec promotion checks.
23. [ ] Implement gated code patch generation.

## Global Definition Of Done

- Core artifacts exist and are internally linked.
- Factory check passes on the fake example.
- README explains usage and boundaries.
- No private or customer-specific data is present.
- Public GitHub publication only contains reviewed public-safe content.
