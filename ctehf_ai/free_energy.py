"""Free-energy correspondence for SCAM (Section 4.2.1, Theorem 4.1)."""

from dataclasses import dataclass
from typing import Optional
import numpy as np

from .state import LearnerState
from .ethical import EthicalCompetenceConfig


@dataclass
class PrecisionPrior:
    base_precision: float = 1.0
    threshold: float = 0.2
    penalty_precision: float = 100.0

    def precision(self, value: float) -> float:
        if value < self.threshold:
            return self.penalty_precision
        return self.base_precision


def ethical_precision(
    state: LearnerState,
    config: Optional[EthicalCompetenceConfig] = None,
) -> dict:
    config = config or EthicalCompetenceConfig()
    return {
        "MA": PrecisionPrior(
            threshold=config.m_min, penalty_precision=100.0).precision(state.MA),
        "PJ": PrecisionPrior(
            threshold=config.p_min, penalty_precision=100.0).precision(state.PJ),
        "RP": PrecisionPrior(
            threshold=config.r_min, penalty_precision=100.0).precision(state.RP),
    }


def variational_free_energy(
    q_state: np.ndarray, observation: np.ndarray,
    observation_noise: float = 0.1,
) -> float:
    eps = 1e-9
    q = np.clip(q_state, eps, 1.0 - eps)
    entropy = -np.sum(q * np.log(q) + (1 - q) * np.log(1 - q))
    log_lik = -np.sum((observation - q_state) ** 2 / (2 * observation_noise ** 2))
    return float(-entropy - log_lik)
