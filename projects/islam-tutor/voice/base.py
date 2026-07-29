"""Provider-Abstraktion für Sprache.

Aufbau nach demselben Muster wie die Connector-Schicht im Elternprojekt:
Abstract Base Class, konkrete Provider, definierter Fallback. Ein Wechsel von
Whisper auf ElevenLabs oder auf ein lokales Modell aendert Konfiguration, nicht Code.

Die wichtigste Regel dieses Moduls ist eine Ablehnung: `TTSProvider.synthesize`
weist arabischen Korantext ab. Siehe docs/adr/0002-no-tts-for-quran.md.
Die Pruefung sitzt in der Basisklasse, damit kein Provider sie ueberspringen kann.
"""
from __future__ import annotations

import re
from abc import ABC, abstractmethod
from dataclasses import dataclass, field


@dataclass
class Transcript:
    text: str
    language: str | None = None
    confidence: float | None = None
    segments: list[dict] = field(default_factory=list)
    provider: str = ""


@dataclass
class AudioResult:
    audio: bytes | None = None
    mime_type: str | None = None
    provider: str = ""
    rejected: bool = False
    rejection_reason: str | None = None
    error: str | None = None

    @property
    def succeeded(self) -> bool:
        return not self.rejected and self.error is None and bool(self.audio)


# --------------------------------------------------------------------------
# Arabisch-Erkennung
# --------------------------------------------------------------------------

_ARABIC_DIACRITICS = re.compile(r"[ً-ٰٟۖ-ۭ]")

# Alef-Varianten werden auf das schlichte Alef vereinheitlicht. Der Korantext
# in Uthmani-Orthographie nutzt Alef Wasla (ٱ), nicht das gewoehnliche
# Alef (ا). Ohne diese Normalisierung greift kein Wortmarker auf
# Korantext — genau dieser Fehler ist bei der Entwicklung aufgetreten:
# Al-Fatiha wurde nicht als Rezitationstext erkannt.
_ALEF_VARIANTS = str.maketrans({
    "ٱ": "ا",  # Alef Wasla
    "ٲ": "ا",  # Alef with wavy hamza above
    "ٳ": "ا",  # Alef with wavy hamza below
    "آ": "ا",  # Alef with madda
    "أ": "ا",  # Alef with hamza above
    "إ": "ا",  # Alef with hamza below
    "ى": "ي",  # Alef maksura zu Ya
    "ة": "ه",  # Ta marbuta zu Ha
})


def _is_arabic_letter(ch: str) -> bool:
    """Arabischer Buchstabe im Unicode-Block, ohne Diakritika.

    Bewusst ueber Blockgrenzen statt eine Zeichenklasse: eine erste Fassung
    nutzte den Bereich bis ي und verfehlte damit Alef Wasla und die
    erweiterten Buchstaben, die im Korantext vorkommen.
    """
    return ch.isalpha() and "؀" <= ch <= "ۿ"


def _normalise_arabic(text: str) -> str:
    """Diakritika entfernen und Alef-Varianten vereinheitlichen."""
    return _ARABIC_DIACRITICS.sub("", text).translate(_ALEF_VARIANTS)


# Wortmarker, die auf rituellen oder koranischen Text hindeuten. Sie stehen in
# normalisierter Form: ohne Diakritika, mit schlichtem Alef.
_RECITATION_MARKERS: tuple[str, ...] = (
    "بسم الله",
    "الحمد لله",
    "الرحمن الرحيم",
    "مالك يوم الدين",
    "اياك نعبد",
    "اهدنا",
    "قل هو الله",
    "سبحان ربي",
    "التحيات لله",
    "اعوذ بالله",
    "الله اكبر",
    "سمع الله لمن حمده",
    "اللهم صل على",
    "السلام عليكم ورحمة الله",
    "لا اله الا الله",
)

ARABIC_SHARE_THRESHOLD = 0.30
"""Ab welchem Anteil arabischer Buchstaben ein Text als arabisch gilt.

Kein Nullwert, weil ein einzelnes arabisches Fachwort in einem deutschen Satz
('Was bedeutet رُكُوع?') kein Rezitationstext ist und vorgelesen werden darf.
"""


