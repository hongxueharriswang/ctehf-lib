"""Basic usage: state, EC, HF, and safety gap."""

from ctehf_ai import (
    LearnerState, InvisibleCapacity,
    ethical_competence, educational_flourishing,
    safety_gap, interpret_safety_gap,
)


def main():
    s = LearnerState(
        competencies={"algorithmic_literacy": 0.7, "metacognition": 0.6},
        knowledge={"domain_knowledge": 0.7},
        invisible={c: 0.7 for c in InvisibleCapacity},
    )
    print(f"MA  = {s.MA:.3f}")
    print(f"PJ  = {s.PJ:.3f}")
    print(f"RP  = {s.RP:.3f}")
    print(f"IC  = {s.IC:.3f}")
    print(f"DC  = {s.DC:.3f}")
    print(f"EC  = {ethical_competence(s):.3f}")
    print(f"HF_ed = {educational_flourishing(s):.3f}")

    gap = safety_gap(0.85, 0.55)
    print(f"\nSafety gap = {gap:.3f}")
    print(f"Interpretation: {interpret_safety_gap(gap).value}")


if __name__ == "__main__":
    main()
