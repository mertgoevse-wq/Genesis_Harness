"""Klassifikation von Anfragen und Durchsetzung der Content Policy.

Dieses Modul setzt docs/CONTENT_POLICY.md Abschnitt 3 in Code um. Es ist bewusst
KEIN Prompt: ein Prompt kann durch Umformulierung umgangen werden, eine
Klassifikation mit anschliessendem Pfadwechsel nicht.

Entwurfsentscheidung — Muster statt LLM-Klassifikator:
Die Erkennung arbeitet mit Wortmustern, nicht mit einem Modellaufruf. Gruende:
  1. Deterministisch und testbar. Fuer jede Policy-Regel existiert ein Test, der
     immer dasselbe Ergebnis liefert.
  2. Kein Kaltstart-Risiko. Der Guard funktioniert, bevor irgendein LLM angebunden ist.
  3. Kein Kostenfaktor pro Anfrage.

Die Grenze dieses Ansatzes ist bekannt und dokumentiert: Muster erkennen nicht
jede Umschreibung. Deshalb ist der Muster-Guard nur die erste von zwei Schranken.
Die zweite ist die Zitatpflicht in citation_check.py: eine Antwort ohne Quelle
verlaesst das System nicht, unabhaengig davon, wie die Frage formuliert war.
"""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum


class RequestCategory(str, Enum):
    """Kategorie einer Nutzeranfrage."""

    LEARNING = "learning"
    """Lernfrage. Regulaerer Pfad."""

    RULING_REQUEST = "ruling_request"
    """Verlangt ein religioeses Rechtsurteil. Wird umgeleitet, nicht beantwortet."""

    PERSONAL_VALIDITY = "personal_validity"
    """Fragt nach der Gueltigkeit einer konkreten eigenen Handlung. Wird umgeleitet."""

    MADHHAB_RANKING = "madhhab_ranking"
    """Verlangt eine Bewertung, welche Rechtsschule richtig ist. Wird umgeleitet."""

    JUDGEMENT_OF_PERSON = "judgement_of_person"
    """Verlangt ein Urteil ueber den Glauben oder die Praxis einer Person. Wird abgelehnt."""

    DISTRESS = "distress"
    """Anzeichen von Belastung oder Zwangsschleife. Verlaesst den Lernkontext."""


@dataclass(frozen=True)
class GuardDecision:
    """Ergebnis der Vorpruefung."""

    category: RequestCategory
    allow_generation: bool
    matched_patterns: tuple[str, ...] = ()
    redirect_message_key: str | None = None
    teaching_hint: str | None = None

    @property
    def is_blocked(self) -> bool:
        return not self.allow_generation


# --------------------------------------------------------------------------
# Muster
# --------------------------------------------------------------------------
# Deutsch, Englisch und Tuerkisch, weil das die erwarteten Nutzersprachen sind.
# Muster sind absichtlich eng gefasst: ein falscher Treffer blockiert eine
# legitime Lernfrage, und das ist auch ein Schaden.

_RULING_PATTERNS: tuple[str, ...] = (
    # Determinierer zwischen Kopula und Praedikat sind optional und vielfaeltig:
    # 'ist erlaubt', 'ist es erlaubt', 'ist das haram', 'sind diese Dinge makruh'.
    # Eine erste Fassung verlangte 'ist [es]' und verfehlte 'Ist das haram?' —
    # der Test test_ruling_requests_are_blocked hat das aufgedeckt.
    r"\b(ist|sind|wäre|waere|wären|waeren)\s+((das|es|dies|dieses|dieser|diese|jenes|so\s+etwas)\s+)?"
    r"(erlaubt|verboten|halal|haram|makruh|zulässig|zulaessig|gestattet|untersagt)\b",
    r"\bdarf\s+ich\b",
    r"\bdürfen\s+wir\b",
    r"\bwäre\s+es\s+(erlaubt|verboten|haram|halal)\b",
    r"\b(is|are)\s+it\s+(allowed|permissible|forbidden|halal|haram)\b",
    r"\b(am|are)\s+i\s+allowed\b",
    r"\bcan\s+i\s+(eat|drink|wear|marry|do)\b",
    r"\b(caiz|helal|haram)\s+mı\b",
    r"\bfatwa\b",
    r"\bfetva\b",
    r"\brechtsgutachten\b",
    r"\bgib\s+mir\s+ein\s+urteil\b",
    r"\bwas\s+ist\s+das\s+urteil\s+(für|zu|über)\b",
    r"\bwhat\s+is\s+the\s+ruling\s+(on|for)\b",
)

