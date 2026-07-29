"""Zitatpflicht — jede inhaltliche Aussage braucht eine Quelle.

Content Policy 6.1: "Zitieren, nicht behaupten."

Dies ist die zweite Schranke neben policy.py. Wo der Muster-Guard eine
umformulierte Fatwa-Anfrage durchlassen kann, faengt diese Pruefung sie:
eine Antwort, deren Aussagen nicht auf abgerufene Passagen zurueckfuehrbar sind,
verlaesst das System nicht.

Ansatz: Anspruchsdeckung statt Wortpruefung.
Die Antwort wird in Aussagesaetze zerlegt. Fuer jeden Satz mit inhaltlicher
Substanz wird geprueft, ob genuegend Inhaltswoerter im Retrieval-Kontext
vorkommen. Das ist eine Naeherung, aber eine ehrliche: sie erkennt, wenn ein
Modell Inhalt hinzuerfindet, der nirgends im Kontext stand.

Was diese Pruefung NICHT kann: sie erkennt keine subtile Fehlinterpretation
korrekter Quellen. Dafuer braucht es menschliche Pruefung — deshalb bleiben
Fiqh-Inhalte auf `scholar_review_pending`.
"""
from __future__ import annotations

import re
import unicodedata
from dataclasses import dataclass, field

MIN_COVERAGE = 0.55
"""Anteil der Inhaltswoerter eines Satzes, der im Kontext vorkommen muss."""

MIN_CLAIM_WORDS = 4
"""Kuerzere Saetze gelten als Ueberleitung, nicht als inhaltliche Aussage."""

# Funktionswoerter tragen keine inhaltliche Last und werden nicht gezaehlt.
_STOPWORDS: frozenset[str] = frozenset(
    """
    der die das den dem des ein eine einen einem eines und oder aber wenn dann
    als wie so noch nur auch schon sein ist sind war waren wird werden wurde
    hat haben hatte kann koennen muss muessen soll sollen darf duerfen
    ich du er sie es wir ihr man sich mich dich uns euch mir dir ihm ihn ihnen
    in an auf aus bei mit nach von vor zu zum zur ueber unter durch fuer gegen
    ohne um bis seit waehrend nicht kein keine sehr mehr viel wenig alle jede
    jeder jedes dieser diese dieses hier dort da doch mal etwa dabei damit
    dass weil denn also dadurch deshalb daher zwar jedoch sondern
    the a an and or but if then as like so still only also already be is are
    was were will would has have had can could must should may might
    i you he she it we they me him her them us in on at from with by for
    to of about under through without around until since during not no
    very more much few all every this that these those here there
    """.split()
)


def _normalise(text: str) -> str:
    """Kleinschreibung, Diakritika entfernen, Interpunktion zu Leerzeichen."""
    decomposed = unicodedata.normalize("NFKD", text.lower())
    stripped = "".join(ch for ch in decomposed if not unicodedata.combining(ch))
    return re.sub(r"[^\w\s]", " ", stripped, flags=re.UNICODE)


def _content_words(text: str) -> list[str]:
    words = _normalise(text).split()
    return [w for w in words if len(w) > 2 and w not in _STOPWORDS]


def _split_sentences(text: str) -> list[str]:
    parts = re.split(r"(?<=[.!?])\s+|\n{2,}", text or "")
    return [p.strip() for p in parts if p.strip()]


@dataclass
class UncoveredClaim:
    sentence: str
    coverage: float
    unmatched_words: list[str]


@dataclass
class CitationResult:
    passed: bool
    reason: str = ""
    checked_claims: int = 0
    uncovered: list[UncoveredClaim] = field(default_factory=list)
    cited_source_ids: list[str] = field(default_factory=list)

    @property
    def coverage_ratio(self) -> float:
        if self.checked_claims == 0:
            return 1.0
        return (self.checked_claims - len(self.uncovered)) / self.checked_claims


