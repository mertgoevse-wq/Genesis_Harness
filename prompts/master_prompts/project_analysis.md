---
id: project_analysis
type: master_prompt
version: 1.0.0
owning_agent: any
requires_layers: [L0, L1, L2, L4]
optional_layers: [L5]
skills: [software-engineering]
---

# Master Prompt — Project Analysis

**Use when:** you need to understand a codebase, subsystem, or problem space *before* deciding
anything. Analysis precedes architecture; architecture precedes code.

**Do not use when:** the question is a single lookup you can answer by reading one file.

---

## Prompt

```
You are performing a PROJECT ANALYSIS for Genesis Harness.

## Subject
<what you are analysing — repository, subsystem, module, or problem space>

## Analysis Question
<the specific decision this analysis must inform>
If this is blank, stop and ask. Analysis without a decision to serve is a survey, not work.

## Depth
survey | working | forensic
- survey:   structure and entry points only
- working:  enough to change it safely
- forensic: enough to rewrite it

## Method

1. INVENTORY
   List what actually exists. Do not describe intent — describe files, directories,
   entry points, and dependencies you have verified are present.

2. STRUCTURE
   Map the components and how they relate. Identify:
   - entry points and control flow
   - data ownership: who writes what, who reads what
   - dependency direction, and any cycles
   - boundaries that are enforced vs merely conventional

3. CONVENTIONS
   Extract the patterns the code actually follows: naming, error handling, file layout,
   testing approach. State where the codebase is internally inconsistent.

4. CONSTRAINTS
   What limits change? Platform, runtime, external contracts, data formats, deployed
   consumers, absent tooling. Mark each verified or assumed.

5. RISK
   Where is this fragile? Look for: unbounded growth, silent failure paths, missing
   validation, coupling that will resist the intended change, untested critical paths,
   size violations, secrets in source.

6. GAP
   What is missing relative to the analysis question — and what could you not determine?

7. ANSWER
   Answer the analysis question directly. Recommend a next action.

## Rules
- Report only what you verified. Do not infer file contents you did not read.
- Distinguish "this is the pattern" from "this is the pattern in the three files I read".
- Absence of evidence is a finding — report "no tests found", not silence.
- Do not propose a redesign. That is the Architect Agent's output, not this one's.
- If the subject is larger than you can cover at the requested depth, say so and state
  what you did cover.

## Output
Use the PROJECT ANALYSIS format below. Lead with the answer to the analysis question.
```

---

## Output Format

```markdown
# Project Analysis: <subject>

**Date:** YYYY-MM-DD · **Depth:** survey | working | forensic
**Question:** <the analysis question>

## Answer
<2-5 sentences answering the question directly, with a recommended next action>

## 1. Inventory
| Path | Type | Purpose | Size |
|---|---|---|---|

## 2. Structure
```
<component / control-flow diagram>
```

| Component | Responsibility | Owns | Depends on |
|---|---|---|---|

**Dependency cycles:** <none | list>

## 3. Conventions
| Aspect | Observed pattern | Consistent? |
|---|---|---|

## 4. Constraints
| Constraint | Value | Verified? |
|---|---|---|

## 5. Risks
| # | Severity | Risk | Location | Consequence |
|---|---|---|---|---|

## 6. Gaps & Unknowns
| Gap | Why it matters | How to resolve |
|---|---|---|

## 7. Coverage
**Examined:** <what you actually read>
**Not examined:** <what you did not, and why>
```

---

## Quality Bar

Rejected if it: describes intent instead of observed reality · asserts a pattern from an
unstated sample size · omits the "not examined" section · proposes a redesign · answers a
different question than the one asked · reports no risks without saying where it looked.
