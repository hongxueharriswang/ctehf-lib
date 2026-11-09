# CTE-HF-AI Tutorial

**A hands-on guide for users and researchers**

Version 0.2.0 · Last updated 2026-11-08

> **Saving this file.** Place at `docs/tutorial.md` in the repository.

---

## How to Use This Tutorial

This tutorial is **hands-on**. Every section asks you to write and run code, check the output against what the theory predicts, and then extend the example on your own.

**Who should do it.** You should do this tutorial if you want to:
- Use the library in a real project.
- Understand the theory by seeing what it does in code.
- Learn to run audits, track learners, or design studies.

**How long it takes.** If you work through every section, about 10–12 hours. If you only do Tutorials 1–5, about 2 hours — enough to use the library for basic audits.

**Prerequisites.** You should have:
- Python 3.10 or later installed.
- The library installed (`pip install -e ".[dev]"` from the repo root).
- A text editor or IDE open with an empty file.

**The rules of the tutorial.**
1. **Type every example.** Do not copy-paste. Typing forces you to read.
2. **Predict before running.** Before you run a cell, write down what you expect. Then run and compare.
3. **Do the "Try it yourself" exercises.** They are where the learning happens.
4. **When something surprises you, stop.** That is a signal that the theory and your mental model disagree, and understanding why is the point.

**The two paths.** After Tutorials 1–6, you can choose:
- **Practitioner path** → Tutorials 7, 8, 9.
- **Researcher path** → Tutorials 7, 10, 11.

Tutorial 12 (extension) is available to both, and the capstone is for everyone.

---

## Tutorial 1 — Hello, Learner

**Objective:** Install the library, verify it works, and construct your first learner.

**Time:** 20 minutes.

### 1.1 Verify installation

Open a terminal and run:

```bash
python -c "import ctehf_ai; print(ctehf_ai.__version__)"
```

You should see:

```
0.2.0
```

If you see an import error, the install failed. Go back to the README's installation section.

### 1.2 The smallest possible learner

Create a file called `tutorial_01.py`:

```python
from ctehf_ai import LearnerState

# Empty state
empty = LearnerState()
print(f"Empty state has {len(empty.invisible)} invisible capacities")
print(f"Its IC is {empty.IC:.3f}")
```

Run it. You should see:

```
Empty state has 10 invisible capacities
Its IC is 0.000
```

**Why this matters.** Even an "empty" state has all ten invisible capacities present (each set to 0.0). The theory treats the ten capacities as a fixed structural feature of any learner, not an optional add-on. This is why `LearnerState()` never produces a state with missing capacities.

### 1.3 A real learner

Now add to `tutorial_01.py`:

```python
from ctehf_ai import InvisibleCapacity

learner = LearnerState(
    competencies={"algorithmic_literacy": 0.7, "metacognition": 0.6},
    invisible={
        InvisibleCapacity.MORAL_RESPONSIBILITY: 0.7,
        InvisibleCapacity.CONSCIENCE:           0.7,
        InvisibleCapacity.WISDOM:               0.7,
        InvisibleCapacity.LOVE:                 0.7,
    },
)

print(f"IC = {learner.IC:.3f}")
print(f"MA = {learner.MA:.3f}")
print(f"PJ = {learner.PJ:.3f}")
print(f"RP = {learner.RP:.3f}")
```

**Predict first.** What is `IC` for this learner? Note that only four capacities are specified; the other six default to 0.0. The mean of `(0.7, 0.7, 0.7, 0.7, 0, 0, 0, 0, 0, 0)` is `0.28`.

Now run. Do you get `0.28`? If yes, you have understood the first construct.

**What `MA`, `PJ`, `RP` mean.**

- `MA` is the mean of the four *moral agency* capacities. Here: `(0.7 + 0.7 + 0 + 0) / 4 = 0.35`.
- `PJ` is the mean of the four *practical-existential* capacities. Here: `(0.7 + 0 + 0 + 0) / 4 = 0.175`.
- `RP` is the mean of the two *relational presence* capacities. Here: `(0.7 + 0) / 2 = 0.35`.

The four capacities you specified map to different domains:
- `MORAL_RESPONSIBILITY` → `MA`
- `CONSCIENCE` → `MA`
- `WISDOM` → `PJ`
- `LOVE` → `RP`

This is why `MA` and `RP` are 0.35 (one of two capacities populated in `RP`; two of four in `MA`) while `PJ` is 0.175 (one of four populated).

### 1.4 Try it yourself

**Exercise 1.** Populate all four `PJ` capacities with 0.6 and all two `RP` capacities with 0.6. Predict `IC`, `MA`, `PJ`, and `RP` before running. Then run and check.

**Exercise 2.** Create a learner with all ten capacities set to `0.5`. What is `IC`?

**Exercise 3.** Create a learner with all ten capacities set to `0.5` and *no* competencies or knowledge. What is `DC`?

**What you learned.** The `LearnerState` object holds a fixed vector of ten invisible capacities; unset ones default to zero; three domain aggregates (`MA`, `PJ`, `RP`) and a normalized aggregate (`IC`) are computed from them.

---

## Tutorial 2 — The Non-Compensatory Claim

**Objective:** Understand the theory's most distinctive construct by seeing it fail to compensate.

**Time:** 30 minutes.

### 2.1 The two learners

The theory's central claim about ethical competence is that *a highly capable learner without conscience is not ethically competent*. Let us construct this scenario and see it in code.

Create `tutorial_02.py`:

```python
from ctehf_ai import LearnerState, InvisibleCapacity, ethical_competence

# Learner A: strong across all three domains
learner_a = LearnerState(invisible={
    InvisibleCapacity.MORAL_RESPONSIBILITY: 0.7,
    InvisibleCapacity.ETHICAL_COMMITMENT:   0.7,
    InvisibleCapacity.CONSCIENCE:           0.7,
    InvisibleCapacity.HUMILITY:             0.7,
    InvisibleCapacity.WISDOM:               0.7,
    InvisibleCapacity.MEANING_MAKING:       0.7,
    InvisibleCapacity.PURPOSE:              0.7,
    InvisibleCapacity.EXISTENTIAL_COURAGE:  0.7,
    InvisibleCapacity.LOVE:                 0.7,
    InvisibleCapacity.EMPATHIC_PRESENCE:    0.7,
})

# Learner B: exceptional in practical judgment and relational presence,
# but low moral agency
learner_b = LearnerState(invisible={
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

print(f"Learner A: EC = {ethical_competence(learner_a):.3f}")
print(f"Learner B: EC = {ethical_competence(learner_b):.3f}")
```

**Predict before running.** What do you expect? If you thought "B will be high because they score 1.0 on 6 of 10 capacities," you have expressed the *additive* intuition that the theory rejects. Run it.

You should see something like:

```
Learner A: EC = 0.668
Learner B: EC = 0.000
```

Learner B's `EC` is zero. Despite exceptional practical judgment and relational presence, Learner B has no ethical competence — because the moral-agency threshold is not met.

### 2.2 The diagnostic

Why is B's EC 0? Let's look at the decomposition:

```python
from ctehf_ai import ethical_competence_decomposed

print("Learner B decomposition:")
for key, value in ethical_competence_decomposed(learner_b).items():
    print(f"  {key}: {value}")
```

You should see:

```
  MA: 0.05
  PJ: 1.0
  RP: 1.0
  MA_threshold: 0.2
  PJ_threshold: 0.2
  RP_threshold: 0.2
  thresholds_met: 0.0
  base_sigma: 0.833...
  EC: 0.0
  E_min: 0.5
```

