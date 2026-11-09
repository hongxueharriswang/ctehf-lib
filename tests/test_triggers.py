"""Tests for ECA trigger sets (Section 3.8)."""

from ctehf_ai import (
    LearnerState, InvisibleCapacity, Event, CorrectiveAction,
    TriggerSet, pedagogical_triggers, safety_gap_triggers,
)


def _state(level=0.5):
    return LearnerState(invisible={c: level for c in InvisibleCapacity})


def test_pedagogical_triggers_ai_dependence():
    ts = pedagogical_triggers(perf_ai=0.8, perf_indep=0.5)
    actions = ts.fire(Event.ASSESSMENT_COMPLETED, _state())
    assert CorrectiveAction.INCREASE_AI_FREE_PRACTICE in actions


def test_pedagogical_triggers_no_fire_when_ok():
    ts = pedagogical_triggers(perf_ai=0.5, perf_indep=0.5)
    actions = ts.fire(Event.ASSESSMENT_COMPLETED, _state(0.5))
    assert actions == [CorrectiveAction.NOOP]


def test_pedagogical_ethical_threshold():
    ts = pedagogical_triggers(0.5, 0.5, m_min=0.3)
    low = LearnerState(invisible={c: 0.1 for c in InvisibleCapacity})
    actions = ts.fire(Event.SCAM_POSTERIOR_UPDATED, low)
    assert CorrectiveAction.FLAG_MORAL_FORMATION in actions


def test_safety_gap_rules():
    balanced = safety_gap_triggers(0.75, 0.73)
    assert CorrectiveAction.SUSTAIN_AND_MONITOR in balanced.fire(
        Event.SAFETY_GAP_COMPUTED, _state())

    ai_dep = safety_gap_triggers(0.85, 0.70)
    assert CorrectiveAction.INCREASE_AI_FREE_PRACTICE in ai_dep.fire(
        Event.SAFETY_GAP_COMPUTED, _state())

    anomaly = safety_gap_triggers(0.60, 0.75)
    assert CorrectiveAction.INVESTIGATE_ANOMALY in anomaly.fire(
        Event.SAFETY_GAP_COMPUTED, _state())

    large = safety_gap_triggers(0.90, 0.40)
    assert CorrectiveAction.FLAG_FOR_PEDAGOGICAL_REVIEW in large.fire(
        Event.SAFETY_GAP_COMPUTED, _state())


def test_trigger_set_rules_accessible():
    ts = safety_gap_triggers(0.9, 0.4)
    assert len(ts.rules) == 4
