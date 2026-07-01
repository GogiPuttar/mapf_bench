from mapf_bench.core.problem import AgentTask, GridMap, MAPFProblem, Action
from mapf_bench.core.simulator import run_simulation
from mapf_bench.solvers.wait_solver import WaitSolver
from mapf_bench.solvers.greedy_solver import GreedySolver


def test_wait_solver_times_out_when_not_at_goal():
    problem = MAPFProblem(
        grid=GridMap(width=4, height=4, obstacles=frozenset()),
        agents=(AgentTask("a0", (0, 0), (3, 3)),),
        max_steps=4,
    )

    result = run_simulation(problem, WaitSolver())

    assert result.success is False
    assert result.steps == 4
    assert result.final_positions["a0"] == (0, 0)


def test_wait_solver_succeeds_if_already_at_goal():
    problem = MAPFProblem(
        grid=GridMap(width=4, height=4, obstacles=frozenset()),
        agents=(AgentTask("a0", (0, 0), (0, 0)),),
        max_steps=4,
    )

    result = run_simulation(problem, WaitSolver())

    assert result.success is True
    assert result.steps == 0


class FixedActionSolver:
    name = "fixed"

    def __init__(self, actions_by_step):
        self.actions_by_step = actions_by_step
        self.step_index = 0

    def reset(self, problem):
        self.agent_ids = [a.agent_id for a in problem.agents]
        self.step_index = 0

    def step(self, observation):
        if self.step_index >= len(self.actions_by_step):
            return {agent_id: Action.WAIT for agent_id in self.agent_ids}

        actions = self.actions_by_step[self.step_index]
        self.step_index += 1
        return actions


def test_greedy_solver_reaches_single_agent_goal():
    problem = MAPFProblem(
        grid=GridMap(width=4, height=4, obstacles=frozenset()),
        agents=(AgentTask("a0", (0, 0), (3, 0)),),
        max_steps=8,
    )

    result = run_simulation(problem, GreedySolver())

    assert result.success is True
    assert result.final_positions["a0"] == (3, 0)


def test_greedy_solver_avoids_wall_and_obstacle():
    problem = MAPFProblem(
        grid=GridMap(width=4, height=4, obstacles=frozenset({(1, 0)})),
        agents=(AgentTask("a0", (0, 0), (2, 0)),),
        max_steps=8,
    )

    result = run_simulation(problem, GreedySolver())

    assert result.num_invalid_moves == 0
    assert result.final_positions["a0"] != (1, 0)


def test_vertex_collision_is_detected():
    problem = MAPFProblem(
        grid=GridMap(width=4, height=4, obstacles=frozenset()),
        agents=(
            AgentTask("a0", (0, 1), (1, 1)),
            AgentTask("a1", (2, 1), (1, 1)),
        ),
        max_steps=1,
    )

    solver = FixedActionSolver(
        [
            {
                "a0": Action.RIGHT,
                "a1": Action.LEFT,
            }
        ]
    )

    result = run_simulation(problem, solver)

    assert result.num_vertex_collisions == 1
    assert result.history[0].vertex_collisions == [["a0", "a1"]]


def test_edge_collision_is_detected():
    problem = MAPFProblem(
        grid=GridMap(width=4, height=4, obstacles=frozenset()),
        agents=(
            AgentTask("a0", (0, 0), (1, 0)),
            AgentTask("a1", (1, 0), (0, 0)),
        ),
        max_steps=1,
    )

    solver = FixedActionSolver(
        [
            {
                "a0": Action.RIGHT,
                "a1": Action.LEFT,
            }
        ]
    )

    result = run_simulation(problem, solver)

    assert result.num_edge_collisions == 1
    assert result.history[0].edge_collisions == [["a0", "a1"]]