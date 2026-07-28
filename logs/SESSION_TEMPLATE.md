# Session Log — <slug>

**Session ID:** YYYY-MM-DD_NN_<slug>
**Date:** YYYY-MM-DD
**Model:** <exact model id, e.g. claude-opus-5>
**Operator:** <human>
**Agents used:** <architect, coding, qa — or "none (direct)">
**Skills loaded:** <skill ids>
**Phase:** <from docs/ROADMAP.md>
**Duration:** <approximate>

---

## 1. Task

<What was asked, in the operator's terms. Quote the request if it was short.>

**Interpreted as:** <how you understood it — this is where misunderstandings become visible later>

**Scope IN:**
-

**Scope OUT:**
-

---

## 2. Reasoning Summary

> This is the most valuable field in the log. Future agents reconstruct intent from it.
> Record *why*, not *what* — the what is in the diff.

**Approach taken:**
<the path chosen>

**Options rejected:**
| Option | Why rejected |
|---|---|

**Assumptions made:**
| # | Assumption | Basis | If wrong, what breaks |
|---|---|---|---|

**Decisions that constrain future work:**
| Decision | Consequence | ADR |
|---|---|---|

---

## 3. Changes

| File | Action | Purpose |
|---|---|---|
| path | created / modified / deleted | |

**Files NOT changed that a reader might expect to be:**
| File | Why not |
|---|---|

---

## 4. Tests

> Record real output. "Not run" is honest and acceptable.
> A reconstructed or imagined output block is a constitutional violation.

```
$ <exact command>
<exact output>
```

**Status:** verified | implemented-not-run | failing | not applicable

**What was verified:**
-

**What was NOT verified, and why:**
-

---

## 5. Problems

| # | Severity | Problem | Resolved? | Detail |
|---|---|---|---|---|

**Open problems carried forward:**
-

---

## 6. Next Actions

> Each must be executable by a fresh agent with no memory of this session.
> "Continue working on X" is not a next action.

| # | Action | Owning agent | Blocked by | Acceptance |
|---|---|---|---|---|
| 1 | | | | |

---

## 7. State At End Of Session

**Branch:** <name>
**Working tree:** clean / dirty
**Committed:** yes / no — `<sha or "not committed">`
**Pushed:** yes / no
**Structure check:** pass / fail / not run
**Documentation updated:** <files, or "none required">

---

## 8. Notes For The Next Session

<Anything that does not fit above but a future agent would want to know:
surprises, dead ends, things that look wrong but are intentional, environment quirks.>