_PERSONAL_VALIDITY_PATTERNS: tuple[str, ...] = (
    r"\b(ist|war)\s+mein\w*\s+\w{0,12}\s*(gebet|wudu|ghusl|fasten|salah|gültig|ungültig)\b",
    r"\b(gebet|wudu|ghusl|fasten)\s+gültig\b",
    r"\bmuss\s+ich\s+(das\s+)?(gebet|wudu|ghusl)\s+wiederholen\b",
    r"\bzählt\s+mein\w*\s+(gebet|fasten|wudu)\b",
    r"\bwas\s+mein\s+(prayer|wudu|ghusl|fast)\s+valid\b",
    r"\bis\s+my\s+(prayer|wudu|ghusl|fast)\s+valid\b",
    r"\bdo\s+i\s+(have\s+to|need\s+to)\s+repeat\s+(my\s+)?(prayer|wudu|ghusl)\b",
    r"\bhabe\s+ich\s+(mein\w*\s+)?(gebet|wudu)\s+richtig\b",
)

_MADHHAB_RANKING_PATTERNS: tuple[str, ...] = (
    # Artikel im Deutschen richtet sich nach dem Genus: 'welche Rechtsschule ist
    # die richtige', 'welcher Madhhab ist der beste'. Eine erste Fassung kannte
    # nur 'die' und verfehlte die maskuline Variante — aufgedeckt durch
    # test_madhhab_ranking_is_blocked.
    r"\bwelche\w*\s+(madhhab|madhab|rechtsschule|mezhep)\s+ist\s+((der|die|das)\s+)?"
    r"(richtig|best|korrekt|wahr|stärkst|staerkst|authentischst)\w*",
    r"\bwhich\s+(madhhab|school\s+of\s+(law|thought))\s+is\s+(the\s+)?(right|correct|best|true|strongest)",
    r"\bhangi\s+mezhep\s+(doğru|en\s+iyi)",
    r"\b(ist|sind)\s+(die\s+)?(hanafi|shafii|schafi|maliki|hanbali|jafari)\w*\s+(besser|richtiger|korrekter|stärker)",
    r"\bsollte\s+ich\s+(die\s+)?(madhhab|rechtsschule)\s+wechseln\b",
)

_JUDGEMENT_PATTERNS: tuple[str, ...] = (
    r"\bist\s+(er|sie|derjenige|diese\s+person|jemand)\s+(noch\s+)?(ein\s+)?(muslim|gläubig|ungläubig|kafir|kufr|murtad|apostat)\b",
    r"\bis\s+(he|she|this\s+person|someone)\s+(still\s+)?(a\s+)?(muslim|believer|disbeliever|kafir|apostate)\b",
    r"\bkommt\s+(er|sie|man)\s+(dafür\s+)?in\s+(die\s+)?(hölle|dschahannam|paradies)\b",
    r"\bwird\s+(er|sie|man)\s+(dafür\s+)?bestraft\b",
    r"\btakfir\b",
    r"\bist\s+das\s+sünde\s+für\s+(mich|ihn|sie)\b",
)

# Umlaute werden mit Alternation erfasst. Nutzer tippen 'aufhören' und
# 'aufhoeren'; ein Muster, das nur eine Form kennt, verfehlt die halbe Zielgruppe.
# Genau dieser Fall ist bei der Entwicklung aufgefallen: 'kann nicht aufhoeren'
# lief durch den Guard, weil das Muster nur 'aufhören' kannte.
_UE = "(ü|ue)"
_OE = "(ö|oe)"
_AE = "(ä|ae)"

