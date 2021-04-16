#!/usr/bin/env bash
if [[ -d ./venv ]]; then
    . ./venv/bin/activate

    python -m unittest discover tests/
else
    echo "no virtualenv"
fi