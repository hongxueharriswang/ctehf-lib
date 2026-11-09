"""SCAM learner model (Section 4.2)."""

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional
import numpy as np

from .capacities import InvisibleCapacity
from .state import LearnerState, COMPETENCIES, SKILLS


@dataclass
class SCAMConfig:
    process_noise: float = 0.05
    observation_noise: float = 0.1
    initial_uncertainty: float = 0.3


class SCAMModel:
    def __init__(
        self, initial_state: LearnerState,
        config: Optional[SCAMConfig] = None,
        observation_fn: Optional[Callable[[np.ndarray], np.ndarray]] = None,
    ):
        self.config = config or SCAMConfig()
        self._keys = initial_state.all_keys()
        self._state = initial_state.to_vector()
        self._unc = np.full_like(self._state, self.config.initial_uncertainty)
        self._observation_fn = observation_fn or (lambda x: x)
        self._history: List[Dict[str, np.ndarray]] = []

    def predict(self, process_noise: Optional[float] = None) -> None:
        q = process_noise if process_noise is not None else self.config.process_noise
        self._unc = np.sqrt(self._unc ** 2 + q ** 2)

    def update(self, observation: np.ndarray) -> None:
        obs = np.asarray(self._observation_fn(np.asarray(observation, float)))
        if obs.shape != self._state.shape:
            raise ValueError(f"Shape mismatch {obs.shape} vs {self._state.shape}")
        r = self.config.observation_noise
        k = self._unc ** 2 / (self._unc ** 2 + r ** 2 + 1e-12)
        self._state = np.clip(self._state + k * (obs - self._state), 0.0, 1.0)
        self._unc = np.sqrt((1 - k) * self._unc ** 2)
        self._history.append({
            "state": self._state.copy(), "uncertainty": self._unc.copy(),
        })

    @property
    def posterior(self) -> np.ndarray:
        return self._state.copy()

    @property
    def posterior_uncertainty(self) -> np.ndarray:
        return self._unc.copy()

    @property
    def posterior_state(self) -> LearnerState:
        return self._to_learner_state(self._state)

    def credible_interval(self, confidence: float = 0.95):
        from scipy.stats import norm
        z = norm.ppf((1 + confidence) / 2)
        return (np.clip(self._state - z * self._unc, 0.0, 1.0),
                np.clip(self._state + z * self._unc, 0.0, 1.0))

    def ic_estimate(self):
        idx = [i for i, k in enumerate(self._keys) if k.startswith("v_")]
        vals, uncs = self._state[idx], self._unc[idx]
        return (float(np.mean(vals)),
                float(np.sqrt(np.sum(uncs ** 2)) / len(idx)))

    @property
    def history(self) -> List[Dict[str, np.ndarray]]:
        return list(self._history)

    def _to_learner_state(self, vec: np.ndarray) -> LearnerState:
        comps, skills, invisible, knowledge, unc = {}, {}, {}, {}, {}
        for i, key in enumerate(self._keys):
            val = float(vec[i])
            if key in COMPETENCIES:
                comps[key] = val
            elif key in SKILLS:
                skills[key] = val
            elif key.startswith("v_"):
                for c in InvisibleCapacity:
                    if c.value == key:
                        invisible[c] = val
                        break
            else:
                knowledge[key] = val
            unc[key] = float(self._unc[i])
        return LearnerState(competencies=comps, skills=skills,
                            invisible=invisible, knowledge=knowledge,
                            uncertainty=unc)
