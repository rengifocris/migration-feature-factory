# V0 Release Checklist

Status: passed
Date: 2026-07-06

## Release Scope

V0 includes:

- public-safe repository rules and README;
- clean architecture and decision support docs;
- migration workflow and traceability harness docs;
- V0 artifact templates;
- agent role contracts;
- repo-scoped Codex skill;
- optional Codex hook example;
- minimal standard-library scripts;
- fake login migration example;
- contribution guide;
- MIT License.

V0 excludes:

- Supabase persistence;
- semantic search;
- dashboards;
- package publication;
- managed hooks;
- real migration data;
- real target application code.

## Checklist

| Gate | Status | Evidence |
| --- | --- | --- |
| License decision exists | passed | `LICENSE`, `docs/release/license-decision.md` |
| Contribution guide exists | passed | `CONTRIBUTING.md` |
| README points to main usage paths | passed | `README.md` |
| Fake example passes factory check | passed | `python3 scripts/factory_check.py --strict-placeholders examples/fake-login-migration` |
| Scripts compile | passed | `python3 -m py_compile ...` |
| Hook example parses as JSON | passed | `python3 -m json.tool .codex/hooks.json.example` |
| Codex skill validates | passed | skill validator output: `Skill is valid!` |
| Public-safety scan reviewed | passed | `docs/release/public-safety-review.md` |
| Git diff whitespace check passes | passed | `git diff --check` |

## Smoke Commands

```sh
git diff --check
python3 -m py_compile scripts/scaffold_feature.py scripts/factory_check.py scripts/summarize_context.py
python3 scripts/factory_check.py --strict-placeholders examples/fake-login-migration
python3 scripts/factory_check.py --light examples/fake-login-migration
python3 scripts/summarize_context.py examples/fake-login-migration
python3 -m json.tool .codex/hooks.json.example >/dev/null
python3 "$SKILL_CREATOR_DIR/scripts/quick_validate.py" .agents/skills/migration-feature-factory
```

## Release Decision

Recommendation: treat the repository as V0 release-ready.

Reason:

- All planned V0 factory surfaces exist.
- The fake example passes the factory check.
- Public-safety review passed.
- The repository has explicit contribution and license expectations.

## Next Work

- Decide whether to tag `v0.1.0`.
- Decide whether to package the factory as a Codex plugin.
- Decide whether Supabase persistence/search belongs in this repository or a
  separate adapter repository.
