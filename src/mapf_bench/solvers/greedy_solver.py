from mapf_bench.core.problem import ACTION_DELTAS, Action, MAPFProblem, Position
from mapf_bench.core.solver import ActionDict, Observation


class GreedySolver:
    name = "greedy"

    def reset(self, problem: MAPFProblem) -> None:
        self.problem = problem
        self.goals = {a.agent_id: a.goal for a in problem.agents}
        self.agent_ids = [a.agent_id for a in problem.agents]

    def step(self, observation: Observation) -> ActionDict:
        actions: ActionDict = {}

        for agent_id in self.agent_ids:
            current = observation[agent_id]
            goal = self.goals[agent_id]

            candidates = sorted(
                list(Action),
                key=lambda action: self._manhattan(
                    self._apply_action(current, action),
                    goal,
                ),
            )

            chosen = Action.WAIT

            for action in candidates:
                proposed = self._apply_action(current, action)
                if self.problem.grid.is_free(proposed):
                    chosen = action
                    break

            actions[agent_id] = chosen

        return actions

    @staticmethod
    def _apply_action(pos: Position, action: Action) -> Position:
        dx, dy = ACTION_DELTAS[action]
        return pos[0] + dx, pos[1] + dy

    @staticmethod
    def _manhattan(a: Position, b: Position) -> int:
        return abs(a[0] - b[0]) + abs(a[1] - b[1])