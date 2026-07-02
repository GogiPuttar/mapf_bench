from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Literal

import yaml


@dataclass(frozen=True)
class PluginConfig:
    type: Literal["builtin", "python"]
    name: str | None = None
    module: str | None = None
    class_name: str | None = None
    params: dict[str, Any] = field(default_factory=dict)


def load_plugin_config(path: str) -> PluginConfig:
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    plugin_type = data.get("type")
    if plugin_type not in {"builtin", "python"}:
        raise ValueError(f"Unsupported plugin type: {plugin_type}")

    return PluginConfig(
        type=plugin_type,
        name=data.get("name"),
        module=data.get("module"),
        class_name=data.get("class") or data.get("class_name"),
        params=data.get("params", {}) or {},
    )