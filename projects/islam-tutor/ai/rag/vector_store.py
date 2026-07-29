"""Speicher- und Suchschicht fuer Chunks.

Entwurfsentscheidung — lexikalischer Index als Startpunkt, nicht als Notloesung:
Die Architektur nennt einen Vector Store. Dieses Modul liefert das Interface und
eine BM25-basierte Implementierung, die ohne Embedding-Anbieter funktioniert.

Warum nicht direkt semantisch:
  1. Die Wissensbasis ist klein (dreistellige Chunk-Zahl). BM25 arbeitet auf dieser
     Groesse gut und braucht keine Infrastruktur.
  2. Die Anfragen enthalten haeufig Fachtermini — 'Ruku', 'Wudu', 'Tashahhud',
     'Fatha'. Bei Termini schlaegt exakte Wortuebereinstimmung semantische
     Aehnlichkeit oft, weil das Wort selbst der Suchschluessel ist.
  3. Das System laeuft und ist testbar, bevor ein API-Key existiert. Ein Guard,
     den man erst nach Anbieterbindung testen kann, ist ein schlechter Guard.

Semantische Suche ist ein Upgrade fuer Umschreibungen ('wie halte ich die Haende
beim Stehen'). `HybridStore` kombiniert beide, sobald ein Embedder vorliegt.
"""
from __future__ import annotations

import math
import re
import unicodedata
from abc import ABC, abstractmethod
from collections import Counter
from dataclasses import dataclass
from typing import Protocol

from ai.rag.chunker import Chunk

# --------------------------------------------------------------------------
# Tokenisierung
# --------------------------------------------------------------------------
# Arabische Diakritika werden entfernt, damit 'رَبِّ' und 'ربّ' dasselbe Token
# ergeben. Ohne das findet eine Suche mit unvokalisiertem Text nichts im
# vokalisierten Korantext.

_ARABIC_DIACRITICS = re.compile(r"[ً-ٰٟۖ-ۭـ]")


def normalise(text: str) -> str:
    lowered = unicodedata.normalize("NFKD", (text or "").lower())
    without_marks = "".join(ch for ch in lowered if not unicodedata.combining(ch))
    without_arabic_marks = _ARABIC_DIACRITICS.sub("", without_marks)
    return re.sub(r"[^\w\s؀-ۿ]", " ", without_arabic_marks, flags=re.UNICODE)


# Funktionswoerter werden verworfen. Ohne diesen Schritt dominieren 'was', 'ist',
# 'wie' das Ranking: bei rund hundert Chunks ist ihre IDF noch positiv, und sie
# kommen in fast jeder Anfrage vor. Eine Frage nach 'Was ist Ruku?' fand dadurch
# Chunks mit vielen 'ist' statt den Chunk ueber Ruku.
_STOPWORDS: frozenset[str] = frozenset(
    """
    der die das den dem des ein eine einen einem eines und oder aber wenn dann
    als wie was wer wo wann warum wieso welche welcher welches so noch nur auch
    schon sein ist sind war waren wird werden wurde hat haben hatte kann koennen
    können muss muessen müssen soll sollen darf duerfen dürfen wuerde würde
    ich du er sie es wir ihr man sich mich dich uns euch mir dir ihm ihn ihnen
    mein meine meinem meinen dein deine seine
    in im an am auf aus bei beim mit nach von vom vor zu zum zur ueber über
    unter durch fuer für gegen ohne um bis seit waehrend während ins ans
    nicht kein keine sehr mehr viel
    wenig alle jede jeder jedes dieser diese dieses hier dort da doch mal etwa
    dabei damit dass weil denn also dadurch deshalb daher zwar jedoch sondern
    the a an and or but if then as like so how what who where when why which
    is are were will would has have had can could must should may might
    you he she it we they me him her them us my your his its
    on at from with by for to of about under through without around until
    since during not no very more much few all every this that these those
    """.split()
)


def tokenize(text: str) -> list[str]:
    """Zerlegt Text in Suchtoken. Funktionswoerter werden verworfen."""
    return [t for t in normalise(text).split() if len(t) > 1 and t not in _STOPWORDS]


# --------------------------------------------------------------------------
# Ergebnistypen
# --------------------------------------------------------------------------

@dataclass
class SearchHit:
    chunk: Chunk
    score: float
    matched_terms: tuple[str, ...] = ()

    def __repr__(self) -> str:  # pragma: no cover - Diagnose
        return f"SearchHit({self.chunk.chunk_id}, {self.score:.3f})"


class Embedder(Protocol):
    """Minimales Interface fuer einen Embedding-Anbieter.

    Bewusst als Protocol: kein Anbieter-SDK wird importiert, solange keiner
    angebunden ist. Eine Implementierung muss nur diese Methode erfuellen.
    """

    def embed(self, texts: list[str]) -> list[list[float]]: ...


