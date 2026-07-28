# Genesis OS — Konkreter Entwicklungsplan

**Version:** 1.0
**Datum:** 2026-07-28
**Grundlage:** Architektur-Audit vom selben Tag
**Optimiert für:** Maximale Wirkung bei minimalem Aufwand

---

## Leitprinzip

Jede Phase muss ein **lauffähiges, testbares, demonstrierbares Delta** produzieren.
Kein Code ohne Test, kein Modul ohne Nutzer-sichtbare Wirkung.

---

## Phase 1 — Chirurgische Konsolidierung

**Ziel:** Aus 60+ Fragmenten ein installierbares, lauffähiges Python-Package machen.
Kein neuer Code — nur Aufräumen, Zusammenführen, Lauffähig-Machen.

**Warum wichtig:** Ohne das kann nichts getestet, nichts deployed, nichts importiert werden.
31 Commits, und das Projekt hat keinen Entry-Point und keine Dependencies.

### Dateien/Systeme betroffen

**Neue Struktur** (12 Module statt 60+):

```
genesis/
├── __init__.py
├── __main__.py                  # CLI Entry-Point
├── config.py                    # Zentrale Settings (Pydantic BaseSettings)
│
├── decision/                    # ← venture_decision + product_validation_engine (zusammengeführt)
│   ├── __init__.py
│   ├── engine.py                # ← venture_decision/decision_engine.py
│   ├── validation.py            # ← product_validation_engine/validation_engine.py
│   ├── scoring.py               # ← product_validation_engine/scoring.py
│   └── scorers/                 # ← venture_decision/scoring/ (unverändert)
│       ├── market.py
│       ├── competition.py
│       ├── technical.py
│       └── risk.py
│
├── intelligence/                # ← opportunity_intelligence + live_intelligence (zusammengeführt)
│   ├── __init__.py
│   ├── opportunity.py           # ← opportunity_intelligence/opportunity_detector.py
│   ├── discovery/               # ← opportunity_intelligence/discovery/ (unverändert)
│   │   ├── market_research.py
│   │   ├── trend_monitor.py
│   │   └── competitor_analyzer.py
│   └── connectors/              # ← live_intelligence/ (base.py + connectors/)
│       ├── base.py
│       ├── market_data.py
│       ├── saas_trends.py
│       ├── github_signals.py
│       └── startup_signals.py
│
├── revenue/                     # ← revenue_intelligence (unverändert, nur verschoben)
│   ├── __init__.py
│   ├── pricing.py
│   ├── subscriptions.py
│   ├── acquisition.py
│   └── experiments.py
│
├── growth/                      # ← growth_intelligence + customer_intelligence (zusammengeführt)
│   ├── __init__.py
│   ├── engine.py                # ← growth_intelligence/growth_engine.py
│   ├── customer.py              # ← customer_intelligence/customer_intelligence_engine.py
│   └── validation_loop.py       # ← validation_engine/validation_loop.py
│
├── builder/                     # ← mvp_builder + deployment_intelligence (zusammengeführt)
│   ├── __init__.py
│   ├── mvp.py                   # ← mvp_builder/builder_engine.py
│   └── deploy.py                # ← deployment_intelligence/deployment_planner.py + providers/
│
├── memory/                      # ← memory_system/founder_memory + storage (zusammengeführt)
│   ├── __init__.py
│   ├── founder.py               # ← memory_system/founder_memory/founder_memory_store.py
│   └── store.py                 # ← memory_system/storage/knowledge_store.py
│
├── improvement/                 # ← self_improvement (unverändert, nur verschoben)
│   ├── __init__.py
│   ├── engine.py
│   ├── weakness_detector.py
│   ├── task_prioritizer.py
│   └── evaluator.py
│
├── orchestrator.py              # ← orchestrator/master_orchestrator.py (verschlankt)
│
└── api/                         # Platzhalter für Phase 2
    └── __init__.py
```

**Gelöscht** (komplett entfernen — kein Informationsverlust):

