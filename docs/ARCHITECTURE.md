# Genesis Harness — Architecture

**Version:** 1.0.0 · **Last updated:** 2026-07-28 · **Phase:** 0 — Foundation

---

## 1. What This System Is

Genesis Harness is an **AI development operating system**: infrastructure that lets multiple
specialised AI agents collaboratively design, build, verify, and document complex software, with
continuity across sessions and across models.

It is not the Genesis Engine. It is the harness the Genesis Engine will later be built inside.

**The central problem it solves:** an AI session is amnesiac, its confidence is uncorrelated with
its correctness, and its output quality degrades as scope grows. The harness addresses each with
structure rather than with exhortation.

| Problem | Mechanism |
|---|---|
| Sessions forget | Append-only session logs + handoff artefacts + the cold-start test |
| Confidence ≠ correctness | Mandatory verification states, confidence labels, QA authority to block |
| Quality degrades with scope | Role separation, one owner per artefact, decomposition into cold-startable units |
| Process drifts | Layered prompts, machine-readable registry, scripted gates |

---

## 2. Subsystem Map

```
                         ┌──────────────┐
                         │   CLAUDE.md  │  Constitution — highest authority
                         │ (the rules)  │  after explicit human instruction
                         └───────┬──────┘
                                 │ governs
         ┌───────────────────────┼───────────────────────┐
         ▼                       ▼                       ▼
  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
  │   AGENTS    │ loads   │   SKILLS    │         │   PROMPTS   │
  │   (who)     │────────▶│   (what     │         │   (how they │
  │             │         │  they know) │         │  are told)  │
  │ agents/     │         │ skills/     │         │ prompts/    │
  │ .claude/    │         │             │         │             │
  └──────┬──────┘         └─────────────┘         └──────┬──────┘
         │                                                │
         │ produce                          compose into ─┘
         ▼
  ┌─────────────┐         ┌─────────────┐         ┌─────────────┐
  │   OUTPUTS   │────────▶│    LOGS     │         │    DOCS     │
  │  handoffs,  │ recorded│  (memory)   │ inform  │  (truth)    │
  │  code, ADRs │  in     │  logs/      │────────▶│  docs/      │
  └──────┬──────┘         └─────────────┘         └─────────────┘
         │
         │ gated by
         ▼
  ┌─────────────┐         ┌─────────────┐
  │   SCRIPTS   │ reads   │   CONFIGS   │
  │ (enforce)   │────────▶│ (registry)  │
  │ scripts/    │         │ configs/    │
  └─────────────┘         └─────────────┘
```

---

## 3. Components

| Component | Responsibility | Owns | Depends on |
|---|---|---|---|
| **Constitution** (`CLAUDE.md`) | Defines roles, philosophy, workflow, rules, quality bar | The rules | Nothing |
| **Agents** (`agents/`, `.claude/agents/`) | Roles with scope, authority, workflow, output contract | Their deliverables | Constitution, skills, prompts |
| **Skills** (`skills/`) | Knowledge domains + domain-specific guardrails | Domain competence | Nothing |
| **Prompts** (`prompts/`) | Layered instruction composition and benchmarking | Instruction shape | Constitution |
| **Logs** (`logs/`) | Append-only session memory | Project history | Nothing |
| **Docs** (`docs/`) | Current-state truth: architecture, agents, workflow, roadmap | Shared understanding | Everything above |
| **Configs** (`configs/`) | Machine-readable registry and thresholds | Operative numbers | Nothing |
| **Scripts** (`scripts/`) | Enforcement: commit gates, structure checks, log creation | Automation | Configs |
| **Templates** (`templates/`) | Structural forms for artefacts | Artefact uniformity | Nothing |

---

## 4. The Three Core Separations

The whole design rests on three separations. Collapsing any of them is what makes multi-agent
systems fail.

### 4.1 Role vs Knowledge — agents vs skills

An **agent** is *who does the work*: a scope, an authority, a workflow, an output contract.
A **skill** is *what it knows*: a domain, its methods, its guardrails.

