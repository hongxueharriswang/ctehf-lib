"""Tests for DC three-constituent decomposition (Section 3.2.3)."""

import pytest
from ctehf_ai import (
    LearnerState, DCConfig, disciplinary_mastery, professional_performance,
    transferable_competencies, domain_competence, dc_decomposed,
)


def test_disciplinary_mastery():
    assert disciplinary_mastery({"a": 0.5, "b": 0.7}) == pytest.approx(0.6)
    assert disciplinary_mastery({}) == 0.0


def test_professional_performance():
    assert professional_performance({}, {}) == 0.0
    assert professional_performance({"a": 0.6}, {"b": 0.4}) == pytest.approx(0.5)


def test_transferable_competencies():
    # Only recognized competencies count
    comps = {"algorithmic_literacy": 0.6, "not_a_competency": 1.0}
    assert transferable_competencies(comps) == pytest.approx(0.6)


def test_domain_competence_full():
    dc = domain_competence({"algorithmic_literacy": 0.7}, {"k": 0.5})
    assert 0 <= dc <= 1


def test_dc_config_validation():
    with pytest.raises(ValueError):
        DCConfig(w_disc=0.5, w_prof=0.5, w_comp=0.5)


def test_dc_decomposed_keys():
    d = dc_decomposed({"algorithmic_literacy": 0.6}, {"k": 0.8})
    for key in ("DC_disc", "DC_prof", "DC_comp", "DC", "w_disc", "w_prof", "w_comp"):
        assert key in d


def test_learner_state_dc_decomposed():
    s = LearnerState(competencies={"algorithmic_literacy": 0.7},
                     knowledge={"k": 0.5})
    d = s.DC_decomposed
    assert "DC" in d
    assert d["DC"] == pytest.approx(s.DC)


def test_ethical_judgment_competency_vs_ec_construct():
    """Per §3.2.3: 'ethical_judgment' is a competency (DC_comp);
    EC is a separate integrative construct with thresholds."""
    from ctehf_ai import ethical_competence
    s = LearnerState(
        competencies={"ethical_judgment": 0.9},
        invisible={c: 0.05 for c in __import__("ctehf_ai").InvisibleCapacity},
    )
    assert s.DC > 0  # competency contributes to DC
    assert ethical_competence(s) < 0.5  # but EC fails threshold
