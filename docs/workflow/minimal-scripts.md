# Minimal Scripts

Status: draft
Audience: maintainers, Codex users

## Purpose

The scripts provide deterministic helpers for discovery, scaffolding, checking
and summarizing migration packages. They are intentionally small adapters around
the Markdown templates.

They do not connect to databases, generate embeddings, perform code migration
or replace review judgment.

## Scripts

| Script | Purpose |
| --- | --- |
| `scripts/scaffold_feature.py` | Create a migration package from templates. |
| `scripts/discover_features.py` | Scan a source repo for likely API, job and listener entry points. |
| `scripts/generate_migration_packages.py` | Create one draft migration package per discovered source feature. |
| `scripts/build_migration_roadmap.py` | Build a recommended migration order from discovery output. |
| `scripts/generate_technical_foundation.py` | Generate technical foundation and architecture blueprint docs. |
| `scripts/generate_mock_and_model_governance.py` | Generate mock-server, synthetic-data and model-governance docs. |
| `scripts/factory_check.py` | Validate required package files, index sections, artifact links and basic public-safety signals. |
| `scripts/summarize_context.py` | Print or write a compact context summary from the package index. |

## Command Examples

Create a package:

```sh
python3 scripts/scaffold_feature.py \
  --feature "Fake Login Migration" \
  --feature-id "FAKE-LOGIN-001" \
  --legacy-system "Legacy Auth" \
  --target-system "Target Auth" \
  --output examples/fake-login-migration
```

Check a package:

```sh
python3 scripts/factory_check.py examples/fake-login-migration
```

Run a light check suitable for optional hooks:

```sh
python3 scripts/factory_check.py --light examples/fake-login-migration
```

Print a context summary:

```sh
python3 scripts/summarize_context.py examples/fake-login-migration
```

Write a context summary:

```sh
python3 scripts/summarize_context.py \
  examples/fake-login-migration \
  --output examples/fake-login-migration/context-summary.md
```

Discover fake source features:

```sh
python3 scripts/discover_features.py \
  --source examples/fake-source-service \
  --source-name "Fake Source Service" \
  --output /tmp/source-feature-inventory.md
```

Generate packages from fake source discovery:

```sh
python3 scripts/generate_migration_packages.py \
  --source examples/fake-source-service \
  --source-name "Fake Source Service" \
  --target-system "Target Service" \
  --output-root /tmp/migration-packages \
  --write-inventory /tmp/source-feature-inventory.md \
  --write-inventory-json /tmp/discovery.json
```

Build a roadmap:

```sh
python3 scripts/build_migration_roadmap.py \
  --inventory-json /tmp/discovery.json \
  --packages-root /tmp/migration-packages \
  --output /tmp/migration-roadmap.md
```

Generate a technical foundation:

```sh
python3 scripts/generate_technical_foundation.py \
  --inventory-json /tmp/discovery.json \
  --target-system "Target Service" \
  --language-policy english \
  --output /tmp/technical-foundation.md
```

Generate mock-server, synthetic-data and model-governance strategy:

```sh
python3 scripts/generate_mock_and_model_governance.py \
  --inventory-json /tmp/discovery.json \
  --target-system "Target Service" \
  --language-policy english \
  --code-root examples/fake-source-service \
  --output /tmp/mock-server-and-model-governance.md
```

## Smoke Examples

Use a temporary directory when testing script behavior without changing the
repository:

```sh
tmpdir="$(mktemp -d)"
python3 scripts/scaffold_feature.py \
  --feature "Smoke Migration" \
  --feature-id "SMOKE-001" \
  --legacy-system "Legacy Demo" \
  --target-system "Target Demo" \
  --output "$tmpdir/smoke-migration"
python3 scripts/factory_check.py "$tmpdir/smoke-migration"
python3 scripts/factory_check.py --light "$tmpdir/smoke-migration"
python3 scripts/summarize_context.py "$tmpdir/smoke-migration"
python3 scripts/discover_features.py \
  --source examples/fake-source-service \
  --source-name "Fake Source Service" \
  --format json \
  --output "$tmpdir/discovery.json"
python3 scripts/generate_migration_packages.py \
  --inventory-json "$tmpdir/discovery.json" \
  --target-system "Target Service" \
  --output-root "$tmpdir/packages"
python3 scripts/build_migration_roadmap.py \
  --inventory-json "$tmpdir/discovery.json" \
  --packages-root "$tmpdir/packages" \
  --output "$tmpdir/migration-roadmap.md"
python3 scripts/generate_technical_foundation.py \
  --inventory-json "$tmpdir/discovery.json" \
  --target-system "Target Service" \
  --language-policy english \
  --output "$tmpdir/technical-foundation.md"
python3 scripts/generate_mock_and_model_governance.py \
  --inventory-json "$tmpdir/discovery.json" \
  --target-system "Target Service" \
  --language-policy english \
  --code-root examples/fake-source-service \
  --output "$tmpdir/mock-server-and-model-governance.md"
```

Fresh scaffolds may produce placeholder warnings until the package is filled.
Factory check exits non-zero only for errors.

## Hook Compatibility

The optional `.codex/hooks.json.example` file calls:

- `scripts/factory_check.py --light` after edits;
- `scripts/summarize_context.py` before compaction;
- `scripts/factory_check.py` when the turn stops.

If `MIGRATION_FACTORY_PACKAGE` is set, hooks pass that package path to the
scripts. If no package is discoverable, the scripts skip safely.
