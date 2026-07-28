# Agent Registry

**Version:** 1.0.0 · **Last updated:** 2026-07-28

An **agent** is a role with a defined scope, authority, workflow, and output contract.
Agents are *who does the work*; [skills](../skills/README.md) are *what they know*.

Machine-readable registry: `configs/harness.config.json`.
Collaboration model and full contracts: [`docs/AGENTS.md`](../docs/AGENTS.md).

## Roster

| Agent | Role class | Owns | Can block | Charter |
|---|---|---|---|---|
| [architect](architect/AGENT.md) | Software Architect | Structure, contracts, tech choices | Implementation violating a contract | `architect/AGENT.md` |
| [research](research/AGENT.md) | Research Lead | Factual claims about the outside world | Decisions built on unverified claims | `research/AGENT.md` |
| [coding](coding/AGENT.md) | Implementation | Source file contents | — | `coding/AGENT.md` |
| [simulation-scientist](simulation-scientist/AGENT.md) | Domain Science | Physical/numerical correctness | Unstable or invalid models | `simulation-scientist/AGENT.md` |
| [game-design](game-design/AGENT.md) | Systems Design | Player experience | Incoherent player-facing systems | `game-design/AGENT.md` |
| [qa](qa/AGENT.md) | Verification | The definition of "done" | **Any commit** | `qa/AGENT.md` |

## Two-File Structure

Each agent exists in two places, deliberately:

| File | Purpose | Length |
|---|---|---|
| `agents/<id>/AGENT.md` | **Canonical charter.** Full purpose, responsibilities, knowledge, workflow, output format, quality bar, interfaces. The authoritative definition. | Long |
| `.claude/agents/<id>.md` | **Runtime adapter.** YAML frontmatter for Claude Code discovery, tool grants, and a condensed operating contract that points back at the charter. | Short |

The adapter is what makes the agent invocable. The charter is what makes it correct.
**When they disagree, the charter wins** — and the adapter is a bug to be fixed.

## Charter Structure

Every `AGENT.md` has the same eight sections:

| Section | Contains |
|---|---|
| Header | ID, version, role class, authority (what it can block) |
| 1. Purpose | Why the agent exists and its defining stance |
| 2. Responsibilities / Knowledge Domains | What it owns, in detail |
| 3. Knowledge & Skills | Which `skills/` it loads |
| 4/5. Workflow | The ordered stages, plus hard rules and stop conditions |
| 5/6. Output Format | The exact template its deliverable must follow |
| 6/7. Quality Bar | The conditions under which its own output is rejected |
| 7/8. Interfaces | Who it receives from, requests from, hands off to, escalates to |

## Invocation

**Automatic** — Claude Code selects an agent from the `description` field in its adapter.
**Explicit** — name the agent: *"Use the architect agent to design the event bus."*

## Collaboration Rules

1. **One owner per artefact.** Two agents never hold authority over the same file.
2. **Handoffs are artefacts, not conversations.** Use `templates/HANDOFF_TEMPLATE.md`.
   Work handed off without a handoff block is rejected.
3. **Cold-start test.** A handoff must be sufficient for a fresh agent with no memory of the
   session. If it is not, it is incomplete.
4. **Delegation implies collection.** The delegating agent integrates the result. Never end a
   turn with outstanding children.
5. **QA is terminal.** No commit proceeds past a CRITICAL finding.
6. **Escalate contradictions, decide judgement calls.** Two agents in unresolvable conflict go to
   the human; ordinary ambiguity is decided and logged as an assumption.

## Typical Flows

```
Feature:     game-design → architect → coding → qa
Subsystem:   research → architect → coding → qa
Simulation:  simulation-scientist → architect → coding → qa
Bug:         qa → coding → qa
Tech choice: research → architect → (ADR)
```

## Adding an Agent

1. Copy `templates/AGENT_TEMPLATE.md` to `agents/<id>/AGENT.md` and fill all sections.
2. Create the adapter at `.claude/agents/<id>.md` with frontmatter and minimum tool grants.
3. Register in `configs/harness.config.json`.
4. Add rows to the roster above and to `docs/AGENTS.md`.
5. Define its interfaces with **existing** agents — an agent with no interfaces is a smell.
6. Record the addition in a session log.
