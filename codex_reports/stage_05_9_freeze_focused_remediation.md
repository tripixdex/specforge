# Stage 5.9 Freeze-Focused Remediation

## Summary
Stage 5.9 was a narrow remediation pass aimed only at the remaining re-audit blockers before a final freeze decision:

1. contradiction detection missed realistic overloaded English and Russian phrasing
2. Russian human-facing output still leaked English display values in exports
3. generated artifacts were valid but still had a few prototype-smelling weak spots

This pass did not add major new features, did not redesign the product, and did not introduce LLM behavior.

## Re-audit blockers addressed

### 1. Contradiction detection hardening
Addressed by:
- widening team-size extraction for realistic phrasing such as `team is just two people`, `me and one contractor`, and `команда всего 2 человека`
- broadening short-timeline, scope-breadth, multi-platform, and overloaded-integration detection
- keeping contradiction families based on normalized signals rather than only narrow phrase matches
- preserving contradiction curation so overload cases still collapse to the expected three families instead of duplicating noisy variants

### 2. Language consistency hardening
Addressed by:
- adding a small display-localization layer for product type, audience, audience mode, platform hints, and tradeoff labels
- using localized display values in generated Russian markdown artifacts
- reducing obvious mixed-language leakage in Russian human-facing outputs

### 3. Small artifact usefulness pass
Addressed by:
- tightening inferred goal normalization so one huge overloaded paragraph is less likely to become a single raw “goal”
- making recommended MVP cuts more explicit about:
  - what stays in
  - what gets deferred
  - what should be decided first
- slightly strengthening the summary wording and downstream artifact content without turning this stage into a broad content rewrite

## Files changed

### Core logic
- `src/specforge/pipeline/analysis_signals.py`
- `src/specforge/pipeline/analysis_contradictions.py`
- `src/specforge/pipeline/intake.py`
- `src/specforge/pipeline/analysis_outcomes.py`
- `src/specforge/pipeline/generate.py`
- `src/specforge/pipeline/analysis_assumptions.py`
- `src/specforge/pipeline/language.py`
- `src/specforge/pipeline/export_render.py`

### API/UI stage truth updates
- `src/specforge/api/app.py`
- `src/specforge/api/schemas.py`
- `src/specforge/ui/copy.py`

### Tests
- `tests/test_analyze.py`
- `tests/test_api.py`
- `tests/test_eval.py`
- `tests/test_generate_export.py`
- `tests/test_ui.py`

### Eval corpus
- `eval/founder_cases.json`
- `eval/edge_cases.json`

### Minimal docs
- `README.md`
- `docs/EVAL_PLAN.md`
- `docs/ACCEPTANCE_CRITERIA.md`
- `docs/DEMO_SCENARIOS.md`
- `REPORT_INDEX.md`
- `pyproject.toml`

## New tests and eval cases

### New regression tests
- realistic English overloaded wording triggers all three curated contradiction families
- realistic Russian overloaded wording triggers all three curated contradiction families
- near-miss broad-but-resourced brief remains restrained
- Russian export uses localized human-facing values
- English export remains cleanly English-facing

### New eval cases
- `founder_en_realistic_overloaded_phrase_variant`
- `founder_ru_realistic_overloaded_phrase_variant`
- `edge_resourced_enterprise_near_miss`

The eval corpus now contains 25 cases.

## Commands run

```bash
make lint
make test
python3 -m specforge.cli analyze --input /tmp/specforge_stage59_en_overloaded.txt
python3 -m specforge.cli analyze --input /tmp/specforge_stage59_ru_overloaded.txt
python3 -m specforge.cli analyze --input /tmp/specforge_stage59_near_miss.txt
python3 -m specforge.cli generate --input /tmp/specforge_stage59_ru_export.txt --output-root outputs --run-label stage59-ru-export
python3 -m specforge.cli generate --input /tmp/specforge_stage59_en_export.txt --output-root outputs --run-label stage59-en-export
python3 -m specforge.eval.runner
python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8000
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/analyze -H 'content-type: application/json' -d '{...}'
curl -s -X POST http://127.0.0.1:8000/ui/analyze -F 'title=Stage 5.9 UI Check' -F 'brief_text=...' -F 'demo_name=founder-app-idea'
```

## Results

### Lint and tests
- `make lint`: passed
- `make test`: passed
- total tests: `35`

### Smoke checks
- realistic EN overloaded brief: `Contradictions: 3`
- realistic RU overloaded brief: `Противоречия: 3`
- near-miss contradiction brief: `Contradictions: 0`
- RU export language smoke check:
  - localized values observed: `программный инструмент`, `операционная команда`, `локальная работа`
  - obvious English display leakage removed from the checked fields
- EN export language smoke check:
  - retained English-facing values such as `internal tool`, `operations team`, `local-first`

### Eval
- `python3 -m specforge.eval.runner`: passed
- cases: `25`
- passed: `25`
- failed: `0`
- score: `100.0`

### API/UI verification
- API health returned `stage-5-9-freeze-focused-remediation`
- API analyze returned `contradictions: 3` on the realistic Russian overloaded brief
- UI analyze rendered `SpecForge Stage 5.9` with Russian localized contradiction cards and `Противоречия: 3`

## Remaining limitations
- contradiction detection is stronger and less phrase-fragile, but it remains a deterministic heuristic system rather than a general semantic planner
- Russian wording is materially cleaner, but some phrases remain intentionally simple rather than stylistically polished
- generated artifacts are stronger and less dump-like, but they are still compact planning aids rather than full delivery specifications
- the API still returns canonical structured values in some machine-oriented fields, which is acceptable for this local deterministic MVP

## Recommendation
`READY FOR FINAL RE-AUDIT`