_DISTRESS_PATTERNS: tuple[str, ...] = (
    rf"\b(kann|schaffe)\s+(ich\s+)?(es\s+)?nicht\s+(mehr\s+)?(aufh{_OE}ren|stoppen|kontrollieren)\b",
    rf"\bich\s+(kann|schaffe)\s+(es\s+)?nicht\s+mehr\b",
    r"\bich\s+muss\s+(das\s+|mein\w*\s+)?(wudu|gebet|ghusl|waschung)\s+(immer\s+wieder|st(ä|ae)ndig|mehrmals)\b",
    r"\b(zwang|zwangsgedanken|zwangshandlung|waswas|waswasa|skrupulos)\w*\b",
    r"\bich\s+habe\s+(so\s+)?angst\s+(davor\s+)?dass\s+(mein|meine|ich)\b",
    r"\bi\s+(can'?t|cannot)\s+stop\s+(repeating|redoing|washing|checking)\b",
    r"\b(obsessive|intrusive|scrupul\w+)\s*(thoughts?)?\b",
    rf"\bich\s+wiederhole\s+(es\s+|das\s+)?(zehn|zwanzig|hundert|st{_AE}ndig|immer\s+wieder|jedes\s+mal)\b",
    r"\bverzweif\w+\b",
    r"\bich\s+hasse\s+mich\b",
    rf"\bmacht\s+mich\s+(fertig|verr{_UE}ckt|kaputt)\b",
    r"\bnie\s+(gut|richtig)\s+genug\b",
)

_CATEGORY_PATTERNS: tuple[tuple[RequestCategory, tuple[str, ...]], ...] = (
    # Reihenfolge ist Prioritaet. Belastung wird zuerst geprueft, weil sie den
    # Lernkontext ganz verlaesst und andere Kategorien ueberstimmt.
    (RequestCategory.DISTRESS, _DISTRESS_PATTERNS),
    (RequestCategory.JUDGEMENT_OF_PERSON, _JUDGEMENT_PATTERNS),
    (RequestCategory.PERSONAL_VALIDITY, _PERSONAL_VALIDITY_PATTERNS),
    (RequestCategory.MADHHAB_RANKING, _MADHHAB_RANKING_PATTERNS),
    (RequestCategory.RULING_REQUEST, _RULING_PATTERNS),
)

_COMPILED: tuple[tuple[RequestCategory, tuple[re.Pattern[str], ...]], ...] = tuple(
    (category, tuple(re.compile(p, re.IGNORECASE) for p in patterns))
    for category, patterns in _CATEGORY_PATTERNS
)


# --------------------------------------------------------------------------
# Antworten fuer blockierte Kategorien
# --------------------------------------------------------------------------
# Diese Texte sind kein Ausweichen. Sie sagen, was das System stattdessen tut,
# und liefern echten Lerninhalt statt nur einer Absage.

