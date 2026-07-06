#!/usr/bin/env python3
"""Discover migration feature candidates from a source repository.

The scanner is intentionally heuristic. It finds likely entry points and writes
metadata, not source excerpts. Generated output is a discovery seed, not an
implementation-ready behavior contract.
"""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
from dataclasses import asdict, dataclass
from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    ".hg",
    ".svn",
    ".gradle",
    ".mvn",
    ".next",
    ".tox",
    ".venv",
    "__pycache__",
    "build",
    "coverage",
    "dist",
    "node_modules",
    "out",
    "target",
    "vendor",
    "venv",
}
SOURCE_SUFFIXES = {
    ".java",
    ".kt",
    ".js",
    ".jsx",
    ".ts",
    ".tsx",
    ".py",
    ".yaml",
    ".yml",
    ".json",
}
TEST_PATH_RE = re.compile(r"(^|/)(test|tests|spec|__tests__)(/|$)|test\.|spec\.", re.I)
MAX_FILE_BYTES = 1_000_000

JAVA_MAPPING_RE = re.compile(
    r"@(GetMapping|PostMapping|PutMapping|PatchMapping|DeleteMapping|RequestMapping)\b"
    r"(?:\((?P<args>[^)]*)\))?"
)
JAVA_REQUEST_METHOD_RE = re.compile(r"RequestMethod\.(GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)")
JAVA_STRING_RE = re.compile(r'"([^"]*)"|\'([^\']*)\'')
JAVA_CLASS_RE = re.compile(r"\b(class|interface)\s+[A-Za-z_][A-Za-z0-9_]*")
JAVA_METHOD_RE = re.compile(
    r"\b([A-Za-z_][A-Za-z0-9_]*)\s*\([^;]*\)\s*(?:throws\s+[^{]+)?\{?"
)
JAVA_SCHEDULED_RE = re.compile(r"@Scheduled\b(?:\((?P<args>[^)]*)\))?")
JAVA_LISTENER_RE = re.compile(r"@(KafkaListener|JmsListener|RabbitListener)\b(?:\((?P<args>[^)]*)\))?")

NODE_ROUTE_RE = re.compile(
    r"\b(?:router|app)\.(get|post|put|patch|delete|all)\s*\(\s*([\"'`])([^\"'`]+)\2",
    re.I,
)
PY_ROUTE_RE = re.compile(
    r"@(?:[A-Za-z_][A-Za-z0-9_]*\.)?(get|post|put|patch|delete|route)\s*"
    r"\(\s*([\"'])([^\"']+)\2(?P<args>[^)]*)\)",
    re.I,
)
PY_DEF_RE = re.compile(r"\bdef\s+([A-Za-z_][A-Za-z0-9_]*)\s*\(")
OPENAPI_PATH_RE = re.compile(r"^\s+[\"']?(/[^:\"']*)[\"']?:\s*$")
OPENAPI_METHOD_RE = re.compile(r"^\s+(get|post|put|patch|delete|head|options):\s*$", re.I)

RISK_ORDER = {"low": 0, "medium": 1, "high": 2}
API_METHOD_RISK = {
    "GET": "low",
    "HEAD": "low",
    "OPTIONS": "low",
    "POST": "medium",
    "PUT": "medium",
    "PATCH": "medium",
    "DELETE": "high",
    "ANY": "medium",
    "ALL": "medium",
}


