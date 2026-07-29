# Islam Tutor AI

**Status:** Phase 1 — Foundation
**Parent:** Genesis Harness
**Version:** 0.1.0
**Last updated:** 2026-07-29

Eine moderne, interaktive Lernplattform für Muslime und alle, die den Islam lernen möchten.

---

## Was dieses System ist

Ein **Lernwerkzeug**. Es erklärt, übt ab, strukturiert Lernpfade und zeigt immer die Quelle,
aus der eine Information stammt.

## Was dieses System nicht ist

Es ist **kein religiöses Urteilssystem**. Es erteilt keine Fatwas, entscheidet keine
Rechtsfragen und ersetzt keine Gelehrten. Wo Meinungen der Rechtsschulen abweichen,
zeigt es die Unterschiede — es wählt nicht aus.

Die vollständigen Regeln stehen in [`docs/CONTENT_POLICY.md`](docs/CONTENT_POLICY.md).
Diese Datei ist für dieses Projekt bindend und hat Vorrang vor Feature-Wünschen.

---

## Module

| Modul | Verzeichnis | Zweck |
|---|---|---|
| **AI Tutor** | `ai/tutor/` | Chat, Lernpläne, Erklärungen — RAG-basiert mit Quellenpflicht |
| **RAG Engine** | `ai/rag/` | Chunking, Embedding, Retrieval über die Wissensbasis |
| **Namaz Trainer** | `knowledge/prayer/` | Gebetsabläufe, Bewegungen, Texte, Übersetzungen |
| **Wudu / Ghusl** | `knowledge/purification/` | Interaktive Lektionen zur rituellen Reinigung |
| **Arabic Learning** | `knowledge/arabic/` | Buchstaben, Aussprache, Lesen, Koranarabisch |
| **Voice** | `voice/` | STT/TTS mit austauschbaren Providern |
| **Backend** | `backend/` | FastAPI, Auth, Progress-Tracking |
| **Frontend** | `frontend/` | Lern-UI |

---

## Verzeichnisstruktur

```
islam-tutor/
├── frontend/          Lern-UI (HTML/JS, Single-Page)
├── backend/           FastAPI-Service
│   └── app/
│       ├── api/routes/    HTTP-Endpoints
│       ├── core/          Config, Security
│       ├── models/        DB-Modelle
│       ├── schemas/       Pydantic-Contracts
│       └── services/      Geschäftslogik
├── ai/
│   ├── rag/           Retrieval-Pipeline
│   ├── tutor/         Tutor-Engine
│   ├── prompts/       System-Prompts (versioniert)
│   ├── guardrails/    Content-Policy als Code
│   └── evaluation/    Qualitätsmessung der Antworten
├── knowledge/
│   ├── schema/        JSON-Schemas für alle Inhaltstypen
│   ├── sources/       Quellenregister mit Provenance
│   ├── quran/         Koran-Texte + Übersetzungen
│   ├── prayer/        Gebetsabläufe je Gebet und Rechtsschule
│   ├── purification/  Wudu / Ghusl / Tayammum
│   └── arabic/        Alphabet, Tajwid-Grundlagen, Vokabular
├── voice/
│   ├── stt/           Speech-to-Text
│   ├── tts/           Text-to-Speech
│   └── providers/     Whisper, ElevenLabs, lokale Modelle
├── agents/            Projektbezogene Agenten-Definitionen
├── configs/           Agent-Registry, MCP-Config, Settings
├── assets/            Icons, Animationen, Audio
├── docs/              Architektur, Policy, ADRs
├── tests/             Unit + Integration
└── scripts/           Ingest, Verify, Build
```

---

## Schnellstart

```bash
# Backend
cd backend
pip install -e ".[dev]"
uvicorn app.main:app --reload --port 8100

# Wissensbasis validieren (prüft Schema + Quellenangaben)
python scripts/verify_knowledge.py

# Tests
pytest tests/ -v
```

---

## Dokumentation

| Dokument | Inhalt |
|---|---|
| [`docs/CONTENT_POLICY.md`](docs/CONTENT_POLICY.md) | **Bindende Regeln für religiöse Inhalte** |
| [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) | Systemaufbau, Datenfluss, Grenzen |
| [`docs/AGENTS.md`](docs/AGENTS.md) | Agenten-Roster und Zuständigkeiten |
| [`docs/KNOWLEDGE_MODEL.md`](docs/KNOWLEDGE_MODEL.md) | Datenmodell der Wissensbasis |
| [`docs/STATUS.md`](docs/STATUS.md) | Aktueller Stand, was fehlt |
| [`CHANGELOG.md`](CHANGELOG.md) | Änderungshistorie |
| [`docs/adr/`](docs/adr/) | Architekturentscheidungen |

---

## Beziehung zu Genesis Harness

Islam Tutor AI ist ein **Child Project** unter `Genesis_Harness/projects/`. Es erbt:

- die Verfassung aus `Genesis_Harness/CLAUDE.md`
- den MCP-Layer (Filesystem, GitHub, Browser Research, AI Models)
- die Logging- und Session-Disziplin

Es hat **eigene** Agenten, eigene Content-Policy und eigene Qualitätsschwellen, weil der
Inhaltsbereich religiös sensibel ist und strengere Regeln braucht als generische Software.
