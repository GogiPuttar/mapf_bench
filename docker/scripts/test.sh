#!/usr/bin/env bash
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
cd "$REPO_ROOT"

versions=("22.04" "24.04" "devel")

for version in "${versions[@]}"; do
    tag="mapf-bench:ubuntu-${version}"
    docker build \
        --build-arg "UBUNTU_VERSION=${version}" \
        -f docker/Dockerfile \
        -t "$tag" \
        .
    docker run --rm "$tag"
done
