# Installation

## Prerequisites

- Python 3.6+ (CI currently targets 3.9 in
  `.github/workflows/github-actions.yml`; the pinned versions in
  `requirements.txt` are from 2019-2020 and are not verified to install
  cleanly on modern Python — see the caveat below).
- Node.js + npm, for building the React frontend. **As documented below,
  `npm run build` was not verified to produce a working `static/bundle.js`
  on current tooling — read the Frontend caveat before relying on it.**
- `p7zip` (the `7z` command) on your `PATH` if you need `.7z`/`.rar`
  extraction support — `pyunpack` shells out to it. CI installs it via
  `apt-get install p7zip-full`.

## Backend (Python) dependencies

```bash
python -m venv venv
. venv/bin/activate            # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Caveat:** `requirements.txt` pins exact, several-years-old versions
(e.g. `Flask==1.1.1`, `Werkzeug==1.0.0`) that are not verified to install
on a current Python 3.x — if `pip install` fails on version resolution,
you'll need to update the pins yourself; that's a real maintenance task.

## Frontend (Node) dependencies

```bash
npm install
```

`package.json` lives at the repo root alongside `app.py`. Two npm scripts
matter:

- `npm run build` — runs webpack once, producing `static/bundle.js` (see
  `webpack.config.js`'s `output.path`). Required before `python app.py`
  will serve a working web UI — see the build caveat immediately below,
  which currently fails on modern tooling.
- `npm start` — runs `webpack-dev-server` on port `8081` with a catch-all
  proxy to `http://localhost:8080` (`webpack.config.js`'s
  `devServer.proxy`), for frontend development against a backend you run
  separately. See [running.md](running.md).

**Caveat — `npm run build` does not work out of the box.** Two separate,
real problems exist:

1. **Plain `npm run build` fails outright on current Node.js.** On the
   Node version used to verify this doc (`v26.8.1`), it fails immediately
   with:

   ```
   Error: error:0308010C:digital envelope routines::unsupported
       at new Hash (node:internal/crypto/hash:112:19)
       ...
     code: 'ERR_OSSL_EVP_UNSUPPORTED'
   ```

   This is the incompatibility between webpack 4's default (MD4-based)
   module hashing and OpenSSL 3, which Node.js has used by default since
   Node 17 — an environment/tooling mismatch, not a code defect;
   `package.json` pins `webpack@^4.42.0`, which predates OpenSSL 3. A
   known workaround:

   ```bash
   NODE_OPTIONS=--openssl-legacy-provider npm run build
   ```

   It is not applied anywhere in this repo's own scripts or CI (CI does
   not run the frontend build at all — see
   `.github/workflows/github-actions.yml`), and upgrading webpack is the
   real long-term fix.

2. **Even with that workaround, the build does not land in `static/`.**
   `webpack.config.js` sets:

   ```js
   output: {
     path: __dirname + './static/',
     ...
   }
   ```

   `__dirname` has no trailing slash, so this is plain string
   concatenation, not a path join — it produces `.../<checkout-dir
   name>./static/` (note the literal `.` glued onto the checkout
   directory's name) instead of `.../<checkout-dir name>/static/`. After
   a successful build, the real `static/` directory in the repo still
   had no `bundle.js`, while a sibling directory one level up — named
   after this checkout's directory with a `.` appended — did.

   This is a pre-existing bug in `webpack.config.js`, independent of the
   Node/OpenSSL issue above, and it means `npm run build`'s output is not
   reliably usable as-is on **any** Node version. If you hit this, either
   fix `output.path` to `path.join(__dirname, 'static')` (or
   `path.resolve(__dirname, 'static')`) and rebuild, or manually move the
   built `bundle.js`/`bundle.js.map` into the repo's `static/` directory
   after each build. Like the broken `flask run` path documented in
   [running.md](running.md), this is a known, pre-existing repo issue.

Continue to [running.md](running.md) once both sets of dependencies are
installed.
