---
id: simulation
category: engineering
version: 1.0.0
primary_agents: [simulation-scientist, architect, coding]
supporting_agents: [qa, game-design]
---

# Skill: Simulation

## 1. Purpose

Provide the engineering discipline for building simulations that are **numerically stable,
reproducible, performant, and verifiable** — the bridge between a scientific model and running
code.

Where `physics`/`chemistry`/`biology` answer *what the model is*, this skill answers *how to
compute it correctly and fast enough*.

## 2. Knowledge Domain

### Numerical integration
Explicit Euler (and why it gains energy); semi-implicit / symplectic Euler; velocity Verlet;
leapfrog; Runge–Kutta (RK2, RK4, RKF45); implicit and semi-implicit methods; adaptive time
stepping; sub-stepping; operator splitting. Order of accuracy vs stability vs cost.

### Stability & error
Stiffness and stiff systems; CFL condition; von Neumann stability analysis; truncation vs
round-off error; error accumulation over long runs; energy drift; convergence testing
(halve Δt, verify error scales with the expected order); conditioning.

### Determinism & reproducibility
Fixed vs variable timestep; the accumulator pattern; floating-point non-determinism across
platforms and compilers; seeded PRNGs and stream separation; deterministic ordering of parallel
reductions; replay and state snapshotting; checksum/desync detection.

### Spatial data structures
Uniform grids; hash grids; quadtrees/octrees; BVH; k-d trees; sweep-and-prune; neighbour lists
and Verlet lists with skin distance; rebuild vs refit strategies.

### Performance
Data-oriented design; struct-of-arrays vs array-of-structs; cache locality; SIMD; multithreading
and work partitioning; GPU compute suitability; hierarchical/multi-rate updates; level of detail;
sleeping and deactivation; profiling before optimising.

### Architecture patterns
Entity-component-system; double buffering of state; command/event queues; fixed-step simulation
with interpolated rendering; deterministic lockstep; authoritative server with client prediction
and reconciliation; save/load of full simulation state.

### Validation & verification
Verification (solving the equations right) vs validation (solving the right equations);
analytical benchmark cases; convergence studies; conservation monitoring; regression baselines
with tolerances; property-based invariant testing; differential testing against a reference
implementation.

## 3. When To Use

**Use when:**
- Implementing any time-stepped or iterative numerical system.
- Diagnosing instability, explosion, jitter, drift, or tunnelling.
- Choosing a timestep, integrator, or spatial structure.
- Requiring reproducibility (replays, networked lockstep, scientific runs, regression tests).
- Optimising a simulation loop.
- Designing how simulation state is stored, saved, or synchronised.

## 4. Method

1. **Separate model from solver.** The governing equations are one artefact; the integrator is
   another. Do not entangle them.
2. **Fix the timestep** for anything that must be deterministic or stable. Use the accumulator
   pattern and interpolate for rendering.
3. **Choose the integrator from the system's character**, not habit: symplectic for
   energy-conserving mechanics, implicit for stiff systems, adaptive for varying dynamics.
4. **Derive the stability limit** and set Δt below it with margin. Document the margin.
5. **Instrument conservation** from day one — energy, momentum, mass, count. Drift is the earliest
   signal that something is wrong.
6. **Establish a reference case** with a known answer before optimising anything.
7. **Run a convergence study**: halve Δt; error must fall at the integrator's stated order.
   If it does not, the implementation disagrees with the theory.
8. **Profile before optimising.** Then optimise data layout before algorithms, and algorithms
   before micro-optimisation.
9. **Snapshot and replay** to make bugs reproducible.

## 5. Expected Output

- **Solver specification**: integrator, timestep, sub-stepping policy, stability margin.
- **Determinism policy**: fixed-step guarantee, PRNG seeding scheme, ordering guarantees,
  and explicitly what is *not* deterministic.
- **State layout**: what constitutes full simulation state, and how it is saved/restored.
- **Conservation instrumentation**: which quantities are monitored, tolerance, and the action on
  breach.
- **Convergence study results**: Δt vs error, with the observed order.
- **Performance budget**: target step time, current step time, dominant cost, next bottleneck.
- **Regression baselines**: reference scenarios with expected outputs and tolerances.

## 6. Guardrails

- Never use a variable timestep in a system that must be deterministic or stable.
- Never ship explicit Euler for oscillatory or orbital mechanics — it injects energy.
- Never claim determinism across platforms without testing it; floating point does not guarantee it.
- Never optimise before a correctness baseline exists.
- Never tune a magic constant to hide instability — find the stability violation.
- Never let a conservation check exist without an action when it is breached.
- Never present a simulation result without its timestep, tolerance, and duration.
- Clamping and damping are band-aids; state clearly when one is used to mask a real instability.

## 7. Related

`skills/physics` · `skills/chemistry` · `skills/biology` · `skills/astronomy` ·
`skills/software-engineering` · `skills/game-development`
