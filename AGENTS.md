# AGENTS.md

Read these before making changes:

- [docs/architecture/index.md](docs/architecture/index.md) — what
  App-Manager is and how it's built
- [docs/user/index.md](docs/user/index.md) — how to install, run, and
  call it

Both are tables of contents; follow the links inside them for detail.
This file intentionally doesn't repeat their content.

## Verification

This repo has both a Python backend and a Node frontend.

- **Python:** `pylint *` and `python -m unittest discover tests/`, run
  directly (not via `scripts/test.sh` — that script silently no-ops
  unless a `./venv` directory exists; see
  [docs/architecture/deployment.md](docs/architecture/deployment.md)).
  Requires the dependencies in `requirements.txt` installed first.
- **Frontend:** `npm run build` must succeed if you touch anything under
  `src/js/` or `webpack.config.js`. There is no meaningful `npm test` —
  `jest` is configured but no test files exist yet.
- **Docs-only changes** (like this one): no code verification needed.
  Confirm internal doc links resolve and `git diff --stat` is scoped to
  `docs/`, `README.md`, and `AGENTS.md`.

Run the Python and/or frontend check above before committing, matching
whichever part of the tree you touched.