REDIRECT_MESSAGES: dict[str, dict[str, str]] = {
    "ruling_request": {
        "de": (
            "Diese Frage verlangt ein religiöses Rechtsurteil, und das gebe ich nicht — "
            "dafür braucht es einen Gelehrten, der deinen Kontext kennt und Verantwortung "
            "dafür übernimmt.\n\n"
            "Was ich stattdessen tun kann: dir zeigen, was die Quellen zu diesem Thema "
            "sagen, welche Bedingungen sie nennen und wo sich die Rechtsschulen "
            "unterscheiden. Damit kannst du die Frage informiert stellen."
        ),
        "en": (
            "This asks for a religious ruling, and I do not give those — that requires a "
            "scholar who knows your context and takes responsibility for the answer.\n\n"
            "What I can do instead: show you what the sources say on this topic, which "
            "conditions they name, and where the schools of law differ."
        ),
    },
    "personal_validity": {
        "de": (
            "Ob eine konkrete Handlung von dir gültig war, kann ich nicht beurteilen. "
            "Das hängt von Umständen ab, die ich nicht kenne, und es ist eine Rechtsfrage.\n\n"
            "Was ich tun kann: dir die Bedingungen erklären, die die Quellen für diese "
            "Handlung nennen — Schritt für Schritt und mit Quellenangabe. Für die "
            "Beurteilung deines Falls ist ein Gelehrter der richtige Ansprechpartner."
        ),
        "en": (
            "I cannot judge whether a specific act of yours was valid. That depends on "
            "circumstances I do not know, and it is a question of religious law.\n\n"
            "What I can do: explain the conditions the sources name for this act, step by "
            "step and with citations. For your specific case, a scholar is the right person."
        ),
    },
    "madhhab_ranking": {
        "de": (
            "Ich bewerte keine Rechtsschule als die richtige. Die vier sunnitischen Schulen "
            "sind anerkannt, und ihre Unterschiede entstehen aus unterschiedlicher Methodik "
            "bei der Auslegung derselben Quellen — nicht daraus, dass eine mehr wüsste.\n\n"
            "Was ich zeigen kann: wie sich die Schulen methodisch unterscheiden und wie sich "
            "das bei einer konkreten Frage auswirkt. Welche du folgst, ist deine Entscheidung, "
            "meist geprägt von Region und Gemeinschaft."
        ),
        "en": (
            "I do not rank schools of law. The four Sunni schools are recognised, and their "
            "differences come from differing methodology in interpreting the same sources — "
            "not from one knowing more.\n\n"
            "What I can show: how the schools differ methodologically and how that plays out "
            "on a specific question."
        ),
    },
    "judgement_of_person": {
        "de": (
            "Über den Glauben oder das Schicksal eines Menschen urteile ich nicht — weder "
            "über dich noch über jemand anderen. Das steht keinem System zu und auch keinem "
            "Einzelnen.\n\n"
            "Wenn du wissen möchtest, was die Quellen zu einem Thema sagen, frage gern "
            "danach. Über Personen sprechen wir hier nicht."
        ),
        "en": (
            "I do not judge anyone's faith or fate — not yours and not anyone else's. That "
            "is not something a system can do, nor an individual.\n\n"
            "If you want to know what the sources say on a topic, ask about the topic."
        ),
    },
    "distress": {
        "de": (
            "Ich halte hier kurz an, weil deine Nachricht klingt, als würde dich das gerade "
            "sehr beschäftigen.\n\n"
            "Wiederholte Zweifel daran, ob eine Waschung oder ein Gebet 'richtig genug' war, "
            "sind verbreiteter, als man denkt. Und sie lassen sich nicht dadurch auflösen, "
            "dass man noch genauere Regeln lernt — dafür bin ich das falsche Werkzeug. Eher "
            "das Gegenteil: mehr Detailwissen macht den Zweifel oft größer.\n\n"
            "Was hilft, ist ein Gespräch — mit einer Vertrauensperson, einem Gelehrten, dem "
            "du das offen sagen kannst, oder bei anhaltender Belastung mit professioneller "
            "Unterstützung. Wenn du magst, lernen wir gern etwas anderes zusammen weiter."
        ),
        "en": (
            "I am pausing here, because your message sounds like this is weighing on you.\n\n"
            "Repeated doubt about whether a washing or prayer was 'right enough' is more "
            "common than people think. And it does not resolve by learning more precise "
            "rules — I am the wrong tool for that. Often more detail makes the doubt larger.\n\n"
            "What helps is a conversation — with someone you trust, with a scholar you can "
            "be open with, or with professional support if it persists."
        ),
    },
}

TEACHING_HINTS: dict[str, str] = {
    "ruling_request": "Bedingungen und Quellenlage zum Thema darstellen, ohne Einzelfallurteil.",
    "personal_validity": "Bedingungen der Handlung erklaeren, ohne den konkreten Fall zu bewerten.",
    "madhhab_ranking": "Methodische Unterschiede der Rechtsschulen darstellen, ohne Rangfolge.",
    "judgement_of_person": "Kein Lerninhalt zu Personen. Auf Themenfragen umlenken.",
    "distress": "Lernkontext verlassen. Keine weiteren Detailregeln liefern.",
}


# --------------------------------------------------------------------------
# Oeffentliche API
# --------------------------------------------------------------------------