Six agents × nine skills would be fifty-four documents if fused. Separated, an agent gains a new
domain by loading a skill, and a skill improves for every agent at once.

**Test:** if the answer to "why do we need this?" is *"it needs to know about X"*, you want a
skill. If it is *"someone must own deciding X"*, you want an agent.

### 4.2 Stable vs Volatile — the prompt layers

| Layer | Volatility |
|---|---|
| L0 identity, L1 principles, L4 output contract | Rare |
| L2 domain context | Per phase |
| L3 task contract | Per task |
| L5 reasoning layer | Rare, opt-in |

A correction placed in the wrong layer either evaporates (behaviour fix put in L3) or contaminates
everything (task fix put in L0). The routing table in `prompts/README.md` exists to prevent this.

### 4.3 Claim vs Evidence — verification states

Three states, never blurred: **verified** (executed and observed) · **implemented** (exists,
unrun) · **planned** (does not exist).

Four confidence labels for external claims: **VERIFIED** · **KNOWN** · **ASSUMED** · **UNKNOWN**.

This separation is why the QA Agent can block a commit and why a benchmark's truthfulness axis
can reject an output outright.

---

## 5. Data Flow — The Genesis Loop

```
 human request
      │
      ▼
 ┌──────────┐   task contract (L3)
 │ 1 INTAKE ├──────────────────────────┐
 └──────────┘                          │
      │                                ▼
      ▼                          ┌───────────┐
 ┌──────────┐  findings report   │  research │
 │2 RESEARCH│◀───────────────────┤   agent   │
 └────┬─────┘                    └───────────┘
      │ verified constraints
      ▼
 ┌──────────┐  architecture spec + ADR + implementation units
 │ 3 DESIGN │◀── architect agent
 └────┬─────┘
      │ handoff (contracts, acceptance criteria)
      ▼
 ┌──────────┐
 │ 4 PLAN   │  units decomposed until cold-startable
 └────┬─────┘
      │
      ▼
 ┌──────────┐  code + verification evidence
 │ 5 BUILD  │◀── coding agent  (+ simulation-scientist / game-design specs)
 └────┬─────┘
      │ handoff (what was verified, what was not)
      ▼
 ┌──────────┐  QA report — VERDICT
 │ 6 VERIFY │◀── qa agent          ── CRITICAL ──▶ back to BUILD
 └────┬─────┘
      │ PASS
      ▼
 ┌──────────┐  session log written to logs/sessions/
 │ 7 LOG    │
 └────┬─────┘
      │
      ▼
 ┌──────────┐  auto_commit.ps1 — 9 gates
 │ 8 COMMIT │
 └──────────┘
```

**Artefacts are the transport, not conversation.** Every arrow above is a file, which is what
makes the loop survive a context reset.

---

## 6. Invariants

Statements that must be true at all times. Violating one is a defect, not a style choice.

| # | Invariant | Enforced by |
|---|---|---|
| 1 | Every registered agent has both a charter and a runtime adapter | `verify_structure.ps1` |
| 2 | Every registered skill has a `SKILL.md` | `verify_structure.ps1` |
| 3 | Exactly one agent holds authority over any given artefact | Review (`agents/README.md` §Collaboration) |
| 4 | Every session that changes the repository has a session log | `auto_commit.ps1` gate 6 |
| 5 | No commit contains credential-shaped content | `auto_commit.ps1` gate 3 |
| 6 | Session logs are append-only | Constitution §7.3; review |
| 7 | A `PASS` verdict requires actual execution | QA charter; `quality_gates.json` |
| 8 | Every external claim carries a confidence label | L4 output contract |
| 9 | The charter is authoritative over its adapter | `agents/README.md` |
| 10 | Config numbers are operative over constitution prose | `CLAUDE.md` §9 |
| 11 | No markdown file exceeds 800 lines | `verify_structure.ps1` (warning) |
| 12 | Every script parses without syntax errors | `verify_structure.ps1` |

---

## 7. Load Envelope

The foundation is documentation and scripts, so the relevant limits are **context** and
**maintenance**, not throughput.