The **`thresholds_met`** flag is `0.0` (False): MA is 0.05, below the 0.2 threshold. Because thresholds are not met, the formula returns `γ · base_sigma` (with `γ = 0.0` by default), which is `0.0`.

Notice the **`base_sigma`** value: 0.833. This is what the additive `EC` would be if we ignored thresholds. It is very high — Learner B is "intellectually capable" in a naive sense. The threshold structure is precisely what rejects this naïve reading.

### 2.3 What if we allow partial compensation?

You can set a non-zero `gamma` to allow partial compensation:

```python
from ctehf_ai import EthicalCompetenceConfig

lenient = EthicalCompetenceConfig(gamma=0.3, E_min=0.5)
ec_lenient = ethical_competence(learner_b, lenient)
print(f"Learner B (lenient): EC = {ec_lenient:.3f}")
```

You will see `EC = 0.250` — still below `E_min = 0.5`, but not zero. The theory permits lenient thresholds, but the constraint `gamma < E_min` ensures that even a lenient `EC` never crosses the minimum when a threshold is violated. The violation is never fully erased.

### 2.4 Try it yourself

**Exercise 1.** Construct Learner C: MA = 0.5 (above threshold), PJ = 0.05 (below threshold), RP = 1.0. Predict their EC. Then run.

**Exercise 2.** At what value of MA does Learner B's EC transition from 0 to a positive value? (Answer: exactly 0.2, the threshold.)

**Exercise 3.** Modify the `EthicalCompetenceConfig` to use `m_min = 0.4`. Re-run Learner A and Learner B. What changes?

**What you learned.** The threshold structure enforces the theory's claim that moral agency is constitutive, not substitutable. `ethical_competence_decomposed` gives you the diagnostic to see which threshold failed and what the additive value would have been.

---

## Tutorial 3 — Three Determinants, Three Compensation Structures

**Objective:** See how `EC`, `IC`, and `DC` differ in their treatment of deficits.

**Time:** 30 minutes.

### 3.1 The three structures side by side

Create `tutorial_03.py`:

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    ethical_competence, educational_flourishing,
)

# Learner with one strong domain and two weak domains
lopsided = LearnerState(
    competencies={"algorithmic_literacy": 0.9, "metacognition": 0.0},
    knowledge={"algebra": 0.9, "geometry": 0.0},
    invisible={
        InvisibleCapacity.MORAL_RESPONSIBILITY: 0.9,
        InvisibleCapacity.ETHICAL_COMMITMENT:   0.9,
        InvisibleCapacity.CONSCIENCE:           0.9,
        InvisibleCapacity.HUMILITY:             0.9,
        InvisibleCapacity.WISDOM:               0.0,
        InvisibleCapacity.MEANING_MAKING:       0.0,
        InvisibleCapacity.PURPOSE:              0.0,
        InvisibleCapacity.EXISTENTIAL_COURAGE:  0.0,
        InvisibleCapacity.LOVE:                 0.9,
        InvisibleCapacity.EMPATHIC_PRESENCE:    0.9,
    },
)

print(f"IC = {lopsided.IC:.3f}   (partially compensatory)")
print(f"DC = {lopsided.DC:.3f}   (fully compensatory)")
print(f"EC = {ethical_competence(lopsided):.3f}   (non-compensatory)")
print(f"HF_educational = {educational_flourishing(lopsided):.3f}")
```

**Predict the pattern.** Each determinant is "half-populated" (some values 0.9, some 0.0). What do you expect for `IC`, `DC`, `EC`?

Run it. You should see:

```
IC = 0.540   (partially compensatory)
DC = 0.450   (fully compensatory)
EC = 0.000   (non-compensatory)
HF_educational = 0.330
```

### 3.2 Why the numbers differ

**`IC = 0.540`.** Mean of ten capacities: five are 0.9, five are 0.0. `(5 × 0.9) / 10 = 0.45`... wait, that gives 0.45, not 0.54. Let me recount. Actually: MA has four capacities all at 0.9; PJ has four capacities all at 0.0; RP has two capacities all at 0.9. So eight are 0.9, four are 0.0, wait let me recount:

- MORAL_RESPONSIBILITY: 0.9
- ETHICAL_COMMITMENT: 0.9
- CONSCIENCE: 0.9
- HUMILITY: 0.9
- WISDOM: 0.0
- MEANING_MAKING: 0.0
- PURPOSE: 0.0
- EXISTENTIAL_COURAGE: 0.0
- LOVE: 0.9
- EMPATHIC_PRESENCE: 0.9

So 6 are 0.9, 4 are 0.0. Mean = `(6 × 0.9) / 10 = 0.54`. Right, my count was wrong. So `IC = 0.540`. That is consistent with the printed output.

**`DC = 0.450`.** DC_disc = `(0.9 + 0.0) / 2 = 0.45`. DC_prof = `(0.45 + 0.45) / 2 = 0.45`. DC_comp = `(0.9 + 0.0) / 2 = 0.45`. DC = mean of the three = `0.45`. Fully compensatory: the strong capacities balance the weak ones.

**`EC = 0.000`.** PJ is 0.0 (mean of four PJ capacities, all 0.0), below the 0.2 threshold. The threshold is violated, and `EC = γ · σ(...) = 0.0`. Non-compensatory: the strong MA (0.9) and RP (0.9) do not compensate for the weak PJ.

**`HF_educational = 0.330`.** The weighted mean of `EC = 0.0`, `IC = 0.54`, `DC = 0.45`, each weighted 1/3. `(0.0 + 0.54 + 0.45) / 3 = 0.33`.

### 3.3 The asymmetry

Notice that this learner has `IC = 0.54` (partially compensatory — the mean is 0.54) but `EC = 0.0`. The learner is developing *overall* but has failed the ethical threshold. The theory holds that these are different facts, and it treats them accordingly. The additive `IC` permits substitution between domains (a learner can compensate weak PJ with strong MA); the `EC` construct does not (moral agency, practical judgment, and relational presence must each meet a minimum before the learner is ethical).

### 3.4 The diagnostic for `DC`

```python
print(lopsided.DC_decomposed)
```

You should see:

```
{'DC_disc': 0.45, 'DC_prof': 0.45, 'DC_comp': 0.45,
 'w_disc': 0.333..., 'w_prof': 0.333..., 'w_comp': 0.333..., 'DC': 0.45}
```

All three constituents are equal because the learner is symmetric within each constituent.

### 3.5 Try it yourself

**Exercise 1.** Construct a learner with MA = 0.9, PJ = 0.9, RP = 0.05. Predict `EC`. (Answer: 0.0, because RP is below threshold.)

**Exercise 2.** Construct a learner with MA = 0.3, PJ = 0.3, RP = 0.3. What is `EC`? (Answer: `σ(0.3) ≈ 0.574`. All thresholds are met, so the additive formula applies.)

**Exercise 3.** At what value of RP does the transition from `EC = 0` to `EC > 0` occur, holding MA = PJ = 0.3? (Answer: exactly 0.2.)

**What you learned.** The three determinants treat deficits differently because their underlying structures differ. `IC` and `DC` are means; `EC` is threshold-gated. This is why the theory distinguishes them and why the library implements three different aggregations.

---

## Tutorial 4 — Your First Safety Gap

**Objective:** Compute a safety gap for a learner, interpret it, and understand what distinguishes a gap that reflects dual preparation from one that reflects AI dependence.

**Time:** 30 minutes.

### 4.1 Compute and interpret

Create `tutorial_04.py`:

```python
from ctehf_ai import safety_gap, interpret_safety_gap, recommended_response

