"""Pedagogical actions and trajectories (Section 4.1)."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, List, Optional
import numpy as np

from .state import LearnerState


class ActionType(Enum):
    SCAFFOLD = "scaffold"
    FADE = "fade"
    REFLECT = "reflect"
    ASSESS = "assess"


@dataclass
class PedagogicalAction:
    action_type: ActionType
    description: str = ""
    involves_ai: bool = False
    has_ai_free_alternative: bool = True
    under_human_review: bool = True
    transparent: bool = True
    ai_autonomy: float = 0.0
    target: Optional[str] = None
    intensity: float = 0.1


class TransitionFunction:
    def __init__(self, learning_rate: float = 0.1, decay_rate: float = 0.01):
        self.learning_rate = learning_rate
        self.decay_rate = decay_rate

    def __call__(
        self, state: LearnerState, action: PedagogicalAction,
        rng: Optional[np.random.Generator] = None,
    ) -> LearnerState:
        new = state.copy()
        target = action.target or ""
        gain = self.learning_rate * action.intensity
        if target in new.competencies:
            new.competencies[target] = min(1.0, new.competencies[target] + gain)
        elif target in new.skills:
            new.skills[target] = min(1.0, new.skills[target] + gain)
        elif target in new.knowledge:
            new.knowledge[target] = min(1.0, new.knowledge[target] + gain)
        else:
            for c in new.invisible:
                if c.value == target or c.name.lower() == target.lower():
                    new.invisible[c] = min(1.0, new.invisible[c] + gain)
                    break
        for c in new.invisible:
            if c.value != target:
                new.invisible[c] = max(
                    0.0, new.invisible[c] - self.decay_rate * action.intensity)
        if rng is not None:
            for c in new.invisible:
                new.invisible[c] = float(
                    np.clip(new.invisible[c] + rng.normal(0, 0.005), 0.0, 1.0))
        return new


@dataclass
class Trajectory:
    states: List[LearnerState]
    actions: List[PedagogicalAction]

    @property
    def initial(self) -> LearnerState:
        return self.states[0]

    @property
    def final(self) -> LearnerState:
        return self.states[-1]

    @property
    def length(self) -> int:
        return len(self.actions)


@dataclass
class TrajectoryOptimizer:
    transition: TransitionFunction = field(default_factory=TransitionFunction)
    action_pool: List[PedagogicalAction] = field(default_factory=list)

    def greedy_optimize(
        self, initial: LearnerState, horizon: int,
        objective: Optional[Callable[[LearnerState], float]] = None,
        rng: Optional[np.random.Generator] = None,
    ) -> Trajectory:
        objective = objective or (lambda s: s.IC + s.DC)
        states, actions = [initial], []
        current = initial
        for _ in range(horizon):
            best_a, best_v, best_next = None, -np.inf, None
            for a in self.action_pool:
                nxt = self.transition(current, a, rng)
                v = objective(nxt)
                if v > best_v:
                    best_v, best_a, best_next = v, a, nxt
            if best_a is None:
                break
            actions.append(best_a)
            states.append(best_next)
            current = best_next
        return Trajectory(states=states, actions=actions)
