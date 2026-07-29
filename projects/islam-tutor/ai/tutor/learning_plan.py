"""Lernplan-Generator.

Entwurfsentscheidung — regelbasiert statt LLM-generiert:
Ein Lernplan ist eine Reihenfolge mit Abhaengigkeiten. Wer das Gebet lernen will,
braucht zuerst die Reinigung, dann die Bewegungen, dann die Texte — diese Ordnung
ist didaktisch und aendert sich nicht pro Anfrage. Ein LLM wuerde sie jedes Mal
neu erfinden, mit dem Risiko, eine Abhaengigkeit zu vertauschen.

Regelbasiert ist hier also nicht die aermere, sondern die richtige Loesung. Was
das LLM beitraegt, liegt im Chat: Erklaerung, Rueckfrage, Anpassung an
Verstaendnisprobleme.

Alle Plaene verweisen ausschliesslich auf existierende Module. Ein Plan, der auf
fehlende Inhalte zeigt, wird gekuerzt statt mit Platzhaltern gefuellt.
"""
from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PlanStep:
    day: int
    title: str
    focus: str
    module: str
    deep_link: str | None = None
    estimated_minutes: int = 15
    practice: str | None = None


@dataclass
class LearningPlan:
    goal: str
    steps: list[PlanStep] = field(default_factory=list)
    minutes_per_day: int = 15
    madhhab: str | None = None
    note: str = ""

    @property
    def total_days(self) -> int:
        return max((s.day for s in self.steps), default=0)


# --------------------------------------------------------------------------
# Bausteine
# --------------------------------------------------------------------------
# Jeder Baustein ist eine Lerneinheit mit fester Reihenfolge innerhalb ihres
# Ziels. Der Generator verteilt sie auf Tage entsprechend der verfuegbaren Zeit.

_PurificationBlocks: list[tuple[str, str, str, str | None, int, str | None]] = [
    (
        "Wudu — Überblick",
        "Verstehen, welche Elemente Pflicht sind und welche Sunnah. Die vier Pflichtelemente merken.",
        "purification",
        "/purification/wudu",
        10,
        "Die vier Pflichtelemente aus dem Gedächtnis aufsagen: Gesicht, Arme, Kopf, Füße.",
    ),
    (
        "Wudu — Schritte 1 bis 5",
        "Absicht, Basmala, Hände, Mund, Nase. Die vorbereitenden Schritte einüben.",
        "purification",
        "/purification/wudu#step-1",
        12,
        "Die Reihenfolge trocken durchgehen, ohne Wasser.",
    ),
    (
        "Wudu — Schritte 6 bis 11",
        "Gesicht, Arme, Kopf, Ohren, Füße, Abschluss. Die Pflichtelemente in der Praxis.",
        "purification",
        "/purification/wudu#step-6",
        15,
        "Einmal vollständig durchführen und dabei auf Knöchel und Ellbogen achten.",
    ),
    (
        "Wudu — Häufige Fehler",
        "Die dokumentierten Fehlerquellen durchgehen und beim eigenen Ablauf prüfen.",
        "purification",
        "/purification/wudu",
        8,
        None,
    ),
]

_PrayerBlocks: list[tuple[str, str, str, str | None, int, str | None]] = [
    (
        "Fajr — Überblick",
        "Das kürzeste Gebet: zwei Rak'a. Struktur und Zeitfenster verstehen.",
        "prayer",
        "/prayer/fajr",
        10,
        None,
    ),
    (
        "Die Bewegungen kennenlernen",
        "Qiyam, Ruku, Sujud, Jalsa, Qa'da. Was der Körper in jedem Schritt tut.",
        "prayer",
        "/prayer/movement/ruku",
        15,
        "Jede Bewegung einmal langsam einnehmen und die Position halten.",
    ),
    (
        "Takbir und Eröffnung",
        "Eröffnungs-Takbir, Thana, Ta'awwudh. Die ersten Schritte mit Text.",
        "prayer",
        "/prayer/movement/takbir_ihram",
        12,
        "Den Takbir und das Eröffnungsbittgebet sprechen.",
    ),
    (
        "Al-Fatiha im Gebet",
        "Die Sure, die in jeder Rak'a rezitiert wird. Text und Aussprache.",
        "quran",
        "/quran/1",
        20,
        "Al-Fatiha zweimal langsam rezitieren.",
    ),
    (
        "Ruku und Sujud mit Text",
        "Die Tasbih-Formeln in Verbeugung und Niederwerfung.",
        "prayer",
        "/prayer/movement/sujud",
        12,
        "Bewegung und Text zusammen üben, dreimal je Position.",
    ),
    (
        "Tashahhud lernen",
        "Der Text des abschließenden Sitzens. Der längste Text im Gebet.",
        "prayer",
        "/prayer/movement/qada_final",
        20,
        "Den Tashahhud in vier Abschnitten lernen, jeden zehnmal.",
    ),
    (
        "Fajr vollständig",
        "Die zwei Rak'a von Anfang bis Taslim ohne Unterbrechung.",
        "prayer",
        "/prayer/fajr",
        20,
        "Ein vollständiges Fajr-Gebet durchgehen.",
    ),
    (
        "Maghrib — drei Rak'a",
        "Das Zwischensitzen kommt hinzu. Was sich gegenüber zwei Rak'a ändert.",
        "prayer",
        "/prayer/maghrib",
        15,
        None,
    ),
    (
        "Dhuhr — vier Rak'a",
        "Die dritte und vierte Rak'a: nur Al-Fatiha, keine weitere Sure, stille Rezitation.",
        "prayer",
        "/prayer/dhuhr",
        15,
        None,
    ),
    (
        "Alle fünf Gebete im Überblick",
        "Rak'a-Zahlen, Zeitfenster und laute oder stille Rezitation nebeneinander.",
        "prayer",
        "/prayer/isha",
        12,
        "Die fünf Gebete mit ihren Rak'a-Zahlen aus dem Gedächtnis aufschreiben.",
    ),
]

