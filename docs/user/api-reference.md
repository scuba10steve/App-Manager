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
`has_uninstaller` (same), `is_package` (always `false` — the `PACKAGE` column is
not even selected by `load_apps()`, so the field defaults to `false` in every
response).

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

Body: `{"source_url": ..., "system": ..., "name": ...}`. Validation is stricter
than `POST /app` — URL is validated unconditionally, regardless of `is_package`
(which is not even accepted as a parameter on this endpoint).

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
- **`is_package: true`** — effectively unreachable via the normal REST flow
  (since `is_package` always returns `false` from `GET /apps`, as documented above).
  If somehow reached, would shell out to the host's detected package manager
  instead of downloading. See
  [../architecture/components.md](../architecture/components.md#known-defects-worth-knowing-before-you-touch-this-code)
  for the full mechanism.

## `DELETE /app/<id>/install`

Uninstall. **Does not actually run under any condition** — always returns
`204` having done nothing. The implementation discovers an uninstaller by
scanning the install directory for `.exe` files, but due to a tuple-truthiness
bug (`__discover_uninstaller` returns a 2-tuple that is always truthy, then
attempts to look up element 0 — which may be a full file path or `None` — as
an extension key in `InstallerFactory`'s extension dict), the runner is never
resolved, and the uninstall branch is unreachable. See
[../architecture/components.md](../architecture/components.md#known-defects-worth-knowing-before-you-touch-this-code)
for details.
