"""End-to-end v0.2.0 integration test."""

from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    ethical_competence, educational_flourishing, total_flourishing,
    evaluate_success, safety_gap, interpret_safety_gap,
    check_fcp_compliance, FCPStatus, MultiAgentTutoringSystem,
    Event, CorrectiveAction, safety_gap_triggers,
    GovernanceDaemons,
)


def test_full_pipeline_v02():
    initial = LearnerState(
        competencies={"algorithmic_literacy": 0.3, "metacognition": 0.3},
        invisible={c: 0.4 for c in InvisibleCapacity},
    )
    final = LearnerState(
        competencies={"algorithmic_literacy": 0.7, "metacognition": 0.7},
        invisible={c: 0.75 for c in InvisibleCapacity},
    )
    assert ethical_competence(final) > 0.5
    assert total_flourishing(final, 0.05) > educational_flourishing(final)
    assert evaluate_success(initial, final, 0.85, 0.80).successful
    assert interpret_safety_gap(safety_gap(0.85, 0.80)).value == "balanced"
    assert check_fcp_compliance(final, 0.85, 0.80) == FCPStatus.COMPLIANT
    assert MultiAgentTutoringSystem().accountability_preserved()

    # New v0.2.0 integration: DC decomposition
    dc = final.DC_decomposed
    assert "DC" in dc and "DC_disc" in dc

    # New v0.2.0: trigger fires
    ts = safety_gap_triggers(0.90, 0.40)
    actions = ts.fire(Event.SAFETY_GAP_COMPUTED, final)
    assert CorrectiveAction.FLAG_FOR_PEDAGOGICAL_REVIEW in actions

    # New v0.2.0: daemons run
    g = GovernanceDaemons()
    result = g.run(
        trajectory=[initial, final],
        perf_ai_trajectory=[0.6, 0.85],
        perf_indep_trajectory=[0.55, 0.80],
        ai_action_log=[{"has_ai_free_alternative": True,
                         "under_human_review": True, "transparent": True}],
    )
    assert set(result.keys()) == {"d_dual_prep", "d_ethics", "d_transparency"}
