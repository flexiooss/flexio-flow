#!/usr/bin/env bash
python3 -m mypy --ignore-missing-imports ./src/main.py "$@"