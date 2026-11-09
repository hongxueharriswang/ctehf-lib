"""SCAM over noisy observations."""

import numpy as np
from ctehf_ai import LearnerState, InvisibleCapacity, SCAMModel, ethical_competence


def main():
    rng = np.random.default_rng(0)
    true = LearnerState(invisible={c: 0.7 for c in InvisibleCapacity})
    m = SCAMModel(true)
    n = len(true.to_vector())
    for t in range(10):
        noisy = np.clip(true.to_vector() + rng.normal(0, 0.2, n), 0, 1)
        m.predict(); m.update(noisy)
        point, unc = m.ic_estimate()
        print(f"t={t+1:2d} IC={point:.3f} ± {unc:.3f} EC={ethical_competence(m.posterior_state):.3f}")


if __name__ == "__main__":
    main()
