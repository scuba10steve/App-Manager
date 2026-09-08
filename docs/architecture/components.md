# Components

## Route table

| Method | Path | Resource | Notes |
|---|---|---|---|
| GET | `/apps` | `AppListAPI` (`src/manager/app_list_api.py`) | list all apps |
| DELETE | `/apps` | `AppListAPI` | delete all apps, no confirmation |
| POST | `/app` | `AppRegisterAPI` (`src/manager/app_api.py`) | register a new app |
| DELETE | `/app/<id>` | `AppRegisterAPI` | delete one app (409 if installed) |
| GET | `/app/<id>` | `AppAPI` (`src/manager/app_api.py`) | fetch one app |
| PUT | `/app/<id>` | `AppAPI` | edit one app — **does not persist**, see [../user/api-reference.md](../user/api-reference.md) |
| POST | `/app/<id>/install` | `AppInstallAPI` (`src/installer/installer_api.py`) | run the install |
| DELETE | `/app/<id>/install` | `AppInstallAPI` | run the uninstall — **never actually runs**, see [../user/api-reference.md](../user/api-reference.md) |

`AppAPI` and `AppRegisterAPI` are two separate `flask_restful` resources
both bound to the URL pattern `/app/<int:app_id>` under different endpoint
names (`app_inquiry_update_delete` and `app_registration`, `app.py:58-59`).
This works because the two resources' `app_id`-taking methods don't
overlap (`GET`/`PUT` on `AppAPI` vs. `DELETE` on `AppRegisterAPI`) —
Werkzeug dispatches by method, so both rules coexist on the same path
without conflict for those verbs. There is one exception: `AppRegisterAPI`
is registered on **both** `/app` and `/app/<int:app_id>`
(`api.add_resource(AppRegisterAPI, '/app', '/app/<int:app_id>', ...)`,
`app.py:59`), so `POST /app/<id>` is also routable — it dispatches to
`AppRegisterAPI.post(self)`, which takes no `app_id` parameter, so
Werkzeug's captured `app_id` kwarg makes the call raise `TypeError` (a
`500`). It's a stray, broken route rather than a real capability.

## Module map

| Module | Responsibility |
|---|---|
| `app.py` | Composition root: builds the dependency graph, wires Flask routes, starts the server |
| `src/model/application.py` | `Application` domain object; `ApplicationEncoder`/`ApplicationDecoder` for JSON (de)serialization |
| `src/repository/app_repo.py` | `AppRepository` — SQLite CRUD for apps (`apps.db`) |
| `src/repository/repo_initializer.py` | `AppRepositoryInitializer(AppRepository)` — creates the `APPS`/`SYSTEM_METADATA` schema on first run |
| `src/manager/app_api.py` | `AppAPI` (get/put single app), `AppRegisterAPI` (post/delete single app) |
| `src/manager/app_list_api.py` | `AppListAPI` (get/delete all apps) |
| `src/manager/app_initializer.py` | `ApplicationInitializer` — detects host OS (`platform.system()`) and a default package manager (`choco`/`apt`/`brew`) |
| `src/manager/validator/input_validator.py` | `Validator` — regex URL validation (`https?://.+`), non-empty system-string validation |
| `src/installer/app_downloader.py` | `ApplicationDownloader` — HTTP download to `./working/cache/installers/`, skips re-download if the file already exists |
| `src/installer/app_installer.py` | `ApplicationInstaller` — orchestrates download → runner/extractor lookup → run, and uninstall |
| `src/installer/installer_api.py` | `AppInstallAPI` — the `/app/<id>/install` REST resource |
| `src/installer/factory/installer_factory.py` | `InstallerFactory` — maps a file extension (`exe`/`zip`/`7z`/`rar`) or a package-manager command (`choco`/`brew`) to a runner/extractor instance |
| `src/installer/factory/extractor.py` | `Extractor`, `ZipExtractor`, `SevenZipExtractor`, `RarExtractor` |
| `src/installer/factory/runner.py` | `CommandRunner`, `ChocoRunner`, `HomebrewRunner` — shell out to run an installer or a package manager |
| `src/js/App.js`, `src/js/index.js` | React SPA — see [../user/web-ui.md](../user/web-ui.md) |

## Known defects worth knowing before you touch this code

These are documented here as **current behavior**, not fixed as part of
this documentation task (spec: out of scope):

