# Prompt Benchmarks

**Version:** 1.0.0 · **Last updated:** 2026-07-28

Prompt changes are not opinions. A benchmark is what turns "this feels better" into "this scores
0.6 higher on instruction compliance across eight held-out cases."

**Status: manual.** No automated runner exists yet. Benchmarks are currently executed by hand and
recorded in session logs. Building the runner is a Phase 2 item — see `docs/ROADMAP.md`.

---

## Files

| File | Contains |
|---|---|
| `README.md` | This — how to run and interpret a benchmark |
| `rubric.md` | The five-axis scoring rubric |
| `cases.md` | The golden case set |

---

## The Rule

**No benchmark case, no prompt change.**

If you cannot construct a case where the current prompt fails, you do not have evidence that a
problem exists — you have an aesthetic preference about prompt wording. Aesthetic changes to
prompts are how frameworks rot: each one is individually harmless and collectively unmeasurable.

---

## Procedure

```
1. REPRODUCE
   Run the failing case against the current prompt. Record the output verbatim.
   If it does not fail, there is no problem to fix. Stop.

2. BASELINE
   Score the current output against rubric.md. Record all five axis scores.

3. ROUTE
   Identify the layer that owns the problem (see the routing table in prompts/README.md).

4. CHANGE ONE THING
   A single edit. Two edits produce an unattributable result.

5. RE-RUN — HELD OUT
   Run against cases you did NOT use to write the fix.
   Scoring well on the case you optimised against measures nothing.

6. COMPARE
   Record before/after per axis. A change that improves one axis and degrades another is
   a trade-off to state explicitly, not a win.

7. RECORD
   Session log: what changed, why, measured effect, what was not tested.
   Bump the prompt's version.
```

---

## Regression Discipline

Every prompt bug that is fixed becomes a permanent case in `cases.md`. This is the same
principle as a regression test: the value is not in catching the bug once, it is in never
letting it return.

---

## Interpreting Results

| Observation | Meaning |
|---|---|
| One axis up, others flat | Real improvement |
| One axis up, another down | A trade-off — state it, do not bury it |
| All axes up sharply | Suspect the scoring, not the prompt. Re-score blind if possible |
| Improvement only on the fix case | Overfitting. The change did not generalise |
| High variance across runs | The prompt is under-constrained. Add structure, not emphasis |

---

## Known Bias

The same model both produces and scores these outputs. That is a real limitation of the current
manual method, and it is why:

- Rubric criteria are **behavioural and checkable** ("did it include the Not Done section?")
  rather than impressionistic ("was it good?").
- **Held-out cases are mandatory** — self-scoring on the optimisation target is meaningless.
- Scores are recorded as **evidence in the session log**, not as a verdict.

Do not report a benchmark result as objective. Report it as what it is: a structured,
same-model assessment against explicit criteria.
