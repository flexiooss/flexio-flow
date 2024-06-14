#!/usr/bin/env bash
set -e

CURRENT_PWD=$PWD
SCRIPT_DIR=$(dirname $(readlink -f $0))

cd ${SCRIPT_DIR}

python3 -m venv ${SCRIPT_DIR}/venv
source ${SCRIPT_DIR}/venv/bin/activate

#python3 -m pip install --upgrade pip
python3 -m ensurepip --upgrade


set +e

python3 -m pip install "cython<3.0.0" wheel
python3 -m pip install "pyyaml==6.0.1" --no-build-isolation
python3 -m pip install -r ${SCRIPT_DIR}/requirements.txt

cd ${CURRENT_PWD}
