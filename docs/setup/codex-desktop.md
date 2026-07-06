# Codex Desktop Setup

Status: draft
Audience: Codex Desktop users and maintainers

## Purpose

This guide explains how to use Migration Feature Factory from Codex Desktop.

The recommended setup keeps workflow, enforcement and repository instructions
separate:

```text
Skill: reusable migration workflow
AGENTS.md: repository expectations
Hooks: optional mechanical checks
Scripts: deterministic validation helpers
Templates: artifact contracts
```

## Recommended V0 Setup

1. Open this repository in Codex Desktop.
2. Keep the factory workflow in a repo-scoped skill under `.agents/skills`.
3. Keep repo expectations in `AGENTS.md`.
4. Keep hook examples under `.codex/hooks.json.example`.
5. Do not enable hooks automatically. Copy and trust hooks only after reviewing
   the command scripts they run.

## Expected Repository Shape

```text
migration-feature-factory/
  AGENTS.md
  .agents/
    skills/
      migration-feature-factory/
        SKILL.md
        references/
  .codex/
    hooks.json.example
  scripts/
    scaffold_feature.py
    factory_check.py
    summarize_context.py
  templates/
  docs/
```

## Codex Surfaces

Use the smallest Codex surface that matches the need.

| Need | Surface |
| --- | --- |
| One-off instruction for the current conversation | Prompt/thread context |
| Durable repo convention | `AGENTS.md` |
| Reusable migration workflow | Skill |
| Mechanical validation around lifecycle events | Hook |
| Deterministic check or scaffold | Script |
| Future installable bundle | Plugin |

## Skill Setup

Codex can discover repository skills from `.agents/skills` in the repository.
The V0 factory should place the migration skill here:

```text
.agents/skills/migration-feature-factory/SKILL.md
```

The skill should be focused and use progressive disclosure:

- `SKILL.md` contains trigger rules and the workflow summary;
- detailed instructions live in `references/`;
- scripts are called only when deterministic checks are needed.

Example prompt:

```text
$migration-feature-factory
Create a migration package for the fake login flow. Preserve legacy behavior,
use clean architecture proportionally, and produce the parity plan first.
```

## AGENTS.md Setup

The repository `AGENTS.md` should define durable expectations:

- public-safe content only;
- no real customer data;
- behavior parity is mandatory for migration examples;
- prefer Markdown-first workflow before scripts;
- run the factory check before claiming a package is complete.

`AGENTS.md` is not the skill. It is the repo's standing instruction layer.

## Hook Setup

Hooks should be optional in V0.

Recommended examples:

```text
Stop:
  python scripts/factory_check.py examples/fake-login-migration

PreCompact:
  python scripts/summarize_context.py examples/fake-login-migration

PostToolUse:
  python scripts/factory_check.py examples/fake-login-migration --light
```

Notes:

- Codex hooks are enabled by default in Codex, but non-managed command hooks
  require review and trust before they run.
- Keep public hook files as examples, not active local policy.
- Prefer git-root-based paths in hook commands so they work from subfolders.
- Hook scripts must not print secrets, credentials or private source content.

## Codex Desktop Settings

In Codex Desktop, use Settings for common app behavior and `config.toml` for
advanced configuration. Useful areas:

- Integrations and MCP: connect tools only when the factory needs them.
- Git: standardize commit and PR conventions if desired.
- Browser: enable only for frontend or documentation verification needs.
- Agent configuration: adjust sandbox and approval behavior according to the
  repository risk.

## Operating Flow In Codex Desktop

1. Start a thread in this repository.
2. Ask Codex to use the migration factory skill.
3. Scaffold or create a feature package.
4. Fill intake, legacy behavior and parity plan before implementation.
5. Use the decision support contract when architecture or validation choices
   arise.
6. Run `factory_check.py`.
7. Update the context pack before long pauses or compaction.
8. Commit and push only reviewed public-safe changes.

## Source Notes

This setup follows current Codex behavior:

- Codex Desktop uses the same agent configuration model as CLI and IDE for
  advanced options.
- Skills are available in Codex Desktop and can be discovered from repository
  `.agents/skills` folders.
- `AGENTS.md` provides durable repo guidance.
- Hooks are lifecycle enforcement around Codex events and must be reviewed and
  trusted when they are non-managed command hooks.

Official references:

- https://developers.openai.com/codex/app/settings
- https://developers.openai.com/codex/skills
- https://developers.openai.com/codex/guides/agents-md
- https://developers.openai.com/codex/hooks
