#!/usr/bin/env sh

python3 -m venv packages/
# shellcheck disable=SC2039
source packages/bin/activate

python3 -m pip install -r requirements.txt
