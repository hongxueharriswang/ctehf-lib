"""Two-register flourishing model (Section 3.4.2)."""

from dataclasses import dataclass
from typing import Optional
import numpy as np

from .state import LearnerState
from .ethical import EthicalCompetenceConfig, ethical_competence


@dataclass
class FlourishingConfig:
    w_EC: float = 1.0 / 3.0
    w_IC: float = 1.0 / 3.0
    w_DC: float = 1.0 / 3.0

    def __post_init__(self) -> None:
        total = self.w_EC + self.w_IC + self.w_DC
        if not np.isclose(total, 1.0):
            raise ValueError(f"Flourishing weights must sum to 1 (got {total})")


def educational_flourishing(
    state: LearnerState,
    ethical_config: Optional[EthicalCompetenceConfig] = None,
    flourishing_config: Optional[FlourishingConfig] = None,
) -> float:
    ethical_config = ethical_config or EthicalCompetenceConfig()
    flourishing_config = flourishing_config or FlourishingConfig()
    ec = ethical_competence(state, ethical_config)
    return float(
        flourishing_config.w_EC * ec
        + flourishing_config.w_IC * state.IC
        + flourishing_config.w_DC * state.DC
    )


def total_flourishing(
    state: LearnerState,
    external_epsilon: float = 0.0,
    ethical_config: Optional[EthicalCompetenceConfig] = None,
    flourishing_config: Optional[FlourishingConfig] = None,
) -> float:
    return float(educational_flourishing(state, ethical_config, flourishing_config)
                 + external_epsilon)
