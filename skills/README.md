# Skill Registry

**Version:** 1.0.0 · **Last updated:** 2026-07-28

A **skill** is a knowledge domain an agent loads to do its work. Agents are *who*; skills are
*what they know*. Skills contain no orchestration logic — they are pure domain competence plus
the guardrails specific to that domain.

Machine-readable registry: `configs/harness.config.json`.

## Catalogue

| Skill | Category | Primary agents | Answers |
|---|---|---|---|
| [physics](physics/SKILL.md) | science | simulation-scientist, research | Mechanics, thermo, fluids, EM, gravitation |
| [chemistry](chemistry/SKILL.md) | science | simulation-scientist, research | Matter, reactions, kinetics, equilibrium |
| [biology](biology/SKILL.md) | science | simulation-scientist, research | Cells, genetics, populations, ecosystems |
| [astronomy](astronomy/SKILL.md) | science | simulation-scientist, research | Orbits, stars, planets, cosmic scale |
| [simulation](simulation/SKILL.md) | engineering | simulation-scientist, architect, coding | Stability, determinism, performance, validation |
| [game-development](game-development/SKILL.md) | engineering | game-design, coding, architect | Loops, feel, engine architecture, networking |
| [software-engineering](software-engineering/SKILL.md) | engineering | coding, architect, qa | Structure, errors, testing, security, debugging |
| [ai-agents](ai-agents/SKILL.md) | meta | architect, coding, research | Agent design, orchestration, evaluation |
| [prompt-engineering](prompt-engineering/SKILL.md) | meta | architect, research, coding | Prompt structure, contracts, benchmarking |

## Skill Structure

Every `SKILL.md` has the same seven sections. This uniformity is what lets an agent load an
unfamiliar skill and use it correctly.

| Section | Contains |
|---|---|
| 1. Purpose | Why this skill exists, in 1–3 sentences |
| 2. Knowledge Domain | The actual subject matter, grouped by sub-domain |
| 3. When To Use | Trigger conditions — and explicit non-triggers |
| 4. Method | The ordered procedure for applying the skill |
| 5. Expected Output | The artefacts the skill is required to produce |
| 6. Guardrails | Domain-specific failure modes and hard prohibitions |
| 7. Related | Links to skills that compose with this one |

## Loading Rules

1. **Load the primary skill for the task, plus any skill it lists under "Related" that the task
   actually touches.** Do not load the whole library.
2. **`software-engineering` is the default.** When no other skill applies, it does.
3. **Science skills specify the model; `simulation` specifies the solver.** A simulated system
   almost always needs both.
4. **Guardrails are non-negotiable.** A skill's guardrails have the same force as CLAUDE.md when
   that skill is loaded.
5. **Conflicts resolve upward**: skill guardrails < agent charter < CLAUDE.md < explicit human
   instruction.

## Adding a Skill

1. Copy `templates/SKILL_TEMPLATE.md` to `skills/<id>/SKILL.md`.
2. Fill all seven sections. A skill with an empty Guardrails section is not finished.
3. Register it in `configs/harness.config.json`.
4. Add a row to the catalogue above.
5. Link it from the `Related` section of at least one existing skill.
6. Record the addition in a session log.
