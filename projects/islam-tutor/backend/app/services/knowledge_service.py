"""Zugriff auf die Wissensbasis — die einzige Auslieferungsgrenze.

Architektur-Invariante (docs/ARCHITECTURE.md 5.1): kein `placeholder`-Inhalt
verlaesst das Backend. Diese Regel ist hier durchgesetzt, nicht in den Routen.
Eine Route, die Wissensdaten liefert, ruft diesen Service — sie liest keine
Datei direkt. Damit gibt es genau eine Stelle, an der die Invariante gelten muss.

Caching: die Wissensbasis besteht aus Dateien, die sich selten aendern. Sie wird
einmal geladen und bei Aenderung der Datei-Mtime neu eingelesen. Kein TTL, weil
ein Zeitablauf hier nichts abbildet — relevant ist die Datei, nicht die Uhr.
"""
from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from ai.guardrails.provenance_filter import ProvenanceFilter, assert_deliverable


class KnowledgeNotFound(Exception):
    """Ein angefragter Datensatz existiert nicht."""


class KnowledgeBlocked(Exception):
    """Ein Datensatz existiert, ist aber nicht auslieferbar."""


@dataclass(frozen=True)
class _CacheEntry:
    mtime: float
    data: dict[str, Any]


class KnowledgeService:
    """Laedt, filtert und liefert Inhalte der Wissensbasis."""

    def __init__(self, knowledge_dir: Path) -> None:
        self.root = knowledge_dir
        self._cache: dict[Path, _CacheEntry] = {}

    # ------------------------------------------------------------------
    # Laden
    # ------------------------------------------------------------------

    def _read(self, path: Path) -> dict[str, Any]:
        if not path.exists():
            raise KnowledgeNotFound(f"{path.name} existiert nicht.")

        mtime = path.stat().st_mtime
        cached = self._cache.get(path)
        if cached and cached.mtime == mtime:
            return cached.data

        with path.open(encoding="utf-8") as fh:
            data = json.load(fh)
        self._cache[path] = _CacheEntry(mtime=mtime, data=data)
        return data

    def invalidate(self) -> None:
        self._cache.clear()

    # ------------------------------------------------------------------
    # Ausliefern
    # ------------------------------------------------------------------

    def _deliver(
        self, data: dict[str, Any], *, madhhab: str | None, language: str, context: str
    ) -> dict[str, Any]:
        """Filtert einen Datensatz und prueft die Invariante.

        Der `assert_deliverable`-Aufruf ist ein Sicherheitsnetz, kein Ersatz fuer
        den Filter. Wenn er ausloest, ist der Filter fehlerhaft — und ein lauter
        Fehler ist besser als ein stiller Policy-Verstoss in Produktion.
        """
        prov_filter = ProvenanceFilter(madhhab=madhhab, language=language)
        result = prov_filter.filter_record(data)

        if result.data is None:
            raise KnowledgeBlocked(
                f"{context} ist nicht auslieferbar (provenance=placeholder oder "
                "Rechtsschule passt nicht)."
            )

        assert_deliverable(result.data, context=context)

        payload = dict(result.data)
        payload["_meta"] = {
            "removed_records": result.removed_count,
            "review_pending_count": result.review_pending_count,
            "disputed_count": result.disputed_count,
            "madhhab_filter": madhhab,
        }
        return payload

    # ------------------------------------------------------------------
    # Gebet
    # ------------------------------------------------------------------

    def list_prayers(self, *, language: str = "de") -> list[dict[str, Any]]:
        """Kurzliste aller Gebete fuer Navigationszwecke."""
        out: list[dict[str, Any]] = []
        for path in sorted((self.root / "prayer").glob("*.json")):
            if path.name == "movements.json":
                continue
            data = self._read(path)
            if data.get("provenance") == "placeholder":
                continue
            name = data.get("name", {})
            translations = name.get("translations", {})
            out.append(
                {
                    "id": data["id"],
                    "order": data.get("order"),
                    "name_arabic": name.get("arabic"),
                    "name_transliteration": name.get("transliteration"),
                    "name_local": translations.get(language) or translations.get("en"),
                    "fard_rakat": data.get("units", {}).get("fard"),
                    "step_count": len(data.get("sequence", [])),
                    "provenance": data.get("provenance"),
                }
            )
        return sorted(out, key=lambda p: p.get("order") or 99)

    def get_prayer(
        self, prayer_id: str, *, madhhab: str | None = None, language: str = "de"
    ) -> dict[str, Any]:
        """Vollstaendiger Gebetsablauf mit aufgeloesten Bewegungen.

        Die Sequenz verweist auf Bewegungen; hier werden sie eingesetzt, damit
        das Frontend nicht zwei Requests koppeln muss.
        """
        data = self._read(self.root / "prayer" / f"{prayer_id}.json")
        payload = self._deliver(
            data, madhhab=madhhab, language=language, context=f"prayer/{prayer_id}"
        )

        movements = self._movement_index(madhhab=madhhab, language=language)
        resolved: list[dict[str, Any]] = []
        for step in payload.get("sequence", []):
            movement = movements.get(step.get("movement_id"))
            if movement is None:
                # Bewegung wurde ausgefiltert (Rechtsschule oder Provenance).
                # Der Schritt entfaellt mit ihr — ein Schritt ohne Bewegung
                # waere fuer den Lernenden inhaltsleer.
                continue
            resolved.append({**step, "movement": movement})
        payload["sequence"] = resolved
        payload["_meta"]["resolved_steps"] = len(resolved)
        return payload

    def _movement_index(
        self, *, madhhab: str | None, language: str
    ) -> dict[str, dict[str, Any]]:
        data = self._read(self.root / "prayer" / "movements.json")
        prov_filter = ProvenanceFilter(madhhab=madhhab, language=language)
        result = prov_filter.filter_many(data.get("movements", []))
        return {m["id"]: m for m in result.data}

    def list_movements(
        self, *, madhhab: str | None = None, language: str = "de"
    ) -> list[dict[str, Any]]:
        return list(self._movement_index(madhhab=madhhab, language=language).values())

    # ------------------------------------------------------------------
    # Reinigung
    # ------------------------------------------------------------------

    def get_purification(
        self, kind: str, *, madhhab: str | None = None, language: str = "de"
    ) -> dict[str, Any]:
        allowed = {"wudu", "ghusl", "tayammum"}
        if kind not in allowed:
            raise KnowledgeNotFound(f"Unbekannte Reinigungsart '{kind}'. Erlaubt: {sorted(allowed)}")
        data = self._read(self.root / "purification" / f"{kind}.json")
        return self._deliver(
            data, madhhab=madhhab, language=language, context=f"purification/{kind}"
        )

    def list_purification(self, *, language: str = "de") -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for kind in ("wudu", "ghusl", "tayammum"):
            path = self.root / "purification" / f"{kind}.json"
            if not path.exists():
                continue
            data = self._read(path)
            if data.get("provenance") == "placeholder":
                continue
            name = data.get("name", {})
            out.append(
                {
                    "id": data["id"],
                    "name_arabic": name.get("arabic"),
                    "name_transliteration": name.get("transliteration"),
                    "name_local": (name.get("translations") or {}).get(language),
                    "step_count": len(data.get("steps", [])),
                    "provenance": data.get("provenance"),
                }
            )
        return out

    # ------------------------------------------------------------------
    # Arabisch
    # ------------------------------------------------------------------

    def get_alphabet(self, *, language: str = "de") -> dict[str, Any]:
        data = self._read(self.root / "arabic" / "alphabet.json")
        return self._deliver(data, madhhab=None, language=language, context="arabic/alphabet")

    def get_letter(self, letter_id: str, *, language: str = "de") -> dict[str, Any]:
        alphabet = self.get_alphabet(language=language)
        for letter in alphabet.get("letters", []):
            if letter.get("id") == letter_id:
                return letter
        raise KnowledgeNotFound(f"Buchstabe '{letter_id}' existiert nicht.")

    def get_curriculum(self, *, language: str = "de") -> list[dict[str, Any]]:
        return self.get_alphabet(language=language).get("curriculum", [])

    # ------------------------------------------------------------------
    # Koran
    # ------------------------------------------------------------------

    def list_surahs(self, *, language: str = "de") -> list[dict[str, Any]]:
        out: list[dict[str, Any]] = []
        for path in sorted((self.root / "quran").glob("surah_*.json")):
            data = self._read(path)
            if data.get("provenance") == "placeholder":
                continue
            name = data.get("name", {})
            out.append(
                {
                    "id": data["id"],
                    "number": data.get("number"),
                    "name_arabic": name.get("arabic"),
                    "name_transliteration": name.get("transliteration"),
                    "name_local": (name.get("translations") or {}).get(language),
                    "ayah_count": data.get("ayah_count"),
                    "provenance": data.get("provenance"),
                    "audio_available": bool((data.get("audio") or {}).get("available")),
                }
            )
        return sorted(out, key=lambda s: s.get("number") or 999)

    def get_surah(self, number: int, *, language: str = "de") -> dict[str, Any]:
        data = self._read(self.root / "quran" / f"surah_{number:03d}.json")
        return self._deliver(data, madhhab=None, language=language, context=f"quran/{number}")

    # ------------------------------------------------------------------
    # Transparenz
    # ------------------------------------------------------------------

    def get_sources(self) -> dict[str, Any]:
        """Oeffentliches Quellenregister.

        Content Policy 10.2: die Quellenauswahl ist eine menschliche Entscheidung
        mit Perspektive. Sie transparent zu machen ist Teil der Ehrlichkeit des
        Systems, nicht ein Zusatzfeature.
        """
        data = self._read(self.root / "sources" / "registry.json")
        sources = []
        for source in data.get("sources", []):
            sources.append(
                {
                    key: value
                    for key, value in source.items()
                    if key not in ("checksum", "raw_path")
                }
            )
        return {
            "version": data.get("version"),
            "updated": data.get("updated"),
            "sources": sources,
            "planned_sources": data.get("planned_sources", []),
            "rules": data.get("rules", []),
        }

    def content_status(self) -> dict[str, Any]:
        """Ehrlicher Statusbericht: was ist geprueft, was nicht.

        Wird im Frontend angezeigt. Ein System, das seinen eigenen Reifegrad
        verschweigt, taeuscht — auch ohne falsche Einzelaussage.
        """
        counts: dict[str, int] = {"verified": 0, "scholar_review_pending": 0, "disputed": 0, "placeholder": 0}
        modules: dict[str, dict[str, int]] = {}

        for path in sorted(self.root.rglob("*.json")):
            if "schema" in path.parts or path.name == "registry.json":
                continue
            module = path.parent.name
            data = self._read(path)
            module_counts = modules.setdefault(module, dict.fromkeys(counts, 0))

            def scan(node: Any, bucket: dict[str, int]) -> None:
                if isinstance(node, dict):
                    provenance = node.get("provenance")
                    if provenance in counts:
                        counts[provenance] += 1
                        bucket[provenance] += 1
                    for value in node.values():
                        scan(value, bucket)
                elif isinstance(node, list):
                    for value in node:
                        scan(value, bucket)

            scan(data, module_counts)

        total = sum(counts.values()) or 1
        return {
            "totals": counts,
            "by_module": modules,
            "verified_share": round(counts["verified"] / total, 3),
            "review_pending_share": round(counts["scholar_review_pending"] / total, 3),
            "note": (
                "Inhalte mit dem Status 'scholar_review_pending' sind noch nicht von einer "
                "fachlich qualifizierten Person geprüft. Sie werden mit sichtbarem Hinweis "
                "ausgeliefert. Inhalte mit 'placeholder' erreichen keinen Nutzer."
            ),
        }
