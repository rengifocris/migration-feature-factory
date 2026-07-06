# Technical Foundation Generation

Status: draft
Audience: architects, spec owners, developers, reviewers

## Purpose

Technical foundation generation creates the architecture and implementation
rules that all generated migration packages must follow.

It answers questions such as:

- Which stack and company libraries are mandatory?
- Should the migration use vertical slices, layered modules, ports/adapters or
  another target pattern?
- Which artifacts can be generated safely?
- Which artifacts require human engineering judgment?
- Where should DTOs, models, mappers, validators and ACLs live?
- Which code style and validation rules are non-negotiable?

## Boundary

The factory may generate:

- technical foundation spec;
- architecture blueprint;
- option/recommendation tables;
- package/module blueprint;
- DTO/model/ACL generation policy;
- code style and defensive-programming rules;
- Mermaid diagrams;
- validation gates.

The factory must not generate production code from this artifact alone. Code
generation begins only after a migration package has behavior evidence, parity
plan, Hard Spec and accepted architecture decision.

## Recommended Architecture Default

Default recommendation for non-trivial API migrations:

- vertical slices by feature/API area;
- generated OpenAPI DTOs stay at the web/client boundary;
- application use cases own orchestration;
- domain models are curated only where business rules or invariants exist;
- adapters or ACLs isolate legacy/external/company-library contracts;
- mappers are explicit where behavior or compatibility matters;
- guard clauses protect invalid state early;
- ArchUnit or equivalent tests protect boundaries where available.

This is clean architecture applied proportionally. It is not pattern dumping.

## Decision Points

| Decision | Option A | Option B | Recommendation |
| --- | --- | --- | --- |
| Slicing | Technical layers only | Vertical slices by feature/API area | Vertical slices with clean internal boundaries |
| DTOs | Use generated DTOs everywhere | Boundary DTOs only | Boundary DTOs only; curate internal models |
| ACLs | Direct integration calls | Adapter/ACL boundary | Adapter/ACL for external, legacy or company contracts |
| Domain model | Generate from contracts | Curate where invariants exist | Curate only where business behavior justifies it |
| Defensive style | Fail later in services | Guard clauses at boundaries and use cases | Guard clauses with normalized errors |

## Command

```sh
python3 scripts/generate_technical_foundation.py \
  --inventory-json /path/to/source-feature-inventory.json \
  --target-system "Target Service" \
  --target-pom /path/to/pom.xml \
  --language-policy spanish-first \
  --output /path/to/technical-foundation.md
```

## Review Gate

Before accepting the generated technical foundation:

- confirm the target stack and company libraries;
- decide whether generated DTO packages are boundary-only;
- decide the vertical slice naming convention;
- decide when ACLs are required;
- decide which architecture tests enforce boundaries;
- record accepted decisions in package ADRs and implementation briefs.

## Search Anchors

- technical foundation generation
- architecture blueprint
- generated DTO policy
- ACL policy
- vertical slice migration
- defensive programming
- guard clauses
