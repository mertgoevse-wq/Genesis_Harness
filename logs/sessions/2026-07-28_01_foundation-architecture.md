# Session Log — foundation-architecture

**Session ID:** 2026-07-28_01_foundation-architecture
**Date:** 2026-07-28
**Model:** claude-opus-5
**Operator:** mertgoevse-wq
**Agents used:** none as subagents — architect / coding / qa roles performed inline by the lead session
**Skills loaded:** software-engineering, ai-agents, prompt-engineering
**Phase:** 0 — Foundation
**Duration:** single session

---

## 1. Task

Create the complete foundation architecture for Genesis Harness: agent architecture, skill
architecture, prompt engineering framework, documentation system, logging system, and Git
workflow. Explicitly **not** the Genesis Engine — the infrastructure that will later allow
multiple AI agents to collaboratively develop complex software.

**Interpreted as:** build the real files, not descriptions of files. The repository was an empty
skeleton (directories with `.gitkeep`, empty `README.md` and `docs/ROADMAP.md`), so this is a
greenfield structural build with one pre-existing constraint: a `CLAUDE.md` that referenced
`prompts/system_layers/fable5_layer.md` as an "additional reasoning layer".

**Scope IN:**
- `CLAUDE.md` project constitution (AI role, philosophy, agent workflow, doc/git/log rules, quality standards)
- 6 agents: architect, research, coding, simulation-scientist, game-design, qa
- 9 skills: physics, chemistry, biology, astronomy, simulation, game-development, software-engineering, ai-agents, prompt-engineering
- Prompt framework: `system_layers/`, `master_prompts/`, `generators/`, `benchmarks/`
- Logging system with `SESSION_TEMPLATE.md`
- `scripts/auto_commit.ps1` with safety checks
- Docs: `ARCHITECTURE.md`, `AGENTS.md`, `WORKFLOW.md`, `ROADMAP.md`
- Verification: `git status`, structure verification, file existence

**Scope OUT:**
- The Genesis Engine itself
- Runtime code, test runner, CI
- Automated benchmark execution
- Any external dependency or service

---

## 2. Reasoning Summary

**Approach taken:**

The design rests on three separations, chosen because collapsing any of them is what makes
multi-agent systems fail in practice:

1. **Role vs knowledge (agents vs skills).** An agent is *who does the work* — scope, authority,
   workflow, output contract. A skill is *what it knows* — domain, method, guardrails. Fusing
   them would produce 6 × 9 = 54 documents' worth of duplication and mean a domain improvement
   had to be applied six times.

2. **Stable vs volatile (prompt layers L0–L5).** L0 identity and L1 principles change rarely,
   L2 domain context changes per phase, L3 task contract changes per task, L4 output contract
   changes rarely, L5 reasoning is opt-in for complex work. A correction placed in the wrong
   layer either evaporates (behaviour fix put in a task prompt) or contaminates everything
   (task fix put in identity). The routing table in `prompts/README.md` exists to prevent this.

3. **Claim vs evidence (verification states).** `verified` / `implemented-not-run` / `planned`,
   plus VERIFIED / KNOWN / ASSUMED / UNKNOWN for external claims. This is the separation that
   gives the QA Agent something concrete to enforce and gives the benchmark rubric a
   truthfulness axis that can reject an output outright.

Agents were given a **two-file structure**: a long canonical charter at `agents/<id>/AGENT.md`
and a short runtime adapter at `.claude/agents/<id>.md`. The adapter is what makes the agent
discoverable and invocable by Claude Code; the charter is what makes it correct. The charter is
declared authoritative, so a divergence is a bug in the adapter rather than an ambiguity.

The **registry** (`configs/harness.config.json`) drives `verify_structure.ps1`, so registering a
new agent or skill automatically extends verification. Registering without creating the files
fails the commit gate. This makes drift mechanically detectable rather than a matter of vigilance.

`auto_commit.ps1` was built as **nine sequential gates that abort before staging anything**, so a
failed gate leaves the repository byte-identical to how it was found. The secret scanner reports
file and line only, never the matched value, so a failed-commit log does not itself become a leak.

**Options rejected:**

