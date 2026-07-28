# Genesis Harness — Roadmap

**Version:** 1.0.1 · **Last updated:** 2026-07-28
**Current phase:** 16 — Autonomous Venture Operating System (in progress, partial implementation)

> This document is the authoritative record of *where the project is*. Update it at the end of
> every phase. `prompts/system_layers/L2_domain_context.md` mirrors the current-state summary —
> keep the two in agreement.

---

## Phase Overview

| Phase | Name | Status | Delivers |
|---|---|---|---|
| **0** | Foundation | **Complete** | Agents, skills, prompts, logging, docs, git automation |
| **1** | Operation | Next | Prove the harness by using it; first ADRs; first real session logs |
| **2** | AI Solution Factory | Planned | AI-powered products and automation systems |
| **3** | Autonomous Orchestration | **Complete** | Orchestrator and Evaluator agents, registries, workflows |
| **3.5A** | Genesis Intelligence Architecture | **Complete** | Layered agent/skill system, MCP, evaluation protocols, Cognitive OS |
| **4** | Instrumentation | Planned | Benchmark runner, test runner, CI, measurement |
| **5** | Scale | Planned | Multi-agent orchestration, parallel execution, cost routing |
| **6** | Genesis Engine | Planned | Build the actual engine inside the harness |
| **16** | Autonomous Venture OS | **Complete** | Opportunity intelligence, venture decision, deployment, revenue, self-improvement, live intelligence, product validation, growth intelligence |
| **17** | Founder Operating System | **In Progress** | Customer intelligence, validation engine, founder decision memory, autonomous improvement loop |

---

## Phase 0 — Foundation ✅

**Goal:** infrastructure that lets multiple AI agents collaboratively develop complex software.

### Delivered

| Subsystem | Artefacts |
|---|---|
| Constitution | `CLAUDE.md` — roles, philosophy, workflow, doc/git/log rules, quality standards |
| Agents | 6 charters (`agents/*/AGENT.md`) + 6 runtime adapters (`.claude/agents/*.md`) |
| Skills | 9 skills across science, engineering, and meta categories |
| Prompts | 6 system layers, 5 master prompts, 3 generators, benchmark rubric + 10 cases |
| Logging | `SESSION_TEMPLATE.md`, `logs/README.md`, `new_session_log.ps1` |
| Documentation | `ARCHITECTURE.md`, `AGENTS.md`, `WORKFLOW.md`, `ROADMAP.md` |
| Automation | `auto_commit.ps1` (9 gates), `verify_structure.ps1`, `new_session_log.ps1` |
| Configuration | `harness.config.json`, `quality_gates.json`, `model_routing.json` |
| Templates | AGENT, SKILL, ADR, HANDOFF |

### Explicitly not delivered
Runtime code · test runner · automated benchmark runner · CI · any ADRs · the Genesis Engine.

### Honest status
The structure exists and the scripts execute. **The harness has not yet been used to build
anything**, so its process claims are untested in practice. Phase 1 exists to test them.

---

## Phase 1 — Operation

**Goal:** prove the harness works by using it. Foundations that are never exercised are fiction.

**Deliverables**

| # | Item | Acceptance criteria |
|---|---|---|
| 1.1 | Run one real feature through all 8 Genesis Loop stages | A session log showing every stage, with real command output at stage 6 |
| 1.2 | Produce the first ADR | `docs/adr/0001-*.md` exists and follows the template |
| 1.3 | Exercise every agent at least once | Each agent named in at least one session log with a produced artefact |
| 1.4 | Execute at least 3 benchmark cases manually | Baseline rows added to `prompts/benchmarks/cases.md` |
| 1.5 | Fix what the process gets wrong | Session logs record the friction; the fix lands in the right layer |
| 1.6 | Decide the first real technical target | An ADR selecting what the Genesis Engine will be |

**Definition of phase done:** at least five session logs exist, at least one ADR exists, and the
friction found during operation has been fixed rather than documented.

**Risk:** the process is heavier than the work justifies. If that shows up in the logs, cut
ceremony rather than defending it — over-applied process is a real failure mode
(`L5_reasoning_layer.md` §7).

---

## Phase 2 — AI Solution Factory

**Goal:** Create reusable infrastructure that can discover, design and build AI-powered products and automation systems.

**Deliverables:**
- Business Strategist Agent
- Product Manager Agent
- Automation Engineer Agent
- Marketing Agent
- Sales Agent
- Related skills and prompt generators

---

## Phase 3 — Autonomous Orchestration System ✅

**Goal:** Create the orchestration layer to autonomously manage multi-agent workflows.

**Status:** Completed. The Orchestrator and Evaluator agents have been implemented alongside the Agent Registry, Skill Registry, and predefined workflow templates.

---

## Phase 3.5A — Genesis Intelligence Architecture ✅

