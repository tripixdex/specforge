# Stage 5.7 Final Fix Pass

## Audit Findings Addressed

- A) Contradiction detection weakness in overloaded briefs
- B) Partial language-following in UI and exported artifacts
- C) Secondary polish for artifact trust and readability

## What Changed

### 1. Stronger deterministic contradiction detection

- added [analysis_contradictions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_contradictions.py) as a focused rule module for overload contradictions
- expanded overload detection to catch:
  - low budget + short timeline + broad or multi-platform scope
  - many integrations + urgency + low-cost framing
  - web + mobile + tiny team + short deadline
  - simple-MVP framing combined with enterprise-ish breadth
- added contradiction curation so each contradiction family appears once with merged evidence instead of noisy duplicates
- reduced [analysis_decisions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_decisions.py) from 441 lines to 154 lines by moving contradiction logic out of the already-large decisions module

### 2. Language-following tightened across surfaces

- localized remaining hard-coded UI labels in [index.html](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/templates/index.html) and [copy.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/copy.py)
- localized count labels, severity chips, evidence labels, page title, and artifact-kind labels in the browser UI
- localized CLI summary and export console output in [cli.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/cli.py)
- kept `html lang` aligned with the detected brief language in the UI verification path

### 3. Small artifact readability pass

- updated exported brief headings in [export_render.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export_render.py) from rougher wording to calmer phrasing such as `Deterministic Interpretation` and `Priority Open Questions`
- changed generated structure wording from `contradiction pressure` to `requirement overload` in [generate.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/generate.py)

### 4. Eval coverage upgraded from audit misses

- added explicit English and Russian overloaded-brief cases in:
  - [eval/founder_cases.json](/Users/vladgurov/Desktop/work/specforge/eval/founder_cases.json)
  - [eval/edge_cases.json](/Users/vladgurov/Desktop/work/specforge/eval/edge_cases.json)
- expanded the eval harness with an optional contradiction ceiling in [runner.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/eval/runner.py) and [models.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/eval/models.py) so overload cases fail if contradictions are missing or overly noisy
- refreshed eval output under [outputs/evals/stage-05/](/Users/vladgurov/Desktop/work/specforge/outputs/evals/stage-05)

### 5. Docs truth pass

- updated [README.md](/Users/vladgurov/Desktop/work/specforge/README.md)
- updated [docs/DEMO_SCENARIOS.md](/Users/vladgurov/Desktop/work/specforge/docs/DEMO_SCENARIOS.md)
- updated [docs/ACCEPTANCE_CRITERIA.md](/Users/vladgurov/Desktop/work/specforge/docs/ACCEPTANCE_CRITERIA.md)
- updated [docs/EVAL_PLAN.md](/Users/vladgurov/Desktop/work/specforge/docs/EVAL_PLAN.md)
- updated [REPORT_INDEX.md](/Users/vladgurov/Desktop/work/specforge/REPORT_INDEX.md)

## New Eval Cases

- `founder_ru_overloaded_brief`
- `edge_english_overloaded_multiplatform_mvp`

Both cases require the three curated overload contradiction families:

- `fast-cheap-feature-rich`
- `small-team-aggressive-deadline-broad-scope`
- `minimal-mvp-vs-enterprise-scope`

They also set `max_contradictions: 3` so duplicate-family spam now fails the eval.

## Commands Run

```bash
make lint
make test
python3 -m specforge.eval.runner
python3 - <<'PY'
from specforge.pipeline import create_raw_brief, normalize_brief, analyze_brief
text = '''Нужен простой MVP за 2 недели.
Бюджет до $8k, команда из 2 человек.
При этом нужны веб и мобильное приложение, CRM, Slack, биллинг, аналитика и роли доступа.
Нужно сделать быстро и недорого.'''
brief = normalize_brief(create_raw_brief(text, title='RU Smoke'))
_, report = analyze_brief(brief)
print('ru_contradictions', len(report.contradictions))
print('ru_categories', [item.category for item in report.contradictions])
PY
python3 - <<'PY'
from specforge.pipeline import create_raw_brief, normalize_brief, analyze_brief
text = '''Need a simple MVP in 10 days on a lean budget.
Team is just me plus one contractor.
It has to ship on web and mobile with Salesforce, Stripe, Slack, analytics, admin, and billing from day one.'''
brief = normalize_brief(create_raw_brief(text, title='EN Smoke'))
_, report = analyze_brief(brief)
print('en_contradictions', len(report.contradictions))
print('en_categories', [item.category for item in report.contradictions])
PY
python3 - <<'PY'
from fastapi.testclient import TestClient
from specforge.api.app import app
client = TestClient(app)
response = client.post('/ui/analyze', data={
    'title': 'Русский UI Smoke',
    'brief_text': 'Нужен простой MVP за 2 недели. Бюджет до $8k. Нужны веб и мобильное приложение, CRM и Slack.',
    'demo_name': 'founder-app-idea',
    'output_label': ''
})
print('ui_status', response.status_code)
print('ui_lang_ru', '<html lang="ru">' in response.text)
print('ui_has_contradictions_label', 'Противоречия' in response.text)
print('ui_has_evidence_label', 'Основания:' in response.text)
PY
python3 - <<'PY'
from fastapi.testclient import TestClient
from specforge.api.app import app
client = TestClient(app)
response = client.post('/analyze', json={
    'title': 'API Verification',
    'brief_text': 'Need a simple MVP in 10 days on a lean budget. Team is just me plus one contractor. It has to ship on web and mobile with Salesforce, Stripe, Slack, analytics, admin, and billing from day one.'
})
body = response.json()
print('api_status', response.status_code)
print('api_has_3_contradictions', body['counts']['contradictions'] == 3)
print('api_open_question_en', body['top_open_questions'][0])
PY
```

## Results

- `make lint`: passed
- `make test`: passed, `31 passed`
- Russian overloaded smoke: `3` contradictions with the expected three categories and Russian recommendation text
- English overloaded smoke: `3` contradictions with the expected three categories and English recommendation text
- eval run: passed, `22/22` cases, output at [outputs/evals/stage-05/eval_summary.md](/Users/vladgurov/Desktop/work/specforge/outputs/evals/stage-05/eval_summary.md)
- UI verification path: passed, `status 200`, `<html lang="ru">`, `Противоречия`, and `Основания:` present
- API verification path: passed, `status 200`, `counts.contradictions == 3`, top open question returned in English

## Remaining Limitations

- contradiction detection is still rules-based and will miss nuanced business tradeoffs that are not visible in deterministic wording
- language-following is scoped to English and Russian only
- [export_render.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export_render.py) is still 370 lines; it was not split in this stage because the changes were minor wording adjustments rather than a responsibility change
- a live cross-process `uvicorn` plus `curl` check was attempted, but the sandbox here did not keep the listener reachable between commands; route verification was completed with real in-process `TestClient` requests instead

## Readiness Recommendation

READY FOR RE-AUDIT
