---
id: game-development
category: engineering
version: 1.0.0
primary_agents: [game-design, coding, architect]
supporting_agents: [qa, simulation-scientist]
---

# Skill: Game Development

## 1. Purpose

Provide both the **design** discipline (what makes a game work as an experience) and the
**engineering** discipline (how real-time interactive systems are built) so that gameplay
intent survives contact with implementation.

## 2. Knowledge Domain

### Design
Core/mid/meta loop structure; player verbs and agency; risk/reward; pacing, tension, release;
difficulty and mastery curves; economy design (sources, sinks, faucets, drains, inflation);
progression axes and gating; emergent vs authored complexity; failure states and recovery cost;
onboarding and teaching through play; session length design; retention and endgame structure;
multiplayer balance, counterplay, and asymmetry; degenerate strategies and dominant-option analysis.

### Game feel
Input latency budgets; input buffering and coyote time; animation cancelling; acceleration curves;
screen shake, hitstop, and impact framing; audio-visual feedback layering; camera behaviour and
smoothing; responsiveness thresholds (sub-100 ms perceived immediacy); readability under visual load.

### Engine architecture
Game loop structure; fixed-step update with interpolated render; entity-component-system; scene
graphs and transform hierarchies; event/message systems; state machines and behaviour trees;
resource loading and streaming; save systems and versioned save data; modding/data-driven design;
hot reload.

### Real-time systems
Frame budget arithmetic (16.67 ms @ 60 Hz, 8.33 ms @ 120 Hz); update vs render separation;
physics stepping and interpolation; spatial partitioning for queries; object pooling; garbage
pressure and allocation avoidance in the hot path; level of detail; culling; async loading.

### Networking
Client-server authority; lockstep determinism; client-side prediction; server reconciliation;
entity interpolation and extrapolation; lag compensation; snapshot and delta compression;
tick-rate selection; anti-cheat surface and trust boundaries.

### UX & accessibility
HUD information hierarchy; affordance and discoverability; control remapping; colour-independent
information encoding; subtitle and text scaling; difficulty and assist options; motion-sensitivity
options; input-timing accommodations; readable contrast; screen-reader considerations for menus.

### Production
Vertical slice discipline; prototype-to-production transitions; playtesting protocol and how to
read player behaviour vs player opinion; telemetry design; balance iteration loops; content
pipelines; scope control.

## 3. When To Use

**Use when:**
- Designing or reviewing any player-facing system.
- Building an engine subsystem, game loop, or real-time architecture.
- Diagnosing "it works but feels bad".
- Setting frame budgets or making performance trade-offs against gameplay.
- Designing networking authority or predicting multiplayer failure modes.
- Planning playtests or interpreting their results.

## 4. Method

1. State the player fantasy, then the core loop, before any system detail.
2. Convert every feel requirement into a number before implementation.
3. Separate simulation update from render; fix the simulation step; interpolate for display.
4. Set the frame budget and allocate it per subsystem before optimising anything.
5. Design the economy as a closed system; verify it cannot trivially break or trivially stall.
6. Run the adversarial pass on every system: degenerate optimum, griefer, low-skill player,
   maximum-skill player.
7. Specify accessibility accommodations at design time.
8. Define playtest questions with pass conditions before the playtest, not after.
9. Prefer data-driven configuration for anything that will be balance-tuned.

## 5. Expected Output

- **System spec** with loops, verbs, feedback channels, and numeric feel targets.
- **Economy table**: resources, sources, sinks, rates, caps, and the failure mode if unbalanced.
- **Frame budget**: per-subsystem millisecond allocation against the target frame rate.
- **Architecture note**: update/render separation, authority model, state ownership.
- **Adversarial review**: degenerate strategies and mitigations.
- **Accessibility requirements** as testable statements.
- **Playtest criteria**: questions with explicit pass conditions.

## 6. Guardrails

- Never accept a feel word ("snappy", "weighty", "juicy") as a specification.
- Never couple gameplay logic to the render frame rate.
- Never design a resource with a source and no sink.
- Never trust the client in a competitive multiplayer system.
- Never treat accessibility as post-launch polish.
- Never balance from opinion alone — use observed behaviour and telemetry.
- Never let a system ship without feedback for every player action.
- Distinguish "players said" from "players did"; the second is evidence, the first is a hypothesis.

## 7. Related

`skills/simulation` · `skills/software-engineering` · `skills/physics` · `skills/ai-agents`