| Dimension | Now | Comfortable | Breaks at |
|---|---|---|---|
| Agents | 6 | ~12 | Beyond ~15, authority overlap becomes hard to reason about |
| Skills | 9 | ~20 | Beyond ~25, skill selection itself needs tooling |
| Session logs | 0 | ~500 | Reading "the last two" stays O(1); search needs an index past ~500 |
| Full-context load | ~4k lines of markdown | ~8k | Selective loading is already required; L2 exists to bound it |
| Structure check | <1s | — | Line-counting every markdown file becomes slow past ~2000 files |

**First bottleneck:** context, not compute. This is why skills are loaded selectively, why L2
carries only current-phase facts, and why agents read the two most recent logs rather than all of
them.

---

## 8. Design Decisions

| Decision | Alternative rejected | Reason |
|---|---|---|
| Charter + adapter split for agents | Single file in `.claude/agents/` | Native adapters must stay short to be cheap to load; charters must be long to be complete |
| Skills as a separate axis from agents | Knowledge embedded in each agent | Avoids N×M duplication; a skill improvement propagates to every agent that loads it |
| Layered prompts (L0–L5) | One system prompt per agent | Makes a fix land in one place and routes it correctly by volatility |
| PowerShell scripts | Cross-platform shell or Node | The environment is Windows-first; adding a runtime needs an ADR |
| JSON registry driving the structure check | Hardcoded file lists in the script | Registering a component automatically extends verification |
| Append-only logs | Editable status document | The history of what was believed is evidence; rewriting it destroys the audit trail |
| Manual benchmarks | Automated runner now | An honest manual method beats a fake automated one; the runner is Phase 2 |

Decisions taken from Phase 1 onward are recorded as ADRs in `docs/adr/`.

---

## 9. What Does Not Exist Yet

Stated explicitly so nobody documents aspiration as fact:

- **No runtime code.** The repository is specification, documentation, and PowerShell scripts.
- **No test runner.** Verification is by script execution and structural checks.
- **No automated benchmark runner.** Cases are defined; execution is manual.
- **No ADRs.** `docs/adr/` is established by convention; the first ADR arrives with Phase 1.
- **No CI.** Gates run locally via `auto_commit.ps1`.
- **No Genesis Engine.** That is the point of the harness, not part of it.

See `docs/ROADMAP.md` for when each of these is scheduled.

---

## 10. Autonomous Orchestration Layer

The autonomous orchestration layer acts as the executive control system, managing workflows, delegating tasks to specific agents based on the Agent Registry and Skill Registry, and tracking execution. The Orchestrator Agent executes predefined workflows (e.g., product creation, automation creation) and triggers the Evaluator Agent to verify the quality of all generated outputs according to the Evaluation Rubric.

---

## 11. Genesis Cognitive OS (Phase 3.5A)

The core intelligence layer connecting the harness's capabilities.

- **4-Layer Agent Architecture**: Executive, Development, Business, and Quality layers containing over 30 specialized agents.
- **Dynamic Skill Loading**: Evaluates complexity and injects necessary knowledge modules into agent context based on `skill_loading_protocol.md`.
- **Agent Selection**: Primary and support agent routing via `agent_selection_protocol.md`.
- **Self Improvement**: Post-task evaluation of missed capabilities or knowledge gaps (`self_improvement_protocol.md`).
- **MCP Integration**: Connection to external tools and databases, governed by security and validation rules in `docs/MCP_ARCHITECTURE.md`.
- **Benchmarking**: Explicit agent, product, and code evaluation rubrics stored in `prompts/benchmarks/genesis_evaluation/`.


## Genesis Intelligence Harvester
The Harvester sits alongside the Agent layer. It comprises Discovery, Ranking, Analysis, Knowledge Graph, Engine, and Prompt Lab modules. It feeds abstract architectural patterns back into the Genesis Core via formal Improvement Proposals (ADRs).


## Autonomous AI Operating System Layer
Genesis operates as an autonomous OS. The `orchestration/` package schedules DAG-resolved tasks to an `AgentWorkerPool`, while `core/model_router/` evaluates task types and dispatches prompts to the optimal LLM backend.


