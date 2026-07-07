#!/usr/bin/env python3
"""Group raw discovery entries into capability-level migration candidates."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
from collections import defaultdict
from pathlib import Path
from typing import Any


HTTP_MUTATIONS = {"POST", "PUT", "PATCH", "DELETE"}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Create a capability backlog from raw discovery inventory. "
            "Use this before package generation when endpoint discovery "
            "over-splits the real migration scope."
        )
    )
    parser.add_argument("--inventory-json", required=True, type=Path)
    parser.add_argument("--output-json", required=True, type=Path)
    parser.add_argument("--output-md", type=Path)
    parser.add_argument("--rules-json", type=Path, help="Optional capability rules JSON.")
    parser.add_argument("--id-prefix", default="CAP")
    parser.add_argument("--source-name")
    parser.add_argument("--date", default=dt.date.today().isoformat())
    parser.add_argument(
        "--default-risk",
        choices=["low", "medium", "high"],
        default="medium",
        help="Risk used when a capability has no stronger signal.",
    )
    return parser.parse_args()


def slugify(value: str) -> str:
    value = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower())
    return value.strip("-") or "capability"


def load_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def display_path(path: Path) -> str:
    return path.name if path.is_absolute() else path.as_posix()


def text_feature(feature: dict[str, Any], key: str) -> str:
    return str(feature.get(key, "")).strip()


def feature_text(feature: dict[str, Any]) -> str:
    return " ".join(
        [
            text_feature(feature, "name"),
            text_feature(feature, "trigger"),
            text_feature(feature, "source_path"),
            text_feature(feature, "operation"),
            " ".join(str(item) for item in feature.get("notes", []))
            if isinstance(feature.get("notes"), list)
            else str(feature.get("notes", "")),
        ]
    ).lower()


def path_group(feature: dict[str, Any]) -> str:
    source_path = text_feature(feature, "source_path")
    if source_path:
        stem = Path(source_path).stem
        if stem:
            return stem
    trigger = text_feature(feature, "trigger").strip("/")
    if trigger:
        return trigger.split("/")[0]
    return text_feature(feature, "kind") or "capability"


def normalize_rules(payload: dict[str, Any] | None) -> list[dict[str, Any]]:
    if not payload:
        return []
    raw_rules = payload.get("capabilities", [])
    if not isinstance(raw_rules, list):
        raise ValueError("rules JSON must contain a 'capabilities' array")

    rules: list[dict[str, Any]] = []
    for index, rule in enumerate(raw_rules, start=1):
        if not isinstance(rule, dict):
            raise ValueError("each capability rule must be an object")
        name = str(rule.get("name") or f"Capability {index}").strip()
        matches = rule.get("match", [])
        if isinstance(matches, str):
            matches = [matches]
        if not isinstance(matches, list):
            raise ValueError(f"rule {name!r} match must be a string or array")
        rules.append(
            {
                "id": str(rule.get("id") or ""),
                "name": name,
                "slug": slugify(str(rule.get("slug") or name)),
                "risk": str(rule.get("risk") or "").lower(),
                "match": [str(item).lower() for item in matches],
                "summary": str(rule.get("summary") or ""),
                "migration_focus": str(rule.get("migration_focus") or ""),
                "decision": str(rule.get("decision") or ""),
            }
        )
    return rules


def group_key(feature: dict[str, Any], rules: list[dict[str, Any]]) -> str:
    combined = feature_text(feature)
    for rule in rules:
        if any(term and term in combined for term in rule["match"]):
            return str(rule["slug"])
    return slugify(path_group(feature))


def risk_rank(risk: str) -> int:
    return {"low": 0, "medium": 1, "high": 2}.get(risk, 1)


def capability_risk(features: list[dict[str, Any]], default_risk: str) -> str:
    risks = [str(item.get("risk", default_risk)).lower() for item in features]
    if any(risk == "high" for risk in risks):
        return "high"
    operations = {text_feature(item, "operation").upper() for item in features}
    if operations & HTTP_MUTATIONS:
        return "medium"
    return max(risks or [default_risk], key=risk_rank)


def title_from_slug(slug: str) -> str:
    return " ".join(part.capitalize() for part in slug.split("-") if part)


def render_markdown(payload: dict[str, Any]) -> str:
    features = payload.get("features", [])
    if not isinstance(features, list):
        features = []

    lines = [
        "# Capability Backlog",
        "",
        "Status: candidate scope; requires human review",
        f"Generated: {payload.get('generated_at', '')}",
        f"Source system: {payload.get('source_name', 'source system')}",
        f"Raw discovery entries: {payload.get('raw_feature_count', 0)}",
        "",
        "This backlog groups raw discovery entries into migration capabilities.",
        "Raw entries are behavior evidence, not implementation package units.",
        "",
        "| Capability ID | Capability | Risk | Evidence Count | Source Groups |",
        "| --- | --- | --- | ---: | --- |",
    ]
    for feature in features:
        source_groups = ", ".join(feature.get("source_groups", []))
        lines.append(
            "| {id} | {name} | {risk} | {count} | {groups} |".format(
                id=feature.get("feature_id", ""),
                name=str(feature.get("name", "")).replace("|", "\\|"),
                risk=feature.get("risk", ""),
                count=feature.get("endpoint_count", 0),
                groups=source_groups.replace("|", "\\|"),
            )
        )

    lines.extend(["", "## Evidence Membership", ""])
    for feature in features:
        lines.extend(
            [
                f"### {feature.get('feature_id', '')} - {feature.get('name', '')}",
                "",
                "| Raw ID | Kind | Operation | Trigger | Source Anchor |",
                "| --- | --- | --- | --- | --- |",
            ]
        )
        for item in feature.get("evidence", []):
            trigger = str(item.get("trigger", "")).replace("|", "\\|")
            lines.append(
                "| {id} | {kind} | {operation} | `{trigger}` | `{anchor}` |".format(
                    id=item.get("feature_id", ""),
                    kind=item.get("kind", ""),
                    operation=item.get("operation", ""),
                    trigger=trigger,
                    anchor=item.get("source_anchor", ""),
                )
            )
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    inventory = load_json(args.inventory_json)
    rules = normalize_rules(load_json(args.rules_json) if args.rules_json else None)
    inventory_ref = display_path(args.inventory_json)
    raw_features = inventory.get("features", [])
    if not isinstance(raw_features, list):
        raw_features = []
    features = [item for item in raw_features if isinstance(item, dict)]

    groups: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for feature in features:
        groups[group_key(feature, rules)].append(feature)

    rule_by_slug = {rule["slug"]: rule for rule in rules}
    capability_features: list[dict[str, Any]] = []
    for index, slug in enumerate(sorted(groups), start=1):
        evidence = groups[slug]
        rule = rule_by_slug.get(slug, {})
        feature_id = rule.get("id") or f"{args.id_prefix}-{index:03d}"
        name = rule.get("name") or title_from_slug(slug)
        source_ids = [text_feature(item, "feature_id") for item in evidence]
        source_groups = sorted({path_group(item) for item in evidence})
        methods = sorted(
            {text_feature(item, "operation").upper() for item in evidence if item.get("operation")}
        )
        risk = str(rule.get("risk") or capability_risk(evidence, args.default_risk))
        summary = rule.get("summary") or (
            f"Preserve observable behavior for the {name} capability."
        )
        migration_focus = rule.get("migration_focus") or (
            "Confirm source behavior, target boundary, adapters, mappers and validation evidence."
        )
        decision = rule.get("decision") or (
            "Group raw discovery entries as one capability until human review approves a split."
        )
        capability_features.append(
            {
                "feature_id": feature_id,
                "kind": "capability",
                "line": 1,
                "name": name,
                "notes": [
                    "capability backlog candidate; requires human scope review",
                    f"raw evidence count: {len(evidence)}",
                    f"raw evidence ids: {', '.join(source_ids)}",
                    migration_focus,
                ],
                "operation": "CAPABILITY",
                "risk": risk,
                "slug": f"cap-{index:03d}-{slug}",
                "source_anchor": f"{inventory_ref}:1",
                "source_path": inventory_ref,
                "trigger": name,
                "summary": summary,
                "decision": decision,
                "endpoint_count": len(evidence),
                "endpoint_ids": source_ids,
                "http_methods": methods,
                "source_groups": source_groups,
                "evidence": [
                    {
                        "feature_id": item.get("feature_id", ""),
                        "kind": item.get("kind", ""),
                        "operation": item.get("operation", ""),
                        "trigger": item.get("trigger", ""),
                        "source_anchor": item.get("source_anchor")
                        or f"{item.get('source_path', '')}:{item.get('line', '')}",
                    }
                    for item in evidence
                ],
            }
        )

    payload = {
        "source_name": args.source_name or inventory.get("source_name", "source system"),
        "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "date": args.date,
        "status": "candidate capability backlog",
        "basis": (
            "Grouped from raw discovery inventory; raw entries are behavior evidence, "
            "not implementation package units."
        ),
        "raw_inventory": inventory_ref,
        "raw_feature_count": len(features),
        "features": capability_features,
    }

    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    print(f"Wrote {args.output_json}")

    if args.output_md:
        args.output_md.parent.mkdir(parents=True, exist_ok=True)
        args.output_md.write_text(render_markdown(payload), encoding="utf-8")
        print(f"Wrote {args.output_md}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
