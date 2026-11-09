"""Governance: DEPRECATED pointwise filter.

Section 5.1 of the revised paper supersedes the pointwise filter with the
trajectory-daemon formulation. Use ctehf_ai.daemons.GovernanceDaemons for
new code. Retained for backward compatibility only.
"""

from dataclasses import dataclass
from enum import Enum
import warnings
from typing import List, Optional

from .trajectories import PedagogicalAction


class GovernanceFramework(Enum):
    EDUCATOR = "educator"
    RESEARCHER = "researcher"
    STUDENT = "student"


@dataclass
class GovernanceConfig:
    require_dual_prep_alternatives: bool = True
    require_human_review: bool = True
    require_transparency: bool = True
    max_ai_autonomy: float = 0.7


def is_admissible(
    action: PedagogicalAction,
    config: Optional[GovernanceConfig] = None,
) -> bool:
    warnings.warn(
        "is_admissible is deprecated; use ctehf_ai.daemons.GovernanceDaemons "
        "for the trajectory-monitor formulation (Section 5.1).",
        DeprecationWarning, stacklevel=2)
    config = config or GovernanceConfig()
    if action.involves_ai:
        if config.require_dual_prep_alternatives and not action.has_ai_free_alternative:
            return False
        if config.require_human_review and not action.under_human_review:
            return False
        if config.require_transparency and not action.transparent:
            return False
    return action.ai_autonomy <= config.max_ai_autonomy


def filter_admissible(
    actions: List[PedagogicalAction],
    config: Optional[GovernanceConfig] = None,
) -> List[PedagogicalAction]:
    warnings.warn(
        "filter_admissible is deprecated; use ctehf_ai.daemons.GovernanceDaemons.",
        DeprecationWarning, stacklevel=2)
    return [a for a in actions if is_admissible(a, config)]