**Goal:** Evolve Genesis into a world-class autonomous AI operating architecture based on modern agentic patterns.

**Status:** Completed. Added 19 new specialized agents across 4 layers (Executive, Development, Business, Quality). Added 14 new skills. Established Genesis Cognitive OS, evaluation metrics, and dynamic skill-loading/agent-selection protocols. Integrated MCP architecture docs.

---

## Phase 4 — Instrumentation

**Goal:** replace judgement with measurement wherever measurement is possible.

| # | Item | Notes |
|---|---|---|
| 2.1 | Test runner | Requires an ADR: which language and runner. Sets `quality_gates.json → testing.coverageEnforced: true` |
| 2.2 | Automated benchmark runner | Executes `prompts/benchmarks/cases.md`, scores against the rubric, records results |
| 2.3 | CI | Runs `verify_structure.ps1` and the test suite on push |
| 2.4 | Session log index | Search across logs by agent, date, and phase — the "read the last two" heuristic stops scaling past ~500 logs |
| 2.5 | Coverage enforcement | Turn on the 80% gate once a runner exists |
| 2.6 | Structure check for source files | Extend the 800-line check beyond markdown |

**Blocked by:** Phase 1. Instrumenting a process nobody has run measures the wrong things.

---

## Phase 5 — Scale

**Goal:** multiple agents working in parallel without losing coherence.

| # | Item | Notes |
|---|---|---|
| 3.1 | Parallel execution model | Fan-out with a collector; the delegation-implies-collection rule made mechanical |
| 3.2 | Shared state protocol | How parallel agents avoid contradicting each other; extends the one-owner-per-artefact rule |
| 3.3 | Cost routing | Make `model_routing.json` operative rather than advisory |
| 3.4 | Conflict resolution | A defined procedure for evidence-resistant agent disagreement |
| 3.5 | Context budget management | Programmatic selective loading of skills and layers |
| 3.6 | Agent evaluation harness | Per-agent quality measurement over time |

**Blocked by:** Phase 2. Parallelism without measurement multiplies unmeasured error.

---

## Phase 6 — Genesis Engine

**Goal:** build the actual engine, inside the harness, using its process.

Scope is deliberately undefined at this point. Defining it is deliverable **1.6**, and it will be
recorded as an ADR rather than assumed here. Writing engine requirements now would be exactly the
aspirational documentation `CLAUDE.md` §5.2 prohibits.

What is already known:
- The `simulation-scientist` and `game-design` agents and the `physics`/`chemistry`/`biology`/
  `astronomy`/`simulation`/`game-development` skills exist because the engine is expected to be
  simulation-heavy and interactive.
- That expectation is an **assumption**, not a decision. ADR 1.6 either confirms or replaces it.

---

## Next Actions

Executable by a fresh agent with no memory of any prior session.

| # | Action | Owner | Blocked by |
|---|---|---|---|
| 1 | Decide what to do with `prompts/system_layers/fable5_layer.md` — see Open Problems | human | operator decision |
| 2 | Run `pwsh -File scripts/auto_commit.ps1 -DryRun -Message "test"` and confirm all gates behave as documented | qa | — |
| 3 | Pick a small real feature and run it through all 8 stages of the Genesis Loop | architect | — |
| 4 | Execute benchmark cases C-001, C-003, and C-008; record baselines in `cases.md` | qa | — |
| 5 | Write ADR 0001 selecting the first real technical target | architect | 3 |

---

## Open Problems

| # | Problem | Severity | Raised | Status |
|---|---|---|---|---|
| 1 | `prompts/system_layers/fable5_layer.md` is a 5,055-line verbatim dump of a different user's Claude Code system prompt, labelled "This is a replacement system prompt". It contains a third party's email address, references a macOS environment, and is not a reasoning layer. `CLAUDE.md` originally pointed to it. | HIGH | 2026-07-28 | **Open** — left untouched; the constitution now points to `L5_reasoning_layer.md` instead. Operator to decide: delete, archive, or keep. |
| 2 | The harness has never been used to build anything; its process claims are unverified in practice | MEDIUM | 2026-07-28 | Open — this is what Phase 1 addresses |
| 3 | Benchmarks are self-scored by the same model that produces the output | MEDIUM | 2026-07-28 | Open — mitigated by behavioural criteria and held-out cases; see `benchmarks/README.md` §Known Bias |
| 4 | `quality_gates.json` sets an 80% coverage target that nothing can currently enforce | LOW | 2026-07-28 | Open by design — `coverageEnforced: false` until Phase 2 |

---

## Phase History

| Phase | Started | Completed | Sessions |
|---|---|---|---|
| 0 — Foundation | 2026-07-28 | 2026-07-28 | `2026-07-28_01_foundation-architecture` |
