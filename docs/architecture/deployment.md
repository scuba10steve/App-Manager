# Deployment & CI

Three deployment/CI paths exist in this repo, of differing vintage and
reliability. None are scheduler-aware — see
[current-state-vs-goal.md](current-state-vs-goal.md).

## GitHub Actions (`.github/workflows/github-actions.yml`) — current

Runs on push/PR to the default branch: installs `p7zip-full`, installs
`pylint`/`pytest` plus `requirements.txt` with a plain global `pip install`
(no virtualenv), runs `pylint *`, then runs `scripts/test.sh`.

**Known defect:** `scripts/test.sh` only executes the test suite when a
`./venv` directory exists:

```bash
if [[ -d ./venv ]]; then
    . ./venv/bin/activate
    python -m unittest discover tests/
else
    echo "no virtualenv"
fi
```

Because the GitHub Actions job never creates a `venv` (it installs
dependencies globally), this branch always takes the `else` path — it
prints `"no virtualenv"` and exits `0` **without running any tests**. The
"Test with unittest" CI step has always been green, but it has never
actually executed `tests/`. `pylint *` (the previous step) does still run
for real.

## Travis CI (`.travis.yml`) — legacy

Predates the GitHub Actions workflow. Builds a virtualenv, installs
`requirements.txt` into it, runs `pylint *` then
`python -m unittest discover tests/` directly (not through
`scripts/test.sh`, so this path *did* run tests for real). On a tagged
build it also runs `scripts/package.py $TRAVIS_TAG` and uploads the
resulting archives to GitHub Releases. Travis's free tier for open-source
projects has been wound down industry-wide since this was set up — treat
this pipeline as dormant unless you've independently confirmed the Travis
org/repo link still runs builds.

## `scripts/package.py` — release packaging

Zips/tars `src/`, `app.py`, `package.json`, `requirements.txt`, and
`webpack.config.js` into `build/package-<version>.{zip,tar.bz2}`.

**Known gap:** it does not include `static/` — the built frontend bundle
(`static/bundle.js`, produced by `npm run build`, see
[../user/installation.md](../user/installation.md)) is absent from every
release package this script produces. A package installed from a tagged
release has a working API but no working web UI until someone builds the
frontend separately.

## Cloud Foundry (`deploy/manifest.yml`)

```yaml
applications:
- name: app-manager
  command: flask run --port $PORT --host 0.0.0.0
  env:
    FLASK_APP: app.py
```

This `cf push` manifest starts the app with `flask run`, which — as
documented in [overview.md](overview.md) and
[../user/running.md](../user/running.md) — cannot find `app.py`'s Flask
`app` object (it's local to `main()`, not module-level). Pushing this
manifest as-is would fail to start. Treat it as stale until the entry
point mismatch is fixed.