## Genesis Intelligence Harvester v2
Harvester v2 expands data connectors across GitHub, HuggingFace, arXiv, PapersWithCode, Anthropic, Google, OpenAI, LangChain, LangGraph, CrewAI, AutoGen, and MCP Registry. It extracts concepts into a Knowledge Graph (Agent, Skill, Tool, Pattern, Workflow) and outputs Genesis Improvement Proposals (GIPs).


## Genesis Control Center
Genesis Control Center (`control-center/`) provides real-time visual telemetry. It includes an `EventBus` (`events/`), a Python HTTP/WebSocket server (`backend/`), and a clean Linear/Notion-inspired single page web application (`frontend/`) to visualize agent hierarchies, running DAG tasks, model router allocations, costs, and logs.


## Genesis Runtime Engine
Genesis Runtime Engine (`genesis_runtime/`) provides the end-to-end execution environment. It coordinates goal decomposition (`planner/`), explicit agent lifecycle state transitions (`CREATED -> PLANNING -> READY -> RUNNING -> EVALUATING -> COMPLETED/FAILED`), dynamic skill loading (`skill_system/`), memory persistence (`memory/`), and event emission (`events/`).


## Genesis Persistent Intelligence Memory System
Genesis Memory System (`memory_system/`) persists long-term architectural insights, successful workflows, prompt structures, failures, and benchmark results. It syncs with the `harvester/knowledge_graph` and features semantic retrieval (`retrieval/`) and post-project retrospectives (`learning/agent_memory.py`).


## Genesis Self Evolution Loop
Genesis Self Evolution Loop (`evolution/`) continuously monitors agent execution metrics (`evaluation/`), identifies prompt or skill weaknesses (`optimization/`), executes benchmark experiments (`experiments/`), and generates Genesis Evolution Reports in `docs/evolution/` (`proposals/`). Self-modifications are strictly non-autonomous and require formal approval.


## Genesis Tool Intelligence & MCP Architecture
Genesis Tool Intelligence (`tool_intelligence/`) and MCP System (`mcp/`) discover, evaluate, and sand-box external tools and Model Context Protocol servers. It maintains `configs/tool_registry.json` and `configs/mcp_registry.json`, dynamically routing tools to agents based on security constraints and capability matching.


## Genesis Autonomous Product Factory Architecture
Genesis Autonomous Product Factory (`product_factory/`) orchestrates end-to-end AI product creation (`IDEA -> RESEARCHING -> VALIDATING -> DESIGNING -> BUILDING -> TESTING -> DEPLOYING -> LAUNCHED -> LEARNING`). It utilizes specialized agents (`product-founder`, `customer-researcher`, `business-modeler`, `ux-researcher`, `growth-strategist`, `financial-analyst`, `investor-agent`), PRD generation (`product_management/prd_generator.py`), and binds directly to Genesis Runtime, Harvester, and Memory System.


## Genesis Autonomous Founder Intelligence Architecture
Genesis Founder Intelligence (`founder_intelligence/`) scans market trends (`market_scanner/`), generates top 50 AI business opportunities (`idea_engine/`), calculates 0-100 StartupScores (`startup_analysis/`), and runs simulated VC investment reviews (`investor_engine/`). High-scoring startup candidates (>80) are passed directly into the Product Factory.


## Genesis Autonomous Venture & Engineering OS (Phase 7)
Phase 7 elevates Genesis Harness into the **Genesis Autonomous Venture & Engineering Operating System**. Key additions include:
- **Venture Pipeline (`venture_pipeline/`)**: End-to-end opportunity scanning, demand prediction, business model generation, VC simulation, and runtime building.
- **Knowledge Graph (`knowledge_graph/`)**: Expanded relationship engine mapping Agents, Skills, Tools, Models, Products, and Code Patterns.
- **Agent Factory (`agent_factory/`)**: Dynamic agent team assembly based on prompt domain context.
- **Model Performance Tracker (`core/model_router/`)**: Task complexity analysis and fallback routing.


