from mapf_bench.core.problem import AgentTask, GridMap, MAPFProblem
from mapf_bench.core.simulator import run_simulation
from mapf_bench.plugins.loader import load_pathfinder_from_file


def test_builtin_greedy_plugin_loads_and_runs():
    problem = MAPFProblem(
        grid=GridMap(width=4, height=4, obstacles=frozenset()),
        agents=(AgentTask("a0", (0, 0), (3, 0)),),
        max_steps=8,
    )

    plugin = load_pathfinder_from_file("examples/plugins/greedy.yaml")
    result = run_simulation(problem, plugin)

    assert result.success is True
    assert result.final_positions["a0"] == (3, 0)