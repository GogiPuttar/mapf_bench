from dataclasses import dataclass
from enum import Enum


Position = tuple[int, int]


class Action(str, Enum):
    WAIT = "wait"
    UP = "up"
    DOWN = "down"
    LEFT = "left"
    RIGHT = "right"


ACTION_DELTAS: dict[Action, tuple[int, int]] = {
    Action.WAIT: (0, 0),
    Action.UP: (0, -1),
    Action.DOWN: (0, 1),
    Action.LEFT: (-1, 0),
    Action.RIGHT: (1, 0),
}


@dataclass(frozen=True)
class GridMap:
    width: int
    height: int
    obstacles: frozenset[Position]

    def in_bounds(self, pos: Position) -> bool:
        x, y = pos
        return 0 <= x < self.width and 0 <= y < self.height

    def is_free(self, pos: Position) -> bool:
        return self.in_bounds(pos) and pos not in self.obstacles


@dataclass(frozen=True)
class AgentTask:
    agent_id: str
    start: Position
    goal: Position


@dataclass(frozen=True)
class MAPFProblem:
    grid: GridMap
    agents: tuple[AgentTask, ...]
    max_steps: int