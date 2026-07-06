#!/usr/bin/env python3
"""Generate a technical foundation and architecture blueprint document."""

from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path


DEFAULT_STACK = "Java 21, Spring Boot, OpenAPI Generator"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Generate a technical foundation spec from discovery metadata."
    )
    parser.add_argument("--inventory-json", required=True, type=Path)
    parser.add_argument("--target-system", required=True)
    parser.add_argument("--source-system")
    parser.add_argument("--target-pom", type=Path)
    parser.add_argument("--base-package")
    parser.add_argument("--language-policy", choices=("english", "spanish-first"), default="english")
    parser.add_argument("--sensitivity", default="internal")
    parser.add_argument("--roadmap-path", default="migration-roadmap.md")
    parser.add_argument("--output", required=True, type=Path)
    return parser.parse_args()


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
            "properties": {},
            "api_package": "not detected",
            "model_package": "not detected",
            "input_spec": "not detected",
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
        "properties": properties,
        "api_package": properties.get("openapi-generator-maven-plugin.apiPackage", "not detected"),
        "model_package": properties.get("openapi-generator-maven-plugin.modelPackage", "not detected"),
        "input_spec": properties.get("openapi-generator-maven-plugin.inputSpec", "not detected"),
    }


def dependency_contains(pom: dict[str, object], value: str) -> bool:
    dependencies = pom.get("dependencies", [])
    return any(value in item for item in dependencies if isinstance(item, str))


def company_libraries(pom: dict[str, object]) -> list[str]:
    dependencies = pom.get("dependencies", [])
    return [
        item
        for item in dependencies
        if isinstance(item, str)
        and (
            "arch-ram" in item
            or ".lib." in item
        )
    ]


def source_summary(inventory: dict[str, object]) -> dict[str, object]:
    features = inventory.get("features", [])
    if not isinstance(features, list):
        features = []
    counters = {
        "count": len(features),
        "risk": Counter(str(item.get("risk", "unknown")) for item in features if isinstance(item, dict)),
        "method": Counter(str(item.get("operation", "unknown")) for item in features if isinstance(item, dict)),
        "kind": Counter(str(item.get("kind", "unknown")) for item in features if isinstance(item, dict)),
        "source": Counter(str(item.get("source_path", "unknown")) for item in features if isinstance(item, dict)),
    }
    return counters


def counter_text(counter: Counter[str]) -> str:
    if not counter:
        return "none"
    return ", ".join(f"{key}: {value}" for key, value in sorted(counter.items()))


def detected_stack(pom: dict[str, object]) -> str:
    java_version = pom.get("java_version", "not detected")
    spring_version = pom.get("spring_boot_version", "not detected")
    if java_version == "not detected" and spring_version == "not detected":
        return DEFAULT_STACK
    return f"Java {java_version}, Spring Boot {spring_version}, OpenAPI Generator"


def base_package(args: argparse.Namespace, pom: dict[str, object]) -> str:
    if args.base_package:
        return args.base_package
    api_package = str(pom.get("api_package", ""))
    match = re.match(r"(.+)\.web\.api$", api_package)
    if match:
        return match.group(1)
    return "target.base.package"


