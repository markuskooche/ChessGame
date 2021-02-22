#!/usr/bin/env sh

python -m venv packages/
# shellcheck disable=SC2039
source packages/bin/activate

python3 main.py
