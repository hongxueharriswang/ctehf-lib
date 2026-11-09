"""Multi-agent tutoring system (Section 4.3)."""

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List


class AgentRole(Enum):
    HUMAN_TEACHER = "human_teacher"
    AI_TUTOR = "ai_tutor"
    PEER_LEARNER = "peer_learner"
    REFLECTION = "reflection"


@dataclass
class Agent:
    role: AgentRole
    name: str
    accountable: bool = False
    bounded: bool = True

    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"role": self.role.value, "name": self.name}


@dataclass
class HumanTeacherAgent(Agent):
    role: AgentRole = AgentRole.HUMAN_TEACHER
    name: str = "human_teacher"
    accountable: bool = True
    bounded: bool = False

    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"action": "moral_exemplification",
                "role": self.role.value, "non_delegable": True}


@dataclass
class AITutorAgent(Agent):
    role: AgentRole = AgentRole.AI_TUTOR
    name: str = "ai_tutor"

    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"action": "generate_and_review", "role": self.role.value,
                "requires_human_review": True,
                "ai_free_alternative_available": True}


@dataclass
class PeerLearningAgent(Agent):
    role: AgentRole = AgentRole.PEER_LEARNER
    name: str = "peer_learner"

    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"action": "community_accountability", "role": self.role.value}


@dataclass
class ReflectionAgent(Agent):
    role: AgentRole = AgentRole.REFLECTION
    name: str = "reflection"

    def act(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"action": "narrative_identity_formation", "role": self.role.value}


@dataclass
class MultiAgentTutoringSystem:
    human_teacher: HumanTeacherAgent = field(default_factory=HumanTeacherAgent)
    ai_tutor: AITutorAgent = field(default_factory=AITutorAgent)
    peer: PeerLearningAgent = field(default_factory=PeerLearningAgent)
    reflection: ReflectionAgent = field(default_factory=ReflectionAgent)

    def all_agents(self) -> List[Agent]:
        return [self.human_teacher, self.ai_tutor, self.peer, self.reflection]

    def accountability_preserved(self) -> bool:
        return self.human_teacher.accountable is True

    def coordinate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        return {"agents": {a.name: a.act(context) for a in self.all_agents()},
                "human_accountability_preserved": self.accountability_preserved()}
