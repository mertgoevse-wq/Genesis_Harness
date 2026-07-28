# ADR-0001 — Consolidate Genesis into a Single Python Package

**Date:** 2026-07-28
**Status:** accepted
**Deciders:** Principal Software Architect (AI session) + human operator
**Session:** 2026-07-28_07_phase1_consolidation

---

## 1. Context

The repository had grown to more than 60 top-level directories and 519 Python
files. Most of the new directories were stubs or duplicate conceptual modules.
There was no installable package, no CLI, and no working test runner. The
project could not be imported or executed as a unit. The architecture audit
identified the need for a radical consolidation before any further capability
work could succeed.

**Constraints in force:**

| Constraint | Value | VERIFIED / ASSUMED |
|---|---|---|
| Python version | >= 3.10 | VERIFIED |
| Linting | ruff | VERIFIED |
| Testing | pytest | VERIFIED |
| No real external APIs in Phase 1 | true | ASSUMED (per approved plan) |

---

## 2. Decision

Consolidate the real core logic into a single installable `genesis/` Python
package, remove or archive the duplicate/stub directories, and expose the
runtime through a CLI entry point. The package layout follows the approved
Phase 1 development plan.

**Because:** the project was unbuildable, untestable, and unmaintainable at its
previous scale of empty modules.

---

## 3. Options Considered

### Option A — Keep all directories and incrementally refactor  ← rejected
- **Shape:** Leave every top-level package in place and slowly merge them.
- **Pros:** Preserves every file path; minimal immediate churn.
- **Cons:** 60+ directories remain; no installable package; tests cannot run;
  every future change touches many import paths.
- **Fails when:** any new feature needs to import more than a handful of
  modules, because the dependency graph is a mess of stubs.

### Option B — Consolidate into `genesis/` package, archive or delete legacy dirs  ← chosen
- **Shape:** Move real logic to `genesis/{decision,intelligence,revenue,growth,builder,memory,improvement}`,
  add `pyproject.toml`, CLI, and a focused test suite; archive or delete the rest.
- **Pros:** Single installable package; tests pass; clear module boundaries;
  ready for Phase 2 LLM/API work.
- **Cons:** Large diff; old import paths removed; archived stubs still occupy
  disk if not ignored.
- **Fails when:** a future phase needs a deleted module's code, but the
  archive contains the original stubs.

---

## 4. Consequences

**Positive:**
- `pip install -e ".[dev]"` works.
- `python -m genesis analyze "..."` returns structured JSON.
- `pytest` passes with 31 tests covering all consolidated modules.
- `ruff check` passes.
- Repository is now buildable, testable, and ready for LLM integration.

**Negative — accepted costs:**
- Large one-time diff.
- Some historical phase directories are no longer in the main tree.
- Old session logs and references to deleted modules remain in `logs/` and may
  become stale.

**Now harder to do:**
- Refer to old module paths by import; they no longer exist.

**Now locked in:**
- The `genesis/` package structure and module boundaries.

---

## 5. Reversal Trigger

**We revisit this if:** the Phase 2 LLM work reveals that a critical piece of
legacy logic was deleted rather than archived, or the package layout cannot
support the FastAPI service planned for Phase 2.

**Cost of reversal at that point:** moderate — would require restoring an
archived module or adding a new subpackage.

---

## 6. Verification

| Claim underpinning this decision | Label | Source |
|---|---|---|
| Package installs | VERIFIED | `pip install -e ".[dev]"` executed successfully |
| CLI runs | VERIFIED | `python -m genesis analyze "..."` produced JSON |
| Tests pass | VERIFIED | `pytest tests/ -v` reported 31 passes |
| Linter passes | VERIFIED | `ruff check genesis/ tests/` reported no errors |
| Structure check passes | VERIFIED | `scripts/verify_structure.ps1` passed (one pre-existing warning) |

---

## 7. Affected Artefacts

| Artefact | Change required |
|---|---|
| `pyproject.toml` | Created |
| `genesis/` | Created as consolidated package |
| `tests/` | Replaced with focused test suite |
| `docs/ARCHITECTURE.md` | Updated with package layout |
| `docs/ROADMAP.md` | Updated current phase to 1 |
| `README.md` | Updated quick-start instructions |
| `.gitignore` | Added `_archive/` entry |
| Old top-level directories | Deleted or moved to `_archive/` |

---

## 8. References

- `plans/DEVELOPMENT_PLAN_v1.md`
- `docs/ARCHITECTURE_AUDIT_2026-07-28.md`
