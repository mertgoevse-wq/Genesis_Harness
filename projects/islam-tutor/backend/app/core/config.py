"""Zentrale Konfiguration.

Alle Einstellungen kommen aus Umgebungsvariablen mit dem Prefix ISLAM_TUTOR_.
Keine Geheimnisse im Code, keine Magic Numbers in der Geschaeftslogik.
"""
from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ISLAM_TUTOR_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # --- Anwendung ----------------------------------------------------
    app_name: str = "Islam Tutor AI"
    version: str = "0.1.0"
    debug: bool = False
    port: int = 8100

    # --- Pfade --------------------------------------------------------
    project_root: Path = PROJECT_ROOT
    knowledge_dir: Path = PROJECT_ROOT / "knowledge"
    frontend_dir: Path = PROJECT_ROOT / "frontend"
    audio_dir: Path = PROJECT_ROOT / "voice" / "audio_assets"

    # --- Inhalt -------------------------------------------------------
    default_language: str = "de"
    supported_languages: tuple[str, ...] = ("de", "en", "tr")
    default_madhhab: str | None = None
    """Keine Vorauswahl. Ohne Auswahl zeigt das System alle Varianten —
    Content Policy 5: das System bevorzugt keine Rechtsschule."""

    supported_madhahib: tuple[str, ...] = ("hanafi", "shafii", "maliki", "hanbali", "jafari")

    # --- Retrieval ----------------------------------------------------
    retrieval_limit: int = 6
    min_citation_coverage: float = 0.55

    # --- LLM ----------------------------------------------------------
    anthropic_api_key: str | None = Field(default=None, repr=False)
    llm_model: str = "claude-sonnet-5"
    llm_max_tokens: int = 1500

    # --- Voice --------------------------------------------------------
    stt_provider: str = "none"
    tts_provider: str = "none"
    elevenlabs_api_key: str | None = Field(default=None, repr=False)

    # --- CORS ---------------------------------------------------------
    cors_origins: tuple[str, ...] = ("http://localhost:8100", "http://127.0.0.1:8100")

    @property
    def llm_configured(self) -> bool:
        return bool(self.anthropic_api_key)


@lru_cache
def get_settings() -> Settings:
    return Settings()
