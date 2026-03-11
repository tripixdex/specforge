# Stage 3.1 Architecture Cleanup

## What Was Inspected

- pipeline module sizes and responsibility boundaries across [src/specforge/pipeline/](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline)
- FastAPI package separation across [src/specforge/api/](/Users/vladgurov/Desktop/work/specforge/src/specforge/api)
- CLI and API output-policy behavior
- legacy reporting layout and report discoverability

## What Changed

- split the overloaded analysis implementation so [analyze.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analyze.py) is now orchestration-only
- moved low-level analysis signals into [analysis_signals.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_signals.py)
- moved assumption-specific logic into [analysis_assumptions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_assumptions.py)
- moved ambiguity, contradiction, and missing-decision rules into [analysis_findings.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_findings.py)
- moved higher-level outcome assembly into [analysis_outcomes.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_outcomes.py)
- moved markdown renderers out of [export.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export.py) into [export_render.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export_render.py)
- added [REPORT_INDEX.md](/Users/vladgurov/Desktop/work/specforge/REPORT_INDEX.md) and the new primary per-stage report directory [codex_reports/](/Users/vladgurov/Desktop/work/specforge/codex_reports)
- added lightweight repository hygiene notes to [README.md](/Users/vladgurov/Desktop/work/specforge/README.md) and [docs/ARCHITECTURE.md](/Users/vladgurov/Desktop/work/specforge/docs/ARCHITECTURE.md)
- added a pointer-style [REPORT.md](/Users/vladgurov/Desktop/work/specforge/REPORT.md) so old expectations do not silently break

## Architectural Findings

- The FastAPI layer was already cleanly separated into app, routes, schemas, and service modules. No business logic was living in route handlers.
- The biggest maintainability issue was the deterministic pipeline, not the API layer.
- The prior [analyze.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analyze.py) was too large and mixed orchestration, heuristics, rule predicates, and output shaping.
- The prior [export.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export.py) mixed filesystem writes with all markdown rendering logic.
- `intake.py` is still moderately large, but its responsibility remains cohesive enough to keep as-is for now.

## File Size Findings

Initial audit candidates:

- `774` lines: [analyze.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analyze.py)
- `336` lines: [export.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export.py)
- `292` lines: [intake.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/intake.py)

Post-cleanup pipeline sizes:

- `73` lines: [analyze.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analyze.py)
- `97` lines: [export.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export.py)
- `255` lines: [export_render.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export_render.py)
- `292` lines: [intake.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/intake.py)
- `245` lines: [analysis_signals.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_signals.py)
- `123` lines: [analysis_ambiguities.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_ambiguities.py)
- `195` lines: [analysis_decisions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_decisions.py)
- `112` lines: [analysis_outcomes.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_outcomes.py)
- `88` lines: [analysis_assumptions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_assumptions.py)

Assessment:

- `analyze.py` and `export.py` were not acceptable at their previous sizes because they mixed multiple responsibilities.
- `intake.py` remains a review candidate by size, but the content is still one cohesive normalization pass, so it was left unchanged.
- `export_render.py` is still above the preferred threshold, but it is a renderer-only module now. Keeping the renderers together is more maintainable than arbitrarily fragmenting them by markdown file.
- the first split of the analysis layer was not sufficient because one findings module still landed above the target threshold, so it was split again into ambiguity and decision-focused modules.

## CLI And API Consistency

- The CLI and API both run the same deterministic intake/analyze/generate pipeline.
- The API intentionally enforces a stricter output policy by always exporting under repo-local `outputs/` and sanitizing `output_label`.
- The CLI still accepts `--output-root`. This is a real divergence, but it is preserved intentionally to avoid regressing documented CLI behavior.
- The difference is acceptable for now because the API is the constrained local demo surface, while the CLI remains a more flexible local developer tool.

## Decisions To Keep As-Is

- kept [intake.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/intake.py) unsplit because its size comes from one normalization responsibility rather than mixed concerns
- kept the CLI `--output-root` option to avoid behavior regression
- preserved the legacy `codex reports/` directory instead of renaming or rewriting old reports

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
print(response.status_code)
print(response.json()["demo_name"])
PY
```

## Results

- `make lint`: passed
- `make test`: passed
- `python3 -m specforge.cli demo`: passed
- API verification via `TestClient` on `GET /demo`: passed with HTTP `200`

## Remaining Architecture Risks

- [intake.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/intake.py) is still near the upper size limit and may need splitting if more normalization rules are added
- [export_render.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export_render.py) could become oversized again if many new artifact formats are added
- the CLI/API output-policy difference must stay documented until there is an explicit decision to unify it
- the legacy `codex reports/` path contains stage history outside the new primary reporting convention
