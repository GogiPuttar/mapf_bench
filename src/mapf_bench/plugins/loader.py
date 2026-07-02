from __future__ import annotations

import importlib
from typing import Any

from mapf_bench.plugins.base import PathfinderPlugin
from mapf_bench.plugins.builtin import BuiltinStepPathfinder
from mapf_bench.plugins.config import PluginConfig, load_plugin_config


def load_pathfinder_from_file(path: str) -> PathfinderPlugin:
    config = load_plugin_config(path)
    return load_pathfinder(config)


def load_pathfinder(config: PluginConfig) -> PathfinderPlugin:
    if config.type == "builtin":
        if not config.name:
            raise ValueError("Builtin plugin config requires 'name'")

        plugin = BuiltinStepPathfinder(config.name)
        plugin.configure(config.params)
        return plugin

    if config.type == "python":
        if not config.module or not config.class_name:
            raise ValueError("Python plugin config requires 'module' and 'class'")

        module = importlib.import_module(config.module)
        cls = getattr(module, config.class_name)
        plugin = cls()
        plugin.configure(config.params)
        return plugin

    raise ValueError(f"Unsupported plugin type: {config.type}")