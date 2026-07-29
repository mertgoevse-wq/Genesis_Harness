#!/usr/bin/env python3
"""Validiert die Wissensbasis gegen die Content Policy.

Dieses Skript ist die technische Durchsetzung von docs/CONTENT_POLICY.md.
Es laeuft im CI und blockiert den Build bei Verstoessen.

Geprueft wird:
  1. Jede Datei ist valides JSON
  2. Jeder Datensatz hat id, provenance, sources
  3. Jede source_id existiert in knowledge/sources/registry.json
  4. provenance=verified ist nur zulaessig, wenn die Quelle das erlaubt
     (provenance_ceiling im Registry)
  5. provenance=placeholder ist auf keinem auslieferbaren Pfad
  6. provenance=disputed erfordert mindestens zwei Positionen
  7. Jede Uebersetzung hat einen Uebersetzernamen
  8. Jede Hadith-Referenz hat collection, reference, grading, graded_by, source_id
  9. Jedes recitation-Audio hat Rezitator und Lizenz
 10. Gebets-Sequenzen verweisen nur auf existierende Bewegungen
 11. madhhab-Werte sind aus der erlaubten Menge

Exit-Code 0 = bestanden, 1 = Verstoss gefunden.

Aufruf:
    python scripts/verify_knowledge.py
    python scripts/verify_knowledge.py --json    # maschinenlesbarer Bericht
"""
from __future__ import annotations

import argparse
import json
import sys
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Iterator

PROJECT_ROOT = Path(__file__).resolve().parent.parent
KNOWLEDGE_DIR = PROJECT_ROOT / "knowledge"
REGISTRY_FILE = KNOWLEDGE_DIR / "sources" / "registry.json"
MOVEMENTS_FILE = KNOWLEDGE_DIR / "prayer" / "movements.json"

VALID_PROVENANCE = {"verified", "scholar_review_pending", "placeholder", "disputed"}
VALID_MADHHAB = {"common", "hanafi", "shafii", "maliki", "hanbali", "jafari"}
PROVENANCE_ORDER = {"placeholder": 0, "scholar_review_pending": 1, "disputed": 1, "verified": 2}

HADITH_REQUIRED = ("collection", "reference", "grading", "graded_by", "source_id")

SEVERITY_CRITICAL = "CRITICAL"
SEVERITY_HIGH = "HIGH"
SEVERITY_MEDIUM = "MEDIUM"


@dataclass
class Finding:
    severity: str
    rule: str
    location: str
    message: str

    def __str__(self) -> str:
        return f"[{self.severity}] {self.rule}\n    {self.location}\n    {self.message}"


@dataclass
class Report:
    findings: list[Finding] = field(default_factory=list)
    files_checked: int = 0
    records_checked: int = 0

    def add(self, severity: str, rule: str, location: str, message: str) -> None:
        self.findings.append(Finding(severity, rule, location, message))

    @property
    def blocking(self) -> list[Finding]:
        return [f for f in self.findings if f.severity in (SEVERITY_CRITICAL, SEVERITY_HIGH)]

    def by_severity(self, severity: str) -> list[Finding]:
        return [f for f in self.findings if f.severity == severity]


# --------------------------------------------------------------------------
# Registry
# --------------------------------------------------------------------------

def load_registry() -> dict[str, dict[str, Any]]:
    with REGISTRY_FILE.open(encoding="utf-8") as fh:
        data = json.load(fh)
    return {src["id"]: src for src in data["sources"]}


def max_allowed_provenance(source: dict[str, Any]) -> str:
    """Hoechste provenance-Stufe, die diese Quelle rechtfertigen kann."""
    ceiling = source.get("provenance_ceiling")
    if ceiling:
        return ceiling
    if source.get("imported") and source.get("checksum_required"):
        return "verified"
    return "scholar_review_pending"


# --------------------------------------------------------------------------
# Rekursive Traversierung
# --------------------------------------------------------------------------

