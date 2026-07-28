---
id: L2_domain_context
layer: 2
name: Domain Context
version: 1.0.0
changes_frequency: per-project-phase
---

# L2 — Domain Context Layer

> **Composition rule:** L2 supplies the situational facts an agent needs to reason correctly
> about *this* repository at *this* moment. It is the layer that changes when the project changes.
> It contains facts and constraints, not method (L1) and not the task (L3).

---

## 1. The System

**Genesis Harness** — an AI development operating system. Infrastructure that lets multiple
specialised AI agents collaboratively design, build, verify, and document complex software with
continuity across sessions and models.

**It is not the Genesis Engine.** It is the harness the Genesis Engine will later be built inside.
Do not build engine features during foundation phases.

## 2. Current State

| Field | Value |
|---|---|
| Phase | Phase 0 — Foundation |
| Repository | `C:\Genesis_Harness` |
| Default branch | `main` |
| Platform | Windows 11, PowerShell 7+ primary, Git Bash available |
| Runtime code | None yet — the repository is currently specification, documentation, and scripts |
| Test runner | None yet — verification is by script execution and structural checks |

> **Maintenance:** update this table at the end of every phase. A stale L2 causes agents to
> reason about a system that no longer exists. See `docs/ROADMAP.md` for the authoritative phase
> state.

## 3. Repository Map

```
CLAUDE.md            Constitution — highest authority after the human
.claude/agents/      Runtime agent adapters (Claude Code discovery)
agents/<id>/AGENT.md Canonical agent charters
skills/<id>/SKILL.md Knowledge domains
prompts/             This framework: system_layers, master_prompts, generators, benchmarks
logs/sessions/       Append-only session history — the harness's memory
docs/                ARCHITECTURE, AGENTS, WORKFLOW, ROADMAP, adr/
scripts/             PowerShell automation (commit, verify, session logging)
configs/             Machine-readable registry, quality gates, model routing
templates/           ADR, AGENT, SKILL, HANDOFF, SESSION templates
```

## 4. Standing Constraints

| Constraint | Value | Type |
|---|---|---|
| Operating system | Windows 11 | hard |
| Shell for automation | PowerShell 7+ (`pwsh`) | hard |
| Line endings | Repository is authored on Windows; scripts must tolerate CRLF | hard |
| Secrets | Never in source. No secret store configured yet | hard |
| Remote | `origin` → GitHub, single operator | contextual |
| Network access | Not assumed available to agents; verify before depending on it | contextual |
| External services | None approved. Adding one requires an ADR | policy |

## 5. Conventions

- **Files:** Markdown for specification, PowerShell (`.ps1`) for automation, JSON for config.
- **Naming:** agent and skill IDs are `kebab-case`; session logs are
  `YYYY-MM-DD_NN_slug.md`; ADRs are `NNNN-title.md`.
- **Dates:** always absolute (`2026-07-28`), never relative.
- **Documents describing current state** carry a version and a last-updated date.
- **Commits:** conventional (`feat:`, `fix:`, `docs:`, …); infrastructure commits authored by the
  AI at the operator's request may use the `AI:` prefix.

## 6. Domain Vocabulary

| Term | Meaning here |
|---|---|
| **Harness** | The agent infrastructure — this repository |
| **Engine** | The future Genesis Engine, built later *inside* the harness |
| **Agent** | A role with scope, authority, workflow, and an output contract |
| **Skill** | A knowledge domain an agent loads |
| **Charter** | `agents/<id>/AGENT.md` — the authoritative agent definition |
| **Adapter** | `.claude/agents/<id>.md` — the runtime-invocable wrapper |
| **Genesis Loop** | The eight-stage workflow (intake → … → commit) |
| **Handoff** | The artefact transferring work between agents |
| **Cold-start test** | Could a fresh agent resume from these artefacts alone? |
| **Session log** | The append-only record in `logs/sessions/` — the harness's memory |

## 7. What Is Explicitly Out Of Scope Right Now

- Building the Genesis Engine itself.
- Adding runtime dependencies, package managers, or build systems without an ADR.
- Introducing external services, APIs, or paid tooling.
- Rewriting or reformatting session logs.
- Any network-dependent workflow presented as reliable without verification.