- **`InstallerFactory` never actually extracts archives.**
  `ApplicationInstaller.install()` (`src/installer/app_installer.py:39-53`)
  only runs the downloaded file if its name matches `self.exec_pattern`
  (`r'.+\.exe'`, an `.exe`). For `zip`/`7z`/`rar` downloads, a runner is
  looked up from `InstallerFactory`, but its `.extract()` method is never
  called — the archive is downloaded and left in
  `./working/cache/installers/`, nothing is installed, and no error is
  raised.
- **The `is_package=True` install branch 500s before it ever reaches a
  package-manager runner, on any platform.**
  `ApplicationInstaller.install()`'s package branch
  (`src/installer/app_installer.py:51-53`) does
  `InstallerFactory().with_command('').find()` — an empty string, which is
  falsy, so `InstallerFactory.find()`'s `if self.command:` check never
  matches and it returns `None` regardless of whether the host's package
  manager is `choco`, `apt`, or `brew`. The very next line,
  `runner.run_cmd(package_manager, [...])`, then raises `AttributeError`
  (an unhandled `500`) because `runner` is `None`. Note the call is
  `run_cmd`, not `run` — `ChocoRunner.run()`/`HomebrewRunner.run()` are
  never reached by this path.
- **`HomebrewRunner.run()` has its own, separate, unreachable bug.**
  `src/installer/factory/runner.py:41-45`:
  ```python
  def run(self, packages, install_dir=None):
      if sys.platform != "linux" or sys.platform != "darwin":
          raise Exception("Not running a *nix plaform!!! ...")
  ```
  `sys.platform` can never equal both `"linux"` and `"darwin"` at once, so
  the `or` makes this condition **always true** — if this method were ever
  called, it would raise unconditionally on Linux, macOS, and Windows
  alike. In practice it's dead code: the live install path above calls
  `run_cmd()` directly and never reaches `HomebrewRunner.run()` (or
  `ChocoRunner.run()`), so this tautology guard is latent, not the actual
  failure mechanism for `is_package=True` installs.
- **`has_installer`/`has_uninstaller` are dead fields.** `Application`
  declares both (`src/model/application.py:14-15`), they're serialized to
  every API response, but nothing in the codebase ever sets either to
  `True`. Treat them as always-`False` placeholders, not real signals.
- **`is_package` always reads back from the database as `False` — for two
  separate, independent reasons.** First: the `PACKAGE` column is bound
  with a Python `bool` (`src/repository/app_repo.py:44`), which `sqlite3`
  coerces to int (`1`/`0`), then SQLite's TEXT affinity converts to string
  (`'1'`/`'0'`) instead of the intended `'True'`/`'False'`.
  `AppRepository.load_app` checks `cols['PACKAGE'] == 'True'`
  (`src/repository/app_repo.py:85`), which never matches `'1'`/`'0'`, so
  `is_package` is reconstructed as `False`. This is what makes the
  package-manager install branch (`src/installer/app_installer.py:50-53`)
  **unreachable through the normal REST flow** (`POST /app/<id>/install`
  on a package registration). Second, and separately: `AppRepository.load_apps()`
  (used by `GET /apps`) doesn't even select the `PACKAGE` column —
  its query is `SELECT ID, NAME, SOURCE_URL, SYSTEM, INSTALLED FROM APPS`
  (`src/repository/app_repo.py:62-63`) — so every app returned from
  `load_apps()` falls back to the `Application` constructor's default,
  which is also `False`. `GET /apps` and `GET /app/<id>`/the install path
  both end up showing `is_package: false`, but via two unrelated bugs.
  See [data-model.md](data-model.md) for the schema details.
- **Uninstall never actually runs, under any condition.**
  `ApplicationInstaller.uninstall()`'s helper `__discover_uninstaller`
  (`src/installer/app_installer.py:80-86`) returns a 2-tuple
  (`(path_or_None, has_uninstaller)`); `uninstall()` then checks `if ext:`
  on that tuple (`src/installer/app_installer.py:73`) — a non-empty tuple
  is always truthy in Python, even `(None, False)`, so this check always
  passes. It then does `self.factory.with_extension(ext[0]).find()`,
  looking up `ext[0]` (a full file path, or `None`, when no uninstaller
  was found) as a key in `InstallerFactory`'s `exe`/`zip`/`7z`/`rar`
  extension dict — which never matches, so `find()` returns `None` and
  `runner` stays falsy. `DELETE /app/<id>/install` therefore always
  returns `204` having done nothing, on every call. See
  [../user/api-reference.md](../user/api-reference.md) for the fuller
  walkthrough.
