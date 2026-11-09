"""Tests for capacities, state, COH, trajectories, and FCP (consolidated)."""

import pytest
import numpy as np
from ctehf_ai import (
    InvisibleCapacity, Domain, ALL_INVISIBLE_CAPACITIES,
    LearnerState, COHObject, ConstraintDaemon, ConstraintHierarchy,
    PedagogicalAction, ActionType, TransitionFunction, TrajectoryOptimizer,
    FCPStatus, check_fcp_compliance,
)


def test_ten_capacities():
    assert len(ALL_INVISIBLE_CAPACITIES) == 10


def test_state_initialization():
    s = LearnerState()
    assert len(s.invisible) == 10


def test_state_clips():
    s = LearnerState(invisible={InvisibleCapacity.WISDOM: 1.5,
                                 InvisibleCapacity.LOVE: -0.3})
    assert s.invisible[InvisibleCapacity.WISDOM] == 1.0
    assert s.invisible[InvisibleCapacity.LOVE] == 0.0


def test_ic_normalized():
    s = LearnerState(invisible={c: 0.5 for c in InvisibleCapacity})
    assert 0 <= s.IC <= 1
    assert s.IC == pytest.approx(0.5)


def test_coh_hierarchy():
    h = ConstraintHierarchy()
    h.register(COHObject(name="root", level=0))
    h.register(COHObject(name="child", level=1, parent="root"))
    assert h.root.name == "root"
    assert "child" in h.get("root").children


def test_coh_daemon_violation():
    h = ConstraintHierarchy()
    h.register(COHObject(name="root", level=0,
                          daemons=[ConstraintDaemon("pos", lambda s: s > 0)]))
    assert len(h.enforce_all(-1)) == 1
    assert len(h.enforce_all(1)) == 0


def test_transition_increases_target():
    s = LearnerState(invisible={c: 0.3 for c in InvisibleCapacity})
    a = PedagogicalAction(action_type=ActionType.SCAFFOLD,
                           target=InvisibleCapacity.WISDOM.value, intensity=1.0)
    s2 = TransitionFunction()(s, a)
    assert s2.invisible[InvisibleCapacity.WISDOM] > 0.3


def test_trajectory_optimizer():
    s = LearnerState(invisible={c: 0.3 for c in InvisibleCapacity})
    pool = [PedagogicalAction(action_type=ActionType.SCAFFOLD,
                               target=InvisibleCapacity.WISDOM.value, intensity=1.0)]
    traj = TrajectoryOptimizer(action_pool=pool).greedy_optimize(s, horizon=5)
    assert traj.length == 5
    assert traj.final.IC >= traj.initial.IC


def test_fcp_compliant():
    s = LearnerState(invisible={c: 0.8 for c in InvisibleCapacity})
    assert check_fcp_compliance(s, 0.9, 0.85) == FCPStatus.COMPLIANT


def test_fcp_ethical_violation():
    s = LearnerState(invisible={c: 0.1 for c in InvisibleCapacity})
    assert check_fcp_compliance(s, 0.9, 0.85) == FCPStatus.ETHICAL_VIOLATED
