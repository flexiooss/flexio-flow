#!/usr/bin/env bash

ROOT_PWD=$PWD
cd $PWD'/src'
python3.7 -m mypy main.py "$@"
cd $ROOT_PWD