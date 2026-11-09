"""Domain Competence DC(s) as three-constituent composite (Section 3.2.3).

DC is fully compensatory (unlike EC, which is non-compensatory) because
disciplinary mastery, professional performance, and transferable competencies
are genuinely substitutable for a given domain outcome.
"""

from dataclasses import dataclass
from typing import Dict, Optional
import numpy as np

from .state import COMPETENCIES


@dataclass
class DCConfig:
    w_disc: float = 1.0 / 3.0
    w_prof: float = 1.0 / 3.0
    w_comp: float = 1.0 / 3.0

    def __post_init__(self) -> None:
        total = self.w_disc + self.w_prof + self.w_comp
        if not np.isclose(total, 1.0):
            raise ValueError(f"DC weights must sum to 1 (got {total})")
        if min(self.w_disc, self.w_prof, self.w_comp) < 0:
            raise ValueError("DC weights must be non-negative")


def disciplinary_mastery(knowledge: Dict[str, float]) -> float:
    return float(np.mean(list(knowledge.values()))) if knowledge else 0.0


def professional_performance(
    knowledge: Dict[str, float], competencies: Dict[str, float]
) -> float:
    if not knowledge and not competencies:
        return 0.0
    k = np.mean(list(knowledge.values())) if knowledge else 0.0
    c = np.mean(list(competencies.values())) if competencies else 0.0
    return float((k + c) / 2.0)


def transferable_competencies(competencies: Dict[str, float]) -> float:
    relevant = {k: v for k, v in competencies.items() if k in COMPETENCIES}
    return float(np.mean(list(relevant.values()))) if relevant else 0.0


def domain_competence(
    competencies: Dict[str, float],
    knowledge: Dict[str, float],
    config: Optional[DCConfig] = None,
) -> float:
    config = config or DCConfig()
    return float(
        config.w_disc * disciplinary_mastery(knowledge)
        + config.w_prof * professional_performance(knowledge, competencies)
        + config.w_comp * transferable_competencies(competencies)
    )


def dc_decomposed(
    competencies: Dict[str, float],
    knowledge: Dict[str, float],
    config: Optional[DCConfig] = None,
) -> Dict[str, float]:
    config = config or DCConfig()
    return {
        "DC_disc": disciplinary_mastery(knowledge),
        "DC_prof": professional_performance(knowledge, competencies),
        "DC_comp": transferable_competencies(competencies),
        "w_disc": config.w_disc,
        "w_prof": config.w_prof,
        "w_comp": config.w_comp,
        "DC": domain_competence(competencies, knowledge, config),
    }
