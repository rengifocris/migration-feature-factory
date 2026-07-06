# Agent Roles

Status: draft
Audience: migration orchestrators, contributors, Codex users

## Purpose

Agent roles define responsibility boundaries for Migration Feature Factory.

Agents are not personalities. They are scoped responsibilities with explicit
inputs, outputs, allowed decisions, forbidden decisions, evidence requirements
and blocked protocols.

## Role Set

| Role | Primary Responsibility | Main Output |
| --- | --- | --- |
| [Migration Orchestrator](migration-orchestrator.md) | Own lifecycle, gates, routing and synthesis. | Updated package index and handoffs. |
| [Legacy Analyst](legacy-analyst.md) | Extract observable legacy behavior and evidence. | Legacy behavior inventory. |
| [Product Owner / Business Analyst](product-owner-business-analyst.md) | Convert goals and behavior into product scope. | Epic/User Story inputs and scope decisions. |
| [Spec Owner](spec-owner.md) | Align stories, specs, spikes and implementation contracts. | Hard Spec and implementation readiness. |
| [Architect](architect.md) | Choose proportional target architecture and boundaries. | Architecture decision. |
| [Developer](developer.md) | Implement approved scope in the target repo. | Implementation summary and evidence. |
| [Peer Reviewer](peer-reviewer.md) | Challenge assumptions, scope and architecture before build or closeout. | Proceed/revise/spike/stop decision. |
| [Code Reviewer](code-reviewer.md) | Review concrete diffs for correctness and maintainability. | Approve/request changes/block decision. |
| [QA Reviewer](qa-reviewer.md) | Validate acceptance criteria and behavior parity evidence. | Pass/fail QA decision. |
| [Technical Writer](technical-writer.md) | Keep documentation, closeout and public-safe wording clear. | Updated docs and closeout language. |

## Common Contract

Every agent role must define:

- mission;
- when to use;
- inputs;
- outputs;
- allowed decisions;
- forbidden decisions;
- evidence required;
- handoff contract;
- blocked protocol.

## Shared Rules

- Legacy behavior is the contract.
- Observable behavior changes require a separate approved story.
- Use the decision support contract when a material choice is needed.
- Offer one or two serious options plus a recommendation.
- Recommend a Spike when evidence is insufficient.
- Keep peer review, code review and QA review separate.
- Do not paste raw private source material into public artifacts.

## Handoff Shape

```markdown
## Handoff

- Source role:
- Target role:
- Mission:
- Inputs:
- Non-goals:
- Required output:
- Evidence required:
- Blocked protocol:
```

## Search Anchors

Terms people might search for:

- migration agents
- agent roles
- role contracts
- handoff contract
- peer reviewer
- code reviewer
- QA reviewer
- migration orchestrator
