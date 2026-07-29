# Architektur — Islam Tutor AI

**Version:** 0.1.0
**Datum:** 2026-07-29
**Status:** Phase 1 (Foundation)

---

## 1. Systemüberblick

```
┌──────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  Chat  ·  Namaz-Trainer  ·  Wudu  ·  Arabisch  ·  Profil     │
└───────────────────────────┬──────────────────────────────────┘
                            │ HTTP / JSON
┌───────────────────────────▼──────────────────────────────────┐
│                     BACKEND (FastAPI)                        │
│  /chat  /prayer  /purification  /arabic  /progress  /voice   │
└───┬──────────────┬──────────────┬─────────────┬──────────────┘
    │              │              │             │
    ▼              ▼              ▼             ▼
┌────────┐  ┌────────────┐  ┌──────────┐  ┌─────────┐
│ TUTOR  │  │ KNOWLEDGE  │  │ PROGRESS │  │  VOICE  │
│ ENGINE │  │  SERVICE   │  │ SERVICE  │  │ SERVICE │
└───┬────┘  └─────┬──────┘  └────┬─────┘  └────┬────┘
    │             │              │             │
    ▼             ▼              ▼             ▼
┌─────────────────────────┐  ┌──────┐  ┌──────────────┐
│      RAG PIPELINE       │  │  DB  │  │ STT/TTS      │
│  Retrieve → Rerank      │  │      │  │ Provider-    │
│  → Assemble → Cite      │  │      │  │ Abstraktion  │
└──────────┬──────────────┘  └──────┘  └──────────────┘
           │
    ┌──────▼───────┐        ┌──────────────────┐
    │ VECTOR STORE │        │    GUARDRAILS    │
    │  + KNOWLEDGE │◄───────┤ Policy · Citation│
    │     BASE     │        │ Provenance-Filter│
    └──────────────┘        └──────────────────┘
```

### Der entscheidende Pfad

Jede Tutor-Antwort läuft durch **fünf** Stationen. Keine darf übersprungen werden:

```
Nutzerfrage
   │
   ├─1─► PRE-GUARD      Ist das eine Rechtsfrage? Eine Fatwa-Anfrage?
   │                    → wenn ja: Lehrantwort + Verweis, keine Generierung
   │
   ├─2─► RETRIEVAL      Suche in der Wissensbasis, gefiltert auf
   │                    provenance ∈ {verified, scholar_review_pending, disputed}
   │                    und auf das Madhhab des Nutzers
   │
   ├─3─► GENERATION     LLM erhält NUR die abgerufenen Passagen als Grundlage.
   │                    Leeres Retrieval ⇒ Antwort "keine belegte Information",
   │                    nicht Generierung aus Modellwissen.
   │
   ├─4─► CITATION CHECK Jede inhaltliche Aussage muss auf eine abgerufene
   │                    Quelle zurückführbar sein. Sonst: Rückweisung.
   │
   └─5─► POST-GUARD     Enthält die Antwort ein Urteil? Ein unbelegtes Zitat?
                        Eine erfundene Hadith-Referenz? → Abbruch.
```

Die Guardrails sind **kein Prompt**, sondern Code. Ein Prompt kann umgangen werden;
ein Filter, der auf fehlende `source_id` prüft, nicht.

---

## 2. Subsysteme

### 2.1 Knowledge Layer (`knowledge/`)

Die Wissensbasis ist **dateibasiert und versioniert** — JSON, kein CMS. Begründung:

- Inhalte sind religiös sensibel und müssen im Git-Diff überprüfbar sein.
- Ein Reviewer soll eine Änderung als Pull Request lesen können.
- Kein stiller Content-Drift durch Datenbank-Edits.

```
knowledge/
├── schema/            JSON-Schema pro Inhaltstyp — Validierung im CI
├── sources/
│   └── registry.json  Whitelist erlaubter Quellen + Lizenz + Prüfsumme
├── quran/             surah_NNN.json — Arabisch, Transliteration, Übersetzungen
├── prayer/            fajr.json, dhuhr.json, … + movements.json
├── purification/      wudu.json, ghusl.json, tayammum.json
└── arabic/            alphabet.json, tajwid.json, vocabulary.json
```

