# App-Manager
[![Build Status](https://travis-ci.org/scuba10steve/App-Manager.svg?branch=master)](https://travis-ci.org/scuba10steve/App-Manager)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/3bc6bf2c2e7745dfae80ad74054fedcd)](https://www.codacy.com/app/scuba10steve/App-Manager?utm_source=github.com&utm_medium=referral&utm_content=scuba10steve/App-Manager&utm_campaign=Badge_Grade)

A pythonic application manager to manage applications as if they were
packages — a Flask REST API + React UI for registering and installing
apps on a host machine. Currently being revived as the base for an
externally controllable scheduler.

## Quickstart

```bash
python -m venv venv && . venv/bin/activate
pip install -r requirements.txt
npm install && npm run build
python app.py
```

Then visit `http://localhost:8080`.

Both `pip install -r requirements.txt` and `npm run build` have known,
current issues (stale pinned versions; a Node/OpenSSL incompatibility and
a wrong output path) — see [installation.md](docs/user/installation.md)
before assuming this happy path works unmodified.

## Documentation

- [Architecture docs](docs/architecture/index.md) — how it's built
- [User docs](docs/user/index.md) — installation, running, the API, and the web UI

For contributors/agents working in this repo, see [AGENTS.md](AGENTS.md).
