# Genesis Harness — Workflow

**Version:** 1.0.0 · **Last updated:** 2026-07-28

The operating process. This document is procedural — what to do, in what order, with what gate
at each step. The reasoning behind it is in [`ARCHITECTURE.md`](ARCHITECTURE.md); the rules it
enforces are in [`CLAUDE.md`](../CLAUDE.md).

---

## 1. Session Bootstrap

Run this at the start of every session, before touching anything.

```powershell
# 1. Understand the working state BEFORE changing it
git -C C:\Genesis_Harness status

# 2. Verify the structure is intact
pwsh -File scripts/verify_structure.ps1

# 3. Open a session log
pwsh -File scripts/new_session_log.ps1 -Slug "<short-kebab-slug>"
```

Then read, in order:

| # | Read | For |
|---|---|---|
| 1 | `CLAUDE.md` | The rules |
| 2 | `docs/ROADMAP.md` | Current phase and next actions |
| 3 | The two most recent `logs/sessions/*.md` | Work queue, open problems, assumptions in force |
| 4 | The owning agent's charter | The contract you are working under |

**Declare the owning agent before starting.** Every task belongs to exactly one.

---

## 2. The Genesis Loop

| # | Stage | Owner | Produces | Gate to pass |
|---|---|---|---|---|
| 1 | **Intake** | any | Task contract (L3) | Acceptance criteria exist and are objectively checkable |
| 2 | **Research** | research | Findings report | Every claim labelled; no unretrieved citations |
| 3 | **Design** | architect | Architecture spec + ADR | Every component has a contract; decision has a reversal trigger |
| 4 | **Plan** | architect | Implementation units | Each unit passes the cold-start test |
| 5 | **Build** | coding | Code + evidence | Executed, or honestly marked `implemented-not-run` |
| 6 | **Verify** | qa | QA report | Verdict is PASS or PASS WITH FINDINGS; no CRITICAL |
| 7 | **Log** | any | Session log | All required fields; real test output |
| 8 | **Commit** | any | Commit + push | All nine `auto_commit.ps1` gates |

**Stages may be compressed for small work. Skipping a stage must be stated explicitly** in the
session log — "no research stage; the API was already verified in session 2026-07-28_01."

---

## 3. Stage Detail

### Stage 1 — Intake
Write the task contract using `prompts/system_layers/L3_task_contract.md`.

- Goal is one sentence describing an **end state**, not an activity.
- **Scope OUT is mandatory** — it preserves the operator's decision about size.
- Every acceptance criterion names its verification method.

> **A task without acceptance criteria is not a task. Send it back.**

### Stage 2 — Research
Only when something about the outside world is unknown and load-bearing.

- Skip it explicitly when nothing is unknown; do not perform ceremonial research.
- Every finding is labelled VERIFIED / KNOWN / ASSUMED / UNKNOWN.
- A "could not determine" section is always present.

### Stage 3 — Design
Required when the change crosses a component boundary, adds a dependency, or selects a technology.

- At least two genuinely different options.
- Decision + one-sentence reason + **reversal trigger**.
- Every component gets a contract. Every performance-sensitive design gets a load envelope.
- ADR written to `docs/adr/NNNN-title.md`.

### Stage 4 — Plan
Decompose into implementation units.

- **Stop decomposing when a unit fits one context.** Depth is an outcome, not a goal.
- Each unit: goal, inputs, acceptance criteria, owning agent.
- Apply the cold-start test to each.

### Stage 5 — Build
- Read the surrounding code first; match its conventions; reuse what exists.
- Write the failing test first where a runner exists. Where none exists, **write down the manual
  verification command before implementing** — deciding how to verify afterwards produces
  verification that fits the code rather than the requirement.
- Execute. Capture the exact command and exact output.
- Harden boundaries and error paths. Then refine and re-run.

### Stage 6 — Verify
- **Derive the test plan from the acceptance criteria before reading the implementation.**
- Security pass first, always.
- Evidence pass: check every verification claim against real output.
- If it could not be executed, the verdict is `NOT VERIFIED` — never `PASS`.
- **CRITICAL blocks the commit.**

### Stage 7 — Log
Fill `logs/SESSION_TEMPLATE.md` completely.