| Option | Why rejected |
|---|---|
| Single-file agents in `.claude/agents/` only | Native adapters must stay short to be cheap to load; complete charters must be long. One file cannot be both |
| Duplicating skills into `.claude/skills/` for native discovery | 9 near-identical stub files with no benefit; agents read skills by path perfectly well |
| Embedding domain knowledge inside each agent | N×M duplication; a physics correction would need applying in three charters |
| One system prompt per agent | A fix would have to land in six places, and would land at the wrong volatility |
| Cross-platform shell scripts (bash/Node) | Environment is Windows-first; adding a runtime requires an ADR, and this is Phase 0 |
| Hardcoding file lists in `verify_structure.ps1` | Registry-driven checking means registration and verification cannot drift apart |
| Building an automated benchmark runner now | An honest manual method beats a fake automated one; scheduled as Phase 2 |
| Overwriting `fable5_layer.md` with a clean alias | See Problems §1 — the file is not what it was described as, and I did not create it |

**Assumptions made:**

| # | Assumption | Basis | If wrong, what breaks |
|---|---|---|---|
| 1 | Top-level `agents/`, `skills/`, `prompts/`, `logs/`, `docs/`, `scripts/`, `configs/` are wanted alongside `.claude/`, not nested inside it | The requested structure listed them, and the repo skeleton already had all seven at top level | Paths in every registry, doc, and script would need rewriting |
| 2 | PowerShell 7+ is available and is the intended automation shell | Windows 11 environment; `pwsh` present | Scripts fail to run; would need a bash port |
| 3 | The Genesis Engine will be simulation-heavy and interactive | Justifies the simulation-scientist and game-design agents and the four science skills | Those agents and skills are dead weight until repurposed. Recorded as ROADMAP item 1.6 to confirm or replace |
| 4 | Model IDs in `model_routing.json` are current | Environment documentation as of 2026-07-28 | Routing guidance names non-existent models; the file is advisory only, so impact is low |

**Decisions that constrain future work:**

| Decision | Consequence | ADR |
|---|---|---|
| Charter is authoritative over adapter | Adapter divergence is always the bug | none yet |
| Config numbers are operative over constitution prose | Changing a threshold means editing JSON, then correcting the constitution | none yet |
| Session logs are append-only | Corrections require a new log referencing the old one | none yet |
| One owner per artefact | New agents must not overlap existing authority | none yet |
| Registry drives structure verification | Adding a component means registering it or the gate fails | none yet |

No ADRs were written this session. `docs/adr/` is established by convention; ADR 0001 is
scheduled as ROADMAP next-action 5 because the first real decision belongs to Phase 1.

---

## 3. Changes

**63 files authored: 60 created, 3 modified** (`CLAUDE.md`, `README.md`, `docs/ROADMAP.md` already
existed — the latter two were empty, `CLAUDE.md` held a 35-line stub). Counted by inventory, not
by memory: `Get-ChildItem -Recurse -File | Where-Object { $_.FullName -notmatch '\\\.git\\' -and $_.Name -ne '.gitkeep' }`
returns 65, of which 2 are pre-existing and untouched (`.claude/settings.local.json`,
`prompts/system_layers/fable5_layer.md`).

