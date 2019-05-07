#!/usr/bin/env bash
set -e
python3.7 -m venv $PWD/venv
source $PWD/venv/bin/activate
python3.7 -m pip install --upgrade pip

set +e
python3.7 -m pip install -r requirements.txt
