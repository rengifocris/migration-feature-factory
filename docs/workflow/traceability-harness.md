# Traceability Harness And Hooks

Status: draft
Audience: migration orchestrators, QA reviewers, Codex users

## Purpose

The traceability harness keeps a migration package coherent across iterations,
review cycles and context compaction.

The package index is the source of truth. Hooks and scripts are adapters that
help check the index, but they do not replace human review.

## Core Rule

Every legacy behavior, accepted requirement, architecture decision, change
request and validation result must be findable from the package index.

If the link is missing, the package is not ready.

## Stable IDs

Use short, stable IDs in package artifacts:

| Prefix | Meaning | Example |
| --- | --- | --- |
| `LB` | Legacy behavior | `LB-01` |
| `AC` | Acceptance criterion | `AC-01` |
| `HS` | Hard Spec requirement | `HS-01` |
| `ADR` | Architecture decision | `ADR-01` |
| `EV` | Validation evidence | `EV-01` |
| `CHG` | Change intake item | `CHG-01` |
| `R` | Risk | `R-01` |

Do not reuse an ID after deleting or superseding content. Mark it superseded
and create a new ID when the meaning changes.

## Package Index Updates

Update the package index when:

- an artifact is created, moved, renamed or superseded;
- lifecycle state changes;
- a decision is accepted;
- a blocker appears or clears;
- validation evidence changes;
- a change request is classified;
- closeout is updated.

## Traceability Matrix Rules

Each traceability row must include:

- source evidence or artifact;
- behavior, requirement or decision ID;
- target artifact section;
- validation evidence or explicit gap;
- status.

Use these statuses:

| Status | Meaning |
| --- | --- |
| `pending` | Known but not yet mapped or validated. |
| `planned` | Target artifact and validation path are defined. |
| `validated` | Evidence exists and passed. |
| `gap` | Evidence is missing and risk is open. |
| `accepted-risk` | Missing or partial evidence was approved. |
| `superseded` | Replaced by a newer row or decision. |

Rules:

- Every `LB` must map to validation evidence or a documented gap.
- Every `AC` must map to at least one `HS`.
- Every `HS` must map to validation evidence or accepted risk.
- Every architecture constraint must map to an `ADR` or implementation boundary.
- Every `CHG` must map to affected artifacts and a decision.

## Change Log Rules

Do not silently mutate scope. For every meaningful new input:

1. Create or update a `CHG` row.
2. Classify the change.
3. List impacted artifacts.
4. Record the decision or decision owner.
5. Update the affected artifacts.

Use the change intake template when the change affects behavior, architecture,
validation, scope, risk or delivery sequence.

## Context Pack

Before compaction, handoff or closeout, update the package context pack with:

- current lifecycle state;
- current gate;
- last completed gate;
- key decisions;
- open blockers;
- artifacts to inspect first;
- validation already run;
- validation still missing;
- next prompt.

## Optional Hook Examples

The repository provides an inert hook example at:

```text
.codex/hooks.json.example
```

It is not active unless a user copies it to `.codex/hooks.json`, reviews it and
trusts it in Codex.

Current Codex hook behavior to account for:

- project-local hooks load only when the project `.codex/` layer is trusted;
- non-managed command hooks require review and trust before running;
- commands run from the session working directory;
- hook commands should resolve paths from the git root;
- multiple matching hooks may run concurrently;
- hook examples must not print secrets, raw private source, prompts or customer
  data.

## Hook-To-Script Mapping

The example hooks map Codex lifecycle events to the future minimal scripts from
EPIC-06.

| Event | Matcher | Script | Purpose |
| --- | --- | --- | --- |
| `PostToolUse` | `Bash|apply_patch|Edit|Write` | `scripts/factory_check.py --light` | Fast artifact consistency check after edits. |
| `PreCompact` | `manual|auto` | `scripts/summarize_context.py` | Refresh the context pack before compaction. |
| `Stop` | none | `scripts/factory_check.py` | Full package consistency check when the turn ends. |

If a hook runs outside a migration package and no `MIGRATION_FACTORY_PACKAGE`
environment variable is set, the scripts skip safely.

## Validation Checklist

- [ ] Package index artifact table is current.
- [ ] Traceability matrix has no orphan behaviors, criteria or requirements.
- [ ] Change log has every meaningful new input.
- [ ] Decision log records accepted architecture or validation decisions.
- [ ] Context pack can resume the work after compaction.
- [ ] Hook examples remain inert unless intentionally copied and trusted.
