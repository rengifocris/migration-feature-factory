#!/usr/bin/env python3
"""Print a compact migration package context summary."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


INDEX_FILE = "migration-package-index.md"
SUMMARY_SECTIONS = [
    "Current Status",
    "Context Pack",
    "Decision Log",
    "Change Log",
    "Open Questions",
    "Validation Summary",
    "Risks",
]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Summarize a migration package for handoff or compaction."
    )
    parser.add_argument(
        "package",
        nargs="?",
        type=Path,
        help="Package directory or migration-package-index.md. If omitted, cwd is checked.",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="Optional file path to write the summary. Defaults to stdout.",
    )
    return parser.parse_args()


def resolve_index(path: Path | None) -> Path | None:
    candidate = path or Path.cwd()
    if candidate.is_file() and candidate.name == INDEX_FILE:
        return candidate
    if candidate.is_dir() and (candidate / INDEX_FILE).exists():
        return candidate / INDEX_FILE
    if path is None:
        print("No migration package found in current directory; skipping.")
        return None
    print(f"Migration package index not found at {candidate}", file=sys.stderr)
    return None


def section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body").strip() if match else ""


def metadata_line(text: str, label: str) -> str:
    pattern = re.compile(rf"^{re.escape(label)}:\s*(.+)$", re.MULTILINE)
    match = pattern.search(text)
    return match.group(1).strip() if match else ""


def compact_section(body: str, max_lines: int = 12) -> str:
    lines = [line.rstrip() for line in body.splitlines() if line.strip()]
    if len(lines) <= max_lines:
        return "\n".join(lines)
    visible = lines[:max_lines]
    visible.append(f"... {len(lines) - max_lines} more line(s)")
    return "\n".join(visible)


def display_path(path: Path) -> str:
    resolved = path.resolve()
    try:
        return str(resolved.relative_to(Path.cwd().resolve()))
    except ValueError:
        return path.name


def build_summary(index_path: Path) -> str:
    text = index_path.read_text(encoding="utf-8")
    title = text.splitlines()[0].lstrip("# ").strip() if text.splitlines() else INDEX_FILE
    lines = [
        f"# Context Summary - {title}",
        "",
        f"- Package: `{display_path(index_path.parent)}`",
        f"- Feature ID: {metadata_line(text, 'Feature ID') or 'not set'}",
        f"- Legacy system: {metadata_line(text, 'Legacy system') or 'not set'}",
        f"- Target system: {metadata_line(text, 'Target system') or 'not set'}",
        f"- Last updated: {metadata_line(text, 'Last updated') or 'not set'}",
        "",
    ]

    for heading in SUMMARY_SECTIONS:
        body = section(text, heading)
        if not body:
            continue
        lines.extend([f"## {heading}", "", compact_section(body), ""])

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    index_path = resolve_index(args.package)
    if index_path is None:
        return 0 if args.package is None else 2

    summary = build_summary(index_path)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(summary, encoding="utf-8")
        print(f"Wrote context summary: {args.output}")
        return 0

    print(summary, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
