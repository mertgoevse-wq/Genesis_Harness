# Logging System

**Version:** 1.0.0 · **Last updated:** 2026-07-28

Session logs are the harness's memory. They are the mechanism by which work survives the end of
a context window, a model change, or a six-week gap.

**Every AI session that changes the repository writes a log. No exceptions.**
A change without a log is an incomplete change.

---

## Layout

```
logs/
├── README.md              This file
├── SESSION_TEMPLATE.md    The required structure
└── sessions/              YYYY-MM-DD_NN_<slug>.md
```

## Naming

```
YYYY-MM-DD_NN_<slug>.md
│          │   └─ short kebab-case description
│          └───── sequence number within that day, zero-padded (01, 02, ...)
└──────────────── ISO date
```

Example: `2026-07-28_01_foundation-architecture.md`

Sorting lexicographically sorts chronologically. That is the point of the format.

---

## Creating A Log

```powershell
pwsh -File scripts/new_session_log.ps1 -Slug "foundation-architecture"
```

The script picks the next sequence number for today, copies the template, and stamps the date.
It refuses to overwrite an existing file.

---

## Required Fields

| Field | Why it exists |
|---|---|
| **date** | Ordering and staleness assessment |
| **model** | Behaviour differs by model; a log without one cannot be interpreted |
| **agents used** | Attribution and workflow analysis |
| **task** | What was asked, and how it was interpreted |
| **reasoning summary** | **The point of the log** — why, including options rejected |
| **changes** | What moved, including what deliberately did not |
| **tests** | Real command, real output, honest status |
| **problems** | What went wrong, resolved or carried forward |
| **next actions** | Executable by a fresh agent with no memory |

---

## Rules

1. **Append-only.** A past log is never rewritten. Correct it with a new entry that references
   the old one. The history of what was believed is part of the record.
2. **Reasoning over description.** The diff already records what changed. The log exists to
   record why, and what was considered and rejected.
3. **Real output only.** The tests section contains commands actually run and output actually
   observed. `not run` is a valid value. **Fabricating a result is a CRITICAL violation** —
   it poisons every future session that trusts the log.
4. **Next actions pass the cold-start test.** If a fresh agent cannot execute it from the text
   alone, rewrite it.
5. **Absolute dates.** `2026-07-28`, never "yesterday".
6. **Honest status.** `verified` / `implemented-not-run` / `failing` are three different things.

---

## Reading Logs At Session Start

The bootstrap sequence in `CLAUDE.md` §10 requires reading the two most recent session logs.
Read them for:

- **Next actions** — the work queue
- **Open problems** — what is already known to be broken
- **Assumptions** — what the previous session bet on, which may now be falsifiable
- **Notes for the next session** — the things that do not fit anywhere else

If a log's assumption contradicts what you observe now, that is a finding. Record it in your own
log rather than editing theirs.

---

## What Does Not Belong Here

- Secrets, tokens, credentials, or personal data.
- Full file contents — reference paths instead.
- Verbatim transcripts. Summarise reasoning; do not paste the conversation.
- Aspirational descriptions of work that was not done.
