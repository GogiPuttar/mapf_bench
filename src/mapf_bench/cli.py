import typer
from rich import print

from mapf_bench.core.metrics import compute_metrics
from mapf_bench.core.simulator import run_simulation
from mapf_bench.io.replay import write_run_outputs
from mapf_bench.io.scenarios import load_problem
from mapf_bench.solvers import make_solver


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


if __name__ == "__main__":
    app()