# --------------------------------------------------------------------------
# Interface
# --------------------------------------------------------------------------

class ChunkStore(ABC):
    """Interface fuer alle Suchimplementierungen."""

    @abstractmethod
    def index(self, chunks: list[Chunk]) -> None:
        """Baut den Index auf. Ersetzt einen bestehenden Index vollstaendig."""

    @abstractmethod
    def search(
        self,
        query: str,
        *,
        limit: int = 8,
        modules: tuple[str, ...] | None = None,
        madhhab: str | None = None,
    ) -> list[SearchHit]:
        """Sucht Chunks zu einer Anfrage.

        Args:
            query: Anfragetext.
            limit: Maximale Trefferzahl.
            modules: Optionale Einschraenkung auf Module.
            madhhab: Optionale Rechtsschule. Bei Angabe werden nur Chunks mit
                madhhab in {'common', madhhab} geliefert — Content Policy 5.
        """

    @property
    @abstractmethod
    def size(self) -> int: ...


# --------------------------------------------------------------------------
# BM25
# --------------------------------------------------------------------------

class LexicalStore(ChunkStore):
    """BM25-Ranking ueber die Chunk-Texte.

    BM25 statt reinem TF-IDF, weil es Dokumentlaenge normalisiert. Ohne das
    gewinnen lange Uebersichts-Chunks systematisch gegen praezise Schritt-Chunks,
    obwohl der Schritt-Chunk die bessere Antwort ist.
    """

    K1 = 1.5
    B = 0.75

    TITLE_WEIGHT = 3
    """Gewicht von Titel- und ID-Treffern gegenueber Volltext-Treffern.

    Feldgewichtung nach dem BM25F-Prinzip. Ohne sie verdraengen lange
    Uebersichts-Chunks den praeziseren Treffer: eine Suche nach 'Wudu Schritte'
    fand die Tayammum-Uebersicht vor der Wudu-Uebersicht, weil dort 'wudu'
    im Volltext vorkommt und der Chunk kuerzer ist. Ein Treffer im Titel oder
    in der record_id ist ein deutlich staerkeres Relevanzsignal als einer im
    Fliesstext, und die Gewichtung macht das explizit.
    """

    def __init__(self) -> None:
        self._chunks: list[Chunk] = []
        self._term_freqs: list[Counter[str]] = []
        self._doc_lengths: list[int] = []
        self._doc_freq: Counter[str] = Counter()
        self._avg_length: float = 0.0

    # ----------------------------------------------------------------------

    def index(self, chunks: list[Chunk]) -> None:
        self._chunks = list(chunks)
        self._term_freqs = []
        self._doc_lengths = []
        self._doc_freq = Counter()

        for chunk in self._chunks:
            body_tokens = tokenize(chunk.text)
            # record_id mitindexieren, damit 'fajr' oder 'wudu' als Anfrage den
            # zugehoerigen Datensatz trifft, auch wenn der Titel uebersetzt ist.
            title_tokens = tokenize(f"{chunk.title} {chunk.record_id.replace('_', ' ')}")

            freqs = Counter(body_tokens)
            for token in title_tokens:
                freqs[token] += self.TITLE_WEIGHT

            self._term_freqs.append(freqs)
            # Laenge ohne Titelgewichtung: die Gewichtung soll den Score heben,
            # nicht den Chunk als kuenstlich lang erscheinen lassen.
            self._doc_lengths.append(len(body_tokens) + len(title_tokens))
            self._doc_freq.update(freqs.keys())

        total = sum(self._doc_lengths)
        self._avg_length = (total / len(self._doc_lengths)) if self._doc_lengths else 0.0

    @property
    def size(self) -> int:
        return len(self._chunks)

    # ----------------------------------------------------------------------

    def _idf(self, term: str) -> float:
        n = len(self._chunks)
        df = self._doc_freq.get(term, 0)
        if df == 0:
            return 0.0
        # BM25-IDF mit +1 zur Vermeidung negativer Werte bei haeufigen Termen
        return math.log(1 + (n - df + 0.5) / (df + 0.5))

    def search(
        self,
        query: str,
        *,
        limit: int = 8,
        modules: tuple[str, ...] | None = None,
        madhhab: str | None = None,
    ) -> list[SearchHit]:
        query_terms = tokenize(query)
        if not query_terms or not self._chunks:
            return []

        hits: list[SearchHit] = []

        for position, chunk in enumerate(self._chunks):
            if modules and chunk.module not in modules:
                continue
            if madhhab and chunk.madhhab not in ("common", madhhab):
                continue

            freqs = self._term_freqs[position]
            length = self._doc_lengths[position] or 1
            score = 0.0
            matched: list[str] = []

            for term in query_terms:
                tf = freqs.get(term, 0)
                if tf == 0:
                    continue
                matched.append(term)
                idf = self._idf(term)
                numerator = tf * (self.K1 + 1)
                denominator = tf + self.K1 * (1 - self.B + self.B * length / (self._avg_length or 1))
                score += idf * numerator / denominator

            if score > 0:
                hits.append(SearchHit(chunk=chunk, score=score, matched_terms=tuple(dict.fromkeys(matched))))

        hits.sort(key=lambda h: (-h.score, h.chunk.chunk_id))
        return hits[:limit]


