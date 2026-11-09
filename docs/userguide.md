# CTE-HF-AI User Guide

**Version 0.2.0** · Last updated 2026-11-08

This is the comprehensive user guide for `ctehf-lib`, the Python implementation of the Computational Theory of Education for Human Flourishing in the AI Era (CTE-HF-AI). It assumes you have read the README and want to use the library in depth.

> **Saving this file.** Place it at `docs/user_guide.md` in the repository. The README's link table can point here.

---

## Table of Contents

**Part I — Getting Started**
1. [Who this guide is for](#1-who-this-guide-is-for)
2. [Installation and setup](#2-installation-and-setup)
3. [Your first program](#3-your-first-program)
4. [The theory in fifteen minutes](#4-the-theory-in-fifteen-minutes)

**Part II — Core Constructs**
5. [Learner state](#5-learner-state)
6. [Invisible capacities](#6-invisible-capacities)
7. [Domain competence](#7-domain-competence)
8. [Ethical competence](#8-ethical-competence)
9. [Flourishing](#9-flourishing)
10. [Educational success](#10-educational-success)
11. [Safety gap](#11-safety-gap)

**Part III — Dynamic Constructs**
12. [ECA trigger constraints](#12-eca-trigger-constraints)
13. [Governance daemons](#13-governance-daemons)
14. [SCAM learner model](#14-scam-learner-model)
15. [Hybrid dynamics](#15-hybrid-dynamics)
16. [Free-energy precision](#16-free-energy-precision)
17. [Embeddings](#17-embeddings)

**Part IV — System-Level Constructs**
18. [COH hierarchy](#18-coh-hierarchy)
19. [Multi-agent tutoring](#19-multi-agent-tutoring)
20. [FCP compliance](#20-fcp-compliance)
21. [Threshold calibration](#21-threshold-calibration)

**Part V — Workflows**
22. [Running a safety-gap audit](#22-running-a-safety-gap-audit)
23. [Designing a dual-preparation assessment](#23-designing-a-dual-preparation-assessment)
24. [Tracking a learner across a semester](#24-tracking-a-learner-across-a-semester)
25. [Detecting governance drift](#25-detecting-governance-drift)
26. [Validating a SCAM deployment](#26-validating-a-scam-deployment)
27. [Running research simulations](#27-running-research-simulations)

**Part VI — Extending and Integrating**
28. [Writing a custom encoder](#28-writing-a-custom-encoder)
29. [Writing a custom ECA rule](#29-writing-a-custom-eca-rule)
30. [Writing a custom governance daemon](#30-writing-a-custom-governance-daemon)
31. [Integrating with institutional data](#31-integrating-with-institutional-data)
32. [Integrating with an AI tutor](#32-integrating-with-an-ai-tutor)

**Part VII — Reference**
33. [Configuration reference](#33-configuration-reference)
34. [Troubleshooting](#34-troubleshooting)
35. [Frequently asked questions](#35-frequently-asked-questions)
36. [Glossary](#36-glossary)
37. [What's coming in v0.3.0](#37-whats-coming-in-v030)
38. [Getting help](#38-getting-help)

---

# Part I — Getting Started

## 1. Who this guide is for

This guide is for three audiences:

**Researchers and educators** who want to use the library to test the theory's predictions or to run institutional audits. They will find Parts I, II, and V most useful — especially §22 (safety-gap audits), §23 (dual-preparation assessment), and §27 (research simulations). The formal notation in Parts II and III is optional reading; the code examples are self-contained.

**Learning engineers and developers** who want to integrate the library into an AI tutoring system or an assessment platform. They will want Parts I, II, III, IV, and VI — especially §14 (SCAM), §31 (institutional data), and §32 (tutor integration).

**Students of the theory** who want to see the FCP Principle, ethical competence, and invisible-capacity vector as executable code. They will find §4 (theory in fifteen minutes) a useful companion to the paper's §1 and §3.

If you have not yet installed the library, go to §2 first. If you are already installed and want a quick demonstration, go to §3. If you want the conceptual orientation before touching code, go to §4.

## 2. Installation and setup

### 2.1 Prerequisites

- **Python 3.10 or later.** The library uses `X | None` type syntax, which requires 3.10+. It has been tested on 3.10, 3.11, and 3.12.
- **NumPy 1.24+ and SciPy 1.10+.** Both are installed automatically.
- **Git** for cloning; optional if you install from a local tarball.

### 2.2 Install from source (recommended)

```bash
git clone https://github.com/hongxueharriswang/ctehf-lib.git
cd ctehf-lib
python3 -m venv .venv
source .venv/bin/activate         # Linux/macOS
# .venv\Scripts\activate          # Windows PowerShell

pip install --upgrade pip
pip install -e ".[dev]"
```

The `-e` flag installs the package in *editable* mode: changes you make to `src/ctehf_ai/` take effect immediately without reinstalling. The `[dev]` extra installs `pytest`, `pytest-cov`, and `ruff`.

### 2.3 Verify the installation

```bash
pytest
```

You should see 42+ tests pass in under two seconds. If any test fails, see §34.

```bash
python -c "import ctehf_ai; print(ctehf_ai.__version__)"
# 0.2.0

python -c "import ctehf_ai; print(len(ctehf_ai.__all__))"
# 65
```

### 2.4 Opening in VS Code

```bash
code .
```

Install the Python extension if you have not already. Select the interpreter from the `.venv` you just created: *Cmd/Ctrl+Shift+P* → *Python: Select Interpreter* → `.venv/bin/python`.

The `pyproject.toml` configures `pytest` to discover tests automatically, so running the test suite from the VS Code Test Explorer works out of the box.

### 2.5 Install as a dependency (not editable)

If you are building *on* the library rather than modifying it:

```bash
pip install git+https://github.com/hongxueharriswang/ctehf-lib.git
```

A PyPI release is planned for v0.3.0.

### 2.6 Installation troubleshooting

| Symptom | Cause | Fix |
|---|---|---|
| `error: Python 3.9 not supported` | Wrong interpreter | `python3.10 -m venv .venv` (use an explicit version) |
| `ModuleNotFoundError: ctehf_ai` after install | Editable install failed silently | `pip install -e .` from repo root, then `python -c "import ctehf_ai"` |
| `ImportError: cannot import name 'X'` | Stale version cached | `pip uninstall ctehf-ai && pip install -e ".[dev]"` |
| `pytest: command not found` | Dev extras not installed | `pip install -e ".[dev]"` |
| Tests fail with `numpy` import error | Old numpy from system Python | Confirm `which python` points to `.venv/bin/python` |

## 3. Your first program

Save this as `demo.py`:

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    ethical_competence, educational_flourishing,
    safety_gap, interpret_safety_gap,
)

# 1. Describe a learner
state = LearnerState(
    competencies={"algorithmic_literacy": 0.7, "metacognition": 0.6},
    knowledge={"algebra": 0.7},
    invisible={
        InvisibleCapacity.MORAL_RESPONSIBILITY: 0.7,
        InvisibleCapacity.CONSCIENCE:           0.7,
        InvisibleCapacity.WISDOM:               0.7,
        InvisibleCapacity.PURPOSE:              0.6,
        InvisibleCapacity.LOVE:                 0.7,
        InvisibleCapacity.EMPATHIC_PRESENCE:    0.6,
    },
)

# 2. Read the three aggregate determinants
print(f"IC (invisible capacities)  = {state.IC:.3f}")
print(f"DC (domain competence)     = {state.DC:.3f}")
print(f"EC (ethical competence)    = {ethical_competence(state):.3f}")

# 3. Read education's contribution to flourishing
print(f"HF_educational             = {educational_flourishing(state):.3f}")

# 4. Compute a safety gap for this learner
gap = safety_gap(perf_ai=0.85, perf_indep=0.55)
print(f"Safety gap                 = {gap:+.3f}")
print(f"Interpretation             = {interpret_safety_gap(gap).value}")
```

Run it:

```bash
python demo.py
```

Expected output (approximately):

```
IC (invisible capacities)  = 0.660
DC (domain competence)     = 0.700
EC (ethical competence)    = 0.674
HF_educational             = 0.678
Safety gap                 = +0.300
Interpretation             = large_divergence
```

### 3.1 What each block does

**Block 1** constructs a `LearnerState`. The four optional dictionaries describe different facets of the learner: professional competencies, domain knowledge, invisible capacities, and (omitted here) core skills. Invisible capacities not listed default to `0.0`, so specifying only the six you care about is valid — the other four are present but empty.

**Block 2** reads the three determinants of flourishing. `IC` is the mean of the ten invisible capacities. `DC` is a weighted composite of `DC_disc`, `DC_prof`, and `DC_comp`. `EC` is a nonlinear construct that penalizes any domain falling below its threshold.

**Block 3** computes `HF_educational = f(EC, IC, DC)` — education's contribution to flourishing.

**Block 4** computes a safety gap between AI-assisted and independent performance, and reads its interpretation.

### 3.2 Where to go next

- If you want to understand what these numbers *mean* conceptually, go to §4.
- If you want to compute each construct in more depth, go to §5–§11.
- If you want the full audit workflow, go to §22.

## 4. The theory in fifteen minutes

This section is a plain-language orientation to the theory. You do not need to read the paper to use the library, though the paper's §3 is the authoritative reference.

### 4.1 The problem the theory addresses

Generative AI now performs tasks that were long taken as proxies for human capability — writing, reasoning, problem-solving, even simulating ethical deliberation. An educational system that measures only AI-assisted performance can no longer distinguish two very different learners:

- A learner who can reason through a problem alone and uses AI to extend that reasoning.
- A learner who cannot reason through the problem but can prompt AI to produce an answer.

The theory's central question is: **what must education cultivate when AI can simulate many of its visible outputs?** It answers by distinguishing what is *measurable* from what is *developmentally essential*, and by formalizing the latter.

### 4.2 The three determinants of flourishing

The theory holds that education contributes to flourishing through three determinants:

**Ethical competence (`EC`).** The integrative construct spanning moral agency, practical-existential judgment, and relational presence. The theory's strongest claim: `EC` is **non-compensatory**. A highly capable learner without conscience is not ethically competent, and no amount of practical judgment or relational warmth compensates. This is why the code enforces thresholds: if *any* of the three domains falls below its threshold, `EC` is suppressed below the minimum, regardless of the other two.

**Invisible-capacity aggregate (`IC`).** The mean of ten capacities organized into three domains: moral agency (responsibility, ethical commitment, conscience, humility), practical-existential judgment (wisdom, meaning-making, purpose, existential courage), and relational presence (love, empathic presence). `IC` is **partially compensatory**: a learner may compensate slower wisdom development with stronger purpose, subject to no-regression bounds on any critical domain. It is the *profile* of development that matters, not any single capacity.

**Domain competence (`DC`).** The learner's demonstrated capability in a disciplinary or professional domain, decomposed into disciplinary mastery, professional performance, and transferable competencies. `DC` is **fully compensatory**: for a given domain outcome, metacognitive reasoning, authentic task performance, and content recall are genuinely substitutable routes to the same capability.

The three compensation structures differ because their underlying structures differ. This is one of the theory's core claims.

### 4.3 Two registers of flourishing

Education's contribution to flourishing is one thing; flourishing as such is another:

```
HF_educational = f(EC, IC, DC)        # what education is accountable for
HF             = HF_educational + ε    # total flourishing, including ε
```

The residual `ε` captures health, family, economic conditions, social relationships, and societal factors. It is **outside the system** — education does not control it. Confusing `HF_educational` with `HF` is a category error, and the library preserves this distinction.

### 4.4 The FCP Principle

The theory's organizing logic:

```
Flourishing  ──>  Ethical Competence  ──>  Dual Preparation
```

Three determinations, each constraining the next:

1. **Flourishing determines the aim.** Education is for the formation of persons who can live well.
2. **Ethical competence determines the construct.** It is the minimal integrating construct that makes the aim jointly actionable in educational design and assessment.
3. **Dual preparation determines the design principle.** Learners must be prepared both for AI-assisted co-work and for verified independent capability — because a competence demonstrated only with AI assistance has not been shown to be a competence at all.

Violating any determination fails to be educational in the theory's sense. `fcp.py` checks this.

### 4.5 The safety gap

`Gap = Perf_AI − Perf_indep` at the individual, course, program, or institutional level. Four interpretations:

| Gap | Interpretation | Response |
|---|---|---|
| `|Gap| ≤ ε_small` | balanced | sustain and monitor |
| `Gap > ε_small` | AI dependence | increase AI-free practice |
| `Gap < −ε_small` | measurement anomaly | investigate |
| `|Gap| ≥ ε_large` | large divergence | flag for review |

The safety gap is an **audit device, not an optimization target**. A system that optimizes directly for low gaps will be tempted to weaken AI-assisted performance to match unassisted performance; the recommended responses are pedagogical.

### 4.6 What is beyond the theory

The theory formalizes education's contribution to flourishing. It does not theorize:

- How disciplinary knowledge becomes procedural. (§3.2.3 explicitly defers this.)
- How transfer is achieved. (Deferred.)
- How professional performance is scaffolded. (Deferred.)

These are legitimate subjects of educational research that this theory does not attempt to model. The library is correspondingly silent on them; `DC` is specified at the resolution needed to make `f(EC, IC, DC)` well-defined, not as a full theory of disciplinary learning.

---

# Part II — Core Constructs

## 5. Learner state

The `LearnerState` object holds a bounded, uncertainty-annotated vector spanning four subspaces.

### 5.1 Construction

```python
from ctehf_ai import LearnerState, InvisibleCapacity, Domain

state = LearnerState(
    competencies={
        "algorithmic_literacy": 0.7,
        "ethical_judgment": 0.6,
        "creative_abduction": 0.5,
        "metacognition": 0.7,
        "emotional_intelligence": 0.6,
        "systems_thinking": 0.5,
    },
    skills={
        "learning_to_learn": 0.7,
        "judge": 0.6,
        "create": 0.5,
        "relate": 0.6,
        "be": 0.5,
    },
    invisible={
        InvisibleCapacity.MORAL_RESPONSIBILITY: 0.7,
        InvisibleCapacity.ETHICAL_COMMITMENT:   0.65,
        InvisibleCapacity.CONSCIENCE:           0.7,
        InvisibleCapacity.HUMILITY:             0.6,
        InvisibleCapacity.WISDOM:               0.7,
        InvisibleCapacity.MEANING_MAKING:       0.6,
        InvisibleCapacity.PURPOSE:              0.7,
        InvisibleCapacity.EXISTENTIAL_COURAGE:  0.5,
        InvisibleCapacity.LOVE:                 0.8,
        InvisibleCapacity.EMPATHIC_PRESENCE:    0.7,
    },
    knowledge={"algebra": 0.7, "geometry": 0.6, "statistics": 0.5},
)
```

All four dictionaries are optional. Unspecified invisible capacities default to `0.0`; unspecified competencies, skills, and knowledge are simply absent from the state (they do not appear in `to_vector()` unless at least one entry exists in the category).

### 5.2 Value clipping

All values are clipped to `[0, 1]` on construction. Out-of-range values are **silently clipped**, not rejected:

```python
s = LearnerState(invisible={
    InvisibleCapacity.WISDOM: 1.5,   # → 1.0
    InvisibleCapacity.LOVE: -0.3,   # → 0.0
})
```

If you need strict validation, check before constructing.

### 5.3 Properties

| Property | Type | Meaning |
|---|---|---|
| `state.MA` | `float` | Moral agency aggregate (mean of four MA capacities) |
| `state.PJ` | `float` | Practical-existential judgment aggregate |
| `state.RP` | `float` | Relational presence aggregate |
| `state.IC` | `float` | Normalized invisible-capacity aggregate, mean of all ten |
| `state.DC` | `float` | Domain competence, three-constituent composite |
| `state.DC_decomposed` | `dict` | Per-constituent breakdown |

All properties are deterministic and pure; they do not modify the state.

```python
print(f"MA = {state.MA:.3f}")   # moral agency
print(f"PJ = {state.PJ:.3f}")   # practical judgment
print(f"RP = {state.RP:.3f}")   # relational presence
print(f"IC = {state.IC:.3f}")
print(f"DC = {state.DC:.3f}")

print(state.DC_decomposed)
# {'DC_disc': 0.60, 'DC_prof': ..., 'DC_comp': ..., 'w_disc': 0.333, ..., 'DC': 0.62}
```

### 5.4 Domain aggregates

```python
from ctehf_ai import Domain

aggregates = state.domain_aggregates()
print(aggregates[Domain.MORAL_AGENCY])       # same as state.MA
print(aggregates[Domain.PRACTICAL_EXISTENTIAL])
print(aggregates[Domain.RELATIONAL_PRESENCE])
```

### 5.5 Uncertainty

The state carries an uncertainty estimate per variable. In v0.2.0, uncertainty is populated by SCAM's posterior (see §14), not by manual construction. If you construct a state manually, all uncertainties default to `0.0` — meaning "no uncertainty recorded," which is appropriate for a state observed without measurement error or assumed as ground truth.

### 5.6 Copy semantics

```python
copy = state.copy()
copy.competencies["algorithmic_literacy"] = 0.9
print(state.competencies["algorithmic_literacy"])   # still 0.7 — copy is deep
```

### 5.7 Vector serialization

```python
v = state.to_vector()
print(v.shape)          # (n,)
print(state.all_keys()) # ordered list of keys corresponding to positions

# Round-trip through SCAM (which uses vector representation internally)
from ctehf_ai import SCAMModel
model = SCAMModel(state)
print(model.posterior_state.IC)   # approximately state.IC
```

`all_keys()` returns variables in this order: competencies, skills, invisible capacities, knowledge. Two states constructed with the same key sets will have aligned vectors.

### 5.8 Full reference: the six competencies and five skills

The six human-irreplaceable competencies (`COMPETENCIES`) are:

1. `algorithmic_literacy` — capacity to understand, use, and critically evaluate algorithms
2. `ethical_judgment` — deliberative skill of reasoning about moral questions (note: *distinct* from `EC`, see §7.4)
3. `creative_abduction` — capacity to generate and select novel hypotheses
4. `metacognition` — knowledge and regulation of one's own cognition
5. `emotional_intelligence` — capacity to perceive, understand, and manage emotions
6. `systems_thinking` — capacity to reason about complex interdependent systems

The five core skills (`SKILLS`) are:

1. `learning_to_learn`
2. `judge`
3. `create`
4. `relate`
5. `be`

The library does not enforce that you populate all six or all five; partial states are valid.

## 6. Invisible capacities

The ten invisible capacities are the theory's core developmental construct. They are organized into three domains.

### 6.1 The ten capacities and their domains

| Domain | Capacity | Symbol | Enum name |
|---|---|---|---|
| **Moral agency** | Moral responsibility | `v_MR` | `MORAL_RESPONSIBILITY` |
| | Ethical commitment | `v_ECom` | `ETHICAL_COMMITMENT` |
| | Conscience | `v_Con` | `CONSCIENCE` |
| | Humility | `v_Hum` | `HUMILITY` |
| **Practical-existential judgment** | Wisdom | `v_Wis` | `WISDOM` |
| | Meaning-making | `v_MM` | `MEANING_MAKING` |
| | Purpose | `v_Pur` | `PURPOSE` |
| | Existential courage | `v_ECou` | `EXISTENTIAL_COURAGE` |
| **Relational presence** | Love | `v_Love` | `LOVE` |
| | Empathic presence | `v_EPres` | `EMPATHIC_PRESENCE` |

### 6.2 Domain membership

```python
from ctehf_ai import DOMAIN_MEMBERSHIP, Domain

for domain, members in DOMAIN_MEMBERSHIP.items():
    print(f"{domain.value}: {[m.name for m in members]}")

# MA: ['MORAL_RESPONSIBILITY', 'ETHICAL_COMMITMENT', 'CONSCIENCE', 'HUMILITY']
# PJ: ['WISDOM', 'MEANING_MAKING', 'PURPOSE', 'EXISTENTIAL_COURAGE']
# RP: ['LOVE', 'EMPATHIC_PRESENCE']
```

### 6.3 Aggregation

```python
from ctehf_ai import aggregate_domain, aggregate_all_domains, normalized_ic, InvisibleCapacity

capacities = {c: 0.7 for c in InvisibleCapacity}

print(aggregate_domain(capacities, Domain.MORAL_AGENCY))         # 0.7
print(aggregate_all_domains(capacities))                          # {Domain.MA: 0.7, ...}
print(normalized_ic(capacities))                                  # 0.7

# A more heterogeneous case
capacities = {
    InvisibleCapacity.MORAL_RESPONSIBILITY: 0.3,
    InvisibleCapacity.ETHICAL_COMMITMENT:   0.4,
    InvisibleCapacity.CONSCIENCE:           0.2,
    InvisibleCapacity.HUMILITY:             0.5,
    InvisibleCapacity.WISDOM:               0.9,
    InvisibleCapacity.MEANING_MAKING:       0.8,
    InvisibleCapacity.PURPOSE:              0.9,
    InvisibleCapacity.EXISTENTIAL_COURAGE:  0.7,
    InvisibleCapacity.LOVE:                 0.8,
    InvisibleCapacity.EMPATHIC_PRESENCE:    0.9,
}

print(aggregate_all_domains(capacities))
# {MA: 0.35, PJ: 0.825, RP: 0.85}
print(normalized_ic(capacities))    # 0.625 — the mean across all ten
```

### 6.4 Why normalization matters

`IC ∈ [0, 1]`, comparable to `EC` and `DC`. This makes `HF_educational = f(EC, IC, DC)` dimensionally homogeneous: all three arguments live in the same range, so `f` can be a weighted mean without re-scaling.

### 6.5 Why partially compensatory

`IC` is the mean of ten capacities, not a non-compensatory constraint. A learner may compensate slower wisdom development with stronger purpose, and still be developing well overall. Compensation is *bounded* by the success criterion's no-regression condition (§10), which protects critical domains: no domain may regress by more than `ρ_k`.

If you need non-compensatory treatment of invisible capacities (e.g., for a specific research question), use `EC`'s threshold structure or construct a custom aggregation.

## 7. Domain competence

`DC` is the third determinant of flourishing. In v0.1.0 it was a single-number mean of competencies and knowledge; in v0.2.0 it is a three-constituent composite (§3.2.3 of the paper).

### 7.1 The three constituents

**`DC_disc`** — disciplinary mastery: declarative and procedural knowledge in the domain. In the current implementation, the mean of the `knowledge` dictionary.

**`DC_prof`** — professional performance: enacted competence in authentic tasks. In the current implementation, the joint mean of knowledge and competencies (a proxy for "the learner who can perform"). Real deployments should substitute a performance-task rubric score here.

**`DC_comp`** — transferable competencies exercised within the domain: the mean of the six `COMPETENCIES` entries present in the state.

### 7.2 The composite and its weights

```python
from ctehf_ai import DCConfig, domain_competence, dc_decomposed

# Default: equal weights
dc = domain_competence(state.competencies, state.knowledge)

# Custom weighting (must sum to 1)
config = DCConfig(w_disc=0.5, w_prof=0.3, w_comp=0.2)
dc = domain_competence(state.competencies, state.knowledge, config)

# Diagnostic decomposition
d = dc_decomposed(state.competencies, state.knowledge, config)
print(d)
# {
#   'DC_disc': 0.60,
#   'DC_prof': ...,
#   'DC_comp': ...,
#   'w_disc': 0.5, 'w_prof': 0.3, 'w_comp': 0.2,
#   'DC': 0.58,
# }
```

`DCConfig` validates that the weights are non-negative and sum to 1.

### 7.3 Why fully compensatory

The theory treats `DC` as fully compensatory because, *for a given domain outcome*, different routes are genuinely substitutable. A learner who reasons metacognitively rather than recalling content, or who performs well on an authentic task rather than a knowledge test, has demonstrated the same domain capability by different routes.

If your institutional context has a reason to treat one constituent as non-substitutable (e.g., professional performance in a licensed profession), you can override the aggregate:

```python
def licensed_dc(state, dc_config=None):
    d = dc_decomposed(state.competencies, state.knowledge, dc_config)
    # In licensed professions, professional performance must meet a floor
    if d["DC_prof"] < 0.6:
        return min(d["DC"], 0.5)
    return d["DC"]
```

The library does not enforce this; the theory treats `DC` as fully compensatory. Departures are legitimate but should be documented as such.

### 7.4 The competency `ethical_judgment` vs. the construct `EC`

This is the most common source of confusion in the library. They are different things:

| Aspect | `ethical_judgment` (competency) | `EC` (construct) |
|---|---|---|
| Where | In `state.competencies["ethical_judgment"]` | Computed by `ethical_competence(state)` |
| What | Deliberative skill of reasoning about moral questions | Integrative construct spanning MA, PJ, RP |
| Measurement | Standard competency assessment | Threshold-gated nonlinear aggregation |
| Role in flourishing | Contributes to `DC_comp` | Is the non-compensatory determinant of `HF_educational` |
| Can substitute for other things? | Yes (within `DC_comp`) | No (constitutive thresholds) |

A learner may exercise ethical judgment competently in a case analysis while scoring low on `EC` because the moral-agency threshold is unmet. Conversely, a learner with strong moral agency may deliberate poorly in a novel case.

```python
from ctehf_ai import LearnerState, InvisibleCapacity, ethical_competence

# A skilled deliberator with low moral agency
deliberator = LearnerState(
    competencies={"ethical_judgment": 0.9},
    invisible={c: 0.05 for c in InvisibleCapacity},
)

print(deliberator.DC)                  # ~0.15 (nonzero — competency contributes to DC_comp)
print(ethical_competence(deliberator)) # < 0.5 (fails threshold — MA is 0.05)
```

Conflating these would allow deliberative skill to substitute for moral agency, which is exactly the compensation the non-compensatory formulation prevents.

## 8. Ethical competence

`EC` is the theory's most distinctive construct. It is **non-compensatory**: if any of its three domains falls below its threshold, `EC` is suppressed below the minimum, and no amount of the other two domains can compensate.

### 8.1 The threshold-gated formulation

```
           ⎧ σ(w_MA · MA + w_PJ · PJ + w_RP · RP)     if all thresholds met
EC(s)  =   ⎨
           ⎩ γ · σ(...)                                otherwise
```

where:

- `MA`, `PJ`, `RP` are the domain aggregates (§5.3)
- `w_MA`, `w_PJ`, `w_RP` are non-negative weights summing to 1 (default 1/3 each)
- `σ` is a bounded monotone activation (sigmoid)
- `m_min`, `p_min`, `r_min` are thresholds (default 0.2 each)
- `E_min` is the minimum for ethical competence (default 0.5)
- `γ ∈ [0, 1)` is the penalty multiplier (default 0.0)

With the default `γ = 0.0`, any threshold violation forces `EC = 0`. With `γ > 0`, the violation reduces `EC` proportionally but the calibration `0 ≤ γ < E_min` ensures the result is still below `E_min`.

### 8.2 Basic use

```python
from ctehf_ai import ethical_competence

ec = ethical_competence(state)
print(f"{ec:.3f}")
```

### 8.3 Configuration

```python
from ctehf_ai import EthicalCompetenceConfig

config = EthicalCompetenceConfig(
    w_MA=0.4, w_PJ=0.3, w_RP=0.3,   # must sum to 1
    m_min=0.3, p_min=0.25, r_min=0.25,
    E_min=0.6,
    gamma=0.1,                       # 0 <= gamma < E_min
)

ec = ethical_competence(state, config)
```

Validation is strict: weights must sum to 1, weights must be non-negative, and `gamma` must be in `[0, E_min)`.

### 8.4 The threshold semantics

The threshold is what makes `EC` non-compensatory. Consider a learner with `MA = 0.05` but `PJ = RP = 1.0`. With `m_min = 0.2`, the MA threshold is violated, and:

```python
from ctehf_ai import LearnerState, InvisibleCapacity, ethical_competence

skilled_but_unethical = LearnerState(invisible={
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

print(ethical_competence(skilled_but_unethical))
# 0.0  — no amount of PJ or RP compensates for MA below threshold
```

This is the theory's central claim about ethical competence, made operational.

### 8.5 Diagnostic decomposition

```python
from ctehf_ai import ethical_competence_decomposed

d = ethical_competence_decomposed(state)
# {
#   'MA': 0.7, 'PJ': 0.6, 'RP': 0.75,
#   'MA_threshold': 0.2, 'PJ_threshold': 0.2, 'RP_threshold': 0.2,
#   'thresholds_met': 1.0,
#   'base_sigma': ...,
#   'EC': ...,
#   'E_min': 0.5,
# }
```

### 8.6 Threshold satisfaction check

```python
from ctehf_ai import is_ethical_threshold_satisfied

if not is_ethical_threshold_satisfied(state):
    print("Learner has failed the ethical competence minimum")
```

### 8.7 The precision variant

The library also exposes `ethical_competence_via_precision`, which implements the same logic through precision-weighted priors (see §16). In the conjugate case, it produces the same result as `ethical_competence`; under amortization (neural sub-model), it may differ. For most purposes, use `ethical_competence`.

```python
from ctehf_ai import ethical_competence_via_precision

ec1 = ethical_competence(state)
ec2 = ethical_competence_via_precision(state)
print(abs(ec1 - ec2))    # small in the conjugate case
```

### 8.8 Choosing thresholds

The default thresholds (`0.2` for each domain, `0.5` for `E_min`) are placeholders. Real deployments must calibrate them:

- **`m_min`, `p_min`, `r_min`** — what level of moral agency / practical judgment / relational presence is *minimally required* for the learner to be considered ethical? This is a normative question specific to your educational context.
- **`E_min`** — what level of the integrated construct is acceptable for the learner to proceed? In some contexts (e.g., professional licensure), `E_min` should be high; in others (e.g., early undergraduate), lower.

§21 covers calibration. §33 lists every threshold with defaults.

## 9. Flourishing

The two-register model: `HF_educational` (what education is accountable for) and `HF` (total flourishing including `ε`).

### 9.1 Educational register

```python
from ctehf_ai import educational_flourishing, FlourishingConfig

# Default: equal weights
hf = educational_flourishing(state)
print(f"{hf:.3f}")

# Custom weights (must sum to 1)
config = FlourishingConfig(w_EC=0.5, w_IC=0.3, w_DC=0.2)
hf = educational_flourishing(state, flourishing_config=config)
```

### 9.2 Total register

```python
from ctehf_ai import total_flourishing

hf_total = total_flourishing(state, external_epsilon=0.1)
print(f"{hf_total:.3f}")
```

The `ε` captures contributions from outside the system. Typical values:

| `ε` | Interpretation |
|---|---|
| `0.0` | Education's contribution only |
| `0.1` | Modest external contributions (stable family, adequate resources) |
| `0.2` | Substantial external contributions |
| `−0.1` | Adverse external conditions (instability, scarcity) |

`ε` is not a component of the system. It does not appear in the COH 9-tuple. Conflating `HF_educational` with `HF` would treat education as the sole determinant of flourishing, which the theory explicitly disclaims.

### 9.3 Why two registers

Many flourishing frameworks treat flourishing as either wholly measurable (and therefore a single score) or wholly unmeasurable (and therefore purely qualitative). The two-register model takes a middle position:

- **`HF_educational`** is measurable and auditable. Education is accountable for it.
- **`HF`** is not fully measurable. Education contributes to it but does not determine it.

The library preserves this distinction. `educational_flourishing` is an audit device; `total_flourishing` is a conceptual acknowledgment, not a score.

## 10. Educational success

The five-condition non-monotonic criterion.

### 10.1 Why non-monotonic

Empirical work on wisdom development (Ardelt) shows curvilinear, dimension-specific trajectories with temporary plateaus and declines. A criterion requiring `v_i^(T) > v_i^(0)` for every capacity would classify such trajectories as failures. The theory instead permits temporary regressions, provided aggregate development is meaningful and no critical domain regresses significantly.

### 10.2 The five conditions

An educational process is successful iff:

1. **Dual preparation satisfied.** `Perf_AI ≥ θ_collab` and `Perf_indep ≥ θ_indep`.
2. **Ethical threshold satisfied.** `EC(S_T) ≥ E_min`, with thresholds met.
3. **Aggregate IC development.** `ΔIC ≥ Δ_min`.
4. **No critical regression.** Every critical domain: `min(v_j^(T) − v_j^(0)) ≥ −ρ_k`.
5. **Human accountability preserved.** No pedagogical action delegates moral or assessment authority to an AI system.

### 10.3 Basic use

```python
from ctehf_ai import LearnerState, InvisibleCapacity, evaluate_success

initial = LearnerState(invisible={c: 0.3 for c in InvisibleCapacity})
final   = LearnerState(invisible={c: 0.7 for c in InvisibleCapacity})

report = evaluate_success(initial, final, perf_ai=0.85, perf_indep=0.80)

print(report.successful)              # True
print(report.dual_preparation_satisfied)
print(report.ethical_threshold_satisfied)
print(report.aggregate_ic_development)  # 0.4
print(report.aggregate_ic_satisfied)    # True (0.4 ≥ 0.05 default)
print(report.no_critical_regression)
print(report.human_accountability_preserved)
```

### 10.4 Custom criteria

```python
from ctehf_ai import SuccessCriteria, Domain, EthicalCompetenceConfig

criteria = SuccessCriteria(
    delta_min=0.10,                     # require stronger aggregate development
    rho={                               # tighter no-regression tolerances
        Domain.MORAL_AGENCY: 0.03,
        Domain.PRACTICAL_EXISTENTIAL: 0.05,
        Domain.RELATIONAL_PRESENCE: 0.03,
    },
    theta_collab=0.6,
    theta_indep=0.6,
    ethical_config=EthicalCompetenceConfig(m_min=0.3, p_min=0.3, r_min=0.3),
)

report = evaluate_success(initial, final, 0.85, 0.80, criteria=criteria)
```

### 10.5 Reading the report

The `SuccessReport` dataclass exposes each condition individually. When a trajectory fails, you can diagnose which condition failed:

```python
if not report.successful:
    if not report.dual_preparation_satisfied:
        print("Dual preparation failed: AI or independent performance below threshold.")
    if not report.ethical_threshold_satisfied:
        print(f"Ethical competence below E_min: {report.details['EC']:.3f} < {report.details['E_min']}")
    if not report.aggregate_ic_satisfied:
        print(f"Aggregate IC development insufficient: {report.aggregate_ic_development:.3f} < {report.details['delta_min']}")
    if not report.no_critical_regression:
        print("Critical domain regression detected:")
        for domain, regression in report.critical_domain_regressions.items():
            if regression < -criteria.rho[Domain(domain)]:
                print(f"  {domain}: {regression:.3f}")
    if not report.human_accountability_preserved:
        print("Human accountability was not preserved.")
```

## 11. Safety gap

`Gap = Perf_AI − Perf_indep`, with four-way interpretation.

### 11.1 Definition and use

```python
from ctehf_ai import safety_gap, interpret_safety_gap, recommended_response

gap = safety_gap(perf_ai=0.85, perf_indep=0.55)
interpretation = interpret_safety_gap(gap)
print(f"Gap = {gap:+.3f}  [{interpretation.value}]")
print(recommended_response(interpretation))
```

### 11.2 The four interpretations

| Condition | Enum | Meaning |
|---|---|---|
| `|Gap| ≤ ε_small` | `BALANCED` | Prepared for both independent and collaborative work |
| `Gap > ε_small` | `AI_DEPENDENCE` | Performance depends on AI assistance |
| `Gap < −ε_small` | `MEASUREMENT_ANOMALY` | Unassisted performance exceeds assisted; likely anomaly |
| `|Gap| ≥ ε_large` | `LARGE_DIVERGENCE` | Substantial separation in either direction |

Defaults: `ε_small = 0.05`, `ε_large = 0.25`.

### 11.3 Custom thresholds

```python
interpretation = interpret_safety_gap(gap, small_threshold=0.10, large_threshold=0.30)
```

### 11.4 The audit-not-target principle

A system that optimizes directly for low gaps will be tempted to weaken AI-assisted performance to match unassisted performance. The recommended responses are pedagogical — increase AI-free practice, redesign assessment, flag for review — not reward signals. Institutional users should treat the safety gap as an **audit device**.

---

# Part III — Dynamic Constructs

## 12. ECA trigger constraints

Event–condition–action rules, per COH's trigger-constraint semantics.

### 12.1 The three canonical pedagogical triggers

```python
from ctehf_ai import pedagogical_triggers, Event

t_ped = pedagogical_triggers(perf_ai=0.85, perf_indep=0.55, m_min=0.2)

# Fire on an assessment event
actions = t_ped.fire(Event.ASSESSMENT_COMPLETED, state)
print([a.value for a in actions])
```

### 12.2 The safety-gap triggers

```python
from ctehf_ai import safety_gap_triggers

t_safety = safety_gap_triggers(perf_ai=0.90, perf_indep=0.40)
actions = t_safety.fire(Event.SAFETY_GAP_COMPUTED, state)
# [CorrectiveAction.FLAG_FOR_PEDAGOGICAL_REVIEW]
```

### 12.3 Events and actions

**Events** (`Event` enum): `ASSESSMENT_COMPLETED`, `SCAM_POSTERIOR_UPDATED`, `LONGITUDINAL_COMPARISON`, `SAFETY_GAP_COMPUTED`.

**Actions** (`CorrectiveAction` enum): `NOOP`, `INCREASE_AI_FREE_PRACTICE`, `FLAG_MORAL_FORMATION`, `TARGETED_DOMAIN_INTERVENTION`, `SUSTAIN_AND_MONITOR`, `INVESTIGATE_ANOMALY`, `FLAG_FOR_PEDAGOGICAL_REVIEW`.

### 12.4 The no-op default

`TriggerSet.fire()` returns `[NOOP]` when no rule fires. This makes the return type uniform: you always get a non-empty list.

```python
t = safety_gap_triggers(0.75, 0.73)   # balanced
actions = t.fire(Event.SAFETY_GAP_COMPUTED, state)
# [CorrectiveAction.SUSTAIN_AND_MONITOR] — not [NOOP], because balanced rule fires
```

To distinguish "a rule fired with action X" from "no rule fired," check for `[NOOP]`:

```python
result = t.fire(event, state)
if result == [CorrectiveAction.NOOP]:
    print("No trigger fired")
```

### 12.5 Inspecting the rules

```python
for rule in t_ped.rules:
    print(f"{rule.name}: {rule.event.value} → {rule.action.value}")
```

## 13. Governance daemons

Trajectory-monitoring governance, per §5 of the paper. Supersedes the pointwise filter (§5.1).

### 13.1 What a daemon is

A governance daemon is a function `d: S^T → A_act ∪ {noop}` — it receives a state trajectory and returns a corrective action (or `noop`). This is different from a pointwise filter, which checks each state in isolation.

### 13.2 The three daemons

```python
from ctehf_ai import (
    daemon_dual_prep, daemon_ethics, daemon_transparency,
    GovernanceDaemons,
)

trajectory = [LearnerState(invisible={c: 0.8 for c in InvisibleCapacity}) for _ in range(5)]
perf_ai   = [0.50, 0.60, 0.70, 0.80, 0.90]
perf_ind  = [0.50, 0.50, 0.50, 0.50, 0.50]
ai_log    = [{"has_ai_free_alternative": True, "under_human_review": True, "transparent": True}]

print(daemon_dual_prep(trajectory, perf_ai, perf_ind))
# 'increase-ai-free-practice' — gap growing

print(daemon_ethics(trajectory))
# 'noop' — EC margin stable

print(daemon_transparency(ai_log))
# 'noop' — all actions declared
```

### 13.3 Running all three at once

```python
result = GovernanceDaemons().run(
    trajectory=trajectory,
    perf_ai_trajectory=perf_ai,
    perf_indep_trajectory=perf_ind,
    ai_action_log=ai_log,
)
print(result)
# {'d_dual_prep': 'increase-ai-free-practice', 'd_ethics': 'noop', 'd_transparency': 'noop'}
```

### 13.4 What trajectory monitoring enables

**Drift detection.** A trajectory where every state satisfies thresholds but the *trend* violates them (e.g., gap growing monotonically, EC margin shrinking toward zero).

**Anticipatory correction.** Using the derivative of the safety gap, a daemon can fire before the gap exceeds threshold.

**Trajectory-level constraints.** "The safety gap must not increase monotonically over a semester" cannot be checked at a single point.

### 13.5 The deprecated pointwise filter

`is_admissible()` and `filter_admissible()` remain for backward compatibility but emit `DeprecationWarning`. For new code, use `GovernanceDaemons`.

```python
import warnings
from ctehf_ai import is_admissible

with warnings.catch_warnings():
    warnings.simplefilter("ignore", DeprecationWarning)
    result = is_admissible(action)
```

## 14. SCAM learner model

The Student Cognitive and Affective Model.

### 14.1 Basic use

```python
import numpy as np
from ctehf_ai import LearnerState, InvisibleCapacity, SCAMModel

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
    print(f"t={t+1:2d}  IC={ic_point:.3f} ± {ic_unc:.3f}")
```

### 14.2 The predict/update cycle

**`model.predict()`** — prediction step. Increases uncertainty by `process_noise`.

**`model.update(observation)`** — posterior update. Reduces uncertainty by the Kalman gain, moves the state estimate toward the observation.

### 14.3 Reading the posterior

```python
posterior = model.posterior                     # np.ndarray of point estimates
uncertainty = model.posterior_uncertainty       # np.ndarray of uncertainties
posterior_state = model.posterior_state         # LearnerState reconstructed

point, unc = model.ic_estimate()                # (IC_point, IC_uncertainty)
lower, upper = model.credible_interval(0.95)    # 95% credible interval
```

### 14.4 History

```python
for record in model.history:
    print(record["state"][:5], record["uncertainty"][:5])
```

### 14.5 The observation function

SCAM's observation function maps raw evidence to state-space observations. The default is identity — pass a vector of the same shape as `state.to_vector()`.

For real deployments, replace it with a learned encoder:

```python
def observation_fn(raw_evidence):
    """Map high-dimensional evidence to state-space observations."""
    # raw_evidence might be a dict with 'scores', 'artefact_embeddings', etc.
    # Return a vector of shape (n,) where n = len(state.to_vector())
    scores = raw_evidence["scores"]
    artefacts = raw_evidence["artefact_embeddings"]
    # ... reduce to sufficient statistics ...
    return reduced

model = SCAMModel(true_state, observation_fn=observation_fn)
```

See §28 for a worked example.

### 14.6 Configuration

```python
from ctehf_ai import SCAMConfig

config = SCAMConfig(
    process_noise=0.05,        # how much uncertainty grows per predict step
    observation_noise=0.1,     # assumed observation noise
    initial_uncertainty=0.3,   # starting uncertainty
)

model = SCAMModel(true_state, config=config)
```

### 14.7 Common pitfalls

**Shapes must match.** `update(observation)` raises `ValueError` if `observation.shape != state.shape`. Ensure your observation function returns the right shape.

**The default observation function does no inference.** It is `lambda x: x`. Passing raw evidence without an observation function will just track the evidence; it will not estimate the learner state. Real deployments need an observation function.

**SCAM tracks, it does not infer initial state.** Pass a state that is already a reasonable starting estimate.

## 15. Hybrid dynamics

Continuous evolution between events, discrete transitions at events.

### 15.1 Basic use

```python
import numpy as np
from ctehf_ai import (
    LearnerState, InvisibleCapacity, PedagogicalAction, ActionType,
    TransitionFunction, HybridDynamics,
)

def continuous_f(s_vec, action, params):
    """Continuous dynamics: ds/dt. Here, simple linear drift."""
    return 0.05 * np.ones_like(s_vec)

dynamics = HybridDynamics(
    continuous_f=continuous_f,
    discrete_g=TransitionFunction(),
    trigger_condition=lambda s: s.invisible[InvisibleCapacity.WISDOM] > 0.6,
    dt=0.1,
)

state = LearnerState(invisible={c: 0.5 for c in InvisibleCapacity})
action = PedagogicalAction(
    action_type=ActionType.SCAFFOLD,
    target=InvisibleCapacity.WISDOM.value,
    intensity=1.0,
)

next_state = dynamics.step(state, action)
```

### 15.2 Continuous only

```python
next_state = dynamics.evolve_continuous(state, action, steps=20)
```

### 15.3 Theorem 3.1 assumption checks

```python
from ctehf_ai import empirical_lipschitz, check_theorem_3_1_assumptions

points = [np.zeros(10), np.ones(10), 0.5 * np.ones(10)]
L_f = empirical_lipschitz(lambda x: 2 * x, points)
L_g = empirical_lipschitz(lambda x: 0.5 * x, points)

status = check_theorem_3_1_assumptions(L_f, L_g, trigger_measurable=True)
print(status)
# {'f_lipschitz_satisfied': True, 'f_lipschitz_constant': 2.0,
#  'g_lipschitz_satisfied': True, 'g_lipschitz_constant': 0.5,
#  'trigger_measurable': True, 'theorem_3_1_applies': True}
```

The Theorem 3.1 guarantee (existence and uniqueness of trajectories) is *not* automatic. It holds only when `f` and `g` are Lipschitz and triggers are measurable. `check_theorem_3_1_assumptions` is the practical check.

### 15.4 When the assumptions fail

SCAM's neural sub-model is not Lipschitz by default. If your SCAM implementation uses an unconstrained neural network, the theorem does not apply, and trajectories may not be unique (in practice they often are, but the guarantee is absent).

To restore the guarantee, constrain the network:

- Spectral normalization on each layer.
- Lipschitz-constrained architectures (e.g., gradient-penalized).
- Domain restriction to a compact region on which the function is empirically Lipschitz.

Document the choice in your implementation.

## 16. Free-energy precision

SCAM's inference as free-energy minimization, with thresholds as precision-weighted priors.

### 16.1 Precision priors

```python
from ctehf_ai import PrecisionPrior

p = PrecisionPrior(
    base_precision=1.0,       # precision when above threshold
    threshold=0.3,
    penalty_precision=100.0,  # precision when below threshold
)

print(p.precision(0.5))    # 1.0 (above threshold)
print(p.precision(0.1))    # 100.0 (below threshold)
```

### 16.2 Ethical precisions

```python
from ctehf_ai import ethical_precision

precisions = ethical_precision(state)
print(precisions)    # {'MA': 1.0, 'PJ': 1.0, 'RP': 1.0}  (if all above threshold)

# With a learner below MA threshold
low_ma_state = LearnerState(invisible={
    InvisibleCapacity.MORAL_RESPONSIBILITY: 0.1,
    InvisibleCapacity.CONSCIENCE:           0.1,
    # ...
})
print(ethical_precision(low_ma_state))    # {'MA': 100.0, ...}
```

### 16.3 EC via precision

```python
from ctehf_ai import ethical_competence, ethical_competence_via_precision

# In the conjugate case, these agree (up to numerical differences)
ec1 = ethical_competence(state)
ec2 = ethical_competence_via_precision(state)
```

The precision formulation is the free-energy interpretation of the same construct. When `MA < m_min`, the precision on the ethical dimension becomes large, pushing the variational posterior into the penalty region. The two functions produce the same result in the conjugate case; the precision variant is the theoretically grounded one for Bayesian integration.

### 16.4 Variational free energy

```python
import numpy as np
from ctehf_ai import variational_free_energy

q = np.array([0.5, 0.5, 0.5, 0.5, 0.5])   # variational posterior
x = np.array([0.5, 0.5, 0.5, 0.5, 0.5])   # observation

F = variational_free_energy(q, x, observation_noise=0.1)
print(F)
```

The free energy is a bounded scalar. For SCAM integration, use `ethical_competence_via_precision` rather than computing `variational_free_energy` directly.

## 17. Embeddings

`E_learner`, `E_action`, `E_artefact` — three maps into a shared Hilbert space.

### 17.1 Default implementations

```python
from ctehf_ai import (
    IdentityLearnerEmbedding, IdentityActionEmbedding, MeanArtefactEmbedding,
    LearnerState, InvisibleCapacity, PedagogicalAction, ActionType,
)
import numpy as np

# Learner → state vector
e_learner = IdentityLearnerEmbedding()
v = e_learner(LearnerState(invisible={c: 0.5 for c in InvisibleCapacity}))
print(v.shape)    # (10,)

# Action → one-hot over ActionType
e_action = IdentityActionEmbedding()
v = e_action(PedagogicalAction(action_type=ActionType.SCAFFOLD))
print(v.shape)    # (4,)

# Artefact → mean over vectorized artefacts
e_artefact = MeanArtefactEmbedding()
v = e_artefact({"a": np.array([1.0, 2.0]), "b": np.array([3.0, 4.0])})
print(v)          # [2.0, 3.0]
```

### 17.2 Similarity retrieval

```python
from ctehf_ai import similarity_in_H, nearest_neighbours

query = e_learner(LearnerState(invisible={c: 0.5 for c in InvisibleCapacity}))
candidates = {
    "similar": e_learner(LearnerState(invisible={c: 0.52 for c in InvisibleCapacity})),
    "distant": e_learner(LearnerState(invisible={c: 0.90 for c in InvisibleCapacity})),
}

result = nearest_neighbours(query, candidates, delta=0.2)
print(result)
# {'similar': 0.0632...}   — only 'similar' within delta
```

### 17.3 Compositional reasoning

Because `H` is a Hilbert space, distances and inner products are defined. You can average artefact embeddings to represent a portfolio, subtract to represent change, or cluster to represent groups:

```python
portfolio = e_artefact({
    "essay1": essay1_embedding,
    "essay2": essay2_embedding,
    "reflection": reflection_embedding,
})

# Change in representation between two time points
change = e_artefact({"t2": artefact_t2}) - e_artefact({"t1": artefact_t1})
magnitude = np.linalg.norm(change)
```

### 17.4 Replacing the default encoders

The defaults are placeholders. For production use, substitute a trained encoder:

```python
class TrainedLearnerEncoder:
    def __init__(self, model):
        self.model = model

    def __call__(self, state: LearnerState) -> np.ndarray:
        return self.model.encode(state.to_vector())
```

See §28 for a worked example.

---

# Part IV — System-Level Constructs

## 18. COH hierarchy

The Constrained Object Hierarchy with runtime constraint daemons.

### 18.1 Building a hierarchy

```python
from ctehf_ai import COHObject, ConstraintDaemon, ConstraintHierarchy

h = ConstraintHierarchy()

# Root
h.register(COHObject(name="HF_educational", level=0))

# Level 1
h.register(COHObject(name="EC", level=1, parent="HF_educational"))
h.register(COHObject(name="IC", level=1, parent="HF_educational"))
h.register(COHObject(name="DC", level=1, parent="HF_educational"))

# Constraint at level 1
h.register(COHObject(
    name="EC_constraint",
    level=1,
    parent="HF_educational",
    daemons=[ConstraintDaemon(
        name="ec_minimum",
        check=lambda s: s["ec"] >= 0.5,
        message="EC below E_min",
    )],
))
```

### 18.2 Enforcing constraints

```python
violations = h.enforce_all({"ec": 0.3, "ic": 0.7, "dc": 0.6})
print(violations)    # ['[ec_minimum] EC below E_min']

# Enforce only one level
violations_level1 = h.enforce_level(1, {"ec": 0.3, "ic": 0.7, "dc": 0.6})
```

### 18.3 The 9-tuple interpretation

The COH hierarchy in the library is a structural skeleton. The full 9-tuple components (C, A, M, N, E, I, T, G, D) are instantiated across the library's modules, not in `COHObject` alone. See the theory-to-code map in the README.

## 19. Multi-agent tutoring

The bounded multi-agent tutoring system.

### 19.1 Basic use

```python
from ctehf_ai import MultiAgentTutoringSystem

system = MultiAgentTutoringSystem()

# Check accountability
print(system.accountability_preserved())    # True

# Coordinate agents
result = system.coordinate({"learner_id": "L001", "session": 3})
print(result["agents"])
# {
#   'human_teacher': {'action': 'moral_exemplification', ..., 'non_delegable': True},
#   'ai_tutor': {'action': 'generate_and_review', ..., 'ai_free_alternative_available': True},
#   'peer_learner': {'action': 'community_accountability', ...},
#   'reflection': {'action': 'narrative_identity_formation', ...},
# }
```

### 19.2 What each agent does

| Agent | Role | Non-delegable | Bounded |
|---|---|---|---|
| `HumanTeacherAgent` | moral exemplification, dialogic instruction | **Yes** | No |
| `AITutorAgent` | content generation, feedback under human review | No | **Yes** |
| `PeerLearningAgent` | community of accountability | No | Yes |
| `ReflectionAgent` | narrative identity formation | No | Yes |

The `HumanTeacherAgent` is the only agent with `accountable=True`. If any composition of agents does not preserve this, the accountability check fails.

### 19.3 Custom agents

```python
from ctehf_ai import Agent, AgentRole

class SubjectMatterExpert(Agent):
    role = AgentRole.HUMAN_TEACHER
    name = "subject_expert"
    accountable = False    # not the accountable agent
    bounded = False

    def act(self, context):
        return {"action": "expert_review", "role": self.role.value}
```

The library does not validate that custom agents follow the pattern; it validates only that `system.accountability_preserved()` returns `True`.

## 20. FCP compliance

Check compliance with the Flourishing–Competence–Preparation Principle.

### 20.1 Basic use

```python
from ctehf_ai import check_fcp_compliance, FCPStatus

status = check_fcp_compliance(state, perf_ai=0.85, perf_indep=0.80)
print(status)
# FCPStatus.COMPLIANT
```

### 20.2 The two failure modes

```python
# Ethical violation
bad_state = LearnerState(invisible={c: 0.1 for c in InvisibleCapacity})
print(check_fcp_compliance(bad_state, 0.85, 0.80))
# FCPStatus.ETHICAL_VIOLATED

# Preparation violation
print(check_fcp_compliance(state, 0.85, 0.30))
# FCPStatus.PREPARATION_VIOLATED
```

### 20.3 Configuration

```python
from ctehf_ai import FCPPrinciple, EthicalCompetenceConfig

principle = FCPPrinciple(
    ethical_config=EthicalCompetenceConfig(m_min=0.3, p_min=0.3, r_min=0.3),
    theta_collab=0.6,
    theta_indep=0.6,
    max_safety_gap=0.15,
)

status = check_fcp_compliance(state, 0.85, 0.80, principle)
```

## 21. Threshold calibration

Calibrate thresholds from empirical data.

### 21.1 Quantile-based calibration

```python
from ctehf_ai import ThresholdCalibrator

# Assume `ec_scores` is a list of EC values from a validation set
# Set E_min at the 25th percentile
e_min = ThresholdCalibrator.calibrate_from_quantile(ec_scores, quantile=0.25)
print(e_min)
```

### 21.2 Balanced-accuracy calibration

```python
positive = [...]   # values for learners known to be ethically competent
negative = [...]   # values for learners known to be not

threshold, score = ThresholdCalibrator.calibrate_balanced_accuracy(positive, negative)
print(threshold, score)    # (thr, balanced_accuracy)
```

### 21.3 Full calibration workflow

```python
from ctehf_ai import EthicalCompetenceConfig

# Calibrate each domain threshold from a validation set
m_min = ThresholdCalibrator.calibrate_from_quantile(ma_values, 0.25)
p_min = ThresholdCalibrator.calibrate_from_quantile(pj_values, 0.25)
r_min = ThresholdCalibrator.calibrate_from_quantile(rp_values, 0.25)
E_min = ThresholdCalibrator.calibrate_from_quantile(ec_values, 0.50)

config = EthicalCompetenceConfig(
    m_min=m_min, p_min=p_min, r_min=r_min, E_min=E_min,
)
```

Calibration is context-specific; see §34 for common pitfalls.

---

# Part V — Workflows

## 22. Running a safety-gap audit

The safety gap audit is the theory's most operationally actionable construct. It gives institutions a measurable quantity for a distinction they have so far made only rhetorically.

### 22.1 The audit

```python
import csv
from ctehf_ai import safety_gap, interpret_safety_gap, recommended_response

def run_audit(csv_path):
    """Run a safety-gap audit on a CSV of learner records.

    Expected columns: learner_id, course, perf_ai, perf_indep
    """
    results = {"individual": [], "course": {}, "institution": []}

    with open(csv_path) as f:
        for row in csv.DictReader(f):
            gap = safety_gap(
                perf_ai=float(row["perf_ai"]),
                perf_indep=float(row["perf_indep"]),
            )
            interp = interpret_safety_gap(gap)
            results["individual"].append({
                "learner_id": row["learner_id"],
                "course": row["course"],
                "gap": gap,
                "interpretation": interp.value,
                "response": recommended_response(interp),
            })
            results["course"].setdefault(row["course"], []).append(gap)
            results["institution"].append(gap)

    # Aggregate
    results["course_summary"] = {
        course: {
            "n": len(gaps),
            "mean_gap": sum(gaps) / len(gaps),
            "interpretation": interpret_safety_gap(sum(gaps) / len(gaps)).value,
        }
        for course, gaps in results["course"].items()
    }
    results["institution_summary"] = {
        "n": len(results["institution"]),
        "mean_gap": sum(results["institution"]) / len(results["institution"]),
        "interpretation": interpret_safety_gap(
            sum(results["institution"]) / len(results["institution"])
        ).value,
    }
    return results


results = run_audit("learner_records.csv")
print(results["institution_summary"])
```

### 22.2 Reading the output

The audit produces three levels of aggregation:

- **Individual** — the learner's gap and recommended response.
- **Course** — course-level mean gap, indicating whether the course's design supports dual preparation.
- **Institution** — institution-level mean gap, indicating whether the institution as a whole has a dual-preparation problem.

### 22.3 Interpreting course-level gaps

A course with `mean_gap > 0.15` and `|Gap|` in the "AI dependence" range is a course where assessment design is not distinguishing AI-supported from independent performance. The recommended response is to redesign assessment around process documentation and AI-aware task design, not to prohibit AI use.

### 22.4 Institutional policy

The audit is an **audit device, not a target**. Institutions that set "reduce the safety gap" as a KPI will find their courses weakening AI-assisted performance to match unassisted performance. The right use is to identify courses where the gap is large *because assessment does not require independent demonstration*, and to redesign those assessments.

## 23. Designing a dual-preparation assessment

Dual preparation is the design principle that learners must be prepared both for AI-assisted co-work and for verified independent capability.

### 23.1 Design principles

**Paired assessment.** Every competency is assessed twice: once with AI available, once without. The safety gap is computed per learner.

**AI-aware task design.** Assessment tasks are designed so that AI assistance is either genuinely helpful (in the assisted mode) or genuinely absent (in the unassisted mode), not accidentally available or accidentally prohibited.

**Process documentation.** Assessment captures the process, not only the output, so that independent capability can be verified from artifacts (drafts, revision histories, reflection) rather than from output alone.

**AI-free alternatives.** Every AI-mediated task has a declared AI-free alternative. The governance daemon checks this.

### 23.2 Assessment design template

```python
from dataclasses import dataclass

@dataclass
class DualPrepAssessment:
    name: str
    task_description: str
    ai_assisted_version: str
    ai_free_version: str
    process_artifacts: list[str]     # what evidence the process produces
    scoring_rubric: dict             # rubric for each version

# Example
assessment = DualPrepAssessment(
    name="Argument Analysis",
    task_description="Analyze a complex argument in a provided text.",
    ai_assisted_version="Use any AI tools you wish; submit both your final analysis and a log of AI interactions.",
    ai_free_version="No AI tools. Submit your analysis with your revision history.",
    process_artifacts=["drafts", "revision_log", "reflection"],
    scoring_rubric={
        "argument_identification": 0.3,
        "evidence_evaluation": 0.3,
        "counterargument_consideration": 0.2,
        "clarity": 0.2,
    },
)
```

### 23.3 Verifying dual preparation from assessment data

```python
from ctehf_ai import safety_gap, interpret_safety_gap

def assess_dual_prep(learner_id, ai_score, indep_score):
    gap = safety_gap(ai_score, indep_score)
    interp = interpret_safety_gap(gap)

    if interp.value == "balanced":
        return {"status": "dual_prep_verified", "gap": gap}
    elif interp.value == "ai_dependence":
        return {
            "status": "ai_dependence_detected",
            "gap": gap,
            "response": "Schedule AI-free practice; do not advance until independent demonstration.",
        }
    elif interp.value == "measurement_anomaly":
        return {
            "status": "anomaly_investigate",
            "gap": gap,
            "response": "Review assessment design; unassisted performance exceeding assisted is unexpected.",
        }
    else:
        return {
            "status": "large_divergence",
            "gap": gap,
            "response": "Individual pedagogical review required.",
        }
```

### 23.4 Reporting to students

Do **not** report the safety gap as a "score." Report the dual-preparation verification:

> Your AI-assisted performance and your independent performance are both at the expected level. You have demonstrated both collaborative and independent capability in this assessment.

Not:

> Your safety gap is +0.15.

The gap is an institutional diagnostic; it is not a learner-facing metric, and treating it as one would distort learner behavior (encouraging them to sandbag their AI-assisted performance to lower their gap).

## 24. Tracking a learner across a semester

### 24.1 The workflow

```python
import numpy as np
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    SCAMModel, ethical_competence, educational_flourishing,
    GovernanceDaemons,
)

# 1. Initialise SCAM from the first assessment
initial_state = LearnerState(invisible={
    InvisibleCapacity.MORAL_RESPONSIBILITY: 0.4,
    InvisibleCapacity.ETHICAL_COMMITMENT:   0.4,
    InvisibleCapacity.CONSCIENCE:           0.4,
    InvisibleCapacity.HUMILITY:             0.4,
    InvisibleCapacity.WISDOM:               0.5,
    InvisibleCapacity.MEANING_MAKING:       0.4,
    InvisibleCapacity.PURPOSE:              0.5,
    InvisibleCapacity.EXISTENTIAL_COURAGE:  0.3,
    InvisibleCapacity.LOVE:                 0.5,
    InvisibleCapacity.EMPATHIC_PRESENCE:    0.4,
})

model = SCAMModel(initial_state)
trajectory = [initial_state]
ai_scores = []
indep_scores = []

# 2. At each assessment, update SCAM and record scores
for assessment in range(1, 9):
    # (Real deployments: replace these with actual scores)
    ai_score = 0.5 + 0.05 * assessment + np.random.normal(0, 0.05)
    indep_score = 0.45 + 0.06 * assessment + np.random.normal(0, 0.05)
    ai_scores.append(ai_score)
    indep_scores.append(indep_score)

    observation = initial_state.to_vector() + np.random.normal(0, 0.1, len(initial_state.to_vector()))
    model.predict()
    model.update(np.clip(observation, 0, 1))

    current = model.posterior_state
    trajectory.append(current)

    print(f"Assessment {assessment}: "
          f"IC={current.IC:.3f}  EC={ethical_competence(current):.3f}  "
          f"HF={educational_flourishing(current):.3f}  "
          f"Gap={ai_score - indep_score:+.3f}")

# 3. End-of-semester: check daemons and success
daemons = GovernanceDaemons()
result = daemons.run(
    trajectory=trajectory,
    perf_ai_trajectory=ai_scores,
    perf_indep_trajectory=indep_scores,
    ai_action_log=[],
)
print(result)
```

### 24.2 Reading the trajectory

The per-assessment print gives you a live view of the learner's development. If `EC` is drifting toward `E_min`, or if the gap is growing, the daemons will flag it.

### 24.3 End-of-semester evaluation

```python
from ctehf_ai import evaluate_success

final_state = model.posterior_state

report = evaluate_success(
    initial_state=initial_state,
    final_state=final_state,
    perf_ai=np.mean(ai_scores),
    perf_indep=np.mean(indep_scores),
)
print(f"Semester outcome: {'successful' if report.successful else 'incomplete'}")
if not report.successful:
    print("Failure reason:", report)
```

## 25. Detecting governance drift

The daemon layer's key capability is drift detection — catching a trajectory that is trending toward a violation before any single state violates it.

### 25.1 The workflow

```python
from ctehf_ai import GovernanceDaemons, LearnerState, InvisibleCapacity

# Assume `trajectory`, `perf_ai`, `perf_indep`, `ai_log` from a course
result = GovernanceDaemons().run(
    trajectory=trajectory,
    perf_ai_trajectory=perf_ai,
    perf_indep_trajectory=perf_indep,
    ai_action_log=ai_log,
)

# Act on each daemon's output
if result["d_dual_prep"] == "increase-ai-free-practice":
    print("Course-level intervention: add AI-free practice sessions.")
elif result["d_dual_prep"] == "monitor-closely":
    print("Gap trending upward but still within threshold; monitor.")
elif result["d_dual_prep"] == "investigate-anomaly":
    print("Unassisted performance exceeds assisted; investigate measurement.")

if result["d_ethics"] == "halt-and-remediate":
    print("Ethical competence below E_min for at least one learner; immediate remediation.")
elif result["d_ethics"] == "flag-moral-formation":
    print("Ethical competence margin shrinking; flag for moral-formation scaffolding.")

if result["d_transparency"] == "block-action":
    print("Sustained transparency violations; block AI-mediated actions pending review.")
elif result["d_transparency"] == "require-disclosure":
    print("Transparency violation; require disclosure of AI use.")
```

### 25.2 The "monitor-closely" output

The `d_dual_prep` daemon returns `monitor-closely` when the gap is within threshold but trending upward. This is not a violation — it is an early warning. Use it to trigger additional observation, not intervention.

### 25.3 Combining with the audit

The daemon layer runs at the trajectory level; the audit (§22) runs at the population level. Use both:

- **Daemon layer** — catch individual trajectories trending toward violation.
- **Audit** — compute safety gaps at course and institutional level to detect system-wide patterns.

## 26. Validating a SCAM deployment

Before trusting SCAM's estimates in real decisions, validate them against independent human assessments.

### 26.1 The validation protocol

```python
from ctehf_ai import SCAMModel, LearnerState
import numpy as np

def validate_scam(learners, human_assessments, model_factory):
    """Validate SCAM against human assessments.

    learners: list of LearnerState (initial states)
    human_assessments: list of dicts with keys matching IC, EC, DC,
                        and per-capacity assessments where available
    model_factory: callable that returns a SCAMModel for a given learner
    """
    results = []

    for learner, human in zip(learners, human_assessments):
        model = model_factory(learner)

        # Feed evidence
        for obs in human["observations"]:
            model.predict()
            model.update(obs)

        estimate = model.posterior_state

        results.append({
            "ic_scam": estimate.IC,
            "ic_human": human["IC"],
            "ic_error": abs(estimate.IC - human["IC"]),
            "ec_scam": ...,   # similarly for EC, DC
            "ec_human": human["EC"],
        })

    ic_errors = [r["ic_error"] for r in results]
    return {
        "mean_ic_error": np.mean(ic_errors),
        "max_ic_error": np.max(ic_errors),
        "ic_correlation": np.corrcoef(
            [r["ic_scam"] for r in results],
            [r["ic_human"] for r in results],
        )[0, 1],
    }
```

### 26.2 Convergence

SCAM's posterior should converge toward the true state as evidence accumulates. Test:

```python
# True state
true = LearnerState(invisible={c: 0.7 for c in InvisibleCapacity})

# SCAM with noise
model = SCAMModel(LearnerState(invisible={c: 0.3 for c in InvisibleCapacity}))

for t in range(20):
    noisy_obs = np.clip(true.to_vector() + np.random.normal(0, 0.1, len(true.to_vector())), 0, 1)
    model.predict()
    model.update(noisy_obs)

print(f"True IC: {true.IC:.3f}")
print(f"SCAM IC: {model.posterior_state.IC:.3f}")
```

After 20 observations, the SCAM estimate should be within `±0.05` of the true value (assuming the noise model is correct).

### 26.3 Calibration

The **credible interval** should be *calibrated*: a 95% interval should contain the true value 95% of the time. To test:

```python
# Repeated trials
in_interval = 0
n_trials = 1000

for _ in range(n_trials):
    true = LearnerState(invisible={c: 0.5 for c in InvisibleCapacity})
    model = SCAMModel(true, SCAMConfig(initial_uncertainty=0.3))

    # Short observation sequence
    for _ in range(5):
        noisy = np.clip(true.to_vector() + np.random.normal(0, 0.1, len(true.to_vector())), 0, 1)
        model.predict()
        model.update(noisy)

    lower, upper = model.credible_interval(0.95)
    if np.all(lower <= true.to_vector()) and np.all(true.to_vector() <= upper):
        in_interval += 1

print(f"Empirical coverage: {in_interval / n_trials:.3f}")   # should be near 0.95
```

If coverage is far from 0.95, the noise model is misspecified. Adjust `observation_noise` and `process_noise`.

## 27. Running research simulations

The `experiments.py` module provides four research-agenda simulations.

### 27.1 The four studies

```python
from ctehf_ai.experiments import (
    study1_safety_gap,
    study2_dual_prep,
    study3_scam_validation,
    study4_threshold_effects,
)

print(study1_safety_gap(n_learners=200))
# {'mean_gap': 0.148, 'std_gap': 0.132, 'interpretations': {...}}

print(study2_dual_prep(n_learners=100))
# {'dual_prep_mean_gap': 0.022, 'ai_dependent_mean_gap': 0.245}

print(study3_scam_validation(n_learners=50))
# {'mean_absolute_error': 0.023, 'max_error': 0.087}

print(study4_threshold_effects())
# {'mean_ec_above_threshold': 0.642, 'mean_ec_below_threshold': 0.0,
#  'discontinuity_magnitude': 0.642}
```

### 27.2 What the simulations show

- **Study 1** — the mean gap in a population under the assumed generator is ~0.15, with a wide spread.
- **Study 2** — dual-prep design produces a much smaller gap (~0.02) than AI-dependent design (~0.25).
- **Study 3** — SCAM recovers the true IC within ~0.02 on average.
- **Study 4** — the threshold produces a discontinuity in EC (0.64 above, 0.0 below).

### 27.3 The relationship to real studies

These are *simulations*, not empirical results. The real Study 1 requires institutional assessment data; Study 2 requires a quasi-experimental comparison; Study 3 requires human assessments to validate against; Study 4 requires longitudinal data on ethical behavior. The simulations validate that the theory's formal predictions are internally consistent; the real studies validate that they are empirically correct.

---

# Part VI — Extending and Integrating

## 28. Writing a custom encoder

The default encoders are placeholders. For real deployments, substitute trained encoders.

### 28.1 The Embedding protocol

The library defines `Embedding` as a `typing.Protocol`, meaning any object with the `__call__(obj) -> np.ndarray` method satisfies it. You do not need to subclass anything.

### 28.2 A learned learner encoder

```python
import numpy as np
from ctehf_ai import LearnerState

class TrainedLearnerEncoder:
    """Learner encoder that uses a trained PyTorch model."""

    def __init__(self, model):
        self.model = model

    def __call__(self, state: LearnerState) -> np.ndarray:
        state_vec = state.to_vector()
        # Convert to torch tensor, batch, forward, convert back
        with torch.no_grad():
            x = torch.from_numpy(state_vec).float().unsqueeze(0)
            embedding = self.model.encode(x).squeeze(0).numpy()
        return embedding
```

### 28.3 A learned artefact encoder

```python
import numpy as np

class TrainedArtefactEncoder:
    """Encoder that reduces artefacts (text, responses) to vectors."""

    def __init__(self, embedding_model):
        self.embedding_model = embedding_model

    def __call__(self, artefacts: dict[str, np.ndarray]) -> np.ndarray:
        if not artefacts:
            return np.zeros(self.embedding_model.dim)
        # Each artefact is already embedded; take the mean
        return np.mean(list(artefacts.values()), axis=0)


# The embedding_model would be a sentence encoder
# (e.g., SBERT, or any model that maps text to vectors)
```

### 28.4 Integrating with SCAM

```python
from ctehf_ai import SCAMModel

# Artifact encoder -> SCAM observation function -> state estimate
artefact_encoder = TrainedArtefactEncoder(embedding_model)
scam = SCAMModel(
    initial_state=true_state,
    observation_fn=lambda raw: raw,   # if raw is already a state vector
)
```

The design choice here is: does your SCAM take raw evidence (and use an observation function to reduce it to state-space) or already-reduced evidence? Both are valid; the observation function is the extension point.

## 29. Writing a custom ECA rule

```python
from ctehf_ai import ECARule, TriggerSet, Event, CorrectiveAction

def build_custom_triggers() -> TriggerSet:
    """Custom triggers for a specific institutional policy."""

    def low_wisdom(state):
        from ctehf_ai import InvisibleCapacity
        return state.invisible[InvisibleCapacity.WISDOM] < 0.3

    def low_purpose(state):
        from ctehf_ai import InvisibleCapacity
        return state.invisible[InvisibleCapacity.PURPOSE] < 0.3

    return TriggerSet([
        ECARule(
            name="low_wisdom_trigger",
            event=Event.SCAM_POSTERIOR_UPDATED,
            condition=low_wisdom,
            action=CorrectiveAction.TARGETED_DOMAIN_INTERVENTION,
            description="Flag for wisdom-specific scaffolding when wisdom falls below 0.3.",
        ),
        ECARule(
            name="low_purpose_trigger",
            event=Event.SCAM_POSTERIOR_UPDATED,
            condition=low_purpose,
            action=CorrectiveAction.TARGETED_DOMAIN_INTERVENTION,
            description="Flag for purpose-specific scaffolding when purpose falls below 0.3.",
        ),
    ])
```

## 30. Writing a custom governance daemon

```python
def daemon_cohort_balance(cohort_trajectories, threshold=0.15):
    """Daemon that monitors the balance of IC development across a cohort.

    Fires when the spread of IC development across the cohort exceeds threshold.
    """
    final_ics = [t[-1].IC for t in cohort_trajectories]
    initial_ics = [t[0].IC for t in cohort_trajectories]
    development = [f - i for f, i in zip(final_ics, initial_ics)]

    spread = max(development) - min(development)
    if spread > threshold:
        return "intervene-cohort-level"
    return "noop"
```

Custom daemons can be composed with the library's daemons:

```python
from ctehf_ai import GovernanceDaemons

def full_governance_check(cohorts, ...):
    standard = GovernanceDaemons().run(...)
    custom = daemon_cohort_balance(cohorts)
    return {**standard, "d_cohort_balance": custom}
```

## 31. Integrating with institutional data

### 31.1 From LMS exports

Most LMSs export assessment data as CSV with columns like `student_id`, `assignment_id`, `score`, `date`. To run a safety-gap audit:

```python
import csv
from collections import defaultdict
from ctehf_ai import safety_gap, interpret_safety_gap

def audit_from_lms(csv_path, ai_assignment_ids, indep_assignment_ids):
    """Compute safety gaps from paired AI-assisted and unassisted assessments."""
    by_student = defaultdict(dict)

    with open(csv_path) as f:
        for row in csv.DictReader(f):
            assignment = row["assignment_id"]
            if assignment in ai_assignment_ids:
                by_student[row["student_id"]]["ai"] = float(row["score"])
            elif assignment in indep_assignment_ids:
                by_student[row["student_id"]]["indep"] = float(row["score"])

    results = {}
    for student, scores in by_student.items():
        if "ai" not in scores or "indep" not in scores:
            continue   # skip students without paired assessments
        gap = safety_gap(scores["ai"], scores["indep"])
        results[student] = {
            "gap": gap,
            "interpretation": interpret_safety_gap(gap).value,
        }
    return results
```

### 31.2 From database

```python
import sqlite3
from ctehf_ai import safety_gap, interpret_safety_gap

def audit_from_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.execute("""
        SELECT student_id, course_id, perf_ai, perf_indep
        FROM assessments
        WHERE perf_ai IS NOT NULL AND perf_indep IS NOT NULL
    """)
    results = []
    for student_id, course_id, perf_ai, perf_indep in cursor:
        gap = safety_gap(perf_ai, perf_indep)
        results.append({
            "student_id": student_id,
            "course_id": course_id,
            "gap": gap,
            "interpretation": interpret_safety_gap(gap).value,
        })
    conn.close()
    return results
```

### 31.3 From a research dataset

If you have a dataset of learner records with invisible-capacity assessments:

```python
import csv
from ctehf_ai import LearnerState, InvisibleCapacity, ethical_competence

CAPACITY_COLUMNS = {
    "moral_responsibility": InvisibleCapacity.MORAL_RESPONSIBILITY,
    "ethical_commitment": InvisibleCapacity.ETHICAL_COMMITMENT,
    "conscience": InvisibleCapacity.CONSCIENCE,
    "humility": InvisibleCapacity.HUMILITY,
    "wisdom": InvisibleCapacity.WISDOM,
    "meaning_making": InvisibleCapacity.MEANING_MAKING,
    "purpose": InvisibleCapacity.PURPOSE,
    "existential_courage": InvisibleCapacity.EXISTENTIAL_COURAGE,
    "love": InvisibleCapacity.LOVE,
    "empathic_presence": InvisibleCapacity.EMPATHIC_PRESENCE,
}

def learner_from_row(row):
    return LearnerState(
        competencies={
            "algorithmic_literacy": float(row["algorithmic_literacy"]),
            "metacognition": float(row["metacognition"]),
            # ...
        },
        invisible={
            capacity: float(row[col])
            for col, capacity in CAPACITY_COLUMNS.items()
            if col in row
        },
        knowledge={
            k.removeprefix("knowledge_"): float(v)
            for k, v in row.items()
            if k.startswith("knowledge_")
        },
    )

with open("learners.csv") as f:
    for row in csv.DictReader(f):
        state = learner_from_row(row)
        print(row["id"], ethical_competence(state))
```

### 31.4 Data anonymization

Before running audits, ensure learner records are anonymized. The library does not do this for you; it is an institutional responsibility.

## 32. Integrating with an AI tutor

The library's constructs can wrap an AI tutoring system to enforce the theory's constraints.

### 32.1 The wrapping pattern

```python
from ctehf_ai import (
    LearnerState, PedagogicalAction,
    GovernanceDaemons, daemon_transparency,
    ECARule, TriggerSet, Event, CorrectiveAction,
)

class GovernedAITutor:
    """An AI tutor that enforces the CTE-HF-AI constraints."""

    def __init__(self, underlying_tutor, scam_model, governance_daemons):
        self.tutor = underlying_tutor
        self.scam = scam_model
        self.governance = governance_daemons
        self.action_log = []

    def propose_action(self, learner_state, context):
        """Propose an action from the underlying tutor."""
        proposal = self.tutor.propose(learner_state, context)

        action = PedagogicalAction(
            action_type=proposal["type"],
            involves_ai=True,
            has_ai_free_alternative=proposal.get("has_alternative", True),
            under_human_review=proposal.get("under_review", True),
            transparent=proposal.get("transparent", True),
            ai_autonomy=proposal.get("autonomy", 0.3),
        )
        self.action_log.append({
            "has_ai_free_alternative": action.has_ai_free_alternative,
            "under_human_review": action.under_human_review,
            "transparent": action.transparent,
        })
        return action

    def check_transparency(self):
        """Run the transparency daemon before executing any AI action."""
        status = daemon_transparency(self.action_log[-5:])
        if status == "block-action":
            raise RuntimeError("Sustained transparency violations; AI action blocked.")
        return status
```

### 32.2 Human-in-the-loop enforcement

The theory's Axiom 4 says human accountability is non-delegable. In practice:

```python
class HumanAccountableTutor:
    def __init__(self, ai_tutor, human_teacher):
        self.ai_tutor = ai_tutor
        self.human_teacher = human_teacher

    def suggest(self, learner_state, context):
        """AI proposes; human approves."""
        proposal = self.ai_tutor.propose(learner_state, context)
        approval = self.human_teacher.review(proposal, context)
        if not approval["approved"]:
            return {"action": "noop", "reason": approval["reason"]}
        return {**proposal, "approved_by": self.human_teacher.name}
```

The library's `MultiAgentTutoringSystem` provides the structure; `HumanTeacherAgent.accountable = True` marks the accountable agent.

### 32.3 Logging for audit

Every action in a production deployment should be logged with its governance attributes:

```python
import json

def log_action(action, context, governance_status):
    record = {
        "timestamp": ...,   # ISO 8601
        "learner_id": context["learner_id"],
        "action_type": action.action_type.value,
        "involves_ai": action.involves_ai,
        "has_ai_free_alternative": action.has_ai_free_alternative,
        "under_human_review": action.under_human_review,
        "transparent": action.transparent,
        "ai_autonomy": action.ai_autonomy,
        "governance_status": governance_status,
    }
    with open("action_log.jsonl", "a") as f:
        f.write(json.dumps(record) + "\n")
```

This log is the evidence base for governance audits.

---

# Part VII — Reference

## 33. Configuration reference

Every configurable object in the library, with defaults.

### 33.1 `EthicalCompetenceConfig`

| Field | Default | Constraint | Meaning |
|---|---|---|---|
| `w_MA` | `1/3` | ≥0, weights sum to 1 | Weight of moral agency |
| `w_PJ` | `1/3` | ≥0 | Weight of practical judgment |
| `w_RP` | `1/3` | ≥0 | Weight of relational presence |
| `m_min` | `0.2` | >0 | Moral-agency threshold |
| `p_min` | `0.2` | >0 | Practical-judgment threshold |
| `r_min` | `0.2` | >0 | Relational-presence threshold |
| `E_min` | `0.5` | — | Minimum ethical competence |
| `gamma` | `0.0` | `0 ≤ γ < E_min` | Penalty multiplier on violation |

### 33.2 `FlourishingConfig`

| Field | Default | Constraint | Meaning |
|---|---|---|---|
| `w_EC` | `1/3` | ≥0, sum to 1 | Weight of ethical competence |
| `w_IC` | `1/3` | ≥0 | Weight of invisible-capacity aggregate |
| `w_DC` | `1/3` | ≥0 | Weight of domain competence |

### 33.3 `DCConfig`

| Field | Default | Constraint | Meaning |
|---|---|---|---|
| `w_disc` | `1/3` | ≥0, sum to 1 | Weight of disciplinary mastery |
| `w_prof` | `1/3` | ≥0 | Weight of professional performance |
| `w_comp` | `1/3` | ≥0 | Weight of transferable competencies |

### 33.4 `SuccessCriteria`

| Field | Default | Meaning |
|---|---|---|
| `delta_min` | `0.05` | Minimum aggregate IC development |
| `rho` | `{MA: 0.05, PJ: 0.05, RP: 0.05}` | Per-domain no-regression tolerance |
| `theta_collab` | `0.5` | Minimum AI-assisted performance |
| `theta_indep` | `0.5` | Minimum independent performance |
| `ethical_config` | `EthicalCompetenceConfig()` | Nested EC config |

### 33.5 `SCAMConfig`

| Field | Default | Meaning |
|---|---|---|
| `process_noise` | `0.05` | Uncertainty growth per predict step |
| `observation_noise` | `0.1` | Assumed observation noise |
| `initial_uncertainty` | `0.3` | Starting uncertainty |

### 33.6 `FCPPrinciple`

| Field | Default | Meaning |
|---|---|---|
| `ethical_config` | `EthicalCompetenceConfig()` | Nested EC config |
| `theta_collab` | `0.5` | Minimum AI-assisted performance |
| `theta_indep` | `0.5` | Minimum independent performance |
| `max_safety_gap` | `0.2` | Maximum acceptable gap |

### 33.7 `PrecisionPrior`

| Field | Default | Meaning |
|---|---|---|
| `base_precision` | `1.0` | Precision when above threshold |
| `threshold` | `0.2` | Precision switch threshold |
| `penalty_precision` | `100.0` | Precision when below threshold |

### 33.8 `GovernanceDaemons`

| Field | Default | Meaning |
|---|---|---|
| `epsilon_small` | `0.05` | Small-gap threshold for dual-prep daemon |
| `ethical_config` | `None` | Nested EC config (defaults applied if None) |

### 33.9 Trigger functions

`safety_gap_triggers(perf_ai, perf_indep, epsilon_small=0.05, epsilon_large=0.25)`

`pedagogical_triggers(perf_ai, perf_indep, theta_gap=0.1, m_min=0.2, rho=0.05)`

## 34. Troubleshooting

### 34.1 Common errors

**`ValueError: Domain weights must sum to 1`**

You passed weights to `EthicalCompetenceConfig` or `FlourishingConfig` that do not sum to 1. This is a check that ensures the aggregate is well-defined:

```python
# Wrong
config = EthicalCompetenceConfig(w_MA=0.5, w_PJ=0.3, w_RP=0.3)  # sums to 1.1

# Right
config = EthicalCompetenceConfig(w_MA=0.4, w_PJ=0.3, w_RP=0.3)
```

**`ValueError: gamma must satisfy 0 <= gamma < E_min`**

The penalty multiplier `gamma` must be less than `E_min`, so that a threshold violation always produces EC below E_min:

```python
# Wrong
config = EthicalCompetenceConfig(E_min=0.5, gamma=0.6)

# Right
config = EthicalCompetenceConfig(E_min=0.5, gamma=0.3)
```

**`ValueError: Observation shape (N,) != state shape (M,)`**

SCAM's `update()` requires the observation to have the same shape as `state.to_vector()`. If your observation function returns something else, adjust it:

```python
model = SCAMModel(state, observation_fn=my_obs_fn)
# Ensure len(my_obs_fn(raw)) == len(state.to_vector())
```

**`DeprecationWarning: is_admissible is deprecated`**

You are using the pointwise filter from v0.1.0. Switch to `GovernanceDaemons`:

```python
from ctehf_ai import GovernanceDaemons
g = GovernanceDaemons()
result = g.run(trajectory, perf_ai, perf_indep, action_log)
```

### 34.2 Wrong answers

**EC is unexpectedly 0**

Check the threshold conditions:

```python
from ctehf_ai import ethical_competence_decomposed
d = ethical_competence_decomposed(state)
if d["MA"] < d["MA_threshold"]:
    print(f"MA below threshold: {d['MA']:.3f} < {d['MA_threshold']}")
```

**IC is unexpectedly low**

Some invisible capacities are not populated (default to 0.0):

```python
print(state.invisible)
# {<InvisibleCapacity.MORAL_RESPONSIBILITY: 'v_MR'>: 0.7, ...}
# Check for any 0.0 values that should have been populated
```

**DC changed unexpectedly between v0.1.0 and v0.2.0**

This is expected. `DC` is now a three-constituent composite, not a mean. Recalibrate any thresholds or comparisons that depended on the old value. See `docs/v0.2.0_migration.md`.

**FCP compliance always fails**

Check which condition fails:

```python
from ctehf_ai import check_fcp_compliance, FCPStatus
status = check_fcp_compliance(state, perf_ai, perf_indep)
if status == FCPStatus.ETHICAL_VIOLATED:
    # EC below E_min
    ...
elif status == FCPStatus.PREPARATION_VIOLATED:
    # Either perf below threshold or safety gap too large
    ...
```

### 34.3 Performance

**SCAM is slow for large cohorts**

SCAM's Kalman-style update is O(n) in the state dimension, which is small (~30). For large cohorts, batch the observations. The library does not currently expose batch APIs; this is planned for v0.3.0.

**Trigger evaluation is slow with many rules**

`TriggerSet.fire()` evaluates every rule. For large rule sets, filter by event first:

```python
ts_relevant = TriggerSet([r for r in ts.rules if r.event == event])
```

**Numpy warnings during evolution**

`HybridDynamics.evolve_continuous` clips values to `[0, 1]`. If your `continuous_f` returns huge values, the clip may introduce saturation. Adjust `dt` or the `continuous_f` scale.

### 34.4 Version mismatches

If you see unexpected behavior after an upgrade, check the version:

```python
import ctehf_ai
print(ctehf_ai.__version__)
```

And check the CHANGELOG for breaking changes. v0.2.0 has three:

- `DC` is now three-constituent (breaking for DC comparisons).
- `governance.is_admissible` is deprecated.
- `__all__` expanded from 42 to 65 exports.

## 35. Frequently asked questions

**Q: Why does `EC` return 0 for some learners?**

Because a threshold was violated. This is the theory's central claim: a capable learner without conscience is not ethically competent. If you want a purely additive `EC` for comparison, compute `σ(w · (MA, PJ, RP))` directly:

```python
from scipy.special import expit

def additive_ec(state, w_MA=1/3, w_PJ=1/3, w_RP=1/3):
    linear = w_MA * state.MA + w_PJ * state.PJ + w_RP * state.RP
    return float(expit(linear))
```

But be aware: this is *not* the theory's `EC`; it is the componsatory baseline against which the theory's non-compensatory claim is contrasted.

**Q: Can I use `LearnerState` without populating all ten invisible capacities?**

Yes. Unspecified capacities default to 0.0. Partial states are valid. For production use, however, you should populate all ten to get a meaningful `IC`.

**Q: What is the difference between `IC` and `EC`?**

`IC` is the mean of ten capacities. `EC` is the threshold-gated integration of three *domains* (each domain being the mean of its four or two constituent capacities). `IC` is partially compensatory; `EC` is non-compensatory.

**Q: Why is `DC` fully compensatory?**

Because, for a given domain outcome, disciplinary mastery, professional performance, and transferable competencies are genuinely substitutable. A learner who reasons metacognitively rather than recalling content has demonstrated the same capability by a different route. If your context requires non-substitutability (e.g., professional licensure), override the aggregate (see §7.3).

**Q: Can I use the library without SCAM?**

Yes. `state.DC`, `state.IC`, `ethical_competence(state)`, `educational_flourishing(state)`, `safety_gap(a, b)`, and the trigger sets all work independently of SCAM. SCAM is needed only for temporal tracking (predict/update) and posterior uncertainty.

**Q: What does `ε` in the total flourishing register mean?**

`ε` captures flourishing contributions from outside education's reach: health, family, economic conditions, social relationships, societal factors. It is *not* a component of the system. `HF = HF_educational + ε` distinguishes what education is accountable for from what it contributes to. The library treats `ε` as an explicit input parameter, not a component of `LearnerState`.

**Q: Can I trust SCAM's estimates?**

Not without validation. SCAM's estimates inherit the quality of its observation function and the validity of its noise model. Before using SCAM for high-stakes decisions, run §26's validation protocol against human assessments.

**Q: What thresholds should I use?**

The defaults are placeholders. Calibrate on your context (§21). A calibration workflow:

1. Collect EC (or MA, PJ, RP) values from a validation set of learners.
2. Decide the normative level: what does "minimally ethical" mean in your context?
3. Set thresholds at the appropriate quantile.
4. Validate against a held-out set.

**Q: Can I extend the library with custom modules?**

Yes. Follow the protocols (§28–§30) and the paper's vocabulary. If your extension changes the theory's formal content (e.g., makes `EC` compensatory), do not call it `ethical_competence` — use a distinct name.

## 36. Glossary

| Term | Definition |
|---|---|
| **COH** | Constrained Object Hierarchies — the mathematical theory of intelligence on which the CTE-HF-AI is built |
| **CTE-HF-AI** | Computational Theory of Education for Human Flourishing in the AI Era |
| **DC** | Domain competence — the third determinant of flourishing, fully compensatory |
| **DC_disc** | Disciplinary mastery — declarative and procedural knowledge in the domain |
| **DC_prof** | Professional performance — enacted competence in authentic tasks |
| **DC_comp** | Transferable competencies — the six competencies exercised within the domain |
| **EC** | Ethical competence — the first determinant of flourishing, non-compensatory |
| **ECA** | Event-condition-action — the form of trigger constraints |
| **FCP Principle** | Flourishing–Competence–Preparation — the theory's organizing logic |
| **HF** | Human flourishing — total flourishing, including `ε` |
| **HF_educational** | Education's contribution to flourishing, `f(EC, IC, DC)` |
| **IC** | Invisible-capacity aggregate — mean of the ten capacities, partially compensatory |
| **MA** | Moral agency — domain aggregate, mean of four capacities |
| **PJ** | Practical-existential judgment — domain aggregate, mean of four capacities |
| **RP** | Relational presence — domain aggregate, mean of two capacities |
| **Safety gap** | `Perf_AI − Perf_indep`, the divergence between AI-assisted and unassisted performance |
| **SCAM** | Student Cognitive and Affective Model — the learner state-space model |
| **ε** | The residual capturing flourishing contributions outside education's reach |

## 37. What's coming in v0.3.0

| Feature | Status | Paper reference |
|---|---|---|
| `validity.py` — Meta-Theorem of Joint Validity as runtime check | Planned | §8.2 |
| Trained encoder examples (SBERT integration, etc.) | Planned | §3.2.2 |
| Batch SCAM APIs for large cohorts | Planned | §4.2 |
| Empirical Studies 5–6 (embedding retrieval, daemon drift) | Planned | §6.2 |
| Expanded calibration helpers | Planned | §7 |
| PyPI release | Planned | — |
| Jupyter notebook tutorials | Planned | — |

Track progress at [github.com/hongxueharriswang/ctehf-lib/issues](https://github.com/hongxueharriswang/ctehf-lib/issues).

## 38. Getting help

**Documentation**
- README: overview and quick start
- Theory paper: the authoritative reference
- `docs/theory_mapping.md`: detailed paper-to-code map
- `docs/v0.2.0_migration.md`: breaking changes from v0.1.0

**Community**
- GitHub Issues: bug reports and feature requests — [github.com/hongxueharriswang/ctehf-lib/issues](https://github.com/hongxueharriswang/ctehf-lib/issues)
- GitHub Discussions: questions and design discussions (if enabled)

**Reporting a bug**

Please include:
- Python version and OS
- `ctehf_ai.__version__`
- The minimal code that reproduces the issue
- The expected behavior and the actual behavior
- Any traceback (full, not paraphrased)

**Suggesting a feature**

Please describe:
- The construct or workflow you need
- Which part of the paper it connects to
- Whether it changes the theory's formal content (if yes, it needs a paper revision first)

**Contact**

Harris Wang · harrisw@athabascau.ca · Athabasca University

---

**End of user guide.**

For the paper, see the author's preprint repository. For the README, see `README.md`. For the theory-to-code map, see `docs/theory_mapping.md`.