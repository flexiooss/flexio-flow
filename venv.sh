#!/usr/bin/env bash
set -e
if [ ! -f /usr/bin/python3.7 ]; then
    echo "Python 3.7 is required"
    exit 1
fi
python3.7 -m venv $PWD/venv
source $PWD/venv/bin/activate
python3.7 -m pip install --upgrade pip

set +e
python3.7 -m pip install -r requirements.txt
