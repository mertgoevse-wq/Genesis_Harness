# Genesis Harness — Active Task Tracker

**Current phase:** Founder Operating System (Phase 17)  
**Last updated:** 2026-07-28  
**Session log:** `logs/sessions/2026-07-28_06_founder_operating_system.md`

---

## In Progress

| # | Task | Owner | Status | Notes |
|---|---|---|---|---|
| 1 | Founder Operating System evolution | Architect / CTO | **Review** | Customer intelligence, validation engine, growth enhancements, founder memory, autonomous improvement loop. Tests pass. |
| 2 | Clean runtime artifacts from working tree | DevOps | **Done** | `tests/test_db.json` and `logs/founder_memory.json` now ignored. |
| 3 | Deprecation warning cleanup | Backend | **Done** | Replaced `datetime.utcnow()` with timezone-aware equivalents. |

---

## Backlog

| Priority | Task | Owner | Rationale |
|---|---|---|---|
| High | Add lazy/guarded imports to `orchestrator/master_orchestrator.py` | Architect | Prevents one broken subsystem from crashing the whole orchestrator. |
| High | Generate real visual assets (logo, banner, architecture diagrams) | Designer | GitHub professionalization and project identity. |
| High | Implement live API connectors with key-based adapters | Backend | Replace placeholder intelligence with real market/GitHub/startup data. |
| Medium | Add end-to-end founder-OS integration test | QA | Verify full customer → validation → memory → orchestrator flow. |
| Medium | Add generated `pyproject.toml` to MVP scaffold | Backend | Declare Python >=3.9 requirement for generated products. |
| Medium | Reduce `prompts/system_layers/fable5_layer.md` below 800 lines | Docs | Structure verification warning. |
| Low | Evaluate and remove duplicate/legacy subsystems | Architect | Reduce maintenance surface and confusion. |

---

## Definition of Next Stable Milestone

- [ ] Lazy imports make the orchestrator resilient to broken subsystems.
- [ ] Visual assets are committed to `docs/assets/` and referenced from `README.md`.
- [ ] At least one live connector (e.g., GitHub signals) fetches real data when an API key is provided.
- [ ] All tests pass and structure verification is clean (excluding pre-existing warning).
