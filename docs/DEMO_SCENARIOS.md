# Demo Scenarios

Stage 5.6 demos now include the deterministic CLI flow, the local FastAPI layer, the guided browser UI, and a local evaluation run, with extra emphasis on trust and human usability before expert review.

## Scenario 1: Contradictory Founder Brief

Input:
- a founder brief that asks for a minimal MVP while also demanding enterprise scope, low budget, and aggressive timing

Implemented behavior:
- detects stronger contradiction patterns for overloaded scope
- surfaces missing decisions around pricing and security
- recommends a narrower MVP cut
- follows the input language in deterministic recommendations

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
- provides a visible `New brief` reset path
- renders explicit empty states and a humane short-brief clarification state
- shows a short repo-local path first, with the full path still available

Verified command:
- `python3 -m pytest tests/test_ui.py -q`

## Scenario 5: Bilingual Smoke Check

Input:
- one Russian founder/client-like brief and one English founder/client-like brief

Implemented behavior:
- Russian input produces Russian deterministic findings and recommendations
- English input produces English deterministic findings and recommendations
- Cyrillic titles export to readable transliterated folder names under `outputs/`

Verified command:
- `python3 -m pytest tests/test_analyze.py -q`

## Scenario 6: Local Evaluation Corpus

Input:
- the Stage 5 eval corpus under `eval/`

Implemented behavior:
- runs 20 deterministic corpus cases
- checks structural expectations such as minimum finding counts, required categories, MVP-cut presence, and required artifacts
- writes inspectable summaries and per-case bundles under `outputs/evals/stage-05/`

Verified command:
- `python3 -m specforge.eval.runner`
