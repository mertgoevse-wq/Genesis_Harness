"""Provider-Auswahl für Sprache.

Alle Provider sind hier registriert. Der Aufrufer nennt einen Namen aus der
Konfiguration und bekommt eine Instanz — oder den NullProvider, wenn nichts
konfiguriert ist. Es wird keine Exception geworfen, weil kein Provider
angebunden ist: das System soll ohne Sprachanbindung vollstaendig nutzbar sein.

Registrierte Provider:

    STT   none            NullSTT — sagt ehrlich, dass nichts konfiguriert ist
          whisper_local   Lokales Whisper-Modell, offline
          whisper_api     OpenAI Whisper API

    TTS   none            NullTTS
          elevenlabs      ElevenLabs
          system          Browser-native Synthese (Signal an das Frontend)

Alle TTS-Provider erben die Ablehnungspruefung aus voice.base.TTSProvider und
koennen sie nicht umgehen.
"""
from __future__ import annotations

import os
from functools import lru_cache

from voice.base import AudioResult, STTProvider, Transcript, TTSProvider


# --------------------------------------------------------------------------
# Null-Provider
# --------------------------------------------------------------------------

class NullSTT(STTProvider):
    """Kein STT konfiguriert. Antwortet ehrlich statt zu scheitern."""

    name = "none"

    def transcribe(self, audio: bytes, *, language: str | None = None) -> Transcript:
        return Transcript(text="", provider=self.name)

    @property
    def available(self) -> bool:
        return False


class NullTTS(TTSProvider):
    """Kein TTS konfiguriert. Die Ablehnungspruefung greift trotzdem.

    Das ist beabsichtigt: eine Anfrage mit Korantext wird auch ohne Provider
    als abgelehnt gemeldet, nicht als 'nicht konfiguriert'. Die inhaltliche
    Grenze ist von der technischen Verfuegbarkeit unabhaengig.
    """

    name = "none"

    def _synthesize(self, text: str, *, language: str, voice: str | None, kind: str) -> AudioResult:
        return AudioResult(provider=self.name, error="Provider nicht verfügbar.")

    @property
    def available(self) -> bool:
        return False


# --------------------------------------------------------------------------
# Whisper
# --------------------------------------------------------------------------

class WhisperLocalSTT(STTProvider):
    """Lokales Whisper-Modell. Laeuft offline, keine Daten verlassen das Gerät.

    Der Import liegt in der Methode, damit das Paket ohne installiertes Whisper
    importierbar bleibt.
    """

    name = "whisper_local"

    def __init__(self, model_size: str = "base") -> None:
        self.model_size = model_size
        self._model = None

    @property
    def available(self) -> bool:
        try:
            import whisper  # noqa: F401
        except ImportError:
            return False
        return True

    def transcribe(self, audio: bytes, *, language: str | None = None) -> Transcript:
        if not self.available:
            return Transcript(text="", provider=self.name)

        import tempfile

        import whisper

        if self._model is None:
            self._model = whisper.load_model(self.model_size)

        with tempfile.NamedTemporaryFile(suffix=".wav", delete=True) as handle:
            handle.write(audio)
            handle.flush()
            result = self._model.transcribe(handle.name, language=language)

        return Transcript(
            text=result.get("text", "").strip(),
            language=result.get("language"),
            segments=result.get("segments", []),
            provider=self.name,
        )


class WhisperAPISTT(STTProvider):
    """Whisper über API. Erfordert einen Schlüssel."""

    name = "whisper_api"

    def __init__(self, api_key: str | None = None) -> None:
        self._api_key = api_key or os.environ.get("OPENAI_API_KEY")

    @property
    def available(self) -> bool:
        return bool(self._api_key)

    def transcribe(self, audio: bytes, *, language: str | None = None) -> Transcript:
        if not self.available:
            return Transcript(text="", provider=self.name)
        raise NotImplementedError(
            "Anbindung ausstehend. Die Abstraktion ist vollständig; hier fehlt der "
            "HTTP-Aufruf gegen den Anbieter."
        )


# --------------------------------------------------------------------------
# TTS
# --------------------------------------------------------------------------

class ElevenLabsTTS(TTSProvider):
    """ElevenLabs. Nur für Erklärtexte und Übersetzungen — nie für Korantext."""

    name = "elevenlabs"

    def __init__(self, api_key: str | None = None, voice_id: str | None = None) -> None:
        self._api_key = api_key or os.environ.get("ELEVENLABS_API_KEY")
        self.voice_id = voice_id

    @property
    def available(self) -> bool:
        return bool(self._api_key)

    def _synthesize(self, text: str, *, language: str, voice: str | None, kind: str) -> AudioResult:
        raise NotImplementedError(
            "Anbindung ausstehend. Die Abstraktion inklusive Ablehnungsprüfung ist "
            "vollständig; hier fehlt der HTTP-Aufruf gegen den Anbieter."
        )


class SystemTTS(TTSProvider):
    """Browser-native Synthese.

    Liefert kein Audio, sondern signalisiert dem Frontend, die Web Speech API zu
    nutzen. Dadurch bleibt die Ablehnungsprüfung serverseitig wirksam: das
    Frontend fragt an, der Server entscheidet, ob synthetisiert werden darf.
    """

    name = "system"

    @property
    def available(self) -> bool:
        return True

    def _synthesize(self, text: str, *, language: str, voice: str | None, kind: str) -> AudioResult:
        return AudioResult(
            audio=None,
            mime_type="application/x-client-speech",
            provider=self.name,
        )


# --------------------------------------------------------------------------
# Auswahl
# --------------------------------------------------------------------------

_STT_PROVIDERS: dict[str, type[STTProvider]] = {
    "none": NullSTT,
    "whisper_local": WhisperLocalSTT,
    "whisper_api": WhisperAPISTT,
}

_TTS_PROVIDERS: dict[str, type[TTSProvider]] = {
    "none": NullTTS,
    "elevenlabs": ElevenLabsTTS,
    "system": SystemTTS,
}


@lru_cache
def get_stt_provider(name: str = "none") -> STTProvider:
    """Liefert einen STT-Provider. Unbekannter Name ergibt NullSTT."""
    provider_class = _STT_PROVIDERS.get(name, NullSTT)
    return provider_class()


@lru_cache
def get_tts_provider(name: str = "none") -> TTSProvider:
    """Liefert einen TTS-Provider. Unbekannter Name ergibt NullTTS."""
    provider_class = _TTS_PROVIDERS.get(name, NullTTS)
    return provider_class()


def available_providers() -> dict[str, list[str]]:
    """Welche Provider technisch nutzbar sind. Für /health und Diagnose."""
    return {
        "stt": [name for name in _STT_PROVIDERS if get_stt_provider(name).available],
        "tts": [name for name in _TTS_PROVIDERS if get_tts_provider(name).available],
    }
