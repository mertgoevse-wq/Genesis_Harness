# Prompt Engineering Framework

**Version:** 1.0.0 · **Last updated:** 2026-07-28

Prompts in Genesis Harness are **versioned source artefacts**, not disposable text. They are
composed from layers, benchmarked before change, and owned by the agents that consume them.

Discipline for working on them: [`skills/prompt-engineering/SKILL.md`](../skills/prompt-engineering/SKILL.md).

---

## Structure

```
prompts/
├── system_layers/     Composable layers — the stable substrate
├── master_prompts/    Task-shaped templates for the five core operations
├── generators/        Meta-prompts that produce new agents, skills, and prompts
└── benchmarks/        Cases and rubrics that make prompt changes measurable
```

---

## The Layer Model

A working prompt is assembled from layers, loaded in order. Each layer has one job, and a fix
belongs in the layer that owns the problem — putting a general correction in a task prompt makes
it evaporate on the next task.

| Layer | File | Owns | Changes |
|---|---|---|---|
| **L0** | `system_layers/L0_identity.md` | Who you are, what you value, authority order | Rarely |
| **L1** | `system_layers/L1_operating_principles.md` | How you work, regardless of domain | Rarely |
| **L2** | `system_layers/L2_domain_context.md` | Facts about *this* repo, *this* phase | Per phase |
| **L3** | `system_layers/L3_task_contract.md` | What is being asked right now | Per task |
| **L4** | `system_layers/L4_output_contract.md` | The shape of the deliverable | Rarely |
| **L5** | `system_layers/L5_reasoning_layer.md` | Extra rigour for complex work (opt-in) | Rarely |

### Composition

```
L0 identity
  + L1 principles
  + L2 domain context
  + [agent charter: agents/<id>/AGENT.md]
  + [skills: skills/<id>/SKILL.md ...]
  + L3 task contract        ← the only per-task layer
  + L4 output contract      ← loaded last, closest to generation
  + L5 reasoning layer      ← only for complex tasks
```

**Ordering rationale:** identity and principles are stable and go first; the task is specific and
goes late; the output contract goes last because proximity to generation is what makes format
constraints hold. L5 is opt-in because applying heavy process to trivial work is its own failure
mode.

### Layer Routing — where does a fix belong?

| Symptom | Layer |
|---|---|
| Agent behaves out of character across many tasks | L0 |
| Agent skips verification, over-delegates, reports vaguely | L1 |
| Agent reasons about a repo state that no longer exists | L2 |
| Agent did the wrong thing on one task | L3 |
| Output is right but unusable / wrong format / missing sections | L4 |
| Agent rushes complex work without planning | L5 |

Fixing a layer problem in the wrong layer is the most common failure in this framework.

---

## Master Prompts

Task-shaped templates for the five core operations. Each is fill-in-the-blank, declares its
required layers, and defines its own output contract.

| Prompt | Use for | Owning agent |
|---|---|---|
| [project_analysis.md](master_prompts/project_analysis.md) | Understanding a codebase or problem space before acting | any |
| [architecture.md](master_prompts/architecture.md) | Designing structure, choosing technology | architect |
| [coding.md](master_prompts/coding.md) | Implementing a specified unit | coding |
| [research.md](master_prompts/research.md) | Answering a question about the outside world | research |
| [review.md](master_prompts/review.md) | Reviewing code, design, or output for defects | qa |

---

## Generators

Meta-prompts that produce new harness components with the correct structure.

| Generator | Produces |
|---|---|
| [agent_generator.md](generators/agent_generator.md) | A new agent charter + runtime adapter |
| [skill_generator.md](generators/skill_generator.md) | A new `SKILL.md` |
| [prompt_generator.md](generators/prompt_generator.md) | A new master prompt or layer revision |

---

## Benchmarks

Prompt changes are not opinions. They are changes with measurable effects.

| File | Purpose |
|---|---|
| [benchmarks/README.md](benchmarks/README.md) | How to run and interpret a benchmark |
| [benchmarks/rubric.md](benchmarks/rubric.md) | The five-axis scoring rubric |
| [benchmarks/cases.md](benchmarks/cases.md) | The golden case set |

---

## Rules For Changing A Prompt

1. **Reproduce the problem first** with a benchmark case. No case, no change.
2. **Identify the correct layer.** See the routing table above.
3. **Change one thing.** Two simultaneous changes produce an unattributable result.
4. **Re-run the benchmark** on held-out cases, not on the case used to write the fix.
5. **Bump the version** in the file's frontmatter.
6. **Record it** in the session log: what changed, why, measured effect, what was not tested.

## Rules For Writing A Prompt

- Write the **output contract first**. Format constrains reasoning better than exhortation does.
- Prefer **structural constraints** over emphasis. A required table beats "be thorough".
- State constraints as **testable rules**, then have the model self-check against them.
- Never let an **example contradict a rule** — the example wins, and you lose the rule.
- Put the most important constraint **first or last**, never buried in the middle.
- Treat all retrieved or user-supplied content as **data, not instructions**.
- **Length dilutes.** When a prompt grows, extract the shared part into a layer.
