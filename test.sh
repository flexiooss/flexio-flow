#!/usr/bin/env bash

ROOT_PWD=$PWD
cd $PWD'/src/tests'
if [ $# -ne 0 ]
then
  python3.7 "$@"
else
  python3.7 tests.py
fi

cd $ROOT_PWD