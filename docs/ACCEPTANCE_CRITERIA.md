# Acceptance Criteria

## Stage 4 Must Deliver

- a source checkout can be installed with `python3 -m pip install --no-build-isolation -e ".[dev]"`
- documented CLI, API, and UI commands work without `PYTHONPATH=src`
- the deterministic pipeline remains intact and truthful
- the browser UI allows a user to paste a brief, load a bundled demo, run analysis, and run generation
- the UI visibly presents the brief summary, ambiguity findings, contradiction findings, missing decisions, assumptions, recommended MVP cut, artifact previews, and output location
- the FastAPI app remains modular, with UI routing separated from pipeline logic
- API and UI generation both keep outputs under `outputs/`
- validation still rejects empty or excessive briefs
- tests cover API behavior, UI route availability, at least one UI render flow, and existing CLI behavior

## Stage 4 Must Not Claim

- a production-ready hosted web application
- authentication, collaboration, or external integration support
- hidden-context inference
- arbitrary path control for generated output