| File | Action | Purpose |
|---|---|---|
| `CLAUDE.md` | modified | Project constitution — replaced a 35-line stub, preserved its reasoning-layer contract |
| `README.md` | modified | Entry point — was empty |
| `docs/ROADMAP.md` | modified | Phases, next actions, open problems — was empty |
| `docs/ARCHITECTURE.md` | created | Subsystems, separations, data flow, 12 invariants, load envelope |
| `docs/AGENTS.md` | created | Authority model, interaction matrix, standard flows, failure modes |
| `docs/WORKFLOW.md` | created | Bootstrap, 8 stages, gates, decision rules, session close |
| `agents/README.md` | created | Agent registry and two-file structure |
| `agents/architect/AGENT.md` | created | Architect charter |
| `agents/research/AGENT.md` | created | Research charter |
| `agents/coding/AGENT.md` | created | Coding charter |
| `agents/simulation-scientist/AGENT.md` | created | Simulation Scientist charter |
| `agents/game-design/AGENT.md` | created | Game Design charter |
| `agents/qa/AGENT.md` | created | QA charter |
| `.claude/agents/{architect,research,coding,simulation-scientist,game-design,qa}.md` | created | 6 runtime adapters with YAML frontmatter and tool grants |
| `skills/README.md` | created | Skill registry, structure, loading rules |
| `skills/{physics,chemistry,biology,astronomy}/SKILL.md` | created | 4 science skills |
| `skills/{simulation,game-development,software-engineering}/SKILL.md` | created | 3 engineering skills |
| `skills/{ai-agents,prompt-engineering}/SKILL.md` | created | 2 meta skills |
| `prompts/README.md` | created | Layer model, composition order, layer routing table |
| `prompts/system_layers/L0_identity.md` | created | Identity, values, authority order |
| `prompts/system_layers/L1_operating_principles.md` | created | How to work, regardless of domain |
| `prompts/system_layers/L2_domain_context.md` | created | Current repo state, constraints, vocabulary |
| `prompts/system_layers/L3_task_contract.md` | created | Task contract template and rules |
| `prompts/system_layers/L4_output_contract.md` | created | Output shape, evidence block format, prohibitions |
| `prompts/system_layers/L5_reasoning_layer.md` | created | Structured planning, decomposition, verification before completion |
| `prompts/master_prompts/{project_analysis,architecture,coding,research,review}.md` | created | 5 master prompts |
| `prompts/generators/{agent,skill,prompt}_generator.md` | created | 3 meta-prompts |
| `prompts/benchmarks/{README,rubric,cases}.md` | created | Method, 5-axis rubric, 10 golden cases |
| `logs/SESSION_TEMPLATE.md` | created | Required session log structure |
| `logs/README.md` | created | Logging rules and naming |
| `scripts/auto_commit.ps1` | created | 9-gate commit automation |
| `scripts/verify_structure.ps1` | created | Registry-driven structure verification |
| `scripts/new_session_log.ps1` | created | Session log creation |
| `scripts/README.md` | created | Script usage and conventions |
| `configs/harness.config.json` | created | Agent/skill/prompt registry |
| `configs/quality_gates.json` | created | Operative thresholds |
| `configs/model_routing.json` | created | Model tier guidance |
| `templates/{AGENT,SKILL,ADR,HANDOFF}_TEMPLATE.md` | created | 4 artefact templates |
| `templates/README.md` | created | Template index and rules |
| `docs/adr/.gitkeep` | created | ADR directory established |
| `{agents,skills,prompts,scripts,configs,templates,logs}/.gitkeep` | deleted | Obsolete — directories now have content |

**Files NOT changed that a reader might expect to be:**

| File | Why not |
|---|---|
| `prompts/system_layers/fable5_layer.md` | Not what it was described as — see Problems §1. Left byte-identical; not created by me, so not overwritten |
| `.claude/settings.local.json` | Existing permission config; no reason to touch it |

---

## 4. Tests

```
$ pwsh -NoProfile -File C:\Genesis_Harness\scripts\verify_structure.ps1

=== Genesis Harness — structure verification ===
Repository: C:\Genesis_Harness
[... 15 directories PASS, 2 root files PASS, 4 docs PASS, 18 prompt files PASS,
     2 logging PASS, 4 templates PASS, 6 config checks PASS,
     19 agent checks PASS, 10 skill checks PASS, 6 script checks PASS ...]

-- Size limits
   WARN  prompts/system_layers/fable5_layer.md is 2123 lines (limit 800) — CLAUDE.md section 8.1

Structure verification: 86 passed, 0 failed, 1 warning(s).
```

```
$ pwsh -NoProfile -File C:\Genesis_Harness\scripts\new_session_log.ps1 -Slug "foundation-architecture" -Model "claude-opus-5" -Agents "architect, coding, qa (acting inline)"

Created logs/sessions/2026-07-28_01_foundation-architecture.md
```
Verified the created file: header substitution applied correctly (session ID, date, model, and
agents fields populated; remaining placeholders left for manual completion).

**Status:** verified — for structure verification and session log creation.

**What was verified:**
- All 51 created files exist at their claimed paths (`verify_structure.ps1`, exit code 0)
- All three JSON configs parse as valid JSON
- All six agent adapters begin with `---` (valid frontmatter first line)
- All three PowerShell scripts parse without syntax errors (PowerShell AST parser)
- Every registered agent has both a charter and an adapter; every registered skill has a `SKILL.md`
- `new_session_log.ps1` creates a correctly named and correctly substituted log

**What was NOT verified, and why:**
- **`auto_commit.ps1` gates 3–9 have not been executed.** Only its syntax was checked. Gates 1–2
  and the secret scan logic are untested against real input. Running a real commit is
  ROADMAP next-action 2.
- **No benchmark case has been executed.** All ten cases in `prompts/benchmarks/cases.md` are
  defined but unrun; the baseline table is empty by design.
- **No agent has been invoked.** The six adapters are structurally valid but have never been
  dispatched. Their descriptions have not been shown to actually trigger correct auto-selection.
- **The Genesis Loop has never been run end to end.** This is the whole point of Phase 1.

---

## 5. Problems