- The **reasoning summary** is the point — record why, including options rejected.
- The **tests section takes real output**. "Not run" is honest; invention is a CRITICAL violation.
- **Next actions must be executable by a fresh agent** with no memory of the session.

### Stage 8 — Commit
```powershell
pwsh -File scripts/auto_commit.ps1 -Message "<type>: <description>" -DryRun   # inspect first
pwsh -File scripts/auto_commit.ps1 -Message "<type>: <description>" -Push
```

---

## 4. Gates

### Commit gates (`auto_commit.ps1`)

| # | Gate | Blocking | Escape hatch |
|---|---|---|---|
| 1 | Repository check | yes | — |
| 2 | Change check | yes | — |
| 3 | Secret scan | yes | none by design |
| 4 | Large file check | no (warns) | — |
| 5 | Structure check | yes | `-SkipStructureCheck` |
| 6 | Session log check | yes | `-AllowNoSessionLog` |
| 7 | Branch confirmation | prompts | `-Force` |
| 8 | Commit | yes | — |
| 9 | Push | only with `-Push` | — |

A failed gate aborts **before anything is staged**. The repository is left exactly as it was.

### Review gates

| Trigger | Gate |
|---|---|
| Any code written or modified | Self-review against `CLAUDE.md` §8.1, then QA |
| Auth, input handling, file system, external API, crypto | **Security review, mandatory** |
| Structural change | Architect review |
| Any commit | `verify_structure.ps1` must pass |
| Simulation code | Simulation Scientist validates conservation and validity range |

---

## 5. Definition of Done

A unit of work is done only when **all** are true:

- [ ] It does what was asked — the whole scope, not the easy part
- [ ] It runs. Verified by execution, not by reading
- [ ] Errors handled explicitly; no silent failures
- [ ] No secrets, credentials, or personal data in source
- [ ] Files under 800 lines; functions under 50; nesting under 4
- [ ] Inputs validated at system boundaries
- [ ] Documentation updated in the same change
- [ ] Session log written
- [ ] `verify_structure.ps1` passes

---

## 6. Decision Rules

| Situation | Rule |
|---|---|
| Requirement is ambiguous | Decide the way a careful colleague would; state the assumption; continue |
| Two readings change the deliverable materially | Ask |
| Proceeding would be unsafe or make the work useless if wrong | Block and ask |
| Two agents contradict each other, evidence-resistant | Escalate to the human |
| Something is hard or awkward | Do it, or report it blocked with the blocker named. Never drop it silently |
| You disagree with the request | Say so once, with a reason. If reaffirmed, build the full thing |
| A gate fails | Fix the cause. Never bypass a gate to reach green |
| You are uncertain mid-task | Do everything not dependent on the answer first |

---

## 7. Prompt Change Workflow

Prompts are source. Changing one follows its own procedure:

```
1. Reproduce the problem with a benchmark case      (no case → no change)
2. Route it to the correct layer                    (prompts/README.md routing table)
3. Change exactly one thing
4. Re-run on HELD-OUT cases                         (minimum 3)
5. Score against prompts/benchmarks/rubric.md
6. Bump the version in frontmatter
7. Record in the session log: what, why, measured effect, what was not tested
```

---

## 8. Session Close

```powershell
pwsh -File scripts/verify_structure.ps1
pwsh -File scripts/auto_commit.ps1 -Message "<type>: <description>" -Push
```

Then complete the session log's **State At End Of Session** section and report to the operator:

1. Files created or changed
2. **What was verified** (with the command) and **what was not**
3. Problems found, resolved and unresolved
4. The next action

---

## 9. Anti-Patterns

| Anti-pattern | Correct behaviour |
|---|---|
| "Should work" | State the verification status |
| Reporting unrun tests as passing | `implemented-not-run` |
| Skipping the session log | It is gate 6; a change without a log is incomplete |
| Bypassing a gate to reach green | Fix the cause |
| Silently narrowing scope | Deliver the rest, or say what you left and why |
| Mixing refactor with feature | Two commits |
| Ending a turn with agents outstanding | Collect their results first |
| Editing a past session log | Append a new entry that references it |
| Ceremonial process on trivial work | One obvious action + one obvious verification |
