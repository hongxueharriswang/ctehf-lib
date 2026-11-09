"""Demonstrates the v0.2.0 additions aligned with the revised paper."""

from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    Event, CorrectiveAction,
    safety_gap_triggers, GovernanceDaemons,
    IdentityLearnerEmbedding, similarity_in_H, nearest_neighbours,
    empirical_lipschitz, check_theorem_3_1_assumptions,
    ethical_precision, variational_free_energy,
    PedagogicalAction, ActionType,
)
import numpy as np


def demo_dc():
    """DC three-constituent decomposition (§3.2.3)."""
    s = LearnerState(
        competencies={"algorithmic_literacy": 0.8, "ethical_judgment": 0.7},
        knowledge={"algebra": 0.6, "geometry": 0.7},
    )
    print("DC decomposition:", s.DC_decomposed)


def demo_triggers():
    """ECA trigger set for the safety gap (§3.8)."""
    ts = safety_gap_triggers(0.90, 0.40)
    s = LearnerState(invisible={c: 0.5 for c in InvisibleCapacity})
    actions = ts.fire(Event.SAFETY_GAP_COMPUTED, s)
    print("Triggered actions:", [a.value for a in actions])


def demo_daemons():
    """Governance trajectory daemons (§5)."""
    s = LearnerState(invisible={c: 0.8 for c in InvisibleCapacity})
    g = GovernanceDaemons()
    result = g.run(
        trajectory=[s, s, s],
        perf_ai_trajectory=[0.5, 0.6, 0.7],
        perf_indep_trajectory=[0.5, 0.5, 0.5],
        ai_action_log=[{"has_ai_free_alternative": True,
                         "under_human_review": True, "transparent": True}],
    )
    print("Daemon outputs:", result)


def demo_embeddings():
    """Embedding similarity retrieval (§3.2.2)."""
    emb = IdentityLearnerEmbedding()
    query = emb(LearnerState(invisible={c: 0.5 for c in InvisibleCapacity}))
    candidates = {
        "similar": emb(LearnerState(invisible={c: 0.52 for c in InvisibleCapacity})),
        "distant": emb(LearnerState(invisible={c: 0.9 for c in InvisibleCapacity})),
    }
    result = nearest_neighbours(query, candidates, delta=0.2)
    print("Similarity retrieval:", result)


def demo_hybrid():
    """Hybrid dynamics and Theorem 3.1 assumptions (§3.9)."""
    def linear_f(s_vec, action, params):
        return 0.05 * np.ones_like(s_vec)
    pts = [np.zeros(5), np.ones(5), 0.5 * np.ones(5)]
    L = empirical_lipschitz(lambda x: 2 * x, pts)
    print(f"Empirical Lipschitz constant: {L:.3f}")
    status = check_theorem_3_1_assumptions(L, 1.0, True)
    print("Theorem 3.1 applies:", status["theorem_3_1_applies"])


def demo_free_energy():
    """Free-energy precision and variational bound (§4.2.1)."""
    s = LearnerState(invisible={
        InvisibleCapacity.MORAL_RESPONSIBILITY: 0.1,
        InvisibleCapacity.ETHICAL_COMMITMENT: 0.1,
        InvisibleCapacity.CONSCIENCE: 0.1,
        InvisibleCapacity.HUMILITY: 0.1,
        InvisibleCapacity.WISDOM: 0.8,
        InvisibleCapacity.MEANING_MAKING: 0.8,
        InvisibleCapacity.PURPOSE: 0.8,
        InvisibleCapacity.EXISTENTIAL_COURAGE: 0.8,
        InvisibleCapacity.LOVE: 0.8,
        InvisibleCapacity.EMPATHIC_PRESENCE: 0.8,
    })
    print("Ethical precisions:", ethical_precision(s))
    q = np.full(5, 0.5)
    x = np.full(5, 0.6)
    print(f"Variational free energy: {variational_free_energy(q, x):.3f}")


def main():
    print("=" * 60); print("DC decomposition (3.2.3)"); demo_dc()
    print("=" * 60); print("ECA triggers (3.8)"); demo_triggers()
    print("=" * 60); print("Governance daemons (5)"); demo_daemons()
    print("=" * 60); print("Embeddings (3.2.2)"); demo_embeddings()
    print("=" * 60); print("Hybrid dynamics (3.9)"); demo_hybrid()
    print("=" * 60); print("Free-energy precision (4.2.1)"); demo_free_energy()


if __name__ == "__main__":
    main()