_ArabicBlocks: list[tuple[str, str, str, str | None, int, str | None]] = [
    (
        "Lerneinheit 1 — Bekannte Laute",
        "Elf Buchstaben, deren Laut aus dem Deutschen bekannt ist. Formen erkennen und schreiben.",
        "arabic",
        "/arabic/curriculum/1",
        15,
        "Jeden Buchstaben in allen vier Positionsformen von Hand schreiben.",
    ),
    (
        "Verwechslungsgefahr — Punkte",
        "Ba, Ta, Tha, Nun und Dal, Dhal, Ra, Zay unterscheiden sich nur in den Punkten.",
        "arabic",
        "/arabic/confusion/b_t_th",
        12,
        "Aus einer gemischten Reihe die Buchstaben benennen.",
    ),
    (
        "Lerneinheit 2 — Neue Laute",
        "Acht Buchstaben ohne direkte deutsche Entsprechung, aber gut beschreibbar.",
        "arabic",
        "/arabic/curriculum/2",
        15,
        None,
    ),
    (
        "Vokalzeichen",
        "Fatha, Kasra, Damma, Sukun und Shadda. Damit wird Lesen möglich.",
        "arabic",
        "/arabic/vowel/fatha",
        15,
        "Bekannte Buchstaben mit allen Vokalzeichen laut lesen.",
    ),
    (
        "Lerneinheit 3 — Emphatische Laute",
        "Sad, Dad, Ta, Za im Kontrast zu ihren nicht-emphatischen Gegenstücken.",
        "arabic",
        "/arabic/curriculum/3",
        18,
        "Die Paare Sin–Sad und Dal–Dad nebeneinander sprechen.",
    ),
    (
        "Lerneinheit 4 — Rachenlaute",
        "Ain, Ghain, Ha und Qaf. Die schwierigste Gruppe. Realistisch: das braucht Wochen.",
        "arabic",
        "/arabic/curriculum/4",
        20,
        "Täglich fünf Minuten nur diese vier Laute. Ohne Erfolgsdruck.",
    ),
    (
        "Verbindungen lesen",
        "Sechs Buchstaben verbinden sich nicht nach vorne. Wortgrenzen im Schriftbild erkennen.",
        "arabic",
        "/arabic/curriculum/5",
        15,
        None,
    ),
    (
        "Erste Wörter — Al-Fatiha",
        "Die Sure Wort für Wort lesen, mit Wortanalyse.",
        "quran",
        "/quran/1",
        20,
        "Vers 1 und 2 lesen, ohne auf die Transliteration zu schauen.",
    ),
]

_MemorizeBlocks: list[tuple[str, str, str, str | None, int, str | None]] = [
    ("Al-Fatiha — Basmala", "Vers 1 lernen. Wort für Wort mit Bedeutung.", "quran", "/quran/1#1", 12,
     "Vers 1 zehnmal wiederholen, dann aus dem Gedächtnis."),
    ("Al-Fatiha — Verse 2 bis 4", "Lobpreis und Attribute. Drei kurze Verse als Einheit.", "quran", "/quran/1#2", 18,
     "Verse 1 bis 4 zusammenhängend."),
    ("Wiederholung 1 bis 4", "Festigen, bevor Neues dazukommt.", "quran", "/quran/1", 10,
     "Ohne Vorlage aufsagen. Bei Stocken zurück zum Text, nicht raten."),
    ("Al-Fatiha — Vers 5", "Das Bekenntnis. Kurz, aber rhythmisch eigenständig.", "quran", "/quran/1#5", 12, None),
    ("Al-Fatiha — Verse 6 und 7", "Die Bitte um Leitung. Vers 7 ist der längste und schwerste.", "quran", "/quran/1#6", 20,
     "Vers 7 in drei Teile zerlegen und einzeln üben."),
    ("Al-Fatiha vollständig", "Alle sieben Verse zusammenhängend.", "quran", "/quran/1", 15,
     "Dreimal vollständig, langsam."),
    ("Festigung mit Abstand", "Nach einem Tag Pause erneut aufsagen. Vergessen ist Teil des Lernens.", "quran", "/quran/1", 10,
     "Ohne Vorlage. Was fehlt, gezielt nacharbeiten."),
]

