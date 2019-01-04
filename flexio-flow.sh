#!/usr/bin/env bash

SCRIPT_DIR=$(dirname $(readlink -f $0))

source ${SCRIPT_DIR}/venv/bin/activate
python3.7 ${SCRIPT_DIR}/src/main.py "$@"
deactivate