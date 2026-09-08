# Deployment & CI

Three deployment/CI paths exist in this repo, of differing vintage and
reliability. None are scheduler-aware — see
[current-state-vs-goal.md](current-state-vs-goal.md).

## GitHub Actions (`.github/workflows/github-actions.yml`) — current

**Known defect: this workflow has never actually run.** Its trigger is:

```yaml
on:
  push:
    branches: [ $default-branch ]
  pull_request:
    branches: [ $default-branch ]
```

`$default-branch` is an unsubstituted GitHub starter-workflow template
placeholder. GitHub does **not** interpolate it in `on:` branch filters —
it's matched as a literal branch name, and no branch is actually named
`$default-branch`. This repo's real default branch is `master`, so
neither trigger ever fires; the workflow has never executed on this repo,
period. (If it ever were retargeted at `master`, it would then: install
`p7zip-full`, install `pylint`/`pytest` plus `requirements.txt` with a
plain global `pip install` (no virtualenv), run `pylint *`, then run
`scripts/test.sh`.)

**A second, independent defect** would still make the test step a no-op
even if the trigger were fixed: `scripts/test.sh` only executes the test
suite when a `./venv` directory exists:

```bash
if [[ -d ./venv ]]; then
    . ./venv/bin/activate
    python -m unittest discover tests/
else
    echo "no virtualenv"
fi
```

The workflow's "Install dependencies" step installs everything globally
and never creates a `venv`, so `scripts/test.sh` would always take the
`else` path — print `"no virtualenv"` and exit `0` — without running
`tests/`. Both defects would need fixing (the trigger, and the venv
guard) before this workflow would actually lint or test anything.

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
frontend separately — and, per the caveats in
[../user/installation.md](../user/installation.md), `npm run build`
currently fails outright on modern Node and lands its output in the wrong
directory even when it does run, so "build it yourself" is not a
one-command fix today.

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
