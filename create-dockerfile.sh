#!/bin/bash

set -e
export DOCKER_BUILDKIT=1

for one in */config.yaml; do
    python3 create-dockerfile.py -o ${one%/*} ${one}
done