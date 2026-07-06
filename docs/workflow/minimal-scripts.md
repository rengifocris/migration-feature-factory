# Minimal Scripts

Status: draft
Audience: maintainers, Codex users

## Purpose

The scripts provide deterministic helpers for scaffolding, checking and
summarizing migration packages. They are intentionally small adapters around
the Markdown templates.

They do not inspect target application code, connect to databases, generate
embeddings or replace review judgment.

## Scripts

| Script | Purpose |
| --- | --- |
| `scripts/scaffold_feature.py` | Create a migration package from templates. |
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
