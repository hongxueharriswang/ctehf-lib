"""Embedding E as three shared-Hilbert-space maps (Section 3.2.2)."""

from typing import Any, Dict, Protocol
import numpy as np

from .state import LearnerState
from .trajectories import PedagogicalAction, ActionType


class Embedding(Protocol):
    def __call__(self, obj: Any) -> np.ndarray: ...


class IdentityLearnerEmbedding:
    def __call__(self, state: LearnerState) -> np.ndarray:
        return state.to_vector()


class IdentityActionEmbedding:
    def __init__(self):
        self._index = {t: i for i, t in enumerate(ActionType)}

    def __call__(self, action: PedagogicalAction) -> np.ndarray:
        v = np.zeros(len(self._index))
        v[self._index[action.action_type]] = 1.0
        return v


class MeanArtefactEmbedding:
    def __call__(self, artefacts: Dict[str, np.ndarray]) -> np.ndarray:
        if not artefacts:
            return np.zeros(0)
        return np.mean(list(artefacts.values()), axis=0)


def similarity_in_H(a: np.ndarray, b: np.ndarray) -> float:
    return float(np.linalg.norm(a - b))


def nearest_neighbours(
    query: np.ndarray, candidates: Dict[str, np.ndarray], delta: float = 0.3,
) -> Dict[str, float]:
    return {
        k: similarity_in_H(query, v)
        for k, v in candidates.items()
        if similarity_in_H(query, v) <= delta
    }
