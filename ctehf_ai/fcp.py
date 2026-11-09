"""Flourishing-Competence-Preparation Principle (Sections 1.1, 3.4.1)."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional

from .state import LearnerState
from .ethical import EthicalCompetenceConfig, ethical_competence
from .safety_gap import safety_gap


class FCPStatus(Enum):
    COMPLIANT = "compliant"
    ETHICAL_VIOLATED = "ethical_violated"
    PREPARATION_VIOLATED = "preparation_violated"


@dataclass
class FCPPrinciple:
    ethical_config: EthicalCompetenceConfig = field(
        default_factory=EthicalCompetenceConfig)
    theta_collab: float = 0.5
    theta_indep: float = 0.5
    max_safety_gap: float = 0.2


def check_fcp_compliance(
    state: LearnerState, perf_ai: float, perf_indep: float,
    principle: Optional[FCPPrinciple] = None,
) -> FCPStatus:
    principle = principle or FCPPrinciple()
    if ethical_competence(state, principle.ethical_config) < principle.ethical_config.E_min:
        return FCPStatus.ETHICAL_VIOLATED
    gap = safety_gap(perf_ai, perf_indep)
    if gap > principle.max_safety_gap:
        return FCPStatus.PREPARATION_VIOLATED
    if perf_ai < principle.theta_collab or perf_indep < principle.theta_indep:
        return FCPStatus.PREPARATION_VIOLATED
    return FCPStatus.COMPLIANT