## Genesis Autonomous Venture Execution Platform (Phase 8)
Phase 8 transforms Genesis Harness into an active, production-grade **Autonomous Venture Execution Platform**:
- **Venture Execution Engine (`venture_execution/`)**: Drives execution graphs through startup creation, product validation, and SaaS launches.
- **Agent Collaboration Protocol (`agent_collaboration/`)**: Multi-agent task handoffs, shared context, and result aggregation.
- **Skill Intelligence Engine (`skill_intelligence/`)**: Automated skill detection, ranking, and dependency loading.
- **Autonomous Project Memory (`memory_system/project_memory/`)**: Tracks complete milestone timelines from idea to post-launch.
- **Quality Intelligence (`quality_intelligence/`)**: Multi-dimension quality scoring for architecture, business, market, and technical execution.
- **Execution Tools (`execution_tools/`)**: Tool selection and security boundary checks.


## Genesis Autonomous Software Engineering Factory (Phase 9)
Phase 9 transforms Genesis into an autonomous **Software Engineering Factory**:
- **Software Factory Engine (`software_factory/`)**: Requirements analysis, architecture planning, development, testing, code review, and deployment release.
- **Engineering Team Assembly (`engineering_team/`)**: Coordinates team formation across Architect, Developers, QA, Security, and DevOps.
- **Coding Pipeline (`coding_pipeline/`)**: Requirement -> Architecture -> Issues -> Implementation -> Testing -> Review -> Security -> Release.
- **GitHub Engine (`github_engine/`)**: Repository analysis, issue creation, branch planning, and PR generation.
- **Code & Testing Intelligence (`code_intelligence/` & `testing_intelligence/`)**: Repository parsing, code quality scoring, and automated coverage analysis.
- **Security Engineering Layer (`security_intelligence/`)**: Secret scanning, vulnerability risk analysis, and permission review.


## Genesis Autonomous Research & Scientific Intelligence Platform (Phase 10)
Phase 10 transforms Genesis into a **Scientific Research Intelligence Platform**:
- **Autonomous Research Engine (`research_intelligence/`)**: Research orchestrator, paper scanning, trend detection, hypothesis evaluation, experiment design, and report generation.
- **Scientific Source Connectors (`research_connectors/`)**: Connectors for arXiv, PapersWithCode, HuggingFace, and DeepMind/Anthropic/OpenAI research feeds.
- **Scientific Memory (`memory_system/research_memory/`)**: Long-term research discoveries and hypothesis history.
- **Research Benchmarking (`research_benchmarks/`)**: Evaluates novelty score, evidence quality, and reasoning quality.
- **Specialized Research Agents**: Research Director, Scientific Analyst, Experiment Designer, Technology Scout.
- **Research Discoveries**: Integrated with Evolution Loop under `docs/evolution/research_discoveries/`.


## Genesis Autonomous Knowledge & Intelligence Fabric (Phase 11 Fabric)
Phase 11 introduces the central **Knowledge & Intelligence Fabric**:
- **Knowledge Fabric Core (`knowledge_fabric/core/`)**: Knowledge orchestrator, intelligence router, context manager.
- **Subsystem Connectors (`knowledge_fabric/connectors/`)**: Connectors for agents, skills, tools, memory, research, and venture pipelines.
- **Cross-Domain Reasoning Engine (`knowledge_fabric/reasoning/`)**: Cross-domain reasoner, decision engine, recommendation engine.
- **Global Context System (`global_context/`)**: Context builder, ranker, and retriever.


## Genesis Autonomous Agent Runtime 2.0 (Phase 12)
Phase 12 transforms Genesis into a distributed **Autonomous Agent Runtime 2.0**:
- **Runtime Core (`agent_runtime/core/`)**: Full lifecycle state machine (`CREATED`, `INITIALIZING`, `LOADING_CONTEXT`, `EXECUTING`, `COMMUNICATING`, `WAITING`, `EVALUATING`, `LEARNING`, `COMPLETED`, `FAILED`).
- **Parallel Execution Graph (`agent_runtime/execution/`)**: Parallel executor, task queue, and dependency graph manager.
- **Message Bus Integration (`agent_collaboration/message_bus.py`)**: Inter-agent messaging bus, conversation memory, and knowledge sharing.
- **Self-Reflection & Telemetry (`agent_runtime/reflection/` & `telemetry/`)**: Execution review, failure analysis, and dashboard telemetry.


