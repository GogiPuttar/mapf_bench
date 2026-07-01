import typer
from rich import print

from mapf_bench.core.metrics import compute_metrics
from mapf_bench.core.simulator import run_simulation
from mapf_bench.io.replay import write_run_outputs
from mapf_bench.io.scenarios import load_problem
from mapf_bench.solvers import make_solver
from mapf_bench.render.ascii import render_ascii
from mapf_bench.render.config import load_render_config


app = typer.Typer()

@app.callback()
def main():
    """MAPF benchmark CLI."""
    pass

@app.command()
def run(
    scenario: str = typer.Option(..., "--scenario", "-s"),
    solver: str = typer.Option("wait", "--solver"),
    out: str = typer.Option("runs/latest", "--out"),
    seed: int | None = typer.Option(None, "--seed"),
):
    problem = load_problem(scenario)
    solver_obj = make_solver(solver, seed=seed)

    result = run_simulation(problem, solver_obj)
    write_run_outputs(out, problem, result, solver)

    metrics = compute_metrics(problem, result)
    print(metrics)

@app.command()
def replay(
    replay_path: str = typer.Argument(...),
    mode: str = typer.Option("ascii", "--mode"),
    config: str | None = typer.Option(None, "--config"),
):
    render_config = load_render_config(config)

    if mode == "ascii":
        render_ascii(replay_path, render_config)
        return

    if mode == "gui":
        from mapf_bench.render.pygame_gui import render_pygame

        render_pygame(replay_path, render_config)
        return

    raise typer.BadParameter(f"Unknown replay mode: {mode}")

if __name__ == "__main__":
    app()