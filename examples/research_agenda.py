"""Four research-agenda simulations (Section 6.2)."""

from ctehf_ai.experiments import (
    study1_safety_gap, study2_dual_prep,
    study3_scam_validation, study4_threshold_effects,
)


def main():
    print("Study 1:", study1_safety_gap())
    print("Study 2:", study2_dual_prep())
    print("Study 3:", study3_scam_validation())
    print("Study 4:", study4_threshold_effects())


if __name__ == "__main__":
    main()
