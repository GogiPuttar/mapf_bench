import yaml

from mapf_bench.core.problem import AgentTask, GridMap, MAPFProblem


def load_problem(path: str) -> MAPFProblem:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    grid_data = data["grid"]
    obstacles = frozenset(tuple(p) for p in grid_data.get("obstacles", []))

    grid = GridMap(
        width=int(grid_data["width"]),
        height=int(grid_data["height"]),
        obstacles=obstacles,
    )

    agents = tuple(
        AgentTask(
            agent_id=str(a["id"]),
            start=tuple(a["start"]),
            goal=tuple(a["goal"]),
        )
        for a in data["agents"]
    )

    return MAPFProblem(
        grid=grid,
        agents=agents,
        max_steps=int(data.get("max_steps", 128)),
    )