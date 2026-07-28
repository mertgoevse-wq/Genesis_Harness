# Genesis Harness

An **AI development operating system** — infrastructure that lets multiple specialised AI agents
collaboratively design, build, verify, and document complex software, with continuity across
sessions and across models.

**Version:** 1.0.0 · **Phase:** 0 — Foundation · **Last updated:** 2026-07-28

> This is the harness, not the engine. The Genesis Engine will later be built *inside* it.

---

## The Problem

An AI coding session is amnesiac, its confidence is uncorrelated with its correctness, and its
output quality degrades as scope grows. Genesis Harness addresses each with structure rather than
with exhortation.

| Problem | Mechanism |
|---|---|
| Sessions forget | Append-only session logs, handoff artefacts, the cold-start test |
| Confidence ≠ correctness | Mandatory verification states, confidence labels, QA authority to block commits |
| Quality degrades with scope | Role separation, one owner per artefact, decomposition into cold-startable units |
| Process drifts | Layered prompts, a machine-readable registry, scripted commit gates |

---

## Start Here

| If you are… | Read |
|---|---|
| An AI agent starting a session | [`CLAUDE.md`](CLAUDE.md) — the constitution — then [`docs/ROADMAP.md`](docs/ROADMAP.md) |
| Trying to understand the design | [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) |
| Trying to get work done | [`docs/WORKFLOW.md`](docs/WORKFLOW.md) |
| Curious who does what | [`docs/AGENTS.md`](docs/AGENTS.md) |
| Wondering what is next | [`docs/ROADMAP.md`](docs/ROADMAP.md) |

---

## Structure

```
CLAUDE.md               Constitution — highest authority after explicit human instruction
.claude/agents/         Runtime agent adapters (Claude Code discovery)
agents/<id>/AGENT.md    Canonical agent charters — 6 agents
skills/<id>/SKILL.md    Knowledge domains — 9 skills
prompts/
  system_layers/        L0–L5 composable instruction layers
  master_prompts/       Analysis · Architecture · Coding · Research · Review
  generators/           Meta-prompts that produce new agents, skills, prompts
  benchmarks/           Rubric + golden cases that make prompt changes measurable
logs/
  SESSION_TEMPLATE.md   Required session log structure
  sessions/             Append-only session history — the harness's memory
docs/                   ARCHITECTURE · AGENTS · WORKFLOW · ROADMAP · adr/
scripts/                PowerShell automation — commit gates, structure check, log creation
configs/                Machine-readable registry, quality thresholds, model routing
templates/              AGENT · SKILL · ADR · HANDOFF
```

---

## Agents

| Agent | Owns | Can block |
|---|---|---|
| [Architect](agents/architect/AGENT.md) | Structure, contracts, technology decisions | Implementation violating a contract |
| [Research](agents/research/AGENT.md) | Factual claims about the outside world | Decisions built on unverified claims |
| [Coding](agents/coding/AGENT.md) | Source file contents | — |
| [Simulation Scientist](agents/simulation-scientist/AGENT.md) | Physical and numerical correctness | Unstable or invalid models |
| [Game Design](agents/game-design/AGENT.md) | Player experience | Incoherent player-facing systems |
| [QA](agents/qa/AGENT.md) | The definition of done | **Any commit** |

## Skills

**Science** — [physics](skills/physics/SKILL.md) · [chemistry](skills/chemistry/SKILL.md) ·
[biology](skills/biology/SKILL.md) · [astronomy](skills/astronomy/SKILL.md)

**Engineering** — [simulation](skills/simulation/SKILL.md) ·
[game-development](skills/game-development/SKILL.md) ·
[software-engineering](skills/software-engineering/SKILL.md)

**Meta** — [ai-agents](skills/ai-agents/SKILL.md) ·
[prompt-engineering](skills/prompt-engineering/SKILL.md)

---

## The Genesis Loop

```
INTAKE → RESEARCH → DESIGN → PLAN → BUILD → VERIFY → LOG → COMMIT
```

Each stage has an owning agent, a produced artefact, and a gate. Artefacts — not conversation —
carry work between stages, which is what makes the loop survive a context reset.
Full detail in [`docs/WORKFLOW.md`](docs/WORKFLOW.md).

---

## Usage

Requires **PowerShell 7+** (`pwsh`). Run from the repository root.

```powershell
# Start a session
pwsh -File scripts/new_session_log.ps1 -Slug "my-task"

# Verify the repository structure
pwsh -File scripts/verify_structure.ps1

# Commit — nine safety gates, dry run first
pwsh -File scripts/auto_commit.ps1 -Message "feat: add X" -DryRun
pwsh -File scripts/auto_commit.ps1 -Message "feat: add X" -Push
```

`auto_commit.ps1` blocks on: credential-shaped content, structure failures, a missing session log,
and unconfirmed commits to `main`. It never force-pushes, never rewrites history, and never uses
`--no-verify`.

---

## Core Rules

Three rules carry most of the weight. The rest are in [`CLAUDE.md`](CLAUDE.md).

1. **Never report a result you did not observe.** `verified` (executed), `implemented-not-run`,
   and `planned` are three different things and are never blurred. Fabricating a test result,
   a citation, or command output is a CRITICAL defect.
2. **Never silently narrow scope.** Deliver the whole thing, or say explicitly what you left and
   why. Scaling the work down is the operator's decision.
3. **Every change writes a session log.** The reasoning summary — *why*, including options
   rejected — is how the next session reconstructs intent.

---

## Current State

The foundation exists and the scripts execute. **The harness has not yet been used to build
anything**, so its process claims are untested in practice. Phase 1 exists to test them.

Known open problems are tracked in [`docs/ROADMAP.md`](docs/ROADMAP.md#open-problems).
