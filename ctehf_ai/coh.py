"""Constrained Object Hierarchies (Section 4.1)."""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional


class ConstraintViolation(Exception):
    pass


@dataclass
class ConstraintDaemon:
    name: str
    check: Callable[[Any], bool]
    message: str = "Constraint violated"

    def enforce(self, state: Any) -> None:
        if not self.check(state):
            raise ConstraintViolation(f"[{self.name}] {self.message}")


@dataclass
class COHObject:
    name: str
    level: int
    components: List[str] = field(default_factory=list)
    daemons: List[ConstraintDaemon] = field(default_factory=list)
    parent: Optional[str] = None
    children: List[str] = field(default_factory=list)


class ConstraintHierarchy:
    def __init__(self) -> None:
        self._nodes: Dict[str, COHObject] = {}
        self._root: Optional[str] = None

    def register(self, node: COHObject) -> None:
        self._nodes[node.name] = node
        if node.parent is None:
            self._root = node.name
        elif node.parent in self._nodes:
            self._nodes[node.parent].children.append(node.name)

    def get(self, name: str) -> COHObject:
        return self._nodes[name]

    @property
    def root(self) -> Optional[COHObject]:
        return self._nodes.get(self._root) if self._root else None

    def nodes(self) -> List[COHObject]:
        return list(self._nodes.values())

    def enforce_all(self, state: Any) -> List[str]:
        violations = []
        for node in self._nodes.values():
            for d in node.daemons:
                try:
                    d.enforce(state)
                except ConstraintViolation as e:
                    violations.append(str(e))
        return violations

    def enforce_level(self, level: int, state: Any) -> List[str]:
        violations = []
        for node in self._nodes.values():
            if node.level != level:
                continue
            for d in node.daemons:
                try:
                    d.enforce(state)
                except ConstraintViolation as e:
                    violations.append(str(e))
        return violations