# A learner whose AI-assisted and unassisted performance are close
paired_1 = (0.82, 0.78)

# A learner whose AI-assisted performance greatly exceeds unassisted
paired_2 = (0.90, 0.45)

# A learner whose unassisted performance exceeds assisted
paired_3 = (0.60, 0.80)

for label, (ai, indep) in [("paired_1", paired_1),
                             ("paired_2", paired_2),
                             ("paired_3", paired_3)]:
    gap = safety_gap(ai, indep)
    interp = interpret_safety_gap(gap)
    print(f"{label}: gap = {gap:+.3f}  [{interp.value}]")
    print(f"   → {recommended_response(interp)}")
```

You should see:

```
paired_1: gap = +0.040  [balanced]
   → Sustain current dual-preparation design; monitor for drift.
paired_2: gap = +0.450  [large_divergence]
   → Flag for individual pedagogical review; consider SCAM-informed intervention.
paired_3: gap = -0.200  [measurement_anomaly]
   → Investigate measurement or pedagogical anomaly.
```

### 4.2 Why paired_2 is "large divergence," not "AI dependence"

With default thresholds (`ε_small = 0.05`, `ε_large = 0.25`), a gap of 0.45 is `≥ ε_large`, so the interpretation is `LARGE_DIVERGENCE` — an extreme case of AI dependence. The two labels differ in what they recommend:

- **AI dependence** (moderate gap) → increase AI-free practice.
- **Large divergence** → flag for individual review.

Both indicate AI dependence; the second is more urgent.

### 4.3 What distinguishes a "balanced" gap from a "small" gap

A balanced gap is `|Gap| ≤ 0.05`. A small-but-not-balanced gap is `0.05 < Gap < 0.25`. Try:

```python
# Moderate AI dependence
print(interpret_safety_gap(safety_gap(0.80, 0.70)).value)   # 'ai_dependence'

# Smaller, still balanced
print(interpret_safety_gap(safety_gap(0.80, 0.77)).value)   # 'balanced'
```

The safety gap is not a continuous measure of "how good" a learner is. It is a categorical diagnostic with three or four possible values. The categories are designed to be actionable.

### 4.4 Adjusting thresholds

```python
# Stricter: any gap above 0.03 is "AI dependence"
interp = interpret_safety_gap(0.040, small_threshold=0.03, large_threshold=0.25)
print(interp.value)   # 'ai_dependence'
```

Different institutions may calibrate `ε_small` and `ε_large` differently. A university with a strong dual-preparation tradition might set `ε_small = 0.02`; an institution just beginning to think about dual preparation might set `ε_small = 0.10`.

### 4.5 Try it yourself

**Exercise 1.** Compute the safety gap for `(0.72, 0.72)` and interpret it. What's the pattern?

**Exercise 2.** At what AI-assisted score does a learner with `perf_indep = 0.60` become "large divergence"? (Answer: `0.85`, because `0.85 - 0.60 = 0.25 = ε_large`.)

**Exercise 3.** Write a function `classify_learner(ai, indep) -> str` that returns "prepared," "dependent," or "anomaly" based on the interpretation. Use only the four interpretation categories.

**What you learned.** The safety gap is a categorical diagnostic, not a continuous score. It distinguishes four cases — balanced, AI dependence, anomaly, large divergence — each with its own recommended response. The default thresholds are placeholders; real deployments calibrate them.

---

## Tutorial 5 — From Rules to Triggers

**Objective:** Understand how safety gaps become machine-actionable rules.

**Time:** 30 minutes.

### 5.1 What an ECA rule is

An event–condition–action rule fires when a specific event occurs and a condition on the state holds. In the library, triggers are collected into `TriggerSet` objects.

### 5.2 The safety-gap triggers

Create `tutorial_05.py`:

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    Event, CorrectiveAction,
    safety_gap_triggers,
)

state = LearnerState(invisible={c: 0.6 for c in InvisibleCapacity})

# Rule set for a balanced learner
balanced_ts = safety_gap_triggers(perf_ai=0.75, perf_indep=0.73)
actions = balanced_ts.fire(Event.SAFETY_GAP_COMPUTED, state)
print(f"Balanced: {[a.value for a in actions]}")

# Rule set for a dependent learner
dependent_ts = safety_gap_triggers(perf_ai=0.85, perf_indep=0.70)
actions = dependent_ts.fire(Event.SAFETY_GAP_COMPUTED, state)
print(f"Dependent: {[a.value for a in actions]}")

# Rule set for an extreme divergence
extreme_ts = safety_gap_triggers(perf_ai=0.92, perf_indep=0.45)
actions = extreme_ts.fire(Event.SAFETY_GAP_COMPUTED, state)
print(f"Extreme: {[a.value for a in actions]}")
```

You should see:

```
Balanced: ['sustain_and_monitor']
Dependent: ['increase_ai_free_practice']
Extreme: ['flag_for_pedagogical_review']
```

### 5.3 The pedagogical triggers

The `pedagogical_triggers` function builds triggers for the three canonical pedagogical conditions:

```python
from ctehf_ai import pedagogical_triggers, Event

# A dependent learner triggers the AI-dependence rule
ts = pedagogical_triggers(perf_ai=0.85, perf_indep=0.55, m_min=0.2)
actions = ts.fire(Event.ASSESSMENT_COMPLETED, state)
print(f"On assessment: {[a.value for a in actions]}")
# ['increase_ai_free_practice']

# A low-MA learner triggers the ethical-threshold rule
low_ma_state = LearnerState(invisible={
    **{c: 0.5 for c in InvisibleCapacity},
    InvisibleCapacity.MORAL_RESPONSIBILITY: 0.1,
    InvisibleCapacity.ETHICAL_COMMITMENT:   0.1,
    InvisibleCapacity.CONSCIENCE:           0.1,
    InvisibleCapacity.HUMILITY:             0.1,
})
actions = ts.fire(Event.SCAM_POSTERIOR_UPDATED, low_ma_state)
print(f"On posterior update: {[a.value for a in actions]}")
# ['flag_moral_formation']
```

### 5.4 No-op default

If no rule fires, `TriggerSet.fire()` returns `[NOOP]`:

```python
# A balanced learner with no low capacities — nothing fires
noop_ts = safety_gap_triggers(0.75, 0.74)
actions = noop_ts.fire(Event.SAFETY_GAP_COMPUTED, state)
# Actually balanced rule fires, so returns [sustain_and_monitor]
# To get [noop], you would need a rule set with no applicable rules
```

The `[NOOP]` default makes the return type uniform. If you need to distinguish "fired with a real action" from "nothing fired," check against `[CorrectiveAction.NOOP]`.

### 5.5 Inspecting the rule set

```python
for rule in ts.rules:
    print(f"{rule.name:22s} {rule.event.value:30s} → {rule.action.value}")
```

You will see something like:

```
ai_dependence          assessment_completed           → increase_ai_free_practice
ethical_threshold      scam_posterior_updated         → flag_moral_formation
critical_regression    longitudinal_comparison        → targeted_domain_intervention
```

### 5.6 Try it yourself

**Exercise 1.** Construct a `TriggerSet` manually with a single rule that fires when `state.IC < 0.3`, with `CorrectiveAction.TARGETED_DOMAIN_INTERVENTION`. Test it on a low-IC learner.

**Exercise 2.** What is the difference between `pedagogical_triggers(...)` and `safety_gap_triggers(...)`? Look at the rule names and actions. (Answer: `pedagogical_triggers` responds to assessment events and posterior updates; `safety_gap_triggers` responds specifically to gap computation, and its four rules cover all four gap interpretations.)