def classify(message: str) -> GuardDecision:
    """Klassifiziert eine Nutzeranfrage vor der Generierung.

    Args:
        message: Rohtext der Nutzeranfrage.

    Returns:
        GuardDecision. Bei allow_generation=False darf der regulaere
        Generierungspfad NICHT betreten werden.
    """
    text = (message or "").strip()
    if not text:
        return GuardDecision(RequestCategory.LEARNING, allow_generation=True)

    for category, patterns in _COMPILED:
        matched = tuple(p.pattern for p in patterns if p.search(text))
        if matched:
            return GuardDecision(
                category=category,
                allow_generation=False,
                matched_patterns=matched,
                redirect_message_key=category.value,
                teaching_hint=TEACHING_HINTS.get(category.value),
            )

    return GuardDecision(RequestCategory.LEARNING, allow_generation=True)


def redirect_message(key: str, language: str = "de") -> str:
    """Liefert den Umleitungstext fuer eine blockierte Kategorie."""
    messages = REDIRECT_MESSAGES.get(key)
    if not messages:
        return REDIRECT_MESSAGES["ruling_request"].get(language, REDIRECT_MESSAGES["ruling_request"]["de"])
    return messages.get(language) or messages.get("de") or next(iter(messages.values()))


# --------------------------------------------------------------------------
# Nachpruefung der generierten Antwort
# --------------------------------------------------------------------------

_FORBIDDEN_OUTPUT_PATTERNS: tuple[tuple[str, str], ...] = (
    (r"\bals\s+(gelehrter|mufti|imam)\s+(sage|erkläre|urteile)\s+ich\b", "authority-simulation"),
    (r"\bas\s+a\s+(scholar|mufti|imam)\s+i\s+(say|rule|declare)\b", "authority-simulation"),
    (r"\bich\s+erteile\s+(dir\s+)?(die\s+)?(erlaubnis|fatwa)\b", "issuing-ruling"),
    (r"\bmein\s+urteil\s+(ist|lautet)\b", "issuing-ruling"),
    (r"\bdas\s+ist\s+(für\s+dich\s+)?(definitiv|eindeutig)\s+(haram|halal)\b", "issuing-ruling"),
    (r"\bdie\s+(richtige|einzig\s+wahre)\s+rechtsschule\s+ist\b", "madhhab-preference"),
    (r"\b(hanafi|shafii|maliki|hanbali)\s+ist\s+die\s+(richtige|beste|stärkste)\b", "madhhab-preference"),
    (r"\bder\s+koran\s+sagt\s*[:\"„]", "translation-as-original"),
    (r"\bein\s+hadith\s+besagt\s+(ungefähr|etwa|in\s+etwa)\b", "unsourced-hadith"),
    (r"\bich\s+erinnere\s+mich\s+an\s+einen\s+hadith\b", "unsourced-hadith"),
    (r"\bes\s+gibt\s+einen\s+hadith,?\s+(der|wo)\b(?![^.]*\b(Bukhari|Muslim|Tirmidhi|Nasai|Abu\s+Dawud|Ibn\s+Majah)\b)", "unsourced-hadith"),
)

_COMPILED_OUTPUT: tuple[tuple[re.Pattern[str], str], ...] = tuple(
    (re.compile(pattern, re.IGNORECASE), rule) for pattern, rule in _FORBIDDEN_OUTPUT_PATTERNS
)


@dataclass
class OutputViolation:
    rule: str
    pattern: str
    excerpt: str


@dataclass
class OutputCheck:
    passed: bool
    violations: list[OutputViolation] = field(default_factory=list)


def check_output(answer: str) -> OutputCheck:
    """Prueft eine generierte Antwort auf Policy-Verstoesse.

    Wird nach der Generierung und nach der Zitatpruefung aufgerufen. Ein Verstoss
    fuehrt zum Verwerfen der Antwort, nicht zu einer Warnung.
    """
    violations: list[OutputViolation] = []
    for pattern, rule in _COMPILED_OUTPUT:
        match = pattern.search(answer or "")
        if match:
            start = max(0, match.start() - 40)
            end = min(len(answer), match.end() + 40)
            violations.append(
                OutputViolation(rule=rule, pattern=pattern.pattern, excerpt=answer[start:end].strip())
            )
    return OutputCheck(passed=not violations, violations=violations)
