"""Tests for governance daemons (Section 5)."""

import pytest
from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    GovernanceDaemons, daemon_dual_prep, daemon_ethics, daemon_transparency,
)


def _state(level=0.7):
    return LearnerState(invisible={c: level for c in InvisibleCapacity})


def test_dual_prep_noop_when_balanced():
    traj = [_state(0.7)] * 5
    ai = [0.75] * 5
    ind = [0.74] * 5
    assert daemon_dual_prep(traj, ai, ind) == "noop"


def test_dual_prep_fires_on_ai_dependence():
    traj = [_state(0.7)] * 5
    ai = [0.5, 0.6, 0.7, 0.8, 0.9]
    ind = [0.5] * 5
    assert daemon_dual_prep(traj, ai, ind) == "increase-ai-free-practice"


def test_dual_prep_anomaly():
    traj = [_state(0.7)] * 5
    ai = [0.4] * 5
    ind = [0.7] * 5
    assert daemon_dual_prep(traj, ai, ind) == "investigate-anomaly"


def test_ethics_noop_when_above():
    traj = [_state(0.8)] * 5
    assert daemon_ethics(traj) == "noop"


def test_ethics_halt_when_below():
    traj = [_state(0.1)] * 5
    assert daemon_ethics(traj) == "halt-and-remediate"


def test_transparency_noop():
    assert daemon_transparency([{"has_ai_free_alternative": True,
                                  "under_human_review": True,
                                  "transparent": True}]) == "noop"


def test_transparency_block():
    bad = [{"has_ai_free_alternative": False,
            "under_human_review": True,
            "transparent": True}] * 3
    assert daemon_transparency(bad) == "block-action"


def test_governance_daemons_run():
    g = GovernanceDaemons()
    result = g.run(
        trajectory=[_state(0.8)] * 3,
        perf_ai_trajectory=[0.75, 0.76, 0.77],
        perf_indep_trajectory=[0.74, 0.75, 0.76],
        ai_action_log=[{"has_ai_free_alternative": True,
                         "under_human_review": True,
                         "transparent": True}],
    )
    assert set(result.keys()) == {"d_dual_prep", "d_ethics", "d_transparency"}
