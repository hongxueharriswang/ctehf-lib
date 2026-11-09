"""Invisible capacities and domains (Section 3.2.1, Table 1)."""

from enum import Enum
from typing import Dict, Tuple
import numpy as np


class InvisibleCapacity(Enum):
    MORAL_RESPONSIBILITY = "v_MR"
    ETHICAL_COMMITMENT = "v_ECom"
    CONSCIENCE = "v_Con"
    HUMILITY = "v_Hum"
    WISDOM = "v_Wis"
    MEANING_MAKING = "v_MM"
    PURPOSE = "v_Pur"
    EXISTENTIAL_COURAGE = "v_ECou"
    LOVE = "v_Love"
    EMPATHIC_PRESENCE = "v_EPres"


class Domain(Enum):
    MORAL_AGENCY = "MA"
    PRACTICAL_EXISTENTIAL = "PJ"
    RELATIONAL_PRESENCE = "RP"


DOMAIN_MEMBERSHIP: Dict[Domain, Tuple[InvisibleCapacity, ...]] = {
    Domain.MORAL_AGENCY: (
        InvisibleCapacity.MORAL_RESPONSIBILITY,
        InvisibleCapacity.ETHICAL_COMMITMENT,
        InvisibleCapacity.CONSCIENCE,
        InvisibleCapacity.HUMILITY,
    ),
    Domain.PRACTICAL_EXISTENTIAL: (
        InvisibleCapacity.WISDOM,
        InvisibleCapacity.MEANING_MAKING,
        InvisibleCapacity.PURPOSE,
        InvisibleCapacity.EXISTENTIAL_COURAGE,
    ),
    Domain.RELATIONAL_PRESENCE: (
        InvisibleCapacity.LOVE,
        InvisibleCapacity.EMPATHIC_PRESENCE,
    ),
}

ALL_INVISIBLE_CAPACITIES: Tuple[InvisibleCapacity, ...] = tuple(InvisibleCapacity)


def aggregate_domain(capacities: Dict[InvisibleCapacity, float], domain: Domain) -> float:
    members = DOMAIN_MEMBERSHIP[domain]
    return float(np.mean([capacities[c] for c in members]))


def aggregate_all_domains(capacities: Dict[InvisibleCapacity, float]) -> Dict[Domain, float]:
    return {d: aggregate_domain(capacities, d) for d in Domain}


def normalized_ic(capacities: Dict[InvisibleCapacity, float]) -> float:
    return float(np.mean(list(capacities.values())))
