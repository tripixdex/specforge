# Stage 3 Report

## Changes Made

- added a modular FastAPI package at [src/specforge/api/app.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/api/app.py), [src/specforge/api/routes.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/api/routes.py), [src/specforge/api/schemas.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/api/schemas.py), and [src/specforge/api/service.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/api/service.py)
- implemented typed endpoints for `GET /health`, `POST /analyze`, `POST /generate`, and `GET /demo`
- added request validation for empty and oversized briefs and normalized JSON error responses
- enforced a repo-local API output policy under `outputs/` with sanitized output labels
- kept the Stage 2 deterministic pipeline and CLI behavior intact
- updated packaging to support a normal editable install workflow without documented `PYTHONPATH=src` hacks
- added an `api` Make target and updated Stage 3 docs to describe the real local API surface and limits
- added API tests covering health, analyze, generate, validation failure, response shape, and safe output handling

## Commands Run

```bash
python3 -m pip install --no-build-isolation -e ".[dev]"
make lint
make test
python3 -m specforge.cli demo
python3 - <<'PY'
from fastapi.testclient import TestClient
from specforge.api.app import app

client = TestClient(app)
response = client.post(
    "/generate",
    json={
        "brief_text": "Internal Ops Tool\nGoals:\n- Reduce reporting work\nConstraints:\n- Keep it local-first\n- Budget under $10k\n",
        "title": "Internal Ops Tool",
        "output_label": "stage3-api-demo",
    },
)
print(response.status_code)
print(response.json()["output_path"])
PY
```

## Results

- editable install succeeded and `specforge==0.4.0` was installed in editable mode
- `make lint`: passed
- `make test`: passed, `15 passed`
- `python3 -m specforge.cli demo`: passed and generated [outputs/demo-founder-app](/Users/vladgurov/Desktop/work/specforge/outputs/demo-founder-app)
- API verification: passed with HTTP `200` and generated [outputs/stage3-api-demo](/Users/vladgurov/Desktop/work/specforge/outputs/stage3-api-demo)
- confirmed generated bundles remained under [outputs/](/Users/vladgurov/Desktop/work/specforge/outputs)

## Known Limitations

- the API is local demo software only; it does not provide auth, persistence, rate limiting, or production hardening
- `/demo` returns a fixed bundled sample instead of a configurable demo catalog
- the deterministic analyzer remains heuristic and cannot infer hidden business context
- the CLI still allows a caller to choose `--output-root`; the stricter repo-local output policy is enforced for the API surface

## Sample Generated Bundle

- API sample bundle: [outputs/stage3-api-demo](/Users/vladgurov/Desktop/work/specforge/outputs/stage3-api-demo)

## What Remains For Stage 4

- decide whether the next interface is a browser UI, richer local project history, or an optional assisted-analysis layer
- add clearer demo workflows for comparing sample briefs through the API
- improve local observability and packaging polish if a stronger reviewer demo is needed
