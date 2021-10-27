#!/bin/bash

A=\
../python-algo-me/boss_beating_strats.py

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )/../python-algo-me/" && pwd )"
${PYTHON_CMD:-python3} -u "$DIR/$A"
