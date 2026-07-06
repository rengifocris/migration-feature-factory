# Mock Server, Synthetic Data And Model Governance

Status: draft
Audience: architects, developers, spec owners, QA reviewers

## Purpose

This workflow gate defines how a migration package uses mock servers,
synthetic data and model governance before implementation starts.

It exists because behavior parity is not only an API-contract problem. Many
migrations also depend on external clients, enrichment flows, generated DTOs,
manual mappers, canonical models, validation rules and failure semantics.

## Boundary

The factory may generate:

- a mock-server strategy;
- a synthetic scenario matrix;
- happy, edge and bad fixture profiles;
- a model-governance policy;
- code-context signal tables using terms and source-relative anchors;
- Mermaid diagrams for mock and model flows;
- validation gates.

The factory must not:

- copy source code excerpts into generated docs;
- copy production or private payloads into synthetic data;
- decide a company-specific mock-server tool without platform approval;
- merge enrichment behavior into the non-enriched baseline model without an
  accepted change request;
- claim behavior parity before tests or evidence exist.

## Recommended Default

For non-trivial service migrations:

- use in-process fakes for fast application/use-case tests;
- use a contract-backed mock server for adapter, ACL and E2E parity tests;
- keep synthetic data deterministic, small and fake;
- cover happy, edge and bad cases explicitly;
- preserve the non-enriched source/canonical record;
- expose enriched records as separate read/result models;
- keep generated DTOs at the web/client boundary;
- curate internal models only where behavior, invariants or readability justify
  them;
- test mappers with fixture pairs;
- record every fixture and model decision in the package index or ADR.

## When To Run This Gate

Run this gate after technical foundation generation and before implementation
briefs are accepted when any of these are true:

- the feature uses external services, clients, ACLs or adapters;
- the feature enriches source data before exposing it;
- generated DTOs or client models could leak into application/domain code;
- mapper behavior affects observable output;
- parity tests need upstream happy, edge or bad cases;
- real upstream systems are unavailable, unsafe or too slow for automated
  tests.

## Decision Points

| Decision | Option A | Option B | Recommendation |
| --- | --- | --- | --- |
| Use-case test doubles | mock server everywhere | in-process fakes for use cases | in-process fakes for speed and focused assertions |
| Adapter/ACL validation | hand-written client stubs | contract-backed mock server | mock server for protocol and failure parity |
| Source record handling | mutate the record during enrichment | preserve raw and expose enriched separately | preserve non-enriched baseline and assemble enriched output separately |
| DTO/model policy | generated DTOs everywhere | boundary DTOs plus curated internal models | boundary DTOs; curated models only where justified |
| Fixture strategy | one large example payload | scenario-specific fixtures | one fixture profile per behavior risk |

## Code-Context Discovery

The generator can scan optional code roots for configured terms. The output is
limited to:

- matched term;
- classification;
- source-relative anchor;
- required action.

It does not copy code lines or private payloads.

Suggested scan terms:

```text
model
dto
mapper
client
adapter
acl
canonical
record
enrich
enrichment
validator
```

Teams can pass company or domain terms through `--scan-term` and
`--domain-context`. Those terms remain in private target artifacts, not in the
public factory repository.

## Command

```sh
python3 scripts/generate_mock_and_model_governance.py \
  --inventory-json /path/to/source-feature-inventory.json \
  --target-system "Target Service" \
  --target-pom /path/to/pom.xml \
  --code-root /path/to/source-or-target-code \
  --scan-term "enrichment" \
  --domain-context "Preserve the non-enriched source record" \
  --language-policy spanish-first \
  --output /path/to/mock-server-and-model-governance.md
```

## Review Gate

Before accepting the generated artifact:

- confirm the mock-server tool or testing approach is approved by the target
  platform;
- confirm the scenario matrix includes happy, edge and bad cases;
- confirm no production/private payloads are copied into fixtures;
- confirm generated DTOs, curated models, mappers, clients and validators have
  clear boundaries;
- confirm raw/non-enriched and enriched models are distinct where required;
- link the accepted decisions to package ADRs, parity plans and implementation
  briefs.

## Search Anchors

- mock server and model governance
- synthetic data generation
- parity fixtures
- code context signals
- generated dto boundary
- enriched record
- non enriched record