## Genesis Live Control Center + Product Interface (Phase 13)
Phase 13 delivers a live human-facing dashboard and product interface:
- **Control Center Backend API (`control-center/backend/api_server.py`)**: REST endpoints serving system status, active agents, skills, workflows, projects, telemetry, and quality scores.
- **Genesis Dashboard Application (`control-center/frontend/`)**: Modern dark-mode Web Dashboard UI (`index.html`, `style.css`, `app.js`).
- **Real User Workflow (`scripts/run_saas_idea_workflow.py`)**: End-to-end execution script triggering Founder Intelligence & Research Intelligence to produce validated SaaS venture specifications.


## Genesis Autonomous Product Launch Engine (Phase 14)
Phase 14 transforms Genesis into an autonomous **Product Launch Engine**:
- **Autonomous Product Generation Pipeline (`product_launch/`)**: Idea processing, product spec generation, business plan generation, codebase planning, landing page creation, and marketing strategy.
- **Generated Product Workspaces (`generated_products/<product_name>/`)**: Complete product packages containing `README.md`, `BUSINESS_PLAN.md`, `MARKET_ANALYSIS.md`, `PRD.md`, `TECHNICAL_ARCHITECTURE.md`, `ROADMAP.md`, `SECURITY_REVIEW.md`, `DEPLOYMENT_PLAN.md`, and `MARKETING_PLAN.md`.
- **Real Standalone Demo Workflow (`scripts/run_product_launch.py`)**: End-to-end execution script creating complete product packages from high-level prompts.


## Genesis Autonomous Venture Operating System (Phase 16 — Current Evolution)

The next evolution of Genesis Harness transforms it from an AI development framework into an
autonomous business operating system. Five new subsystems were added to support end-to-end
venture creation:

| Subsystem | Responsibility | Key Files |
|---|---|---|
| **Opportunity Intelligence** | Discover market opportunities, technology trends, and SaaS ideas | `opportunity_intelligence/` |
| **Venture Decision Engine** | Score venture ideas across market, competition, monetization, technical complexity, and risk | `venture_decision/` |
| **Deployment Intelligence** | Generate deployment configurations for Docker, Vercel, Supabase, and cloud | `deployment_intelligence/` |
| **Revenue Intelligence** | Recommend pricing, subscription models, acquisition channels, and growth experiments | `revenue_intelligence/` |
| **Self-Improvement Loop** | Detect weaknesses, prioritize improvements, and evaluate results | `self_improvement/` |

These subsystems are wired into `orchestrator/master_orchestrator.py`, which now produces a richer
autonomous cycle output including opportunities, venture decision, revenue strategy, deployment
plan, and self-improvement tasks.

### Data Flow

```
 human goal
      │
      ▼
 ┌─────────────────────────────────────┐
 │       Opportunity Intelligence        │
 │  (signals, trends, competitor gaps)   │
 └─────────────┬─────────────────────────┘
               ▼
 ┌─────────────────────────────────────┐
 │        Venture Decision Engine      │
 │  (GO / MAYBE / NO-GO with scores)  │
 └─────────────┬─────────────────────────┘
               ▼
 ┌─────────────────────────────────────┐
 │        Revenue Intelligence         │
 │  (pricing, subscriptions, growth)   │
 └─────────────┬─────────────────────────┘
               ▼
 ┌─────────────────────────────────────┐
 │       Deployment Intelligence       │
 │  (Docker, Vercel, Supabase, cloud)   │
 └─────────────┬─────────────────────────┘
               ▼
 ┌─────────────────────────────────────┐
 │       Self-Improvement Loop         │
 │  (weakness detection, task queue)   │
 └─────────────────────────────────────┘
```

