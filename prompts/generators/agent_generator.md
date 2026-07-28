---
id: agent_generator
type: generator
version: 1.0.0
produces: [agents/<id>/AGENT.md, .claude/agents/<id>.md]
skills: [ai-agents, prompt-engineering]
---

# Generator — New Agent

Produces a complete agent: the canonical charter and the runtime adapter.

**Precondition:** the new agent must not overlap an existing agent's authority. Two agents with
authority over the same artefact is the most common multi-agent failure. Check
`agents/README.md` first.

---

## Prompt

```
Generate a new Genesis Harness agent.

## Inputs
- Agent ID (kebab-case):
- Purpose (one sentence):
- Role class:
- What it OWNS (its authority):
- What it can BLOCK:
- Why an existing agent cannot do this:

## Method

1. JUSTIFY
   State why this cannot be a skill loaded by an existing agent.
   Agents are roles with authority; skills are knowledge. If the answer is "it needs to know
   about X", you want a skill, not an agent. Stop and generate a skill instead.

2. BOUND
   Define the scope in one sentence. Then define what it explicitly does NOT own.
   Check every existing agent in agents/README.md for authority overlap. Report any found.

3. RESPONSIBILITIES
   3-5 responsibility clusters. Each is a thing it produces or decides, not a topic it knows.

4. SKILLS
   Which skills/ it loads. Primary first. If none fit, the skill must be generated first.

5. WORKFLOW
   An ordered, named-stage pipeline. Each stage is a verb. Include:
   - hard rules (the things it must never do)
   - stop conditions (when it halts rather than continuing)
   - escalation conditions (when it goes to the human)
   An agent without stop conditions runs until the budget dies.

6. OUTPUT FORMAT
   The exact template its deliverable follows. Design this so the RECEIVING agent can
   consume it without interpretation. Write the format before the prose — format
   constrains behaviour more reliably than instruction.

7. QUALITY BAR
   The conditions under which its own output is REJECTED. Write 5-8, phrased as
   "Output is rejected if it...". This is the agent's self-check.

8. INTERFACES
   A table: receives from / requests from / hands off to / escalates to.
   An agent with no interfaces is disconnected from the loop and is a smell.

9. EMIT BOTH FILES
   - agents/<id>/AGENT.md      — full charter, structured per agents/README.md
   - .claude/agents/<id>.md    — adapter: YAML frontmatter (name, description, tools)
                                 + condensed operating contract + pointer to the charter

10. REGISTER
    - configs/harness.config.json
    - roster row in agents/README.md
    - roster row in docs/AGENTS.md
    - a session log entry

## Rules
- Minimum tool grant in the adapter. Every extra tool is an extra failure mode.
- The `description` field in the adapter frontmatter is what triggers automatic selection —
  write it as trigger conditions, not as a job title.
- The charter is authoritative. If the adapter and charter disagree, that is a bug.
- Do not create an agent whose responsibilities are a subset of an existing one.
```

---

## Adapter Frontmatter Template

```yaml
---
name: <id>
description: <what it does>. Use PROACTIVELY when <trigger>, <trigger>, or <trigger>. Produces <output>.
tools: <minimum set>
---
```

## Verification

- [ ] Charter has all eight sections
- [ ] Adapter frontmatter is valid YAML with name, description, tools
- [ ] `description` states trigger conditions, not a job title
- [ ] No authority overlap with an existing agent
- [ ] Workflow has stop conditions and escalation conditions
- [ ] Output format is consumable by the named receiving agent
- [ ] Quality bar has 5-8 rejection conditions
- [ ] Interfaces reference agents that actually exist
- [ ] Registered in config, `agents/README.md`, and `docs/AGENTS.md`