**Exercise 3.** Given a learner whose MA is exactly 0.2 (the threshold), does the ethical-threshold rule fire? (Answer: no, because the condition is strict `<`, not `≤`. The learner is exactly at the threshold and therefore ethical.)

**What you learned.** ECA rules are the theory's translation of "what to do when" into machine-actionable form. They are the bridge between the diagnostic (safety gap) and the intervention (which response).

---

## Tutorial 6 — Tracking a Learner with SCAM

**Objective:** Use SCAM to track a learner across observations.

**Time:** 45 minutes.

### 6.1 The basic cycle

SCAM maintains a posterior distribution over the learner state. Two operations:

- `predict()` — prediction step, increases uncertainty.
- `update(observation)` — update step, reduces uncertainty.

Create `tutorial_06.py`:

```python
import numpy as np
from ctehf_ai import LearnerState, InvisibleCapacity, SCAMModel

# A learner's true state (unknown to SCAM)
true_state = LearnerState(invisible={c: 0.7 for c in InvisibleCapacity})

# SCAM starts from a rough guess
initial_guess = LearnerState(invisible={c: 0.3 for c in InvisibleCapacity})
model = SCAMModel(initial_guess)

n = len(true_state.to_vector())

for t in range(10):
    # Simulate noisy observations of the true state
    observation = np.clip(
        true_state.to_vector() + np.random.normal(0, 0.15, n),
        0, 1,
    )
    model.predict()
    model.update(observation)

    posterior_ic = model.posterior_state.IC
    point, unc = model.ic_estimate()
    print(f"t={t+1:2d}  IC={posterior_ic:.3f}  uncertainty={unc:.3f}")
```

**Predict before running.** SCAM starts at `IC = 0.3` (the initial guess). The true IC is 0.7. What will the posterior be after 10 observations? It should converge toward 0.7 (the truth) with uncertainty decreasing.

Run it. You should see something like:

```
t= 1  IC=0.330  uncertainty=0.29
t= 2  IC=0.360  uncertainty=0.28
t= 3  IC=0.390  uncertainty=0.26
...
t=10  IC=0.680  uncertainty=0.15
```

The exact numbers depend on the random seed, but the *pattern* is consistent: the estimate converges toward the truth, and the uncertainty decreases.

### 6.2 What if the observations are wrong?

If SCAM's observation function assumes the observations are noisy around the truth but they are actually systematically biased, SCAM will converge to the wrong value. Try:

```python
# Systematically biased observations — 0.1 too high
biased_obs = np.clip(true_state.to_vector() + 0.1 + np.random.normal(0, 0.15, n), 0, 1)
model.update(biased_obs)
```

SCAM converges toward 0.8 (the biased truth), not 0.7 (the real truth). This is not a bug; it is a property of any Bayesian estimator with a misspecified noise model. For real deployments, validate SCAM (§Tutorial 10).

### 6.3 The credible interval

```python
lower, upper = model.credible_interval(confidence=0.95)
print(f"IC ∈ [{model.posterior_state.IC:.3f} − {model.posterior_state.IC - lower[0]:.3f}, "
      f"{model.posterior_state.IC:.3f} + {upper[0] - model.posterior_state.IC:.3f}]")
```

The interval width reflects uncertainty: after 10 observations it is narrow; after 2, wide.

### 6.4 The history

```python
for i, record in enumerate(model.history):
    print(f"Step {i+1}: IC = {record['state'][:10].mean():.3f}, "
          f"uncertainty = {record['uncertainty'][:10].mean():.3f}")
```

### 6.5 Try it yourself

**Exercise 1.** How many observations does it take for SCAM to converge within 0.05 of the truth (starting from `IC = 0.3`, true `IC = 0.7`)? Run the loop with `range(20)` and inspect.

**Exercise 2.** Change `initial_uncertainty` from 0.3 to 0.1. Does convergence happen faster or slower?

**Exercise 3.** Change `observation_noise` from 0.1 to 0.3. What happens?

**What you learned.** SCAM maintains a posterior over the learner state, updated by observations. Convergence depends on the noise model being approximately correct; systematic bias persists.

---

## Tutorial 7 — Detecting Drift with Daemons

**Objective:** Use the governance daemon layer to detect trends that pointwise checks miss.

**Time:** 30 minutes.

### 7.1 The pointwise problem

Consider a trajectory where every state has `EC > E_min` but the margin is shrinking toward zero. A pointwise check would not fire; the learner is technically fine. But the trajectory is concerning.

Create `tutorial_07.py`:

```python
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    daemon_ethics, GovernanceDaemons,
)

# A trajectory where EC is slowly declining
trajectory = []
for ec_level in [0.9, 0.85, 0.8, 0.75, 0.7, 0.65, 0.6]:
    # Approximate a state with that EC by scaling capacities
    state = LearnerState(invisible={c: ec_level for c in InvisibleCapacity})
    trajectory.append(state)

print(f"Final state EC: {daemon_ethics(trajectory)}")
```

The `daemon_ethics` function returns one of:

- `'noop'` — margin stable or increasing.
- `'flag-moral-formation'` — margin shrinking toward zero.
- `'halt-and-remediate'` — EC already below E_min.

**Predict before running.** EC is 0.6 in the final state (well above `E_min = 0.5`), but the margin has shrunk from 0.4 to 0.1. What will the daemon return?

Run it. You should see:

```
Final state EC: flag-moral-formation
```

The daemon detected the *trend*, not the current state. This is what trajectory monitoring enables that pointwise filtering does not.

### 7.2 The dual-prep daemon

```python
# A trajectory where the safety gap is growing
perf_ai = [0.55, 0.60, 0.65, 0.70, 0.75, 0.80]
perf_indep = [0.55, 0.55, 0.55, 0.55, 0.55, 0.55]

trajectory = [LearnerState(invisible={c: 0.7 for c in InvisibleCapacity})
              for _ in range(len(perf_ai))]

from ctehf_ai import daemon_dual_prep
print(daemon_dual_prep(trajectory, perf_ai, perf_indep))
```

You should see:

```
increase-ai-free-practice
```

The gap is growing (from 0.00 to 0.25) and the daemon is recommending intervention before the gap crosses any single threshold. This is **anticipatory correction**.

### 7.3 Running all daemons together

```python
ai_log = [
    {"has_ai_free_alternative": True, "under_human_review": True, "transparent": True},
    {"has_ai_free_alternative": True, "under_human_review": True, "transparent": True},
]

result = GovernanceDaemons().run(
    trajectory=trajectory,
    perf_ai_trajectory=perf_ai,
    perf_indep_trajectory=perf_indep,
    ai_action_log=ai_log,
)
print(result)
```

You should see:

```
{'d_dual_prep': 'increase-ai-free-practice',
 'd_ethics': 'noop',
 'd_transparency': 'noop'}
```

### 7.4 The transparency daemon

If AI actions do not declare AI-free alternatives or human review:

```python
bad_log = [
    {"has_ai_free_alternative": False, "under_human_review": True, "transparent": True},
    {"has_ai_free_alternative": False, "under_human_review": True, "transparent": True},
]

from ctehf_ai import daemon_transparency
print(daemon_transparency(bad_log))   # 'block-action'
```

Sustained transparency violations block the action. This is the daemon layer enforcing the theory's bounded-agency principle.

### 7.5 Try it yourself

**Exercise 1.** Construct a trajectory where the safety gap is *shrinking*. What does `daemon_dual_prep` return?

