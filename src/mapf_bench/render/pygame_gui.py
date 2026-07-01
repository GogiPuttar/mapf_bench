import json
import sys
import time

from mapf_bench.render.config import ReplayRenderConfig

def build_agent_color_table(replay, config):
    palette = config.agent_palette

    table = {}

    for i, agent in enumerate(replay["agents"]):
        table[agent["id"]] = palette[i % len(palette)]

    return table

def render_pygame(replay_path: str, config: ReplayRenderConfig) -> None:
    try:
        import pygame
    except ImportError as exc:
        raise RuntimeError(
            "pygame is not installed. Install with: pip install -e '.[gui]'"
        ) from exc

    with open(replay_path, "r", encoding="utf-8") as f:
        replay = json.load(f)

    width = replay["grid"]["width"]
    height = replay["grid"]["height"]
    obstacles = {tuple(p) for p in replay["grid"].get("obstacles", [])}
    goals = {a["id"]: tuple(a["goal"]) for a in replay["agents"]}
    history = replay["history"]
    agent_colors = build_agent_color_table(replay, config)

    cell = config.cell_size_px
    sidebar_width = 240
    window_size = (width * cell + sidebar_width, height * cell)

    pygame.init()
    screen = pygame.display.set_mode(window_size)
    pygame.display.set_caption(f"mapf_bench replay: {replay.get('solver', 'unknown')}")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 24)

    frame_index = 0
    paused = False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    return
                if event.key == pygame.K_SPACE:
                    paused = not paused
                if event.key == pygame.K_RIGHT:
                    frame_index = min(frame_index + 1, len(history) - 1)
                if event.key == pygame.K_LEFT:
                    frame_index = max(frame_index - 1, 0)

        frame = history[frame_index]
        _draw_frame(
            screen,
            font,
            replay,
            frame,
            obstacles,
            goals,
            agent_colors,
            config,
        )

        pygame.display.flip()

        if not paused:
            frame_index += 1
            if frame_index >= len(history):
                if config.loop:
                    frame_index = 0
                else:
                    frame_index = len(history) - 1
                    paused = True

        clock.tick(config.fps if config.fps > 0 else 60)


def _draw_frame(
    screen,
    font,
    replay,
    frame,
    obstacles,
    goals,
    agent_colors,
    config,
):
    import pygame

    width = replay["grid"]["width"]
    height = replay["grid"]["height"]
    cell = config.cell_size_px

    theme = config.theme

    screen.fill(theme.background)

    positions = {
        agent_id: tuple(pos)
        for agent_id, pos in frame["positions"].items()
    }

    collision_agents = set()
    for group in frame.get("vertex_collisions", []):
        collision_agents.update(group)
    for group in frame.get("edge_collisions", []):
        collision_agents.update(group)

    if config.show_goals:
        for agent_id, goal in goals.items():
            x, y = goal
            pygame.draw.rect(
                screen,
                agent_colors[agent_id],
                pygame.Rect(x * cell, y * cell, cell, cell),
            )

    for x, y in obstacles:
        pygame.draw.rect(
            screen,
            theme.obstacle,
            pygame.Rect(x * cell, y * cell, cell, cell),
        )

    if config.show_grid:
        for x in range(width + 1):
            pygame.draw.line(
                screen,
                theme.grid,
                (x * cell, 0),
                (x * cell, height * cell),
            )

        for y in range(height + 1):
            pygame.draw.line(
                screen,
                theme.grid,
                (0, y * cell),
                (width * cell, y * cell),
            )

    for agent_id, pos in positions.items():
        x, y = pos
        center = (x * cell + cell // 2, y * cell + cell // 2)
        radius = max(8, cell // 3)

        base = agent_colors[agent_id]

        color = (
            theme.collision
            if agent_id in collision_agents
            else base
        )
        pygame.draw.circle(screen, color, center, radius)

        label = font.render(agent_id, True, theme.text)
        label_rect = label.get_rect(center=center)
        screen.blit(label, label_rect)

    _draw_sidebar(screen, font, replay, frame, config)


def _draw_sidebar(screen, font, replay, frame, config):
    import pygame

    theme = config.theme
    sidebar_x = replay["grid"]["width"] * config.cell_size_px

    pygame.draw.rect(
        screen,
        theme.sidebar,
        pygame.Rect(sidebar_x, 0, 240, screen.get_height()),
    )

    lines = [
        f"Solver: {replay.get('solver', 'unknown')}",
        f"Step: {frame['step']}",
        "",
        "Controls:",
        "Space: pause",
        "Left/Right: step",
        "Q/Esc: quit",
        "",
        f"Vertex: {len(frame.get('vertex_collisions', []))}",
        f"Edge: {len(frame.get('edge_collisions', []))}",
        f"Invalid: {len(frame.get('invalid_moves', []))}",
    ]

    y = 16
    for line in lines:
        text = font.render(line, True, theme.text)
        screen.blit(text, (sidebar_x + 12, y))
        y += 26