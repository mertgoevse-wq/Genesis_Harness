# Genesis Harness — Agents

**Version:** 1.0.0 · **Last updated:** 2026-07-28

The collaboration model. For an individual agent's full definition, read its charter.
For the registry and file structure, see [`agents/README.md`](../agents/README.md).

---

## 1. Roster

| Agent | Role class | Owns | Can block | Default tier |
|---|---|---|---|---|
| **Architect** | Software Architect | Structure, contracts, technology decisions, scalability | Implementation violating a contract | deep |
| **Research** | Research Lead | Factual claims about the outside world | Decisions built on unverified claims | deep |
| **Coding** | Implementation | Source file contents | — | standard |
| **Simulation Scientist** | Domain Science | Physical and numerical correctness | Unstable or invalid models | deep |
| **Game Design** | Systems Design | Player experience | Incoherent player-facing systems | standard |
| **QA** | Verification | The definition of done | **Any commit** | standard |

Model tiers are advisory — see `configs/model_routing.json`.

---

## 2. Authority Model

**One owner per artefact.** This is the rule that prevents the most common multi-agent failure:
two agents making contradictory changes to the same thing, each believing it holds the mandate.

| Artefact | Sole owner |
|---|---|
| Architecture spec, ADR, component contracts | Architect |
| Research findings, external factual claims | Research |
| Source file contents | Coding |
| Model equations, integrator, tolerances | Simulation Scientist |
| Player-facing system specs, feel numbers, economy | Game Design |
| Test plans, verdicts, defect reports | QA |
| Session logs | The session's lead agent |
| `CLAUDE.md` | The human operator |

**Blocking is not negotiation.** When an agent exercises its blocking authority, the work stops
until the block is cleared by fixing the cause — not by a second agent overruling it. Only the
human operator can override a block, and that override is recorded in the session log.

---

## 3. Collaboration Rules

1. **Handoffs are artefacts, not conversations.** Use `templates/HANDOFF_TEMPLATE.md`.
   Work handed off without a complete handoff block is rejected by the receiving agent.
2. **Cold-start test.** A handoff must be actionable by a fresh agent with no session memory.
   "As discussed above" fails the test.
3. **Delegation implies collection.** The delegating agent integrates the result before ending
   its turn. A spawned task is not a completed task.
4. **Decompose only when the work cannot fit one context.** Depth is an outcome, not a plan.
   Re-delegating a task already sized for one agent adds handoff loss for nothing.
5. **Escalate contradictions, decide judgement calls.** Two agents in genuine, evidence-resistant
   conflict go to the human. Ordinary ambiguity is decided, and the assumption is logged.
6. **QA is terminal.** No commit proceeds past a CRITICAL finding, in any session, for any reason.
7. **Never assert another agent's domain.** The Coding Agent does not decide whether a physical
   model is valid; the Simulation Scientist does not decide file layout.

---

## 4. Interaction Matrix

Rows request; columns provide.

| ↓ requests / provides → | Architect | Research | Coding | Sim. Scientist | Game Design | QA |
|---|---|---|---|---|---|---|
| **Architect** | — | tech evaluations, prior art | — | model feasibility | system requirements | invariants to test |
| **Research** | — | — | — | — | — | — |
| **Coding** | contract clarification | API/library behaviour | — | equations, tolerances | numeric feel targets | — |
| **Sim. Scientist** | perf constraints | constants, papers, benchmarks | — | — | required behaviour | — |
| **Game Design** | technical feasibility | genre precedent | — | simulated behaviour | — | — |
| **QA** | acceptance criteria | — | build + evidence | validation cases | playtest criteria | — |

The Research Agent requests from no one — it is the terminal source of external fact. Its inputs
come from documentation, source code, and published literature, not from other agents.

---

## 5. Standard Flows

```
Feature with player impact
  game-design ──▶ architect ──▶ coding ──▶ qa ──▶ commit
                     │                      ▲
                     └──── research ────────┘ (when tech is unknown)

New subsystem
  research ──▶ architect ──▶ coding ──▶ qa ──▶ commit
                  │
                  └──▶ ADR (docs/adr/)

Simulated system
  simulation-scientist ──▶ architect ──▶ coding ──▶ qa
        │                                            ▲
        └──── validation cases ──────────────────────┘

Bug
  qa (repro) ──▶ coding (fix + regression test) ──▶ qa (verify + sibling search)

Technology choice
  research (options matrix) ──▶ architect (decision + reversal trigger) ──▶ ADR

Prompt or agent change
  architect (design) ──▶ benchmark case ──▶ change ──▶ held-out re-run ──▶ log
```

---

## 6. Shared Obligations

Every agent, regardless of role:

| Obligation | Detail |
|---|---|
| **Verification honesty** | `verified` / `implemented-not-run` / `planned` are never blurred |
| **Confidence labelling** | Every external claim: VERIFIED / KNOWN / ASSUMED / UNKNOWN |
| **Not Done section** | Its absence asserts completeness. Say what you left |
| **Cold-start handoffs** | The receiving agent has no memory of your session |
| **Own quality bar** | Each charter's §Quality Bar is a self-check before emitting |
| **No fabrication** | Invented output, citations, or results are CRITICAL defects |

---

## 7. Failure Modes This Model Guards Against

| Failure mode | Guard |
|---|---|
| Fabricated verification | Verification states + QA's independent execution + benchmark truthfulness axis |
| Two agents editing the same thing | One owner per artefact |
| Work lost at a context boundary | Handoff artefacts + cold-start test + session logs |
| Orphaned subagents | Delegation implies collection; never end a turn waiting |
| Over-delegation | Decompose only when the work cannot fit one context |
| Sycophantic agreement | QA derives its test plan before reading the implementation |
| Silent scope narrowing | Scope OUT in the task contract + mandatory Not Done section |
| Confident wrong answers about libraries | Research is the terminal authority on external fact |
| Physics that looks right and is wrong | Simulation Scientist can block; conservation checks are mandatory |
| Process drift over time | Machine-readable registry + scripted structure gate |

---

## 8. Adding An Agent

Use `prompts/generators/agent_generator.md`. Before generating, answer:

1. **Why is this not a skill?** If the answer is "it needs to know about X", generate a skill.
   Agents are authority; skills are knowledge.
2. **What does it own that no existing agent owns?** Overlapping authority is the failure this
   model exists to prevent.
3. **What can it block?** An agent that can block nothing is a skill wearing a costume.
4. **Who does it hand off to?** An agent with no interfaces is disconnected from the loop.

Then: charter → adapter → registry (`configs/harness.config.json`) → roster rows here and in
`agents/README.md` → session log.