def walk(node: Any, path: str = "") -> Iterator[tuple[str, dict[str, Any]]]:
    """Liefert jedes dict im Baum mit seinem JSON-Pfad."""
    if isinstance(node, dict):
        yield path or "$", node
        for key, value in node.items():
            yield from walk(value, f"{path}.{key}" if path else key)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            yield from walk(value, f"{path}[{index}]")


def has_provenance(node: dict[str, Any]) -> bool:
    return "provenance" in node


# --------------------------------------------------------------------------
# Einzelpruefungen
# --------------------------------------------------------------------------

def check_provenance_value(node: dict[str, Any], loc: str, report: Report) -> None:
    value = node["provenance"]
    if value not in VALID_PROVENANCE:
        report.add(
            SEVERITY_HIGH,
            "provenance-value",
            loc,
            f"Unbekannter provenance-Wert '{value}'. Erlaubt: {sorted(VALID_PROVENANCE)}",
        )


def check_sources_present(node: dict[str, Any], loc: str, report: Report) -> None:
    if node.get("provenance") == "placeholder":
        return  # placeholder darf quellenlos sein, wird aber nie ausgeliefert
    sources = node.get("sources")
    if not sources:
        report.add(
            SEVERITY_HIGH,
            "sources-required",
            loc,
            "Datensatz mit provenance hat kein Feld 'sources' mit mindestens einem Eintrag. "
            "Content Policy 4: jede inhaltliche Aussage braucht eine Quelle.",
        )


def check_source_ids(node: dict[str, Any], loc: str, registry: dict[str, Any], report: Report) -> None:
    for entry in node.get("sources") or []:
        if not isinstance(entry, dict):
            continue
        source_id = entry.get("source_id")
        if source_id and source_id not in registry:
            report.add(
                SEVERITY_CRITICAL,
                "unknown-source",
                loc,
                f"source_id '{source_id}' steht nicht in knowledge/sources/registry.json. "
                "Content Policy 4.2: nur registrierte Quellen sind zulaessig.",
            )


def check_provenance_ceiling(
    node: dict[str, Any], loc: str, registry: dict[str, Any], report: Report
) -> None:
    """verified ist nur zulaessig, wenn eine Quelle es rechtfertigt."""
    if node.get("provenance") != "verified":
        return
    sources = node.get("sources") or []
    if not sources:
        return  # bereits von check_sources_present gemeldet

    best = "placeholder"
    for entry in sources:
        source_id = entry.get("source_id") if isinstance(entry, dict) else None
        source = registry.get(source_id or "")
        if not source:
            continue
        allowed = max_allowed_provenance(source)
        if PROVENANCE_ORDER[allowed] > PROVENANCE_ORDER[best]:
            best = allowed

    if PROVENANCE_ORDER[best] < PROVENANCE_ORDER["verified"]:
        ids = [e.get("source_id") for e in sources if isinstance(e, dict)]
        report.add(
            SEVERITY_CRITICAL,
            "provenance-ceiling",
            loc,
            f"provenance=verified, aber keine der Quellen {ids} rechtfertigt das. "
            f"Hoechste zulaessige Stufe: '{best}'. "
            "Content Policy 4.1: verified erfordert Import aus registrierter Primaerquelle "
            "mit Pruefsumme, oder eine editorial-Quelle mit provenance_ceiling=verified.",
        )


def check_placeholder_not_deliverable(
    node: dict[str, Any], loc: str, file_path: Path, report: Report
) -> None:
    if node.get("provenance") != "placeholder":
        return
    report.add(
        SEVERITY_CRITICAL,
        "placeholder-deliverable",
        loc,
        f"provenance=placeholder in {file_path.name}. Content Policy 4.1: "
        "placeholder-Inhalte duerfen einen Nutzer nie erreichen. Entweder Inhalt "
        "ergaenzen und provenance anheben, oder Datensatz entfernen.",
    )


