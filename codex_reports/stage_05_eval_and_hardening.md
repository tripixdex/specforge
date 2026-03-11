# Stage 5: Eval And Hardening

## What Was Implemented

- added a local eval corpus under [eval/](/Users/vladgurov/Desktop/work/specforge/eval) with 20 labeled cases across founder, client, internal, and edge-case briefs
- added a typed eval harness in [src/specforge/eval/runner.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/eval/runner.py), [src/specforge/eval/loader.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/eval/loader.py), and [src/specforge/eval/models.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/eval/models.py)
- added shared validation helpers in [src/specforge/input_validation.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/input_validation.py)
- added a shared demo registry in [src/specforge/demo_catalog.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/demo_catalog.py)
- tightened CLI, API, and UI handling for empty or oversized brief text, trimmed labels, and invalid demo selection
- updated docs to reflect the real Stage 5 boundary and eval workflow

## Eval Design

- the corpus uses structural expectations instead of exact wording matches
- each case can require minimum finding counts, required categories, MVP-cut presence, and required artifact files
- the runner executes the existing deterministic pipeline end to end and exports per-case bundles under `outputs/evals/stage-05/`
- the runner writes stable summary artifacts:
  - [eval_summary.json](/Users/vladgurov/Desktop/work/specforge/outputs/evals/stage-05/eval_summary.json)
  - [eval_summary.md](/Users/vladgurov/Desktop/work/specforge/outputs/evals/stage-05/eval_summary.md)

## Hardening Changes

- API and UI now share trimmed optional-field handling instead of relying on raw form text
- CLI file input now uses the same brief-size guardrails as the API and UI
- invalid UI demo identifiers no longer silently fall back without explanation; the page shows the issue and resets to the default demo safely
- API output labels accept surrounding whitespace and still sanitize to safe repo-local names
- the CLI `--output-root` escape hatch remains as-is to avoid behavior regression; this is still an intentional divergence from the stricter API/UI local-only policy

## File Size Review

- [src/specforge/eval/runner.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/eval/runner.py) is the largest new Stage 5 module at 227 lines and stays under the soft review threshold
- [src/specforge/ui/templates/index.html](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/templates/index.html) remains above the soft target but was not expanded materially in Stage 5
- the corpus is split across four files to avoid one oversized monolithic dataset file

## Decisions Kept As-Is

- kept the existing deterministic heuristics rather than redesigning the analyzer
- kept the server-rendered UI approach rather than adding a richer frontend stack
- kept the CLI `--output-root` option for local developer flexibility, but documented the divergence clearly

## Commands Run

```bash
make lint
make test
python3 -m specforge.cli demo
python3 - <<'PY'
from fastapi.testclient import TestClient
from specforge.api.app import app

client = TestClient(app)
response = client.get("/demo")
print("status", response.status_code)
print("demo", response.json()["demo_name"])
PY
python3 - <<'PY'
from fastapi.testclient import TestClient
from specforge.api.app import app

client = TestClient(app)
response = client.get("/ui")
print("status", response.status_code)
print("has_heading", "SpecForge Stage 5" in response.text)
PY
python3 -m specforge.eval.runner
```

## Results

- `make lint`: passed
- `make test`: passed, `23 passed`
- `python3 -m specforge.cli demo`: passed and generated [outputs/demo-founder-app](/Users/vladgurov/Desktop/work/specforge/outputs/demo-founder-app)
- API verification on `/demo`: passed with HTTP `200`
- UI verification on `/ui`: passed with HTTP `200`
- `python3 -m specforge.eval.runner`: passed with `20/20` cases and generated [outputs/evals/stage-05/](/Users/vladgurov/Desktop/work/specforge/outputs/evals/stage-05)

## Remaining Limitations

- the eval rubric is useful and inspectable, but it is not a scientific benchmark
- the deterministic analyzer still uses heuristic rules and can miss nuanced business context
- the browser UI remains intentionally simple and local-only
- the CLI/API output policy divergence still exists and should be revisited only if the CLI contract can change safely

## Readiness Recommendation

READY FOR EXPERT AUDIT
