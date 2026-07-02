from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal, Mapping, Protocol, runtime_checkable

from mapf_bench.core.problem import Action, MAPFProblem, Position


@dataclass(frozen=True)
class PathfinderCapabilities:
    supports_full_plan: bool = False
    supports_step: bool = False
    supports_lifelong: bool = False
    supports_training: bool = False
    supports_batch_eval: bool = False

    centralized: bool = True
    decentralized: bool = False

    requires_gpu: bool = False
    requires_compiled_extensions: bool = False


@dataclass(frozen=True)
class PlanRequest:
    problem: MAPFProblem
    seed: int | None = None
    time_limit_sec: float | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class PlanResult:
    status: Literal["success", "partial", "timeout", "failure", "unsupported"]
    paths: dict[str, list[Position]] = field(default_factory=dict)
    actions: dict[str, list[Action]] | None = None

    runtime_sec: float = 0.0
    cost: float | None = None
    makespan: int | None = None

    message: str = ""
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StepRequest:
    problem: MAPFProblem
    step_index: int
    positions: dict[str, Position]
    seed: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class StepResult:
    actions: dict[str, Action]
    values: dict[str, float] | None = None
    logits: dict[str, list[float]] | None = None
    communication: dict[str, Any] | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@runtime_checkable
class PathfinderPlugin(Protocol):
    plugin_id: str
    capabilities: PathfinderCapabilities

    def configure(self, config: Mapping[str, Any]) -> None:
        ...

    def reset(self, problem: MAPFProblem, *, seed: int | None = None) -> None:
        ...

    def plan(self, request: PlanRequest) -> PlanResult:
        ...

    def step(self, request: StepRequest) -> StepResult:
        ...

    def close(self) -> None:
        ...