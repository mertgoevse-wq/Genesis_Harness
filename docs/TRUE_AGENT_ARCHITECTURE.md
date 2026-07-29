# TRUE AGENT ARCHITECTURE (Phase 16)

## 1. Übersicht
Genesis Harness ist nun eine echte kognitive Architektur (Cognitive Architecture). Agenten sind nicht länger nur ausführende Funktionen einer Queue, sondern besitzen Identität, Kontext, Fähigkeiten und einen eigenen Entscheidungskreislauf.

## 2. Agent Runtime & Lifecycle
Jeder Agent (`AutonomousAgent`) wird durch `agent_runtime.py` instanziiert und durchläuft bei jedem Task den **OODA Loop** (Observe, Orient/Analyze, Decide/Plan, Act/Execute):
1. **Observe:** Liest das Environment & Task.
2. **Analyze:** LLM Provider bewertet Kontext und greift auf Langzeitgedächtnis zu.
3. **Plan:** LLM generiert einen Lösungsansatz.
4. **Select Skill / Select Tool:** Wählt das passende Werkzeug aus seiner Whitelist aus.
5. **Execute:** Führt die Aktion über das Tool (z.B. Filesystem, MCP) aus.
6. **Evaluate:** QA Agent / LLM bewertet das Ergebnis (Success/Failure).
7. **Remember:** Schreibt Learnings in das JSON-Langzeitgedächtnis.

## 3. Tool System
Agenten agieren *nicht* direkt auf dem System, sondern über das Interface `BaseTool`.
- `FileSystemTool`: Lesen/Schreiben von Dateien.
- `TerminalTool`: Ausführen von Bash/Powershell.
- `BrowserTool`: Headless Web-Steuerung.
- `GitTool`, `TestTool`, `DocumentationTool`

## 4. LLM Provider Interface
Das System unterstützt Multi-LLM Architekturen über das `LLMProvider` Interface. 
Verfügbare Adapter in `genesis/providers/`:
- `ClaudeProvider` (Anthropic)
- `GeminiProvider` (Google)
- `OpenAIProvider`
- `OllamaProvider` (Lokal)
-> Dadurch können z.B. komplexe Research-Agenten mit Gemini, Coding-Agenten mit Claude und einfache Logging-Agenten mit lokalem Ollama betrieben werden.

## 5. Model Context Protocol (MCP) Integration
Für komplexe Ein- und Ausgaben wurden MCP-Adapter (`genesis/mcp/adapters.py`) implementiert:
- **FilesystemMCP:** Dateisystem über Protokollgrenzen hinweg.
- **GithubMCP:** Für Repo-Management.
- **VoiceMCP / VideoMCP:** Für externe Render-Engines wie OmniVoiceStudio.

## 6. Self Improvement & Memory
`AgentStateStore` speichert jeden Lauf unter `logs/memory/<AgentID>/`. Erkenntnisse aus Fehlern oder Erfolgen fließen über `retrieve_past_learnings()` in zukünftige **Analyze**-Schritte ein. Am Ende eines iterativen Loops bewertet der MetaAgent das Gesamtergebnis und schreibt es ins Projektwissen (Self-Improvement Loop in `meta_loop.py`).
