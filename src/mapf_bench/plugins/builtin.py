from __future__ import annotations

from typing import Any, Mapping

from mapf_bench.core.problem import MAPFProblem
from mapf_bench.core.solver import Observation
from mapf_bench.plugins.base import (
    PathfinderCapabilities,
    PlanRequest,
    PlanResult,
    StepRequest,
    StepResult,
)
from mapf_bench.solvers import make_solver


class BuiltinStepPathfinder:
    capabilities = PathfinderCapabilities(
        supports_step=True,
        supports_full_plan=False,
        centralized=False,
        decentralized=True,
    )

    def __init__(self, name: str) -> None:
        self.plugin_id = f"builtin/{name}"
        self.name = name
        self.params: dict[str, Any] = {}
        self.solver = None

    def configure(self, config: Mapping[str, Any]) -> None:
        self.params = dict(config)

    def reset(self, problem: MAPFProblem, *, seed: int | None = None) -> None:
        solver_seed = self.params.get("seed", seed)
        self.solver = make_solver(self.name, seed=solver_seed)
        self.solver.reset(problem)

    def step(self, request: StepRequest) -> StepResult:
        if self.solver is None:
            self.reset(request.problem, seed=request.seed)

        actions = self.solver.step(Observation(request.positions))
        return StepResult(actions=actions)

    def plan(self, request: PlanRequest) -> PlanResult:
        return PlanResult(
            status="unsupported",
            message=f"{self.plugin_id} only supports step()",
        )

    def close(self) -> None:
        self.solver = None