```
agent_runtime/          # 66 LOC Stubs
knowledge_fabric/       # 66 LOC Stubs
global_context/         # 24 LOC Stubs
software_factory/       # 41 LOC Stubs (inkl. Syntax-Fehler)
venture_execution/      # 21 LOC Stubs
product_launch/         # 69 LOC Stubs
agent_factory/          # 20 LOC Stubs
agent_collaboration/    # 30 LOC Stubs
coding_pipeline/        # 3 LOC
code_intelligence/      # 4 LOC
engineering_team/       # 3 LOC
execution_tools/        # 7 LOC
founder_intelligence/   # 95 LOC (dupliziert Funktionalität aus opportunity_intelligence)
github_engine/          # 7 LOC
knowledge_graph/        # 16 LOC
quality_intelligence/   # 14 LOC
research_benchmarks/    # 3 LOC
research_connectors/    # 3 LOC
research_intelligence/  # 35 LOC Stubs
security_intelligence/  # 4 LOC
skill_intelligence/     # 13 LOC
testing_intelligence/   # 3 LOC
tool_intelligence/      # 19 LOC
venture_pipeline/       # 43 LOC
product_factory/        # 61 LOC
genesis_runtime/        # 123 LOC (wird in Phase 2 neu gebaut mit echtem LLM)
orchestration/          # 147 LOC (dupliziert orchestrator/)
control-center/         # 99 LOC hardcoded Status (wird in Phase 2 als echte API neu gebaut)
```

**Archiviert** (nach `_archive/` verschoben, falls man Referenzen braucht):

```
harvester/              # 119 LOC — Konzept behalten, Code archivieren
evolution/              # Konzept-Docs
```

### Implementierungsstrategie

1. `pyproject.toml` erstellen mit: `pydantic`, `pydantic-settings`, `pytest`, `ruff`
2. `genesis/` Package-Struktur anlegen
3. Die 8 Kern-Module File für File migrieren (Import-Pfade anpassen)
4. `genesis/__main__.py` erstellen: `python -m genesis analyze "AI Customer Support SaaS"`
5. `genesis/orchestrator.py` verschlanken: nur die 8 echten Module importieren
6. `ruff check genesis/` muss clean sein
7. Alte Verzeichnisse löschen oder nach `_archive/` verschieben
8. Tests migrieren und mit pytest lauffähig machen

### Tests

```bash
# Muss nach Phase 1 funktionieren:
pip install -e .
python -m genesis analyze "AI Customer Support SaaS"  # CLI Output
pytest tests/ -v                                        # Alle Tests grün
ruff check genesis/                                     # 0 Fehler
```

Spezifische Tests:
- `test_decision_engine.py` — VentureDecision mit bekanntem Input → erwarteter Score ±2
- `test_opportunity_detector.py` — detect() returned sortierte Opportunities
- `test_validation_engine.py` — GO/MODIFY/REJECT bei definierten Schwellwerten
- `test_pricing_engine.py` — 3 Tiers mit korrekten Preisen
- `test_founder_memory.py` — record_decision() + previous_decisions() Roundtrip

### Erfolgskriterien

- [ ] `pip install -e .` funktioniert fehlerfrei
- [ ] `python -m genesis analyze "X"` gibt strukturierten JSON-Output
- [ ] `pytest` meldet ≥15 Tests, alle grün
- [ ] `ruff check` meldet 0 Fehler
- [ ] Verzeichnisanzahl auf Root-Level: ≤20 (statt 60+)
- [ ] `genesis/` hat ≤40 Python-Dateien (statt 519)
- [ ] LOC in `genesis/`: ~2.500 (der echte Kern, ohne Stubs)

---

## Phase 2 — LLM-Kern: Von Heuristik zu Intelligenz

**Ziel:** Genesis nutzt ein LLM für echtes Reasoning. Der MVP-Builder generiert
prompt-spezifischen Code. Die Venture-Analyse liefert intelligente Ergebnisse.

**Warum wichtig:** Ohne LLM ist Genesis eine if/else-Maschine.
Das LLM ist der Unterschied zwischen "Tool" und "AI Operating System".

### Dateien/Systeme betroffen

```
genesis/
├── llm/                         # NEU
│   ├── __init__.py
│   ├── client.py                # Unified LLM Client (Anthropic + OpenAI)
│   ├── prompts.py               # Prompt Templates für Analyse, Code-Gen, etc.
│   └── cost_tracker.py          # Token-Usage + Kosten-Tracking
│
├── decision/
│   └── engine.py                # ERWEITERT: LLM-Reasoning statt nur Score-Aggregation
│
├── intelligence/
│   └── opportunity.py           # ERWEITERT: LLM beschreibt Opportunities, nicht Placeholder-Text
│
├── builder/
│   └── mvp.py                   # UMGEBAUT: LLM generiert prompt-spezifischen Code
│
├── api/                         # NEU
│   ├── __init__.py
│   ├── app.py                   # FastAPI App
│   ├── routes/
│   │   ├── analyze.py           # POST /api/v1/analyze — Venture-Analyse
│   │   ├── build.py             # POST /api/v1/build — MVP generieren
│   │   └── health.py            # GET /health
│   ├── auth.py                  # API-Key Authentication
│   └── schemas.py               # Request/Response Pydantic Models
│
└── config.py                    # ERWEITERT: LLM Provider, API Keys, Rate Limits
```