| # | Severity | Problem | Resolved? | Detail |
|---|---|---|---|---|
| 1 | HIGH | `prompts/system_layers/fable5_layer.md` is not a reasoning layer | **No — escalated** | It is a 2,123-line verbatim dump of a Claude Code system prompt belonging to a different user (contains a third-party email address, a macOS/zsh environment, and `<project-dir>` placeholders), self-labelled "This is a replacement system prompt." The pre-existing `CLAUDE.md` instructed agents to consult it for reasoning principles, which it does not contain. I did not create the file, and its content contradicts how it was described, so I left it byte-identical rather than overwriting or moving it. Instead I wrote `L5_reasoning_layer.md` with the five principles `CLAUDE.md` actually named, and repointed the constitution at it. **Operator decision required: delete, archive, or keep.** |
| 2 | MEDIUM | The harness has never been used to build anything | No — by design | Every process claim in these documents is untested in practice. This is exactly what Phase 1 exists to test |
| 3 | LOW | `quality_gates.json` sets an 80% coverage target nothing can enforce | No — by design | `coverageEnforced: false` with a comment explaining it activates in Phase 2 when a test runner exists. Recorded rather than hidden |
| 4 | LOW | Benchmarks are self-scored by the same model that produces the output | No — mitigated | Documented in `benchmarks/README.md` §Known Bias. Mitigated by behavioural rather than impressionistic criteria, and by mandatory held-out cases |

**Open problems carried forward:** all four. #1 needs an operator decision; #2 resolves through
Phase 1; #3 resolves in Phase 2; #4 is inherent to a single-model benchmark and is documented
rather than solved.

---

## 6. Next Actions

| # | Action | Owning agent | Blocked by | Acceptance |
|---|---|---|---|---|
| 1 | Decide the fate of `prompts/system_layers/fable5_layer.md` (delete / archive / keep) | human | operator decision | The file is removed, moved to an `_archive/` path, or explicitly kept with a note in ROADMAP |
| 2 | Run `pwsh -File scripts/auto_commit.ps1 -Message "test" -DryRun` and confirm gates 1–7 behave as `scripts/README.md` documents | qa | — | A session log records the real output of each gate; any divergence from the documented behaviour is filed as a defect |
| 3 | Pick one small real feature and run it through all 8 Genesis Loop stages | architect | — | A session log shows every stage with its artefact, and real command output at stage 6 |
| 4 | Execute benchmark cases C-001, C-003, C-008; record baselines | qa | — | Three rows added to the baseline table in `prompts/benchmarks/cases.md` |
| 5 | Write ADR 0001 selecting the first real technical target for the Genesis Engine | architect | 3 | `docs/adr/0001-*.md` exists, follows `templates/ADR_TEMPLATE.md`, and includes a reversal trigger |

---

## 7. State At End Of Session

**Branch:** main
**Working tree:** dirty at time of writing — 60 new files plus 3 modified, pending commit
**Committed:** pending — `AI: Create Genesis Harness foundation architecture`
**Pushed:** pending
**Structure check:** pass — 86 passed, 0 failed, 1 warning
**Documentation updated:** `README.md`, `docs/ARCHITECTURE.md`, `docs/AGENTS.md`,
`docs/WORKFLOW.md`, `docs/ROADMAP.md` — all created or filled in this session

---

## 8. Notes For The Next Session

- **Read the ROADMAP open-problems table first.** Problem #1 is the one that needs a human.
- **The `auto_commit.ps1` secret scanner excludes two paths by design** (`scripts/auto_commit.ps1`
  and `configs/quality_gates.json`) because they document the credential patterns they would
  otherwise match. This exclusion is in `$SecretScanExclusions` with a comment. If the scanner
  ever appears to miss something, check that list first.
- **Structure verification is registry-driven.** Adding an agent or skill to
  `configs/harness.config.json` without creating its files will fail the commit gate. That is
  intentional, not a bug.
- **The 800-line warning currently fires only on `fable5_layer.md`.** Once that is resolved, the
  structure check should be clean. If a new warning appears, something grew past the limit.
- **These documents are unusually complete for an unproven system.** Treat the process claims as
  designed-but-untested. If Phase 1 shows the ceremony exceeds the value, cut it — over-applied
  process is a documented failure mode (`L5_reasoning_layer.md` §7), not a virtue to defend.
- **Do not add a `.claude/skills/` mirror.** Skills are loaded by path from `skills/`. Mirroring
  them was considered and rejected as duplication with no benefit.
