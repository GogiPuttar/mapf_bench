import importlib.util

import pytest

from mapf_bench.core.problem import AgentTask, GridMap, MAPFProblem
from mapf_bench.core.simulator import run_simulation
from mapf_bench.plugins.loader import load_pathfinder_from_file


pytestmark = pytest.mark.integration


def test_external_primal2_plugin_smoke():
    if importlib.util.find_spec("mapf_bench_primal2") is None:
        pytest.skip("mapf_bench_primal2 is not installed")

    problem = MAPFProblem(
        grid=GridMap(width=4, height=4, obstacles=frozenset()),
        agents=(AgentTask("a0", (0, 0), (3, 0)),),
        max_steps=8,
    )

    plugin = load_pathfinder_from_file("examples/plugins/primal2.yaml")
    result = run_simulation(problem, plugin)

    assert result.success is True