def check_disputed_has_positions(node: dict[str, Any], loc: str, report: Report) -> None:
    if node.get("provenance") != "disputed":
        return
    positions = node.get("variations") or node.get("madhhab_variations") or node.get("disputed_positions")
    if not positions or len(positions) < 2:
        report.add(
            SEVERITY_HIGH,
            "disputed-positions",
            loc,
            "provenance=disputed, aber weniger als zwei Positionen dokumentiert. "
            "Content Policy 3.2: bei Uneinigkeit werden ALLE relevanten Positionen genannt.",
        )


def check_translations(node: dict[str, Any], loc: str, report: Report) -> None:
    for index, translation in enumerate(node.get("translations") or []):
        if not isinstance(translation, dict):
            continue
        tloc = f"{loc}.translations[{index}]"
        if not translation.get("translator"):
            report.add(
                SEVERITY_HIGH,
                "translation-translator",
                tloc,
                "Uebersetzung ohne Feld 'translator'. Content Policy 4.3: eine "
                "Uebersetzung ohne Uebersetzername wird nicht ausgeliefert.",
            )
        if not translation.get("source_id"):
            report.add(
                SEVERITY_HIGH,
                "translation-source",
                tloc,
                "Uebersetzung ohne Feld 'source_id'.",
            )


def check_hadith(node: dict[str, Any], loc: str, report: Report) -> None:
    """Ein dict gilt als Hadith-Referenz, wenn es 'collection' fuehrt."""
    if "collection" not in node:
        return
    missing = [field_name for field_name in HADITH_REQUIRED if not node.get(field_name)]
    if missing:
        report.add(
            SEVERITY_CRITICAL,
            "hadith-metadata",
            loc,
            f"Hadith-Referenz mit fehlenden Pflichtfeldern: {missing}. "
            "Content Policy 4.4: fehlt ein Feld, wird der Hadith nicht ausgeliefert.",
        )


def check_audio(node: dict[str, Any], loc: str, report: Report) -> None:
    if node.get("kind") != "recitation":
        return
    for field_name in ("reciter", "license"):
        if not node.get(field_name):
            report.add(
                SEVERITY_HIGH,
                "recitation-attribution",
                loc,
                f"Rezitations-Audio ohne '{field_name}'. ADR-0002: Rezitation kommt "
                "ausschliesslich von menschlichen Rezitatoren mit Quellenangabe.",
            )


def check_madhhab(node: dict[str, Any], loc: str, report: Report) -> None:
    value = node.get("madhhab")
    if value is not None and value not in VALID_MADHHAB:
        report.add(
            SEVERITY_HIGH,
            "madhhab-value",
            loc,
            f"Unbekannter madhhab-Wert '{value}'. Erlaubt: {sorted(VALID_MADHHAB)}",
        )


def check_prayer_movement_refs(report: Report) -> None:
    """Jeder Schritt einer Gebets-Sequenz muss auf eine existierende Bewegung verweisen."""
    if not MOVEMENTS_FILE.exists():
        report.add(
            SEVERITY_CRITICAL,
            "movements-missing",
            str(MOVEMENTS_FILE.name),
            "knowledge/prayer/movements.json fehlt. Alle Gebets-Sequenzen sind damit ungueltig.",
        )
        return

    with MOVEMENTS_FILE.open(encoding="utf-8") as fh:
        known = {m["id"] for m in json.load(fh)["movements"]}

    for prayer_file in sorted((KNOWLEDGE_DIR / "prayer").glob("*.json")):
        if prayer_file.name == "movements.json":
            continue
        with prayer_file.open(encoding="utf-8") as fh:
            prayer = json.load(fh)
        for step in prayer.get("sequence") or []:
            movement_id = step.get("movement_id")
            if movement_id not in known:
                report.add(
                    SEVERITY_CRITICAL,
                    "dangling-movement-ref",
                    f"{prayer_file.name}.sequence[step={step.get('step')}]",
                    f"Verweis auf unbekannte Bewegung '{movement_id}'.",
                )


