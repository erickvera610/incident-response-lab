# Incident Workflow Lab

The original fictional history simulator is preserved. The featured application now supports creating actual local records, changing states and reading durable event histories.

**[Open the live demo](https://erickvera610.github.io/incident-response-lab/)** · [Spanish tutorial](TUTORIAL_ES.md) · [Case study](CASE_STUDY.md) · [Measured results](benchmark-results.json)

## Understand it in one minute

Create incident → check version → validate transition → append durable event

SQLite stores incidents and events inside one transaction. BEGIN IMMEDIATE serializes writers. Each transition requires the expected version; stale edits return HTTP 409. A per-incident request key recognizes an identical retry and prevents duplicate events. Parameterized SQL avoids interpolating user input. Invalid transitions roll back.

## Measured evidence

Reproduced with Python by `python benchmark.py`. Execution timestamp is recorded in the JSON report. Synthetic JavaScript values may differ because the random generator differs.

| Measurement | Result |
|---|---|
| retry does not duplicate | True |
| stale write rejected | True |
| persisted state after reopen | Resolved |
| events after resolution | 3 |

## Run locally

Python 3.11 or 3.12, standard library only. No API keys.

```bash
git clone https://github.com/erickvera610/incident-response-lab.git
cd incident-response-lab
python app.py
```

Open http://127.0.0.1:8000. Stop with Ctrl+C. The public browser demo requires no installation.

## Reproduce and inspect

```bash
python -m unittest discover -v
node test_enhanced.cjs
python benchmark.py
python daily_exercise.py
```

Run `python app.py`, open localhost, create an incident and move Open → Investigating → Resolved → Closed. Restart the server to confirm persistence. Public browser storage uses localStorage and is not a shared service.

## Read the source

- `core.py`: public algorithm entry point and preserved original exercise.
- `store.py`: featured implementation.
- `enhanced.js`: browser implementation, readable without a build system.
- `app.py`: localhost HTTP API.
- `test_*.py` and `test_enhanced.cjs`: behavior and edge cases.
- `benchmark.py`: evidence generator.

## Limitations

No authentication, access control, alert integration or multi-user hosted service is provided. Keep the Python service on localhost. The public single-device simulation cannot demonstrate database concurrency; Python tests do. Request-key scope is one incident, and creation itself is not idempotent.

## Daily practical exercises

One dated fictional scenario runs daily through GitHub Actions. `exercises/YYYY-MM-DD/result.json` preserves inputs and outputs; `samples/latest.json` holds the latest input. Bot-authored report commits document script execution, not manual daily development. [Daily Spanish guide](EJERCICIOS_DIARIOS_ES.md).

## Authorship and relevance

Independent AI-assisted learning project in Erik Vera's portfolio. No affiliation with FOX, Tesla or BCG. The documentation distinguishes supplied implementation from improvements the learner actually makes. Code is MIT licensed; third-party data provenance is documented separately.

## Featured portfolio

- [Road Vision Lab](https://github.com/erickvera610/road-vision-lab)
- [Demand Forecasting Lab](https://github.com/erickvera610/consulting-demand-lab)
- [Media Prediction Lab](https://github.com/erickvera610/media-content-lab)
- [Classification Evaluation Lab](https://github.com/erickvera610/ml-model-lab)
- [Incident Workflow Lab](https://github.com/erickvera610/incident-response-lab)