**Invariante:** Jeder Datensatz hat `id`, `provenance`, `sources[]`, `madhhab`.
Ein Datensatz ohne diese Felder validiert nicht und wird nicht geladen.

### 2.2 RAG Pipeline (`ai/rag/`)

| Stufe | Datei | Aufgabe |
|---|---|---|
| Chunking | `chunker.py` | Typspezifisch: Ayah-Ebene für Koran, Schritt-Ebene für Fiqh, Lektion-Ebene für Arabisch |
| Embedding | `embedder.py` | Provider-Abstraktion; Cache auf Disk, weil Inhalte selten ändern |
| Store | `vector_store.py` | Interface + In-Memory/SQLite-Implementierung, austauschbar gegen pgvector/Qdrant |
| Retrieval | `retriever.py` | Hybrid: semantisch + Schlagwort; Filter auf Madhhab und Provenance |
| Assembly | `context_builder.py` | Baut den Kontext und die Zitatliste, die der Generator sehen darf |

**Warum kein Chunking über Ayah-Grenzen hinweg:** Ein halber Vers ist kein Vers. Die
Chunk-Grenze folgt der inhaltlichen Einheit, nicht einer Token-Zahl.

### 2.3 Tutor Engine (`ai/tutor/`)

| Datei | Aufgabe |
|---|---|
| `engine.py` | Orchestriert die 5 Stationen des Antwortpfads |
| `learning_plan.py` | Generiert Lernpläne aus Zielen + aktuellem Stand |
| `spaced_repetition.py` | SM-2-ähnlicher Wiederholungsalgorithmus für Memorierung |
| `session.py` | Gesprächszustand, Themenverlauf, Schleifenerkennung |

### 2.4 Guardrails (`ai/guardrails/`)

| Datei | Aufgabe |
|---|---|
| `policy.py` | Klassifiziert Anfragen; blockiert Fatwa-/Urteilsanfragen |
| `citation_check.py` | Verifiziert, dass jede Aussage eine Quelle hat |
| `provenance_filter.py` | Entfernt `placeholder`-Inhalte aus jedem Retrieval-Ergebnis |
| `loop_detector.py` | Erkennt Skrupulositäts-Schleifen und unterbricht sie |

### 2.5 Voice (`voice/`)

Provider-Abstraktion nach demselben Muster wie `live_intelligence` im Elternprojekt:
Abstract Base Class, konkrete Provider, Fallback.

```
VoiceProvider (ABC)
├── transcribe(audio) → Transcript
└── synthesize(text, voice) → AudioResult

Implementierungen:
├── WhisperLocalProvider     lokal, offline, kostenlos
├── WhisperAPIProvider       OpenAI Whisper API
├── ElevenLabsProvider       TTS, hohe Qualität
└── SystemTTSProvider        Browser-native Fallback
```

**Sonderfall Koranrezitation:** TTS wird **nicht** für arabischen Korantext verwendet.
Rezitation ist eine Kunstform mit Tajwid-Regeln; synthetische Stimmen erzeugen dabei
falsche Aussprache. Stattdessen: Audio registrierter Rezitatoren aus `voice/audio_assets/`,
mit Quellenangabe. Siehe ADR-0002.

### 2.6 Backend (`backend/`)

FastAPI, async, Pydantic-Contracts an jeder Grenze.

```
POST /api/v1/chat                 Tutor-Frage
GET  /api/v1/prayer               Liste der Gebete
GET  /api/v1/prayer/{name}        Ablauf eines Gebets (madhhab-gefiltert)
GET  /api/v1/purification/{type}  wudu | ghusl | tayammum
GET  /api/v1/arabic/alphabet      Buchstaben mit Formen und Aussprache
GET  /api/v1/arabic/lessons       Lektionsliste
POST /api/v1/progress             Lernfortschritt speichern
GET  /api/v1/progress             Lernstand abrufen
POST /api/v1/learning-plan        Lernplan generieren
POST /api/v1/voice/transcribe     Audio → Text
POST /api/v1/voice/synthesize     Text → Audio
GET  /api/v1/sources              Quellenregister (Transparenz-Endpoint)
GET  /health
```

