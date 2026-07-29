# Agent Orchestration (Phase 6-13)

Das Genesis Harness ist nun ein vollständig autonomes Multi-Agenten-System. Der Meta-Loop steuert die Entwicklung, ohne dass menschliche Intervention bei Routinetasks notwendig ist.

## 1. Agent & Skill Discovery
Die `AgentRegistry` und der `SkillLoader` (aus `genesis.core`) scannen dynamisch nach neuen Agenten in `agents/` und laden Skills aus lokalen Ordnern, von GitHub oder systemintern (Claude).

## 2. Der Meta-Loop
Der Ablauf des autonomen Loops (`genesis.core.meta_loop.MetaAgent`):
1. **Ziel-Analyse:** MetaAgent zerlegt User Intents in strukturierte Sub-Tasks (`Task` Objekte).
2. **Capability Matching:** Sub-Tasks werden anhand ihrer `required_skills` an die passenden Agenten vergeben (z.B. UI-Design an `ui-agent`).
3. **Parallele Ausführung:** Die `WorkflowEngine` verarbeitet alle unabhängigen Tasks (ohne abstehende Dependencies) gleichzeitig. 
4. **Validierung (QA):** Abhängige QA-Tasks (z.B. Visual QA) triggern nach Abschluss der Build-Tasks.
5. **State Update:** Der `AgentStateStore` informiert das Live Dashboard via WebSocket.

## 3. Live Development Dashboard
Befindet sich in `genesis/dashboard/`. Startet via:
`uvicorn genesis.dashboard.server:app --reload`
Verbindet sich über WebSockets und bietet einen Agent Activity Viewer und Live-Logs im Browser.

## 4. Anwendungsfall: Islam Tutor
Das Skript `scripts/run_islam_tutor_loop.py` triggert den Meta-Loop. Hierbei werden gleichzeitig:
- `content-agent` -> Quran-Quellen verifizieren
- `ui-agent` -> Namaz Avatar erstellen
- `voice-agent` -> Audio-Pipeline laden
- `visual-qa-agent` -> UI per Playwright-MCP bewerten
