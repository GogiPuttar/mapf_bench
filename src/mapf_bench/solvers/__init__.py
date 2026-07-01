from mapf_bench.solvers.random_solver import RandomSolver
from mapf_bench.solvers.wait_solver import WaitSolver


def make_solver(name: str, seed: int | None = None):
    if name == "wait":
        return WaitSolver()
    if name == "random":
        return RandomSolver(seed=seed)
    raise ValueError(f"Unknown solver: {name}")