# Change Intake Reference

Use this reference whenever new information appears after a package has started.

## Rule

Do not silently fold new input into the migration. Classify it, update impacted
artifacts and record the decision in the package index.

## Classification Guide

| Classification | Keep In Current Migration? | Required Action |
| --- | --- | --- |
| Legacy behavior clarification | Usually yes. | Update behavior inventory, parity plan and affected specs. |
| Target architecture constraint | Yes when mandatory or already accepted. | Add or update an architecture decision and implementation brief. |
| Behavior-preserving improvement | Yes when observable behavior is unchanged. | Document as internal improvement and validate parity. |
| New feature | No. | Create or route to a separate product/design flow. |
| Scope conflict | Not until approved. | Present options and request a decision. |
| Unknown / Spike needed | No. | Create a Spike before implementation. |

## Company Libraries And Platform Constraints

When the user mentions a company-provided library or platform architecture:

1. Treat it as a possible architecture constraint, not an automatic rewrite.
2. Check whether it provides required behavior, governance, security,
   observability, compatibility or platform conventions.
3. Offer one or two options plus a recommendation when adoption affects design.
4. Update the architecture decision, Hard Spec, implementation brief and review
   evidence after acceptance.

Do not wrap a required platform library behind an abstraction unless the target
repository has a real need to replace it independently.

## New Feature Routing

If the requested work is not behavior-preserving migration:

- name the feature request;
- state why it is outside migration scope;
- create a User Story, Hard Spec or Spike only if the user asks to continue;
- link it from the migration package as follow-up work when relevant.

## Update Checklist

After a change is accepted, update:

- package index change log;
- traceability matrix;
- affected intake, inventory, parity plan, story, spec or decision;
- implementation brief;
- review/QA expectations;
- closeout or context pack when the package is near completion.
