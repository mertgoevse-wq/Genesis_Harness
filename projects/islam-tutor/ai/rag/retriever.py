"""Retrieval und Kontextaufbau.

Zusammen bilden `Retriever` und `build_context` die Stationen 2 und 3 des
Antwortpfads aus docs/ARCHITECTURE.md. Wichtig ist die Reihenfolge:
Der Retriever filtert nach Provenance und Rechtsschule, BEVOR der Generator
etwas sieht. Ein Generator, der einen `placeholder`-Chunk im Kontext hat, kann
ihn nicht mehr ignorieren.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from ai.rag.chunker import Chunk, build_all_chunks
from ai.rag.vector_store import ChunkStore, Embedder, HybridStore, SearchHit

MODULE_KEYWORDS: dict[str, tuple[str, ...]] = {
    "prayer": (
        "gebet", "beten", "salah", "salat", "namaz", "rakah", "raka", "rakat", "ruku",
        "sujud", "sajda", "tashahhud", "takbir", "qiyam", "fajr", "dhuhr", "asr",
        "maghrib", "isha", "witr", "sunnah", "fard", "prayer", "bow", "prostrat",
    ),
    "purification": (
        "wudu", "abdest", "ghusl", "gusul", "tayammum", "teyemmum", "waschung",
        "reinigung", "reinheit", "waschen", "ablution", "purification", "taharah",
    ),
    "quran": (
        "koran", "quran", "qur'an", "sure", "surah", "vers", "ayah", "ayat",
        "fatiha", "rezitation", "rezitieren", "auswendig", "memorier",
    ),
    "arabic": (
        "arabisch", "arabic", "buchstabe", "buchstaben", "letter", "alphabet",
        "aussprache", "lesen", "schreiben", "tajwid", "fatha", "kasra", "damma",
        "sukun", "shadda", "vokal", "harakat",
    ),
}


@dataclass
class RetrievalResult:
    """Ergebnis eines Retrievals."""

    query: str
    hits: list[SearchHit] = field(default_factory=list)
    detected_modules: tuple[str, ...] = ()
    madhhab: str | None = None

    @property
    def is_empty(self) -> bool:
        return not self.hits

    @property
    def passages(self) -> list[str]:
        return [hit.chunk.text for hit in self.hits]

    @property
    def source_ids(self) -> list[str]:
        seen: dict[str, None] = {}
        for hit in self.hits:
            for source_id in hit.chunk.source_ids:
                seen.setdefault(source_id, None)
        return list(seen)

    @property
    def has_review_pending(self) -> bool:
        return any(h.chunk.provenance == "scholar_review_pending" for h in self.hits)

    @property
    def has_disputed(self) -> bool:
        return any(h.chunk.provenance == "disputed" for h in self.hits)


def detect_modules(query: str) -> tuple[str, ...]:
    """Erkennt anhand von Fachtermini, welche Module relevant sind.

    Zweck ist nicht Filterung um jeden Preis, sondern Praezision: eine Frage nach
    'Ruku' soll nicht von Arabisch-Chunks verdraengt werden. Wird kein Modul
    erkannt, wird ueber alle gesucht — lieber breiter als falsch eingeengt.
    """
    lowered = (query or "").lower()
    matched = tuple(
        module
        for module, keywords in MODULE_KEYWORDS.items()
        if any(keyword in lowered for keyword in keywords)
    )
    return matched


class Retriever:
    """Sucht relevante Passagen zu einer Anfrage."""

    def __init__(
        self,
        store: ChunkStore | None = None,
        *,
        knowledge_dir: Path | None = None,
        embedder: Embedder | None = None,
    ) -> None:
        self._store = store or HybridStore(embedder=embedder)
        self._chunks: list[Chunk] = []
        self._knowledge_dir = knowledge_dir
        self._indexed = False

    def ensure_indexed(self) -> None:
        if self._indexed:
            return
        self._chunks = build_all_chunks(self._knowledge_dir)
        self._store.index(self._chunks)
        self._indexed = True

    def reindex(self) -> int:
        """Baut den Index neu. Gibt die Chunk-Zahl zurueck."""
        self._indexed = False
        self.ensure_indexed()
        return self._store.size

    @property
    def chunk_count(self) -> int:
        self.ensure_indexed()
        return self._store.size

    def retrieve(
        self,
        query: str,
        *,
        limit: int = 6,
        madhhab: str | None = None,
        modules: tuple[str, ...] | None = None,
    ) -> RetrievalResult:
        self.ensure_indexed()

        detected = modules if modules is not None else detect_modules(query)
        hits = self._store.search(
            query, limit=limit, modules=detected or None, madhhab=madhhab
        )

        # Zweiter Versuch ohne Moduleinschraenkung: besser ein breiterer Treffer
        # als eine leere Antwort, die den Nutzer im Nichts stehen laesst.
        if not hits and detected:
            hits = self._store.search(query, limit=limit, modules=None, madhhab=madhhab)

        return RetrievalResult(
            query=query,
            hits=hits,
            detected_modules=detected,
            madhhab=madhhab,
        )

    def get_chunk(self, chunk_id: str) -> Chunk | None:
        self.ensure_indexed()
        for chunk in self._chunks:
            if chunk.chunk_id == chunk_id:
                return chunk
        return None


# --------------------------------------------------------------------------
# Kontextaufbau
# --------------------------------------------------------------------------

@dataclass
class Citation:
    """Eine Quellenangabe, wie sie der Nutzer sieht."""

    chunk_id: str
    title: str
    module: str
    source_ids: list[str]
    provenance: str
    deep_link: str | None = None
    madhhab: str = "common"


@dataclass
class GenerationContext:
    """Was der Generator sehen darf — und nur das."""

    query: str
    passages: list[str]
    citations: list[Citation]
    madhhab: str | None
    has_review_pending: bool
    has_disputed: bool

    @property
    def is_empty(self) -> bool:
        return not self.passages

    def as_prompt_block(self) -> str:
        """Formatiert die Passagen fuer den Generator.

        Jede Passage ist mit ihrer Nummer versehen, damit das Modell im Text
        darauf verweisen kann und die Zitatpruefung die Zuordnung nachvollzieht.
        """
        blocks = []
        for index, (passage, citation) in enumerate(zip(self.passages, self.citations, strict=True), start=1):
            blocks.append(
                f"[{index}] {citation.title} (Modul: {citation.module}, "
                f"Status: {citation.provenance}, Quellen: {', '.join(citation.source_ids) or 'keine'})\n"
                f"{passage}"
            )
        return "\n\n".join(blocks)


def build_context(result: RetrievalResult) -> GenerationContext:
    """Baut den Generierungskontext aus einem Retrieval-Ergebnis."""
    citations = [
        Citation(
            chunk_id=hit.chunk.chunk_id,
            title=hit.chunk.title or hit.chunk.chunk_id,
            module=hit.chunk.module,
            source_ids=list(hit.chunk.source_ids),
            provenance=hit.chunk.provenance,
            deep_link=hit.chunk.deep_link,
            madhhab=hit.chunk.madhhab,
        )
        for hit in result.hits
    ]
    return GenerationContext(
        query=result.query,
        passages=result.passages,
        citations=citations,
        madhhab=result.madhhab,
        has_review_pending=result.has_review_pending,
        has_disputed=result.has_disputed,
    )
