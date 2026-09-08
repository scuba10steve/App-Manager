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
| DELETE | `/app/<id>/install` | `AppInstallAPI` | run the uninstall |

`AppAPI` and `AppRegisterAPI` are two separate `flask_restful` resources
both bound to the URL pattern `/app/<int:app_id>` under different endpoint
names (`app_inquiry_update_delete` and `app_registration`, `app.py:58-59`).
This works because the two resources define non-overlapping HTTP methods
(`GET`/`PUT` vs. `DELETE`) — Werkzeug dispatches by method, so both rules
coexist on the same path without conflict.

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
- **`HomebrewRunner.run()` always raises, on every platform.**
  `src/installer/factory/runner.py:41-45`:
  ```python
  def run(self, packages, install_dir=None):
      if sys.platform != "linux" or sys.platform != "darwin":
          raise Exception("Not running a *nix plaform!!! ...")
  ```
  `sys.platform` can never equal both `"linux"` and `"darwin"` at once, so
  the `or` makes this condition **always true** — the guard fires
  unconditionally, on Linux, macOS, and Windows alike. `is_package=True`
  installs targeting `brew` cannot currently succeed on any platform.
- **`has_installer`/`has_uninstaller` are dead fields.** `Application`
  declares both (`src/model/application.py:14-15`), they're serialized to
  every API response, but nothing in the codebase ever sets either to
  `True`. Treat them as always-`False` placeholders, not real signals.
- **`is_package` always reads back from the database as `False`.** The
  `PACKAGE` column is bound with a Python `bool` (`src/repository/app_repo.py:44`),
  which `sqlite3` coerces to int (`1`/`0`), then SQLite's TEXT affinity converts
  to string (`'1'`/`'0'`) instead of the intended `'True'`/`'False'`.
  `AppRepository.load_app` checks `cols['PACKAGE'] == 'True'` (`src/repository/app_repo.py:85`),
  which never matches `'1'`/`'0'`, so `is_package` is reconstructed as `False`.
  This makes the package-manager install branch (`src/installer/app_installer.py:50-53`)
  **unreachable through the normal REST flow** (`POST /app/<id>/install` on a package registration).
  See [data-model.md](data-model.md) for the schema details.
