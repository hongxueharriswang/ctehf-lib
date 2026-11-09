"""Hybrid continuous-discrete dynamics + Theorem 3.1 (Section 3.9)."""

from dataclasses import dataclass
from typing import Callable, List, Optional
import numpy as np

from .state import LearnerState
from .capacities import InvisibleCapacity
from .trajectories import PedagogicalAction, TransitionFunction


@dataclass
class HybridDynamics:
    continuous_f: Callable[[np.ndarray, PedagogicalAction, dict], np.ndarray]
    discrete_g: TransitionFunction
    trigger_condition: Callable[[LearnerState], bool]
    dt: float = 0.1

    def evolve_continuous(
        self, state: LearnerState, action: PedagogicalAction,
        params: Optional[dict] = None, steps: int = 10,
    ) -> LearnerState:
        params = params or {}
        s_vec = state.to_vector()
        for _ in range(steps):
            ds = self.continuous_f(s_vec, action, params)
            s_vec = np.clip(s_vec + self.dt * ds, 0.0, 1.0)
        return self._vec_to_state(s_vec, state)

    def step(
        self, state: LearnerState, action: PedagogicalAction,
        params: Optional[dict] = None,
    ) -> LearnerState:
        s_cont = self.evolve_continuous(state, action, params)
        if self.trigger_condition(s_cont):
            return self.discrete_g(s_cont, action)
        return s_cont

    def _vec_to_state(self, vec: np.ndarray, template: LearnerState) -> LearnerState:
        new = template.copy()
        keys = template.all_keys()
        for i, key in enumerate(keys):
            v = float(vec[i])
            if key in new.competencies:
                new.competencies[key] = v
            elif key in new.skills:
                new.skills[key] = v
            elif key in new.knowledge:
                new.knowledge[key] = v
            else:
                for c in InvisibleCapacity:
                    if c.value == key:
                        new.invisible[c] = v
                        break
        return new


def empirical_lipschitz(
    fn: Callable[[np.ndarray], np.ndarray],
    points: List[np.ndarray],
    epsilon: float = 1e-6,
) -> float:
    max_ratio = 0.0
    for i in range(len(points)):
        for j in range(i + 1, len(points)):
            d_in = np.linalg.norm(points[i] - points[j])
            if d_in < epsilon:
                continue
            d_out = np.linalg.norm(fn(points[i]) - fn(points[j]))
            max_ratio = max(max_ratio, d_out / d_in)
    return float(max_ratio)


def check_theorem_3_1_assumptions(
    f_lipschitz: float, g_lipschitz: float, trigger_measurable: bool,
) -> dict:
    return {
        "f_lipschitz_satisfied": f_lipschitz < np.inf,
        "f_lipschitz_constant": f_lipschitz,
        "g_lipschitz_satisfied": g_lipschitz < np.inf,
        "g_lipschitz_constant": g_lipschitz,
        "trigger_measurable": trigger_measurable,
        "theorem_3_1_applies": (
            f_lipschitz < np.inf and g_lipschitz < np.inf and trigger_measurable),
    }
