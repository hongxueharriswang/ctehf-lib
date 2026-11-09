"""Non-compensatory ethical competence EC(s) (Section 3.3).

Note on terminology (Section 3.2.3): the *competency* "ethical_judgment"
(part of DC_comp) and the *construct* EC are distinct. The competency is a
deliberative skill; the construct is the integrative determinant subject to
non-compensatory thresholds.
"""

from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np
from scipy.special import expit

from .state import LearnerState


@dataclass
class EthicalCompetenceConfig:
    w_MA: float = 1.0 / 3.0
    w_PJ: float = 1.0 / 3.0
    w_RP: float = 1.0 / 3.0
    m_min: float = 0.2
    p_min: float = 0.2
    r_min: float = 0.2
    E_min: float = 0.5
    gamma: float = 0.0

    def __post_init__(self) -> None:
        total = self.w_MA + self.w_PJ + self.w_RP
        if not np.isclose(total, 1.0):
            raise ValueError(f"Domain weights must sum to 1 (got {total})")
        if min(self.w_MA, self.w_PJ, self.w_RP) < 0:
            raise ValueError("Weights must be non-negative")
        if not (0.0 <= self.gamma < self.E_min):
            raise ValueError(
                f"gamma must satisfy 0 <= gamma < E_min (got {self.gamma})"
            )


def ethical_competence(
    state: LearnerState,
    config: EthicalCompetenceConfig = EthicalCompetenceConfig(),
) -> float:
    ma, pj, rp = state.MA, state.PJ, state.RP
    linear = config.w_MA * ma + config.w_PJ * pj + config.w_RP * rp
    base = float(expit(linear))
    thresholds_met = (ma >= config.m_min and pj >= config.p_min
                      and rp >= config.r_min)
    return base if thresholds_met else config.gamma * base


def ethical_competence_via_precision(
    state: LearnerState,
    config: Optional[EthicalCompetenceConfig] = None,
) -> float:
    """Free-energy interpretation of the threshold-gated EC (Theorem 4.1).

    When a domain falls below its threshold, its precision becomes large,
    pushing the posterior into the penalty region. Functionally equivalent
    to ethical_competence() in the conjugate case; differs under amortization.
    """
    config = config or EthicalCompetenceConfig()
    ma, pj, rp = state.MA, state.PJ, state.RP
    from .free_energy import ethical_precision
    precisions = ethical_precision(state, config)
    linear = config.w_MA * ma + config.w_PJ * pj + config.w_RP * rp
    weights = []
    for name, val, thr in (("MA", ma, config.m_min),
                            ("PJ", pj, config.p_min),
                            ("RP", rp, config.r_min)):
        weights.append(1.0 / precisions[name] if val < thr else 1.0)
    effective = linear * min(weights)
    base = float(expit(effective))
    if any(v < t for v, t in ((ma, config.m_min), (pj, config.p_min),
                                (rp, config.r_min))):
        return config.gamma * base
    return base


def is_ethical_threshold_satisfied(
    state: LearnerState,
    config: EthicalCompetenceConfig = EthicalCompetenceConfig(),
) -> bool:
    return ethical_competence(state, config) >= config.E_min


def ethical_competence_decomposed(
    state: LearnerState,
    config: EthicalCompetenceConfig = EthicalCompetenceConfig(),
) -> Dict[str, float]:
    ma, pj, rp = state.MA, state.PJ, state.RP
    linear = config.w_MA * ma + config.w_PJ * pj + config.w_RP * rp
    base = float(expit(linear))
    thresholds_met = (ma >= config.m_min and pj >= config.p_min
                      and rp >= config.r_min)
    return {
        "MA": ma, "PJ": pj, "RP": rp,
        "MA_threshold": config.m_min, "PJ_threshold": config.p_min,
        "RP_threshold": config.r_min,
        "thresholds_met": float(thresholds_met),
        "base_sigma": base,
        "EC": ethical_competence(state, config),
        "E_min": config.E_min,
    }
