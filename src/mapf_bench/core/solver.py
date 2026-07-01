from typing import Protocol

from mapf_bench.core.problem import Action, MAPFProblem, Position


Observation = dict[str, Position]
ActionDict = dict[str, Action]


class SolverPlugin(Protocol):
    name: str

    def reset(self, problem: MAPFProblem) -> None:
        ...

    def step(self, observation: Observation) -> ActionDict:
        ...