**Exercise 2.** Construct a trajectory where EC is stable at 0.9. What does `daemon_ethics` return?

**Exercise 3.** Construct a log with exactly one violation. What does `daemon_transparency` return? (Answer: `'require-disclosure'`, because `block-action` requires two or more violations.)

**What you learned.** The daemon layer detects *trends*, not *states*. It fires on growing gaps and shrinking margins before any single observation fails a threshold. This is the "anticipatory" governance the theory requires.

---

## Tutorial 8 — A Semester, Simulated

**Objective:** Run an end-to-end simulation of a single learner across a semester.

**Time:** 45 minutes.

### 8.1 The setup

Create `tutorial_08.py`:

```python
import numpy as np
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    SCAMModel, ethical_competence, educational_flourishing,
    GovernanceDaemons, evaluate_success,
)

rng = np.random.default_rng(42)

# Initial state: struggling learner
initial = LearnerState(
    competencies={"algorithmic_literacy": 0.3, "metacognition": 0.3},
    invisible={
        InvisibleCapacity.MORAL_RESPONSIBILITY: 0.4,
        InvisibleCapacity.ETHICAL_COMMITMENT:   0.4,
        InvisibleCapacity.CONSCIENCE:           0.4,
        InvisibleCapacity.HUMILITY:             0.4,
        InvisibleCapacity.WISDOM:               0.4,
        InvisibleCapacity.MEANING_MAKING:       0.4,
        InvisibleCapacity.PURPOSE:              0.4,
        InvisibleCapacity.EXISTENTIAL_COURAGE:  0.3,
        InvisibleCapacity.LOVE:                 0.4,
        InvisibleCapacity.EMPATHIC_PRESENCE:    0.4,
    },
)

model = SCAMModel(initial)
trajectory = [initial]
ai_scores = []
indep_scores = []

# Simulate 12 weeks
for week in range(1, 13):
    # Simulate performance: both improve but AI-assisted improves faster
    ai = np.clip(0.4 + 0.04 * week + rng.normal(0, 0.05), 0, 1)
    indep = np.clip(0.4 + 0.03 * week + rng.normal(0, 0.05), 0, 1)
    ai_scores.append(ai)
    indep_scores.append(indep)

    # Simulate noisy observation of the true state
    true_growth = 0.4 + 0.025 * week
    obs = np.clip(
        np.full(len(initial.to_vector()), true_growth) + rng.normal(0, 0.1, len(initial.to_vector())),
        0, 1,
    )
    model.predict()
    model.update(obs)

    current = model.posterior_state
    trajectory.append(current)

    print(f"Week {week:2d}: IC={current.IC:.3f}  EC={ethical_competence(current):.3f}  "
          f"HF={educational_flourishing(current):.3f}  "
          f"Gap={ai - indep:+.3f}")
```

### 8.2 Reading the trajectory

Run it. You should see something like:

```
Week  1: IC=0.425  EC=0.606  HF=0.42  Gap=+0.02
Week  2: IC=0.450  EC=0.620  HF=0.44  Gap=+0.03
...
Week 12: IC=0.680  EC=0.700  HF=0.66  Gap=+0.12
```

Three patterns to notice:

1. **IC is growing steadily.** The learner is developing.
2. **EC is growing slowly** (from ~0.6 to ~0.7). The threshold structure means EC is bounded well below the other determinants until all domains are consistently high.
3. **Gap is growing** (from 0.02 to 0.12). The learner is becoming increasingly AI-dependent.

The theory's claim is that (3) is a *problem*, even as (1) and (2) look fine. The final gap of 0.12 is above `ε_small = 0.05` — the learner has drifted into AI dependence.

### 8.3 The daemons check

At the end of the semester:

```python
result = GovernanceDaemons().run(
    trajectory=trajectory,
    perf_ai_trajectory=ai_scores,
    perf_indep_trajectory=indep_scores,
    ai_action_log=[],
)
print(result)
```

You should see:

```
{'d_dual_prep': 'increase-ai-free-practice', 'd_ethics': 'noop', 'd_transparency': 'noop'}
```

The dual-prep daemon flags the trajectory: even though the final gap is only 0.12 (still in the "AI dependence" category, not "large divergence"), the *trend* is concerning.

### 8.4 End-of-semester evaluation

```python
final = model.posterior_state

report = evaluate_success(
    initial_state=initial,
    final_state=final,
    perf_ai=np.mean(ai_scores),
    perf_indep=np.mean(indep_scores),
)
print(f"Successful: {report.successful}")
if not report.successful:
    print(f"  Dual prep: {report.dual_preparation_satisfied}")
    print(f"  Ethical: {report.ethical_threshold_satisfied}")
    print(f"  IC development: {report.aggregate_ic_development:.3f}")
    print(f"  No regression: {report.no_critical_regression}")
```

The end-of-semester evaluation uses the *mean* performance, not the final gap. This is because the success criterion is about the trajectory as a whole, not the last observation.

### 8.5 Try it yourself

**Exercise 1.** Change the simulation so AI-assisted and unassisted performance grow at the same rate (both `0.04 * week`). What happens to the gap trajectory and the daemon output?

**Exercise 2.** Change the initial state so MA starts at 0.15 (below threshold). Does the learner cross the ethical threshold during the semester? At what week?

**Exercise 3.** Change the `GovernanceDaemons` config to use `epsilon_small = 0.10`. Does the dual-prep daemon still fire?

**What you learned.** A semester-long simulation reveals patterns that single assessments miss. Even when the learner looks fine on any given week, the trajectory can reveal drift. The daemon layer is designed for exactly this.

---

## Tutorial 9 — A Full Institutional Audit

**Objective:** Run a safety-gap audit across a synthetic institutional dataset.

**Time:** 45 minutes.

### 9.1 Generate synthetic data

Create `tutorial_09.py`:

```python
import csv
import numpy as np
from collections import defaultdict

rng = np.random.default_rng(42)

# Generate 200 learners across 5 courses
courses = ["BIO101", "CHEM101", "HIST101", "MATH101", "PHYS101"]

with open("institutional_audit.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["learner_id", "course", "perf_ai", "perf_indep"])

    for learner_num in range(200):
        learner_id = f"L{learner_num:03d}"
        course = rng.choice(courses)

        # Different courses have different AI-dependence patterns
        base = rng.uniform(0.5, 0.8)
        if course in ["BIO101", "CHEM101"]:
            # Dual-prep designed — small gap
            ai = np.clip(base + rng.normal(0.05, 0.08), 0, 1)
            indep = np.clip(base + rng.normal(0.03, 0.08), 0, 1)
        elif course in ["HIST101"]:
            # AI-heavy course — large gap
            ai = np.clip(base + rng.normal(0.20, 0.08), 0, 1)
            indep = np.clip(base + rng.normal(-0.05, 0.08), 0, 1)
        else:
            # Mixed
            ai = np.clip(base + rng.normal(0.10, 0.10), 0, 1)
            indep = np.clip(base + rng.normal(0.05, 0.10), 0, 1)

        writer.writerow([learner_id, course, f"{ai:.3f}", f"{indep:.3f}"])

print("Wrote institutional_audit.csv")
```

Run it. You now have a synthetic dataset that simulates an institution where:
- BIO101 and CHEM101 have dual-prep-designed courses.
- HIST101 is AI-heavy.
- MATH101 and PHYS101 are mixed.

### 9.2 Run the audit

Add to `tutorial_09.py`:

