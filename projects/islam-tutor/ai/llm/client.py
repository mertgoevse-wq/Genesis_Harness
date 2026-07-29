"""Generator-Abstraktion mit einem Fallback, der ohne LLM funktioniert.

Entwurfsentscheidung — extraktiver Generator als Standard:
Die naheliegende Variante waere, hier ein Anbieter-SDK zu importieren und ohne
API-Key eine Exception zu werfen. Das haette zur Folge, dass die Guardrails, die
Retrieval-Qualitaet und der gesamte Antwortpfad erst nach Anbieterbindung
testbar sind — bei einem System, dessen wichtigste Eigenschaft die Zitattreue
ist, ist das die falsche Reihenfolge.

Deshalb gibt es zwei Generatoren:

  ExtractiveGenerator   Baut die Antwort ausschliesslich aus den abgerufenen
                        Passagen zusammen. Formuliert nichts hinzu. Erfindet
                        per Konstruktion nichts, weil er nichts generiert.
                        Standard und Fallback.

  AnthropicGenerator    Nutzt ein LLM fuer fliessende Erklaerungen, sieht dabei
                        aber ausschliesslich den Retrieval-Kontext. Laeuft danach
                        durch dieselbe Zitatpruefung wie der extraktive Weg.

Der extraktive Generator ist kein Platzhalter. Er ist die Untergrenze der
Qualitaet: weniger fliessend, aber garantiert quellentreu. Wenn das LLM
ausfaellt oder seine Antwort die Zitatpruefung nicht besteht, faellt das System
hierher zurueck statt zu scheitern.
"""
from __future__ import annotations

import os
from abc import ABC, abstractmethod
from dataclasses import dataclass, field

from ai.rag.retriever import GenerationContext


@dataclass
class GenerationResult:
    text: str
    generator: str
    cited_indices: list[int] = field(default_factory=list)
    tokens_in: int = 0
    tokens_out: int = 0
    error: str | None = None
    verbatim: bool = False
    """Der Generator gibt nach eigener Angabe nur wortgleiche Passagen aus.

    Wird an die Zitatpruefung durchgereicht und waehlt dort das strengere
    Verfahren: wortgleiches Enthaltensein statt Anspruchsdeckung. Ein Generator,
    der das faelschlich setzt, faellt durch — die Zusage wird geprueft, nicht
    geglaubt.
    """

    @property
    def succeeded(self) -> bool:
        return self.error is None and bool(self.text.strip())


class Generator(ABC):
    """Interface fuer alle Antwortgeneratoren."""

    name: str = "abstract"

    @abstractmethod
    def generate(self, context: GenerationContext, *, language: str = "de") -> GenerationResult:
        """Erzeugt eine Antwort ausschliesslich aus dem uebergebenen Kontext."""

    @property
    def available(self) -> bool:
        return True


# --------------------------------------------------------------------------
# Extraktiv
# --------------------------------------------------------------------------

_INTRO: dict[str, str] = {
    "de": "Dazu habe ich folgende belegte Inhalte in meiner Wissensbasis:",
    "en": "Here is the sourced material I have on this:",
}

_MADHHAB_NOTE: dict[str, str] = {
    "de": (
        "Bei den mit unterschiedlichen Positionen markierten Punkten weichen die "
        "Rechtsschulen voneinander ab. Alle dokumentierten Positionen sind aufgeführt; "
        "es wird keine ausgewählt."
    ),
    "en": (
        "Where differing positions are marked, the schools of law diverge. All documented "
        "positions are listed; none is selected."
    ),
}

_REVIEW_NOTE: dict[str, str] = {
    "de": (
        "Hinweis: Teile dieser Inhalte sind noch nicht von einer fachlich qualifizierten "
        "Person geprüft. Der Status steht bei jeder Quelle."
    ),
    "en": (
        "Note: parts of this material have not yet been reviewed by a qualified person. "
        "The status is shown with each source."
    ),
}


class ExtractiveGenerator(Generator):
    """Setzt die Antwort aus den abgerufenen Passagen zusammen.

    Formuliert nichts um und fuegt nichts hinzu. Die Antwort ist dadurch
    trockener als eine LLM-Antwort, aber jede Aussage steht wortgleich im
    Kontext — die Zitatpruefung besteht sie immer.
    """

    name = "extractive"

    def __init__(self, *, max_passages: int = 4) -> None:
        self.max_passages = max_passages

    def generate(self, context: GenerationContext, *, language: str = "de") -> GenerationResult:
        if context.is_empty:
            return GenerationResult(text="", generator=self.name, error="Leerer Kontext.")

        lines: list[str] = [_INTRO.get(language, _INTRO["de"]), ""]
        cited: list[int] = []

        for index, (passage, citation) in enumerate(
            zip(context.passages, context.citations, strict=True), start=1
        ):
            if index > self.max_passages:
                break
            cited.append(index)
            # Ueberschrift und Passage als getrennte Absaetze. Die Zitatpruefung
            # arbeitet absatzweise; stehen beide in einem Block, ist der Block
            # nicht mehr wortgleich in einer Passage enthalten.
            lines.append(f"**{citation.title}**")
            lines.append("")
            lines.append(passage)
            lines.append("")

        if context.has_disputed:
            lines.append(_MADHHAB_NOTE.get(language, _MADHHAB_NOTE["de"]))
            lines.append("")
        if context.has_review_pending:
            lines.append(_REVIEW_NOTE.get(language, _REVIEW_NOTE["de"]))

        return GenerationResult(
            text="\n".join(lines).strip(),
            generator=self.name,
            cited_indices=cited,
            verbatim=True,
        )


