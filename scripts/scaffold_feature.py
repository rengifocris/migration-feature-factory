#!/usr/bin/env python3
"""Create a migration feature package from the repository templates."""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path


ARTIFACTS = [
    ("templates/core/migration-package-index.md", "migration-package-index.md"),
    ("templates/migration/feature-intake.md", "feature-intake.md"),
    ("templates/migration/legacy-behavior-inventory.md", "legacy-behavior-inventory.md"),
    ("templates/migration/behavior-parity-plan.md", "behavior-parity-plan.md"),
    ("templates/migration/change-intake.md", "change-intake.md"),
    ("templates/product/epic.md", "epic.md"),
    ("templates/product/user-story.md", "user-story.md"),
    ("templates/product/hard-spec.md", "hard-spec.md"),
    ("templates/product/spike.md", "spike.md"),
    ("templates/migration/architecture-decision.md", "architecture-decision.md"),
    ("templates/migration/implementation-brief.md", "implementation-brief.md"),
    ("templates/review/review-qa.md", "review-qa.md"),
    ("templates/migration/closeout.md", "closeout.md"),
]

PACKAGE_INDEX_PATHS = {
    "| Epic | not-started | `<path>`": "| Epic | draft | `epic.md`",
    "| User Story | not-started | `<path>`": "| User Story | draft | `user-story.md`",
    "| Hard Spec | not-started | `<path>`": "| Hard Spec | draft | `hard-spec.md`",
    "| Spike | not-started | `<path>`": "| Spike | draft | `spike.md`",
    "| Architecture Decision | not-started | `<path>`": (
        "| Architecture Decision | draft | `architecture-decision.md`"
    ),
    "| Implementation Brief | not-started | `<path>`": (
        "| Implementation Brief | draft | `implementation-brief.md`"
    ),
    "| Review / QA | not-started | `<path>`": "| Review / QA | draft | `review-qa.md`",
    "| Closeout | not-started | `<path>`": "| Closeout | draft | `closeout.md`",
}


def repo_root() -> Path:
    return Path(__file__).resolve().parents[1]


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "feature"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scaffold a behavior-preserving migration package."
    )
    parser.add_argument("--feature", required=True, help="Human-readable feature name.")
    parser.add_argument("--feature-id", required=True, help="Stable feature ID.")
    parser.add_argument("--legacy-system", default="<legacy-system>")
    parser.add_argument("--target-system", default="<target-system>")
    parser.add_argument("--owner", default="migration-orchestrator")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument(
        "--output",
        type=Path,
        help="Output directory. Defaults to packages/<feature-slug>.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite scaffolded files that already exist.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Print files that would be created without writing them.",
    )
    return parser.parse_args()


def replacements(args: argparse.Namespace) -> dict[str, str]:
    migration_slice = args.feature
    return {
        "<Feature Name>": args.feature,
        "<Migration Outcome>": args.feature,
        "<Migration Slice>": migration_slice,
        "<Migration Uncertainty>": f"{args.feature} uncertainty",
        "<Short Title>": args.feature,
        "<feature-id>": args.feature_id,
        "<legacy-system>": args.legacy_system,
        "<target-system>": args.target_system,
        "<owner-or-role>": args.owner,
        "YYYY-MM-DD": args.date,
    }


def render_template(text: str, args: argparse.Namespace, destination: str) -> str:
    for old, new in replacements(args).items():
        text = text.replace(old, new)

    if destination == "migration-package-index.md":
        for old, new in PACKAGE_INDEX_PATHS.items():
            text = text.replace(old, new)
        text = text.replace(
            "| User Story | draft | `user-story.md` | <role>",
            "| User Story | draft | `user-story.md` | product-owner-business-analyst",
        )
        text = text.replace(
            "| Hard Spec | draft | `hard-spec.md` | <role>",
            "| Hard Spec | draft | `hard-spec.md` | spec-owner",
        )
        text = text.replace(
            "| Architecture Decision | draft | `architecture-decision.md` | <role>",
            "| Architecture Decision | draft | `architecture-decision.md` | architect",
        )
        text = text.replace(
            "| Implementation Brief | draft | `implementation-brief.md` | <role>",
            "| Implementation Brief | draft | `implementation-brief.md` | developer",
        )
        text = text.replace(
            "| Review / QA | draft | `review-qa.md` | <role>",
            "| Review / QA | draft | `review-qa.md` | qa-reviewer",
        )
        text = text.replace(
            "| Closeout | draft | `closeout.md` | <role>",
            "| Closeout | draft | `closeout.md` | migration-orchestrator",
        )

    return text


def target_dir(args: argparse.Namespace) -> Path:
    if args.output:
        return args.output
    return Path("packages") / slugify(args.feature)


def validate_targets(output: Path, force: bool) -> list[str]:
    if force:
        return []

    existing = []
    for _, destination in ARTIFACTS:
        path = output / destination
        if path.exists():
            existing.append(str(path))
    return existing


def main() -> int:
    args = parse_args()
    root = repo_root()
    output = target_dir(args)
    existing = validate_targets(output, args.force)

    if existing:
        print("Refusing to overwrite existing files. Use --force if intended.", file=sys.stderr)
        for path in existing:
            print(f"- {path}", file=sys.stderr)
        return 2

    planned = [output / destination for _, destination in ARTIFACTS]
    if args.dry_run:
        print(f"Would create migration package: {output}")
        for path in planned:
            print(path)
        return 0

    output.mkdir(parents=True, exist_ok=True)
    for source, destination in ARTIFACTS:
        template_path = root / source
        destination_path = output / destination
        text = template_path.read_text(encoding="utf-8")
        destination_path.write_text(render_template(text, args, destination), encoding="utf-8")

    print(f"Created migration package: {output}")
    print(f"Next: python3 scripts/factory_check.py {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