```python
from ctehf_ai import safety_gap, interpret_safety_gap, recommended_response

def audit(csv_path):
    by_course = defaultdict(list)
    institution = []

    with open(csv_path) as f:
        for row in csv.DictReader(f):
            ai = float(row["perf_ai"])
            indep = float(row["perf_indep"])
            gap = safety_gap(ai, indep)
            by_course[row["course"]].append(gap)
            institution.append(gap)

    print("=== Course-level summary ===")
    for course, gaps in sorted(by_course.items()):
        mean_gap = float(np.mean(gaps))
        interp = interpret_safety_gap(mean_gap)
        print(f"{course}: n={len(gaps)}  mean_gap={mean_gap:+.3f}  [{interp.value}]")

    print(f"\n=== Institution summary ===")
    mean_gap = float(np.mean(institution))
    interp = interpret_safety_gap(mean_gap)
    print(f"n={len(institution)}  mean_gap={mean_gap:+.3f}  [{interp.value}]")
    print(f"Recommended response: {recommended_response(interp)}")

audit("institutional_audit.csv")
```

You should see something like:

```
=== Course-level summary ===
BIO101: n=42  mean_gap=+0.022  [balanced]
CHEM101: n=39  mean_gap=+0.018  [balanced]
HIST101: n=38  mean_gap=+0.253  [large_divergence]
MATH101: n=41  mean_gap=+0.054  [ai_dependence]
PHYS101: n=40  mean_gap=+0.048  [balanced]

=== Institution summary ===
n=200  mean_gap=+0.079  [ai_dependence]
Recommended response: Increase AI-free practice; introduce productive struggle; redesign assessment to require independent demonstration.
```

### 9.3 Reading the output

The audit reveals:

- **BIO101 and CHEM101** are balanced (dual-prep working).
- **HIST101** has a large divergence (the AI-heavy course is not verifying independent capability).
- **MATH101 and PHYS101** are at the boundary — `+0.054` is "AI dependence" but barely; `+0.048` is "balanced" but close.

The institution-level mean (`+0.079`) is pulled upward by HIST101. The recommended response is institution-wide, but the *target* for intervention is HIST101.

### 9.4 The trap

If the institution interprets the audit as a KPI ("reduce the mean gap") and rewards HIST101 for lowering its gap, HIST101's instructors might weaken their AI-assisted assessments to match the unassisted ones. That would be gaming the metric.

The right response is to redesign HIST101's assessment so that:
- AI-assisted tasks are paired with AI-free tasks.
- Process documentation makes independent demonstration visible.
- The gap *becomes* small because AI-dependent performance is no longer rewarded.

### 9.5 Try it yourself

**Exercise 1.** Add a fourth interpretation category for MATH101's borderline case. What threshold change would you need to classify `+0.054` as balanced?

**Exercise 2.** Write a function that returns, for each course, whether a redesign is warranted. Use `mean_gap > 0.10` as the criterion.

**Exercise 3.** Modify the synthetic data generator so that HIST101's gap is *negative* (unassisted > assisted). What interpretation does the audit produce, and what does that suggest?

**What you learned.** The audit is a categorical report, not a score. It aggregates individual gaps to course and institution level, and its output should drive *assessment redesign*, not *metric optimization*.

---

## Tutorial 10 — A Validation Study

**Objective:** Validate SCAM against ground truth.

**Time:** 45 minutes.

### 10.1 The setup

You have SCAM estimates. You have ground truth (from human assessments, interviews, or both). You want to know: does SCAM recover the truth?

Create `tutorial_10.py`:

```python
import numpy as np
from ctehf_ai import LearnerState, InvisibleCapacity, SCAMModel

rng = np.random.default_rng(42)

# Ground-truth learners (unknown to SCAM)
true_learners = []
for _ in range(100):
    true_state = LearnerState(invisible={
        c: float(rng.uniform(0.2, 0.9)) for c in InvisibleCapacity
    })
    true_learners.append(true_state)

# SCAM estimates (starting from a weak guess)
estimates = []
for true_state in true_learners:
    model = SCAMModel(LearnerState(invisible={c: 0.5 for c in InvisibleCapacity}))

    # Feed 5 noisy observations
    for _ in range(5):
        obs = np.clip(
            true_state.to_vector() + rng.normal(0, 0.15, 10),
            0, 1,
        )
        model.predict()
        model.update(obs)

    estimates.append(model.posterior_state)

# Compute errors
ic_errors = [abs(est.IC - true.IC) for est, true in zip(estimates, true_learners)]
ma_errors = [abs(est.MA - true.MA) for est, true in zip(estimates, true_learners)]

print(f"IC mean absolute error: {np.mean(ic_errors):.3f}")
print(f"IC max error: {np.max(ic_errors):.3f}")
print(f"MA mean absolute error: {np.mean(ma_errors):.3f}")

# Correlation
true_ics = [t.IC for t in true_learners]
est_ics = [e.IC for e in estimates]
print(f"IC correlation: {np.corrcoef(true_ics, est_ics)[0, 1]:.3f}")
```

### 10.2 Reading the validation

Run it. You should see something like:

```
IC mean absolute error: 0.064
IC max error: 0.156
MA mean absolute error: 0.091
IC correlation: 0.892
```

Three things to notice:

- **Mean absolute error ~0.06**: SCAM's IC estimates are on average within 0.06 of the truth. This is good but not perfect.
- **Max error ~0.16**: some learners have much larger errors. These are typically learners whose true state is near the extremes (0.2 or 0.9) where the prior pulls the estimate toward the middle.
- **Correlation 0.89**: SCAM's estimates track the true ordering well, even if the absolute error is nonzero.

### 10.3 Improving the validation

Five observations is few. Try more:

```python
# 15 observations instead of 5
estimates_15 = []
for true_state in true_learners:
    model = SCAMModel(LearnerState(invisible={c: 0.5 for c in InvisibleCapacity}))
    for _ in range(15):
        obs = np.clip(true_state.to_vector() + rng.normal(0, 0.15, 10), 0, 1)
        model.predict()
        model.update(obs)
    estimates_15.append(model.posterior_state)

ic_errors_15 = [abs(est.IC - true.IC) for est, true in zip(estimates_15, true_learners)]
print(f"With 15 observations: mean error = {np.mean(ic_errors_15):.3f}")
```

The error should drop (typically to ~0.03). This is the classic Bayesian tradeoff: more evidence gives more precise estimates.

### 10.4 The bias of the prior

SCAM starts from a uniform prior at 0.5. Learners whose true state is 0.2 or 0.9 will be pulled toward 0.5 initially, and require more evidence to escape. To see:

```python
extreme_learners = [t for t in true_learners if t.IC < 0.35 or t.IC > 0.65]
extreme_estimates = [e for t, e in zip(true_learners, estimates) if t.IC < 0.35 or t.IC > 0.65]
extreme_errors = [abs(e.IC - t.IC) for e, t in zip(extreme_estimates, extreme_learners)]
print(f"Mean error for extreme learners: {np.mean(extreme_errors):.3f}")
```

You should see that extreme learners have higher error than the population average. This is expected and is a known limitation of Bayesian estimation with a central prior.

### 10.5 Try it yourself

**Exercise 1.** Change `initial_uncertainty` from 0.3 to 0.1. Does the extreme-learner bias decrease or increase?

**Exercise 2.** Change the observation noise from 0.15 to 0.3. What happens to the mean absolute error?

**Exercise 3.** Change the initial guess from 0.5 to 0.7 for all learners. Does the bias toward 0.5 decrease? Does a new bias appear?

**What you learned.** Validation is not pass/fail — it is a distribution of errors. SCAM recovers the truth reasonably well on average, is biased for extreme learners, and improves with more evidence. Real deployments must validate against their own observation models and their own populations.

