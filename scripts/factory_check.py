#!/usr/bin/env python3
"""Check a migration package for required artifacts and traceability basics."""

from __future__ import annotations

import argparse
import re
import sys
from dataclasses import dataclass
from pathlib import Path


INDEX_FILE = "migration-package-index.md"
REQUIRED_FILES = [
    INDEX_FILE,
    "feature-intake.md",
    "legacy-behavior-inventory.md",
    "behavior-parity-plan.md",
    "change-intake.md",
    "user-story.md",
    "hard-spec.md",
    "architecture-decision.md",
    "implementation-brief.md",
    "review-qa.md",
    "closeout.md",
]
REQUIRED_INDEX_SECTIONS = [
    "Current Status",
    "Package Artifacts",
    "Traceability Matrix",
    "Decision Log",
    "Change Log",
    "Validation Summary",
    "Context Pack",
    "Consistency Checklist",
]
ALLOWED_TRACE_STATUSES = {
    "pending",
    "planned",
    "validated",
    "gap",
    "accepted-risk",
    "superseded",
}
ID_PATTERN = re.compile(r"^(LB|AC|HS|ADR|EV|CHG|R)-\d{2,}$")
SENSITIVE_PATTERNS = [
    re.compile(r"gh[o]_[A-Za-z0-9_]+"),
    re.compile(r"s[k]-[A-Za-z0-9_-]+"),
    re.compile(r"(?i)private\s+key"),
    re.compile(r"(?i)connection\s+string"),
    re.compile(r"(?i)/users/[^\\s)`]+"),
]


@dataclass
class Finding:
    severity: str
    message: str


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Validate a migration package scaffold and traceability basics."
    )
    parser.add_argument(
        "package",
        nargs="?",
        type=Path,
        help="Package directory or migration-package-index.md. If omitted, cwd is checked.",
    )
    parser.add_argument(
        "--light",
        action="store_true",
        help="Run fast checks only: package index, referenced files and public-safety scan.",
    )
    parser.add_argument(
        "--strict-placeholders",
        action="store_true",
        help="Treat unresolved <placeholder> markers as errors instead of warnings.",
    )
    return parser.parse_args()


def resolve_package(path: Path | None) -> Path | None:
    candidate = path or Path.cwd()
    if candidate.is_file() and candidate.name == INDEX_FILE:
        return candidate.parent
    if candidate.is_dir() and (candidate / INDEX_FILE).exists():
        return candidate
    if path is None:
        print("No migration package found in current directory; skipping.")
        return None
    print(f"Migration package index not found at {candidate}", file=sys.stderr)
    return None


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def section(text: str, heading: str) -> str:
    pattern = re.compile(
        rf"^## {re.escape(heading)}\s*$\n(?P<body>.*?)(?=^## |\Z)",
        re.MULTILINE | re.DOTALL,
    )
    match = pattern.search(text)
    return match.group("body") if match else ""


def split_row(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def is_separator(cells: list[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells)


def table_rows(section_text: str) -> list[list[str]]:
    rows = []
    for line in section_text.splitlines():
        if not line.startswith("|"):
            continue
        cells = split_row(line)
        if not cells or is_separator(cells):
            continue
        if cells[0].lower() in {"artifact", "source", "date"}:
            continue
        rows.append(cells)
    return rows


def clean_path(value: str) -> str:
    return value.strip().strip("`").strip()


def referenced_artifacts(index_text: str) -> list[str]:
    rows = table_rows(section(index_text, "Package Artifacts"))
    paths = []
    for cells in rows:
        if len(cells) < 3:
            continue
        path = clean_path(cells[2])
        if not path or "<" in path or ">" in path:
            continue
        paths.append(path)
    return paths


def placeholder_findings(package: Path, strict: bool) -> list[Finding]:
    severity = "ERROR" if strict else "WARN"
    findings = []
    for path in markdown_files(package):
        for line_no, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            if re.search(r"<[^>\n]+>", line):
                findings.append(
                    Finding(severity, f"{path.name}:{line_no} has unresolved placeholder text")
                )
                break
    return findings


def markdown_files(package: Path) -> list[Path]:
    return sorted(path for path in package.glob("*.md") if path.is_file())


def check_required_files(package: Path, light: bool) -> list[Finding]:
    findings = []
    required = [INDEX_FILE] if light else REQUIRED_FILES
    for name in required:
        if not (package / name).is_file():
            findings.append(Finding("ERROR", f"Missing required artifact: {name}"))
    return findings


def check_referenced_files(package: Path, index_text: str) -> list[Finding]:
    findings = []
    for path_value in referenced_artifacts(index_text):
        target = package / path_value
        if not target.is_file():
            findings.append(Finding("ERROR", f"Package index references missing file: {path_value}"))
    return findings


def check_index_sections(index_text: str, light: bool) -> list[Finding]:
    if light:
        return []
    findings = []
    for heading in REQUIRED_INDEX_SECTIONS:
        if not section(index_text, heading).strip():
            findings.append(Finding("ERROR", f"Package index missing section: {heading}"))
    return findings


def check_traceability_rows(index_text: str, light: bool) -> list[Finding]:
    if light:
        return []
    findings = []
    for cells in table_rows(section(index_text, "Traceability Matrix")):
        if len(cells) < 6:
            findings.append(Finding("ERROR", "Traceability row has fewer than 6 columns"))
            continue
        trace_id = cells[1].strip("` ")
        status = cells[5].strip("` ").lower()
        if "<" not in trace_id and not ID_PATTERN.fullmatch(trace_id):
            findings.append(Finding("ERROR", f"Invalid traceability ID: {trace_id}"))
        if "<" not in status and status not in ALLOWED_TRACE_STATUSES:
            findings.append(Finding("ERROR", f"Invalid traceability status: {status}"))
    return findings


def check_public_safety(package: Path) -> list[Finding]:
    findings = []
    for path in markdown_files(package):
        text = path.read_text(encoding="utf-8")
        for pattern in SENSITIVE_PATTERNS:
            if pattern.search(text):
                findings.append(Finding("ERROR", f"{path.name} has private or sensitive-looking text"))
                break
    return findings


def run_checks(package: Path, args: argparse.Namespace) -> list[Finding]:
    index_path = package / INDEX_FILE
    index_text = read_text(index_path) if index_path.exists() else ""
    findings = []
    findings.extend(check_required_files(package, args.light))
    if index_text:
        findings.extend(check_referenced_files(package, index_text))
        findings.extend(check_index_sections(index_text, args.light))
        findings.extend(check_traceability_rows(index_text, args.light))
    if not args.light:
        findings.extend(placeholder_findings(package, args.strict_placeholders))
    findings.extend(check_public_safety(package))
    return findings


def print_findings(package: Path, findings: list[Finding]) -> None:
    errors = [finding for finding in findings if finding.severity == "ERROR"]
    warnings = [finding for finding in findings if finding.severity == "WARN"]

    if not findings:
        print(f"OK: {package} passed factory checks.")
        return

    for finding in findings:
        print(f"{finding.severity}: {finding.message}")
    print(f"Summary: {len(errors)} error(s), {len(warnings)} warning(s).")


def main() -> int:
    args = parse_args()
    package = resolve_package(args.package)
    if package is None:
        return 0 if args.package is None else 2

    findings = run_checks(package, args)
    print_findings(package, findings)
    return 1 if any(finding.severity == "ERROR" for finding in findings) else 0


if __name__ == "__main__":
    raise SystemExit(main())
