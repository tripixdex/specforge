# Demo Scenarios

Stage 4 demos now include the deterministic CLI flow, the local FastAPI layer, and a guided browser UI.

## Scenario 1: Contradictory Founder Brief

Input:
- a founder brief that asks for a minimal MVP while also demanding enterprise scope, low budget, and aggressive timing

Implemented behavior:
- detects contradiction patterns
- surfaces missing decisions around pricing and security
- recommends a narrower MVP cut

Verified command:
- `python3 -m specforge.cli analyze --input examples/contradictory_founder_brief.txt`

## Scenario 2: Internal Tool Bundle Generation

Input:
- an internal operations brief with clear local-first signals and a limited budget

Implemented behavior:
- identifies internal-tool assumptions
- carries analysis results into generation
- exports a bundle under `outputs/`

Verified command:
- `python3 -m specforge.cli generate --input examples/internal_operations_tool_brief.txt`

## Scenario 3: Local API Demo

Input:
- the bundled founder app brief served through `/demo`

Implemented behavior:
- returns a typed JSON response with deterministic analysis data
- exposes counts, open questions, and recommended MVP cuts
- keeps all processing local

Verified command:
- `python3 -m pytest tests/test_api.py -q`

## Scenario 4: Guided Browser Demo

Input:
- a pasted or bundled brief loaded through `/ui`

Implemented behavior:
- presents a recruiter-demo-friendly workflow instead of raw JSON
- highlights contradictions and unresolved questions visually
- allows analysis and generation from one local UI surface
- previews exported artifacts and shows the repo-local output directory

Verified command:
- `python3 -m pytest tests/test_ui.py -q`