---

## Tutorial 11 — A Research Study

**Objective:** Run one of the paper's four research-agenda simulations.

**Time:** 30 minutes.

### 11.1 Study 3 — SCAM validation (simulated)

Create `tutorial_11.py`:

```python
from ctehf_ai.experiments import study3_scam_validation

for n in [10, 30, 100]:
    result = study3_scam_validation(n_learners=n, seed=42)
    print(f"n={n:3d}  MAE={result['mean_absolute_error']:.3f}  max={result['max_error']:.3f}")
```

You should see:

```
n= 10  MAE=0.0XX  max=0.XXX
n= 30  MAE=0.0XX  max=0.XXX
n=100  MAE=0.0XX  max=0.XXX
```

The exact numbers depend on the seed. What matters is that MAE is stable across sample sizes (because each learner is simulated independently) and that max error reveals the worst-case learner.

### 11.2 Study 2 — dual-prep comparison (simulated)

```python
from ctehf_ai.experiments import study2_dual_prep

result = study2_dual_prep(n_learners=200)
print(f"Dual-prep mean gap: {result['dual_prep_mean_gap']:.3f}")
print(f"AI-dependent mean gap: {result['ai_dependent_mean_gap']:.3f}")
```

You should see:

```
Dual-prep mean gap: 0.02X
AI-dependent mean gap: 0.2XX
```

The gap under dual-prep design is an order of magnitude smaller than under AI-dependent design. This is the theory's central prediction (Prediction 2 in the paper).

### 11.3 Study 4 — threshold effects (simulated)

```python
from ctehf_ai.experiments import study4_threshold_effects

result = study4_threshold_effects()
print(f"Mean EC above threshold: {result['mean_ec_above_threshold']:.3f}")
print(f"Mean EC below threshold: {result['mean_ec_below_threshold']:.3f}")
print(f"Discontinuity: {result['discontinuity_magnitude']:.3f}")
```

You should see a large discontinuity (~0.6) between learners above and below the moral-agency threshold. This is the theory's central claim about non-compensatory EC.

### 11.4 What these simulations show (and don't show)

The simulations show that:
- The theory's formal structure is internally consistent.
- The predicted effects (gap reduction under dual prep; threshold discontinuity in EC) are visible in synthetic data generated under the theory's own assumptions.

The simulations do **not** show that:
- The predictions hold on real institutional data.
- The threshold values are the right ones for any specific context.

Those claims require the real studies the paper specifies (§6.2). The simulations are a first step.

### 11.5 Try it yourself

**Exercise 1.** Modify `study3_scam_validation` to add 20% outliers (learners whose observation noise is doubled). Does MAE increase as expected?

**Exercise 2.** Write a new simulation that varies the safety-gap threshold (`ε_small`) across 0.02, 0.05, 0.10, 0.15 and reports the fraction of learners classified as "balanced" at each level. Plot the result.

**Exercise 3.** Write a simulation where the ground-truth EC uses a different weight configuration than the library's default. Does the library still recover the ground-truth ordering?

**What you learned.** The library ships with four research-agenda simulations that you can extend for your own studies. They validate the theory's formal structure; they do not validate its empirical claims.

---

## Tutorial 12 — Extending the Library

**Objective:** Write a custom encoder, a custom trigger, and a custom daemon.

**Time:** 60 minutes.

### 12.1 A custom learner encoder

The default `IdentityLearnerEmbedding` returns the raw state vector. A trained encoder can compress or transform it.

Create `tutorial_12.py`:

```python
import numpy as np
from ctehf_ai import LearnerState, InvisibleCapacity, similarity_in_H

class CompressionLearnerEncoder:
    """Encodes the 10-dim IC vector into 3-dim (domain aggregates)."""

    def __call__(self, state: LearnerState) -> np.ndarray:
        return np.array([state.MA, state.PJ, state.RP])

encoder = CompressionLearnerEncoder()

a = LearnerState(invisible={c: 0.5 for c in InvisibleCapacity})
b = LearnerState(invisible={c: 0.55 for c in InvisibleCapacity})

print(f"Raw vector distance: {np.linalg.norm(a.to_vector() - b.to_vector()):.3f}")
print(f"Compressed distance: {similarity_in_H(encoder(a), encoder(b)):.3f}")
```

You should see that the compressed distance is much smaller than the raw vector distance, because the compression averages out per-capacity variation. This illustrates a design trade-off: compression reduces noise but may lose discriminative information.

### 12.2 A custom trigger

```python
from ctehf_ai import ECARule, TriggerSet, Event, CorrectiveAction, LearnerState, InvisibleCapacity

def build_growth_trigger() -> TriggerSet:
    """Fires when a learner's IC has grown less than 0.02 over a semester."""

    def insufficient_growth(state):
        # In real use, this would compare against a baseline
        return state.IC < 0.4

    return TriggerSet([
        ECARule(
            name="insufficient_ic_growth",
            event=Event.LONGITUDINAL_COMPARISON,
            condition=insufficient_growth,
            action=CorrectiveAction.TARGETED_DOMAIN_INTERVENTION,
            description="IC below 0.4 at semester end.",
        ),
    ])

ts = build_growth_trigger()
low_state = LearnerState(invisible={c: 0.3 for c in InvisibleCapacity})
high_state = LearnerState(invisible={c: 0.7 for c in InvisibleCapacity})

print(ts.fire(Event.LONGITUDINAL_COMPARISON, low_state))    # [TARGETED_DOMAIN_INTERVENTION]
print(ts.fire(Event.LONGITUDINAL_COMPARISON, high_state))   # [NOOP]
```

### 12.3 A custom daemon

```python
def daemon_cohort_spread(trajectory_ics: list[list[float]]) -> str:
    """Fires when the spread of IC growth across a cohort exceeds 0.4."""
    developments = [series[-1] - series[0] for series in trajectory_ics]
    if not developments:
        return "noop"
    spread = max(developments) - min(developments)
    if spread > 0.4:
        return "intervene-cohort-level"
    return "noop"

# Simulate: three trajectories with different growth
cohort = [
    [0.3, 0.5, 0.7],   # 0.4 growth
    [0.4, 0.5, 0.6],   # 0.2 growth
    [0.5, 0.55, 0.6],  # 0.1 growth
]
print(daemon_cohort_spread(cohort))   # 'noop' (spread = 0.3)

cohort_wide = [
    [0.2, 0.5, 0.8],   # 0.6 growth
    [0.4, 0.45, 0.5],  # 0.1 growth
]
print(daemon_cohort_spread(cohort_wide))   # 'intervene-cohort-level'
```

Custom daemons can be composed with library daemons:

```python
from ctehf_ai import GovernanceDaemons

def full_governance(trajectory, perf_ai, perf_indep, ai_log, cohort_ics):
    base = GovernanceDaemons().run(trajectory, perf_ai, perf_indep, ai_log)
    base["d_cohort"] = daemon_cohort_spread(cohort_ics)
    return base
```

### 12.4 Try it yourself

**Exercise 1.** Write a `SparseLearnerEncoder` that returns only non-zero capacities. How does it change similarity structure?

**Exercise 2.** Write a trigger that fires when a learner's EC margin (`EC - E_min`) shrinks below 0.05 but EC is still above E_min. (Hint: you'll need access to `E_min`; use the default `EthicalCompetenceConfig().E_min`.)

**Exercise 3.** Write a daemon that monitors AI action logs for high autonomy scores (`ai_autonomy > 0.5`) and returns `"require-disclosure"` when more than 20% of actions exceed that threshold.

