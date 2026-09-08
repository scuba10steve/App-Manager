# Running

Two things need to be running: the Flask **backend** (the API, and the
route that serves the built frontend), and — at least once, to produce
the built bundle — the **frontend** build.

## Backend: the command that actually works

```bash
export PORT=8080     # optional, defaults to 8080 if unset
python app.py
```

This works because `app.py`'s `if __name__ == "__main__":` guard calls
`main()`, which builds the Flask `app` object as a local variable and
calls `app.run(port=port)` directly (see
[../architecture/overview.md](../architecture/overview.md)). Host defaults
to Werkzeug's dev default (`127.0.0.1`) since `app.run()` here is never
given a `host=` argument — for something reachable outside `localhost`,
edit that call or run behind a reverse proxy.

## Backend: the command that does NOT work — do not use it

`scripts/run.sh` and this project's original README both say:

```bash
export FLASK_APP=app.py && export PORT=8080 && flask run --port $PORT --host 0.0.0.0
```

**This fails.** The Flask CLI's app-discovery looks for a module-level
`app`/`application` object or a `create_app`/`make_app` factory function
in the module named by `FLASK_APP`. `app.py` has neither — its `app`
object only exists inside `main()`'s local scope. Running this command
raises Flask's "Failed to find Flask application or factory" error. This
is documented here as a known, pre-existing bug in the repo's own
scripts — not something this documentation pass fixes.

## Frontend

Pick one:

- **Build once, then just run the backend** (closest to how a deployed
  instance behaves):
  ```bash
  npm run build
  python app.py
  ```
  `static/index.html` loads `static/bundle.js` directly; the Flask `/`
  route redirects there. **This did not work cleanly during this
  documentation pass** — see the two build caveats in
  [installation.md](installation.md): plain `npm run build` fails outright
  on current Node.js (`ERR_OSSL_EVP_UNSUPPORTED`), and even with the
  `NODE_OPTIONS=--openssl-legacy-provider` workaround, a separate,
  pre-existing bug in `webpack.config.js`'s `output.path` writes the
  bundle to a sibling directory instead of `static/`. Confirm
  `static/bundle.js` actually exists (and is fresh) before trusting this
  path.
- **Dev mode with hot reload:**
  ```bash
  # terminal 1
  python app.py            # backend on :8080
  # terminal 2
  npm start                 # dev server on :8081, proxies API calls to :8080
  ```
  Visit `http://localhost:8081` — the dev server serves the frontend live
  and forwards everything else to the backend. This mode does not depend
  on `npm run build`'s output location, since `webpack-dev-server` serves
  the bundle from memory rather than writing it to disk.

## Confirm it's up

```bash
curl http://localhost:8080/apps
```

Expect `[]` on a fresh database — `apps.db` is created automatically in
the current working directory on first run
(`AppRepositoryInitializer.initialize()`, see
[../architecture/data-model.md](../architecture/data-model.md)).
