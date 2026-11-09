"""Tests for EC and flourishing (Sections 3.3, 3.4.2)."""

import pytest
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    EthicalCompetenceConfig, ethical_competence,
    ethical_competence_via_precision,
    educational_flourishing, total_flourishing,
)


def _full(level=0.7):
    return LearnerState(
        competencies={"algorithmic_literacy": level, "metacognition": level},
        knowledge={"k": level},
        invisible={c: level for c in InvisibleCapacity},
    )


def test_high_ma_above_threshold():
    s = _full(0.7)
    assert ethical_competence(s) > 0.5


def test_low_ma_penalized():
    s = LearnerState(invisible={
        InvisibleCapacity.MORAL_RESPONSIBILITY: 0.05,
        InvisibleCapacity.ETHICAL_COMMITMENT: 0.05,
        InvisibleCapacity.CONSCIENCE: 0.05,
        InvisibleCapacity.HUMILITY: 0.05,
        InvisibleCapacity.WISDOM: 1.0,
        InvisibleCapacity.MEANING_MAKING: 1.0,
        InvisibleCapacity.PURPOSE: 1.0,
        InvisibleCapacity.EXISTENTIAL_COURAGE: 1.0,
        InvisibleCapacity.LOVE: 1.0,
        InvisibleCapacity.EMPATHIC_PRESENCE: 1.0,
    })
    assert ethical_competence(s) < 0.5


def test_weights_validation():
    with pytest.raises(ValueError):
        EthicalCompetenceConfig(w_MA=0.5, w_PJ=0.5, w_RP=0.5)


def test_precision_agrees_when_above_threshold():
    s = _full(0.7)
    assert ethical_competence(s) == pytest.approx(
        ethical_competence_via_precision(s), abs=0.3)


def test_hf_educational_bounded():
    assert 0 <= educational_flourishing(_full(0.7)) <= 1


def test_hf_total_includes_epsilon():
    s = _full(0.7)
    assert total_flourishing(s, 0.1) == pytest.approx(educational_flourishing(s) + 0.1)
