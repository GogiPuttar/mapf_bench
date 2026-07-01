from mapf_bench.core.problem import Action, MAPFProblem
from mapf_bench.core.solver import ActionDict, Observation


class WaitSolver:
    name = "wait"

    def reset(self, problem: MAPFProblem) -> None:
        self.agent_ids = [a.agent_id for a in problem.agents]

    def step(self, observation: Observation) -> ActionDict:
        return {agent_id: Action.WAIT for agent_id in self.agent_ids}