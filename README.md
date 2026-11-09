
# CTE-HF-AI

**A Python library for the Computational Theory of Education for Human Flourishing in the AI Era**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/)
[![Version](https://img.shields.io/badge/version-0.2.0-green.svg)](CHANGELOG.md)
[![Tests](https://img.shields.io/badge/tests-42%2B%20passing-brightgreen.svg)](tests/)

---

## Table of Contents

- [What This Library Is](#what-this-library-is)
- [Why It Exists](#why-it-exists)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Theory in One Page](#theory-in-one-page)
- [Library Tour](#library-tour)
  - [Learner State & Invisible Capacities](#learner-state--invisible-capacities)
  - [Domain Competence](#domain-competence)
  - [Ethical Competence](#ethical-competence)
  - [Two-Register Flourishing](#two-register-flourishing)
  - [Educational Success](#educational-success)
  - [Safety Gap](#safety-gap)
  - [ECA Trigger Constraints](#eca-trigger-constraints)
  - [Governance Daemons](#governance-daemons)
  - [SCAM Learner Model](#scam-learner-model)
  - [Hybrid Dynamics](#hybrid-dynamics)
  - [Free-Energy Precision](#free-energy-precision)
  - [Embedding Interfaces](#embedding-interfaces)
  - [COH Hierarchy](#coh-hierarchy)
  - [Multi-Agent Tutoring](#multi-agent-tutoring)
  - [FCP Compliance](#fcp-compliance)
  - [Research Agenda Simulations](#research-agenda-simulations)
- [Theory-to-Code Map](#theory-to-code-map)
- [Design Principles](#design-principles)
- [Repository Structure](#repository-structure)
- [Development](#development)
- [Examples](#examples)
- [Status & Limitations](#status--limitations)
- [Citation](#citation)
- [Contributing](#contributing)
- [License](#license)

---

## What This Library Is

`ctehf-lib` is a research-grade Python implementation of the **Computational Theory of Education for Human Flourishing in the AI Era (CTE-HF-AI)** — a domain-specific instantiation of **Constrained Object Hierarchies (COH)** applied to education.

Every construct in the theory paper is a callable object in this library: the ten invisible capacities, ethical competence as a non-compensatory construct, domain competence as a three-constituent composite, two-register flourishing, the educational safety gap, ECA trigger constraints, governance daemons, SCAM's Bayesian learner model, hybrid continuous-discrete dynamics, and free-energy precision. All nine COH components (C, A, M, N, E, I, T, G, D) are instantiated.

The library is intended for:

- **Researchers** testing the theory's empirical predictions (Section 6 of the paper).
- **Learning engineers** building AI-assisted educational systems that distinguish AI-supported performance from verified independent capability.
- **Institutional researchers** running safety-gap audits across courses, programs, or institutions.
- **Students of the theory** who want to see the FCP Principle, ethical competence, and invisible-capacity vector as executable code rather than formal notation.

## Why It Exists

Generative AI now performs tasks that were long treated as markers of human cognitive distinctiveness — content generation, structured reasoning, ethical deliberation simulation. Educational systems that optimize only for AI-assisted performance may produce credentials without capability, fluency without understanding, compliance without conscience.

The theory formalizes what education must cultivate when AI can simulate many of its visible outputs:

> **Flourishing → Ethical Competence → Dual Preparation**

This is the *Flourishing–Competence–Preparation (FCP) Principle*: flourishing names education's aim, ethical competence names the developmental construct through which the aim is educationally approached, and dual preparation names the design principle that operationalizes the construct. The library implements all three.

## Quick Start

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    ethical_competence, educational_flourishing,
    safety_gap, interpret_safety_gap,
)

# Construct a learner state
state = LearnerState(
    competencies={"algorithmic_literacy": 0.7, "metacognition": 0.6},
    knowledge={"algebra": 0.7},
    invisible={c: 0.7 for c in InvisibleCapacity},
)

# Read the three aggregate constructs
print(f"IC = {state.IC:.3f}")   # normalized invisible-capacity aggregate ∈ [0, 1]
print(f"DC = {state.DC:.3f}")   # three-constituent domain competence
print(f"EC = {ethical_competence(state):.3f}")   # non-compensatory ethical competence

# Two-register flourishing
print(f"HF_educational = {educational_flourishing(state):.3f}")

# Safety gap diagnostic
gap = safety_gap(perf_ai=0.85, perf_indep=0.55)
print(f"Gap = {gap:+.3f}  [{interpret_safety_gap(gap).value}]")
# Gap = +0.300  [large_divergence]
```

## Installation

### From source (recommended for development)

```bash
git clone https://github.com/hongxueharriswang/ctehf-lib.git
cd ctehf-lib
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Verify

```bash
pytest                     # 42+ tests should pass
python examples/basic_usage.py
```

### As a dependency

```bash
pip install git+https://github.com/hongxueharriswang/ctehf-lib.git
```

A PyPI release is planned for v0.3.0.

## Theory in One Page

The CTE-HF-AI formalizes education's contribution to human flourishing. It uses five core constructs and three registers of measurement.

**Core constructs.**

| Construct | Symbol | Range | Compensation | Meaning |
|---|---|---|---|---|
| Invisible-capacity aggregate | `IC` | [0, 1] | Partially compensatory | Mean of ten invisible capacities across three domains |
| Domain competence | `DC` | [0, 1] | Fully compensatory | Weighted mean of disciplinary mastery, professional performance, and transferable competencies |
| Ethical competence | `EC` | [0, 1] | Non-compensatory | Threshold-gated construct over moral agency, practical judgment, relational presence |
| Flourishing (educational register) | `HF_educational` | [0, 1] | — | `f(EC, IC, DC)` — what education is accountable for |
| Flourishing (total register) | `HF` | ℝ | — | `HF_educational + ε` — ε captures health, family, economic, societal contributions outside the system |

**The asymmetry that matters.** The three flourishing determinants are treated differently because their underlying structures differ:

- **EC is non-compensatory**: a capable learner without conscience is *not ethically competent*, and no amount of practical judgment or relational warmth compensates.
- **IC is partially compensatory**: developmental trajectories legitimately vary; a learner may compensate slower wisdom development with stronger purpose, subject to no-regression bounds on critical domains.
- **DC is fully compensatory**: for a given domain outcome, metacognitive reasoning, authentic task performance, and content recall are genuinely substitutable routes to the same capability.

**The ten invisible capacities**, grouped into three domains:

| Domain | Capacities |
|---|---|
| **Moral agency (MA)** | Moral responsibility, ethical commitment, conscience, humility |
| **Practical-existential judgment (PJ)** | Wisdom, meaning-making, purpose, existential courage |
| **Relational presence (RP)** | Love, empathic presence |

**The FCP Principle.**

```
Flourishing ──> Ethical Competence ──> Dual Preparation
```

Three determinations, each constraining the next. Violating any of them fails to be educational in the theory's sense. See `fcp.py`.

## Library Tour

### Learner State & Invisible Capacities

The `LearnerState` object holds a bounded, uncertainty-annotated vector spanning four subspaces: competencies, skills, invisible capacities, and knowledge.

```python
from ctehf_ai import LearnerState, InvisibleCapacity, Domain, DOMAIN_MEMBERSHIP

state = LearnerState(
    competencies={
        "algorithmic_literacy": 0.7,
        "ethical_judgment": 0.6,
        "creative_abduction": 0.5,
        "metacognition": 0.7,
        "emotional_intelligence": 0.6,
        "systems_thinking": 0.5,
    },
    skills={"learning_to_learn": 0.7, "judge": 0.6},
    invisible={
        InvisibleCapacity.MORAL_RESPONSIBILITY: 0.7,
        InvisibleCapacity.CONSCIENCE: 0.7,
        InvisibleCapacity.WISDOM: 0.7,
        InvisibleCapacity.LOVE: 0.7,
        # unspecified capacities default to 0.0
    },
    knowledge={"algebra": 0.7, "geometry": 0.6},
)

# Domain aggregates
print(state.MA)  # moral agency: mean of the four MA capacities
print(state.PJ)  # practical-existential judgment
print(state.RP)  # relational presence
print(state.IC)  # normalized aggregate ∈ [0, 1]
```

Values are clipped to `[0, 1]` on construction. All ten invisible capacities are always present — unset ones default to 0.0.

### Domain Competence

`DC` decomposes into three weighted constituents (Section 3.2.3).

```python
from ctehf_ai import DCConfig, domain_competence, dc_decomposed

# Diagnostic decomposition
d = state.DC_decomposed
# {
#   "DC_disc": 0.65,   # disciplinary mastery (declarative + procedural knowledge)
#   "DC_prof": 0.62,   # professional performance (knowledge + competencies in authentic tasks)
#   "DC_comp": 0.60,   # transferable competencies exercised within the domain
#   "w_disc": 0.333, "w_prof": 0.333, "w_comp": 0.333,
#   "DC": 0.62,
# }

# Custom weighting (must sum to 1)
weighted = DCConfig(w_disc=0.5, w_prof=0.3, w_comp=0.2)
dc = domain_competence(state.competencies, state.knowledge, weighted)
```

**On the competency "ethical_judgment" vs. the construct "EC".** These are distinct. The competency is a deliberative skill; the construct is an integrative determinant with non-compensatory thresholds. A learner may exercise ethical judgment well in a case analysis while scoring low on `EC` because the moral-agency threshold is unmet. `DC_comp` uses the competency; `EC` uses the construct.

### Ethical Competence

The non-compensatory formulation (Section 3.3.2). The default configuration sets each domain weight to 1/3, each threshold to 0.2, and the minimum ethical competence to 0.5. When any domain falls below its threshold, `EC` is penalized below `E_min` — no amount of the other two domains can raise it above.

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    EthicalCompetenceConfig, ethical_competence,
    ethical_competence_decomposed, is_ethical_threshold_satisfied,
)

# A capable learner with conscience deficit
unethical = LearnerState(invisible={
    InvisibleCapacity.MORAL_RESPONSIBILITY: 0.05,
    InvisibleCapacity.ETHICAL_COMMITMENT:   0.05,
    InvisibleCapacity.CONSCIENCE:           0.05,
    InvisibleCapacity.HUMILITY:             0.05,
    InvisibleCapacity.WISDOM:               1.0,
    InvisibleCapacity.MEANING_MAKING:       1.0,
    InvisibleCapacity.PURPOSE:              1.0,
    InvisibleCapacity.EXISTENTIAL_COURAGE:  1.0,
    InvisibleCapacity.LOVE:                 1.0,
    InvisibleCapacity.EMPATHIC_PRESENCE:    1.0,
})

print(ethical_competence(unethical))      # < 0.5 (threshold violated)
print(is_ethical_threshold_satisfied(unethical))   # False

# Full diagnostic
print(ethical_competence_decomposed(unethical))
# {
#   "MA": 0.05, "PJ": 1.0, "RP": 1.0,
#   "MA_threshold": 0.2, "PJ_threshold": 0.2, "RP_threshold": 0.2,
#   "thresholds_met": 0.0,
#   "base_sigma": ...,
#   "EC": ..., "E_min": 0.5,
# }

# Custom thresholds
config = EthicalCompetenceConfig(m_min=0.3, p_min=0.3, r_min=0.3, E_min=0.6, gamma=0.1)
ec = ethical_competence(state, config)
```

`gamma` is the penalty multiplier applied when any threshold is violated; it must satisfy `0 ≤ gamma < E_min`. With the default `gamma=0.0`, a threshold violation forces `EC = 0`.

### Two-Register Flourishing

`HF_educational = f(EC, IC, DC)`, with weights defaulting to 1/3 each. `HF = HF_educational + ε` adds the un-controlled contributions from outside the system.

```python
from ctehf_ai import (
    educational_flourishing, total_flourishing, FlourishingConfig,
)

# Default weights
print(educational_flourishing(state))

# Custom weighting
config = FlourishingConfig(w_EC=0.5, w_IC=0.3, w_DC=0.2)
print(educational_flourishing(state, flourishing_config=config))

# Total register: add the residual ε
print(total_flourishing(state, external_epsilon=0.1))
```

`ε` is *not* a component of the system and does not appear in any COH tuple. It captures the fact that health, family, economic conditions, social relationships, and societal factors also contribute to flourishing but lie beyond education's direct reach. Conflating `HF_educational` with `HF` is a category error.

### Educational Success

The five-condition non-monotonic criterion (Section 3.7). Unlike a strictly monotonic criterion, it permits temporary regressions in individual capacities provided aggregate development is meaningful and no critical domain regresses significantly.

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity, evaluate_success, SuccessCriteria,
)

initial = LearnerState(invisible={c: 0.3 for c in InvisibleCapacity})
final   = LearnerState(invisible={c: 0.7 for c in InvisibleCapacity})

report = evaluate_success(
    initial_state=initial,
    final_state=final,
    perf_ai=0.85,
    perf_indep=0.80,
)
print(report.successful)          # True
print(report.dual_preparation_satisfied)
print(report.ethical_threshold_satisfied)
print(report.aggregate_ic_development)
print(report.no_critical_regression)
print(report.human_accountability_preserved)
```

Tune the thresholds with `SuccessCriteria(delta_min=..., rho=..., theta_collab=..., theta_indep=..., ethical_config=...)`.

### Safety Gap

`Gap = Perf_AI − Perf_indep`, defined at individual, course, program, or institutional levels. Four-way interpretation (Section 6.1):

| Gap | Interpretation | Recommended response |
|---|---|---|
| `|Gap| ≤ ε_small` | balanced | sustain and monitor |
| `Gap > ε_small` | AI dependence | increase AI-free practice |
| `Gap < −ε_small` | measurement anomaly | investigate |
| `|Gap| ≥ ε_large` | large divergence | flag for review |

```python
from ctehf_ai import safety_gap, interpret_safety_gap, recommended_response

for ai, ind in [(0.85, 0.84), (0.90, 0.45), (0.60, 0.80), (0.92, 0.50)]:
    g = safety_gap(ai, ind)
    i = interpret_safety_gap(g)
    print(f"gap={g:+.3f}  {i.value:22s}  {recommended_response(i)}")
```

The safety gap is intended as an **audit device, not an optimization target**. A system that optimizes directly for low gaps will be tempted to weaken AI-assisted performance to match unassisted performance; the recommended responses are pedagogical, not reward signals.

### ECA Trigger Constraints

COH trigger constraints as event–condition–action rules (Section 3.8). Two trigger sets are provided.

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity, Event, CorrectiveAction,
    pedagogical_triggers, safety_gap_triggers,
)

state = LearnerState(invisible={c: 0.5 for c in InvisibleCapacity})

# T_ped: three canonical pedagogical triggers
t_ped = pedagogical_triggers(perf_ai=0.85, perf_indep=0.55, m_min=0.2)
actions = t_ped.fire(Event.ASSESSMENT_COMPLETED, state)
print([a.value for a in actions])
# ['increase_ai_free_practice']

# T_safety: the four safety-gap triggers of Table 2
t_safety = safety_gap_triggers(perf_ai=0.92, perf_indep=0.45)
actions = t_safety.fire(Event.SAFETY_GAP_COMPUTED, state)
print([a.value for a in actions])
# ['flag_for_pedagogical_review']

# Custom ECA rules
from ctehf_ai import ECARule, TriggerSet

custom = TriggerSet([
    ECARule(
        name="low_wisdom",
        event=Event.SCAM_POSTERIOR_UPDATED,
        condition=lambda s: s.invisible[InvisibleCapacity.WISDOM] < 0.3,
        action=CorrectiveAction.TARGETED_DOMAIN_INTERVENTION,
    ),
])
```

### Governance Daemons

Trajectory-monitoring governance (Section 5). Supersedes the pointwise filter of v0.1.0. Three daemons track trajectories across time, detecting drift before any single state violates a threshold.

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    GovernanceDaemons, daemon_dual_prep, daemon_ethics, daemon_transparency,
)

# Build a short trajectory
trajectory = [LearnerState(invisible={c: 0.8 for c in InvisibleCapacity}) for _ in range(5)]

perf_ai   = [0.50, 0.60, 0.70, 0.80, 0.90]
perf_ind  = [0.50, 0.50, 0.50, 0.50, 0.50]
ai_log    = [
    {"has_ai_free_alternative": True, "under_human_review": True, "transparent": True},
]

# Individual daemons
print(daemon_dual_prep(trajectory, perf_ai, perf_ind))
# 'increase-ai-free-practice'   (gap is growing)

print(daemon_ethics(trajectory))
# 'noop'   (EC margin stable)

print(daemon_transparency(ai_log))
# 'noop'   (all AI actions declared)

# Or all three at once
result = GovernanceDaemons().run(
    trajectory=trajectory,
    perf_ai_trajectory=perf_ai,
    perf_indep_trajectory=perf_ind,
    ai_action_log=ai_log,
)
print(result)
# {'d_dual_prep': 'increase-ai-free-practice', 'd_ethics': 'noop', 'd_transparency': 'noop'}
```

**What trajectory monitoring enables that pointwise filtering does not:**

1. **Drift detection** — a trajectory may have every state satisfying thresholds while the *trend* violates them.
2. **Anticipatory correction** — the daemon computes the derivative of the safety gap and can fire before the gap crosses threshold.
3. **Trajectory-level constraints** — "the safety gap must not increase monotonically over a semester" cannot be checked at a single point.

### SCAM Learner Model

Hybrid Bayesian–neural state-space model (Section 4.2). Tracks the learner state's posterior distribution over time.

```python
import numpy as np
from ctehf_ai import LearnerState, InvisibleCapacity, SCAMModel, ethical_competence

true_state = LearnerState(invisible={
    InvisibleCapacity.MORAL_RESPONSIBILITY: 0.7,
    InvisibleCapacity.WISDOM: 0.75,
    InvisibleCapacity.LOVE: 0.75,
    # ...
})

model = SCAMModel(true_state)
n = len(true_state.to_vector())

for t in range(10):
    noisy = np.clip(true_state.to_vector() + np.random.normal(0, 0.15, n), 0, 1)
    model.predict()
    model.update(noisy)

    ic_point, ic_unc = model.ic_estimate()
    print(f"t={t+1:2d}  IC={ic_point:.3f} ± {ic_unc:.3f}  "
          f"EC={ethical_competence(model.posterior_state):.3f}")

# Uncertainty quantification
lower, upper = model.credible_interval(confidence=0.95)
```

The observation function is the pluggable "neural" component: pass `observation_fn=` to map high-dimensional evidence to state-space observations.

### Hybrid Dynamics

Continuous evolution between assessment events, discrete transitions at events, switching via trigger conditions (Section 3.9).

```python
import numpy as np
from ctehf_ai import (
    LearnerState, InvisibleCapacity, PedagogicalAction, ActionType,
    TransitionFunction, HybridDynamics,
    empirical_lipschitz, check_theorem_3_1_assumptions,
)

# Continuous dynamics: ds/dt = f(s, a, θ)
def continuous_f(s_vec, action, params):
    return 0.05 * np.ones_like(s_vec)   # simple linear drift

dynamics = HybridDynamics(
    continuous_f=continuous_f,
    discrete_g=TransitionFunction(),
    trigger_condition=lambda s: s.invisible[InvisibleCapacity.WISDOM] > 0.6,
    dt=0.1,
)

state = LearnerState(invisible={c: 0.5 for c in InvisibleCapacity})
action = PedagogicalAction(action_type=ActionType.SCAFFOLD,
                            target=InvisibleCapacity.WISDOM.value, intensity=1.0)

next_state = dynamics.step(state, action)

# Theorem 3.1 (existence and uniqueness) assumption checks
pts = [np.zeros(5), np.ones(5), 0.5 * np.ones(5)]
L_f = empirical_lipschitz(lambda x: 2 * x, pts)
L_g = empirical_lipschitz(lambda x: 0.5 * x, pts)
status = check_theorem_3_1_assumptions(L_f, L_g, trigger_measurable=True)
print(status)
# {'f_lipschitz_satisfied': True, 'f_lipschitz_constant': 2.0, ...,
#  'theorem_3_1_applies': True}
```

`empirical_lipschitz` is the practical check for the Lipschitz condition: it estimates `sup |f(x) − f(y)| / |x − y|` on a finite point set. For real neural sub-models, the condition is a design obligation (spectral normalization, Lipschitz-constrained layers, or domain restriction).

### Free-Energy Precision

SCAM's inference is a free-energy formulation, with the non-compensatory thresholds as precision-weighted priors (Section 4.2.1, Theorem 4.1). When moral agency falls below its threshold, the effective precision on the ethical dimension becomes large, pushing the posterior into the penalty region.

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    ethical_precision, PrecisionPrior, variational_free_energy,
    ethical_competence_via_precision,
)

# A learner below the MA threshold
s = LearnerState(invisible={
    InvisibleCapacity.MORAL_RESPONSIBILITY: 0.1,
    InvisibleCapacity.CONSCIENCE:           0.1,
    InvisibleCapacity.WISDOM:               0.8,
    InvisibleCapacity.LOVE:                 0.8,
    # ...
})

precisions = ethical_precision(s)
print(precisions)   # {'MA': 100.0, 'PJ': 1.0, 'RP': 1.0}

# EC via precision formulation (equivalent to ethical_competence in the conjugate case)
print(ethical_competence_via_precision(s))

# Variational free energy F(q)
import numpy as np
q = np.full(5, 0.5)
x = np.full(5, 0.6)
print(variational_free_energy(q, x))
```

### Embedding Interfaces

`E_learner`, `E_action`, `E_artefact` (Section 3.2.2). Protocol interfaces with default implementations; substitute trained encoders for production use.

```python
import numpy as np
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    IdentityLearnerEmbedding, IdentityActionEmbedding, MeanArtefactEmbedding,
    similarity_in_H, nearest_neighbours,
    PedagogicalAction, ActionType,
)

e_learner = IdentityLearnerEmbedding()

query = e_learner(LearnerState(invisible={c: 0.5 for c in InvisibleCapacity}))
candidates = {
    "similar": e_learner(LearnerState(invisible={c: 0.52 for c in InvisibleCapacity})),
    "distant": e_learner(LearnerState(invisible={c: 0.90 for c in InvisibleCapacity})),
}

result = nearest_neighbours(query, candidates, delta=0.2)
print(result)
# {'similar': 0.063...}

# Distance in H
print(similarity_in_H(query, candidates["similar"]))
print(similarity_in_H(query, candidates["distant"]))
```

### COH Hierarchy

The Constrained Object Hierarchy with runtime constraint daemons (Section 4.1).

```python
from ctehf_ai import COHObject, ConstraintDaemon, ConstraintHierarchy

h = ConstraintHierarchy()

h.register(COHObject(name="HF_educational", level=0))
h.register(COHObject(name="EC",             level=1, parent="HF_educational"))
h.register(COHObject(name="IC",             level=1, parent="HF_educational"))
h.register(COHObject(name="DC",             level=1, parent="HF_educational"))

h.register(COHObject(
    name="EC_constraint", level=1, parent="HF_educational",
    daemons=[ConstraintDaemon(
        name="ec_minimum",
        check=lambda s: s["ec"] >= 0.5,
        message="EC below E_min",
    )],
))

violations = h.enforce_all({"ec": 0.3, "ic": 0.7, "dc": 0.6})
print(violations)   # ['[ec_minimum] EC below E_min']
```

### Multi-Agent Tutoring

The bounded multi-agent system (Section 4.3).

```python
from ctehf_ai import MultiAgentTutoringSystem

system = MultiAgentTutoringSystem()
print(system.accountability_preserved())   # True — human teacher is accountable

result = system.coordinate({"learner_id": "L001", "session": 3})
print(result["agents"])         # human_teacher, ai_tutor, peer_learner, reflection
print(result["human_accountability_preserved"])
```

### FCP Compliance

Check compliance with the Flourishing–Competence–Preparation Principle (Sections 1.1, 3.4.1).

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity, FCPStatus, check_fcp_compliance,
)

state = LearnerState(invisible={c: 0.8 for c in InvisibleCapacity})
status = check_fcp_compliance(state, perf_ai=0.85, perf_indep=0.80)
print(status)
# FCPStatus.COMPLIANT

# Failed preparation (dual-preparation violated)
bad = check_fcp_compliance(state, perf_ai=0.85, perf_indep=0.30)
print(bad)
# FCPStatus.PREPARATION_VIOLATED
```

### Research Agenda Simulations

Four flagship studies (Section 6.2). These are simulations; the actual empirical work replaces synthetic data with institutional data.

```python
from ctehf_ai.experiments import (
    study1_safety_gap,
    study2_dual_prep,
    study3_scam_validation,
    study4_threshold_effects,
)

print("Study 1 — safety-gap measurement:",  study1_safety_gap(n_learners=200))
print("Study 2 — dual-prep comparison:",     study2_dual_prep(n_learners=100))
print("Study 3 — SCAM validation:",          study3_scam_validation(n_learners=50))
print("Study 4 — threshold effects:",        study4_threshold_effects())
```

## Theory-to-Code Map

Every module cites the paper section it implements.

| Paper § | Construct | Module |
|---|---|---|
| §3.2 | Learner state | `state.py` |
| §3.2.1 | Invisible capacities & IC | `capacities.py`, `state.py` |
| §3.2.2 | Embedding `E` | `embeddings.py` |
| §3.2.3 | Domain competence `DC` | `dc.py`, `state.py` (`DC`, `DC_decomposed`) |
| §3.3 | Ethical competence `EC` | `ethical.py` |
| §3.4.1 | FCP Principle | `fcp.py` |
| §3.4.2 | Two-register flourishing | `flourishing.py` |
| §3.6 | Axioms (identity constraints) | `success.py`, `fcp.py` |
| §3.7 | Non-monotonic success | `success.py` |
| §3.8 | Trigger constraints `T` | `triggers.py` |
| §3.9 | Hybrid dynamics, Theorem 3.1 | `hybrid.py` |
| §4.1 | COH hierarchy | `coh.py` |
| §4.2 | SCAM learner model | `scam.py` |
| §4.2.1 | Free-energy correspondence | `free_energy.py`, `ethical.py` |
| §4.3 | Multi-agent tutoring | `agents.py` |
| §5 | Governance daemons | `daemons.py` |
| §5.1 | Pointwise filter (deprecated) | `governance.py` |
| §6.1 | Safety gap | `safety_gap.py` |
| §6.2 | Research agenda | `experiments.py` |
| §7 | Threshold calibration | `calibration.py` |

See [`docs/theory_mapping.md`](docs/theory_mapping.md) for a detailed version with line-level references.

## Design Principles

1. **Faithful instantiation, not interpretation.** Every module cites the paper section it implements, and every docstring uses the paper's vocabulary. The code is meant to be readable alongside the paper.

2. **The theory's distinctions are load-bearing.** EC is non-compensatory; IC is partially compensatory; DC is fully compensatory. The library preserves all three compensation structures rather than collapsing them into a single score.

3. **Assumptions are stated.** Where a COH theorem is invoked, its conditions are documented in the docstring and, where possible, exposed as runtime checks (`check_theorem_3_1_assumptions`). The theory's §7 limitation — that some assumptions are implementation obligations, not free inheritances — is preserved in the code.

4. **Deprecations are explicit.** The pointwise governance filter of v0.1.0 is retained but emits a `DeprecationWarning`; the trajectory-daemon formulation supersedes it. Migration guidance is in [`docs/v0.2.0_migration.md`](docs/v0.2.0_migration.md).

5. **No silent numerical surprises.** When `DC` changed from a single-number mean to a three-constituent composite in v0.2.0, it was documented as a breaking change in `CHANGELOG.md`. The user must know when a number they depended on has changed meaning.

## Repository Structure

```
ctehf-lib/
├── .github/workflows/ci.yml        # ruff + pytest on py3.10–3.12
├── docs/
│   ├── theory_mapping.md           # Detailed paper-to-code map
│   └── v0.2.0_migration.md         # Breaking changes from v0.1.0
├── examples/
│   ├── basic_usage.py
│   ├── v02_new_features.py         # DC decomposition, triggers, daemons, embeddings, hybrid, free-energy
│   ├── safety_gap_analysis.py
│   ├── scam_estimation.py
│   └── research_agenda.py
├── src/ctehf_ai/
│   ├── __init__.py                 # Public API — 65 exports
│   ├── agents.py                   # §4.3 multi-agent system
│   ├── calibration.py              # §7 threshold calibration
│   ├── capacities.py               # §3.2.1 ten invisible capacities
│   ├── coh.py                      # §4.1 COH hierarchy
│   ├── daemons.py                  # §5 governance daemons
│   ├── dc.py                       # §3.2.3 domain competence
│   ├── embeddings.py               # §3.2.2 E_learner/E_action/E_artefact
│   ├── ethical.py                  # §3.3 ethical competence
│   ├── experiments.py              # §6.2 research agenda
│   ├── fcp.py                      # §1.1, §3.4.1 FCP compliance
│   ├── flourishing.py              # §3.4.2 two-register model
│   ├── free_energy.py              # §4.2.1 precision & free energy
│   ├── governance.py               # §5.1 deprecated pointwise filter
│   ├── hybrid.py                   # §3.9 hybrid dynamics
│   ├── safety_gap.py               # §6.1 safety gap
│   ├── scam.py                     # §4.2 SCAM learner model
│   ├── state.py                    # §3.2 learner state
│   ├── success.py                  # §3.7 non-monotonic success
│   ├── trajectories.py             # §4.1 pedagogical actions
│   └── triggers.py                 # §3.8 ECA trigger sets
├── tests/
│   ├── test_core.py                # capacities, state, COH, trajectories, FCP
│   ├── test_daemons.py
│   ├── test_dc.py
│   ├── test_embeddings.py
│   ├── test_ethical_flourishing.py
│   ├── test_governance_deprecation.py
│   ├── test_hybrid_free_energy.py
│   ├── test_integration.py         # end-to-end v0.2.0 pipeline
│   ├── test_success_safety.py
│   └── test_triggers.py
├── CHANGELOG.md
├── LICENSE
├── README.md
├── deploy.py                       # one-shot venv + install + test
├── pyproject.toml                  # v0.2.0
└── requirements.txt
```

## Development

### Setup

```bash
git clone https://github.com/hongxueharriswang/ctehf-lib.git
cd ctehf-lib
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

### Run tests

```bash
pytest                                     # all tests, verbose
pytest --cov=ctehf_ai --cov-report=html    # with coverage report (htmlcov/index.html)
pytest tests/test_daemons.py -v            # single module
pytest -k "safety" -v                      # filter by name
```

### Lint

```bash
ruff check src/ tests/
ruff check --fix src/ tests/
```

### One-shot deploy

```bash
python deploy.py
```

Creates the venv if needed, installs dev dependencies, runs the test suite, and prints the activation command.

### Continuous integration

The `.github/workflows/ci.yml` workflow runs `ruff` and `pytest` on Python 3.10, 3.11, and 3.12 on every push and pull request to `main`. A failing CI blocks merges.

## Examples

| File | What it demonstrates |
|---|---|
| `examples/basic_usage.py` | Minimal walk-through: state, EC, HF, safety gap |
| `examples/v02_new_features.py` | All v0.2.0 additions: DC decomposition, triggers, daemons, embeddings, hybrid, free-energy |
| `examples/safety_gap_analysis.py` | Compare safety gaps across two curricula |
| `examples/scam_estimation.py` | SCAM tracking over noisy observations |
| `examples/research_agenda.py` | Run the four flagship simulations |

Run any example after installing:

```bash
python examples/basic_usage.py
```

## Status & Limitations

**Version:** 0.2.0 (aligned with the revised paper).

**What is implemented and tested:** All nine COH components; the ten invisible capacities; non-compensatory ethical competence; three-constituent domain competence; two-register flourishing; non-monotonic success; ECA trigger sets; governance daemons; SCAM's Bayesian core; hybrid dynamics with Theorem 3.1 assumption checks; precision priors and variational free energy; embedding protocol interfaces; multi-agent system; FCP compliance; threshold calibration; four research-agenda simulations.

**What is deferred:**

- Trained encoders for `E_learner`, `E_action`, `E_artefact` (the protocols exist; specific architectures are implementation choices).
- Domain-competence weights calibrated to specific disciplines (§7 limitation).
- An empirical implementation of Study 5 (embedding similarity retrieval) and Study 6 (daemon drift detection) — both need real institutional data.
- The Meta-Theorem of Joint Validity (§8.2) as a runtime check — planned for `validity.py` in v0.3.0.

**Known limitations** (mirroring the paper's §7):

- The ten invisible capacities are hard to measure; SCAM's estimates are provisional.
- Thresholds (`m_min`, `p_min`, `r_min`, `E_min`, `θ_collab`, `θ_indep`, `Δ_min`, `ρ_k`) require empirical calibration.
- The free-energy correspondence holds as an equality in the conjugate case and as a bound (with amortization gap) in the neural case.
- The Lipschitz condition for Theorem 3.1 is an architectural obligation on any real SCAM implementation, not an automatic inheritance.
- The `DC` decomposition is a *specification of the target*, not a theory of how the target is reached.

## Citation

If you use this library in research, please cite both the theory paper and (if relevant) the COH foundations:

```bibtex
@article{wang2026ctehf,
  title   = {A Computational Theory of Education for Human Flourishing in the Age of Artificial Intelligence},
  author  = {Wang, Harris},
  year    = {2026},
  note    = {Athabasca University}
}

@article{wang2025coh,
  title   = {Constrained Object Hierarchies as a Unified Theoretical Model for Intelligence and Intelligent Systems},
  author  = {Wang, Harris},
  journal = {Computers},
  volume  = {14},
  number  = {11},
  pages   = {478},
  year    = {2025},
  doi     = {10.3390/computers14110478}
}
```

If you use the library itself (not just the theory), a software citation is:

```bibtex
@software{wang2026ctehflib,
  title   = {CTE-HF-AI: A Python Library for the Computational Theory of Education for Human Flourishing},
  author  = {Wang, Harris},
  version = {0.2.0},
  year    = {2026},
  url     = {https://github.com/hongxueharriswang/ctehf-lib}
}
```

## Contributing

Contributions are welcome. Because the library is a faithful instantiation of a specific theory, contributions are most useful when they either:

- **Fix a bug** in an existing implementation (please include a test).
- **Add a test** that increases coverage of a documented construct.
- **Add a trained encoder** for `E_learner`, `E_action`, or `E_artefact`, provided it satisfies the protocol and is documented as a domain-specific choice.
- **Add an empirical example** using real institutional data (please anonymize).
- **Improve documentation** where the paper-to-code correspondence is unclear.

Contributions that **change the theory's formal content** (e.g., changing `EC` from non-compensatory to compensatory, or removing a threshold) will be declined unless the change is first made to the paper. The library's value depends on its fidelity to the theory.

### Workflow

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-improvement`.
3. Write the change with tests.
4. Run `ruff check src/ tests/` and `pytest`.
5. Open a pull request with a description of the change and its motivation.

### Reporting issues

Use the GitHub issue tracker. When reporting a bug, please include:

- Python version and OS.
- The minimal code that reproduces the issue.
- The expected behavior and the actual behavior.
- The version of `ctehf_ai` (`python -c "import ctehf_ai; print(ctehf_ai.__version__)"`).

## License

MIT — see [LICENSE](LICENSE).

Copyright © 2026 Harris Wang.

## Acknowledgments

The theory draws on a wide literature, including neo-Aristotelian educational philosophy, moral-development research (Kohlberg, Rest, Narvaez), wisdom research (Sternberg, Ardelt, Grossmann), relational-pedagogy philosophy (Buber, Noddings, Palmer), AI-in-education research, and the free-energy principle (Friston). The COH mathematical foundations are developed in Wang's MDPI *Computers* paper and its preprints.org companion articles. The full reference list is in the theory paper.

---

**Questions, corrections, collaborations:** open an issue at <https://github.com/hongxueharriswang/ctehf-lib/issues> or contact the author.
```