### Implementierungsstrategie

1. `genesis/llm/client.py`: Unified Wrapper um `anthropic` SDK. Unterstützt Claude Sonnet für Analyse, Haiku für Scoring-Enrichment. Streaming optional.
2. `genesis/llm/prompts.py`: Structured Prompts mit Pydantic-Schema-Output für:
   - Marktanalyse (aus Opportunity + Decision)
   - MVP-Scope-Definition (Features, nicht generischer CRUD)
   - Code-Generierung (prompt-spezifische FastAPI-App)
3. `genesis/decision/engine.py` erweitern: Nach dem Score-Calculation schickt das LLM den Score-Vektor + Kontext und generiert ein strukturiertes Reasoning. Das Scoring bleibt deterministisch, das Reasoning wird intelligent.
4. `genesis/builder/mvp.py` umbauen: LLM definiert Models, Routes, Business-Logik basierend auf dem Prompt. Template-Strings bleiben für Boilerplate (Dockerfile, docker-compose), aber die App-Logik wird generiert.
5. `genesis/api/` als FastAPI-Service: Ein Endpoint `POST /api/v1/analyze` nimmt einen Prompt, führt die komplette Pipeline durch, returned strukturierte JSON-Analyse.

### Dependencies (zu pyproject.toml hinzufügen)

```
anthropic>=0.30.0
fastapi>=0.111.0
uvicorn[standard]>=0.30.0
pydantic>=2.8.0
httpx>=0.27.0
```

### Tests

- `test_llm_client.py` — Mock-LLM-Call, Response-Parsing, Error-Handling
- `test_analyze_endpoint.py` — FastAPI TestClient, Input → strukturierter Output
- `test_mvp_generation.py` — Generierter Code für "Legal Doc AI" ≠ "Customer Support AI"
- `test_cost_tracker.py` — Token-Counting korrekt akkumuliert

### Erfolgskriterien

- [ ] `POST /api/v1/analyze {"prompt": "AI-powered invoice processing"}` → JSON mit Opportunity Score, Decision Verdict, Revenue Model, MVP-Scope — alles prompt-spezifisch
- [ ] Zwei verschiedene Prompts erzeugen nachweislich verschiedene MVP-Code-Outputs
- [ ] Kosten pro Analyse-Request: < $0.05 (Sonnet)
- [ ] Response-Zeit: < 15s für vollständige Analyse
- [ ] API-Key Auth funktioniert (ohne Key → 401)

---

## Phase 3 — Persistenz & Multi-User

**Ziel:** Von JSON-Dateien zu PostgreSQL. Nutzer können sich registrieren,
ihre Analysen werden gespeichert, History ist abrufbar.

**Warum wichtig:** Ohne DB kein Multi-User. Ohne Multi-User kein SaaS.
Ohne History kein Lern-Loop.

### Dateien/Systeme betroffen

```
genesis/
├── db/                          # NEU
│   ├── __init__.py
│   ├── engine.py                # SQLAlchemy async engine + session
│   ├── models.py                # User, Project, Analysis, Subscription
│   └── migrations/              # Alembic
│       ├── env.py
│       └── versions/
│           └── 001_initial.py
│
├── api/
│   ├── auth.py                  # ERWEITERT: Supabase Auth oder JWT
│   ├── routes/
│   │   ├── users.py             # NEU: Registrierung, Login, Profile
│   │   ├── projects.py          # NEU: CRUD für Venture-Projekte
│   │   └── analyze.py           # ERWEITERT: Analyse wird in DB gespeichert
│   └── middleware.py            # NEU: Rate Limiting, CORS, Logging
│
├── memory/
│   └── founder.py               # UMGEBAUT: PostgreSQL statt JSON
│
└── config.py                    # ERWEITERT: DATABASE_URL, Auth-Config
```

### Dependencies

```
sqlalchemy[asyncio]>=2.0.31
asyncpg>=0.29.0
alembic>=1.13.0
python-jose[cryptography]>=3.3.0  # JWT
passlib[bcrypt]>=1.7.4
```

### Implementierungsstrategie

1. DB-Models: `User(id, email, hashed_password, plan, created_at)`, `Project(id, user_id, prompt, status)`, `Analysis(id, project_id, decision_json, scores_json, reasoning, created_at)`
2. Alembic Migration Setup mit `DATABASE_URL` aus Environment
3. `genesis/api/auth.py`: JWT-basierte Auth (Register, Login, Token-Refresh). Optional Supabase Auth als Alternative.
4. Alle Analyse-Ergebnisse werden in `Analysis` Tabelle gespeichert
5. `GET /api/v1/projects` zeigt alle Projekte eines Users
6. `GET /api/v1/projects/{id}/analyses` zeigt Analyse-Historie

