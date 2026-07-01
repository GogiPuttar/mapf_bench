import json
from dataclasses import asdict
from pathlib import Path

from mapf_bench.core.metrics import compute_metrics
from mapf_bench.core.problem import MAPFProblem
from mapf_bench.core.simulator import SimulationResult


def write_run_outputs(
    out_dir: str,
    problem: MAPFProblem,
    result: SimulationResult,
    solver_name: str,
) -> None:
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)

    metrics = compute_metrics(problem, result)

    replay = {
        "solver": solver_name,
        "grid": {
            "width": problem.grid.width,
            "height": problem.grid.height,
            "obstacles": sorted(list(problem.grid.obstacles)),
        },
        "agents": [
            {
                "id": a.agent_id,
                "start": a.start,
                "goal": a.goal,
            }
            for a in problem.agents
        ],
        "history": [asdict(step) for step in result.history],
    }

    with open(path / "metrics.json", "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)

    with open(path / "replay.json", "w", encoding="utf-8") as f:
        json.dump(replay, f, indent=2)