import json
import os
import time
import sys

from mapf_bench.render.config import ReplayRenderConfig


def _clear_screen() -> None:
    if not sys.stdout.isatty():
        return

    if os.name == "nt":
        os.system("cls")
    elif os.environ.get("TERM"):
        os.system("clear")


def render_ascii(replay_path: str, config: ReplayRenderConfig) -> None:
    with open(replay_path, "r", encoding="utf-8") as f:
        replay = json.load(f)

    width = replay["grid"]["width"]
    height = replay["grid"]["height"]
    obstacles = {tuple(p) for p in replay["grid"].get("obstacles", [])}
    goals = {a["id"]: tuple(a["goal"]) for a in replay["agents"]}
    history = replay["history"]

    delay = 1.0 / config.fps if config.fps > 0 else 0.0

    while True:
        for frame in history:
            _clear_screen()
            print(_frame_to_ascii(width, height, obstacles, goals, frame, config))
            time.sleep(delay)

        if not config.loop:
            break


def _frame_to_ascii(
    width: int,
    height: int,
    obstacles: set[tuple[int, int]],
    goals: dict[str, tuple[int, int]],
    frame: dict,
    config: ReplayRenderConfig,
) -> str:
    positions = {
        agent_id: tuple(pos)
        for agent_id, pos in frame["positions"].items()
    }

    lines: list[str] = []
    lines.append(f"Step {frame['step']}")

    if frame.get("vertex_collisions"):
        lines.append(f"Vertex collisions: {frame['vertex_collisions']}")
    if frame.get("edge_collisions"):
        lines.append(f"Edge collisions: {frame['edge_collisions']}")
    if frame.get("invalid_moves"):
        lines.append(f"Invalid moves: {frame['invalid_moves']}")

    for y in range(height):
        row: list[str] = []
        for x in range(width):
            pos = (x, y)

            agent_here = [
                agent_id for agent_id, agent_pos in positions.items()
                if agent_pos == pos
            ]

            if agent_here:
                row.append(_agent_symbol(agent_here))
            elif pos in obstacles:
                row.append("■■")
            elif config.show_goals and pos in goals.values():
                goal_agent_ids = [
                    agent_id for agent_id, goal_pos in goals.items()
                    if goal_pos == pos
                ]
                row.append(_goal_symbol(goal_agent_ids[0]))
            else:
                row.append("..")

        lines.append(" ".join(row))

    return "\n".join(lines)


def _agent_symbol(agent_ids: list[str]) -> str:
    if len(agent_ids) > 1:
        return "XX"

    agent_id = agent_ids[0]
    digits = "".join(ch for ch in agent_id if ch.isdigit())

    if digits:
        return f"a{digits[-1]}"

    return agent_id[:2].ljust(2)

def _goal_symbol(agent_id: str) -> str:
    digits = "".join(ch for ch in agent_id if ch.isdigit())

    if digits:
        return f"g{digits[-1]}"

    return ("g" + agent_id[:1]).ljust(2)