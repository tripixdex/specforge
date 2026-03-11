# Stage 4 UI

## What Was Implemented

- added a local browser UI at `/` and `/ui`
- added a guided workflow for loading a demo brief, pasting a brief, running analysis, and generating a bundle
- added visible sections for summary, ambiguity findings, contradiction findings, missing decisions, assumptions, open questions, MVP cut, artifact previews, and output location
- kept the UI local-only and wired it into the existing FastAPI app

## Why This UI Approach Was Chosen

The UI is server-rendered inside FastAPI instead of adding a separate frontend application because that keeps the stack small, local, and easy to explain. It reuses the same runtime, validation rules, and output policy without introducing front-end sprawl.

## Files Added Or Changed

Added:

- [src/specforge/ui/models.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/models.py)
- [src/specforge/ui/service.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/service.py)
- [src/specforge/ui/routes.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/routes.py)
- [src/specforge/ui/templates/index.html](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/templates/index.html)
- [src/specforge/ui/static/specforge.css](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/static/specforge.css)
- [src/specforge/ui/static/specforge_components.css](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/static/specforge_components.css)
- [tests/test_ui.py](/Users/vladgurov/Desktop/work/specforge/tests/test_ui.py)
- [codex_reports/stage_04_ui.md](/Users/vladgurov/Desktop/work/specforge/codex_reports/stage_04_ui.md)

Changed:

- [src/specforge/api/app.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/api/app.py)
- [src/specforge/api/schemas.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/api/schemas.py)
- [pyproject.toml](/Users/vladgurov/Desktop/work/specforge/pyproject.toml)
- [Makefile](/Users/vladgurov/Desktop/work/specforge/Makefile)
- [README.md](/Users/vladgurov/Desktop/work/specforge/README.md)
- [docs/SCOPE.md](/Users/vladgurov/Desktop/work/specforge/docs/SCOPE.md)
- [docs/ACCEPTANCE_CRITERIA.md](/Users/vladgurov/Desktop/work/specforge/docs/ACCEPTANCE_CRITERIA.md)
- [docs/DEMO_SCENARIOS.md](/Users/vladgurov/Desktop/work/specforge/docs/DEMO_SCENARIOS.md)
- [docs/ARCHITECTURE.md](/Users/vladgurov/Desktop/work/specforge/docs/ARCHITECTURE.md)
- [REPORT_INDEX.md](/Users/vladgurov/Desktop/work/specforge/REPORT_INDEX.md)

## Commands Run

```bash
python3 -m pip install --no-build-isolation -e ".[dev]"
make lint
make test
python3 -m specforge.cli demo
python3 -m pytest tests/test_api.py -q
python3 -m pytest tests/test_ui.py -q
python3 - <<'PY'
from fastapi.testclient import TestClient
from specforge.api.app import app

client = TestClient(app)
response = client.get("/demo")
print(response.status_code)
print(response.json()["demo_name"])
PY
python3 - <<'PY'
from fastapi.testclient import TestClient
from specforge.api.app import app

client = TestClient(app)
response = client.get("/ui")
print(response.status_code)
print("SpecForge Stage 4" in response.text)
PY
```

## Results

- editable install verification: passed and installed `specforge 0.5.0`
- `make lint`: passed
- `make test`: passed, `18 passed`
- `python3 -m specforge.cli demo`: passed and generated [outputs/demo-founder-app](/Users/vladgurov/Desktop/work/specforge/outputs/demo-founder-app)
- `python3 -m pytest tests/test_api.py -q`: passed, `7 passed`
- `python3 -m pytest tests/test_ui.py -q`: passed, `3 passed`
- API verification snippet: passed with HTTP `200` and demo name `founder-app-idea`
- UI verification snippet: passed with HTTP `200` and the `SpecForge Stage 4` heading present
- UI generation test produced [outputs/ui-smoke-demo](/Users/vladgurov/Desktop/work/specforge/outputs/ui-smoke-demo)

## Remaining Limitations

- the UI is intentionally server-rendered and simple; it is not a reactive frontend application
- artifact preview is limited to short inline previews rather than a full document viewer
- the UI uses text paste and demo briefs only; it does not accept file uploads in this stage
- the CLI remains more flexible than the browser UI because it still supports custom `--output-root`

## File-Size Concerns

- [src/specforge/ui/templates/index.html](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/templates/index.html) is `241` lines and should be watched if more UI states are added
- the stylesheet was split so [src/specforge/ui/static/specforge.css](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/static/specforge.css) is `238` lines and [src/specforge/ui/static/specforge_components.css](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/static/specforge_components.css) is `174` lines instead of one oversized file
- the UI service and route modules were kept separate to avoid mixing presentation, orchestration, and transport concerns
