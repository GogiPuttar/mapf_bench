from dataclasses import dataclass, field

import yaml


Color = tuple[int, int, int]


@dataclass(frozen=True)
class ReplayTheme:
    background: Color = (245, 245, 245)
    grid: Color = (190, 190, 190)
    obstacle: Color = (40, 40, 40)
    collision: Color = (240, 80, 80)
    text: Color = (20, 20, 20)
    sidebar: Color = (230, 230, 230)


@dataclass(frozen=True)
class ReplayRenderConfig:
    fps: float = 4.0
    cell_size_px: int = 48
    show_grid: bool = True
    show_goals: bool = True
    loop: bool = False

    theme: ReplayTheme = field(default_factory=ReplayTheme)

    agent_palette: list[Color] = field(
        default_factory=lambda: [
            (52, 152, 219),
            (231, 76, 60),
            (46, 204, 113),
            (241, 196, 15),
            (155, 89, 182),
            (230, 126, 34),
            (26, 188, 156),
            (236, 240, 241),
        ]
    )


def _color(value) -> Color:
    if not isinstance(value, list | tuple) or len(value) != 3:
        raise ValueError(f"Expected RGB color [r, g, b], got: {value}")

    return tuple(int(x) for x in value)


def load_render_config(path: str | None) -> ReplayRenderConfig:
    if path is None:
        return ReplayRenderConfig()

    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    default = ReplayRenderConfig()
    theme_data = data.get("theme", {}) or {}

    theme = ReplayTheme(
        background=_color(theme_data.get("background", default.theme.background)),
        grid=_color(theme_data.get("grid", default.theme.grid)),
        obstacle=_color(theme_data.get("obstacle", default.theme.obstacle)),
        collision=_color(theme_data.get("collision", default.theme.collision)),
        text=_color(theme_data.get("text", default.theme.text)),
        sidebar=_color(theme_data.get("sidebar", default.theme.sidebar)),
    )

    palette_data = data.get("agent_palette", default.agent_palette)
    palette = [_color(c) for c in palette_data]

    if not palette:
        raise ValueError("agent_palette must contain at least one RGB color")

    return ReplayRenderConfig(
        fps=float(data.get("fps", default.fps)),
        cell_size_px=int(data.get("cell_size_px", default.cell_size_px)),
        show_grid=bool(data.get("show_grid", default.show_grid)),
        show_goals=bool(data.get("show_goals", default.show_goals)),
        loop=bool(data.get("loop", default.loop)),
        theme=theme,
        agent_palette=palette,
    )