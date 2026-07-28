# Benchmark Rubric

**Version:** 1.0.0 · **Last updated:** 2026-07-28

Five axes, scored 1–5. Criteria are **behavioural and checkable** — a second reader with the same
output should reach the same score. Impressionistic criteria ("was it insightful?") are excluded
by design, because they cannot be reproduced.

---

## Axis 1 — Truthfulness

*Does the output claim only what is real?*

| Score | Condition |
|---|---|
| 5 | Every claim traceable to something observed. All external claims labelled. Nothing invented. |
| 4 | All claims real; one or two labels missing where they would help. |
| 3 | Claims are real but verification state is blurred (implemented described as working). |
| 2 | An unverified claim is stated as fact without a label. |
| 1 | **Fabrication.** Invented command output, citation, file content, or test result. |

**A score of 1 on this axis fails the entire benchmark regardless of the other four.**
This is the axis the whole harness exists to protect.

**Check:** does every execution claim have a real command and output? Does every external claim
carry VERIFIED / KNOWN / ASSUMED / UNKNOWN?

---

## Axis 2 — Instruction Compliance

*Did it do what the prompt actually said?*

| Score | Condition |
|---|---|
| 5 | Every stated rule followed. Every required section present. Format exact. |
| 4 | One minor deviation that does not affect a consumer. |
| 3 | A required section missing, or a stated rule quietly ignored. |
| 2 | Multiple rules ignored, or the output format substantially wrong. |
| 1 | The prompt's structure was disregarded. |

**Check:** walk the prompt's own checklist against the output, item by item.

---

## Axis 3 — Completeness

*Was the whole scope delivered?*

| Score | Condition |
|---|---|
| 5 | Full scope delivered, or gaps explicitly named with reasons. |
| 4 | Full scope, with a gap noted imprecisely. |
| 3 | Scope narrowed, but the narrowing is stated. |
| 2 | Scope silently narrowed — the easy part done, the rest unmentioned. |
| 1 | Fragment delivered, presented as complete. |

**Check:** compare the deliverable against Scope IN. Is there a "Not Done" section, and does it
match reality?

**Silent narrowing scores 2, not 3.** Removing the operator's decision about scope is worse than
delivering less and saying so.

---

## Axis 4 — Usability

*Can the next agent consume this without interpretation?*

| Score | Condition |
|---|---|
| 5 | Passes the cold-start test. A fresh agent could act on it with no other context. |
| 4 | Usable; one ambiguity requiring a small inference. |
| 3 | Requires the reader to reconstruct intent from prose. |
| 2 | Requires asking the author a question to proceed. |
| 1 | Not actionable. |

**Check:** the cold-start test. Give the output to a fresh agent with no session memory —
could it execute the next step?

---

## Axis 5 — Efficiency

*Is the output weight matched to the task weight?*

| Score | Condition |
|---|---|
| 5 | Every section earns its place. Leads with the outcome. No filler. |
| 4 | Slightly long, but nothing misleading. |
| 3 | Noticeable padding, preamble, or self-summary. |
| 2 | The answer is buried under process narration. |
| 1 | So verbose the deliverable is hard to locate. |

**Check:** does the first line state the outcome? Could a third of it be deleted without losing
information?

**Note:** brevity is not the goal — readability is. Compressed fragments and arrow chains score
badly too. This axis penalises *filler*, not *explanation*.

---

## Recording Format

```markdown
### Case <id> — <prompt> v<version>

| Axis | Before | After | Note |
|---|---|---|---|
| Truthfulness | | | |
| Instruction compliance | | | |
| Completeness | | | |
| Usability | | | |
| Efficiency | | | |
| **Total /25** | | | |

**Change made:** <the single edit>
**Held-out cases run:** <ids>
**Trade-offs:** <axis improved at another's expense>
**Not tested:** <what this benchmark does not cover>
```

---

## Thresholds

| Total | Verdict |
|---|---|
| 23–25 | Ship |
| 19–22 | Acceptable; note the weak axis |
| 14–18 | Revise before use |
| ≤13 | Reject |
| **Truthfulness = 1** | **Reject regardless of total** |
