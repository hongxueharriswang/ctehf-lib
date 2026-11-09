"""Governance trajectory daemons (Section 5).

A daemon is d: S^T -> A_act U {noop}. Three daemons per Section 5.3.
"""

from dataclasses import dataclass
from typing import List, Optional

from .state import LearnerState
from .ethical import EthicalCompetenceConfig, ethical_competence
from .safety_gap import safety_gap


NOOP = "noop"


def _slope(values: List[float]) -> float:
    n = len(values)
    if n < 2:
        return 0.0
    xs = list(range(n))
    mx, my = sum(xs) / n, sum(values) / n
    num = sum((xs[i] - mx) * (values[i] - my) for i in range(n))
    den = sum((xs[i] - mx) ** 2 for i in range(n))
    return num / den if den else 0.0


def daemon_dual_prep(
    trajectory: List[LearnerState],
    perf_ai_trajectory: List[float],
    perf_indep_trajectory: List[float],
    epsilon_small: float = 0.05,
) -> str:
    if len(perf_ai_trajectory) != len(perf_indep_trajectory):
        raise ValueError("Performance trajectories must be same length")
    if not perf_ai_trajectory:
        return NOOP
    gaps = [safety_gap(a, i) for a, i in zip(perf_ai_trajectory, perf_indep_trajectory)]
    latest = gaps[-1]
    slope = _slope(gaps[-5:]) if len(gaps) >= 5 else _slope(gaps)
    if latest > epsilon_small and slope > 0:
        return "increase-ai-free-practice"
    if latest < -epsilon_small:
        return "investigate-anomaly"
    if abs(latest) <= epsilon_small and abs(slope) > 0.01:
        return "monitor-closely"
    return NOOP


def daemon_ethics(
    trajectory: List[LearnerState],
    ethical_config: Optional[EthicalCompetenceConfig] = None,
) -> str:
    ethical_config = ethical_config or EthicalCompetenceConfig()
    if not trajectory:
        return NOOP
    ec_values = [ethical_competence(s, ethical_config) for s in trajectory]
    latest = ec_values[-1]
    e_min = ethical_config.E_min
    if latest < e_min:
        return "halt-and-remediate"
    margins = [ec - e_min for ec in ec_values]
    slope = _slope(margins[-5:]) if len(margins) >= 5 else _slope(margins)
    if slope < -0.01:
        return "flag-moral-formation"
    return NOOP


def daemon_transparency(ai_action_log: List[dict]) -> str:
    if not ai_action_log:
        return NOOP
    violations = [
        e for e in ai_action_log
        if not (e.get("has_ai_free_alternative", True)
                and e.get("under_human_review", True)
                and e.get("transparent", True))]
    if not violations:
        return NOOP
    if len(violations) >= 2:
        return "block-action"
    return "require-disclosure"


@dataclass
class GovernanceDaemons:
    """The set D_gov = {d_dual-prep, d_ethics, d_transparency} (Section 5)."""
    epsilon_small: float = 0.05
    ethical_config: Optional[EthicalCompetenceConfig] = None

    def run(
        self,
        trajectory: List[LearnerState],
        perf_ai_trajectory: List[float],
        perf_indep_trajectory: List[float],
        ai_action_log: List[dict],
    ) -> dict:
        return {
            "d_dual_prep": daemon_dual_prep(
                trajectory, perf_ai_trajectory, perf_indep_trajectory,
                self.epsilon_small),
            "d_ethics": daemon_ethics(trajectory, self.ethical_config),
            "d_transparency": daemon_transparency(ai_action_log),
        }
