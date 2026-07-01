from mapf_bench.core.problem import MAPFProblem
from mapf_bench.core.simulator import SimulationResult


def compute_metrics(problem: MAPFProblem, result: SimulationResult) -> dict:
    goals = {a.agent_id: a.goal for a in problem.agents}

    reached = {
        agent_id: result.final_positions[agent_id] == goal
        for agent_id, goal in goals.items()
    }

    return {
        "success": result.success,
        "num_agents": len(problem.agents),
        "steps": result.steps,
        "reached_agents": sum(reached.values()),
        "success_rate_agents": sum(reached.values()) / len(reached),
        "num_vertex_collisions": result.num_vertex_collisions,
        "num_edge_collisions": result.num_edge_collisions,
        "num_invalid_moves": result.num_invalid_moves,
    }