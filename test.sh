#!/usr/bin/env bash

ROOT_PWD=$PWD
cd $PWD'/src'
if [ $# -ne 0 ]
then
  python3 -m unittest "$@"
else
  python3 -m unittest tests.tests
fi

cd $ROOT_PWD