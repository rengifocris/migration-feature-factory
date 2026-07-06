#!/usr/bin/env python3
"""Generate migration packages for discovered source features."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace

SCRIPT_DIR = Path(__file__).resolve().parent
if str(SCRIPT_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPT_DIR))

import discover_features as discovery
import scaffold_feature as scaffold


PLACEHOLDER_RE = re.compile(r"<[^>\n]+>")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create one migration package per discovered source feature."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--source", type=Path, help="Source repository path to scan.")
    source_group.add_argument(
        "--inventory-json",
        type=Path,
        help="Discovery JSON previously written by discover_features.py.",
    )
    parser.add_argument("--source-name", help="Display name for the source system.")
    parser.add_argument("--target-system", default="target-system")
    parser.add_argument("--output-root", required=True, type=Path)
    parser.add_argument("--owner", default="migration-orchestrator")
    parser.add_argument("--id-prefix", default="AUTO")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument("--sensitivity", default="internal")
    parser.add_argument("--language-policy", default="match target project")
    parser.add_argument("--include-tests", action="store_true")
    parser.add_argument("--limit", type=int, help="Limit packages created.")
    parser.add_argument("--force", action="store_true", help="Overwrite generated files.")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--write-inventory",
        type=Path,
        help="Optional markdown source inventory output.",
    )
    parser.add_argument(
        "--write-inventory-json",
        type=Path,
        help="Optional discovery JSON output.",
    )
    return parser.parse_args()


def load_payload(args: argparse.Namespace) -> dict[str, object]:
    if args.inventory_json:
        return json.loads(args.inventory_json.read_text(encoding="utf-8"))

    source = args.source.resolve()
    if not source.is_dir():
        raise FileNotFoundError(f"Source directory not found: {source}")
    source_name = args.source_name or source.name
    features = discovery.discover_features(source, args.include_tests, args.id_prefix)
    return discovery.inventory_payload(source, source_name, features)


def write_optional_inventory(payload: dict[str, object], args: argparse.Namespace) -> None:
    if args.write_inventory:
        discovery.write_output(discovery.render_markdown_inventory(payload), args.write_inventory)
    if args.write_inventory_json:
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
        discovery.write_output(text, args.write_inventory_json)


def text_feature(feature: dict[str, object], key: str) -> str:
    return str(feature.get(key, "")).strip()


def behavior_sentence(feature: dict[str, object]) -> str:
    trigger = text_feature(feature, "trigger") or text_feature(feature, "operation")
    kind = text_feature(feature, "kind")
    return f"Preserve observable behavior for discovered {kind} entry point `{trigger}`."


def source_anchor(feature: dict[str, object]) -> str:
    return text_feature(feature, "source_anchor") or (
        f"{text_feature(feature, 'source_path')}:{text_feature(feature, 'line')}"
    )


def placeholder_value(
    placeholder: str, feature: dict[str, object], args: argparse.Namespace
) -> str:
    label = placeholder.strip("<>").lower()
    if "role" in label or "owner" in label:
        return args.owner
    if "feature" in label or "migration slice" in label or "short title" in label:
        return text_feature(feature, "name")
    if "legacy" in label or "source" in label:
        return args.source_name or "source system"
    if "target" in label:
        return args.target_system
    if "behavior" in label or "capability" in label or "requirement" in label:
        return behavior_sentence(feature)
    if "endpoint" in label or "entry" in label:
        return text_feature(feature, "trigger") or "source entry point"
    if ("path" in label or "reference" in label) and (
        "source" in label or "legacy" in label
    ):
        return source_anchor(feature)
    if "path" in label or "reference" in label:
        return "related artifact pending"
    if "risk" in label or "impact" in label or "mitigation" in label:
        return "to be assessed during discovery"
    if "decision" in label or "recommendation" in label or "option" in label:
        return "complete discovery before deciding"
    if "question" in label:
        return "Which target boundary should own this migration slice?"
    if "notes" in label or "term" in label:
        return "to be discovered"
    return "to be discovered"


def common_replacements(text: str, feature: dict[str, object], args: argparse.Namespace) -> str:
    replacements = {
        "Sensitivity: public-safe-example | internal | confidential": f"Sensitivity: {args.sensitivity}",
        "Language policy: English only | match target project": f"Language policy: {args.language_policy}",
        "Related package index: `../core/migration-package-index.md`": "Related package index: `migration-package-index.md`",
        "Related Epic: `<path-or-none>`": "Related Epic: `epic.md`",
        "Related Hard Spec: `<path-or-none>`": "Related Hard Spec: `hard-spec.md`",
        "Related Epic/User Story: `<path>`": "Related Epic/User Story: `user-story.md`",
        "Related behavior inventory: `<path>`": "Related behavior inventory: `legacy-behavior-inventory.md`",
        "Related parity plan: `<path>`": "Related parity plan: `behavior-parity-plan.md`",
        "- Lifecycle state: draft | discovery | parity-planning | spec-ready |\n  implementation-ready | in-progress | blocked | validated | closed": "- Lifecycle state: discovery",
        "- Current gate:": "- Current gate: automated discovery",
        "- Last completed gate:": "- Last completed gate: source feature discovery",
        "- Next action:": "- Next action: review generated inventory and fill legacy behavior evidence",
        "- Blocked by:": "- Blocked by: behavior evidence and target boundary not yet confirmed",
        "- Unit tests:": "- Unit tests: pending feature-specific behavior evidence",
        "- Integration tests:": "- Integration tests: pending feature-specific behavior evidence",
        "- Contract/API tests:": "- Contract/API tests: pending feature-specific behavior evidence",
        "- E2E tests:": "- E2E tests: pending feature-specific behavior evidence",
        "- Manual evidence:": "- Manual evidence: pending source behavior review",
        "- Not validated:": "- Not validated: behavior parity and target implementation",
        "- Short summary:": f"- Short summary: generated package for `{text_feature(feature, 'name')}`",
        "- Key decisions:": "- Key decisions: generated package is discovery-only; no implementation approved",
        "- Current blockers:": "- Current blockers: behavior contract and target boundary are not yet confirmed",
        "- Files/artifacts to inspect first:": "- Files/artifacts to inspect first: `feature-intake.md`, `legacy-behavior-inventory.md`, `behavior-parity-plan.md`",
        "- Next prompt:": "- Next prompt: inspect source behavior and target architecture boundary for this package",
        "- Approved behavior changes:": "- Approved behavior changes: none",
        "- Behavior changes explicitly not approved:": "- Behavior changes explicitly not approved: any observable difference from the legacy behavior",
        "- New-feature candidates to split:": "- New-feature candidates to split: any behavior not present in the legacy source",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = text.replace("YYYY-MM-DD", args.date)
    text = PLACEHOLDER_RE.sub(lambda match: placeholder_value(match.group(0), feature, args), text)
    return text


def seed_section(feature: dict[str, object]) -> str:
    notes = ", ".join(feature.get("notes", [])) if isinstance(feature.get("notes"), list) else ""
    return (
        "\n## Automated Discovery Seed\n\n"
        f"- Candidate ID: {text_feature(feature, 'feature_id')}\n"
        f"- Candidate: `{text_feature(feature, 'name')}`\n"
        f"- Type: {text_feature(feature, 'kind')}\n"
        f"- Operation: {text_feature(feature, 'operation')}\n"
        f"- Trigger: `{text_feature(feature, 'trigger')}`\n"
        f"- Source anchor: `{source_anchor(feature)}`\n"
        f"- Risk: {text_feature(feature, 'risk')}\n"
        f"- Scanner notes: {notes or 'none'}\n"
        "- Status: discovery seed only; inspect the source before implementation.\n"
    )


def render_file(
    template_text: str,
    destination: str,
    feature: dict[str, object],
    args: argparse.Namespace,
) -> str:
    scaffold_args = SimpleNamespace(
        feature=text_feature(feature, "name"),
        feature_id=text_feature(feature, "feature_id"),
        legacy_system=args.source_name or "source system",
        target_system=args.target_system,
        owner=args.owner,
        date=args.date,
    )
    text = scaffold.render_template(template_text, scaffold_args, destination)
    text = common_replacements(text, feature, args)

    if destination == "migration-package-index.md":
        text = text.replace(
            "to be discovered\n\n## Current Status",
            f"{behavior_sentence(feature)}\n\n## Current Status",
        )
        text = re.sub(
            r"^\| `?[^|]+`? \| LB-01 \| [^|]+ \| `?[^|]+`? \| EV-01 \| pending \|$",
            (
                f"| `{source_anchor(feature)}` | LB-01 | {behavior_sentence(feature)} "
                "| `legacy-behavior-inventory.md` | EV-01 | pending |"
            ),
            text,
            flags=re.MULTILINE,
        )
        text = re.sub(
            r"^\| \d{4}-\d{2}-\d{2} \| ADR-01 \| [^|]+ \| [^|]+ \| [^|]+ \| `?[^|]+`? \|$",
            (
                f"| {args.date} | ADR-01 | Generate a discovery draft package only. "
                "| generate package automatically; create package manually "
                "| generate package automatically, then review before implementation "
                "| `architecture-decision.md` |"
            ),
            text,
            flags=re.MULTILINE,
        )
        text = re.sub(
            r"^\| \d{4}-\d{2}-\d{2} \| CHG-01 \| [^|]+ \| [^|]+ \| `?[^|]+`? \| [^|]+ \|$",
            (
                f"| {args.date} | CHG-01 | Add generated discovery package. "
                "| automated discovery seed | all package artifacts | accepted |"
            ),
            text,
            flags=re.MULTILINE,
        )

    if destination in {
        "feature-intake.md",
        "legacy-behavior-inventory.md",
        "behavior-parity-plan.md",
        "implementation-brief.md",
    }:
        text = text.rstrip() + "\n" + seed_section(feature)
    return text.rstrip() + "\n"


def package_path(output_root: Path, feature: dict[str, object]) -> Path:
    return output_root / text_feature(feature, "slug")


def create_package(
    feature: dict[str, object],
    args: argparse.Namespace,
    root: Path,
) -> tuple[Path, str]:
    destination_root = package_path(args.output_root, feature)
    existing = [
        destination_root / item[1]
        for item in scaffold.ARTIFACTS
        if (destination_root / item[1]).exists()
    ]
    if existing and not args.force:
        return destination_root, "skipped-existing"

    if args.dry_run:
        return destination_root, "would-create"

    destination_root.mkdir(parents=True, exist_ok=True)
    for template, destination in scaffold.ARTIFACTS:
        template_path = root / template
        template_text = template_path.read_text(encoding="utf-8")
        rendered = render_file(template_text, destination, feature, args)
        (destination_root / destination).write_text(rendered, encoding="utf-8")
    return destination_root, "created"


def main() -> int:
    args = parse_args()
    root = Path(__file__).resolve().parents[1]

    try:
        payload = load_payload(args)
    except (FileNotFoundError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    if args.source_name is None:
        args.source_name = str(payload.get("source_name") or "source system")

    write_optional_inventory(payload, args)
    features = payload.get("features", [])
    if not isinstance(features, list):
        print("Inventory JSON has no features list.", file=sys.stderr)
        return 2

    selected = features[: args.limit] if args.limit else features
    results: list[tuple[Path, str, str]] = []
    for feature in selected:
        if not isinstance(feature, dict):
            continue
        path, status = create_package(feature, args, root)
        results.append((path, status, text_feature(feature, "name")))

    for path, status, name in results:
        print(f"{status}: {name} -> {path}")

    if not results:
        print("No feature candidates found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
