from dataclasses import dataclass, field

from mapf_bench.core.problem import ACTION_DELTAS, Action, MAPFProblem, Position
from mapf_bench.core.solver import SolverPlugin

from mapf_bench.plugins.base import PathfinderPlugin, StepRequest


@dataclass
class StepRecord:
    step: int
    positions: dict[str, Position]
    actions: dict[str, str]
    vertex_collisions: list[list[str]] = field(default_factory=list)
    edge_collisions: list[list[str]] = field(default_factory=list)
    invalid_moves: list[str] = field(default_factory=list)


@dataclass
class SimulationResult:
    success: bool
    steps: int
    final_positions: dict[str, Position]
    history: list[StepRecord]
    num_vertex_collisions: int
    num_edge_collisions: int
    num_invalid_moves: int


def apply_action(pos: Position, action: Action) -> Position:
    dx, dy = ACTION_DELTAS[action]
    return pos[0] + dx, pos[1] + dy


def run_simulation(problem: MAPFProblem, solver: SolverPlugin | PathfinderPlugin) -> SimulationResult:
    solver.reset(problem)

    goals = {a.agent_id: a.goal for a in problem.agents}
    positions = {a.agent_id: a.start for a in problem.agents}

    history: list[StepRecord] = []
    total_vertex = 0
    total_edge = 0
    total_invalid = 0

    for step in range(problem.max_steps):
        if all(positions[a] == goals[a] for a in positions):
            return SimulationResult(
                success=True,
                steps=step,
                final_positions=positions,
                history=history,
                num_vertex_collisions=total_vertex,
                num_edge_collisions=total_edge,
                num_invalid_moves=total_invalid,
            )

        if hasattr(solver, "capabilities"):
            step_result = solver.step(
                StepRequest(
                    problem=problem,
                    step_index=step,
                    positions=dict(positions),
                )
            )
            actions = step_result.actions
        else:
            actions = solver.step(dict(positions))
        proposed: dict[str, Position] = {}
        invalid: list[str] = []

        for agent_id, old_pos in positions.items():
            action = actions.get(agent_id, Action.WAIT)
            if isinstance(action, str):
                action = Action(action)

            new_pos = apply_action(old_pos, action)

            if not problem.grid.is_free(new_pos):
                proposed[agent_id] = old_pos
                invalid.append(agent_id)
            else:
                proposed[agent_id] = new_pos

        vertex_collisions: list[list[str]] = []
        by_pos: dict[Position, list[str]] = {}

        for agent_id, pos in proposed.items():
            by_pos.setdefault(pos, []).append(agent_id)

        for agent_ids in by_pos.values():
            if len(agent_ids) > 1:
                vertex_collisions.append(sorted(agent_ids))

        edge_collisions: list[list[str]] = []
        ids = list(positions.keys())

        for i, a in enumerate(ids):
            for b in ids[i + 1:]:
                if positions[a] == proposed[b] and positions[b] == proposed[a]:
                    if positions[a] != positions[b]:
                        edge_collisions.append(sorted([a, b]))

        total_vertex += len(vertex_collisions)
        total_edge += len(edge_collisions)
        total_invalid += len(invalid)

        positions = proposed

        history.append(
            StepRecord(
                step=step,
                positions=dict(positions),
                actions={k: str(v.value if isinstance(v, Action) else v) for k, v in actions.items()},
                vertex_collisions=vertex_collisions,
                edge_collisions=edge_collisions,
                invalid_moves=invalid,
            )
        )

    return SimulationResult(
        success=all(positions[a] == goals[a] for a in positions),
        steps=problem.max_steps,
        final_positions=positions,
        history=history,
        num_vertex_collisions=total_vertex,
        num_edge_collisions=total_edge,
        num_invalid_moves=total_invalid,
    )