_GOAL_BLOCKS: dict[str, list[tuple[str, str, str, str | None, int, str | None]]] = {
    "learn_to_pray": _PurificationBlocks + _PrayerBlocks,
    "learn_purification": _PurificationBlocks,
    "learn_arabic_script": _ArabicBlocks,
    "memorize_fatiha": _MemorizeBlocks,
}

_GOAL_NOTES: dict[str, str] = {
    "learn_to_pray": (
        "Der Plan beginnt mit der Reinigung, weil sie Voraussetzung für das Gebet ist. "
        "Danach kommen Bewegungen vor Texten — die Abfolge im Körper zu haben macht das "
        "Lernen der Texte leichter. Die Zeitangaben sind Anhaltspunkte, kein Soll."
    ),
    "learn_purification": (
        "Wudu zuerst vollständig, dann Ghusl und Tayammum als Varianten. Wer Wudu "
        "sicher kann, versteht die anderen beiden schneller."
    ),
    "learn_arabic_script": (
        "Die Reihenfolge folgt der Schwierigkeit, nicht dem Alphabet. Dadurch gibt es "
        "früher erste Leseerfolge. Die Rachenlaute stehen am Ende und brauchen deutlich "
        "mehr Zeit als die übrigen — das ist normal und kein Anzeichen von Unfähigkeit."
    ),
    "memorize_fatiha": (
        "Der Plan baut Wiederholungen mit Abstand ein, weil verteiltes Üben besser hält "
        "als Wiederholung am Stück. Vergessen zwischen den Einheiten gehört zum Vorgang "
        "und ist kein Rückschritt."
    ),
}

_PRIOR_KNOWLEDGE_FACTOR: dict[str, float] = {
    "none": 1.0,
    "some": 0.7,
    "solid": 0.5,
}


def generate_plan(
    goal: str,
    *,
    minutes_per_day: int = 15,
    madhhab: str | None = None,
    prior_knowledge: str = "none",
    language: str = "de",
) -> LearningPlan:
    """Erzeugt einen Lernplan.

    Args:
        goal: Eines der Ziele aus _GOAL_BLOCKS.
        minutes_per_day: Verfuegbare Zeit. Bestimmt, wie viele Bausteine auf
            einen Tag fallen.
        madhhab: Rechtsschule fuer die Hinweise im Plan.
        prior_knowledge: none | some | solid. Kuerzt die geschaetzte Zeit,
            nicht die Inhalte — weglassen entscheidet der Lernende selbst.
        language: derzeit nur fuer den Hinweistext relevant.

    Raises:
        ValueError: bei unbekanntem Ziel.
    """
    blocks = _GOAL_BLOCKS.get(goal)
    if blocks is None:
        raise ValueError(f"Unbekanntes Ziel '{goal}'. Erlaubt: {sorted(_GOAL_BLOCKS)}")

    factor = _PRIOR_KNOWLEDGE_FACTOR.get(prior_knowledge, 1.0)
    budget = max(minutes_per_day, 5)

    steps: list[PlanStep] = []
    day = 1
    day_used = 0

    for title, focus, module, link, base_minutes, practice in blocks:
        minutes = max(5, round(base_minutes * factor))

        # Ein Baustein wird nicht geteilt. Passt er nicht mehr in den Tag,
        # beginnt ein neuer Tag. Ausnahme: er ist allein schon zu gross —
        # dann bekommt er einen eigenen Tag statt endlos zu wandern.
        if day_used > 0 and day_used + minutes > budget:
            day += 1
            day_used = 0

        steps.append(
            PlanStep(
                day=day,
                title=title,
                focus=focus,
                module=module,
                deep_link=link,
                estimated_minutes=minutes,
                practice=practice,
            )
        )
        day_used += minutes

    note = _GOAL_NOTES.get(goal, "")
    if madhhab:
        note += (
            f" Der Plan zeigt die Variante nach der Rechtsschule {madhhab}; "
            "wo andere Positionen bestehen, werden sie genannt."
        )
    else:
        note += (
            " Es ist keine Rechtsschule gewählt. Wo sich die Schulen unterscheiden, "
            "zeigt der Plan alle dokumentierten Positionen."
        )

    return LearningPlan(
        goal=goal,
        steps=steps,
        minutes_per_day=budget,
        madhhab=madhhab,
        note=note.strip(),
    )


AVAILABLE_GOALS: tuple[str, ...] = tuple(_GOAL_BLOCKS)
