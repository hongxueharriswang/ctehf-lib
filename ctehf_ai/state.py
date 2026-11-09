"""Learner state S = S_comp x S_skill x S_inv x S_know (Section 3.2)."""

from dataclasses import dataclass, field
from typing import Dict, List
import numpy as np

from .capacities import (
    InvisibleCapacity, Domain, ALL_INVISIBLE_CAPACITIES,
    aggregate_all_domains, normalized_ic,
)


COMPETENCIES = (
    "algorithmic_literacy", "ethical_judgment", "creative_abduction",
    "metacognition", "emotional_intelligence", "systems_thinking",
)
SKILLS = ("learning_to_learn", "judge", "create", "relate", "be")


def _clip(v: float) -> float:
    return float(np.clip(v, 0.0, 1.0))


@dataclass
class LearnerState:
    competencies: Dict[str, float] = field(default_factory=dict)
    skills: Dict[str, float] = field(default_factory=dict)
    invisible: Dict[InvisibleCapacity, float] = field(default_factory=dict)
    knowledge: Dict[str, float] = field(default_factory=dict)
    uncertainty: Dict[str, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        for c in ALL_INVISIBLE_CAPACITIES:
            self.invisible.setdefault(c, 0.0)
        for mapping in (self.competencies, self.skills, self.knowledge):
            for k in list(mapping):
                mapping[k] = _clip(mapping[k])
        for c in list(self.invisible):
            self.invisible[c] = _clip(self.invisible[c])
        for k in self.all_keys():
            self.uncertainty.setdefault(k, 0.0)

    def all_keys(self) -> List[str]:
        return (list(self.competencies) + list(self.skills)
                + [c.value for c in self.invisible] + list(self.knowledge))

    def domain_aggregates(self) -> Dict[Domain, float]:
        return aggregate_all_domains(self.invisible)

    @property
    def MA(self) -> float:
        return self.domain_aggregates()[Domain.MORAL_AGENCY]

    @property
    def PJ(self) -> float:
        return self.domain_aggregates()[Domain.PRACTICAL_EXISTENTIAL]

    @property
    def RP(self) -> float:
        return self.domain_aggregates()[Domain.RELATIONAL_PRESENCE]

    @property
    def IC(self) -> float:
        return normalized_ic(self.invisible)

    @property
    def DC(self) -> float:
        """Domain competence DC(s) via three-constituent composite (§3.2.3)."""
        from .dc import domain_competence
        return domain_competence(self.competencies, self.knowledge)

    @property
    def DC_decomposed(self) -> dict:
        """Diagnostic decomposition of DC into DC_disc, DC_prof, DC_comp (§3.2.3)."""
        from .dc import dc_decomposed
        return dc_decomposed(self.competencies, self.knowledge)

    def copy(self) -> "LearnerState":
        return LearnerState(
            competencies=dict(self.competencies), skills=dict(self.skills),
            invisible=dict(self.invisible), knowledge=dict(self.knowledge),
            uncertainty=dict(self.uncertainty),
        )

    def to_vector(self) -> np.ndarray:
        return np.array([self._get(k) for k in self.all_keys()], dtype=float)

    def _get(self, key: str) -> float:
        if key in self.competencies: return self.competencies[key]
        if key in self.skills: return self.skills[key]
        if key in self.knowledge: return self.knowledge[key]
        for c in InvisibleCapacity:
            if c.value == key: return self.invisible[c]
        return 0.0