### Tests

- `test_db_models.py` — CRUD Roundtrip mit SQLite (in-memory)
- `test_auth_flow.py` — Register → Login → Token → Authenticated Request
- `test_analysis_persistence.py` — Analyse erstellen → aus DB lesen → identisch
- `test_rate_limiting.py` — 11. Request in 1 Minute → 429

### Erfolgskriterien

- [ ] User kann sich registrieren, einloggen, Analysen erstellen und abrufen
- [ ] Alembic Migration läuft gegen PostgreSQL fehlerfrei
- [ ] Analyse-History eines Users ist korrekt paginiert
- [ ] Rate Limit: 10 Analysen/Minute für Free-Tier
- [ ] Founder Memory speichert Entscheidungen in DB statt JSON

---

## Phase 4 — Monetarisierung & Production Deployment

**Ziel:** Genesis verdient Geld. Stripe-Subscriptions, Production-Hosting,
Monitoring.

**Warum wichtig:** Alles davor ist Kosten. Ab hier ist es ein Geschäft.

### Dateien/Systeme betroffen

```
genesis/
├── billing/                     # NEU
│   ├── __init__.py
│   ├── stripe_client.py         # Stripe SDK Wrapper
│   ├── plans.py                 # Free, Pro ($29/mo), Enterprise ($99/mo)
│   ├── usage.py                 # Usage-Tracking (Analysen pro Monat)
│   └── webhooks.py              # Stripe Webhook Handler
│
├── api/
│   ├── routes/
│   │   ├── billing.py           # NEU: Checkout, Portal, Webhook
│   │   └── analyze.py           # ERWEITERT: Plan-Check vor Analyse
│   └── middleware.py            # ERWEITERT: Usage-based Rate Limiting per Plan
│
├── db/
│   └── models.py                # ERWEITERT: Subscription, Usage, Invoice
│
└── frontend/                    # NEU: Minimales Dashboard
    ├── index.html               # Landing Page
    ├── app.html                 # Dashboard (Single Page)
    └── pricing.html             # Pricing Page mit Stripe Checkout
```

```
infra/                           # NEU: Auf Root-Level
├── Dockerfile
├── docker-compose.yml
├── fly.toml                     # Fly.io Deployment
├── .github/
│   └── workflows/
│       ├── ci.yml               # Lint + Test auf PR
│       └── deploy.yml           # Auto-Deploy auf main
└── .env.example
```

### Dependencies

```
stripe>=10.0.0
```

### Implementierungsstrategie

1. Stripe Products + Prices im Dashboard anlegen (Free: 0, Pro: $29/mo 50 Analysen, Enterprise: $99/mo unlimited)
2. `genesis/billing/stripe_client.py`: Checkout Session erstellen, Webhook verarbeiten (subscription.created/updated/deleted)
3. `genesis/api/routes/billing.py`: `POST /api/v1/checkout` → Stripe Checkout URL, `POST /api/v1/webhooks/stripe` → Event Handler
4. Usage Tracking: Zähle Analysen pro User pro Monat, blockiere bei Limit
5. `fly.toml` für Fly.io, alternativ `railway.toml`
6. GitHub Actions CI: `ruff check` + `pytest` auf jedem PR, Auto-Deploy auf `main`
7. Minimales Frontend: Landing Page mit Value Prop, Pricing, Dashboard mit Analyse-History

### Tests

- `test_stripe_checkout.py` — Mock Stripe, Checkout-URL wird korrekt generiert
- `test_usage_limits.py` — Free User nach 5 Analysen → 402 Payment Required
- `test_webhook_handling.py` — Simulated subscription.created → User Plan updated
- `test_ci_pipeline.py` — GitHub Actions Workflow YAML ist syntaktisch korrekt

### Erfolgskriterien

- [ ] Nutzer kann sich registrieren, Free Plan nutzen, auf Pro upgraden
- [ ] Stripe Checkout Flow funktioniert end-to-end
- [ ] Usage Limits werden korrekt enforced
- [ ] App ist auf fly.io/railway deployed und erreichbar
- [ ] CI/CD läuft auf jedem Push: Lint → Test → Deploy
- [ ] Landing Page hat klare Value Proposition und CTA

---

## Phase 5 — Echte Markt-Intelligence & Autonomous Loop

