# AUTONOMOUS SOFTWARE ENGINEERING (Phase 17)

## 1. Übersicht
Mit Phase 17 hat Genesis Harness die Stufe echter autonomer Softwareentwicklung (Autonomous Software Engineering) erreicht. Agenten besitzen nun Intelligence-Fähigkeiten (Repository-, Code- und Dependency-Scanning) und durchlaufen einen vollständigen Entwicklungs-Lifecycle, inklusive Git-Integration, Visual QA und Self-Review.

## 2. Intelligence Layer (`genesis/intelligence/`)
Das Framework kann jetzt den Codebase-Kontext selbst erfassen:
- **RepositoryScanner:** Liest die Struktur des Projekts und schließt unnötige Verzeichnisse aus (`__pycache__`, `node_modules`).
- **CodeAnalyzer:** Parst Python-Dateien mittels AST, um Klassen- und Funktionsdefinitionen zu extrahieren.
- **DependencyAnalyzer:** Identifiziert verwendete Bibliotheken aus `requirements.txt` und `package.json`.

## 3. Der Coding Agent (`engineer_agent.py`)
Ein spezialisierter Agent (`SoftwareEngineerAgent`) orchestriert den Entwicklungsprozess in der Methode `run_engineering_loop()`:
1. **Analyze Repository:** Kontext und Projektstruktur einlesen.
2. **Create Plan:** Architektur planen.
3. **Modify Files:** Code schreiben.
4. **Run Tests:** Test-Suite über `TestTool` ausführen.
5. **Fix Errors:** Selbstheilungs-Loop (Self-Correction), falls Tests fehlschlagen.
6. **Commit:** Änderungen via `GitTool` (mit Subprocess) ins Repository einpflegen.

## 4. LLM Provider Interfaces
Die Integration von echten LLM-APIs wurde vorbereitet. Die Interfaces in `genesis/providers/` (`claude.py`, `gemini.py`, `openai.py`, `ollama.py`) implementieren:
- `chat()`
- `analyze()`
- `plan()`
- `generate_code()`
- `review_code()`

*Hinweis:* Über die Umgebungsvariable `GENESIS_LIVE_API=true` können diese in Zukunft auf echte API-Calls umgestellt werden. Der Standard ist ein Mock-Modus für sicheres Testen.

## 5. Visual QA & Self Review
- **Visual Development Loop:** Das `BrowserTool` erlaubt das Erstellen von Screenshots und eine simulierte UI-Analyse zur Erkennung von Overlaps oder Fehlplatzierungen (z.B. für React oder Three.js).
- **Self Review:** Der `agent_runtime.py` Evaluate-Schritt beinhaltet nun Reviews durch *Code Review Agent*, *QA Agent* und *Documentation Agent*. Der *Meta Agent* trifft die finale Entscheidung (Akzeptieren, Verbessern, Zurückweisen).
