#!/usr/bin/env python3
"""Generate mock-server, synthetic-data and model-governance strategy docs."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import os
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from dataclasses import dataclass
from pathlib import Path


EXCLUDED_DIRS = {
    ".git",
    ".gradle",
    ".mvn",
    ".next",
    ".tox",
    ".venv",
    ".codex-venv",
    "BOOT-INF",
    "META-INF",
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
    ".xml",
}
MAX_FILE_BYTES = 1_000_000
DEFAULT_SCAN_TERMS = (
    "acl",
    "adapter",
    "canonical",
    "client",
    "contract",
    "dto",
    "enrich",
    "enrichment",
    "mapper",
    "model",
    "record",
    "schema",
    "validator",
)
STOP_SCAN_TERMS = {
    "and",
    "for",
    "non",
    "the",
    "with",
}


@dataclass(frozen=True)
class CodeSignal:
    root_label: str
    relative_path: str
    line: int
    term: str
    classification: str
    action: str

    @property
    def anchor(self) -> str:
        return f"{self.root_label}/{self.relative_path}:{self.line}"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Generate a mock-server, synthetic-data and model-governance strategy "
            "from discovery metadata and optional code-context signals."
        )
    )
    parser.add_argument("--inventory-json", required=True, type=Path)
    parser.add_argument("--target-system", required=True)
    parser.add_argument("--source-system")
    parser.add_argument("--target-pom", type=Path)
    parser.add_argument(
        "--code-root",
        action="append",
        default=[],
        type=Path,
        help="Optional source or target code root to scan for model/client terms. May be repeated.",
    )
    parser.add_argument(
        "--scan-term",
        action="append",
        default=[],
        help="Additional term to scan for in code roots. May be repeated.",
    )
    parser.add_argument(
        "--domain-context",
        action="append",
        default=[],
        help="Curated domain context to include without copying source excerpts. May be repeated.",
    )
    parser.add_argument("--canonical-model-name", default="Canonical Record")
    parser.add_argument("--raw-model-name", default="Non-Enriched Record")
    parser.add_argument("--enriched-model-name", default="Enriched Record")
    parser.add_argument("--language-policy", choices=("english", "spanish-first"), default="english")
    parser.add_argument("--sensitivity", default="internal")
    parser.add_argument("--roadmap-path", default="migration-roadmap.md")
    parser.add_argument("--technical-foundation-path", default="technical-foundation.md")
    parser.add_argument("--max-signals", type=int, default=40)
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


def utc_now() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_inventory(path: Path) -> dict[str, object]:
    return json.loads(path.read_text(encoding="utf-8"))


def display_path(path: Path) -> str:
    try:
        return path.resolve().relative_to(Path.cwd().resolve()).as_posix()
    except ValueError:
        return path.name


def pom_text(element: ET.Element | None, default: str = "not detected") -> str:
    return element.text.strip() if element is not None and element.text else default


def parse_pom(path: Path | None) -> dict[str, object]:
    if path is None or not path.is_file():
        return {
            "java_version": "not detected",
            "spring_boot_version": "not detected",
            "dependencies": [],
        }

    tree = ET.parse(path)
    root = tree.getroot()
    ns = {"m": root.tag.split("}")[0].strip("{")} if root.tag.startswith("{") else {}
    prefix = "m:" if ns else ""

    properties: dict[str, str] = {}
    props = root.find(f"{prefix}properties", ns)
    if props is not None:
        for child in list(props):
            tag = child.tag.split("}")[-1]
            if child.text:
                properties[tag] = child.text.strip()

    dependencies = []
    for dep in root.findall(f".//{prefix}dependency", ns):
        group = pom_text(dep.find(f"{prefix}groupId", ns), "")
        artifact = pom_text(dep.find(f"{prefix}artifactId", ns), "")
        if artifact:
            dependencies.append(f"{group}:{artifact}" if group else artifact)

    parent = root.find(f"{prefix}parent", ns)
    spring_boot_version = "not detected"
    if parent is not None and pom_text(parent.find(f"{prefix}artifactId", ns), "") == "spring-boot-starter-parent":
        spring_boot_version = pom_text(parent.find(f"{prefix}version", ns))

    return {
        "java_version": properties.get("java.version", "not detected"),
        "spring_boot_version": spring_boot_version,
        "dependencies": dependencies,
    }


def source_summary(inventory: dict[str, object]) -> dict[str, object]:
    features = inventory.get("features", [])
    if not isinstance(features, list):
        features = []
    return {
        "count": len(features),
        "risk": Counter(str(item.get("risk", "unknown")) for item in features if isinstance(item, dict)),
        "method": Counter(str(item.get("operation", "unknown")) for item in features if isinstance(item, dict)),
        "kind": Counter(str(item.get("kind", "unknown")) for item in features if isinstance(item, dict)),
        "source": Counter(str(item.get("source_path", "unknown")) for item in features if isinstance(item, dict)),
    }


def counter_text(counter: Counter[str]) -> str:
    if not counter:
        return "none"
    return ", ".join(f"{key}: {value}" for key, value in sorted(counter.items()))


def markdown_cell(value: object) -> str:
    return str(value).replace("\n", " ").replace("|", "\\|")


def classify_signal(term: str, path: str) -> tuple[str, str]:
    haystack = f"{term} {path}".lower()
    if "enrich" in haystack:
        return "enrichment", "Route through enrichment model/client governance."
    if "client" in haystack or "adapter" in haystack or "acl" in haystack:
        return "integration boundary", "Keep behind adapter/ACL and mock at the boundary."
    if "mapper" in haystack:
        return "mapping boundary", "Map explicitly and cover with parity fixtures."
    if "dto" in haystack or "schema" in haystack or "contract" in haystack:
        return "generated/boundary contract", "Keep generated contract shape at the boundary."
    if "model" in haystack or "record" in haystack or "canonical" in haystack:
        return "model governance", "Decide whether this is raw, canonical or enriched."
    if "validator" in haystack:
        return "validation", "Bind validation cases to synthetic happy/edge/bad data."
    return "context signal", "Review during model and mock strategy acceptance."


def normalized_terms(args: argparse.Namespace) -> list[str]:
    raw_terms = [
        *DEFAULT_SCAN_TERMS,
        *args.scan_term,
        args.canonical_model_name,
        args.raw_model_name,
        args.enriched_model_name,
    ]
    terms: list[str] = []
    seen: set[str] = set()
    for item in raw_terms:
        for part in re.split(r"[^A-Za-z0-9_]+", item):
            term = part.strip()
            if len(term) < 3:
                continue
            key = term.lower()
            if key in STOP_SCAN_TERMS:
                continue
            if key in seen:
                continue
            seen.add(key)
            terms.append(term)
    return terms


def iter_source_files(root: Path) -> list[Path]:
    files: list[Path] = []
    for current, dirs, names in os.walk(root):
        dirs[:] = [
            name
            for name in dirs
            if name not in EXCLUDED_DIRS and not name.startswith(".")
        ]
        current_path = Path(current)
        for name in names:
            path = current_path / name
            if path.suffix.lower() not in SOURCE_SUFFIXES:
                continue
            try:
                if path.stat().st_size > MAX_FILE_BYTES:
                    continue
            except OSError:
                continue
            files.append(path)
    return sorted(files)


def scan_code_signals(args: argparse.Namespace) -> list[CodeSignal]:
    terms = normalized_terms(args)
    signals: list[CodeSignal] = []
    seen: set[tuple[str, str, int, str]] = set()

    for root in args.code_root:
        if not root.is_dir():
            continue
        root_label = root.name or "code-root"
        for path in iter_source_files(root):
            if len(signals) >= args.max_signals:
                return signals
            relative = path.relative_to(root).as_posix()
            try:
                lines = path.read_text(encoding="utf-8", errors="ignore").splitlines()
            except OSError:
                continue
            for index, line in enumerate(lines, start=1):
                lowered = line.lower()
                for term in terms:
                    if term.lower() not in lowered:
                        continue
                    key = (root_label, relative, index, term.lower())
                    if key in seen:
                        continue
                    seen.add(key)
                    classification, action = classify_signal(term, relative)
                    signals.append(
                        CodeSignal(
                            root_label=root_label,
                            relative_path=relative,
                            line=index,
                            term=term,
                            classification=classification,
                            action=action,
                        )
                    )
                    break
                if len(signals) >= args.max_signals:
                    return signals
    return signals


def testing_stack_summary(pom: dict[str, object]) -> str:
    dependencies = [item for item in pom.get("dependencies", []) if isinstance(item, str)]
    detected = []
    if any("spring-boot-starter-test" in item for item in dependencies):
        detected.append("Spring test support")
    if any("wiremock" in item.lower() for item in dependencies):
        detected.append("WireMock-compatible dependency")
    if any("mockserver" in item.lower() for item in dependencies):
        detected.append("MockServer-compatible dependency")
    if any("testcontainers" in item.lower() for item in dependencies):
        detected.append("containerized test support")
    if not detected:
        return "no dedicated mock-server dependency detected"
    return ", ".join(detected)


def scenario_rows(summary: dict[str, object]) -> list[tuple[str, str, str, str]]:
    methods = summary["method"]
    method_counter = methods if isinstance(methods, Counter) else Counter()
    rows = [
        ("MS-001", "happy-minimal", "minimum valid source response", "proves baseline parity"),
        ("MS-002", "happy-complete", "all optional enrichments present", "proves enriched output assembly"),
        ("MS-003", "edge-empty", "empty result or optional data missing", "proves null/empty semantics"),
        ("MS-004", "edge-boundary-values", "limits, dates, identifiers and enum boundaries", "proves validation edges"),
        ("MS-005", "bad-invalid-request", "invalid command/request input", "proves target preserves error semantics"),
        ("MS-006", "bad-not-found", "missing source record or upstream 404", "proves not-found mapping"),
        ("MS-007", "bad-upstream-error", "upstream 5xx or business error", "proves adapter error normalization"),
        ("MS-008", "bad-timeout", "slow or unavailable integration", "proves timeout and retry policy"),
        ("MS-009", "bad-malformed-payload", "unexpected upstream shape", "proves defensive parsing"),
        ("MS-010", "security-denied", "unauthorized or forbidden access", "proves permission behavior"),
    ]
    mutation_count = sum(method_counter.get(method, 0) for method in ("POST", "PUT", "PATCH", "DELETE"))
    if mutation_count:
        rows.append(("MS-011", "mutation-conflict", "duplicate, stale or conflicting write", "proves side-effect safety"))
    return rows


def append_context_lines(lines: list[str], args: argparse.Namespace) -> None:
    lines.extend(
        [
            "### Curated Context",
            "",
            "| Context | Handling |",
            "| --- | --- |",
        ]
    )
    if args.domain_context:
        for item in args.domain_context:
            lines.append(f"| {markdown_cell(item)} | convert into explicit model, mock or fixture rule |")
    else:
        lines.append("| none provided | rely on inventory and code-context signals only |")
    lines.append("")


def append_signal_lines(lines: list[str], signals: list[CodeSignal]) -> None:
    lines.extend(
        [
            "### Code-Context Signals",
            "",
            "The scan stores terms and source-relative anchors only. It does not copy source code excerpts.",
            "",
            "| Signal | Classification | Anchor | Required Action |",
            "| --- | --- | --- | --- |",
        ]
    )
    if signals:
        for signal in signals:
            lines.append(
                "| "
                f"`{markdown_cell(signal.term)}` | "
                f"{markdown_cell(signal.classification)} | "
                f"`{markdown_cell(signal.anchor)}` | "
                f"{markdown_cell(signal.action)} |"
            )
    else:
        lines.append("| none detected | not scanned or no term match | n/a | review manually before implementation |")
    lines.append("")


def append_scenario_lines(lines: list[str], summary: dict[str, object]) -> None:
    lines.extend(
        [
            "### Synthetic Scenario Matrix",
            "",
            "| ID | Fixture Profile | Mock Behavior | Evidence Purpose |",
            "| --- | --- | --- | --- |",
        ]
    )
    for scenario_id, profile, behavior, purpose in scenario_rows(summary):
        lines.append(f"| {scenario_id} | `{profile}` | {behavior} | {purpose} |")
    lines.append("")


def append_english_body(
    lines: list[str],
    args: argparse.Namespace,
    inventory: dict[str, object],
    pom: dict[str, object],
    signals: list[CodeSignal],
    generated_at: str,
) -> None:
    summary = source_summary(inventory)
    lines.extend(
        [
            "## English Engineering Mirror",
            "",
            "### Recommendation",
            "",
            "- Use two test doubles, each at the correct boundary:",
            "  in-process fakes for fast use-case tests and a contract-backed mock server for adapter, ACL and E2E parity tests.",
            f"- Preserve `{args.raw_model_name}` as a non-mutated source/canonical record.",
            f"- Expose `{args.enriched_model_name}` as a separate assembled view/result.",
            f"- Use `{args.canonical_model_name}` as the stable internal model name only where the target needs a curated model.",
            "- Govern generated DTOs, internal models, enrichment models, clients, adapters and mappers explicitly.",
            "- Keep synthetic data deterministic, small, public-safe and traceable to behavior IDs and evidence IDs.",
            "",
            "### Detected Inputs",
            "",
            f"- Generated: {generated_at}",
            f"- Source system: {args.source_system or inventory.get('source_name', 'source system')}",
            f"- Target system: {args.target_system}",
            f"- Candidate count: {summary['count']}",
            f"- Candidate type split: {counter_text(summary['kind'])}",
            f"- Method split: {counter_text(summary['method'])}",
            f"- Risk split: {counter_text(summary['risk'])}",
            f"- Testing stack signals: {testing_stack_summary(pom)}",
            f"- Related roadmap: `{args.roadmap_path}`",
            f"- Related technical foundation: `{args.technical_foundation_path}`",
            "",
        ]
    )
    append_context_lines(lines, args)
    append_signal_lines(lines, signals)
    lines.extend(
        [
            "### Mock Server Decision",
            "",
            "| Decision | Option A | Option B | Recommendation | Gate |",
            "| --- | --- | --- | --- | --- |",
            "| Use-case tests | in-process fakes | external mock server | in-process fakes for speed and clear use-case assertions | developer/QA review |",
            "| Adapter/ACL tests | hand-written client stubs | contract-backed mock server | contract-backed mock server for HTTP/API parity and failure semantics | architecture review |",
            "| E2E parity | call real upstream systems | local deterministic mocks | local deterministic mocks unless a safe certified environment is approved | QA review |",
            "| Slow/unavailable upstreams | skip tests | simulate timeouts/errors | simulate timeout, retry and malformed payload cases | parity plan |",
            "",
            "### Mock Server Boundary",
            "",
            "```mermaid",
            "flowchart LR",
            "  Test[\"Parity or integration test\"] --> Target[\"Target service under test\"]",
            "  Target --> Adapter[\"Adapter / ACL\"]",
            "  Adapter --> Mock[\"Contract-backed mock server\"]",
            "  Mock --> Fixtures[\"Synthetic scenario fixtures\"]",
            "  Fixtures --> Evidence[\"EV-* parity evidence\"]",
            "```",
            "",
        ]
    )
    append_scenario_lines(lines, summary)
    lines.extend(
        [
            "### Synthetic Data Governance",
            "",
            "| Rule | Rationale |",
            "| --- | --- |",
            "| No production data or copied private payloads | keeps generated artifacts public-safe and reviewable |",
            "| Deterministic fixture IDs | makes failures reproducible and diffable |",
            "| One fixture profile per behavior risk | avoids hiding edge cases in one large payload |",
            "| Valid/invalid pairs | proves validation and error behavior intentionally |",
            "| Golden-master snapshots only for observable contracts | avoids coupling tests to private implementation shape |",
            "| Fixture ownership in the package index | keeps data changes traceable to behavior, spec or decision changes |",
            "",
            "### Model Governance",
            "",
            "| Artifact | Policy | Reason |",
            "| --- | --- | --- |",
            f"| `{args.raw_model_name}` | preserve as the non-enriched source/canonical record | prevents enrichment from corrupting the baseline contract |",
            f"| `{args.enriched_model_name}` | assemble as a separate read/result model | makes enrichment optional, testable and auditable |",
            f"| `{args.canonical_model_name}` | curate only when target invariants exist | avoids generated schemas masquerading as domain behavior |",
            "| Generated DTOs | boundary only | generated transport contracts should not leak into use cases |",
            "| Enrichment models | explicit curated models | enrichment rules are behavior-sensitive |",
            "| Clients | isolated behind adapters/ACLs | failure semantics, retries and timeouts need one owner |",
            "| Mappers | explicit and tested with fixtures | mapping can change observable behavior |",
            "| Validators | tied to synthetic happy/edge/bad cases | validation is part of parity evidence |",
            "",
            "### Model Flow",
            "",
            "```mermaid",
            "flowchart LR",
            f"  Source[\"Legacy/source contract\"] --> Raw[\"{args.raw_model_name}\"]",
            f"  Raw --> Canonical[\"{args.canonical_model_name}\"]",
            "  Canonical --> UseCase[\"Application use case\"]",
            "  UseCase --> Client[\"Enrichment client adapter\"]",
            "  Client --> Enrichment[\"Synthetic or real enrichment source\"]",
            f"  UseCase --> Enriched[\"{args.enriched_model_name}\"]",
            "  Enriched --> Response[\"Boundary response DTO\"]",
            "```",
            "",
            "### Validation Gates",
            "",
            "| Gate | Required Evidence |",
            "| --- | --- |",
            "| Before implementation | accepted mock strategy, scenario matrix and model-governance policy |",
            "| Before adapter coding | contract-backed mock scenarios for happy, edge and bad cases |",
            "| Before mapper coding | raw, canonical and enriched fixture pairs accepted |",
            "| Before review | use-case fake tests and adapter mock-server tests passing |",
            "| Before closeout | fixture IDs, parity evidence and residual data/model risks recorded |",
            "",
        ]
    )


def append_spanish_body(
    lines: list[str],
    args: argparse.Namespace,
    inventory: dict[str, object],
    pom: dict[str, object],
    signals: list[CodeSignal],
    generated_at: str,
) -> None:
    summary = source_summary(inventory)
    lines.extend(
        [
            "## Version En Espanol",
            "",
            "### Recomendacion",
            "",
            "- Usar dos tipos de dobles de prueba en la frontera correcta:",
            "  fakes in-process para tests rapidos de casos de uso y mock server basado en contrato para adapter, ACL y paridad E2E.",
            f"- Preservar `{args.raw_model_name}` como registro fuente/canonico no mutado.",
            f"- Exponer `{args.enriched_model_name}` como vista/resultado ensamblado separado.",
            f"- Usar `{args.canonical_model_name}` como modelo interno estable solo cuando el target necesite un modelo curado.",
            "- Gobernar DTOs generados, modelos internos, modelos de enrichment, clients, adapters y mappers de forma explicita.",
            "- Mantener synthetic data deterministica, pequena, segura y trazable a behavior IDs y evidence IDs.",
            "",
            "### Entradas Detectadas",
            "",
            f"- Generado: {generated_at}",
            f"- Sistema fuente: {args.source_system or inventory.get('source_name', 'source system')}",
            f"- Sistema target: {args.target_system}",
            f"- Candidatos descubiertos: {summary['count']}",
            f"- Split por tipo: {counter_text(summary['kind'])}",
            f"- Split por metodo: {counter_text(summary['method'])}",
            f"- Split por riesgo: {counter_text(summary['risk'])}",
            f"- Senales de testing stack: {testing_stack_summary(pom)}",
            f"- Roadmap relacionado: `{args.roadmap_path}`",
            f"- Technical foundation relacionada: `{args.technical_foundation_path}`",
            "",
            "### Contexto Curado",
            "",
            "| Contexto | Tratamiento |",
            "| --- | --- |",
        ]
    )
    if args.domain_context:
        for item in args.domain_context:
            lines.append(f"| {markdown_cell(item)} | convertir en regla explicita de modelo, mock o fixture |")
    else:
        lines.append("| no provisto | usar inventario y senales de codigo como punto de partida |")
    lines.extend(
        [
            "",
            "### Senales Desde Codigo",
            "",
            "El scan guarda terminos y anchors relativos. No copia extractos de codigo fuente.",
            "",
            "| Senal | Clasificacion | Anchor | Accion Requerida |",
            "| --- | --- | --- | --- |",
        ]
    )
    if signals:
        for signal in signals:
            lines.append(
                "| "
                f"`{markdown_cell(signal.term)}` | "
                f"{markdown_cell(signal.classification)} | "
                f"`{markdown_cell(signal.anchor)}` | "
                f"{markdown_cell(signal.action)} |"
            )
    else:
        lines.append("| ninguna | sin scan o sin match | n/a | revisar manualmente antes de implementar |")
    lines.extend(
        [
            "",
            "### Decision De Mock Server",
            "",
            "| Decision | Opcion A | Opcion B | Recomendacion | Gate |",
            "| --- | --- | --- | --- | --- |",
            "| Tests de caso de uso | fakes in-process | mock server externo | fakes in-process para velocidad y assertions claras | developer/QA review |",
            "| Tests de adapter/ACL | stubs manuales de cliente | mock server basado en contrato | mock server basado en contrato para paridad HTTP/API y fallos | architecture review |",
            "| Paridad E2E | llamar sistemas reales | mocks locales deterministicos | mocks locales salvo entorno certificado seguro | QA review |",
            "| Upstreams lentos/no disponibles | omitir tests | simular timeouts/errores | simular timeout, retry y payload malformado | parity plan |",
            "",
            "### Frontera Del Mock Server",
            "",
            "```mermaid",
            "flowchart LR",
            "  Test[\"Test de paridad o integracion\"] --> Target[\"Servicio target bajo prueba\"]",
            "  Target --> Adapter[\"Adapter / ACL\"]",
            "  Adapter --> Mock[\"Mock server basado en contrato\"]",
            "  Mock --> Fixtures[\"Fixtures sinteticos por escenario\"]",
            "  Fixtures --> Evidence[\"Evidencia de paridad EV-*\"]",
            "```",
            "",
            "### Matriz De Escenarios Sinteticos",
            "",
            "| ID | Perfil Fixture | Comportamiento Mock | Proposito De Evidencia |",
            "| --- | --- | --- | --- |",
        ]
    )
    for scenario_id, profile, behavior, purpose in scenario_rows(summary):
        lines.append(f"| {scenario_id} | `{profile}` | {behavior} | {purpose} |")
    lines.extend(
        [
            "",
            "### Gobierno De Synthetic Data",
            "",
            "| Regla | Razon |",
            "| --- | --- |",
            "| No usar datos productivos ni payloads privados copiados | mantiene los artefactos seguros y revisables |",
            "| IDs de fixture deterministicos | hace los fallos reproducibles y comparables |",
            "| Un perfil de fixture por riesgo de comportamiento | evita esconder edge cases en un payload grande |",
            "| Pares validos/invalidos | prueba validacion y errores de forma intencional |",
            "| Golden-master snapshots solo para contratos observables | evita acoplar tests a implementacion privada |",
            "| Ownership de fixtures en el package index | mantiene cambios trazables a behavior, spec o decision |",
            "",
            "### Gobierno De Modelos",
            "",
            "| Artefacto | Politica | Motivo |",
            "| --- | --- | --- |",
            f"| `{args.raw_model_name}` | preservar como registro fuente/canonico no enriquecido | evita que enrichment corrompa el contrato base |",
            f"| `{args.enriched_model_name}` | ensamblar como modelo separado de lectura/resultado | hace el enrichment opcional, testeable y auditable |",
            f"| `{args.canonical_model_name}` | curar solo cuando existan invariantes target | evita tratar schemas generados como comportamiento de dominio |",
            "| DTOs generados | solo frontera | los contratos de transporte no deben filtrarse a casos de uso |",
            "| Modelos de enrichment | modelos curados explicitos | las reglas de enrichment son sensibles al comportamiento |",
            "| Clients | aislados detras de adapters/ACLs | fallos, retries y timeouts necesitan un owner |",
            "| Mappers | explicitos y testeados con fixtures | el mapping puede cambiar comportamiento observable |",
            "| Validators | ligados a happy/edge/bad cases sinteticos | la validacion es parte de la evidencia de paridad |",
            "",
            "### Flujo De Modelos",
            "",
            "```mermaid",
            "flowchart LR",
            f"  Source[\"Contrato legacy/source\"] --> Raw[\"{args.raw_model_name}\"]",
            f"  Raw --> Canonical[\"{args.canonical_model_name}\"]",
            "  Canonical --> UseCase[\"Caso de uso de aplicacion\"]",
            "  UseCase --> Client[\"Adapter de cliente de enrichment\"]",
            "  Client --> Enrichment[\"Fuente de enrichment sintetica o real\"]",
            f"  UseCase --> Enriched[\"{args.enriched_model_name}\"]",
            "  Enriched --> Response[\"DTO de respuesta en frontera\"]",
            "```",
            "",
            "### Gates De Validacion",
            "",
            "| Gate | Evidencia Requerida |",
            "| --- | --- |",
            "| Antes de implementar | mock strategy, scenario matrix y model-governance policy aceptadas |",
            "| Antes de codificar adapters | escenarios mock para happy, edge y bad cases |",
            "| Antes de codificar mappers | pares de fixtures raw, canonico y enriched aceptados |",
            "| Antes de review | tests de use-case con fakes y tests de adapter con mock server pasando |",
            "| Antes de closeout | fixture IDs, evidencia de paridad y riesgos de data/model registrados |",
            "",
        ]
    )


def build_document(args: argparse.Namespace) -> str:
    inventory = load_inventory(args.inventory_json)
    pom = parse_pom(args.target_pom)
    signals = scan_code_signals(args)
    generated_at = utc_now()
    lines = [
        f"# Mock Server, Synthetic Data And Model Governance - {args.target_system}",
        "",
        "Status: draft",
        f"Language policy: {args.language_policy}",
        f"Sensitivity: {args.sensitivity}",
        f"Related roadmap: `{args.roadmap_path}`",
        f"Related technical foundation: `{args.technical_foundation_path}`",
        f"Related discovery inventory: `{display_path(args.inventory_json)}`",
        "",
        "## Purpose",
        "",
        "Define how migration packages should use mock servers, synthetic data and",
        "model governance to preserve observable behavior while improving the target",
        "architecture.",
        "",
    ]
    if args.language_policy == "spanish-first":
        append_spanish_body(lines, args, inventory, pom, signals, generated_at)
    append_english_body(lines, args, inventory, pom, signals, generated_at)
    lines.extend(
        [
            "## Open Questions",
            "",
            "| Question | Owner | Blocks | Status |",
            "| --- | --- | --- | --- |",
            "| Which mock-server tool is already approved by the target platform? | architect/developer | adapter tests | open |",
            "| Which fixtures become golden-master parity snapshots? | QA reviewer/spec-owner | parity plan | open |",
            "| Which model names are canonical in the target codebase? | architect/spec-owner | implementation brief | open |",
            "",
            "## Search Anchors",
            "",
            "- mock server strategy",
            "- synthetic test data",
            "- model governance",
            "- enriched record",
            "- non-enriched record",
            "- anti-corruption layer",
            "- parity fixtures",
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    args = parse_args()
    try:
        text = build_document(args)
    except (OSError, json.JSONDecodeError, ET.ParseError) as exc:
        print(str(exc), file=sys.stderr)
        return 2

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text, encoding="utf-8")
    print(f"Wrote {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
