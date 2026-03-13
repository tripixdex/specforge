# SpecForge

Local-first deterministic tool that turns messy product briefs into structured analysis, planning signals, and a repo-local delivery bundle.

## Why it matters

SpecForge is strongest as a portfolio piece when it is read as an ambiguity-to-structure workflow: take an underspecified brief, surface what is unclear or contradictory, and produce artifacts that make the next product conversation sharper.

## Capabilities

- Deterministic intake, analysis, generation, and export pipeline
- Rule-based ambiguity, contradiction, missing-decision, and assumption analysis
- CLI, FastAPI API, browser UI, and a bundled demo path
- Repo-local export bundles under `outputs/`
- Evaluation corpus with 26 local cases and structural checks
- English and Russian outputs that track input language

## Quick Demo

Install from a source checkout:

```bash
python3 -m pip install --no-build-isolation -e ".[dev]"
```

Fastest showcase path:

```bash
python3 -m specforge.cli demo
```

Browser demo:

```bash
python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8000
```

Then open `http://127.0.0.1:8000/ui`.

Useful CLI examples:

```bash
python3 -m specforge.cli analyze --input examples/contradictory_founder_brief.txt
python3 -m specforge.cli generate --input examples/internal_operations_tool_brief.txt
```

## Verification

The lightweight verification path for this repo is:

```bash
make lint
python3 -m pytest tests/test_api.py -q
python3 -m specforge.cli demo
python3 -m specforge.eval.runner --case-id internal_clear_local_tool
```

This checks style, API behavior, the main demo bundle path, and one focused eval case without starting a broad audit cycle.

## Demo Surface

- `GET /health`
- `GET /demo`
- `POST /analyze`
- `POST /generate`
- `GET /`
- `GET /ui`

The UI and API keep generated bundles under [outputs/](/Users/vladgurov/Desktop/work/specforge/outputs). The browser flow does not upload files and does not allow arbitrary export paths.

## Limitations

- This is local demo software, not a hosted product planning platform
- The analysis is deterministic and rule-based; it does not replace stakeholder discovery
- No auth, collaboration, cloud deployment, or external integrations
- API and UI exports stay repo-local by design
- Output quality depends on the brief containing enough concrete detail to reason about

## Why it is interesting in a portfolio

This repo shows product-thinking mechanics in code: input validation, deterministic analysis, multi-surface delivery, inspectable artifacts, and honest boundaries around what automation can and cannot infer.

## Example Inputs and Artifacts

Sample briefs live in [examples/founder_app_idea.txt](/Users/vladgurov/Desktop/work/specforge/examples/founder_app_idea.txt), [examples/contradictory_founder_brief.txt](/Users/vladgurov/Desktop/work/specforge/examples/contradictory_founder_brief.txt), [examples/agency_client_brief.txt](/Users/vladgurov/Desktop/work/specforge/examples/agency_client_brief.txt), and [examples/internal_operations_tool_brief.txt](/Users/vladgurov/Desktop/work/specforge/examples/internal_operations_tool_brief.txt).

The strongest existing showcase bundle is [outputs/demo-founder-app/analysis_report.md](/Users/vladgurov/Desktop/work/specforge/outputs/demo-founder-app/analysis_report.md) plus the related files in [outputs/demo-founder-app](/Users/vladgurov/Desktop/work/specforge/outputs/demo-founder-app).

## Docs

- [docs/DEMO_SCENARIOS.md](/Users/vladgurov/Desktop/work/specforge/docs/DEMO_SCENARIOS.md)
- [docs/ARCHITECTURE.md](/Users/vladgurov/Desktop/work/specforge/docs/ARCHITECTURE.md)
- [docs/SCOPE.md](/Users/vladgurov/Desktop/work/specforge/docs/SCOPE.md)
- [docs/EVAL_PLAN.md](/Users/vladgurov/Desktop/work/specforge/docs/EVAL_PLAN.md)
