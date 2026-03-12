# Stage 6.1 Smallest Blockers Remediation

## Scope

This pass addressed only the remaining blockers from the final re-audit:

1. near-miss contradiction calibration
2. Russian export leakage cleanup
3. Russian budget phrasing support
4. README/docs truth fix
5. minimum regression coverage to keep those fixes from regressing

## Blockers Addressed

### 1. Near-miss contradiction calibration

Problem from re-audit:
- a realistic near-miss brief produced 2 contradiction findings when it should have stayed quiet

Change made:
- stopped treating generic `budget` mentions as budget-pressure tradeoffs
- stopped treating `post-MVP` as a positive MVP trigger
- stopped counting deferred later-phase platform scope as immediate multi-platform scope
- narrowed broad-scope keywords so generic `dashboard` or `analytics` mentions alone do not over-trigger overload logic

Verified result:
- realistic EN overloaded smoke check still returns `Contradictions: 3`
- realistic RU overloaded smoke check still returns `Противоречия: 3`
- realistic near-miss smoke check now returns `Contradictions: 0`

### 2. Russian export leakage cleanup

Problem from re-audit:
- Russian-facing exports still leaked English values like `2 people`

Change made:
- kept canonical internal team-size strings stable
- localized team-size rendering only in human-facing export output

Verified result:
- `outputs/ru-budget-stage61/constraints.md` now shows `Команда: 2 человека`
- EN export remains English-facing: `outputs/en-export-stage61/constraints.md` shows `Team Size: 2 people`

### 3. Russian budget phrasing support

Problem from re-audit:
- phrases like `бюджет маленький` were missed and rendered as unknown

Change made:
- added deterministic low-budget phrase extraction for:
  - `бюджет маленький`
  - `бюджет ограничен`
  - `денег мало`
  - `хотим недорого`
- reused the same phrase family for low-budget contradiction signaling and tradeoff inference

Verified result:
- API-generated Russian export now shows `Бюджет: Бюджет маленький`
- regression test covers all four Russian phrase variants

### 4. README/docs truth fix

Problem from re-audit:
- README claimed 22 eval cases while the repo had 25

Change made:
- updated README to the current observed corpus size after this pass: `26 local cases`
- added one eval case for the deferred-scope near-miss regression

Verified result:
- `make eval` now reports `Cases: 26`
- README matches the current corpus

### 5. Regression coverage

Added only the minimum new coverage needed:

- unit regression for the exact realistic deferred-scope near-miss
- unit regression for Russian plain-language budget phrases
- export regression for Russian team-size localization and budget phrase rendering
- eval corpus regression case for deferred-scope near-miss restraint

## Files Changed

- `README.md`
- `eval/edge_cases.json`
- `src/specforge/pipeline/analyze.py`
- `src/specforge/pipeline/analysis_contradictions.py`
- `src/specforge/pipeline/analysis_signals.py`
- `src/specforge/pipeline/export_render.py`
- `src/specforge/pipeline/language.py`
- `tests/test_analyze.py`
- `tests/test_eval.py`
- `tests/test_generate_export.py`

## Commands Run

```bash
make lint
make test
python3 -m specforge.cli analyze --input .tmp/en_overloaded_stage61.txt
python3 -m specforge.cli analyze --input .tmp/ru_overloaded_stage61.txt
python3 -m specforge.cli analyze --input .tmp/near_miss_stage61.txt
python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8012
curl -s http://127.0.0.1:8012/health
curl -s -X POST http://127.0.0.1:8012/generate -H 'content-type: application/json' -d '{"brief_text":"Нужен внутренний инструмент для операционной команды. Бюджет маленький, команда 2 человека. Сначала только веб.","title":"RU Budget Smoke","output_label":"ru-budget-stage61"}'
python3 -m specforge.cli generate --input .tmp/en_overloaded_stage61.txt --run-label en-export-stage61
make eval
```

## Results

- `make lint`: passed
- `make test`: passed, `38 passed`
- EN overloaded smoke check: passed, `Contradictions: 3`
- RU overloaded smoke check: passed, `Противоречия: 3`
- realistic near-miss smoke check: passed, `Contradictions: 0`
- RU export language smoke check: passed
  - `Бюджет: Бюджет маленький`
  - `Команда: 2 человека`
- RU budget-phrasing smoke check: passed through live API generate path
- eval run: passed, `Cases: 26`, `Passed: 26`, `Failed: 0`
- API verification path: passed
  - `GET /health` returned `{"status":"ok","app":"specforge","stage":"stage-5-9-freeze-focused-remediation"}`
  - `POST /generate` returned a valid artifact list and wrote `outputs/ru-budget-stage61`

## Remaining Limitations

- Stage identifiers in the API health payload and UI copy still say `5.9`. That did not block the re-audit findings addressed here, so it was left out of this surgical pass.
- Russian budget rendering currently preserves the captured human phrase verbatim, which is correct and inspectable, but still literal rather than normalized.
- The contradiction system is meaningfully better calibrated on the audited near-miss cases, but it remains a deterministic heuristic layer rather than a semantic planner.

## Recommendation

`READY FOR FINAL FREEZE-CHECK`
