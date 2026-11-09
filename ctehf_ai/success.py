"""Non-monotonic educational success criterion (Section 3.7)."""

from dataclasses import dataclass, field
from typing import Dict, Optional
from .capacities import Domain, DOMAIN_MEMBERSHIP
from .state import LearnerState
from .ethical import EthicalCompetenceConfig, ethical_competence


@dataclass
class SuccessCriteria:
    delta_min: float = 0.05
    rho: Dict[Domain, float] = field(default_factory=lambda: {
        Domain.MORAL_AGENCY: 0.05,
        Domain.PRACTICAL_EXISTENTIAL: 0.05,
        Domain.RELATIONAL_PRESENCE: 0.05,
    })
    theta_collab: float = 0.5
    theta_indep: float = 0.5
    ethical_config: EthicalCompetenceConfig = field(
        default_factory=EthicalCompetenceConfig)


@dataclass
class SuccessReport:
    successful: bool
    dual_preparation_satisfied: bool
    ethical_threshold_satisfied: bool
    aggregate_ic_development: float
    aggregate_ic_satisfied: bool
    critical_domain_regressions: Dict[str, float]
    no_critical_regression: bool
    human_accountability_preserved: bool
    details: Dict[str, float] = field(default_factory=dict)


def evaluate_success(
    initial_state: LearnerState,
    final_state: LearnerState,
    perf_ai: float,
    perf_indep: float,
    human_accountability_preserved: bool = True,
    criteria: Optional[SuccessCriteria] = None,
) -> SuccessReport:
    criteria = criteria or SuccessCriteria()
    dual = (perf_ai >= criteria.theta_collab
            and perf_indep >= criteria.theta_indep)
    ec_final = ethical_competence(final_state, criteria.ethical_config)
    ethical_ok = ec_final >= criteria.ethical_config.E_min
    delta_ic = final_state.IC - initial_state.IC
    ic_ok = delta_ic >= criteria.delta_min
    regressions = {}
    for domain, members in DOMAIN_MEMBERSHIP.items():
        regressions[domain.value] = float(
            min(final_state.invisible[m] - initial_state.invisible[m]
                for m in members))
    no_regression = all(
        regressions[domain.value] >= -criteria.rho[domain]
        for domain in DOMAIN_MEMBERSHIP)
    successful = (dual and ethical_ok and ic_ok and no_regression
                  and human_accountability_preserved)
    return SuccessReport(
        successful=successful,
        dual_preparation_satisfied=dual,
        ethical_threshold_satisfied=ethical_ok,
        aggregate_ic_development=float(delta_ic),
        aggregate_ic_satisfied=ic_ok,
        critical_domain_regressions=regressions,
        no_critical_regression=no_regression,
        human_accountability_preserved=human_accountability_preserved,
        details={"perf_ai": perf_ai, "perf_indep": perf_indep,
                 "EC": float(ec_final), "E_min": criteria.ethical_config.E_min,
                 "delta_min": criteria.delta_min},
    )