class CitationChecker:
    """Prueft, ob eine Antwort durch ihren Retrieval-Kontext gedeckt ist."""

    def __init__(self, *, min_coverage: float = MIN_COVERAGE) -> None:
        self.min_coverage = min_coverage

    def check(
        self,
        answer: str,
        context_passages: list[str],
        cited_source_ids: list[str] | None = None,
        *,
        allow_no_information: bool = True,
        verbatim: bool = False,
    ) -> CitationResult:
        """Prueft eine generierte Antwort.

        Args:
            answer: Die generierte Antwort.
            context_passages: Die Passagen, die der Generator sehen durfte.
            cited_source_ids: Die source_ids, die die Antwort mitfuehrt.
            allow_no_information: Wenn True, gilt eine explizite
                "keine belegte Information"-Antwort ohne Quellen als bestanden.
            verbatim: Der Generator gibt nach eigener Angabe nur wortgleiche
                Passagen aus. Dann wird nicht Anspruchsdeckung geprueft, sondern
                wortgleiche Enthaltensein — eine strengere Pruefung, siehe
                `_check_verbatim`.

        Returns:
            CitationResult. Bei passed=False darf die Antwort nicht ausgeliefert werden.
        """
        cited = list(cited_source_ids or [])

        if not answer or not answer.strip():
            return CitationResult(passed=False, reason="Leere Antwort.", cited_source_ids=cited)

        if allow_no_information and self._is_no_information_answer(answer):
            return CitationResult(
                passed=True,
                reason="Explizite Wissenslueckenantwort — Zitatpflicht nicht anwendbar.",
                cited_source_ids=cited,
            )

        if not context_passages:
            return CitationResult(
                passed=False,
                reason=(
                    "Antwort ohne Retrieval-Kontext. Content Policy 6.2: es wird nicht aus "
                    "Modellwissen geantwortet, wenn das Retrieval leer war."
                ),
                cited_source_ids=cited,
            )

        if not cited:
            return CitationResult(
                passed=False,
                reason=(
                    "Antwort ohne Quellenangabe. Content Policy 6.1: jede Antwort nennt ihre "
                    "Quelle oder sagt, dass sie keine hat."
                ),
                cited_source_ids=cited,
            )

        if verbatim:
            return self._check_verbatim(answer, context_passages, cited)

        context_vocabulary = set()
        for passage in context_passages:
            context_vocabulary.update(_content_words(passage))

        uncovered: list[UncoveredClaim] = []
        checked = 0

        for sentence in _split_sentences(answer):
            words = _content_words(sentence)
            if len(words) < MIN_CLAIM_WORDS:
                continue
            checked += 1
            matched = [w for w in words if w in context_vocabulary]
            coverage = len(matched) / len(words)
            if coverage < self.min_coverage:
                uncovered.append(
                    UncoveredClaim(
                        sentence=sentence,
                        coverage=round(coverage, 3),
                        unmatched_words=[w for w in words if w not in context_vocabulary][:12],
                    )
                )

        if uncovered:
            return CitationResult(
                passed=False,
                reason=(
                    f"{len(uncovered)} von {checked} Aussagen sind nicht durch den "
                    "Retrieval-Kontext gedeckt. Content Policy 6.2: eine Wissenslücke wird "
                    "nicht mit plausibel klingendem Text gefüllt."
                ),
                checked_claims=checked,
                uncovered=uncovered,
                cited_source_ids=cited,
            )

        return CitationResult(
            passed=True,
            reason="Alle geprüften Aussagen sind durch den Kontext gedeckt.",
            checked_claims=checked,
            cited_source_ids=cited,
        )

    # ----------------------------------------------------------------------

    def _check_verbatim(
        self, answer: str, context_passages: list[str], cited: list[str]
    ) -> CitationResult:
        """Prueft wortgleiche Uebernahme statt Anspruchsdeckung.

        Warum eine eigene Pruefung: die Anspruchsdeckung ist das richtige
        Instrument fuer freie Generierung, aber das falsche fuer einen
        zitierenden Generator. Sie schlaegt dort auf dessen Rahmentext an
        ("Dazu habe ich folgende belegte Inhalte") und wuerde eine korrekte
        Antwort verwerfen — genau das ist bei der Entwicklung passiert.

        Diese Pruefung ist nicht schwaecher, sondern strenger: jeder
        inhaltstragende Absatz muss WORTGLEICH in einer Passage stehen. Ein
        Generator, der behauptet, nur zu zitieren, und dabei etwas hinzufuegt,
        faellt hier durch — waehrend er die Anspruchsdeckung bestehen koennte.

        Ausgenommen ist ausschliesslich der deklarierte Rahmentext des Systems.
        """
        normalised_context = [_normalise(p) for p in context_passages]
        uncovered: list[UncoveredClaim] = []
        checked = 0

        for block in re.split(r"\n{2,}", answer or ""):
            candidate = block.strip()
            # Fuehrende Ueberschriftszeilen abtrennen. Der Generator setzt sie
            # als eigenen Absatz, aber die Pruefung soll nicht von seiner
            # Zeilenumbruch-Konvention abhaengen.
            while candidate.startswith("**"):
                head, _, rest = candidate.partition("\n")
                if not head.strip().endswith("**"):
                    break
                candidate = rest.strip()

            if not candidate:
                continue
            if self._is_framing(candidate):
                continue
            if len(_content_words(candidate)) < MIN_CLAIM_WORDS:
                continue

            checked += 1
            needle = _normalise(candidate)
            if not any(needle in haystack for haystack in normalised_context):
                uncovered.append(
                    UncoveredClaim(
                        sentence=candidate[:200],
                        coverage=0.0,
                        unmatched_words=["nicht wortgleich im Kontext enthalten"],
                    )
                )

        if uncovered:
            return CitationResult(
                passed=False,
                reason=(
                    f"{len(uncovered)} von {checked} Absätzen stehen nicht wortgleich im "
                    "Kontext, obwohl der Generator wortgleiche Ausgabe deklariert hat."
                ),
                checked_claims=checked,
                uncovered=uncovered,
                cited_source_ids=cited,
            )

        return CitationResult(
            passed=True,
            reason=f"{checked} Absätze wortgleich im Kontext belegt.",
            checked_claims=checked,
            cited_source_ids=cited,
        )

    _FRAMING_MARKERS: tuple[str, ...] = (
        "folgende belegte inhalte",
        "here is the sourced material",
        "rechtsschulen voneinander ab",
        "schools of law diverge",
        "nicht von einer fachlich qualifizierten person",
        "not yet been reviewed by a qualified person",
    )

    def _is_framing(self, text: str) -> bool:
        """Erkennt den vom System selbst gesetzten Rahmentext.

        Diese Liste ist bewusst kurz und explizit. Sie enthaelt nur Texte, die
        aus ai/llm/client.py stammen — keine Heuristik, die versehentlich
        Inhaltsaussagen ausnehmen koennte.
        """
        lowered = _normalise(text)
        return any(marker in lowered for marker in self._FRAMING_MARKERS)

    _NO_INFO_MARKERS: tuple[str, ...] = (
        "keinen belegten inhalt",
        "keine belegte information",
        "keine belegten informationen",
        "nicht in meiner wissensbasis",
        "dazu habe ich keine quelle",
        "no sourced information",
        "not in my knowledge base",
        "i have no source for",
    )

    def _is_no_information_answer(self, answer: str) -> bool:
        lowered = _normalise(answer)
        return any(marker in lowered for marker in self._NO_INFO_MARKERS)


NO_INFORMATION_ANSWER: dict[str, str] = {
    "de": (
        "Zu dieser Frage habe ich keinen belegten Inhalt in meiner Wissensbasis. "
        "Ich könnte dir eine plausibel klingende Antwort formulieren, aber die wäre "
        "geraten — und bei religiösen Inhalten ist Raten der schlechtere Fehler als "
        "Zugeben.\n\n"
        "Was ich anbieten kann: eine verwandte Frage, zu der ich belegte Inhalte habe, "
        "oder den Hinweis, wo du verlässlich nachschlagen kannst."
    ),
    "en": (
        "I have no sourced information on this in my knowledge base. I could produce a "
        "plausible-sounding answer, but it would be guesswork — and with religious "
        "content, guessing is the worse error than admitting the gap.\n\n"
        "What I can offer: a related question I do have sourced material for, or a "
        "pointer to where you can look it up reliably."
    ),
}