**Ziel:** Von ASSUMED zu VERIFIED. Echte externe Daten fließen in die Analyse.
Der Self-Improvement-Loop wird real.

**Warum wichtig:** Hier wird Genesis von einem Tool zu einem unfairen Vorteil.
Echte Daten + LLM-Reasoning + automatische Verbesserung = Moat.

### Dateien/Systeme betroffen

```
genesis/intelligence/connectors/
├── base.py                      # UNVERÄNDERT (bereits sauber)
├── google_trends.py             # NEU: Google Trends / SerpAPI
├── producthunt.py               # NEU: Product Hunt API
├── github_api.py                # NEU: GitHub Search API (Repos, Stars, Commits)
├── crunchbase.py                # NEU: Crunchbase API (Funding, Companies)
└── serp.py                      # NEU: Search Engine Results für Competitor Analysis

genesis/improvement/
├── engine.py                    # ERWEITERT: Echte Metriken aus DB (Conversion, Usage)
├── weakness_detector.py         # ERWEITERT: Analysiert reale User-Daten
└── autonomous_loop.py           # ERWEITERT: Scheduled Cron Job, nicht simuliert
```

### Dependencies

```
serpapi>=2.0.0          # Google Trends + SERP
httpx>=0.27.0           # Async HTTP für APIs
apscheduler>=3.10.0     # Scheduled Jobs für Improvement Loop
```

### Implementierungsstrategie

1. `live_intelligence/base.py` ist bereits die richtige Abstraktion. Für jeden neuen Connector: `_fetch_live()` implementieren, `_fallback()` bleibt als Graceful Degradation.
2. SerpAPI für Google Trends + SERP-Daten (ein API-Key, mehrere Use Cases)
3. GitHub REST API (unauthenticated: 60 req/h, mit Token: 5.000 req/h) für Open-Source-Aktivität
4. Product Hunt API für Launch-Timing und ähnliche Produkte
5. Self-Improvement Loop als APScheduler CronJob: Alle 24h analysiert er Conversion-Rates, User-Feedback, fehlerhafte Analysen → priorisiert Verbesserungen
6. Ergebnisse von Improvement Loop werden als Issues in GitHub erstellt oder als Tasks in der DB gespeichert

### Tests

- `test_google_trends_connector.py` — Mock HTTP, Response-Parsing, Fallback bei Fehler
- `test_github_connector.py` — Mock API, Repo-Count und Star-Count korrekt geparst
- `test_improvement_loop.py` — Schwäche erkannt → Task erstellt → Score verbessert
- `test_end_to_end.py` — Vollständiger Analyse-Flow mit echten Connectors (Integration-Test, optional)

### Erfolgskriterien

- [ ] Mindestens 3 Connectors liefern echte Daten (confidence: VERIFIED)
- [ ] Analyse-Output enthält reale Trend-Daten und Wettbewerber
- [ ] Improvement Loop läuft als Scheduled Job und schreibt Ergebnisse in DB
- [ ] Fallback-Modus funktioniert: Wenn API ausfällt → ASSUMED statt Error
- [ ] Connector-Kosten sind getracked und ≤ $10/Monat für moderate Nutzung

---

## Zusammenfassung — Phasen-Matrix

| Phase | Dauer | Hauptergebnis | Revenue-Impact |
|---|---|---|---|
| **1: Konsolidierung** | 1–2 Wochen | Lauffähiges Package, 12 Module statt 60+ | Keiner (Fundament) |
| **2: LLM-Kern** | 2–3 Wochen | Intelligente Analyse-API, prompt-spezifischer Output | Demonstrierbar, erste Beta-User |
| **3: Persistenz** | 2 Wochen | Multi-User, Auth, History | User können wiederkommen |
| **4: Monetarisierung** | 2–3 Wochen | Stripe, Hosting, CI/CD, Landing Page | **Erster Dollar** |
| **5: Live-Daten** | 3–4 Wochen | Echte Marktdaten, Autonomous Improvement | Qualitäts-Moat, Retention |

**Geschätzte Gesamtdauer bis zum ersten zahlenden Kunden: 10–14 Wochen.**

---

## Nicht in diesem Plan

Bewusst ausgeklammert, weil YAGNI:

- Multi-Agent-Orchestrierung (erst wenn ein Agent echten Wert liefert)
- Knowledge Graph / Embedding-basierte Suche (erst wenn genug Daten existieren)
- Mobile App (Web-First)
- Eigenes LLM-Training (API-First)
- Marketplace / Plugin-System (erst nach PMF)
- Automatisches GitHub-Repo-Erstellen (erst nach validiertem MVP-Builder)
