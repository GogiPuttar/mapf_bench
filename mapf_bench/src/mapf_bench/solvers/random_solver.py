import random

from mapf_bench.core.problem import Action, MAPFProblem
from mapf_bench.core.solver import ActionDict, Observation


class RandomSolver:
    name = "random"

    def __init__(self, seed: int | None = None) -> None:
        self.rng = random.Random(seed)

    def reset(self, problem: MAPFProblem) -> None:
        self.agent_ids = [a.agent_id for a in problem.agents]

    def step(self, observation: Observation) -> ActionDict:
        return {
            agent_id: self.rng.choice(list(Action))
            for agent_id in self.agent_ids
        }