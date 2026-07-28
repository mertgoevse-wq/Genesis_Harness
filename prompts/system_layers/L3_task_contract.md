---
id: L3_task_contract
layer: 3
name: Task Contract
version: 1.0.0
changes_frequency: per-task
---

# L3 — Task Contract Layer

> **Composition rule:** L3 is the only layer that changes per task. It carries *what* is being
> asked, never *how you work* (L1) or *who you are* (L0). If you find yourself correcting
> general behaviour here, the fix belongs in a lower layer.

---

## Purpose

A task contract makes a request executable. It converts "do X" into something an agent can start
cold, finish completely, and be judged against objectively.

**A task without acceptance criteria is not a task. Send it back.**

---

## The Contract Template

```markdown
## Task Contract

**ID:** <phase-NN-slug>
**Owning agent:** architect | research | coding | simulation-scientist | game-design | qa
**Loaded skills:** <skill ids>
**Requested by:** <human | agent id>
**Date:** YYYY-MM-DD

### Goal
<One sentence. What will be true when this is done that is not true now?>

### Context
<Why this now. Links to the ADR, session log, or handoff that produced it. Max one paragraph.>

### Inputs
| Input | Location | Verified present? |
|---|---|---|

### Scope — IN
- <explicit>

### Scope — OUT
- <explicit — this section prevents both silent widening and silent narrowing>

### Constraints
| Constraint | Value | Hard/Soft |
|---|---|---|

### Acceptance Criteria
| # | Criterion | Verified how |
|---|---|---|
| 1 | <objective, checkable statement> | <exact command or observation> |

> Every criterion must be checkable by someone who did not do the work.
> "Code is clean" is not a criterion. "No file exceeds 800 lines" is.

### Deliverables
| # | Artefact | Path | Format |
|---|---|---|---|

### Definition of Done
- [ ] Every acceptance criterion met and evidenced
- [ ] Executed and real output captured (or status honestly recorded as `implemented-not-run`)
- [ ] Documentation updated in the same change
- [ ] Session log written
- [ ] `scripts/verify_structure.ps1` passes

### Stop Conditions
Stop and report if:
- <condition that makes continuing wasteful or unsafe>

### Escalation
Escalate to the human if:
- <condition>

### Assumptions
| # | Assumption | If wrong, what breaks |
|---|---|---|
```

---

## Rules For Filling It

1. **Goal is one sentence and states an end state**, not an activity.
   Bad: "work on logging". Good: "every session writes a log conforming to SESSION_TEMPLATE.md".
2. **Scope OUT is mandatory.** It is how the operator's decision about size is preserved.
3. **Acceptance criteria are objective.** If two reasonable people could disagree on whether it
   was met, rewrite it.
4. **Every criterion names its verification method** — the exact command, the exact file to check,
   or the exact observation.
5. **Assumptions are declared up front**, with the consequence of being wrong.
6. **Stop conditions are real.** An agent that never stops burns budget on a doomed path.

---

## Anti-Patterns

| Anti-pattern | Fix |
|---|---|
| "Improve X" | State the measurable property that improves |
| No Scope OUT | Add it — ambiguity defaults to the agent's judgement, which drifts |
| "Make sure it works" | Name the command that demonstrates it works |
| Criteria that restate the goal | Criteria are *checks*, not paraphrases |
| Behavioural corrections in L3 | Move to L1 — otherwise the fix does not persist |
| Ten criteria for a one-line change | Contract weight should match task weight |

---

## Minimal Form

For small tasks, this reduced form is sufficient — but Goal, Scope OUT, and Acceptance Criteria
are never omitted:

```markdown
**Task:** <id> · **Agent:** <id>
**Goal:** <one sentence end state>
**In:** <bullet> **Out:** <bullet>
**Accept:** 1. <criterion> — verified by `<command>`
**Stop if:** <condition>
```