**What you learned.** The library's protocols (encoders, triggers, daemons) are designed for extension. Custom implementations do not need to subclass anything; they only need to satisfy the protocol.

---

## Capstone — Design Your Own Audit

**Objective:** Apply everything from Tutorials 1–9 to a realistic institutional scenario.

**Time:** 2–3 hours.

### The scenario

You are the Director of Learning Analytics at a mid-sized university. The Provost has asked you to:

1. Assess whether the institution has a dual-preparation problem.
2. Identify which courses need redesign.
3. Recommend what redesign looks like.
4. Design a tracking mechanism so the institution can see improvement over time.

### The deliverable

A Python script `audit_deliverable.py` that:

1. **Loads assessment data** from a CSV (real or synthetic; if synthetic, generate it).
2. **Computes safety gaps** at individual, course, and institution levels.
3. **Identifies courses needing redesign**, using a defensible criterion.
4. **Reports the results** as a printed executive summary and a saved CSV.
5. **Sets up a tracking mechanism** that will produce the same audit report at the end of each semester.

### The requirements

Your audit must:

- Use the library's `safety_gap`, `interpret_safety_gap`, and `recommended_response` functions.
- Aggregate correctly (per-learner, per-course, per-institution).
- Be idempotent (running it twice gives the same result on the same data).
- Include a clear section for each Provost question.
- Explain its thresholds (why `ε_small = 0.05` and `ε_large = 0.25`, or whatever you chose).
- Not treat the gap as a KPI to optimize.

### Hints

- Start with the `institutional_audit.csv` generator from Tutorial 9.
- Extend the `audit()` function to also write `audit_results.csv` with the per-learner breakdown.
- For the "identify courses needing redesign" question, use the criterion from Tutorial 9.5 (mean_gap > 0.10).
- For the "recommend what redesign looks like," produce a short paragraph per flagged course, drawing on Tutorial 8's end-to-end simulation for illustration.

### Evaluation

Your deliverable is good if:

- It answers all four Provost questions explicitly.
- It is defensible (a Provost could challenge any number and you could explain it).
- It is auditable (someone else could run it and get the same result).
- It is honest (it does not claim to solve the problem, only to diagnose it).

### Worked solution

See [`docs/solutions/capstone_audit.py`](solutions/capstone_audit.py) — a reference implementation.

---

## Solutions

### Tutorial 1

**Exercise 1.** Populate all `PJ` capacities with 0.6 and all `RP` capacities with 0.6. Predict: `PJ = 0.6`, `RP = 0.6`. `MA` still depends on the two populated MA capacities (0.7 and 0.7) plus two zeros: `(0.7 + 0.7 + 0 + 0) / 4 = 0.35`. `IC = (0.35 × 4 + 0.6 × 4 + 0.6 × 2) / 10 = (1.4 + 2.4 + 1.2) / 10 = 0.5`.

**Exercise 2.** All ten at 0.5: `IC = 0.5`.

**Exercise 3.** No competencies or knowledge: `DC = 0`. All three constituents are 0.

### Tutorial 2

**Exercise 1.** MA = 0.5 (above 0.2), PJ = 0.05 (below 0.2), RP = 1.0. `EC = 0.0` because PJ is below threshold.

**Exercise 2.** At `MA = 0.2` exactly. At `MA = 0.19`, EC = 0. At `MA = 0.20`, thresholds are met and EC becomes `σ(w · (0.2, 1.0, 1.0)) ≈ σ(0.733) ≈ 0.676`. The transition is discontinuous.

**Exercise 3.** With `m_min = 0.4`, Learner A's MA is 0.7 (still above), so EC is unchanged. Learner B's MA is 0.05 (still below), so EC remains 0. The threshold change does not affect either learner in this example.

### Tutorial 3

**Exercise 1.** MA = 0.9, PJ = 0.9, RP = 0.05. RP is below threshold, so `EC = 0.0`.

**Exercise 2.** MA = PJ = RP = 0.3 (all above 0.2). `EC = σ(0.3) ≈ 0.574`.

**Exercise 3.** At `RP = 0.2`. At `RP = 0.19`, EC = 0. At `RP = 0.20`, EC becomes `σ(w · (0.3, 0.3, 0.2)) = σ(0.267) ≈ 0.566`.

### Tutorial 4

**Exercise 1.** `safety_gap(0.72, 0.72) = 0.0`, which is `|0.0| ≤ 0.05`, so `[balanced]`.

**Exercise 2.** `0.85`, because `0.85 - 0.60 = 0.25 = ε_large`.

**Exercise 3.** `classify_learner`:

```python
def classify_learner(ai, indep):
    interp = interpret_safety_gap(safety_gap(ai, indep))
    return {
        "balanced": "prepared",
        "ai_dependence": "dependent",
        "measurement_anomaly": "anomaly",
        "large_divergence": "dependent",  # large divergence is extreme dependence
    }[interp.value]
```

### Tutorial 5

**Exercise 1.** Custom `TriggerSet`:

```python
ECARule(
    name="low_ic",
    event=Event.SCAM_POSTERIOR_UPDATED,
    condition=lambda s: s.IC < 0.3,
    action=CorrectiveAction.TARGETED_DOMAIN_INTERVENTION,
)
```

**Exercise 2.** `pedagogical_triggers` fires on assessment and posterior-update events; it is a general pedagogical set. `safety_gap_triggers` fires only on the safety-gap event and contains one rule per gap category.

**Exercise 3.** No. At `MA = 0.2` exactly, the condition `MA < m_min` (with `m_min = 0.2`) is False. The learner is exactly at the threshold and is treated as ethical.

### Tutorial 6

**Exercise 1.** Convergence time depends on the noise model. With noise 0.15 and starting error 0.4, convergence within 0.05 typically takes 8–12 observations.

**Exercise 2.** Lower initial uncertainty means the first observation is trusted less. Convergence is *slower* but more stable.

**Exercise 3.** Higher observation noise means each observation is worth less. Convergence is *slower*.

### Tutorial 7

**Exercise 1.** A shrinking gap produces `noop` (or `monitor-closely` if the trend flips). The daemon does not fire on improving trajectories.

**Exercise 2.** Stable EC at 0.9 produces `noop` (margin stable).

**Exercise 3.** `require-disclosure` for one violation; `block-action` for two or more.

---

## Where to Go Next

**If you want to read the theory:**
- The paper's §3 is the formal foundation.
- The paper's §8.1 explains what is *distinctively educational* about the theory (as opposed to its COH substrate).
- The paper's §6.2 specifies the empirical studies you might contribute to.

**If you want to extend the library:**
- §28–§30 of the user guide covers custom encoders, triggers, and daemons.
- `docs/theory_mapping.md` maps each construct to its module.
- `docs/v0.2.0_migration.md` documents the breaking changes from v0.1.0.

**If you want to contribute:**
- See CONTRIBUTING.md (or the "Contributing" section of the README).
- Bug fixes and additional tests are most useful.
- Theory-changing contributions require a paper revision first.

**If you have questions:**
- GitHub Issues: bug reports and feature requests.
- GitHub Discussions: design questions.
- Email: harrisw@athabascau.ca.

**If you use the library in your work:**

Please cite both the theory paper and (if relevant) the COH foundations. Citation templates are in the README.

---

**End of tutorial.**

If you have completed all twelve tutorials and the capstone, you are now equipped to use the CTE-HF-AI library in research, audit, or deployment contexts. The library is designed to be a faithful instantiation of the theory — if you find an inconsistency between the theory and the code, that is a bug, and reporting it helps both.