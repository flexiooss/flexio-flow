#!/usr/bin/env bash

ROOT_PWD=$PWD
PWD=$PWD'/src'
echo $PWD
#python3 -m mypy --ignore-missing-imports main.py "$@"
python3 -m mypy $PWD/main.py "$@"
PWD=ROOT_PWD