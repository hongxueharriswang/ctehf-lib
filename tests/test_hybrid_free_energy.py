"""Tests for hybrid dynamics and free-energy (Sections 3.9, 4.2.1)."""

import numpy as np
import pytest
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    HybridDynamics, TransitionFunction, empirical_lipschitz,
    check_theorem_3_1_assumptions,
    PrecisionPrior, ethical_precision, variational_free_energy,
    PedagogicalAction, ActionType,
    EthicalCompetenceConfig,
)


def _state(level=0.5):
    return LearnerState(invisible={c: level for c in InvisibleCapacity})


def test_hybrid_continuous_evolve():
    def f(s_vec, action, params):
        return 0.1 * np.ones_like(s_vec)
    dyn = HybridDynamics(
        continuous_f=f,
        discrete_g=TransitionFunction(),
        trigger_condition=lambda s: False,
    )
    s2 = dyn.evolve_continuous(_state(0.5), PedagogicalAction(
        action_type=ActionType.REFLECT), steps=5)
    assert s2.invisible[InvisibleCapacity.WISDOM] >= 0.5


def test_empirical_lipschitz_linear():
    fn = lambda x: 2 * x
    pts = [np.array([0.0, 0.0]), np.array([1.0, 1.0]), np.array([0.5, 0.5])]
    L = empirical_lipschitz(fn, pts)
    assert L == pytest.approx(2.0, abs=0.1)


def test_theorem_3_1_check():
    ok = check_theorem_3_1_assumptions(1.0, 1.0, True)
    assert ok["theorem_3_1_applies"] is True
    bad = check_theorem_3_1_assumptions(float("inf"), 1.0, True)
    assert bad["theorem_3_1_applies"] is False


def test_precision_prior_above_threshold():
    p = PrecisionPrior(threshold=0.3, penalty_precision=100.0)
    assert p.precision(0.5) == 1.0


def test_precision_prior_below_threshold():
    p = PrecisionPrior(threshold=0.3, penalty_precision=100.0)
    assert p.precision(0.1) == 100.0


def test_ethical_precision_returns_three():
    result = ethical_precision(_state(0.5))
    assert set(result.keys()) == {"MA", "PJ", "RP"}


def test_variational_free_energy_bounded():
    q = np.array([0.5, 0.5, 0.5])
    x = np.array([0.5, 0.5, 0.5])
    fe = variational_free_energy(q, x)
    assert np.isfinite(fe)
