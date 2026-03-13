# Stage 6.3 Public Path Cleanup

## Blockers Addressed

- Russian public export cleanup: localized public analysis count labels in `analysis_report.md` and removed public `source_type` leakage from analysis and assumption-ledger exports.
- Stage/remediation wording removal: removed the public UI eyebrow stage label and removed the public `/health` stage field.
- Raw internal JSON metadata in UI preview: kept `summary.json` in the generated bundle, but removed it from the default artifact preview and replaced it with a small collapsed technical-details note.

## Files Changed

- `src/specforge/pipeline/export_render.py`
- `src/specforge/ui/copy.py`
- `src/specforge/ui/models.py`
- `src/specforge/ui/service.py`
- `src/specforge/ui/templates/index.html`
- `src/specforge/api/schemas.py`
- `tests/test_api.py`
- `tests/test_generate_export.py`
- `tests/test_ui.py`
- `README.md`
- `docs/DEMO_SCENARIOS.md`
- `docs/ACCEPTANCE_CRITERIA.md`
- `REPORT_INDEX.md`

## Commands Run

- `make lint`
- `make test`
- `python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8012`
- `curl -s http://127.0.0.1:8012/health`
- `curl -s http://127.0.0.1:8012/demo`
- `curl -s http://127.0.0.1:8012/ui | rg -n "SpecForge|Stage 5\\.9|New brief|Start with analysis" -n -S`
- `curl -s -X POST http://127.0.0.1:8012/generate -H 'content-type: application/json' --data @.tmp/ru_generate_payload.json`
- `curl -s -X POST http://127.0.0.1:8012/ui/generate -d title='EN UI Preview Audit' --data-urlencode brief_text@.tmp/en_public_path_brief.txt -d output_label='stage63-en-ui' -d demo_name='founder-app-idea'`
- `sed -n '1,120p' outputs/stage63-ru-api/analysis_report.md`
- `rg -n "source_type|Тип источника|unresolved|explicit|inferred|ambiguities|contradictions|missing_decisions|open_questions|assumptions" outputs/stage63-ru-api/analysis_report.md outputs/stage63-ru-api/assumption_ledger.md -S`
- `rg -n "Stage 5\\.9|stage-5-9|summary\\.json" .tmp/stage63_ui_generate.html outputs/stage63-en-ui -S`

## Results

- `make lint`: passed.
- `make test`: passed, `39 passed`.
- RU export public-path smoke check: passed. `outputs/stage63-ru-api/analysis_report.md` rendered Russian-facing count labels and finding sections without `source_type`, `explicit`, `inferred`, or English count keys.
- UI preview smoke check: passed. The rendered generation page showed only human-readable artifact previews and a collapsed technical-details note instead of raw `summary.json` content.
- API verification path: passed. `/health` returned `{"status":"ok","app":"specforge"}` and `/generate` produced a repo-local bundle under `outputs/stage63-ru-api`.
- Quick manual/demo verification path: passed. `/demo` returned a stable deterministic sample and `/ui` rendered `SpecForge` without stage/remediation wording.

## Public-Path Residual Risk

- I did not find remaining stage/remediation wording in the public UI, the public health response, or the inspected generated public artifacts.
- `summary.json` still exists in the bundle as an internal/export artifact, but it is no longer previewed in the default public UI path.
- Historical stage references remain in repository docs and report history, which is acceptable for internal/project-history context and outside this cleanup scope.

## Recommendation

READY FOR FINAL FREEZE-CHECK