# --------------------------------------------------------------------------
# LLM
# --------------------------------------------------------------------------

SYSTEM_PROMPT: str = """\
Du bist der Lern-Tutor von Islam Tutor AI. Du bist ein Lernwerkzeug, keine religiöse Autorität.

Verbindliche Regeln:

1. Antworte AUSSCHLIESSLICH auf Grundlage der numerierten Passagen im Kontext.
   Wenn eine Information nicht in den Passagen steht, sage, dass du sie nicht hast.
   Ergänze nichts aus eigenem Wissen — auch nicht, wenn du meinst, es zu wissen.

2. Verweise auf die Passagen, aus denen du schöpfst, im Format [1], [2].

3. Erteile keine religiösen Rechtsurteile. Beurteile nicht, ob eine konkrete
   Handlung einer Person gültig war. Verweise bei solchen Fragen auf einen Gelehrten.

4. Bewerte keine Rechtsschule als richtiger oder besser. Wo die Passagen
   unterschiedliche Positionen nennen, gib alle wieder.

5. Erfinde niemals arabischen Korantext oder Hadithe. Gib arabischen Text nur
   wortgleich aus den Passagen wieder. Nenne eine Übersetzung immer Übersetzung,
   nie "der Koran sagt".

6. Ton: ruhig, sachlich, geduldig. Kein Pathos, kein Missionieren, kein Druck.
   Beschäme niemanden für Nichtwissen oder Fehler.

7. Antworte in der Sprache der Frage. Behalte arabische Fachtermini bei und
   erkläre sie beim ersten Vorkommen.

Wenn der Kontext leer ist oder die Frage nicht abdeckt, sage das offen. Eine ehrliche
Wissenslücke ist eine gute Antwort; eine plausibel klingende Erfindung ist der
schwerste Fehler, den du machen kannst."""


class AnthropicGenerator(Generator):
    """LLM-Generator. Importiert das SDK erst bei Verfuegbarkeit.

    Der Import liegt absichtlich in der Methode, nicht am Modulanfang: das
    Gesamtsystem soll ohne installiertes SDK importierbar und testbar bleiben.
    """

    name = "anthropic"

    def __init__(
        self,
        *,
        model: str = "claude-sonnet-5",
        api_key: str | None = None,
        max_tokens: int = 1500,
    ) -> None:
        self.model = model
        self.max_tokens = max_tokens
        self._api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")

    @property
    def available(self) -> bool:
        if not self._api_key:
            return False
        try:
            import anthropic  # noqa: F401
        except ImportError:
            return False
        return True

    def generate(self, context: GenerationContext, *, language: str = "de") -> GenerationResult:
        if context.is_empty:
            return GenerationResult(text="", generator=self.name, error="Leerer Kontext.")
        if not self.available:
            return GenerationResult(
                text="",
                generator=self.name,
                error="Kein API-Key oder SDK nicht installiert.",
            )

        import anthropic

        madhhab_line = (
            f"Der Nutzer folgt der Rechtsschule: {context.madhhab}. "
            "Zeige primär diese Variante und weise darauf hin, dass andere existieren."
            if context.madhhab
            else "Der Nutzer hat keine Rechtsschule gewählt. Zeige die Unterschiede."
        )

        user_message = (
            f"Frage des Lernenden: {context.query}\n\n"
            f"{madhhab_line}\n\n"
            f"Verfügbare Passagen:\n\n{context.as_prompt_block()}\n\n"
            "Beantworte die Frage ausschließlich auf Grundlage dieser Passagen und "
            "verweise mit [n] auf die genutzten Passagen."
        )

        try:
            client = anthropic.Anthropic(api_key=self._api_key)
            response = client.messages.create(
                model=self.model,
                max_tokens=self.max_tokens,
                system=SYSTEM_PROMPT,
                messages=[{"role": "user", "content": user_message}],
            )
            text = "".join(block.text for block in response.content if block.type == "text")
            return GenerationResult(
                text=text,
                generator=self.name,
                cited_indices=_extract_citation_indices(text, len(context.passages)),
                tokens_in=response.usage.input_tokens,
                tokens_out=response.usage.output_tokens,
            )
        except Exception as exc:  # noqa: BLE001 - Anbieterfehler wird bewusst gefangen
            # Explizit statt still: der Aufrufer entscheidet über den Fallback.
            return GenerationResult(text="", generator=self.name, error=f"{type(exc).__name__}: {exc}")


def _extract_citation_indices(text: str, max_index: int) -> list[int]:
    """Liest [n]-Verweise aus der Antwort."""
    import re

    found = {int(m) for m in re.findall(r"\[(\d{1,2})\]", text or "")}
    return sorted(i for i in found if 1 <= i <= max_index)


# --------------------------------------------------------------------------
# Auswahl
# --------------------------------------------------------------------------

def default_generator() -> Generator:
    """Liefert den besten verfuegbaren Generator.

    Reihenfolge ist Absicht: LLM, wenn verfuegbar, sonst extraktiv. Es wird nie
    eine Exception geworfen, weil kein Anbieter konfiguriert ist — ein System,
    das ohne API-Key nicht startet, ist nicht testbar.
    """
    llm = AnthropicGenerator()
    if llm.available:
        return llm
    return ExtractiveGenerator()