def english_body(
    args: argparse.Namespace,
    inventory: dict[str, object],
    pom: dict[str, object],
    generated_at: str,
) -> list[str]:
    summary = source_summary(inventory)
    libs = company_libraries(pom)
    base = base_package(args, pom)
    lines = [
        "## English Engineering Mirror",
        "",
        "### Recommendation",
        "",
        f"- Use a vertical-slice architecture inside `{args.target_system}`.",
        "- Keep generated OpenAPI API interfaces and DTOs at the boundary.",
        "- Put orchestration in application use cases.",
        "- Curate domain/application models only where business rules or invariants exist.",
        "- Use adapters/ACLs for external, legacy and company-library integration boundaries.",
        "- Use explicit mappers when crossing generated DTO, domain and integration boundaries.",
        "- Use guard clauses at web/application boundaries and normalize errors consistently.",
        "- Enforce boundaries with architecture tests where the target stack supports them.",
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
        f"- Stack: {detected_stack(pom)}",
        f"- OpenAPI input spec: `{pom.get('input_spec', 'not detected')}`",
        f"- Generated API package: `{pom.get('api_package', 'not detected')}`",
        f"- Generated DTO package: `{pom.get('model_package', 'not detected')}`",
        f"- Company/platform libraries detected: {', '.join(libs) if libs else 'none detected'}",
        "",
        "### Foundation Decisions",
        "",
        "| Decision | Option A | Option B | Recommendation | Gate |",
        "| --- | --- | --- | --- | --- |",
        "| Architecture slicing | technical layers only | vertical slices by feature/API area | vertical slices with clean internal boundaries | architecture review |",
        "| Generated DTOs | use generated DTOs everywhere | boundary DTOs only | boundary DTOs only; curate internal models | spec review |",
        "| ACL/adapters | direct calls from use cases | adapter/ACL boundary | adapter/ACL for external, legacy or company contracts | implementation brief |",
        "| Domain model | generate from contracts | curate where invariants exist | curate only where business behavior justifies it | feature package review |",
        "| Defensive style | validate late | guard clauses at boundaries and use cases | guard clauses plus normalized errors | code review |",
        "",
        "### Target Package Blueprint",
        "",
        "```text",
        f"{base}/",
        "  <slice>/",
        "    web/                 generated delegate implementations and request boundary",
        "    application/         use cases and orchestration",
        "    domain/              curated business model and policies when justified",
        "    infrastructure/      adapters, ACLs, external clients and persistence",
        "    mapper/              explicit boundary and integration mapping",
        "    validation/          request, command and invariant validation",
        "```",
        "",
        "### Generation Policy",
        "",
        "| Artifact | Policy | Reason |",
        "| --- | --- | --- |",
        "| API interfaces/delegates | generate from OpenAPI | contract consistency |",
        "| Boundary DTOs | generate and keep at web/client boundary | avoids leaking transport shape inward |",
        "| Application commands/results | curate | use-case contract should be stable and readable |",
        "| Domain models | curate only when invariants exist | generated schemas are not domain behavior |",
        "| ACLs/adapters | curate | integration semantics and errors need judgment |",
        "| Mappers | curate or generate only when behavior-neutral | mapping is often compatibility-sensitive |",
        "| Tests | scaffold names, curate assertions | parity evidence must be intentional |",
        "",
        "### Code Style Rules",
        "",
        "- Use guard clauses for invalid input, unsupported state and missing dependencies.",
        "- Keep controllers/delegates thin and free of domain decisions.",
        "- Keep generated DTOs out of domain/application logic unless explicitly accepted.",
        "- Prefer explicit constructors/factories when invariants exist.",
        "- Normalize errors at the API boundary and preserve legacy error semantics.",
        "- Use company libraries directly when they are the required platform boundary.",
        "- Add an adapter only when it protects behavior, testability or replacement risk.",
        "- Keep transaction boundaries in application services/use cases.",
        "- Keep parity tests traceable to `LB-*`, `AC-*`, `HS-*` and `EV-*` IDs.",
        "",
        "### Validation Gates",
        "",
        "| Gate | Required Evidence |",
        "| --- | --- |",
        "| Before package generation | roadmap item selected and duplicate route review complete |",
        "| Before code generation | source OpenAPI contract selected and target package naming accepted |",
        "| Before implementation | behavior inventory, parity plan, Hard Spec and ADR accepted |",
        "| Before review | generated code isolated, implementation scoped, tests passing |",
        "| Before closeout | parity evidence, residual risk and follow-ups recorded |",
        "",
        "### Architecture Diagram",
        "",
        "```mermaid",
        "flowchart LR",
        "  Client[\"Client or integration\"] --> Web[\"Generated API delegate / web adapter\"]",
        "  Web --> App[\"Application use case\"]",
        "  App --> Domain[\"Domain policy / model where justified\"]",
        "  App --> Port[\"Outbound port\"]",
        "  Port --> ACL[\"Adapter / ACL\"]",
        "  ACL --> External[\"External service, legacy API or company library\"]",
        "```",
        "",
        "### Slice Diagram",
        "",
        "```mermaid",
        "flowchart TB",
        "  Contract[\"OpenAPI contract\"] --> Generated[\"Generated API and DTO boundary\"]",
        "  Generated --> UseCase[\"Feature use case\"]",
        "  UseCase --> Rules[\"Domain rules when justified\"]",
        "  UseCase --> Adapters[\"Adapters, ACLs and clients\"]",
        "  UseCase --> Tests[\"Parity tests and review evidence\"]",
        "```",
    ]
    return lines


