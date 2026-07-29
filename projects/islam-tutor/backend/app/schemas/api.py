"""Pydantic-Contracts an den API-Grenzen.

Verfassung 8.1: Inputs werden an Systemgrenzen validiert. Jeder Endpoint hat ein
explizites Request- und Response-Modell — keine rohen dicts nach aussen.
"""
from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

Madhhab = Literal["hanafi", "shafii", "maliki", "hanbali", "jafari"]
Language = Literal["de", "en", "tr"]
Provenance = Literal["verified", "scholar_review_pending", "disputed"]


# --------------------------------------------------------------------------
# Chat
# --------------------------------------------------------------------------

class ChatRequest(BaseModel):
    message: str = Field(min_length=1, max_length=2000, description="Frage des Lernenden")
    madhhab: Madhhab | None = Field(
        default=None,
        description=(
            "Rechtsschule des Nutzers. Ohne Angabe zeigt das System alle Varianten — "
            "es waehlt keine aus."
        ),
    )
    language: Language = "de"
    limit: int = Field(default=6, ge=1, le=12, description="Maximale Zahl abgerufener Passagen")
    include_trace: bool = Field(
        default=False,
        description="Nachvollziehbarkeit des Antwortpfads mitliefern. Fuer Debugging und Audit.",
    )


class CitationOut(BaseModel):
    chunk_id: str
    title: str
    module: str
    source_ids: list[str]
    provenance: str
    deep_link: str | None = None
    madhhab: str = "common"


class TraceOut(BaseModel):
    stage: str
    outcome: str
    detail: str = ""


class NoticesOut(BaseModel):
    review_pending: bool = False
    disputed: bool = False


class ChatResponse(BaseModel):
    text: str
    citations: list[CitationOut] = Field(default_factory=list)
    category: str
    generator: str
    blocked: bool = False
    block_reason: str | None = None
    notices: NoticesOut = Field(default_factory=NoticesOut)
    madhhab: str | None = None
    trace: list[TraceOut] | None = None
    timestamp: str

    model_config = {
        "json_schema_extra": {
            "description": (
                "Antwort des Lern-Tutors. Das Feld 'blocked' ist true, wenn die Anfrage "
                "ein religioeses Rechtsurteil verlangte oder die Ausgabe die Content "
                "Policy verletzt haette. In diesem Fall enthaelt 'text' eine Erklaerung "
                "und einen Verweis, keine Antwort auf die Rechtsfrage."
            )
        }
    }


# --------------------------------------------------------------------------
# Wissen
# --------------------------------------------------------------------------

class PrayerSummary(BaseModel):
    id: str
    order: int | None = None
    name_arabic: str | None = None
    name_transliteration: str | None = None
    name_local: str | None = None
    fard_rakat: int | None = None
    step_count: int = 0
    provenance: str


class PurificationSummary(BaseModel):
    id: str
    name_arabic: str | None = None
    name_transliteration: str | None = None
    name_local: str | None = None
    step_count: int = 0
    provenance: str


class SurahSummary(BaseModel):
    id: str
    number: int | None = None
    name_arabic: str | None = None
    name_transliteration: str | None = None
    name_local: str | None = None
    ayah_count: int | None = None
    provenance: str
    audio_available: bool = False


class ContentStatusResponse(BaseModel):
    totals: dict[str, int]
    by_module: dict[str, dict[str, int]]
    verified_share: float
    review_pending_share: float
    note: str


class SourceEntry(BaseModel):
    id: str
    type: str
    title: str
    publisher: str | None = None
    translator: str | None = None
    url: str | None = None
    language: str | None = None
    license: str | None = None
    license_status: str | None = None
    imported: bool = False
    note: str | None = None
    provenance_ceiling: str | None = None
    checksum_required: bool | None = None
    import_script: str | None = None


class SourcesResponse(BaseModel):
    version: str | None = None
    updated: str | None = None
    sources: list[SourceEntry]
    planned_sources: list[dict] = Field(default_factory=list)
    rules: list[str] = Field(default_factory=list)


# --------------------------------------------------------------------------
# Lernplan
# --------------------------------------------------------------------------

class LearningPlanRequest(BaseModel):
    goal: Literal["learn_to_pray", "learn_arabic_script", "memorize_fatiha", "learn_purification"]
    minutes_per_day: int = Field(default=15, ge=5, le=120)
    madhhab: Madhhab | None = None
    language: Language = "de"
    prior_knowledge: Literal["none", "some", "solid"] = "none"


class PlanStep(BaseModel):
    day: int
    title: str
    focus: str
    module: str
    deep_link: str | None = None
    estimated_minutes: int
    practice: str | None = None


class LearningPlanResponse(BaseModel):
    goal: str
    total_days: int
    minutes_per_day: int
    steps: list[PlanStep]
    madhhab: str | None = None
    note: str


# --------------------------------------------------------------------------
# Voice
# --------------------------------------------------------------------------

class TranscribeResponse(BaseModel):
    text: str
    language: str | None = None
    provider: str
    confidence: float | None = None
    available: bool = True
    message: str | None = None


class SynthesizeRequest(BaseModel):
    text: str = Field(min_length=1, max_length=5000)
    language: Language = "de"
    voice: str | None = None
    kind: Literal["instruction", "translation", "pronunciation"] = "instruction"


class SynthesizeResponse(BaseModel):
    audio_base64: str | None = None
    mime_type: str | None = None
    provider: str
    available: bool = True
    rejected: bool = False
    rejection_reason: str | None = None


# --------------------------------------------------------------------------
# System
# --------------------------------------------------------------------------

class HealthResponse(BaseModel):
    status: Literal["ok", "degraded"]
    version: str
    chunks_indexed: int
    generator: str
    llm_configured: bool
    knowledge_modules: list[str]


class ErrorResponse(BaseModel):
    detail: str
    code: str | None = None
