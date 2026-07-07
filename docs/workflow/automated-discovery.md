# Automated Discovery And Package Generation

Status: draft
Audience: migration orchestrators, maintainers, Codex users

## Purpose

Automated discovery turns a source repository into a migration starting point:

1. discover source entry points;
2. create a source feature inventory;
3. generate one draft migration package per discovered feature;
4. build a recommended migration roadmap;
5. optionally generate technical foundation and mock/model-governance strategy
   from the inventory and target context.

This is automation for discovery and planning. Autonomous gated migration builds
on this by adding behavior proof, candidate-final specs and code patch
generation with human approval gates.

## Automation Boundary

The factory may automatically create:

- feature candidate metadata;
- migration package folders;
- draft intake, behavior inventory, parity plan and spec artifacts;
- roadmap recommendations;
- discovery-only traceability seeds.

The factory must not automatically approve:

- complete behavior understanding;
- implementation readiness;
- target architecture fit;
- parity validation;
- safe production rollout.

Implementation starts only after the generated package is reviewed and updated
with behavior evidence, validation strategy, architecture boundaries and an
implementation brief.

For the higher-autonomy target mode, see
[Autonomous Gated Migration](autonomous-gated-migration.md).

## Pipeline

```text
source repo
  -> discover_features.py
  -> source-feature-inventory.md / discovery.json
  -> generate_migration_packages.py
  -> packages/<feature-slug>/
  -> build_migration_roadmap.py
  -> migration-roadmap.md
  -> generate_technical_foundation.py
  -> generate_mock_and_model_governance.py
```

## Supported Discovery Heuristics

The V0.2 automation layer uses dependency-free heuristics for common entry
points:

| Stack | Signals |
| --- | --- |
| Java / Spring | `@GetMapping`, `@PostMapping`, `@PutMapping`, `@PatchMapping`, `@DeleteMapping`, `@RequestMapping`, `@Scheduled`, `@KafkaListener`, `@JmsListener`, `@RabbitListener` |
| OpenAPI | `openapi` or `swagger` files with `paths` and HTTP methods |
| Node / Express-style HTTP | `app.get`, `app.post`, `router.get`, `router.post`, `put`, `patch`, `delete`, `all` |
| Python / FastAPI or Flask style | `@app.get`, `@router.post`, `@blueprint.route`, and similar route decorators |

Heuristics intentionally produce candidates. They are allowed to miss or
over-split features. The review gate corrects the package before
implementation.

## Classification

| Candidate | Default Risk | Recommended Next Gate |
| --- | --- | --- |
| Read/query API | low | legacy behavior inventory |
| Mutation API | medium | behavior parity plan |
| Scheduled job | medium | behavior inventory plus side-effect review |
| Event/listener | high | Spike before implementation |
| Unknown route or mixed behavior | medium | Spike or manual discovery |

## Commands

Discover features as Markdown:

```sh
python3 scripts/discover_features.py \
  --source examples/fake-source-service \
  --source-name "Fake Source Service" \
  --output /tmp/source-feature-inventory.md
```

Discover features as JSON:

```sh
python3 scripts/discover_features.py \
  --source examples/fake-source-service \
  --source-name "Fake Source Service" \
  --format json \
  --output /tmp/discovery.json
```

Generate packages:

```sh
python3 scripts/generate_migration_packages.py \
  --inventory-json /tmp/discovery.json \
  --target-system "Target Service" \
  --output-root /tmp/migration-packages
```

Build the roadmap:

```sh
python3 scripts/build_migration_roadmap.py \
  --inventory-json /tmp/discovery.json \
  --packages-root /tmp/migration-packages \
  --output /tmp/migration-roadmap.md
```

Generate mock/model governance after the roadmap:

```sh
python3 scripts/generate_mock_and_model_governance.py \
  --inventory-json /tmp/discovery.json \
  --target-system "Target Service" \
  --code-root examples/fake-source-service \
  --output /tmp/mock-server-and-model-governance.md
```

One command can also scan and create packages:

```sh
python3 scripts/generate_migration_packages.py \
  --source examples/fake-source-service \
  --source-name "Fake Source Service" \
  --target-system "Target Service" \
  --output-root /tmp/migration-packages \
  --write-inventory /tmp/source-feature-inventory.md \
  --write-inventory-json /tmp/discovery.json
```

## Output Discipline

Generated artifacts should:

- store source-relative anchors such as `src/main/.../Controller.java:42`;
- avoid copying source code excerpts;
- mark packages as discovery drafts;
- keep unresolved behavior questions visible;
- block implementation until behavior and parity evidence are reviewed.

## Review Gate

Before a generated package becomes implementation-ready:

- confirm the discovered entry point is a real feature slice;
- merge or split packages when the scanner over-splits or under-splits;
- fill legacy behavior inventory with observable behavior;
- define parity evidence;
- identify target module ownership;
- record architecture decisions;
- update the implementation brief.

## Search Anchors

- automated discovery
- package generation
- source feature inventory
- migration roadmap
- automatic migration factory
