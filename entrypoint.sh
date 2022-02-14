#!/bin/bash
set -e

for PYTHON in /opt/python/*/bin/python; do
    $PYTHON -m build --wheel /app
done
