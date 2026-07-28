# Genesis Harness — Roadmap

**Version:** 1.2.0 · **Last updated:** 2026-07-28
**Current phase:** 2 — LLM Core & API (in progress)

> This document is the authoritative record of *where the project is*. Update it at the end of
> every phase. `prompts/system_layers/L2_domain_context.md` mirrors the current-state summary —
> keep the two in agreement.

---

## Phase Overview

| Phase | Name | Status | Delivers |
|---|---|---|---|
| **0** | Foundation | **Complete** | Agents, skills, prompts, logging, docs, git automation |
| **1** | Operation / Package Consolidation | **Complete** | Installable `genesis` package, CLI, tests, pruned stubs |
| **2** | LLM Core & API | **In Progress** | LLM-backed reasoning, FastAPI service |
| **3** | Persistency & Multi-User | Planned | PostgreSQL, auth, user projects, analysis history |
| **4** | Monetization & Deployment | Planned | Stripe subscriptions, hosting, CI/CD |
| **5** | Live Market Intelligence | Planned | Real external data connectors, autonomous improvement |

---

## Phase 0 — Foundation ✅

**Goal:** infrastructure that lets multiple AI agents collaboratively develop complex software.

See the original Phase 0 section for details; the foundation remains unchanged.

---

## Phase 1 — Operation / Package Consolidation ✅

**Goal:** turn the existing 60+ directories of stubs and duplicated ideas into a
single installable, testable `genesis/` Python package.

### Delivered

| Subsystem | Artefacts |
|---|---|
| Package definition | `pyproject.toml`, `genesis/` package |
| CLI | `python -m genesis analyze "..."` |
| Decision | `genesis/decision/` (venture + product validation) |
| Intelligence | `genesis/intelligence/` (opportunity detection + live connectors) |
| Revenue | `genesis/revenue/` (pricing, subscriptions, acquisition, experiments) |
| Growth | `genesis/growth/` (growth, SEO, customer intelligence, validation loop) |
| Builder | `genesis/builder/` (MVP builder + deployment planner) |
| Memory | `genesis/memory/` (founder memory + knowledge store) |
| Improvement | `genesis/improvement/` (weakness detection, prioritization, loop) |
| Orchestrator | `genesis/orchestrator.py` |
| Tests | `tests/test_*.py` covering every module and the CLI |
| Scripts | `scripts/consolidate_phase1.py`, `scripts/create_tests.py`, `scripts/fix_init_exports.py`, `scripts/update_verify.py` |

### Success Criteria

- [x] `pip install -e ".[dev]"` succeeds.
- [x] `python -m genesis analyze "..."` returns structured JSON.
- [x] `pytest tests/` passes (31 tests).
- [x] `ruff check genesis/ tests/` passes.
- [x] `scripts/verify_structure.ps1` passes.
- [x] Top-level directories reduced from 60+ to ≤20.
- [x] `genesis/` package has ≤40 Python files.

### Explicitly not delivered

- LLM integration is only the client layer; business modules still use deterministic heuristics.
- Web API / dashboard remains future work (Phase 2/3).
- Database persistence remains future work (Phase 3).
- Real external API integrations remain future work (Phase 5).

### Honest status

The package is now installable and the tests pass. The LLM client layer is in
place with a deterministic fallback, but the business modules still rely on
heuristic scoring. The next step is to wire the client into the decision and
builder modules.

---

## Phase 2 — LLM Core & API

**Goal:** Genesis produces intelligent, prompt-specific analysis and exposes it
via a web API.

**Planned deliverables**

| # | Item | Acceptance criteria |
|---|---|---|
| 2.1 | Anthropic/OpenAI client wrapper | `genesis/llm/client.py` with mockable interface ✅ |
| 2.2 | LLM-backed venture reasoning | `decision/engine.py` enriches deterministic scores with LLM rationale |
| 2.3 | Prompt-specific MVP generation | `builder/mvp.py` generates code that differs meaningfully per prompt |
| 2.4 | FastAPI app | `genesis/api/app.py` with `/api/v1/analyze` and `/health` |
| 2.5 | API key auth | Requests without valid key return 401 |
| 2.6 | Tests | `pytest` covers LLM client, endpoints, and prompt-specific output |

---

## Phase 3 — Persistency & Multi-User

**Goal:** Move from JSON files to a real database and support multiple users.

| # | Item | Notes |
|---|---|---|
| 3.1 | PostgreSQL + SQLAlchemy models | `User`, `Project`, `Analysis` |
| 3.2 | Alembic migrations | `db/migrations/` |
| 3.3 | JWT or Supabase auth | Register/login/profile endpoints |
| 3.4 | Persist analyses | `POST /api/v1/analyze` stores results |
| 3.5 | Project history | Paginated list of analyses per user |

---

## Phase 4 — Monetization & Deployment

**Goal:** Genesis earns revenue and runs in production.

| # | Item | Notes |
|---|---|---|
| 4.1 | Stripe subscriptions | Free / Pro / Enterprise tiers |
| 4.2 | Usage limits | Enforce per-plan analysis quotas |
| 4.3 | Hosted deployment | Fly.io / Railway / Vercel |
| 4.4 | CI/CD | GitHub Actions lint/test/deploy |
| 4.5 | Landing page | Value prop + pricing + CTA |

---

## Phase 5 — Live Market Intelligence

**Goal:** Replace fallback/assumed data with verified external signals.

| # | Item | Notes |
|---|---|---|
| 5.1 | Google Trends / SerpAPI connector | `genesis/intelligence/connectors/google_trends.py` |
| 5.2 | GitHub API connector | Repository and activity signals |
| 5.3 | Product Hunt / Crunchbase connectors | Launch and funding signals |
| 5.4 | Caching & rate limiting | Avoid API quota exhaustion |
| 5.5 | Autonomous improvement loop | Scheduled execution with real metrics |

---

## Next Actions

Executable by a fresh agent with no memory of any prior session.

| # | Action | Owner | Blocked by |
|---|---|---|---|
| 1 | Load the Phase 2 plan and add the LLM client + FastAPI skeleton | architect | — |
| 2 | Add `.env.example` and document API key setup | docs | — |
| 3 | Add the first integration test for `/api/v1/analyze` | qa | #1 |

---

## Open Problems

| # | Problem | Severity | Raised | Status |
|---|---|---|---|---|
| 1 | `prompts/system_layers/fable5_layer.md` is 2,123 lines and contains third-party content. | HIGH | 2026-07-28 | **Resolved** — archived to `_archive/prompts/system_layers/fable5_layer.md`. |
| 2 | All intelligence signals are fallback/assumed; no real external data yet. | MEDIUM | 2026-07-28 | Open — Phase 5 addresses this. |
| 3 | MVP builder output is still largely template-based and not prompt-specific. | MEDIUM | 2026-07-28 | Open — Phase 2 addresses this. |

---

## Phase History

| Phase | Started | Completed | Sessions |
|---|---|---|---|
| 0 — Foundation | 2026-07-28 | 2026-07-28 | `2026-07-28_01_foundation-architecture` |
| 1 — Operation / Package Consolidation | 2026-07-28 | 2026-07-28 | `2026-07-28_07_phase1_consolidation` |
