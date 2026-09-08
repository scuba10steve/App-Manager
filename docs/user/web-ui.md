# Web UI

The React SPA (`src/js/App.js`) loads the current app list from `GET
/apps` on mount and renders two panes: a left-hand list of app names, and
a right-hand detail table for whichever app is selected.

## What actually works

- Browsing the registered-apps list.
- Selecting an app to view its `id`, `name`, `source_url`, `system`, and
  an `installed` toggle in the detail pane.

## What's wired up but non-functional

- **"Add app" icon** (the `AddCircle` icon next to the list) calls
  `displayCreateAppModal`, which is an empty stub
  (`src/js/App.js`) — clicking it does nothing.
- **"Installed" switch** in the detail pane calls `handleInstalled` on
  change, which only sets local component state
  (`this.setState({selected_app: {installed: event.target.value}})`) —
  it never calls the API, so toggling it does not install or uninstall
  anything. It also replaces the entire `selected_app` object with just
  `{installed: ...}`, dropping every other field, which visibly breaks
  the rest of the detail pane until you re-select the app from the list.

There is currently **no** UI for registering a new app, deleting an app,
or triggering install/uninstall — those require calling the API directly
(curl, the Postman collection, or `scripts/init-app.sh` as an example).
See [api-reference.md](api-reference.md).

## Static assets

`static/index.html`, `static/manifest.json`, `static/favicon.ico` are
checked into the repo. `static/bundle.js` is **not** — it's produced by
`npm run build` (see [installation.md](installation.md)) and is what
`index.html` actually loads.
