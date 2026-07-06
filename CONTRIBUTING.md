# Contributing

Status: active

## Purpose

This repository is public-safe by design. Contributions should improve the
factory without adding private migration data or unnecessary machinery.

## Before You Change Files

- Read `AGENTS.md`.
- Keep examples fake and generic.
- Prefer Markdown-first changes before adding code.
- Use scripts only for deterministic scaffold, check or context-summary work.
- Keep hooks as examples unless users intentionally copy and trust them.

## Public Safety

Do not add:

- real customer or client data;
- credentials, tokens, private keys or connection strings;
- private repository paths;
- raw chat logs, raw email exports or raw sensitive source material;
- proprietary implementation copied from a private codebase.

Use fake products, fake systems, fake IDs and generic behavior in examples.

## Contribution Workflow

1. Keep the change scoped to one backlog item or coherent improvement.
2. Update the nearest index, README or backlog when discoverability changes.
3. Preserve behavior-first migration language:
   legacy behavior is the contract, architecture may improve internally.
4. Run local checks before proposing or pushing a change.
5. Document validation evidence in the final note or PR description.

## Local Checks

Run the checks that match the change:

```sh
git diff --check
python3 -m py_compile scripts/scaffold_feature.py scripts/factory_check.py scripts/summarize_context.py
python3 scripts/factory_check.py --strict-placeholders examples/fake-login-migration
python3 -m json.tool .codex/hooks.json.example >/dev/null
```

Run the public-safety scan:

```sh
rg -n -i --hidden "/users/|software_development|gho_|sk-|secret[^s]|password|api[_-]?key|connection string|private key" . --glob '!**/.git/**'
```

The scan can report intentional safety wording. Review every hit before
committing.

## Pull Request Expectations

- State what changed.
- State what did not change.
- List checks run.
- Note residual risks or intentionally deferred work.
- Do not include private source snippets or private customer context.
