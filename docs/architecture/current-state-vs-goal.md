# Current State vs. Scheduler Goal

**This is a gap note, not a design.** The scheduler itself is future work
to be brainstormed separately once the current system is well understood.

## Current state

App-Manager is a single-host application **installer**, not a scheduler.
Every install/uninstall is:

- **Synchronous** — `POST /app/<id>/install` runs the download/extract/run
  (or package-manager) sequence inline in the request thread and only
  responds once it finishes. Flask's built-in dev server (`app.run()`,
  which is what `python app.py` uses — see
  [overview.md](overview.md)) is single-threaded by default, so a
  long-running install blocks every other request.
- **Immediate** — there is no concept of "run this at time T" or "run this
  every N minutes" anywhere in the code or data model. `SYSTEM_METADATA`
  and `APPS` have no scheduling columns.
- **Unauthenticated** — every route in the [route table](components.md#route-table)
  accepts requests from anyone who can reach the port; there's no API key,
  token, or user model.
- **Foreground-only** — running it means keeping `python app.py` attached
  to a terminal (or a process manager you supply yourself, like `systemd`,
  a container, or the Cloud Foundry manifest — see
  [deployment.md](deployment.md)). There's no built-in daemon/service mode.

## Stated goal (as of 2026-09-07)

Revive this project as an **externally controllable scheduler** installed
on a machine — something a remote caller can use to have operations run at
specified times or intervals, not just as an immediate synchronous action.

## The gap, plainly

To get from "installer" to "scheduler" requires, at minimum: a persistence
model for *when* to run something (not just *what* to run), an execution
path that doesn't block the request thread, some notion of authenticating
the external controller, and a way to run unattended as a long-lived
service. None of that exists today. This note exists so that design work
starts from an accurate picture of what's here, not from what the project
name implies.
