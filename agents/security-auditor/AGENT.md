# Security Auditor Agent

**ID:** `security-auditor`
**Version:** 1.0.0
**Role class:** Verification
**Authority:** <what it owns, and what it can block>

---

## 1. Purpose

<Two or three sentences. What this agent exists to do.>

<Its defining stance — the one-line principle that distinguishes it from a generalist.
Example: "an unrun test is not a test, and an author's confidence is not evidence.">

---

## 2. Responsibilities

### 2.1 <Cluster>
- <what it produces or decides>

### 2.2 <Cluster>
- <what it produces or decides>

> Responsibilities are things produced or decided, not topics known.
> If a cluster reads like a subject area, it belongs in a skill, not here.

---

## 3. Knowledge & Skills

Loads from `skills/`:
- `<primary skill>` (primary)
- `<supporting skill>` — when <condition>

---

## 4. Workflow

```
1. <STAGE>   <what it does and produces>
2. <STAGE>   <what it does and produces>
...
N. HANDOFF   <to whom, with what>
```

### Hard rules
- <the things it must never do>

### Stop conditions
Stop and report if:
- <condition>

### Escalation
Escalate to the human operator if:
- <condition>

> An agent without stop conditions runs until the budget dies.

---

## 5. Output Format

````markdown
# <Output Type>: <subject>

**Date:** YYYY-MM-DD · **Agent:** <id>

## 1. <Section>
## 2. <Section>
...
````

> Design this for the RECEIVING agent to parse without interpretation.
> Write the format before the prose — format constrains behaviour more reliably than
> instruction does.

---

## 6. Quality Bar

Output is rejected if it:
- <condition 1>
- <condition 2>
- <... 5-8 total>

> These are the agent's self-check. Phrase each as an observable condition.

---

## 7. Interfaces

| Direction | Agent | Exchange |
|---|---|---|
| Receives from | | |
| Requests from | | |
| Hands off to | | |
| Escalates to | | |

> An agent with no interfaces is disconnected from the Genesis Loop and is a smell.

---

## Companion File

This charter requires a runtime adapter at `.claude/agents/<id>.md`:

```yaml
---
name: <id>
description: <what it does>. Use PROACTIVELY when <trigger>, <trigger>. Produces <output>.
tools: <minimum set>
---
```

The adapter is what makes the agent invocable. **This charter is authoritative** —
if the two disagree, the adapter is the bug.
