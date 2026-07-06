# Migration Feature Factory

Status: draft planning scaffold

Migration Feature Factory is a public-safe system for moving legacy features into
new applications or services while preserving observable behavior and improving
internal architecture.

The core rule:

> Legacy behavior is the contract. Architecture may improve internally.
> Observable behavior changes require a separate approved story.

## Start Here

- [Vision](docs/vision.md): product direction, architecture principles, agents,
  skills, hooks, scripts and public/private boundaries.
- [Backlog](docs/backlog.md): ordered implementation backlog for building the
  factory.

## Scope

V0 is Markdown-first:

- reusable workflow documentation;
- migration templates;
- agent role contracts;
- a Codex skill;
- optional Codex hook examples;
- minimal scripts for scaffold, checks and context summaries;
- a fake public example with no real customer data.

Supabase, semantic search, dashboards and external integrations are future
adapters, not V0 dependencies.

## Public Safety

This repository must not contain:

- real client/customer migration data;
- secrets, credentials, keys or connection strings;
- private repo paths that identify sensitive work;
- raw chat logs, raw exports or unnecessary personal data.

Use fake examples and generic terminology in public documentation.
