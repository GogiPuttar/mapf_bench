from mapf_bench.core.problem import AgentTask, GridMap, MAPFProblem
from mapf_bench.core.simulator import run_simulation
from mapf_bench.solvers.wait_solver import WaitSolver


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