def arabic_share(text: str) -> float:
    """Anteil arabischer Buchstaben an allen Buchstaben."""
    letters = [ch for ch in text if ch.isalpha()]
    if not letters:
        return 0.0
    arabic = sum(1 for ch in letters if _is_arabic_letter(ch))
    return arabic / len(letters)


def looks_like_recitation(text: str) -> tuple[bool, str]:
    """Prueft, ob ein Text als Rezitationstext behandelt werden muss.

    Drei Signale, jedes fuer sich ausreichend:
      1. Bekannter Anfang eines Koran- oder Gebetstexts
      2. Hoher Anteil arabischer Buchstaben
      3. Vollvokalisierter arabischer Text — Diakritika werden im Alltagsarabisch
         nicht gesetzt, im Korantext dagegen durchgaengig

    Returns:
        (True, Begruendung) wenn abzulehnen, sonst (False, "").
    """
    if not text:
        return False, ""

    normalised = _normalise_arabic(text)
    for marker in _RECITATION_MARKERS:
        if marker in normalised:
            return True, f"Bekannter Rezitationstext erkannt ('{marker}')."

    share = arabic_share(text)
    if share >= ARABIC_SHARE_THRESHOLD:
        diacritic_count = len(_ARABIC_DIACRITICS.findall(text))
        arabic_count = sum(1 for ch in text if _is_arabic_letter(ch))
        if arabic_count and diacritic_count / arabic_count > 0.25:
            return True, (
                "Vollvokalisierter arabischer Text. Durchgehende Diakritika weisen auf "
                "Koran- oder Gebetstext hin."
            )
        return True, (
            f"Überwiegend arabischer Text ({share:.0%} arabische Buchstaben). "
            "Arabische Rezitation wird nicht synthetisiert."
        )

    return False, ""


REJECTION_MESSAGE: str = (
    "Arabischer Korantext und rituelle Gebetstexte werden nicht per Sprachsynthese "
    "ausgegeben. Koranrezitation folgt den Tajwid-Regeln, die ein generisches "
    "Sprachmodell nicht anwendet — eine synthetische Stimme wäre ein fehlerhaftes "
    "Aussprachevorbild für Lernende. Stattdessen werden Aufnahmen menschlicher "
    "Rezitatoren verwendet. Liegt keine Aufnahme vor, zeigt die Oberfläche den Text "
    "ohne Audio. Begründung: docs/adr/0002-no-tts-for-quran.md"
)


# --------------------------------------------------------------------------
# Interfaces
# --------------------------------------------------------------------------

class STTProvider(ABC):
    """Speech-to-Text."""

    name: str = "abstract"

    @abstractmethod
    def transcribe(self, audio: bytes, *, language: str | None = None) -> Transcript: ...

    @property
    def available(self) -> bool:
        return False


class TTSProvider(ABC):
    """Text-to-Speech.

    `synthesize` ist bewusst nicht abstrakt: die Basisklasse fuehrt die
    Ablehnungspruefung durch und delegiert erst danach an `_synthesize`.
    Ein Provider kann die Pruefung damit nicht umgehen, ohne die Basisklasse
    zu veraendern.
    """

    name: str = "abstract"

    def synthesize(
        self, text: str, *, language: str = "de", voice: str | None = None, kind: str = "instruction"
    ) -> AudioResult:
        rejected, reason = looks_like_recitation(text)
        if rejected:
            return AudioResult(
                provider=self.name,
                rejected=True,
                rejection_reason=f"{reason} {REJECTION_MESSAGE}",
            )

        if kind == "pronunciation" and arabic_share(text) > 0:
            # Einzelne Buchstaben und Vokabeln sind als Lernhilfe zugelassen —
            # Content Policy und ADR-0002 unterscheiden Lauthilfe von Rezitation.
            pass

        if not self.available:
            return AudioResult(provider=self.name, error="Provider nicht verfügbar.")

        return self._synthesize(text, language=language, voice=voice, kind=kind)

    @abstractmethod
    def _synthesize(
        self, text: str, *, language: str, voice: str | None, kind: str
    ) -> AudioResult: ...

    @property
    def available(self) -> bool:
        return False
