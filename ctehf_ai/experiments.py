"""Four research-agenda studies (Section 6.2)."""

from typing import Dict
import numpy as np

from .state import LearnerState
from .capacities import InvisibleCapacity
from .safety_gap import safety_gap, interpret_safety_gap
from .ethical import EthicalCompetenceConfig, ethical_competence


def _random_state(rng, base=0.3):
    return LearnerState(
        competencies={
            "algorithmic_literacy": base + rng.uniform(-0.1, 0.1),
            "metacognition": base + rng.uniform(-0.1, 0.1),
        },
        invisible={c: float(np.clip(base + rng.uniform(-0.15, 0.15), 0, 1))
                   for c in InvisibleCapacity},
    )


def study1_safety_gap(n_learners=100, seed=42):
    rng = np.random.default_rng(seed)
    gaps, interps = [], {}
    for _ in range(n_learners):
        base = float(rng.uniform(0.4, 0.9))
        ai = float(np.clip(base + rng.normal(0.15, 0.1), 0, 1))
        ind = float(np.clip(base + rng.normal(0.0, 0.1), 0, 1))
        g = safety_gap(ai, ind)
        gaps.append(g)
        i = interpret_safety_gap(g)
        interps[i.value] = interps.get(i.value, 0) + 1
    return {"mean_gap": float(np.mean(gaps)),
            "std_gap": float(np.std(gaps)),
            "interpretations": interps}


def study2_dual_prep(n_learners=50, seed=42):
    rng = np.random.default_rng(seed)
    def run(dual):
        gaps = []
        for _ in range(n_learners):
            base = float(rng.uniform(0.5, 0.8))
            if dual:
                ai = base + rng.normal(0.1, 0.05)
                ind = base + rng.normal(0.08, 0.05)
            else:
                ai = base + rng.normal(0.2, 0.05)
                ind = base + rng.normal(-0.05, 0.05)
            gaps.append(safety_gap(float(np.clip(ai, 0, 1)),
                                   float(np.clip(ind, 0, 1))))
        return float(np.mean(gaps))
    return {"dual_prep_mean_gap": run(True),
            "ai_dependent_mean_gap": run(False)}


def study3_scam_validation(n_learners=30, seed=42):
    from .scam import SCAMModel
    rng = np.random.default_rng(seed)
    errors = []
    for _ in range(n_learners):
        true = _random_state(rng, base=0.5)
        m = SCAMModel(true)
        for _ in range(10):
            noisy = np.clip(true.to_vector() + rng.normal(0, 0.15, len(true.to_vector())), 0, 1)
            m.predict(); m.update(noisy)
        errors.append(abs(m.posterior_state.IC - true.IC))
    return {"mean_absolute_error": float(np.mean(errors)),
            "max_error": float(np.max(errors))}


def study4_threshold_effects(seed=42):
    config = EthicalCompetenceConfig(m_min=0.3)
    above, below = [], []
    for ma in np.linspace(0.0, 1.0, 50):
        s = LearnerState(invisible={
            InvisibleCapacity.MORAL_RESPONSIBILITY: ma,
            InvisibleCapacity.ETHICAL_COMMITMENT: ma,
            InvisibleCapacity.CONSCIENCE: ma,
            InvisibleCapacity.HUMILITY: ma,
            InvisibleCapacity.WISDOM: 0.7,
            InvisibleCapacity.MEANING_MAKING: 0.7,
            InvisibleCapacity.PURPOSE: 0.7,
            InvisibleCapacity.EXISTENTIAL_COURAGE: 0.7,
            InvisibleCapacity.LOVE: 0.7,
            InvisibleCapacity.EMPATHIC_PRESENCE: 0.7,
        })
        ec = ethical_competence(s, config)
        (above if ma >= config.m_min else below).append(ec)
    return {"mean_ec_above_threshold": float(np.mean(above)),
            "mean_ec_below_threshold": float(np.mean(below)),
            "discontinuity_magnitude": float(np.mean(above) - np.mean(below))}