Der Endpoint `/api/v1/sources` ist bewusst öffentlich: Nutzer sollen prüfen können,
woher das System sein Wissen hat.

---

## 3. Datenfluss: Beispiel „Wie bete ich Fajr?"

```
1. Frontend  → POST /api/v1/chat  {"message": "Wie bete ich Fajr?",
                                    "madhhab": "hanafi"}
2. PRE-GUARD  → Kategorie: LEARNING_QUESTION. Kein Urteil verlangt. Pass.
3. RETRIEVAL  → Query-Embedding; Filter madhhab ∈ {hanafi, common},
                provenance ≠ placeholder
              → Treffer: prayer/fajr.json#rakat, prayer/movements.json#qiyam …
4. ASSEMBLY   → Kontext mit 6 Passagen, jede mit source_id
5. GENERATION → LLM erklärt den Ablauf, ausschließlich auf Basis der 6 Passagen
6. CITATION   → 4 Aussagen, 4 source_ids vorhanden. Pass.
7. POST-GUARD → Kein Urteil, kein unbelegtes Zitat. Pass.
8. Response   → Text + citations[] + madhhab_note + deep_link zum Namaz-Trainer
```

Wenn Schritt 3 leer zurückkommt, endet der Pfad bei Schritt 3 mit:
„Zu dieser Frage habe ich keinen belegten Inhalt in meiner Wissensbasis."
Es folgt **keine** Generierung.

---

## 4. Technologieentscheidungen

| Bereich | Wahl | Begründung |
|---|---|---|
| Backend | FastAPI + Pydantic | Async, Schema-Validierung an der Grenze, passt zum Elternprojekt |
| Wissensbasis | JSON-Dateien in Git | Reviewbar, diffbar, kein stiller Content-Drift |
| Vector Store | Interface + SQLite-Start | Kein Infrastruktur-Zwang in Phase 1; austauschbar |
| Embeddings | Provider-Abstraktion | Lokale Modelle möglich, keine Anbieterbindung |
| Frontend | Vanilla JS, Single-File | Kein Build-Schritt in Phase 1; ersetzbar durch React |
| DB | SQLite → PostgreSQL | Fortschritt/Profil; Migrationspfad über SQLAlchemy |
| Voice | ABC + Provider | Whisper/ElevenLabs/lokal ohne Codeänderung tauschbar |
| Arabische Schrift | Unicode + Web-Font | Keine Bilder, damit Text kopierbar und screenreader-fähig bleibt |

---

## 5. Invarianten

Aussagen, die immer gelten müssen. Verletzung ist ein CRITICAL-Bug.

1. Kein `placeholder`-Inhalt verlässt das Backend.
2. Keine Tutor-Antwort ohne mindestens eine `source_id` oder einen expliziten
   „keine belegte Information"-Hinweis.
3. Arabischer Korantext wird nie vom LLM erzeugt — nur aus `knowledge/quran/` gelesen.
4. Ein Hadith ohne `collection` + `reference` + `grading` wird nicht ausgeliefert.
5. Madhhab-abhängige Inhalte werden nie ohne Madhhab-Kennzeichnung angezeigt.
6. Religionszugehörigkeit und Madhhab verlassen die Datenbank nie.

---

## 6. Was Phase 1 noch nicht enthält

Ehrliche Abgrenzung — diese Punkte sind geplant, nicht gebaut:

- Vollständiger Korantext (nur Al-Fatiha + Struktur als Referenzimplementierung)
- Fachliche Prüfung durch Gelehrte (alle Fiqh-Inhalte: `scholar_review_pending`)
- Echte Embeddings (Interface steht, Provider noch nicht angebunden)
- Animationen für Gebetsbewegungen (Datenmodell steht, Assets fehlen)
- Rezitations-Audio (Verzeichnis + Manifest-Schema steht, Dateien fehlen)
- Auth und Multi-User (Progress-Service arbeitet lokal)
