# Handoff — <from agent> → <to agent>

**Date:** YYYY-MM-DD
**Session:** <session log id>
**Unit:** <id from the architecture document, if any>

> **Cold-start test:** a fresh agent with no memory of this session must be able to act on this
> handoff alone. If it contains "as discussed", "the approach above", or an unexplained
> reference, it fails and must be rewritten.
>
> Work handed off without a complete handoff block is rejected by the receiving agent.

---

## 1. What Was Done

<Factual. What now exists that did not before.>

| Artefact | Path | State |
|---|---|---|

## 2. What Was NOT Done

<In scope but not completed, and why. This section is mandatory — its absence asserts
that nothing was left.>

| Item | Why not | Blocking? |
|---|---|---|

## 3. Files Touched

| File | Action | Purpose |
|---|---|---|

## 4. Verification State

```
$ <exact command run>
<exact output>
```

**Status:** verified | implemented-not-run | failing | not applicable
**Not verified:** <what could not be executed, and what is needed to execute it>

## 5. Contract For The Receiving Agent

**Goal:** <one sentence end state>

**Inputs available:**
| Input | Location |
|---|---|

**Acceptance criteria:**
| # | Criterion | Verified how |
|---|---|---|

**Scope OUT:** <explicitly not the receiving agent's job>

## 6. Assumptions In Force

| # | Assumption | Label (VERIFIED/KNOWN/ASSUMED) | If wrong, what breaks |
|---|---|---|---|

## 7. Open Questions

| # | Question | Blocking? | Who can answer |
|---|---|---|---|

## 8. Constraints The Receiver Must Respect

| Constraint | Source | Hard/Soft |
|---|---|---|

## 9. Known Risks

| Risk | Likelihood | Consequence | Mitigation |
|---|---|---|---|
