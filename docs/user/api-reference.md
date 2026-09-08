# API Reference

All endpoints are unauthenticated JSON over HTTP. A ready-made client for
manual testing ships in the repo root: `postman_collection.json` (import
into Postman; set a `manager` collection variable to your host:port).

Route table: see
[../architecture/components.md#route-table](../architecture/components.md#route-table).

## `GET /apps`

Returns every registered app as a JSON array. Fields per app: `name`,
`source_url`, `system`, `app_id`, `installed`, `has_installer` (always
`false` — see [../architecture/components.md](../architecture/components.md#known-defects-worth-knowing-before-you-touch-this-code)),
`has_uninstaller` (same), `is_package`.

## `DELETE /apps`

Deletes every row in `APPS`. No confirmation prompt, no dry-run. Returns
`204`.

## `POST /app`

Body:
```json
{
  "name": "app-manager",
  "source_url": "https://example.com/app.exe",
  "system": "windows",
  "is_package": false
}
```
If `is_package` is falsy, `source_url` must match `https?://.+` or the
request is rejected. `system` must be a non-empty string either way.
Returns `{"resource_uri": "/app/<id>"}`.

**Upsert-by-identity:** if an app with the same `name` + `system` +
`is_package` already exists, this returns that app's existing `id`
instead of creating a duplicate row (`AppRepository.store_app`).

## `DELETE /app/<id>`

`404` if the app doesn't exist. `409` if `installed` is currently `true`
(uninstall it first — see below). Otherwise `204` and the row is removed.

## `GET /app/<id>`

`200` with the app's JSON, or `404`.

## `PUT /app/<id>`

Body: `{"source_url": ..., "system": ..., "name": ...}`, same validation
as `POST /app`.

**Known bug — does not persist.** The handler sets the new values on the
in-memory `Application` object and returns it via `jsonify(app)`, but
never calls the repository's `update_app()`. The response looks like the
edit succeeded; a subsequent `GET /app/<id>` will show the **old**
values. See `src/manager/app_api.py`'s `AppAPI.put`.

## `POST /app/<id>/install`

Synchronous — the request blocks until the install finishes. Returns
`204` on success. Unlike `PUT`, this path **does** persist: on success it
sets `installed=True` and calls `update_app()`. Raises an unhandled
exception (`500`) if `app_id` doesn't exist.

What actually happens depends on `is_package`:

- **`is_package: false`** — downloads `source_url` to
  `./working/cache/installers/<name>.<ext>` (extension sniffed from the
  URL path, or from the response's `Content-Disposition` header). Only
  `.exe` downloads are actually run (Windows-only, via silent-install
  flags). `.zip`/`.7z`/`.rar` downloads are fetched but **never
  extracted or installed** — see
  [../architecture/components.md](../architecture/components.md#known-defects-worth-knowing-before-you-touch-this-code).
- **`is_package: true`** — shells out to the host's detected package
  manager instead of downloading anything. On Windows this uses `choco`.
  Package-manager installs targeting Homebrew are currently
  **always broken** regardless of platform — see the `HomebrewRunner`
  defect in
  [../architecture/components.md](../architecture/components.md#known-defects-worth-knowing-before-you-touch-this-code).

## `DELETE /app/<id>/install`

Uninstall. Only works if the app was installed via the `.exe` path (an
uninstaller is discovered by scanning the install directory for any
`.exe` file) and only actually runs on `sys.platform == 'win32'`.
Otherwise this silently does nothing and still returns `204` — no error
is raised if uninstall wasn't actually possible.