@dataclass(frozen=True)
class FeatureCandidate:
    feature_id: str
    slug: str
    name: str
    kind: str
    operation: str
    trigger: str
    source_path: str
    line: int
    risk: str
    notes: list[str]

    @property
    def source_anchor(self) -> str:
        return f"{self.source_path}:{self.line}"

    def to_dict(self) -> dict[str, object]:
        data = asdict(self)
        data["source_anchor"] = self.source_anchor
        return data


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Discover API, job and listener candidates in a source repository."
    )
    parser.add_argument("--source", required=True, type=Path, help="Source repository path.")
    parser.add_argument(
        "--source-name",
        help="Display name for the source system. Defaults to the source directory name.",
    )
    parser.add_argument("--id-prefix", default="AUTO", help="Feature ID prefix.")
    parser.add_argument(
        "--include-tests",
        action="store_true",
        help="Include test/spec paths in discovery.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument("--output", type=Path, help="Output path. Defaults to stdout.")
    return parser.parse_args()


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "feature"


def markdown_cell(value: object) -> str:
    text = str(value)
    return text.replace("\n", " ").replace("|", "\\|")


def iter_source_files(source: Path, include_tests: bool) -> list[Path]:
    files: list[Path] = []
    for root, dirs, names in os.walk(source):
        dirs[:] = [name for name in dirs if name not in EXCLUDED_DIRS]
        root_path = Path(root)
        for name in names:
            path = root_path / name
            if path.suffix.lower() not in SOURCE_SUFFIXES:
                continue
            relative = path.relative_to(source).as_posix()
            if not include_tests and TEST_PATH_RE.search(relative):
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            files.append(path)
    return sorted(files)


def read_lines(path: Path) -> list[str]:
    try:
        return path.read_text(encoding="utf-8", errors="ignore").splitlines()
    except OSError:
        return []


def risk_max(current: str, candidate: str) -> str:
    return candidate if RISK_ORDER[candidate] > RISK_ORDER[current] else current


def first_string(args: str | None) -> str:
    if not args:
        return ""
    match = JAVA_STRING_RE.search(args)
    if not match:
        return ""
    return next(group for group in match.groups() if group is not None)


def java_mapping_method(annotation: str, args: str | None) -> str:
    mapping = {
        "GetMapping": "GET",
        "PostMapping": "POST",
        "PutMapping": "PUT",
        "PatchMapping": "PATCH",
        "DeleteMapping": "DELETE",
    }
    if annotation in mapping:
        return mapping[annotation]
    if args:
        match = JAVA_REQUEST_METHOD_RE.search(args)
        if match:
            return match.group(1).upper()
    return "ANY"


def join_routes(base: str, route: str) -> str:
    parts = [part.strip("/") for part in (base, route) if part and part.strip("/")]
    if not parts:
        return "/"
    return "/" + "/".join(parts)


def java_class_base(lines: list[str]) -> tuple[str, int]:
    for index, line in enumerate(lines):
        if not JAVA_CLASS_RE.search(line):
            continue
        for lookback in range(index - 1, max(-1, index - 9), -1):
            match = JAVA_MAPPING_RE.search(lines[lookback])
            if match and match.group(1) == "RequestMapping":
                return first_string(match.group("args")), index
        return "", index
    return "", -1


def next_java_member_name(lines: list[str], start: int) -> str:
    for line in lines[start + 1 : start + 12]:
        stripped = line.strip()
        if not stripped or stripped.startswith("@"):
            continue
        match = JAVA_METHOD_RE.search(stripped)
        if match:
            return match.group(1)
    return "entryPoint"


def nearby_text(lines: list[str], index: int, before: int = 6, after: int = 4) -> str:
    start = max(0, index - before)
    end = min(len(lines), index + after + 1)
    return "\n".join(lines[start:end])


def parse_java(path: Path, source: Path) -> list[dict[str, object]]:
    lines = read_lines(path)
    relative = path.relative_to(source).as_posix()
    base_path, class_line = java_class_base(lines)
    candidates: list[dict[str, object]] = []

    for index, line in enumerate(lines):
        mapping = JAVA_MAPPING_RE.search(line)
        if mapping and index > class_line:
            args = mapping.group("args")
            method = java_mapping_method(mapping.group(1), args)
            route = join_routes(base_path, first_string(args))
            member_name = next_java_member_name(lines, index)
            risk = API_METHOD_RISK.get(method, "medium")
            notes = ["framework: java-spring"]
            if re.search(r"@(PreAuthorize|Secured|RolesAllowed)\b", nearby_text(lines, index)):
                risk = risk_max(risk, "medium")
                notes.append("security annotation nearby")
            candidates.append(
                {
                    "name": f"{method} {route if route else member_name}",
                    "kind": "api",
                    "operation": method,
                    "trigger": route,
                    "source_path": relative,
                    "line": index + 1,
                    "risk": risk,
                    "notes": notes,
                }
            )
            continue

        scheduled = JAVA_SCHEDULED_RE.search(line)
        if scheduled:
            member_name = next_java_member_name(lines, index)
            trigger = scheduled.group("args") or "scheduled"
            candidates.append(
                {
                    "name": f"Scheduled job {member_name}",
                    "kind": "job",
                    "operation": "scheduled",
                    "trigger": trigger,
                    "source_path": relative,
                    "line": index + 1,
                    "risk": "medium",
                    "notes": ["framework: java-spring"],
                }
            )
            continue

        listener = JAVA_LISTENER_RE.search(line)
        if listener:
            member_name = next_java_member_name(lines, index)
            trigger = first_string(listener.group("args")) or listener.group(1)
            candidates.append(
                {
                    "name": f"{listener.group(1)} {member_name}",
                    "kind": "event-listener",
                    "operation": listener.group(1),
                    "trigger": trigger,
                    "source_path": relative,
                    "line": index + 1,
                    "risk": "high",
                    "notes": ["framework: java-spring"],
                }
            )

    return candidates


def parse_node(path: Path, source: Path) -> list[dict[str, object]]:
    lines = read_lines(path)
    relative = path.relative_to(source).as_posix()
    candidates = []
    for index, line in enumerate(lines):
        match = NODE_ROUTE_RE.search(line)
        if not match:
            continue
        method = match.group(1).upper()
        route = match.group(3)
        candidates.append(
            {
                "name": f"{method} {route}",
                "kind": "api",
                "operation": method,
                "trigger": route,
                "source_path": relative,
                "line": index + 1,
                "risk": API_METHOD_RISK.get(method, "medium"),
                "notes": ["framework: node-http"],
            }
        )
    return candidates


def next_python_function_name(lines: list[str], start: int) -> str:
    for line in lines[start + 1 : start + 8]:
        match = PY_DEF_RE.search(line)
        if match:
            return match.group(1)
    return "entry_point"


def parse_python(path: Path, source: Path) -> list[dict[str, object]]:
    lines = read_lines(path)
    relative = path.relative_to(source).as_posix()
    candidates = []
    for index, line in enumerate(lines):
        match = PY_ROUTE_RE.search(line)
        if not match:
            continue
        method = match.group(1).upper()
        if method == "ROUTE":
            methods = re.findall(r"[\"'](GET|POST|PUT|PATCH|DELETE|HEAD|OPTIONS)[\"']", match.group("args"), re.I)
            method = methods[0].upper() if methods else "ANY"
        route = match.group(3)
        function_name = next_python_function_name(lines, index)
        candidates.append(
            {
                "name": f"{method} {route if route else function_name}",
                "kind": "api",
                "operation": method,
                "trigger": route,
                "source_path": relative,
                "line": index + 1,
                "risk": API_METHOD_RISK.get(method, "medium"),
                "notes": ["framework: python-http"],
            }
        )
    return candidates


def parse_openapi_yaml(path: Path, source: Path) -> list[dict[str, object]]:
    lines = read_lines(path)
    if not any("openapi:" in line.lower() or "swagger:" in line.lower() for line in lines[:40]):
        return []
    relative = path.relative_to(source).as_posix()
    candidates = []
    in_paths = False
    current_path = ""
    for index, line in enumerate(lines):
        stripped = line.strip()
        if stripped == "paths:":
            in_paths = True
            continue
        if not in_paths:
            continue
        path_match = OPENAPI_PATH_RE.match(line)
        if path_match:
            current_path = path_match.group(1)
            continue
        method_match = OPENAPI_METHOD_RE.match(line)
        if method_match and current_path:
            method = method_match.group(1).upper()
            candidates.append(
                {
                    "name": f"{method} {current_path}",
                    "kind": "api",
                    "operation": method,
                    "trigger": current_path,
                    "source_path": relative,
                    "line": index + 1,
                    "risk": API_METHOD_RISK.get(method, "medium"),
                    "notes": ["source: openapi"],
                }
            )
    return candidates


def parse_openapi_json(path: Path, source: Path) -> list[dict[str, object]]:
    try:
        data = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
    except (OSError, json.JSONDecodeError):
        return []
    if not isinstance(data, dict) or not ("openapi" in data or "swagger" in data):
        return []
    paths = data.get("paths")
    if not isinstance(paths, dict):
        return []
    relative = path.relative_to(source).as_posix()
    candidates = []
    for route, operations in sorted(paths.items()):
        if not isinstance(route, str) or not isinstance(operations, dict):
            continue
        for method in sorted(operations):
            upper = method.upper()
            if upper not in API_METHOD_RISK:
                continue
            candidates.append(
                {
                    "name": f"{upper} {route}",
                    "kind": "api",
                    "operation": upper,
                    "trigger": route,
                    "source_path": relative,
                    "line": 1,
                    "risk": API_METHOD_RISK.get(upper, "medium"),
                    "notes": ["source: openapi"],
                }
            )
    return candidates


def raw_candidates(source: Path, include_tests: bool) -> list[dict[str, object]]:
    candidates: list[dict[str, object]] = []
    for path in iter_source_files(source, include_tests):
        suffix = path.suffix.lower()
        if suffix in {".java", ".kt"}:
            candidates.extend(parse_java(path, source))
        elif suffix in {".js", ".jsx", ".ts", ".tsx"}:
            candidates.extend(parse_node(path, source))
        elif suffix == ".py":
            candidates.extend(parse_python(path, source))
        elif suffix in {".yaml", ".yml"}:
            candidates.extend(parse_openapi_yaml(path, source))
        elif suffix == ".json":
            candidates.extend(parse_openapi_json(path, source))
    return candidates


def finalize_candidates(
    candidates: list[dict[str, object]], id_prefix: str
) -> list[FeatureCandidate]:
    ordered = sorted(
        candidates,
        key=lambda item: (
            str(item["kind"]),
            str(item["source_path"]),
            int(item["line"]),
            str(item["name"]),
        ),
    )
    slug_counts: dict[str, int] = {}
    finalized: list[FeatureCandidate] = []
    for number, item in enumerate(ordered, start=1):
        base_slug = slugify(f"{item['kind']} {item['name']}")
        seen = slug_counts.get(base_slug, 0) + 1
        slug_counts[base_slug] = seen
        slug = base_slug if seen == 1 else f"{base_slug}-{seen}"
        finalized.append(
            FeatureCandidate(
                feature_id=f"{id_prefix}-{number:03d}",
                slug=slug,
                name=str(item["name"]),
                kind=str(item["kind"]),
                operation=str(item["operation"]),
                trigger=str(item["trigger"]),
                source_path=str(item["source_path"]),
                line=int(item["line"]),
                risk=str(item["risk"]),
                notes=list(item["notes"]),
            )
        )
    return finalized


def discover_features(source: Path, include_tests: bool, id_prefix: str) -> list[FeatureCandidate]:
    return finalize_candidates(raw_candidates(source, include_tests), id_prefix)


def inventory_payload(
    source: Path,
    source_name: str,
    features: list[FeatureCandidate],
    generated_at: str | None = None,
) -> dict[str, object]:
    return {
        "schema": "migration-feature-factory.discovery.v1",
        "generated_at": generated_at or utc_now(),
        "source_name": source_name,
        "source_root_stored": False,
        "feature_count": len(features),
        "features": [feature.to_dict() for feature in features],
    }


def render_markdown_inventory(payload: dict[str, object]) -> str:
    features = payload["features"]
    assert isinstance(features, list)
    lines = [
        "# Source Feature Inventory",
        "",
        "Status: generated",
        f"Generated: {payload['generated_at']}",
        f"Source system: {payload['source_name']}",
        "Source root stored: no",
        "",
        "## Purpose",
        "",
        "List source entry points that can seed migration packages. The inventory",
        "stores metadata and source-relative anchors only; it does not copy source",
        "code excerpts.",
        "",
        "## Summary",
        "",
        f"- Candidates discovered: {payload['feature_count']}",
        "- Implementation readiness: not ready until behavior inventory and parity",
        "  evidence are reviewed.",
        "",
        "## Candidates",
        "",
        "| ID | Type | Candidate | Risk | Source Anchor | Package Slug | Notes |",
        "| --- | --- | --- | --- | --- | --- | --- |",
    ]
    for item in features:
        assert isinstance(item, dict)
        lines.append(
            "| {id} | {kind} | {name} | {risk} | `{anchor}` | `{slug}` | {notes} |".format(
                id=markdown_cell(item["feature_id"]),
                kind=markdown_cell(item["kind"]),
                name=markdown_cell(item["name"]),
                risk=markdown_cell(item["risk"]),
                anchor=markdown_cell(item["source_anchor"]),
                slug=markdown_cell(item["slug"]),
                notes=markdown_cell(", ".join(item.get("notes", []))),
            )
        )
    lines.extend(
        [
            "",
            "## Recommended Next Gate",
            "",
            "- Low-risk read/query APIs: fill legacy behavior inventory first.",
            "- Medium-risk mutations or jobs: fill behavior inventory and parity plan",
            "  before implementation.",
            "- High-risk listeners or destructive operations: create or complete a Spike",
            "  before implementation.",
            "",
            "## Search Anchors",
            "",
            "- automated discovery",
            "- source feature inventory",
            "- migration candidates",
        ]
    )
    return "\n".join(lines) + "\n"


def write_output(text: str, output: Path | None) -> None:
    if output is None:
        print(text, end="")
        return
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(text, encoding="utf-8")
    print(f"Wrote {output}")


def main() -> int:
    args = parse_args()
    source = args.source.resolve()
    if not source.is_dir():
        print(f"Source directory not found: {source}", file=sys.stderr)
        return 2

    source_name = args.source_name or source.name
    features = discover_features(source, args.include_tests, args.id_prefix)
    payload = inventory_payload(source, source_name, features)

    if args.format == "json":
        text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    else:
        text = render_markdown_inventory(payload)
    write_output(text, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