def spanish_body(
    args: argparse.Namespace,
    inventory: dict[str, object],
    pom: dict[str, object],
    generated_at: str,
) -> list[str]:
    summary = source_summary(inventory)
    libs = company_libraries(pom)
    base = base_package(args, pom)
    return [
        "## Version En Espanol",
        "",
        "### Recomendacion",
        "",
        f"- Usar arquitectura por vertical slices dentro de `{args.target_system}`.",
        "- Mantener APIs y DTOs generados por OpenAPI en la frontera web/cliente.",
        "- Colocar la orquestacion en casos de uso de aplicacion.",
        "- Curar modelos de dominio/aplicacion solo cuando existan reglas o invariantes reales.",
        "- Usar adaptadores/ACLs para fronteras externas, legacy y librerias corporativas.",
        "- Usar mappers explicitos al cruzar DTOs generados, modelos internos e integraciones.",
        "- Usar guard clauses en fronteras web/aplicacion y normalizar errores de forma consistente.",
        "- Proteger boundaries con tests de arquitectura cuando el stack lo permita.",
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
        f"- Stack: {detected_stack(pom)}",
        f"- OpenAPI input spec: `{pom.get('input_spec', 'not detected')}`",
        f"- Paquete API generado: `{pom.get('api_package', 'not detected')}`",
        f"- Paquete DTO generado: `{pom.get('model_package', 'not detected')}`",
        f"- Librerias/plataforma detectadas: {', '.join(libs) if libs else 'ninguna detectada'}",
        "",
        "### Decisiones De Fundacion",
        "",
        "| Decision | Opcion A | Opcion B | Recomendacion | Gate |",
        "| --- | --- | --- | --- | --- |",
        "| Slicing de arquitectura | capas tecnicas | vertical slices por feature/API | vertical slices con boundaries internos limpios | revision de arquitectura |",
        "| DTOs generados | usarlos en todas las capas | solo frontera | solo frontera; modelos internos curados | revision de spec |",
        "| ACL/adapters | llamadas directas | boundary adapter/ACL | ACL para contratos externos, legacy o corporativos | implementation brief |",
        "| Modelo de dominio | generar desde contratos | curar donde existan invariantes | curar solo donde haya comportamiento de negocio | revision de paquete |",
        "| Estilo defensivo | validar tarde | guard clauses en fronteras y casos de uso | guard clauses mas errores normalizados | code review |",
        "",
        "### Blueprint De Paquetes Target",
        "",
        "```text",
        f"{base}/",
        "  <slice>/",
        "    web/                 implementaciones delegate generadas y frontera request",
        "    application/         casos de uso y orquestacion",
        "    domain/              modelo y politicas de negocio cuando se justifique",
        "    infrastructure/      adapters, ACLs, clientes externos y persistencia",
        "    mapper/              mapping explicito de frontera e integracion",
        "    validation/          validacion de request, command e invariantes",
        "```",
        "",
        "### Politica De Generacion",
        "",
        "| Artefacto | Politica | Motivo |",
        "| --- | --- | --- |",
        "| Interfaces/delegates API | generar desde OpenAPI | consistencia de contrato |",
        "| DTOs de frontera | generar y mantener en web/client boundary | evita filtrar transporte hacia dentro |",
        "| Commands/results de aplicacion | curar | contrato del caso de uso estable y legible |",
        "| Modelos de dominio | curar solo con invariantes | schemas generados no son comportamiento de dominio |",
        "| ACLs/adapters | curar | semantica de integracion y errores requiere criterio |",
        "| Mappers | curar o generar solo si es behavior-neutral | el mapping suele ser sensible a compatibilidad |",
        "| Tests | scaffolding de nombres, assertions curadas | la evidencia de paridad debe ser intencional |",
        "",
        "### Reglas De Codigo",
        "",
        "- Usar guard clauses para input invalido, estado no soportado y dependencias requeridas.",
        "- Mantener controllers/delegates delgados y sin decisiones de dominio.",
        "- No filtrar DTOs generados hacia dominio/aplicacion salvo decision explicita.",
        "- Preferir constructores/factories explicitos cuando haya invariantes.",
        "- Normalizar errores en la frontera API y preservar semantica legacy.",
        "- Usar librerias corporativas directamente cuando sean el boundary de plataforma requerido.",
        "- Agregar adapter solo cuando proteja comportamiento, testabilidad o riesgo de reemplazo.",
        "- Mantener boundaries transaccionales en servicios/casos de uso de aplicacion.",
        "- Trazar tests de paridad contra IDs `LB-*`, `AC-*`, `HS-*` y `EV-*`.",
        "",
        "### Gates De Validacion",
        "",
        "| Gate | Evidencia Requerida |",
        "| --- | --- |",
        "| Antes de generar paquetes | roadmap item seleccionado y duplicados revisados |",
        "| Antes de generar codigo | contrato OpenAPI fuente seleccionado y naming target aceptado |",
        "| Antes de implementar | behavior inventory, parity plan, Hard Spec y ADR aceptados |",
        "| Antes de review | codigo generado aislado, implementacion acotada y tests pasando |",
        "| Antes de closeout | evidencia de paridad, riesgo residual y follow-ups registrados |",
        "",
        "### Diagrama De Arquitectura",
        "",
        "```mermaid",
        "flowchart LR",
        "  Client[\"Cliente o integracion\"] --> Web[\"API delegate generado / web adapter\"]",
        "  Web --> App[\"Caso de uso de aplicacion\"]",
        "  App --> Domain[\"Politica/modelo de dominio si se justifica\"]",
        "  App --> Port[\"Puerto outbound\"]",
        "  Port --> ACL[\"Adapter / ACL\"]",
        "  ACL --> External[\"Servicio externo, API legacy o libreria corporativa\"]",
        "```",
        "",
        "### Diagrama De Slice",
        "",
        "```mermaid",
        "flowchart TB",
        "  Contract[\"Contrato OpenAPI\"] --> Generated[\"API y DTOs generados en frontera\"]",
        "  Generated --> UseCase[\"Caso de uso de feature\"]",
        "  UseCase --> Rules[\"Reglas de dominio si se justifican\"]",
        "  UseCase --> Adapters[\"Adapters, ACLs y clientes\"]",
        "  UseCase --> Tests[\"Tests de paridad y evidencia de review\"]",
        "```",
        "",
    ]


