# Scripts

**Version:** 1.0.0 · **Last updated:** 2026-07-28

PowerShell automation for the harness. All scripts target **PowerShell 7+ (`pwsh`)** and are run
from the repository root.

| Script | Purpose |
|---|---|
| [auto_commit.ps1](auto_commit.ps1) | Stage, commit, and push behind nine safety gates |
| [verify_structure.ps1](verify_structure.ps1) | Verify the repository structure is intact |
| [new_session_log.ps1](new_session_log.ps1) | Create today's session log from the template |

---

## auto_commit.ps1

```powershell
# See what would happen, change nothing
pwsh -File scripts/auto_commit.ps1 -Message "docs: clarify handoff contract" -DryRun

# Commit locally
pwsh -File scripts/auto_commit.ps1 -Message "feat: add benchmark runner"

# Commit and push
pwsh -File scripts/auto_commit.ps1 -Message "feat: add benchmark runner" -Push
```

### Gates

| # | Gate | Blocks on |
|---|---|---|
| 1 | Repository check | Not a git repo, or git unavailable |
| 2 | Change check | No changes, or no `-Message` |
| 3 | Secret scan | Credential-shaped content in changed files |
| 4 | Large file check | Warns only, above 512 KB |
| 5 | Structure check | `verify_structure.ps1` fails |
| 6 | Session log check | No session log for today |
| 7 | Branch check | Prompts before committing to `main` |
| 8 | Commit | git failure |
| 9 | Push | Only with `-Push`; never forces |

**A failed gate aborts before anything is staged.** The repository is left exactly as it was.

### Escape hatches

| Flag | Effect | When it is legitimate |
|---|---|---|
| `-DryRun` | Evaluate all gates, change nothing | Always safe; use it first |
| `-SkipStructureCheck` | Skip gate 5 | Only when editing `verify_structure.ps1` itself |
| `-AllowNoSessionLog` | Skip gate 6 | Mechanical commits only (`.gitignore`, typo fixes) |
| `-Force` | Skip the gate 7 prompt | Non-interactive runs. **Does not bypass any other gate.** |

The script never force-pushes, never rewrites history, and never passes `--no-verify` —
those are constitutional prohibitions (`CLAUDE.md` §6.2), not defaults.

### Secret scan

Nine credential patterns (AWS keys, private key blocks, GitHub/Slack/Anthropic tokens, generic
`api_key`/`secret` assignments, bearer tokens, connection strings with inline credentials).

It reports **file and line number only — never the matched value**, so the log of a failed
commit does not itself become a leak.

This is a tripwire, not a real secret scanner. A clean pass is not proof there is no secret.

---

## verify_structure.ps1

```powershell
pwsh -File scripts/verify_structure.ps1
pwsh -File scripts/verify_structure.ps1 -Quiet    # failures + summary only
```

Checks: required directories · root files · the four canonical docs · every prompt file ·
logging system · templates · configs (including JSON validity) · every registered agent has
both a charter and an adapter with valid frontmatter · every registered skill has a `SKILL.md` ·
every script parses without syntax errors · no markdown file exceeds 800 lines.

Agent and skill checks are **driven by `configs/harness.config.json`**, so registering a new
component automatically extends the check. Registering without creating the files fails the gate.

Exit code `0` = pass, `1` = at least one failure. Warnings do not fail the run.

---

## new_session_log.ps1

```powershell
pwsh -File scripts/new_session_log.ps1 -Slug "foundation-architecture"
pwsh -File scripts/new_session_log.ps1 -Slug "benchmark-runner" -Model "claude-opus-5" -Agents "architect,coding,qa"
```

Creates `logs/sessions/YYYY-MM-DD_NN_<slug>.md` with the next sequence number for today.
Normalises the slug to kebab-case. **Refuses to overwrite** — session logs are append-only.

---

## Conventions For New Scripts

1. Comment-based help at the top: `.SYNOPSIS`, `.DESCRIPTION`, `.PARAMETER`, `.EXAMPLE`.
2. `Set-StrictMode -Version Latest` and `$ErrorActionPreference = 'Stop'`.
3. Derive paths from `$PSScriptRoot`. Never assume the caller's working directory.
4. Meaningful exit codes: `0` success, `1` failure.
5. **Fail closed.** On an unexpected condition, abort without changing state.
6. Never print a secret, even one you detected.
7. Offer `-DryRun` for anything that mutates state.
8. Register the script in `verify_structure.ps1` so its syntax is checked on every commit.
