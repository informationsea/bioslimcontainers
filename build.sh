#!/bin/bash

set -e
export DOCKER_BUILDKIT=1

for one in */config.yaml; do
    echo "Buiding" ${one}
    python3 create-dockerfile.py -b -o ${one%/*} ${one}
done