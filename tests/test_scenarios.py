from mapf_bench.io.scenarios import load_problem


def test_load_problem():
    problem = load_problem("examples/scenarios/two_agents_swap.yaml")

    assert problem.grid.width == 8
    assert problem.grid.height == 8
    assert len(problem.agents) == 2
    assert problem.max_steps == 32