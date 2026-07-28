---
id: astronomy
category: science
version: 1.0.0
primary_agents: [simulation-scientist, research]
supporting_agents: [coding, game-design]
---

# Skill: Astronomy

## 1. Purpose

Provide the astronomical and astrophysical reasoning required to model celestial bodies, orbital
systems, stellar behaviour, and cosmic scale — with correct reference frames, unit systems, and
honest treatment of the enormous dynamic ranges involved.

## 2. Knowledge Domain

### Celestial mechanics
Two-body problem and Kepler's laws; orbital elements (a, e, i, Ω, ω, ν); orbital energy and
vis-viva equation; Hohmann and bi-elliptic transfers; delta-v budgets; N-body dynamics and
numerical integration; Lagrange points; sphere of influence and patched conics; perturbations;
tidal locking and tidal heating; resonances; Roche limit.

### Reference frames & time
Inertial vs rotating frames; ecliptic, equatorial, galactic coordinates; epochs; Julian dates;
sidereal vs solar time; precession and nutation; barycentric vs heliocentric frames; light-time
correction.

### Stellar physics
Hertzsprung–Russell diagram; stellar classification; mass–luminosity relation; nuclear fusion
chains (pp-chain, CNO); hydrostatic equilibrium; stellar lifecycle by mass; main-sequence
lifetimes; white dwarfs, neutron stars, black holes; Chandrasekhar and TOV limits; supernovae;
variable stars.

### Planetary science
Planet formation and accretion; differentiation; atmospheres and escape velocity, Jeans escape;
greenhouse effect; habitable zones (and their limits as a concept); magnetospheres; impact
cratering; moons and ring systems; exoplanet detection methods and their biases.

### Galactic & cosmological
Galaxy morphology; rotation curves and dark matter evidence; interstellar medium; star formation
regions; the cosmic distance ladder; redshift and Hubble's law; cosmic microwave background;
large-scale structure; ΛCDM as the standard model and its open questions.

### Radiation & observation
Blackbody radiation, Wien's law, Stefan–Boltzmann; magnitude systems (apparent, absolute,
bolometric); flux and luminosity; spectroscopy and spectral lines; Doppler shift; extinction and
reddening; angular size and resolution; parallax.

### Scale & units
AU, light-year, parsec; solar mass/radius/luminosity units; orders of magnitude across 40+
decades; floating-point precision limits when representing astronomical scales.

## 3. When To Use

**Use when:**
- Modelling orbits, star systems, planetary environments, or space navigation.
- Designing space-based games, procedural universe generation, or astronomical visualisation.
- Choosing an integrator for long-duration orbital simulation (energy drift over millions of steps
  is the defining problem).
- Deciding coordinate systems, reference frames, and numeric precision for large-scale space.
- Establishing plausible values for stellar and planetary parameters.

## 4. Method

1. Fix the scale and the reference frame first. Most space-simulation bugs are frame or
   precision bugs, not physics bugs.
2. Choose the unit system deliberately — scaled units (AU, solar masses, years) usually beat SI
   for orbital work and avoid float overflow/underflow.
3. Assess numeric precision: 32-bit float loses metre-level precision at planetary distances.
   State the precision strategy (double, origin rebasing, hierarchical/relative coordinates).
4. Choose the integrator with long-term behaviour in mind — symplectic (Verlet, leapfrog, WHFast)
   for orbits; RK4 drifts energy over long runs.
5. Decide fidelity: Keplerian analytic (fast, stable, no perturbations), patched conics, or full
   N-body — and state the consequence of the choice.
6. Define conservation checks: energy, angular momentum, and orbital element drift.
7. Validate against known systems with published elements.

## 5. Expected Output

- **System specification**: bodies with masses, radii, orbital elements, and epoch; reference
  frame; unit system; precision strategy.
- **Integrator decision** with the long-term drift characteristic stated.
- **Conservation and drift tolerances** over the intended simulated duration.
- **Validation cases** against real systems with published values.
- **Scale/precision analysis** naming where the representation breaks down.
- **Confidence label** on every astronomical constant.

## 6. Guardrails

- Never use single-precision floats for absolute positions at interplanetary scale.
- Never use a non-symplectic integrator for long-duration orbital simulation without declaring
  the energy drift.
- Never state an orbital element without its epoch and reference frame.
- Never present "habitable zone" as a binary or as a sufficient condition for life.
- Never mix scaled and SI units silently.
- Distinguish observation from inference from model (e.g. dark matter is inferred from dynamics).
- Route load-bearing constants and system parameters to the Research Agent.

## 7. Related

`skills/physics` · `skills/simulation` · `skills/game-development`