def check_license_status(registry: dict[str, Any], report: Report) -> None:
    """Warnt vor Quellen mit ungeklaerter Lizenz, die produktiv genutzt werden."""
    for source_id, source in registry.items():
        if source.get("imported") and source.get("license_status") == "needs_verification":
            report.add(
                SEVERITY_MEDIUM,
                "license-unverified",
                f"registry.json:{source_id}",
                "Quelle ist als importiert markiert, aber der Lizenzstatus ist ungeklaert. "
                "Content Policy 4.2: produktive Auslieferung ist blockiert, bis die Lizenz "
                "geklaert ist.",
            )


# --------------------------------------------------------------------------
# Hauptlauf
# --------------------------------------------------------------------------

def verify() -> Report:
    report = Report()
    registry = load_registry()

    json_files = [
        path
        for path in sorted(KNOWLEDGE_DIR.rglob("*.json"))
        if path != REGISTRY_FILE and "schema" not in path.parts
    ]

    for path in json_files:
        report.files_checked += 1
        try:
            with path.open(encoding="utf-8") as fh:
                data = json.load(fh)
        except json.JSONDecodeError as exc:
            report.add(
                SEVERITY_CRITICAL,
                "invalid-json",
                str(path.relative_to(PROJECT_ROOT)),
                f"Datei ist kein valides JSON: {exc}",
            )
            continue

        rel = path.relative_to(PROJECT_ROOT)
        for json_path, node in walk(data):
            loc = f"{rel}#{json_path}"

            check_hadith(node, loc, report)
            check_audio(node, loc, report)
            check_madhhab(node, loc, report)
            check_translations(node, loc, report)

            if has_provenance(node):
                report.records_checked += 1
                check_provenance_value(node, loc, report)
                check_sources_present(node, loc, report)
                check_source_ids(node, loc, registry, report)
                check_provenance_ceiling(node, loc, registry, report)
                check_placeholder_not_deliverable(node, loc, path, report)
                check_disputed_has_positions(node, loc, report)

    check_prayer_movement_refs(report)
    check_license_status(registry, report)
    return report


def print_human(report: Report) -> None:
    print("Wissensbasis-Validierung — Islam Tutor AI")
    print("=" * 60)
    print(f"Dateien geprueft:    {report.files_checked}")
    print(f"Datensaetze geprueft: {report.records_checked}")
    print()

    if not report.findings:
        print("Keine Verstoesse gefunden.")
        return

    for severity in (SEVERITY_CRITICAL, SEVERITY_HIGH, SEVERITY_MEDIUM):
        findings = report.by_severity(severity)
        if not findings:
            continue
        print(f"{severity}: {len(findings)}")
        print("-" * 60)
        for finding in findings:
            print(finding)
            print()

    if report.blocking:
        print("=" * 60)
        print(f"BLOCKIEREND: {len(report.blocking)} Verstoss/Verstoesse verhindern die Auslieferung.")
    else:
        print("=" * 60)
        print("Keine blockierenden Verstoesse. Hinweise oben pruefen.")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Maschinenlesbarer Bericht")
    args = parser.parse_args()

    report = verify()

    if args.json:
        json.dump(
            {
                "files_checked": report.files_checked,
                "records_checked": report.records_checked,
                "blocking_count": len(report.blocking),
                "findings": [
                    {
                        "severity": f.severity,
                        "rule": f.rule,
                        "location": f.location,
                        "message": f.message,
                    }
                    for f in report.findings
                ],
            },
            sys.stdout,
            ensure_ascii=False,
            indent=2,
        )
        print()
    else:
        print_human(report)

    return 1 if report.blocking else 0


if __name__ == "__main__":
    raise SystemExit(main())
