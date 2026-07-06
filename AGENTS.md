# AGENTS.md

## Repository Purpose

This repository defines Migration Feature Factory: a public-safe system for
preserving legacy behavior while migrating features into cleaner target
architectures.

## Public Safety

Do not add:

- real customer or client data;
- secrets, credentials, tokens, private keys or connection strings;
- private repository paths;
- raw chat logs, raw email exports or raw sensitive source material;
- proprietary implementation details copied from a private codebase.

Use fake examples, generic identifiers and public-safe wording.

## Core Rule

Legacy behavior is the contract.

Architecture may improve internally. Observable behavior changes require a
separate approved story.

## Engineering Principle

Be minimalist, not simplistic.

Use the smallest structure that protects behavior, boundaries, invariants,
validation and future maintainability. Do not add DDD, ports/adapters, patterns,
hooks or scripts as decoration.

## Architecture Expectations

- Keep the core workflow independent from Codex, Supabase, GitHub, Jira and any
  programming language.
- Treat skills, hooks, scripts and future persistence layers as adapters.
- Keep templates focused on one responsibility.
- Make decision points explicit with one or two serious options and a
  recommendation.
- Use Spikes when evidence is insufficient for a responsible recommendation.

## Artifact Expectations

When adding or changing factory artifacts:

- update the nearest index or README when discoverability changes;
- keep statuses honest: `draft`, `active`, `blocked`, `validated`,
  `superseded` or `archived`;
- preserve links between package index, behavior inventory, parity plan, specs,
  decisions, implementation briefs and review evidence;
- keep examples fake and public-safe;
- prefer Markdown-first workflow before adding scripts.

## Codex Surface Rules

- Use `AGENTS.md` for durable repo expectations.
- Use `.agents/skills` for reusable Codex workflows.
- Use `.codex/hooks.json.example` only for optional hook examples.
- Use scripts only for deterministic scaffold, check or context-summary work.
- Do not enable hooks automatically for users.

## Validation

Before closing a meaningful change:

- run `git diff --check`;
- scan for private or secret-looking content;
- inspect the changed Markdown for broken local references when practical;
- summarize what changed and what was not validated.

Suggested public-safety scan:

```sh
rg -n -i "secret|password|token|api[_-]?key|connection string|private key|/users/" . --glob '!**/.git/**'
```

The scan may find intentional safety wording. Review hits before committing.

## Git

- Keep commits small and coherent.
- Do not publish real client data.
- Do not rewrite public history unless explicitly requested and justified.
- Push only reviewed public-safe changes.
