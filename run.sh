#!/usr/bin/env bash
FLASK_APP="app.py"
PORT=8080

export FLASK_APP && export PORT && flask run --port $PORT --host 0.0.0.0