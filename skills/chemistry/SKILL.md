---
id: chemistry
category: science
version: 1.0.0
primary_agents: [simulation-scientist, research]
supporting_agents: [coding]
---

# Skill: Chemistry

## 1. Purpose

Provide the chemical reasoning required to model matter, reactions, and material behaviour —
composition, energetics, kinetics, and equilibrium — with correct stoichiometry, units, and
stated validity.

## 2. Knowledge Domain

### Atomic & molecular structure
Electron configuration; periodic trends; ionisation energy and electronegativity; orbital theory;
covalent, ionic, metallic bonding; VSEPR geometry; hybridisation; intermolecular forces
(van der Waals, hydrogen bonding, dipole interactions); isomerism and chirality.

### Stoichiometry & composition
Moles, molar mass, Avogadro's number; balancing equations; limiting reagents; yield (theoretical,
actual, percent); concentration units (molarity, molality, mole fraction, ppm); solution
preparation and dilution.

### Thermochemistry
Enthalpy, entropy, Gibbs free energy; Hess's law; bond energies; heats of formation, combustion,
solution; calorimetry; spontaneity criteria; temperature dependence.

### Kinetics
Rate laws and reaction order; rate constants; Arrhenius equation and activation energy; reaction
mechanisms and rate-determining steps; catalysis; half-life; collision and transition-state theory;
integrated rate equations.

### Equilibrium
Equilibrium constants (Kc, Kp, Ksp); Le Chatelier's principle; acid–base equilibria, pH, pKa,
buffers, titration curves; solubility and precipitation; complex-ion equilibria; coupled equilibria.

### Redox & electrochemistry
Oxidation states; half-reactions; standard potentials; Nernst equation; galvanic and electrolytic
cells; corrosion; Faraday's laws.

### Computational chemistry
Molecular dynamics force fields (bonded/non-bonded terms, Lennard-Jones, Coulomb); ensembles and
thermostats; periodic boundary conditions; timestep constraints (bond vibration limits); coarse-
graining; reaction-diffusion systems; Gillespie stochastic simulation for low-copy-number species.

### Transport
Diffusion (Fick's laws); viscosity; osmosis; mass transfer; partition coefficients.

## 3. When To Use

**Use when:**
- Modelling reactions, material properties, phase behaviour, or molecular interactions.
- Designing a crafting, alchemy, refining, or material system that claims chemical grounding.
- Choosing between deterministic (ODE) and stochastic (Gillespie) reaction modelling.
- Validating that a simulated reaction conserves mass, charge, and energy.
- Selecting a force field, timestep, or thermostat for molecular dynamics.

**Do not use when:**
- The "chemistry" is purely a game-fiction naming layer with no modelled behaviour — say so
  explicitly rather than implying real chemistry.

## 4. Method

1. Define the system: species, phases, temperature, pressure, volume, and whether it is open,
   closed, or isolated.
2. Balance every equation. Verify conservation of mass and charge.
3. Decide thermodynamics (will it happen?) vs kinetics (how fast?) — most modelling errors come
   from conflating these.
4. Choose the modelling regime: equilibrium, deterministic kinetics, stochastic kinetics, or MD.
5. State concentration/unit conventions once and enforce them.
6. For MD, derive the timestep from the fastest vibrational mode; state constraint schemes used.
7. Define validation: known equilibrium constants, known rates, or limiting behaviour.

## 5. Expected Output

- **Reaction/system specification**: species table (formula, phase, molar mass, initial
  concentration), balanced equations, thermodynamic data with sources, rate laws with constants
  and temperature dependence.
- **Modelling regime decision** with justification and cost implication.
- **Conservation checks** (mass, charge, energy) with tolerances.
- **Validity range**: temperature, pressure, and concentration bounds outside which the model
  is invalid.
- **Confidence label** on every thermodynamic or kinetic constant.

## 6. Guardrails

- Never present an unbalanced equation.
- Never quote a rate constant or equilibrium constant without its temperature.
- Never conflate thermodynamic favourability with kinetic accessibility.
- Never use a molecular-dynamics timestep larger than the fastest mode allows without declaring
  the constraint algorithm.
- Never extrapolate a rate law outside its measured range without labelling it ASSUMED.
- Route all load-bearing constants to the Research Agent for verification.

## 7. Related

`skills/physics` · `skills/biology` · `skills/simulation`
