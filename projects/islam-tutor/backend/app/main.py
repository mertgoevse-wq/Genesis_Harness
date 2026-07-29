"""FastAPI-Anwendung — Islam Tutor AI.

Alle Wissens-Endpoints gehen ueber KnowledgeService, damit der Provenance-Filter
an genau einer Stelle greift. Keine Route liest eine Datei direkt.

Start:
    uvicorn backend.app.main:app --reload --port 8100
"""
from __future__ import annotations

import base64
from contextlib import asynccontextmanager
from typing import Annotated, Literal

from fastapi import Depends, FastAPI, HTTPException, Query, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles

from ai.tutor.engine import TutorEngine
from ai.tutor.learning_plan import generate_plan
from backend.app.core.config import Settings, get_settings
from backend.app.schemas.api import (
    ChatRequest,
    ChatResponse,
    ContentStatusResponse,
    HealthResponse,
    LearningPlanRequest,
    LearningPlanResponse,
    PrayerSummary,
    PurificationSummary,
    SourcesResponse,
    SurahSummary,
    SynthesizeRequest,
    SynthesizeResponse,
    TranscribeResponse,
)
from backend.app.services.knowledge_service import (
    KnowledgeBlocked,
    KnowledgeNotFound,
    KnowledgeService,
)
from voice.registry import get_stt_provider, get_tts_provider

