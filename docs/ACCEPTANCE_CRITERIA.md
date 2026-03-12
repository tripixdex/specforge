# Acceptance Criteria

## Stage 5.6 Must Deliver

- a source checkout can be installed with `python3 -m pip install --no-build-isolation -e ".[dev]"`
- documented CLI, API, and UI commands work without `PYTHONPATH=src`
- the deterministic pipeline remains intact and truthful
- the browser UI allows a user to paste a brief, load a bundled demo, run analysis, and run generation
- the UI visibly presents the brief summary, ambiguity findings, contradiction findings, missing decisions, assumptions, recommended MVP cut, artifact previews, and output location
- deterministic human-facing output follows Russian input with Russian text and English input with English text where the system generates findings or artifact copy
- obvious overloaded briefs trigger stronger contradiction detection in both Russian and English
- the browser UI includes a visible `New brief` action that clears stale results and returns the user to Intake
- Cyrillic titles export to readable sanitized or transliterated folder names under `outputs/`
- empty UI sections render explicit states instead of blank-looking boxes
- very short briefs trigger a humane clarification state before the user is overwhelmed by detail
- the documented official human run path is a verified `uvicorn` command
- the FastAPI app remains modular, with UI routing separated from pipeline logic
- API and UI generation both keep outputs under `outputs/`
- validation rejects empty or excessive briefs across surfaces where reasonable
- invalid demo selection and malformed labels are handled explicitly
- a local eval corpus covers at least 15 cases across founder, client, internal, and edge-case briefs
- the eval harness checks structural findings and required artifact generation
- tests cover API behavior, UI route availability, eval loading or execution, and existing CLI behavior

## Stage 5.6 Must Not Claim

- a production-ready hosted web application
- authentication, collaboration, or external integration support
- hidden-context inference
- arbitrary path control for generated output
- benchmark authority beyond the local deterministic rubric
