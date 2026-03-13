# Acceptance Criteria

## Current Must Deliver

- a source checkout can be installed with `python3 -m pip install --no-build-isolation -e ".[dev]"`
- documented CLI, API, and UI commands work without `PYTHONPATH=src`
- the deterministic pipeline remains intact and truthful
- the browser UI allows a user to paste a brief, load a bundled demo, run analysis, and run generation
- the UI visibly presents the brief summary, ambiguity findings, contradiction findings, missing decisions, assumptions, recommended MVP cut, human-readable artifact previews, and output location
- deterministic human-facing output follows Russian input with Russian text and English input with English text across CLI summaries, UI labels, and exported artifact copy where the system generates text, including localized product, audience, platform, and tradeoff display values where reasonable
- obvious overloaded briefs trigger stronger contradiction detection in both Russian and English, including realistic phrasing variants rather than only curated happy-path wording
- contradiction output for overloaded briefs stays curated rather than duplicating the same family excessively
- the browser UI includes a visible `New brief` action that clears stale results and returns the user to Intake
- Cyrillic titles export to readable sanitized or transliterated folder names under `outputs/`
- empty UI sections render explicit states instead of blank-looking boxes
- very short briefs trigger a humane clarification state before the user is overwhelmed by detail
- the documented official human run path is a verified `uvicorn` command
- the FastAPI app remains modular, with UI routing separated from pipeline logic
- API and UI generation both keep outputs under `outputs/`
- validation rejects empty or excessive briefs across surfaces where reasonable
- invalid demo selection and malformed labels are handled explicitly
- a local eval corpus covers at least 20 cases across founder, client, internal, and edge-case briefs
- the eval harness checks structural findings, contradiction ceilings for curated overload cases, required contradiction families for realistic overload variants, and required artifact generation
- tests cover API behavior, UI route availability, eval loading or execution, and existing CLI behavior

## Current Must Not Claim

- a production-ready hosted web application
- authentication, collaboration, or external integration support
- hidden-context inference
- arbitrary path control for generated output
- benchmark authority beyond the local deterministic rubric
- full semantic understanding of every freeform brief variant
