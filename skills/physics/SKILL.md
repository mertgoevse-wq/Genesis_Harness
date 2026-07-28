---
id: physics
category: science
version: 1.0.0
primary_agents: [simulation-scientist, research]
supporting_agents: [coding, game-design]
---

# Skill: Physics

## 1. Purpose

Provide the physical reasoning required to model, implement, and validate mechanical, thermal,
fluid, electromagnetic, and gravitational systems — with correct units, stated assumptions, and
known validity ranges.

This skill exists to prevent the most common simulation failure: code that produces plausible
motion while violating the physics it claims to model.

## 2. Knowledge Domain

### Classical mechanics
Kinematics; Newton's laws; work, energy, power; momentum and impulse; rotational dynamics,
torque, moment of inertia, angular momentum; oscillators and damping; Lagrangian and Hamiltonian
formulations; constraints and generalised coordinates; non-inertial frames and fictitious forces.

### Rigid & soft body dynamics
Inertia tensors; quaternion orientation; collision detection (broad phase / narrow phase, GJK,
SAT); collision response, restitution, and friction models (Coulomb); constraint solvers
(sequential impulse, projected Gauss–Seidel); joints; mass–spring systems; position-based dynamics;
penetration resolution and drift.

### Thermodynamics & statistical mechanics
Laws of thermodynamics; state variables; heat capacity; conduction, convection, radiation;
entropy; ideal and real gases; phase transitions; Boltzmann distribution; ensembles;
equipartition.

### Fluid dynamics
Continuity and Navier–Stokes equations; Reynolds number and regimes; incompressible vs
compressible flow; pressure projection; SPH (smoothed particle hydrodynamics); grid/Eulerian
methods; vorticity; boundary conditions; buoyancy and drag.

### Electromagnetism & waves
Maxwell's equations; electrostatics and magnetostatics; circuits; wave equation; interference,
diffraction, reflection, refraction; geometric and physical optics; radiation.

### Gravitation & orbits
Newtonian gravitation; two-body and N-body problems; Kepler's laws; orbital elements; transfer
orbits; tidal forces; when general-relativistic corrections become non-negligible.

### Cross-cutting
SI units and dimensional analysis; conservation laws; symmetry and Noether's theorem; scaling and
similarity; order-of-magnitude estimation; error propagation.

## 3. When To Use

**Use when:**
- Designing or reviewing any motion, collision, force, thermal, fluid, or orbital system.
- Choosing an integrator or diagnosing instability, energy drift, or jitter.
- Converting a "feel" requirement into physical parameters.
- Validating simulation output against expected physical behaviour.
- Estimating whether a physical approach is computationally feasible at target scale.

**Do not use when:**
- The system is purely economic, narrative, or data-processing.
- A game system only needs to *look* physical and has been explicitly scoped as non-physical —
  in that case say so in the design rather than half-implementing physics.

## 4. Method

1. Identify the regime and scale (length, time, mass, energy). Regime determines which model applies.
2. Choose the fidelity tier and state it: qualitative-plausible / quantitative-approximate /
   quantitative-accurate.
3. Write the governing equations. Define every symbol and unit.
4. Run dimensional analysis. If units do not balance, the model is wrong — stop.
5. Enumerate assumptions and the error each introduces.
6. Choose the numerical scheme and state its stability limit.
7. Define conservation checks and validation cases with known answers.
8. State the validity range and out-of-range failure mode.

## 5. Expected Output

- **Model specification** in the Simulation Scientist output format (equations, symbol table with
  units, assumption ledger, integrator + stability criterion, conservation tolerances, validation
  cases, validity range).
- **Confidence label** on every constant and formula (VERIFIED / KNOWN / ASSUMED).
- **Feasibility verdict** with an order-of-magnitude cost estimate when performance is in question.

## 6. Guardrails

- Never state a physical constant without a confidence label; route load-bearing values to the
  Research Agent.
- Never mix unit systems within one model.
- Never use an explicit integrator on a stiff system without declaring the step-size penalty.
- Never claim energy conservation for a scheme that does not conserve it (forward Euler does not).
- Never present a numerical result as physical truth without stating the tolerance.
- Distinguish *stable*, *accurate*, and *plausible* — they are three different properties.

## 7. Related

`skills/simulation` · `skills/astronomy` · `skills/chemistry` · `skills/game-development`