def build_document(args: argparse.Namespace) -> str:
    inventory = load_inventory(args.inventory_json)
    pom = parse_pom(args.target_pom)
    generated_at = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    lines = [
        f"# Technical Foundation And Architecture Blueprint - {args.target_system}",
        "",
        "Status: draft",
        f"Language policy: {args.language_policy}",
        f"Sensitivity: {args.sensitivity}",
        f"Related roadmap: `{args.roadmap_path}`",
        f"Related discovery inventory: `{display_path(args.inventory_json)}`",
        "",
        "## Purpose",
        "",
        "Define the architecture, generation rules and code-style constraints that",
        "migration packages must follow before implementation starts.",
        "",
    ]
    if args.language_policy == "spanish-first":
        lines.extend(spanish_body(args, inventory, pom, generated_at))
    lines.extend(english_body(args, inventory, pom, generated_at))
    lines.extend(
        [
            "",
            "## Open Questions",
            "",
            "| Question | Owner | Blocks | Status |",
            "| --- | --- | --- | --- |",
            "| Which vertical slice naming convention should be enforced first? | architect | package generation | open |",
            "| Which duplicate OpenAPI routes represent the same target package? | architect/spec-owner | package generation | open |",
            "| Which architecture tests should be mandatory in the target repo? | developer/qa-reviewer | implementation | open |",
            "",
            "## Search Anchors",
            "",
            "- technical foundation",
            "- architecture blueprint",
            "- vertical slice",
            "- generated DTOs",
            "- anti-corruption layer",
            "- guard clauses",
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
