# mapf_bench

`mapf_bench` is a lightweight benchmarking framework for **Multi-Agent Path Finding (MAPF)** and **Lifelong MAPF (LMAPF)** algorithms.

The goal is to provide a common interface for evaluating, visualizing, and comparing different planning algorithms—from classical search methods to reinforcement learning policies—while minimizing code duplication and preserving reproducibility.

Long-term, `mapf_bench` aims to serve as a plugin-based benchmark harness capable of running legacy planners (e.g. PRIMAL2) alongside modern algorithms using a shared simulator, metrics pipeline, and visualization tools.

---

# Features

Current capabilities include:

* Grid-based MAPF simulator
* Built-in baseline planners

  * Wait
  * Random
  * Greedy
* Replay generation
* ASCII replay renderer
* Interactive pygame replay viewer
* Configurable rendering themes and agent palettes
* Automated testing across multiple Ubuntu versions
* Docker-based development and CI environments

---

# Installation

Clone the repository and install in editable mode:

```bash
pip install -e ".[dev]"
```

To enable the pygame replay viewer:

```bash
pip install -e ".[gui]"
```

---

# Running a Benchmark

Run one of the example scenarios:

```bash
mapf-bench run \
    --scenario examples/scenarios/two_agents_swap.yaml \
    --solver greedy \
    --out runs/greedy_demo
```

This generates a replay and metrics in:

```text
runs/greedy_demo/
├── metrics.json
└── replay.json
```

---

# Replay Visualization

### ASCII

```bash
mapf-bench replay \
    runs/greedy_demo/replay.json \
    --config examples/render/ascii.yaml
```

### GUI (pygame)

```bash
mapf-bench replay \
    runs/greedy_demo/replay.json \
    --mode gui \
    --config examples/render/gui.yaml
```

The GUI renderer supports configurable themes, agent color palettes, replay speed, and display options via YAML configuration.

---

# Testing

Run the unit test suite:

```bash
pytest
```

---

# Docker

Build the default development image:

```bash
docker build \
    -f docker/Dockerfile \
    -t mapf-bench:24.04 .
```

Build using a different Ubuntu base:

```bash
docker build \
    --build-arg UBUNTU_VERSION=22.04 \
    -f docker/Dockerfile \
    -t mapf-bench:22.04 .
```

Run the complete Docker compatibility matrix:

```bash
docker/scripts/test.sh
```

The Docker test matrix currently validates:

* Ubuntu 22.04
* Ubuntu 24.04
* Ubuntu 26.04
* Ubuntu devel (forward-compatibility)

---

# Continuous Integration

Every pull request automatically runs:

* Unit tests
* CLI smoke tests
* Replay smoke tests
* Docker build and test matrix

This helps ensure the framework remains reproducible and resilient to dependency and platform changes.

---

# Roadmap

Near-term goals include:

* Configurable solver plugin interface
* External planner adapters (e.g. PRIMAL2)
* Standardized benchmark datasets
* Richer evaluation metrics
* Additional replay backends (SVG, web, ROS 2)
* ROS 2 integration for hardware benchmarking
