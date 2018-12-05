#!/usr/bin/env bash

ROOT_PWD=$PWD
cd $PWD'/src'
echo $PWD
#python3 -m mypy --ignore-missing-imports main.py "$@"
python3 -m mypy main.py "$@"
cd $ROOT_PWD