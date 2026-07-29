"""Voice-Policy — ADR-0002: kein TTS für arabischen Korantext.

Die Ablehnung sitzt in der Basisklasse voice.base.TTSProvider und wird von jedem
Provider geerbt. Diese Tests beweisen, dass kein Provider sie umgehen kann und
dass die Ablehnung unabhaengig von der technischen Verfuegbarkeit greift.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from voice.base import (  # noqa: E402
    AudioResult,
    TTSProvider,
    arabic_share,
    looks_like_recitation,
)
from voice.registry import (  # noqa: E402
    NullTTS,
    SystemTTS,
    available_providers,
    get_stt_provider,
    get_tts_provider,
)

MARK = "policy"

FATIHA_AYAH = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"
TASHAHHUD_START = "التَّحِيَّاتُ لِلَّهِ وَالصَّلَوَاتُ وَالطَّيِّبَاتُ"
TASBIH = "سُبْحَانَ رَبِّيَ الْعَظِيمِ"


class _AlwaysAvailableTTS(TTSProvider):
    """Provider, der alles synthetisieren wuerde, wenn er duerfte.

    Dient dem Beweis, dass die Ablehnung in der Basisklasse greift und nicht
    von der Kooperation des Providers abhaengt.
    """

    name = "test_provider"

    @property
    def available(self) -> bool:
        return True

    def _synthesize(self, text, *, language, voice, kind) -> AudioResult:
        return AudioResult(audio=b"AUDIO", mime_type="audio/mpeg", provider=self.name)


# ==========================================================================
# ADR-0002 — Ablehnung
# ==========================================================================

def test_quran_text_is_rejected_by_any_provider():
    """Auch ein voll funktionsfaehiger Provider darf Korantext nicht sprechen."""
    result = _AlwaysAvailableTTS().synthesize(FATIHA_AYAH)
    assert result.rejected, "Korantext wurde nicht abgelehnt"
    assert result.audio is None
    assert "0002-no-tts-for-quran" in result.rejection_reason.lower()


def test_ritual_prayer_text_is_rejected():
    """Tashahhud und Tasbih sind rituelle Texte und werden ebenfalls abgelehnt."""
    provider = _AlwaysAvailableTTS()
    for text in (TASHAHHUD_START, TASBIH):
        result = provider.synthesize(text)
        assert result.rejected, f"Nicht abgelehnt: {text[:30]}"


def test_rejection_applies_even_without_configured_provider():
    """Die inhaltliche Grenze ist von der Verfuegbarkeit unabhaengig.

    Ein NullTTS ist nicht verfuegbar. Trotzdem soll die Antwort 'abgelehnt'
    lauten, nicht 'nicht konfiguriert' — sonst wuerde die Grenze wirkungslos,
    sobald ein Provider dazukommt.
    """
    result = NullTTS().synthesize(FATIHA_AYAH)
    assert result.rejected
    assert result.rejection_reason


def test_rejection_reason_explains_why():
    """Die Ablehnung erklaert sich, statt nur zu verweigern."""
    reason = _AlwaysAvailableTTS().synthesize(FATIHA_AYAH).rejection_reason.lower()
    assert "tajwid" in reason
    assert "rezitator" in reason or "menschlich" in reason


def test_system_tts_also_rejects():
    """Auch die Browser-Synthese wird serverseitig abgelehnt."""
    assert SystemTTS().synthesize(FATIHA_AYAH).rejected


# ==========================================================================
# Erlaubte Fälle — der Filter darf nicht überschießen
# ==========================================================================

def test_german_explanation_is_allowed():
    """Erklaertexte in der Nutzersprache duerfen vorgelesen werden."""
    result = _AlwaysAvailableTTS().synthesize(
        "Das Fajr-Gebet umfasst zwei Rak'a. Es wird vor Sonnenaufgang verrichtet."
    )
    assert not result.rejected, result.rejection_reason
    assert result.succeeded


def test_translation_is_allowed():
    result = _AlwaysAvailableTTS().synthesize(
        "Im Namen Allahs, des Allerbarmers, des Barmherzigen.", kind="translation"
    )
    assert not result.rejected


def test_single_arabic_term_in_german_sentence_is_allowed():
    """Ein Fachwort im deutschen Satz ist kein Rezitationstext.

    Ein Filter mit Schwelle null wuerde 'Was bedeutet رُكُوع?' ablehnen und damit
    eine legitime Lernfunktion verhindern. Der Schwellwert existiert genau dafuer.
    """
    result = _AlwaysAvailableTTS().synthesize("Was bedeutet der Begriff رُكُوع genau?")
    assert not result.rejected, result.rejection_reason


def test_transliteration_is_allowed():
    """Transliteration ist Lateinschrift und darf gesprochen werden."""
    result = _AlwaysAvailableTTS().synthesize(
        "Der Text lautet in Umschrift: Subhana rabbiya l-azim."
    )
    assert not result.rejected


# ==========================================================================
# Erkennungslogik
# ==========================================================================

def test_arabic_share_computation():
    assert arabic_share("") == 0.0
    assert arabic_share("nur deutscher Text") == 0.0
    assert arabic_share(FATIHA_AYAH) == 1.0
    assert 0.0 < arabic_share("Der Begriff رُكُوع bedeutet Verbeugung") < 0.5


def test_recitation_detection_reasons():
    rejected, reason = looks_like_recitation(FATIHA_AYAH)
    assert rejected
    assert reason

    rejected, reason = looks_like_recitation("Das ist ein deutscher Satz.")
    assert not rejected
    assert reason == ""


def test_empty_text_is_not_recitation():
    assert looks_like_recitation("") == (False, "")


def test_vocalised_arabic_is_detected_as_recitation():
    """Durchgehende Diakritika weisen auf Koran- oder Gebetstext hin."""
    rejected, reason = looks_like_recitation("سُبْحَانَ رَبِّيَ الْأَعْلَى")
    assert rejected
    assert reason


# ==========================================================================
# Registry
# ==========================================================================

def test_unknown_provider_falls_back_to_null():
    """Ein Tippfehler in der Konfiguration darf nichts oeffnen, was zu ist."""
    assert get_tts_provider("gibt_es_nicht").name == "none"
    assert get_stt_provider("gibt_es_nicht").name == "none"


def test_default_providers_are_unavailable():
    """Ohne Konfiguration ist keine Sprachfunktion aktiv — ehrlicher Standard."""
    assert not get_tts_provider("none").available
    assert not get_stt_provider("none").available


def test_available_providers_reports_honestly():
    report = available_providers()
    assert "stt" in report
    assert "tts" in report
    # 'none' ist nie verfuegbar und darf nicht als nutzbar gemeldet werden
    assert "none" not in report["stt"]
    assert "none" not in report["tts"]


def test_null_stt_returns_empty_transcript_without_raising():
    """Ohne Provider gibt es ein leeres Ergebnis, keine Exception."""
    transcript = get_stt_provider("none").transcribe(b"")
    assert transcript.text == ""
    assert transcript.provider == "none"