# --------------------------------------------------------------------------
# Hybrid
# --------------------------------------------------------------------------

class HybridStore(ChunkStore):
    """Kombiniert BM25 mit semantischer Aehnlichkeit, sobald ein Embedder vorliegt.

    Ohne Embedder verhaelt sich diese Klasse identisch zu LexicalStore. Das ist
    beabsichtigt: der Aufrufer muss nicht wissen, ob ein Anbieter angebunden ist.
    Die Fusion nutzt Reciprocal Rank Fusion, weil BM25-Scores und
    Kosinus-Aehnlichkeiten nicht auf derselben Skala liegen und eine
    Score-Addition sie falsch gewichten wuerde.
    """

    RRF_K = 60

    def __init__(self, embedder: Embedder | None = None, *, lexical_weight: float = 1.0,
                 semantic_weight: float = 1.0) -> None:
        self._lexical = LexicalStore()
        self._embedder = embedder
        self._vectors: list[list[float]] = []
        self._chunks: list[Chunk] = []
        self._lexical_weight = lexical_weight
        self._semantic_weight = semantic_weight

    @property
    def size(self) -> int:
        return len(self._chunks)

    @property
    def has_semantic(self) -> bool:
        return self._embedder is not None and bool(self._vectors)

    def index(self, chunks: list[Chunk]) -> None:
        self._chunks = list(chunks)
        self._lexical.index(self._chunks)
        self._vectors = []
        if self._embedder is not None and self._chunks:
            self._vectors = self._embedder.embed([f"{c.title} {c.text}" for c in self._chunks])

    def search(
        self,
        query: str,
        *,
        limit: int = 8,
        modules: tuple[str, ...] | None = None,
        madhhab: str | None = None,
    ) -> list[SearchHit]:
        lexical_hits = self._lexical.search(
            query, limit=limit * 3, modules=modules, madhhab=madhhab
        )
        if not self.has_semantic:
            return lexical_hits[:limit]

        semantic_hits = self._semantic_search(query, limit=limit * 3, modules=modules, madhhab=madhhab)
        return self._fuse(lexical_hits, semantic_hits, limit)

    # ----------------------------------------------------------------------

    def _semantic_search(
        self,
        query: str,
        *,
        limit: int,
        modules: tuple[str, ...] | None,
        madhhab: str | None,
    ) -> list[SearchHit]:
        assert self._embedder is not None
        query_vector = self._embedder.embed([query])[0]
        scored: list[SearchHit] = []
        for position, chunk in enumerate(self._chunks):
            if modules and chunk.module not in modules:
                continue
            if madhhab and chunk.madhhab not in ("common", madhhab):
                continue
            similarity = _cosine(query_vector, self._vectors[position])
            if similarity > 0:
                scored.append(SearchHit(chunk=chunk, score=similarity))
        scored.sort(key=lambda h: (-h.score, h.chunk.chunk_id))
        return scored[:limit]

    def _fuse(
        self, lexical: list[SearchHit], semantic: list[SearchHit], limit: int
    ) -> list[SearchHit]:
        combined: dict[str, tuple[float, SearchHit]] = {}

        for rank, hit in enumerate(lexical, start=1):
            contribution = self._lexical_weight / (self.RRF_K + rank)
            combined[hit.chunk.chunk_id] = (contribution, hit)

        for rank, hit in enumerate(semantic, start=1):
            contribution = self._semantic_weight / (self.RRF_K + rank)
            existing = combined.get(hit.chunk.chunk_id)
            if existing:
                combined[hit.chunk.chunk_id] = (existing[0] + contribution, existing[1])
            else:
                combined[hit.chunk.chunk_id] = (contribution, hit)

        fused = [
            SearchHit(chunk=hit.chunk, score=score, matched_terms=hit.matched_terms)
            for score, hit in combined.values()
        ]
        fused.sort(key=lambda h: (-h.score, h.chunk.chunk_id))
        return fused[:limit]


def _cosine(a: list[float], b: list[float]) -> float:
    if not a or not b or len(a) != len(b):
        return 0.0
    dot = sum(x * y for x, y in zip(a, b, strict=True))
    norm_a = math.sqrt(sum(x * x for x in a))
    norm_b = math.sqrt(sum(y * y for y in b))
    if norm_a == 0 or norm_b == 0:
        return 0.0
    return dot / (norm_a * norm_b)
