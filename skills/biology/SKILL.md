---
id: biology
category: science
version: 1.0.0
primary_agents: [simulation-scientist, research]
supporting_agents: [coding, game-design]
---

# Skill: Biology

## 1. Purpose

Provide the biological reasoning required to model living systems across scales — molecular,
cellular, organismal, population, and ecosystem — including growth, metabolism, inheritance,
selection, and feedback regulation.

## 2. Knowledge Domain

### Molecular & cellular
DNA/RNA structure; replication, transcription, translation; the genetic code; gene regulation
(operons, transcription factors, epigenetics); protein structure and folding; enzyme kinetics
(Michaelis–Menten, inhibition types); metabolic pathways (glycolysis, Krebs cycle, oxidative
phosphorylation, photosynthesis); ATP energetics; membrane transport; signalling cascades; cell
cycle and division; apoptosis.

### Genetics & evolution
Mendelian inheritance; linkage and recombination; mutation types and rates; Hardy–Weinberg
equilibrium; genetic drift; natural, sexual, and artificial selection; fitness landscapes;
speciation; phylogenetics; horizontal gene transfer; evolutionary game theory.

### Organismal
Homeostasis and negative feedback; circulatory, respiratory, digestive, nervous, endocrine, and
immune systems; thermoregulation; growth and allometric scaling; metabolic rate scaling
(Kleiber's law); development and morphogenesis; sensory systems.

### Population & ecology
Exponential and logistic growth; carrying capacity; Lotka–Volterra predator–prey and competition;
age-structured (Leslie matrix) models; metapopulations; trophic levels and energy flow (10% rule);
nutrient cycles; succession; keystone species; biodiversity metrics; stability and resilience.

### Epidemiology
Compartment models (SIR, SEIR, SIRS); basic and effective reproduction number (R₀, Rₑ); contact
networks; vaccination thresholds; stochastic vs deterministic regimes at low prevalence.

### Systems biology
Gene regulatory networks; reaction–diffusion and Turing patterns; oscillators (circadian, cell
cycle); robustness and bistability; agent-based modelling of cells and organisms; multi-scale
coupling.

## 3. When To Use

**Use when:**
- Modelling growth, populations, ecosystems, disease spread, metabolism, or genetics.
- Designing life-simulation, creature, ecology, evolution, or survival systems.
- Choosing between deterministic ODE, stochastic, and agent-based approaches.
- Validating that a biological system produces realistic equilibria rather than runaway or
  extinction.
- Establishing plausible parameter ranges for biological rates.

**Do not use when:**
- The system is biological only in flavour text with no modelled dynamics — declare that
  explicitly.

## 4. Method

1. Choose the scale and the state variables. Biology fails most often from scale mismatch —
   do not model molecules to answer a population question.
2. Decide deterministic vs stochastic. Small populations and low copy numbers require stochastic
   treatment; averages lie there.
3. Write the governing equations with units and per-capita rates clearly distinguished from
   absolute rates.
4. Identify feedback loops and label each as stabilising (negative) or amplifying (positive).
5. Find the equilibria and analyse stability. A model whose only outcomes are extinction or
   explosion is usually mis-parameterised.
6. Bound every parameter with a biologically plausible range and cite the source.
7. Define validation: known equilibria, limiting behaviour, published data, or field observations.

## 5. Expected Output

- **System model**: state variables with units, governing equations, parameter table with
  plausible ranges and sources.
- **Feedback map**: loops identified and signed.
- **Equilibrium analysis**: fixed points, stability, and the conditions producing each.
- **Regime decision**: deterministic / stochastic / agent-based, with justification.
- **Validation cases** and **validity range**.
- **Confidence label** on every biological rate or constant.

## 6. Guardrails

- Never use a deterministic model for small populations without stating the error it introduces.
- Never present an unbounded growth model as realistic — state the limiting resource.
- Never quote a biological rate without its organism, conditions, and units.
- Never imply evolutionary "purpose" or directedness; selection is a filter, not a goal.
- Never extrapolate allometric scaling laws outside their measured mass range.
- Distinguish correlation from mechanism in any biological claim.
- Route load-bearing rates and constants to the Research Agent.

## 7. Related

`skills/chemistry` · `skills/physics` · `skills/simulation` · `skills/game-development`
