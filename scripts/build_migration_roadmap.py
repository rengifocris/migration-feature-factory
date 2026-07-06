#!/usr/bin/env python3
"""Build a migration roadmap from a discovery inventory."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import sys
from pathlib import Path


RISK_WEIGHT = {"low": 0, "medium": 1, "high": 2}
KIND_WEIGHT = {"api": 0, "job": 1, "event-listener": 2}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Create a recommended migration roadmap from discovery JSON."
    )
    parser.add_argument("--inventory-json", required=True, type=Path)
    parser.add_argument("--packages-root", type=Path, default=Path("packages"))
    parser.add_argument("--output", type=Path, help="Output path. Defaults to stdout.")
    return parser.parse_args()


def markdown_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def recommendation(feature: dict[str, object]) -> tuple[str, str]:
    risk = str(feature.get("risk", "medium")).lower()
    kind = str(feature.get("kind", "unknown")).lower()
    operation = str(feature.get("operation", "")).upper()

    if risk == "low" and operation in {"GET", "HEAD", "OPTIONS"}:
        return "start early", "legacy behavior inventory"
    if kind in {"event-listener"} or risk == "high":
        return "spike first", "spike"
    return "migrate after low-risk slices", "behavior parity plan"


def sort_key(feature: dict[str, object]) -> tuple[int, int, str, str]:
    risk = str(feature.get("risk", "medium")).lower()
    kind = str(feature.get("kind", "unknown")).lower()
    return (
        RISK_WEIGHT.get(risk, 1),
        KIND_WEIGHT.get(kind, 3),
        str(feature.get("source_path", "")),
        str(feature.get("line", "")),
    )


def render(payload: dict[str, object], packages_root: Path) -> str:
    raw_features = payload.get("features", [])
    if not isinstance(raw_features, list):
        raw_features = []
    features = [feature for feature in raw_features if isinstance(feature, dict)]
    ordered = sorted(features, key=sort_key)
    generated_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        "# Migration Roadmap",
        "",
        "Status: generated",
        f"Generated: {generated_at}",
        f"Source system: {payload.get('source_name', 'source system')}",
        f"Packages root: `{packages_root.as_posix()}`",
        "",
        "## Recommendation",
        "",
        "- Start with low-risk read/query API slices because behavior is usually",
        "  easier to observe and validate.",
        "- Move mutations and jobs after behavior inventory and parity evidence are",
        "  explicit.",
        "- Put event listeners, destructive operations and unclear side effects",
        "  behind a Spike before implementation.",
        "- Do not migrate code until the package states behavior evidence and target",
        "  architecture boundaries.",
        "",
        "## Summary",
        "",
        f"- Candidates: {len(features)}",
        f"- Low risk: {sum(1 for item in features if item.get('risk') == 'low')}",
        f"- Medium risk: {sum(1 for item in features if item.get('risk') == 'medium')}",
        f"- High risk: {sum(1 for item in features if item.get('risk') == 'high')}",
        "",
        "## Ordered Migration Candidates",
        "",
        "| Order | Feature ID | Candidate | Type | Risk | Package | Recommendation | Next Gate |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    for index, feature in enumerate(ordered, start=1):
        rec, gate = recommendation(feature)
        package = packages_root / str(feature.get("slug", "feature"))
        lines.append(
            "| {order} | {id} | {name} | {kind} | {risk} | `{package}` | {rec} | {gate} |".format(
                order=index,
                id=markdown_cell(feature.get("feature_id", "")),
                name=markdown_cell(feature.get("name", "")),
                kind=markdown_cell(feature.get("kind", "")),
                risk=markdown_cell(feature.get("risk", "")),
                package=markdown_cell(package.as_posix()),
                rec=markdown_cell(rec),
                gate=markdown_cell(gate),
            )
        )
    lines.extend(
        [
            "",
            "## Roadmap Gate",
            "",
            "This roadmap is generated from source entry-point metadata. It is not an",
            "implementation plan until each package has reviewed behavior inventory,",
            "parity evidence, architecture decision and implementation brief.",
            "",
            "## Search Anchors",
            "",
            "- migration roadmap",
            "- migration order",
            "- automated discovery",
            "- feature package generation",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    try:
        payload = json.loads(args.inventory_json.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    text = render(payload, args.packages_root)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
        print(f"Wrote {args.output}")
    else:
        print(text, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
