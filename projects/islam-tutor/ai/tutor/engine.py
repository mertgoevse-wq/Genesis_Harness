"""Tutor-Engine — der fuenfstufige Antwortpfad.

Setzt docs/ARCHITECTURE.md Abschnitt 1 um:

    1 PRE-GUARD       Rechtsfrage? Urteilsanfrage? Belastung? → Umleitung
    2 RETRIEVAL       Suche, gefiltert auf Provenance und Rechtsschule
    3 GENERATION      Nur auf Basis der abgerufenen Passagen
    4 CITATION CHECK  Jede Aussage muss auf eine Passage zurueckfuehrbar sein
    5 POST-GUARD      Urteil? Unbelegtes Zitat? Autoritaetssimulation? → Abbruch

Keine Stufe darf uebersprungen werden. Der Pfad ist so gebaut, dass ein Fehler
in Stufe 3, 4 oder 5 zu einer ehrlichen Nichtantwort fuehrt, nicht zu einer
unkontrollierten Ausgabe.

Fallback-Kette bei Stufe 4: besteht die LLM-Antwort die Zitatpruefung nicht, wird
der extraktive Generator eingesetzt statt die Anfrage abzuweisen. Der extraktive
Weg ist per Konstruktion quellentreu, also besteht er die Pruefung immer.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

from ai.guardrails import policy
from ai.guardrails.citation_check import NO_INFORMATION_ANSWER, CitationChecker
from ai.llm.client import ExtractiveGenerator, Generator, default_generator
from ai.rag.retriever import Citation, Retriever, build_context


class Stage(str):
    PRE_GUARD = "pre_guard"
    RETRIEVAL = "retrieval"
    GENERATION = "generation"
    CITATION = "citation_check"
    POST_GUARD = "post_guard"
    DELIVERED = "delivered"


@dataclass
class TraceEntry:
    stage: str
    outcome: str
    detail: str = ""


@dataclass
class TutorAnswer:
    """Die Antwort des Tutors mit vollstaendiger Nachvollziehbarkeit."""

    text: str
    citations: list[Citation] = field(default_factory=list)
    category: str = policy.RequestCategory.LEARNING.value
    generator: str = "none"
    blocked: bool = False
    block_reason: str | None = None
    has_review_pending: bool = False
    has_disputed: bool = False
    madhhab: str | None = None
    trace: list[TraceEntry] = field(default_factory=list)
    timestamp: str = field(default_factory=lambda: datetime.now(timezone.utc).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return {
            "text": self.text,
            "citations": [
                {
                    "chunk_id": c.chunk_id,
                    "title": c.title,
                    "module": c.module,
                    "source_ids": c.source_ids,
                    "provenance": c.provenance,
                    "deep_link": c.deep_link,
                    "madhhab": c.madhhab,
                }
                for c in self.citations
            ],
            "category": self.category,
            "generator": self.generator,
            "blocked": self.blocked,
            "block_reason": self.block_reason,
            "notices": {
                "review_pending": self.has_review_pending,
                "disputed": self.has_disputed,
            },
            "madhhab": self.madhhab,
            "trace": [{"stage": t.stage, "outcome": t.outcome, "detail": t.detail} for t in self.trace],
            "timestamp": self.timestamp,
        }


class TutorEngine:
    """Orchestriert den Antwortpfad."""

    def __init__(
        self,
        *,
        retriever: Retriever | None = None,
        generator: Generator | None = None,
        knowledge_dir: Path | None = None,
        checker: CitationChecker | None = None,
    ) -> None:
        self.retriever = retriever or Retriever(knowledge_dir=knowledge_dir)
        self.generator = generator or default_generator()
        self.fallback_generator = ExtractiveGenerator()
        self.checker = checker or CitationChecker()

    # ----------------------------------------------------------------------

    def answer(
        self,
        message: str,
        *,
        madhhab: str | None = None,
        language: str = "de",
        limit: int = 6,
    ) -> TutorAnswer:
        trace: list[TraceEntry] = []

        # ---- Stufe 1: Vorpruefung -------------------------------------
        decision = policy.classify(message)
        if decision.is_blocked:
            trace.append(
                TraceEntry(
                    Stage.PRE_GUARD,
                    "blocked",
                    f"Kategorie {decision.category.value}; "
                    f"{len(decision.matched_patterns)} Muster getroffen",
                )
            )
            return TutorAnswer(
                text=policy.redirect_message(decision.redirect_message_key or "", language),
                category=decision.category.value,
                blocked=True,
                block_reason=decision.teaching_hint,
                madhhab=madhhab,
                trace=trace,
            )
        trace.append(TraceEntry(Stage.PRE_GUARD, "pass", "Lernfrage"))

        # ---- Stufe 2: Retrieval ---------------------------------------
        result = self.retriever.retrieve(message, limit=limit, madhhab=madhhab)
        if result.is_empty:
            trace.append(TraceEntry(Stage.RETRIEVAL, "empty", "Keine Treffer in der Wissensbasis"))
            return TutorAnswer(
                text=NO_INFORMATION_ANSWER.get(language, NO_INFORMATION_ANSWER["de"]),
                category=decision.category.value,
                generator="none",
                madhhab=madhhab,
                trace=trace,
            )
        trace.append(
            TraceEntry(
                Stage.RETRIEVAL,
                "pass",
                f"{len(result.hits)} Passagen; Module {result.detected_modules or ('alle',)}",
            )
        )

        context = build_context(result)

        # ---- Stufe 3: Generierung -------------------------------------
        generation = self.generator.generate(context, language=language)
        if not generation.succeeded:
            trace.append(
                TraceEntry(
                    Stage.GENERATION,
                    "fallback",
                    f"{self.generator.name} fehlgeschlagen: {generation.error}",
                )
            )
            generation = self.fallback_generator.generate(context, language=language)
        else:
            trace.append(
                TraceEntry(
                    Stage.GENERATION,
                    "pass",
                    f"{generation.generator}; {generation.tokens_out} Ausgabe-Token",
                )
            )

        if not generation.succeeded:
            trace.append(TraceEntry(Stage.GENERATION, "failed", generation.error or "unbekannt"))
            return TutorAnswer(
                text=NO_INFORMATION_ANSWER.get(language, NO_INFORMATION_ANSWER["de"]),
                category=decision.category.value,
                generator="none",
                madhhab=madhhab,
                trace=trace,
            )

        # ---- Stufe 4: Zitatpruefung -----------------------------------
        citation_result = self.checker.check(
            generation.text,
            context.passages,
            result.source_ids,
            verbatim=generation.verbatim,
        )
        if not citation_result.passed:
            trace.append(
                TraceEntry(
                    Stage.CITATION,
                    "failed",
                    f"{citation_result.reason} (Deckung {citation_result.coverage_ratio:.0%})",
                )
            )
            # Nicht abweisen, sondern auf den quellentreuen Weg wechseln.
            generation = self.fallback_generator.generate(context, language=language)
            citation_result = self.checker.check(
                generation.text,
                context.passages,
                result.source_ids,
                verbatim=generation.verbatim,
            )
            trace.append(
                TraceEntry(
                    Stage.CITATION,
                    "retry_pass" if citation_result.passed else "retry_failed",
                    f"Extraktiver Generator; Deckung {citation_result.coverage_ratio:.0%}",
                )
            )
            if not citation_result.passed:
                return TutorAnswer(
                    text=NO_INFORMATION_ANSWER.get(language, NO_INFORMATION_ANSWER["de"]),
                    category=decision.category.value,
                    generator="none",
                    blocked=True,
                    block_reason="Zitatpflicht nicht erfüllbar.",
                    madhhab=madhhab,
                    trace=trace,
                )
        else:
            trace.append(
                TraceEntry(
                    Stage.CITATION,
                    "pass",
                    f"{citation_result.checked_claims} Aussagen geprüft, alle gedeckt",
                )
            )

        # ---- Stufe 5: Nachpruefung ------------------------------------
        output_check = policy.check_output(generation.text)
        if not output_check.passed:
            rules = ", ".join(v.rule for v in output_check.violations)
            trace.append(TraceEntry(Stage.POST_GUARD, "blocked", f"Regeln verletzt: {rules}"))
            return TutorAnswer(
                text=policy.redirect_message("ruling_request", language),
                category=policy.RequestCategory.RULING_REQUEST.value,
                generator=generation.generator,
                blocked=True,
                block_reason=f"Ausgabe verletzt Policy: {rules}",
                madhhab=madhhab,
                trace=trace,
            )
        trace.append(TraceEntry(Stage.POST_GUARD, "pass", "Keine Verstöße"))
        trace.append(TraceEntry(Stage.DELIVERED, "ok", f"{len(context.citations)} Quellenangaben"))

        cited = _select_citations(context.citations, generation.cited_indices)
        return TutorAnswer(
            text=generation.text,
            citations=cited,
            category=decision.category.value,
            generator=generation.generator,
            has_review_pending=context.has_review_pending,
            has_disputed=context.has_disputed,
            madhhab=madhhab,
            trace=trace,
        )

    # ----------------------------------------------------------------------

    def warmup(self) -> int:
        """Baut den Index vorab. Gibt die Chunk-Zahl zurueck."""
        return self.retriever.chunk_count


def _select_citations(citations: list[Citation], indices: list[int]) -> list[Citation]:
    """Gibt die tatsaechlich verwendeten Quellen zurueck, sonst alle.

    Wenn der Generator keine [n]-Verweise gesetzt hat, werden alle Passagen als
    Quelle gefuehrt. Das ist die konservative Variante: zu viele Quellenangaben
    sind ein Transparenzgewinn, zu wenige eine Policy-Verletzung.
    """
    if not indices:
        return citations
    picked = [citations[i - 1] for i in indices if 1 <= i <= len(citations)]
    return picked or citations
