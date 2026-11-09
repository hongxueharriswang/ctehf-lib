"""Tests for success and safety gap (Sections 3.7, 6.1)."""

import pytest
from ctehf_ai import (
    LearnerState, InvisibleCapacity, evaluate_success,
    safety_gap, interpret_safety_gap, SafetyGapInterpretation,
)


def _state(level):
    return LearnerState(invisible={c: level for c in InvisibleCapacity})


def test_successful():
    r = evaluate_success(_state(0.3), _state(0.7), 0.8, 0.7)
    assert r.successful


def test_failed_dual_prep():
    r = evaluate_success(_state(0.3), _state(0.7), 0.8, 0.2)
    assert not r.successful
    assert not r.dual_preparation_satisfied


def test_temporary_regression_tolerated():
    initial = _state(0.5)
    final_inv = {c: 0.7 for c in InvisibleCapacity}
    final_inv[InvisibleCapacity.PURPOSE] = 0.48
    final = LearnerState(invisible=final_inv)
    r = evaluate_success(initial, final, 0.8, 0.8)
    assert r.no_critical_regression


def test_gap_value():
    assert safety_gap(0.8, 0.5) == pytest.approx(0.3)


def test_interpretations():
    assert interpret_safety_gap(0.0) == SafetyGapInterpretation.BALANCED
    assert interpret_safety_gap(0.1) == SafetyGapInterpretation.AI_DEPENDENCE
    assert interpret_safety_gap(-0.1) == SafetyGapInterpretation.MEASUREMENT_ANOMALY
    assert interpret_safety_gap(0.5) == SafetyGapInterpretation.LARGE_DIVERGENCE
