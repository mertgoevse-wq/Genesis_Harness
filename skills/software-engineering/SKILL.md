---
id: software-engineering
category: engineering
version: 1.0.0
primary_agents: [coding, architect, qa]
supporting_agents: [research, game-design, simulation-scientist]
---

# Skill: Software Engineering

## 1. Purpose

Provide the baseline engineering discipline every agent in this harness is held to: how code is
structured, how errors are handled, how correctness is established, and how systems stay
maintainable as they grow.

This is the default skill. When no other skill applies, this one does.

## 2. Knowledge Domain

### Design & structure
Separation of concerns; cohesion and coupling; dependency direction and inversion; interface
design; layered and hexagonal architecture; module boundaries; composition over inheritance;
pure core / imperative shell; state ownership; the repository pattern; event-driven decomposition.

### Code quality
Naming as documentation; function size and single responsibility; early returns over deep nesting;
immutability by default; explicit over implicit; avoiding primitive obsession; making illegal
states unrepresentable; the cost of premature abstraction (YAGNI) and of real duplication (DRY).

### Error handling
Error taxonomy: expected failure vs bug vs catastrophe; result types vs exceptions; failing fast
at boundaries; never swallowing errors; error context propagation; retry with backoff and its
limits; idempotency; graceful degradation vs silent fallback (the second is a defect); structured
logging.

### Testing
Test pyramid (unit / integration / end-to-end); TDD red-green-refactor; AAA structure;
behavioural over implementation-coupled tests; test naming that states behaviour; fixtures and
isolation; mocking boundaries only; property-based testing; regression tests for every fixed bug;
coverage as a signal, not a goal; flaky-test quarantine and root-causing.

### Security
Input validation at every boundary; injection classes (SQL, command, path, template); output
encoding; authentication vs authorisation; least privilege; secrets management (never in source);
dependency and supply-chain risk; safe defaults; error messages that do not leak internals;
OWASP Top 10 as a checklist, not a ceiling.

### Performance
Measure before optimising; algorithmic complexity first, constants second; data layout and cache
behaviour; N+1 query patterns; pagination and bounded queries; caching with a stated invalidation
strategy; async and concurrency hazards (races, deadlocks, ordering); backpressure.

### Debugging
Reproduce → isolate → hypothesise → test → fix → verify → check for siblings; bisection; reading
the actual error rather than pattern-matching it; instrumenting rather than guessing; rubber-duck
articulation of the mechanism; distinguishing symptom from cause.

### Delivery
Version control hygiene; conventional commits; small reviewable changes; code review as a
correctness gate not a style gate; CI as the source of truth; reversibility of deployments;
documentation as part of the change.

## 3. When To Use

**Use when:** writing, reviewing, refactoring, debugging, testing, or structuring any code in
this repository — which is to say, by default.

## 4. Method

1. Read the surrounding code before writing. Match its conventions.
2. Search for an existing implementation before writing a new one.
3. Define the contract (inputs, outputs, errors, invariants) before the body.
4. Write the failing test first where a runner exists; otherwise define the manual verification
   command before implementing.
5. Implement the minimum that satisfies the contract.
6. Execute it. Capture real output.
7. Harden: boundaries, error paths, edge cases.
8. Refine structure and naming; re-run.
9. Update documentation in the same change.

## 5. Expected Output

- Code that matches the surrounding style and satisfies its stated contract.
- **Verification evidence**: exact command, exact output.
- A change summary: files, action, purpose, and what was *not* done.
- Explicit error-handling table for new boundaries.
- Follow-ups with severity and owner.

## 6. Guardrails

- **Never report unexecuted code as verified.** `implemented-not-run` is the honest status.
- Never leave an empty catch, a swallowed error, or a fallback that hides failure.
- Never hardcode a secret, credential, endpoint, or unexplained number.
- Never exceed 800 lines/file, 50 lines/function, 4 levels of nesting.
- Never mix a refactor with a behavioural change in one commit.
- Never delete or disable a test to reach green.
- Never change a public contract without the Architect Agent.
- Never optimise without a measurement, or abstract without a second real caller.

## 7. Related

`skills/simulation` · `skills/game-development` · `skills/ai-agents` · `skills/prompt-engineering`
