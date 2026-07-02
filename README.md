# mapf_bench
A standardized MAPF/LMAPF benchmark and plugin harness that can preserve legacy algorithms like PRIMAL2 while making new MarmotLab methods easier to compare, test, and deploy.

## Development

Install the package in editable mode:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest
```

Run an example scenario:

```bash
mapf-bench run \
  --scenario examples/scenarios/two_agents_swap.yaml \
  --solver wait \
  --out runs/wait_test
```

## Docker

Build and test the default Ubuntu image:

```bash
docker build -f docker/Dockerfile -t mapf-bench:24.04 .
docker run --rm mapf-bench:24.04
```

Select another Ubuntu base image with `UBUNTU_VERSION`:

```bash
docker build --build-arg UBUNTU_VERSION=22.04 -f docker/Dockerfile -t mapf-bench:22.04 .
```

Run the supported Docker matrix:

```bash
docker/scripts/test.sh
```

The matrix covers Ubuntu `22.04`, `24.04`, `26.04`, and `devel`.
