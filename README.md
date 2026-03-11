# SpecForge

SpecForge is a local-first demo application that turns messy product briefs into a deterministic analysis and a repo-local delivery bundle. Stage 5 keeps the existing CLI, API, and browser UI intact while adding a real evaluation corpus and a small hardening pass.

This is still local demo software. It is not a hosted service, not a SaaS product, and not a fake autonomous product manager.

The repository follows stage-based development and prefers small, responsibility-focused modules over oversized files where practical.

## Stage 5 Capabilities

Implemented now:

- deterministic intake, analysis, generation, and export pipeline
- rule-based ambiguity, contradiction, missing-decision, and assumption analysis
- CLI flows for `analyze`, `generate`, and `demo`
- typed FastAPI endpoints for `/health`, `/analyze`, `/generate`, and `/demo`
- local browser UI at `/` and `/ui`
- guided UI workflow for pasted briefs, demo brief selection, analysis, and generation
- evaluation corpus under `eval/` with 20 local cases
- local eval harness that scores structural expectations and artifact completeness
- safe repo-local bundle generation under `outputs/`
- tighter shared validation for empty, oversized, and malformed local inputs

Still out of scope:

- cloud deployment
- authentication
- external integrations
- required LLM analysis
- arbitrary filesystem export locations from the API or UI

## Install

Verified local workflow from a source checkout:

```bash
python3 -m pip install --no-build-isolation -e ".[dev]"
```

## Run

CLI:

```bash
python3 -m specforge.cli analyze --input examples/contradictory_founder_brief.txt
python3 -m specforge.cli generate --input examples/internal_operations_tool_brief.txt
python3 -m specforge.cli demo
```

API and UI:

```bash
make api
make ui
python3 -m uvicorn specforge.api.app:app --reload
```

Evaluation:

```bash
make eval
python3 -m specforge.eval.runner
python3 -m specforge.eval.runner --case-id internal_clear_local_tool
```

Then open:

```text
http://127.0.0.1:8000/
http://127.0.0.1:8000/ui
```

Example API requests:

```bash
curl -s http://127.0.0.1:8000/health
curl -s http://127.0.0.1:8000/demo
curl -s \
  -X POST http://127.0.0.1:8000/analyze \
  -H "content-type: application/json" \
  -d '{"brief_text":"Need a local-first brief analysis tool.","title":"Local API Demo"}'
```

The UI and API both keep generated bundles under [outputs/](/Users/vladgurov/Desktop/work/specforge/outputs). The browser UI does not upload files and does not accept arbitrary output paths.
The CLI intentionally still allows `--output-root` for local developer flexibility. That divergence remains documented and intentional.

## UI Workflow

The browser UI is a guided local workflow:

- load a bundled demo brief or paste your own
- run deterministic analysis
- inspect ambiguities, contradictions, missing decisions, assumptions, open questions, and the recommended MVP cut
- generate a repo-local bundle and preview the exported artifacts

## Eval Workflow

Stage 5 adds a local evaluation layer:

- corpus files live under [eval/](/Users/vladgurov/Desktop/work/specforge/eval)
- the corpus covers vague founder briefs, contradictory founder briefs, underspecified client briefs, realistic SMB briefs, noisy internal-tool briefs, impossible-triangle cases, and subtle near-miss ambiguities
- expectations are structural rather than brittle exact-text matches
- eval bundles and summaries land under [outputs/evals/](/Users/vladgurov/Desktop/work/specforge/outputs/evals)

## Verification

Verified commands for Stage 5:

```bash
make lint
make test
python3 -m specforge.cli demo
python3 -m pytest tests/test_api.py -q
python3 -m pytest tests/test_ui.py -q
python3 -m specforge.eval.runner
```

## Limits

SpecForge can:

- surface obvious planning gaps from plain text
- provide a guided local UI for demoing the deterministic workflow
- generate a repo-local bundle with markdown and JSON artifacts
- expose the same core flow through CLI, API, and UI surfaces
- score a local evaluation corpus with inspectable deterministic checks

SpecForge cannot:

- infer hidden business context reliably
- replace stakeholder discovery
- behave like a production web service
- write bundles outside the local repo through the API or UI
- act like a benchmarked production planning engine

## Example Inputs

Sample briefs live in [examples/contradictory_founder_brief.txt](/Users/vladgurov/Desktop/work/specforge/examples/contradictory_founder_brief.txt), [examples/agency_client_brief.txt](/Users/vladgurov/Desktop/work/specforge/examples/agency_client_brief.txt), [examples/internal_operations_tool_brief.txt](/Users/vladgurov/Desktop/work/specforge/examples/internal_operations_tool_brief.txt), and [examples/founder_app_idea.txt](/Users/vladgurov/Desktop/work/specforge/examples/founder_app_idea.txt). The Stage 5 evaluation corpus lives under [eval/](/Users/vladgurov/Desktop/work/specforge/eval).

See [docs/SCOPE.md](/Users/vladgurov/Desktop/work/specforge/docs/SCOPE.md), [docs/ARCHITECTURE.md](/Users/vladgurov/Desktop/work/specforge/docs/ARCHITECTURE.md), [docs/ACCEPTANCE_CRITERIA.md](/Users/vladgurov/Desktop/work/specforge/docs/ACCEPTANCE_CRITERIA.md), [docs/DEMO_SCENARIOS.md](/Users/vladgurov/Desktop/work/specforge/docs/DEMO_SCENARIOS.md), [docs/EVAL_PLAN.md](/Users/vladgurov/Desktop/work/specforge/docs/EVAL_PLAN.md), and [REPORT_INDEX.md](/Users/vladgurov/Desktop/work/specforge/REPORT_INDEX.md) for the exact Stage 5 boundary.
