"""CTE-HF-AI v0.2.0: Computational Theory of Education for Human Flourishing.

Aligned with the revised paper: DC three-constituent decomposition,
ECA trigger sets, trajectory daemons, embeddings, hybrid dynamics,
and free-energy precision correspondence.
"""

from .capacities import (
    InvisibleCapacity, Domain, DOMAIN_MEMBERSHIP,
    ALL_INVISIBLE_CAPACITIES, aggregate_domain, aggregate_all_domains, normalized_ic,
)
from .state import LearnerState, COMPETENCIES, SKILLS
from .dc import (
    DCConfig, disciplinary_mastery, professional_performance,
    transferable_competencies, domain_competence, dc_decomposed,
)
from .ethical import (
    EthicalCompetenceConfig, ethical_competence,
    ethical_competence_via_precision,
    is_ethical_threshold_satisfied, ethical_competence_decomposed,
)
from .flourishing import (
    FlourishingConfig, educational_flourishing, total_flourishing,
)
from .success import SuccessCriteria, SuccessReport, evaluate_success
from .safety_gap import (
    safety_gap, SafetyGapInterpretation, interpret_safety_gap, recommended_response,
)
from .triggers import (
    Event, CorrectiveAction, ECARule, TriggerSet,
    pedagogical_triggers, safety_gap_triggers,
)
from .daemons import (
    GovernanceDaemons, daemon_dual_prep, daemon_ethics, daemon_transparency,
)
from .embeddings import (
    Embedding, IdentityLearnerEmbedding, IdentityActionEmbedding,
    MeanArtefactEmbedding, similarity_in_H, nearest_neighbours,
)
from .hybrid import (
    HybridDynamics, empirical_lipschitz, check_theorem_3_1_assumptions,
)
from .free_energy import PrecisionPrior, ethical_precision, variational_free_energy
from .scam import SCAMModel, SCAMConfig
from .coh import COHObject, ConstraintDaemon, ConstraintHierarchy, ConstraintViolation
from .governance import (
    GovernanceConfig, GovernanceFramework, is_admissible, filter_admissible,
)
from .trajectories import (
    ActionType, PedagogicalAction, TransitionFunction, Trajectory, TrajectoryOptimizer,
)
from .agents import (
    Agent, AgentRole, HumanTeacherAgent, AITutorAgent,
    PeerLearningAgent, ReflectionAgent, MultiAgentTutoringSystem,
)
from .fcp import FCPPrinciple, FCPStatus, check_fcp_compliance
from .calibration import ThresholdCalibrator

__version__ = "0.2.0"

__all__ = [
    # v0.1.0 baseline
    "InvisibleCapacity", "Domain", "DOMAIN_MEMBERSHIP",
    "ALL_INVISIBLE_CAPACITIES", "aggregate_domain", "aggregate_all_domains",
    "normalized_ic", "LearnerState", "COMPETENCIES", "SKILLS",
    "EthicalCompetenceConfig", "ethical_competence",
    "is_ethical_threshold_satisfied", "ethical_competence_decomposed",
    "FlourishingConfig", "educational_flourishing", "total_flourishing",
    "SuccessCriteria", "SuccessReport", "evaluate_success",
    "safety_gap", "SafetyGapInterpretation", "interpret_safety_gap",
    "recommended_response",
    "SCAMModel", "SCAMConfig",
    "COHObject", "ConstraintDaemon", "ConstraintHierarchy", "ConstraintViolation",
    "GovernanceConfig", "GovernanceFramework", "is_admissible", "filter_admissible",
    "ActionType", "PedagogicalAction", "TransitionFunction",
    "Trajectory", "TrajectoryOptimizer",
    "Agent", "AgentRole", "HumanTeacherAgent", "AITutorAgent",
    "PeerLearningAgent", "ReflectionAgent", "MultiAgentTutoringSystem",
    "FCPPrinciple", "FCPStatus", "check_fcp_compliance", "ThresholdCalibrator",
    # v0.2.0 additions
    "DCConfig", "disciplinary_mastery", "professional_performance",
    "transferable_competencies", "domain_competence", "dc_decomposed",
    "Event", "CorrectiveAction", "ECARule", "TriggerSet",
    "pedagogical_triggers", "safety_gap_triggers",
    "GovernanceDaemons", "daemon_dual_prep", "daemon_ethics", "daemon_transparency",
    "Embedding", "IdentityLearnerEmbedding", "IdentityActionEmbedding",
    "MeanArtefactEmbedding", "similarity_in_H", "nearest_neighbours",
    "HybridDynamics", "empirical_lipschitz", "check_theorem_3_1_assumptions",
    "PrecisionPrior", "ethical_precision", "variational_free_energy",
    "ethical_competence_via_precision",
]
