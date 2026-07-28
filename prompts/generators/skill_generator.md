---
id: skill_generator
type: generator
version: 1.0.0
produces: [skills/<id>/SKILL.md]
skills: [prompt-engineering, ai-agents]
---

# Generator — New Skill

Produces a `SKILL.md`: a knowledge domain an agent loads. Skills contain competence and
guardrails; they contain no orchestration.

**Precondition:** the domain is not already covered by an existing skill. Check
`skills/README.md`. Overlapping skills cause agents to load two contradictory sets of guardrails.

---

## Prompt

```
Generate a new Genesis Harness skill.

## Inputs
- Skill ID (kebab-case):
- Category: science | engineering | meta
- One-sentence purpose:
- Which agents load it, and for what:
- Why no existing skill covers this:

## Method

1. JUSTIFY
   State why this is a distinct knowledge domain rather than a section of an existing skill.
   If it is "the same subject at a different depth", extend the existing skill instead.

2. PURPOSE (§1)
   1-3 sentences. State what the skill prevents going wrong, not just what it covers.
   The best purpose statements name the failure mode the skill exists to stop.

3. KNOWLEDGE DOMAIN (§2)
   The actual subject matter, grouped into 4-8 named sub-domains.
   Write the real content — concepts, methods, laws, techniques. Not a table of contents,
   not "topics include...". An agent loading this must come away more capable.
   Density matters more than breadth: name the specific things a practitioner would name.

4. WHEN TO USE (§3)
   Trigger conditions as a bulleted list.
   ALSO write explicit non-triggers — "do not use when...". Skills without non-triggers get
   loaded everywhere and dilute context.

5. METHOD (§4)
   The ordered procedure for applying the skill. Numbered steps, each an action.
   This is what converts knowledge into work.

6. EXPECTED OUTPUT (§5)
   The artefacts the skill is required to produce, in bold-labelled form.
   Be concrete: "symbol table with units", not "documentation".

7. GUARDRAILS (§6)
   6-10 domain-specific prohibitions, phrased "Never ...".
   These are the failure modes a practitioner in this domain knows about and a generalist
   does not. This section is why the skill is worth loading.
   A skill with an empty or generic guardrails section is not finished.

8. RELATED (§7)
   Links to skills that compose with this one. Add a reciprocal link in at least one of them.

9. REGISTER
   - configs/harness.config.json
   - catalogue row in skills/README.md
   - a session log entry

## Rules
- Frontmatter: id, category, version, primary_agents, supporting_agents.
- All seven sections, in order, with the standard headings. Uniformity is what lets an agent
  load an unfamiliar skill and use it correctly.
- No orchestration logic — that belongs in an agent charter.
- No content that duplicates CLAUDE.md. Skills are domain-specific.
- Guardrails must be domain-specific. "Write good code" is not a guardrail;
  "never use an explicit integrator on a stiff system without declaring the step-size
  penalty" is.
```

---

## Section Skeleton

```markdown
---
id: <id>
category: science | engineering | meta
version: 1.0.0
primary_agents: [...]
supporting_agents: [...]
---

# Skill: <Name>

## 1. Purpose
## 2. Knowledge Domain
### <Sub-domain>
## 3. When To Use
**Use when:** / **Do not use when:**
## 4. Method
## 5. Expected Output
## 6. Guardrails
## 7. Related
```

## Verification

- [ ] All seven sections present, in order
- [ ] Knowledge domain contains real content, not a topic list
- [ ] 4-8 named sub-domains
- [ ] Non-triggers stated explicitly
- [ ] Method is an ordered procedure of actions
- [ ] Expected output names concrete artefacts
- [ ] 6-10 domain-specific guardrails, none generic
- [ ] Reciprocal link added to a related skill
- [ ] Registered in config and `skills/README.md`
