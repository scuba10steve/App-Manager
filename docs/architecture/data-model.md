# Data Model

## `Application` (`src/model/application.py`)

| Field | Type | Notes |
|---|---|---|
| `name` | str | |
| `source_url` | str | download URL; unused/ignored when `is_package=True` |
| `system` | str | free-text OS/target label, e.g. `"linux"` |
| `app_id` | int | `0` until persisted; assigned by SQLite `AUTOINCREMENT`-free `INTEGER PRIMARY KEY` |
| `installed` | bool | |
| `has_installer` | bool | **dead field** — always `False`, see [components.md](components.md#known-defects-worth-knowing-before-you-touch-this-code) |
| `has_uninstaller` | bool | **dead field** — always `False`, same as above |
| `is_package` | bool | `True` routes install through a system package manager instead of a direct download |

Serialized via `ApplicationEncoder` (a `json.JSONEncoder` subclass,
`app.json_encoder = ApplicationEncoder` in `app.py:53`) which dumps
`__dict__` directly — every field above appears in every API response.
`ApplicationDecoder.decode(json_string)` is the inverse but is only
exercised by the test suite; no production code path calls it.

## SQLite schema (`apps.db`, created by `AppRepositoryInitializer`)

### `APPS`

| Column | Type | Notes |
|---|---|---|
| `ID` | INTEGER | primary key |
| `NAME` | TEXT | |
| `SOURCE_URL` | TEXT | |
| `SYSTEM` | TEXT | |
| `INSTALLED` | TEXT | stores the **string** `'True'`/`'False'`, not a SQLite boolean/integer |
| `PACKAGE` | TEXT | same string-boolean convention as `INSTALLED` |

Indexes: `IDX_DEFAULT` on `(NAME, SYSTEM, SOURCE_URL)`, `IDX_INSTALLED` on
`(INSTALLED)`. There is **no `UNIQUE` constraint** — de-duplication on
`(NAME, SYSTEM, PACKAGE)` happens in application code
(`AppRepository.store_app`, `src/repository/app_repo.py:34-41`) by
selecting before inserting; a second registration with the same
name/system/is_package returns the existing row's `ID` instead of creating
a duplicate.

### `SYSTEM_METADATA`

| Column | Type | Notes |
|---|---|---|
| `SYS_ID` | TEXT | host OS, from `platform.system()` (`"Linux"`/`"Windows"`/`"Darwin"`) |
| `SYS_VERSION` | TEXT | from `platform.version()` |
| `PK_MANAGER` | TEXT | detected default package manager (`apt`/`choco`/`brew`) |

Populated once at startup by `ApplicationInitializer.initialize()` →
`AppRepositoryInitializer.store_sys_metadata()`
(`src/repository/repo_initializer.py:85-93`), which inserts a row only if
one doesn't already exist for that `SYS_ID`.

The database file defaults to `apps.db` in the process's current working
directory (`AppRepository.__init__`, `src/repository/app_repo.py:13-16`) —
there's no configurable path today.
