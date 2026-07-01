from mapf_bench.render.ascii import _frame_to_ascii, _clear_screen
from mapf_bench.render.config import ReplayRenderConfig


def test_ascii_contains_agent():
    frame = {
        "step": 0,
        "positions": {
            "a0": [1, 2],
        },
        "vertex_collisions": [],
        "edge_collisions": [],
        "invalid_moves": [],
    }

    out = _frame_to_ascii(
        width=4,
        height=4,
        obstacles=set(),
        goals={},
        frame=frame,
        config=ReplayRenderConfig(),
    )

    assert "a0" in out

def test_ascii_contains_obstacle():
    frame = {
        "step": 0,
        "positions": {},
        "vertex_collisions": [],
        "edge_collisions": [],
        "invalid_moves": [],
    }

    out = _frame_to_ascii(
        width=2,
        height=2,
        obstacles={(0, 0)},
        goals={},
        frame=frame,
        config=ReplayRenderConfig(),
    )

    assert "■■" in out

def test_ascii_contains_indexed_goal():
    frame = {
        "step": 0,
        "positions": {},
        "vertex_collisions": [],
        "edge_collisions": [],
        "invalid_moves": [],
    }

    out = _frame_to_ascii(
        width=2,
        height=2,
        obstacles=set(),
        goals={"a0": (1, 1)},
        frame=frame,
        config=ReplayRenderConfig(show_goals=True),
    )

    assert "g0" in out


def test_clear_screen_does_not_fail_without_term(monkeypatch):
    monkeypatch.delenv("TERM", raising=False)
    _clear_screen()