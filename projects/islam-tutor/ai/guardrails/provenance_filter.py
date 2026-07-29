"""Provenance-Filter — die harte Grenze der Wissensauslieferung.

Content Policy 4.1: `placeholder`-Inhalte erreichen nie einen Nutzer.

Dieser Filter sitzt im Service-Layer, nicht in der Route. Jeder Pfad, der
Wissensdaten nach aussen gibt, laeuft durch `filter_record`. Damit ist die
Invariante an einer Stelle durchgesetzt statt an jedem Endpoint erneut.

Warum rekursiv: `placeholder` kann auf jeder Ebene stehen. Ein Gebet insgesamt
kann geprueft sein, waehrend ein einzelner Schritt darin noch leer ist. Ein
Filter, der nur die Wurzel prueft, wuerde diesen Schritt ausliefern.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

DELIVERABLE_PROVENANCE: frozenset[str] = frozenset(
    {"verified", "scholar_review_pending", "disputed"}
)
BLOCKED_PROVENANCE: frozenset[str] = frozenset({"placeholder"})

REVIEW_PENDING_NOTICE: dict[str, str] = {
    "de": (
        "Dieser Inhalt wurde noch nicht von einer fachlich qualifizierten Person "
        "geprüft. Er stammt aus einer redaktionellen Zusammenfassung breit "
        "dokumentierter Quellen."
    ),
    "en": (
        "This content has not yet been reviewed by a qualified person. It comes from "
        "an editorial summary of widely documented sources."
    ),
}

DISPUTED_NOTICE: dict[str, str] = {
    "de": (
        "Zu diesem Punkt bestehen unterschiedliche Positionen. Alle dokumentierten "
        "Positionen werden angezeigt; es wird keine ausgewählt."
    ),
    "en": (
        "There are differing positions on this point. All documented positions are "
        "shown; none is selected."
    ),
}


@dataclass
class FilterResult:
    """Ergebnis einer Filterung."""

    data: Any
    removed_count: int = 0
    removed_paths: list[str] = field(default_factory=list)
    review_pending_count: int = 0
    disputed_count: int = 0

    @property
    def has_review_pending(self) -> bool:
        return self.review_pending_count > 0

    @property
    def has_disputed(self) -> bool:
        return self.disputed_count > 0


class ProvenanceFilter:
    """Entfernt nicht auslieferbare Inhalte und sammelt Statusinformation.

    Der Filter mutiert die Eingabe nicht — er baut eine neue Struktur.
    (Verfassung 2.1 Prinzip 5: Immutability by default.)
    """

    def __init__(self, *, madhhab: str | None = None, language: str = "de") -> None:
        self.madhhab = madhhab
        self.language = language

    # ----------------------------------------------------------------------

    def filter_record(self, record: Any) -> FilterResult:
        """Filtert einen Datensatz rekursiv.

        Args:
            record: Beliebige verschachtelte JSON-artige Struktur.

        Returns:
            FilterResult mit der gefilterten Struktur und Statuszaehlern.
        """
        result = FilterResult(data=None)
        result.data = self._walk(record, path="$", result=result)
        return result

    def filter_many(self, records: list[Any]) -> FilterResult:
        """Filtert eine Liste von Datensaetzen und entfernt vollstaendig blockierte."""
        result = FilterResult(data=[])
        kept: list[Any] = []
        for index, record in enumerate(records):
            filtered = self._walk(record, path=f"$[{index}]", result=result)
            if filtered is not None:
                kept.append(filtered)
        result.data = kept
        return result

    # ----------------------------------------------------------------------

    def _walk(self, node: Any, path: str, result: FilterResult) -> Any:
        if isinstance(node, dict):
            return self._walk_dict(node, path, result)
        if isinstance(node, list):
            return self._walk_list(node, path, result)
        return node

    def _walk_dict(self, node: dict[str, Any], path: str, result: FilterResult) -> dict[str, Any] | None:
        provenance = node.get("provenance")

        if provenance in BLOCKED_PROVENANCE:
            result.removed_count += 1
            result.removed_paths.append(path)
            return None

        if provenance == "scholar_review_pending":
            result.review_pending_count += 1
        elif provenance == "disputed":
            result.disputed_count += 1

        if not self._madhhab_matches(node):
            result.removed_count += 1
            result.removed_paths.append(f"{path} (madhhab)")
            return None

        out: dict[str, Any] = {}
        for key, value in node.items():
            if key.startswith("$"):
                continue  # $comment und aehnliche Metafelder nicht ausliefern
            filtered = self._walk(value, f"{path}.{key}", result)
            if filtered is None and isinstance(value, dict):
                continue  # blockiertes Unter-dict weglassen
            out[key] = filtered

        if provenance == "scholar_review_pending":
            out["_notice"] = REVIEW_PENDING_NOTICE.get(self.language, REVIEW_PENDING_NOTICE["de"])
        elif provenance == "disputed":
            out["_notice"] = DISPUTED_NOTICE.get(self.language, DISPUTED_NOTICE["de"])

        return out

    def _walk_list(self, node: list[Any], path: str, result: FilterResult) -> list[Any]:
        out: list[Any] = []
        for index, value in enumerate(node):
            filtered = self._walk(value, f"{path}[{index}]", result)
            if filtered is None:
                continue
            out.append(filtered)
        return out

    def _madhhab_matches(self, node: dict[str, Any]) -> bool:
        """Prueft, ob ein Datensatz zur gewaehlten Rechtsschule passt.

        Ohne gewaehlte Rechtsschule wird nichts ausgefiltert — der Nutzer sieht
        dann alle Varianten. Mit Auswahl bleiben `common` und die eigene Schule.
        Content Policy 5.
        """
        if self.madhhab is None:
            return True
        node_madhhab = node.get("madhhab")
        if node_madhhab is None:
            return True
        return node_madhhab in ("common", self.madhhab)


def assert_deliverable(record: Any, *, context: str = "") -> None:
    """Wirft, wenn irgendwo im Baum ein blockierter Inhalt steht.

    Fuer Tests und als Sicherheitsnetz an Auslieferungsgrenzen. Ein
    durchgerutschter `placeholder` ist laut Verfassung 8.2 ein CRITICAL-Bug —
    also soll er laut scheitern, nicht still passieren.
    """
    offenders: list[str] = []

    def scan(node: Any, path: str) -> None:
        if isinstance(node, dict):
            if node.get("provenance") in BLOCKED_PROVENANCE:
                offenders.append(path)
            for key, value in node.items():
                scan(value, f"{path}.{key}")
        elif isinstance(node, list):
            for index, value in enumerate(node):
                scan(value, f"{path}[{index}]")

    scan(record, "$")
    if offenders:
        where = f" in {context}" if context else ""
        raise AssertionError(
            f"Nicht auslieferbarer Inhalt{where}: provenance=placeholder an {offenders}. "
            "Content Policy 4.1 verletzt."
        )
