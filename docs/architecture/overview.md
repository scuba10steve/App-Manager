# System Overview

App-Manager is a Flask REST API backed by SQLite, paired with a minimal
React single-page app, for registering, installing, and uninstalling
applications on the machine it runs on. As of this writing it performs
installs synchronously and immediately — there is no scheduling concept
yet (see [current-state-vs-goal.md](current-state-vs-goal.md)).

## Request lifecycle

```
Browser / curl / Postman
        |
        v
  Flask app (app.py)          <- composition root, wires routes at startup
        |
        v
  flask_restful Resource      <- src/manager/*, src/installer/installer_api.py
        |
        +--> AppRepository (SQLite, apps.db)      src/repository/app_repo.py
        |
        +--> ApplicationInstaller                  src/installer/app_installer.py
                 |
                 +--> ApplicationDownloader (HTTP)  src/installer/app_downloader.py
                 +--> InstallerFactory              src/installer/factory/*
                          |
                          +--> extractors (zip/7z/rar) or
                          +--> command runners (.exe / choco / brew)
```

## Startup sequence

`app.py` builds a global dependency graph at **import time** (module level,
`app.py:19-25`): an `ApplicationEncoder`/`ApplicationDecoder` pair, an
`AppRepository`, an `ApplicationDownloader`, an `AppRepositoryInitializer`,
an `ApplicationInitializer`, and an `ApplicationInstaller` that wires all of
the above together. `main()` then:

1. Reads the `PORT` env var (default `8080`).
2. Creates the Flask `app` object and a `flask_restful.Api`.
3. Calls `initialize_app(app)`, which runs `REPO_INITIALIZER.initialize()`
   (creates the SQLite schema if missing — see
   [data-model.md](data-model.md)) and `APP_INITIALIZER.initialize()`
   (detects the host OS and default package manager, storing it in
   `SYSTEM_METADATA`).
4. Calls `initialize_api(api)`, which registers every route (see
   [components.md](components.md) for the full table).
5. Registers a `/` route that redirects to `/static/index.html` (the built
   React app — see [../user/web-ui.md](../user/web-ui.md)).
6. Calls `app.run(port=port)`.

Because `app` is a **local variable inside `main()`** (`app.py:34`), not a
module-level name, the Flask CLI's app-discovery (`FLASK_APP=app.py flask
run`) cannot find it. The only working start command is `python app.py` —
see [../user/running.md](../user/running.md) for the full explanation and
the broken command it replaces.
