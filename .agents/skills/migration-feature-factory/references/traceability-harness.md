# Traceability Harness Reference

Use this reference to keep migration artifacts connected across iterations.

## Package Index Discipline

The package index is the coordination point. Update it when:

- an artifact is created, moved or superseded;
- lifecycle state changes;
- a decision is accepted;
- a blocker appears or clears;
- validation evidence changes;
- new input is classified;
- closeout is updated.

## Required Links

Keep these links current:

| Source | Must Link To |
| --- | --- |
| Legacy behavior inventory | Parity evidence and affected acceptance criteria. |
| User Story | Behavior IDs and acceptance criteria. |
| Hard Spec | Acceptance criteria, architecture decisions and validation evidence. |
| Architecture decision | Constraints, tradeoffs and affected implementation boundaries. |
| Implementation brief | Scope, non-goals, behavior IDs, files and required tests. |
| Review/QA | Acceptance criteria, parity evidence and residual risk. |
| Closeout | Changed files/artifacts, validation, decisions and follow-ups. |

## Context Pack

Before compaction, handoff or closeout, keep a compact context pack with:

- current lifecycle state;
- last completed gate;
- next action;
- key decisions;
- open blockers;
- artifacts to inspect first;
- validation already run;
- validation still missing.

## Consistency Checks

Before saying a package is ready:

- every known legacy behavior maps to evidence or a documented gap;
- every acceptance criterion maps to Hard Spec coverage;
- every Hard Spec requirement maps to validation evidence or accepted risk;
- every architecture constraint maps to a decision or boundary;
- every change request is classified;
- every blocker has an owner and next action;
- closeout states what changed, what did not change and residual risk.

## Public Safety

For public examples, use fake systems, fake IDs and generic behavior. Do not
store real customer names, private repo paths, secrets, raw chats or proprietary
source excerpts.