## Genesis Autonomous MVP Builder & Deployment Engine (Phase 15)
Phase 15 transforms Genesis into an autonomous **MVP Builder**:
- **Autonomous MVP Codebase Pipeline (`mvp_builder/`)**: Product analysis, system architecture design, schema design, API design, frontend generation, backend generation, test generation, and deployment packaging.
- **Generated MVP Workspace (`generated_products/<product>/mvp/`)**: Fullstack application codebase containing `frontend/`, `backend/`, `database/`, `tests/`, `docker/`, `docs/`, `README.md`, `ARCHITECTURE.md`, `API_SPEC.md`, `DATABASE_SCHEMA.md`, and `DEPLOYMENT.md`.
- **Real Standalone Demo Workflow (`scripts/run_mvp_builder.py`)**: End-to-end execution script creating complete application codebases from prompts.


## Genesis Revenue-Driven Evolution (Phase 16+)

Phase 16+ hardens Genesis into a revenue-driven autonomous SaaS company by adding
production-grade business intelligence modules and richer product generation.

| Subsystem | Responsibility | Key Files |
|---|---|---|
| **Live Intelligence** | Real-world data connectors with caching/fallback for market, SaaS, GitHub, and startup signals | `live_intelligence/` |
| **Product Validation Engine** | GO / MODIFY / REJECT verdicts with confidence scores across market, competition, pricing, pain, complexity, acquisition, and revenue | `product_validation_engine/` |
| **Growth Intelligence** | Landing page optimization, SEO planning, acquisition channels, and growth experiments | `growth_intelligence/` |
| **Upgraded MVP Builder** | Production-quality FastAPI + SQLAlchemy + Pydantic scaffold with tests and Docker | `mvp_builder/builder_engine.py` |
| **Upgraded Deployment Intelligence** | Real Docker, Vercel, Supabase, and cloud artifact templates with production checklists | `deployment_intelligence/providers/` |

These modules are wired into `orchestrator/master_orchestrator.py`, producing a richer
DISCOVER → ANALYZE → VALIDATE → DECIDE → BUILD → DEPLOY → MARKET → MEASURE → IMPROVE loop.


## Genesis Founder Operating System (Phase 17 — Current Evolution)

Phase 17 transforms Genesis into a founder-centric autonomous SaaS company by adding deep
customer intelligence, continuous validation, founder memory, and a self-improving execution loop.

| Subsystem | Responsibility | Key Files |
|---|---|---|
| **Customer Intelligence** | Personas, ICP discovery, pain points, objections, buying signals, interview scripts | `customer_intelligence/` |
| **Validation Engine** | Continuous validation loop for landing pages, value props, pricing, and demand | `validation_engine/` |
| **Growth Intelligence (Enhanced)** | Channel analysis, SEO opportunities, content strategy, growth loops, conversion experiments | `growth_intelligence/` |
| **Founder Decision Memory** | Persist decisions, successful patterns, failed ideas, and rationale | `memory_system/founder_memory/` |
| **Autonomous Improvement Loop** | Self-audit, weakness detection, task prioritization, and execution | `self_improvement/autonomous_improvement_loop.py` |

### Extended Data Flow

```
 human goal
      │
      ▼
 ┌─────────────────────────────────────┐
 │       Opportunity Intelligence        │
 └─────────────┬─────────────────────────┘
               ▼
 ┌─────────────────────────────────────┐
 │          Customer Intelligence        │
 │   (personas, ICP, pain, objections)   │
 └─────────────┬─────────────────────────┘
               ▼
 ┌─────────────────────────────────────┐
 │          Validation Engine            │
 │   (BUILD / PIVOT / ABANDON)         │
 └─────────────┬─────────────────────────┘
               ▼
 ┌─────────────────────────────────────┐
 │        Venture Decision Engine      │
 └─────────────┬─────────────────────────┘
               ▼
        ... BUILD → DEPLOY → MARKET ...
               ▼
 ┌─────────────────────────────────────┐
 │       Founder Decision Memory         │
 │   (record rationale for learning)     │
 └─────────────┬─────────────────────────┘
               ▼
 ┌─────────────────────────────────────┐
 │     Autonomous Improvement Loop     │
 │   (audit, detect, prioritize, act)  │
 └─────────────────────────────────────┘
```