_engine: TutorEngine | None = None
_knowledge: KnowledgeService | None = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Baut den Index beim Start, nicht beim ersten Request.

    Ein kalter erster Request, der den ganzen Index baut, waere eine unnoetig
    schlechte erste Erfahrung. Der Index ist klein genug, dass das den Start
    nicht merkbar verzoegert.
    """
    global _engine, _knowledge
    settings = get_settings()
    _knowledge = KnowledgeService(settings.knowledge_dir)
    _engine = TutorEngine(knowledge_dir=settings.knowledge_dir)
    count = _engine.warmup()
    app.state.chunks_indexed = count
    yield
    _engine = None
    _knowledge = None


settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    lifespan=lifespan,
    description=(
        "Interaktive Lernplattform für islamisches Wissen und Arabisch.\n\n"
        "**Dieses System ist eine Lernhilfe, kein religiöses Urteilssystem.** Es erteilt "
        "keine Fatwas, beurteilt keine Einzelfälle und bevorzugt keine Rechtsschule. "
        "Jede Antwort führt ihre Quellen mit. Die bindenden Regeln stehen in "
        "`docs/CONTENT_POLICY.md`."
    ),
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=list(settings.cors_origins),
    allow_credentials=False,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)


# --------------------------------------------------------------------------
# Abhaengigkeiten
# --------------------------------------------------------------------------

def get_engine() -> TutorEngine:
    if _engine is None:  # pragma: no cover - nur bei Fehlkonfiguration
        raise HTTPException(status_code=503, detail="Tutor-Engine nicht initialisiert.")
    return _engine


def get_knowledge() -> KnowledgeService:
    if _knowledge is None:  # pragma: no cover
        raise HTTPException(status_code=503, detail="Knowledge-Service nicht initialisiert.")
    return _knowledge


SettingsDep = Annotated[Settings, Depends(get_settings)]
EngineDep = Annotated[TutorEngine, Depends(get_engine)]
KnowledgeDep = Annotated[KnowledgeService, Depends(get_knowledge)]

MadhhabQuery = Annotated[
    Literal["hanafi", "shafii", "maliki", "hanbali", "jafari"] | None,
    Query(description="Rechtsschule. Ohne Angabe werden alle Varianten gezeigt."),
]
LanguageQuery = Annotated[Literal["de", "en", "tr"], Query(description="Anzeigesprache")]


# --------------------------------------------------------------------------
# Fehlerbehandlung
# --------------------------------------------------------------------------

@app.exception_handler(KnowledgeNotFound)
async def handle_not_found(request: Request, exc: KnowledgeNotFound) -> JSONResponse:
    return JSONResponse(status_code=404, content={"detail": str(exc), "code": "not_found"})


@app.exception_handler(KnowledgeBlocked)
async def handle_blocked(request: Request, exc: KnowledgeBlocked) -> JSONResponse:
    # 409 statt 404: der Inhalt existiert, ist aber bewusst nicht auslieferbar.
    # Diese Unterscheidung ist fuer Betreiber wichtig — sie zeigt eine Luecke
    # in der Wissensbasis, nicht einen falschen Pfad.
    return JSONResponse(status_code=409, content={"detail": str(exc), "code": "content_blocked"})


# --------------------------------------------------------------------------
# System
# --------------------------------------------------------------------------

@app.get("/health", response_model=HealthResponse, tags=["system"])
async def health(engine: EngineDep, config: SettingsDep) -> HealthResponse:
    modules = [
        path.name
        for path in sorted(config.knowledge_dir.iterdir())
        if path.is_dir() and path.name not in ("schema", "sources")
    ]
    return HealthResponse(
        status="ok" if engine.retriever.chunk_count > 0 else "degraded",
        version=config.version,
        chunks_indexed=engine.retriever.chunk_count,
        generator=engine.generator.name,
        llm_configured=config.llm_configured,
        knowledge_modules=modules,
    )


@app.get("/api/v1/sources", response_model=SourcesResponse, tags=["transparenz"])
async def sources(knowledge: KnowledgeDep) -> SourcesResponse:
    """Oeffentliches Quellenregister.

    Content Policy 10.2: die Quellenauswahl ist transparent, weil sie eine
    menschliche Entscheidung mit Perspektive ist.
    """
    return SourcesResponse(**knowledge.get_sources())


@app.get("/api/v1/content-status", response_model=ContentStatusResponse, tags=["transparenz"])
async def content_status(knowledge: KnowledgeDep) -> ContentStatusResponse:
    """Ehrlicher Reifegrad der Wissensbasis: was ist geprueft, was nicht."""
    return ContentStatusResponse(**knowledge.content_status())


# --------------------------------------------------------------------------
# Tutor
# --------------------------------------------------------------------------

@app.post("/api/v1/chat", response_model=ChatResponse, tags=["tutor"])
async def chat(payload: ChatRequest, engine: EngineDep) -> ChatResponse:
    """Frage an den Lern-Tutor.

    Die Antwort laeuft durch fuenf Stationen: Vorpruefung, Retrieval, Generierung,
    Zitatpruefung, Nachpruefung. Verlangt die Anfrage ein Rechtsurteil, wird sie
    nicht beantwortet, sondern mit Lehrinhalt und Verweis umgeleitet —
    `blocked` ist dann true.
    """
    answer = engine.answer(
        payload.message,
        madhhab=payload.madhhab,
        language=payload.language,
        limit=payload.limit,
    )
    data = answer.to_dict()
    if not payload.include_trace:
        data.pop("trace", None)
    return ChatResponse(**data)


@app.post("/api/v1/learning-plan", response_model=LearningPlanResponse, tags=["tutor"])
async def learning_plan(payload: LearningPlanRequest) -> LearningPlanResponse:
    """Erzeugt einen Lernplan.

    Regelbasiert, nicht LLM-generiert: die didaktische Reihenfolge hat
    Abhaengigkeiten, die sich nicht pro Anfrage aendern sollten.
    """
    try:
        plan = generate_plan(
            payload.goal,
            minutes_per_day=payload.minutes_per_day,
            madhhab=payload.madhhab,
            prior_knowledge=payload.prior_knowledge,
            language=payload.language,
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc

    return LearningPlanResponse(
        goal=plan.goal,
        total_days=plan.total_days,
        minutes_per_day=plan.minutes_per_day,
        steps=[step.__dict__ for step in plan.steps],
        madhhab=plan.madhhab,
        note=plan.note,
    )


# --------------------------------------------------------------------------
# Gebet
# --------------------------------------------------------------------------

@app.get("/api/v1/prayer", response_model=list[PrayerSummary], tags=["gebet"])
async def list_prayers(knowledge: KnowledgeDep, language: LanguageQuery = "de") -> list[PrayerSummary]:
    return [PrayerSummary(**item) for item in knowledge.list_prayers(language=language)]


@app.get("/api/v1/prayer/movements", tags=["gebet"])
async def list_movements(
    knowledge: KnowledgeDep, madhhab: MadhhabQuery = None, language: LanguageQuery = "de"
) -> dict:
    movements = knowledge.list_movements(madhhab=madhhab, language=language)
    return {"count": len(movements), "movements": movements}


@app.get("/api/v1/prayer/{prayer_id}", tags=["gebet"])
async def get_prayer(
    prayer_id: Literal["fajr", "dhuhr", "asr", "maghrib", "isha"],
    knowledge: KnowledgeDep,
    madhhab: MadhhabQuery = None,
    language: LanguageQuery = "de",
) -> dict:
    """Vollstaendiger Gebetsablauf mit aufgeloesten Bewegungen und Texten."""
    return knowledge.get_prayer(prayer_id, madhhab=madhhab, language=language)


# --------------------------------------------------------------------------
# Reinigung
# --------------------------------------------------------------------------

@app.get("/api/v1/purification", response_model=list[PurificationSummary], tags=["reinigung"])
async def list_purification(
    knowledge: KnowledgeDep, language: LanguageQuery = "de"
) -> list[PurificationSummary]:
    return [PurificationSummary(**item) for item in knowledge.list_purification(language=language)]


@app.get("/api/v1/purification/{kind}", tags=["reinigung"])
async def get_purification(
    kind: Literal["wudu", "ghusl", "tayammum"],
    knowledge: KnowledgeDep,
    madhhab: MadhhabQuery = None,
    language: LanguageQuery = "de",
) -> dict:
    return knowledge.get_purification(kind, madhhab=madhhab, language=language)


# --------------------------------------------------------------------------
# Arabisch
# --------------------------------------------------------------------------

@app.get("/api/v1/arabic/alphabet", tags=["arabisch"])
async def alphabet(knowledge: KnowledgeDep, language: LanguageQuery = "de") -> dict:
    return knowledge.get_alphabet(language=language)


@app.get("/api/v1/arabic/curriculum", tags=["arabisch"])
async def curriculum(knowledge: KnowledgeDep, language: LanguageQuery = "de") -> dict:
    units = knowledge.get_curriculum(language=language)
    return {"count": len(units), "units": units}


@app.get("/api/v1/arabic/letter/{letter_id}", tags=["arabisch"])
async def letter(letter_id: str, knowledge: KnowledgeDep, language: LanguageQuery = "de") -> dict:
    return knowledge.get_letter(letter_id, language=language)


# --------------------------------------------------------------------------
# Koran
# --------------------------------------------------------------------------

@app.get("/api/v1/quran", response_model=list[SurahSummary], tags=["koran"])
async def list_surahs(knowledge: KnowledgeDep, language: LanguageQuery = "de") -> list[SurahSummary]:
    return [SurahSummary(**item) for item in knowledge.list_surahs(language=language)]


@app.get("/api/v1/quran/{number}", tags=["koran"])
async def get_surah(
    number: Annotated[int, Query(ge=1, le=114)],
    knowledge: KnowledgeDep,
    language: LanguageQuery = "de",
) -> dict:
    return knowledge.get_surah(number, language=language)


# --------------------------------------------------------------------------
# Voice
# --------------------------------------------------------------------------

@app.post("/api/v1/voice/transcribe", response_model=TranscribeResponse, tags=["voice"])
async def transcribe(config: SettingsDep) -> TranscribeResponse:
    """Sprache zu Text.

    In Phase 4 ist die Provider-Abstraktion vorhanden, aber kein Provider
    angebunden. Der Endpoint sagt das ehrlich statt einen Fehler zu werfen.
    """
    provider = get_stt_provider(config.stt_provider)
    if not provider.available:
        return TranscribeResponse(
            text="",
            provider=provider.name,
            available=False,
            message=(
                "Kein Speech-to-Text-Provider konfiguriert. Die Abstraktion ist vorhanden; "
                "setze ISLAM_TUTOR_STT_PROVIDER auf 'whisper_local' oder 'whisper_api'."
            ),
        )
    raise HTTPException(status_code=501, detail="Audio-Upload ist noch nicht implementiert.")


@app.post("/api/v1/voice/synthesize", response_model=SynthesizeResponse, tags=["voice"])
async def synthesize(payload: SynthesizeRequest, config: SettingsDep) -> SynthesizeResponse:
    """Text zu Sprache.

    Arabischer Korantext wird abgelehnt. ADR-0002: Rezitation kommt von
    menschlichen Rezitatoren, nicht aus Sprachsynthese.
    """
    provider = get_tts_provider(config.tts_provider)
    result = provider.synthesize(payload.text, language=payload.language, kind=payload.kind)

    if result.rejected:
        return SynthesizeResponse(
            provider=provider.name,
            available=provider.available,
            rejected=True,
            rejection_reason=result.rejection_reason,
        )
    if not provider.available:
        return SynthesizeResponse(
            provider=provider.name,
            available=False,
            rejection_reason=(
                "Kein Text-to-Speech-Provider konfiguriert. Setze "
                "ISLAM_TUTOR_TTS_PROVIDER auf 'elevenlabs' oder 'system'."
            ),
        )
    return SynthesizeResponse(
        audio_base64=base64.b64encode(result.audio).decode() if result.audio else None,
        mime_type=result.mime_type,
        provider=provider.name,
    )


# --------------------------------------------------------------------------
# Frontend
# --------------------------------------------------------------------------

if settings.frontend_dir.exists():
    app.mount(
        "/static",
        StaticFiles(directory=str(settings.frontend_dir)),
        name="static",
    )

    @app.get("/", include_in_schema=False)
    async def index() -> FileResponse:
        return FileResponse(settings.frontend_dir / "index.html")
