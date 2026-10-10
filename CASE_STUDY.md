# Case study: Incident Workflow Lab

## 1. Problem and intended user

The original fictional history simulator is preserved. The featured application now supports creating actual local records, changing states and reading durable event histories.

## 2. Data and information flow

Create incident → check version → validate transition → append durable event

## 3. Why these choices

SQLite stores incidents and events inside one transaction. BEGIN IMMEDIATE serializes writers. Each transition requires the expected version; stale edits return HTTP 409. A per-incident request key recognizes an identical retry and prevents duplicate events. Parameterized SQL avoids interpolating user input. Invalid transitions roll back.

## 4. Reproducible evidence

| Measurement | Result |
|---|---|
| retry does not duplicate | True |
| stale write rejected | True |
| persisted state after reopen | Resolved |
| events after resolution | 3 |

Generated at 2026-10-10T18:37:13.555378+00:00 by the Python benchmark. Read every run in [benchmark-results.json](benchmark-results.json). These results apply only to the documented benchmark. No production performance claim is made.

## 5. What could go wrong

No authentication, access control, alert integration or multi-user hosted service is provided. Keep the Python service on localhost. The public single-device simulation cannot demonstrate database concurrency; Python tests do. Request-key scope is one incident, and creation itself is not idempotent.

## 6. Next substantive improvement

Añade idempotencia también a la creación y una prueba de dos escritores concurrentes. Para alojarlo en un servidor, diseña autenticación y permisos antes de exponer datos.

Open an issue, create a branch, implement the improvement, run the checks, and explain the change in a pull request. Do not describe automated report commits as personal code development.
