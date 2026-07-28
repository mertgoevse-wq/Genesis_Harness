---
id: ai-agents
category: meta
version: 1.0.0
primary_agents: [architect, coding, research]
supporting_agents: [qa]
---

# Skill: AI Agents

## 1. Purpose

Provide the discipline for designing, orchestrating, and debugging multi-agent AI systems —
including this harness itself. This is the skill Genesis Harness applies to its own construction.

## 2. Knowledge Domain

### Agent design
Role definition and scope boundaries; single-responsibility per agent; capability vs authority
(what an agent *can* do vs what it is *allowed* to decide); tool selection and least-privilege
tool grants; stopping conditions; escalation criteria; output contracts.

### Orchestration topologies
Single agent with tools; supervisor/worker; pipeline (sequential handoff); parallel fan-out with
a collector; debate/adversarial pairs; generator–evaluator loops; blackboard/shared-state;
hierarchical decomposition. Selection criteria and the failure mode of each.

### Context engineering
Context window as a scarce budget; what belongs in the system layer vs the task layer vs
retrieved context; progressive disclosure (load detail on demand rather than upfront);
summarisation and compaction strategies; the lost-in-the-middle effect; context pollution from
irrelevant history; when to start a fresh agent instead of continuing one.

### Memory & continuity
Session logs as durable memory; append-only history; handoff artefacts as the transfer mechanism;
state files vs conversation state; the cold-start test (can a fresh agent resume from artefacts
alone?); memory staleness and verification-before-use.

### Tool & action design
Tool granularity; unambiguous descriptions; parameter validation; idempotency; error messages
written *for the agent* to recover from; observation formatting; token cost of observations;
avoiding tools that overlap or shadow each other.

### Evaluation
Task-level success criteria; rubric design; LLM-as-judge and its biases (position, verbosity,
self-preference); golden sets and regression suites; measuring cost and latency alongside quality;
pass@k and consistency across runs; ablation to attribute improvements.

### Failure modes
Hallucinated results and fabricated verification; silent scope reduction; premature termination;
infinite repair loops; delegation without collection (orphaned subagents); over-delegation of
work that fits one context; context poisoning from a bad early assumption; sycophantic agreement
between agents; tool-call thrashing; over-confidence from unlabelled assumptions.

### Cost & routing
Model capability tiers vs task difficulty; routing cheap work to cheap models; the cost of a
retry vs the cost of a stronger model; batching; caching; the economics of parallel fan-out.

## 3. When To Use

**Use when:**
- Designing or modifying any agent, skill, or orchestration in this harness.
- Deciding whether to delegate, and to how many agents.
- Debugging an agent that produced wrong, incomplete, or fabricated output.
- Designing evaluation for agent quality.
- Choosing which model tier handles which work.

## 4. Method

1. **Define the role before the prompt.** An agent whose scope you cannot state in one sentence
   will not behave consistently.
2. **Give it an output contract.** Structured output is what makes an agent composable.
3. **Grant the minimum tools.** Every extra tool is an extra failure mode.
4. **Specify stopping and escalation conditions explicitly** — agents do not infer them.
5. **Design the handoff artefact**, not just the conversation. Apply the cold-start test.
6. **Decompose only when the work cannot fit one context.** Depth is an outcome, not a plan.
7. **If you delegate, you collect.** Never end a turn with children outstanding.
8. **Build the evaluation before scaling the system.** Unmeasured agents drift.
9. **Instrument for the known failure modes** above — especially fabricated verification.

## 5. Expected Output

- **Agent specification**: purpose, responsibilities, authority, tools, workflow, output format,
  quality bar, interfaces, stop conditions.
- **Topology diagram** with data flow and handoff points.
- **Context budget**: what each agent loads, and why.
- **Evaluation plan**: criteria, rubric, golden cases, cost/latency targets.
- **Failure-mode analysis**: which of the known modes this design is exposed to, and the mitigation.

## 6. Guardrails

- Never let an agent report a result it did not produce or observe.
- Never spawn a subagent without a plan for integrating its output.
- Never end a turn while delegated work is outstanding.
- Never give two agents overlapping authority over the same artefact.
- Never treat an agent's confident tone as evidence of correctness.
- Never build a multi-agent system where a single agent suffices.
- Never let an agent silently narrow its assigned scope.
- Always make assumption labelling (VERIFIED/KNOWN/ASSUMED) part of the output contract.

## 7. Related

`skills/prompt-engineering` · `skills/software-engineering`
