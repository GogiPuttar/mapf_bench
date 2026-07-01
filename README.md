# mapf_bench
A standardized MAPF/LMAPF benchmark and plugin harness that can preserve legacy algorithms like PRIMAL2 while making new MarmotLab methods easier to compare, test, and deploy.

## Instructions

### Build

```
cd mapf_bench
pip install -e .
```

or

```
pip install -e ".[dev]"
```

### Test

```
cd mapf_bench
pytest
```

### Run

```
mapf-bench run   --scenario examples/scenarios/two_agents_swap.yaml   --solver wait   --out runs/wait_test
```
