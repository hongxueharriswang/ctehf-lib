"""Trigger constraints T as ECA rules (Section 3.8).

T = {(e_i, c_i, a_i) | e_i in E, c_i: S -> B, a_i in A_act}

Two sets: T_ped (pedagogical) and T_safety (safety-gap, Table 2).
"""

from dataclasses import dataclass
from enum import Enum
from typing import Callable, List, Optional

from .state import LearnerState


class Event(Enum):
    ASSESSMENT_COMPLETED = "assessment_completed"
    SCAM_POSTERIOR_UPDATED = "scam_posterior_updated"
    LONGITUDINAL_COMPARISON = "longitudinal_comparison"
    SAFETY_GAP_COMPUTED = "safety_gap_computed"


class CorrectiveAction(Enum):
    NOOP = "noop"
    INCREASE_AI_FREE_PRACTICE = "increase_ai_free_practice"
    FLAG_MORAL_FORMATION = "flag_moral_formation"
    TARGETED_DOMAIN_INTERVENTION = "targeted_domain_intervention"
    SUSTAIN_AND_MONITOR = "sustain_and_monitor"
    INVESTIGATE_ANOMALY = "investigate_anomaly"
    FLAG_FOR_PEDAGOGICAL_REVIEW = "flag_for_pedagogical_review"


@dataclass
class ECARule:
    name: str
    event: Event
    condition: Callable[[LearnerState], bool]
    action: CorrectiveAction
    description: str = ""

    def fires(self, event: Event, state: LearnerState) -> bool:
        return self.event == event and self.condition(state)

    def fire(self, event: Event, state: LearnerState) -> Optional[CorrectiveAction]:
        return self.action if self.fires(event, state) else None


class TriggerSet:
    def __init__(self, rules: List[ECARule]):
        self._rules = list(rules)

    @property
    def rules(self) -> List[ECARule]:
        return list(self._rules)

    def fire(self, event: Event, state: LearnerState) -> List[CorrectiveAction]:
        actions = []
        for rule in self._rules:
            result = rule.fire(event, state)
            if result is not None and result != CorrectiveAction.NOOP:
                actions.append(result)
        return actions if actions else [CorrectiveAction.NOOP]


def pedagogical_triggers(
    perf_ai: float, perf_indep: float,
    theta_gap: float = 0.1, m_min: float = 0.2, rho: float = 0.05,
) -> TriggerSet:
    """T_ped: three canonical pedagogical ECA rules (Section 3.8.1)."""
    def ai_dep(s: LearnerState) -> bool:
        return (perf_ai - perf_indep) > theta_gap
    def eth_thr(s: LearnerState) -> bool:
        return s.MA < m_min
    def crit_reg(s: LearnerState) -> bool:
        return any(v < rho for v in s.invisible.values())
    return TriggerSet([
        ECARule("ai_dependence", Event.ASSESSMENT_COMPLETED, ai_dep,
                CorrectiveAction.INCREASE_AI_FREE_PRACTICE),
        ECARule("ethical_threshold", Event.SCAM_POSTERIOR_UPDATED, eth_thr,
                CorrectiveAction.FLAG_MORAL_FORMATION),
        ECARule("critical_regression", Event.LONGITUDINAL_COMPARISON, crit_reg,
                CorrectiveAction.TARGETED_DOMAIN_INTERVENTION),
    ])


def safety_gap_triggers(
    perf_ai: float, perf_indep: float,
    epsilon_small: float = 0.05, epsilon_large: float = 0.25,
) -> TriggerSet:
    """T_safety: four safety-gap ECA rules of Table 2 (Section 3.8.2)."""
    gap = perf_ai - perf_indep
    return TriggerSet([
        ECARule("balanced", Event.SAFETY_GAP_COMPUTED,
                lambda s: abs(gap) <= epsilon_small,
                CorrectiveAction.SUSTAIN_AND_MONITOR),
        ECARule("ai_dependence", Event.SAFETY_GAP_COMPUTED,
                lambda s: epsilon_small < gap < epsilon_large,
                CorrectiveAction.INCREASE_AI_FREE_PRACTICE),
        ECARule("measurement_anomaly", Event.SAFETY_GAP_COMPUTED,
                lambda s: -epsilon_large < gap < -epsilon_small,
                CorrectiveAction.INVESTIGATE_ANOMALY),
        ECARule("large_divergence", Event.SAFETY_GAP_COMPUTED,
                lambda s: abs(gap) >= epsilon_large,
                CorrectiveAction.FLAG_FOR_PEDAGOGICAL_REVIEW),
    ])
