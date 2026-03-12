# Terminal Evidence

## Commands run

```bash
pwd
rg --files
git status --short
sed -n '1,260p' README.md
sed -n '1,260p' Makefile
sed -n '1,260p' docs/ARCHITECTURE.md
sed -n '1,260p' REPORT_INDEX.md
wc -l src/specforge/pipeline/*.py src/specforge/api/*.py src/specforge/ui/*.py src/specforge/ui/templates/index.html src/specforge/cli.py
sed -n '1,260p' src/specforge/pipeline/analysis_decisions.py
sed -n '261,520p' src/specforge/pipeline/analysis_decisions.py
sed -n '1,260p' src/specforge/pipeline/analyze.py
sed -n '1,260p' src/specforge/pipeline/language.py
sed -n '1,260p' src/specforge/api/service.py
sed -n '1,260p' src/specforge/ui/service.py
sed -n '1,260p' src/specforge/input_validation.py
sed -n '1,260p' src/specforge/ui/routes.py
sed -n '1,260p' src/specforge/api/routes.py
sed -n '1,260p' src/specforge/ui/templates/index.html
sed -n '261,520p' src/specforge/ui/templates/index.html
sed -n '1,260p' src/specforge/ui/copy.py
sed -n '1,260p' tests/test_api.py
sed -n '1,260p' tests/test_ui.py
sed -n '1,260p' tests/test_analyze.py
sed -n '1,260p' tests/test_generate_export.py
sed -n '1,260p' src/specforge/eval/runner.py
sed -n '1,260p' tests/test_eval.py
sed -n '1,260p' src/specforge/api/app.py
sed -n '1,260p' src/specforge/cli.py
make lint
make test
python3 -m specforge.cli analyze --input examples/contradictory_founder_brief.txt
python3 -m specforge.eval.runner --case-id internal_clear_local_tool
python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8000
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/analyze -H 'content-type: application/json' -d '{"brief_text":"Нужен локальный инструмент для разбора брифов. Бюджет ограничен. Нужен веб и мобильное приложение за 2 недели.","title":"Русский smoke"}'
curl -s -X POST http://127.0.0.1:8000/analyze -H 'content-type: application/json' -d '{"brief_text":"Need a local brief analysis tool. Budget is tight. Need web and mobile in 2 weeks.","title":"English smoke"}'
curl -s http://127.0.0.1:8000/ui
make eval
curl -s -X POST http://127.0.0.1:8000/ui/analyze -H 'content-type: application/x-www-form-urlencoded' --data-urlencode 'title=Русский UI smoke' --data-urlencode 'brief_text=Нужен локальный инструмент для разбора брифов. Бюджет ограничен. Нужен веб и мобильное приложение за 2 недели.' --data-urlencode 'demo_name=founder-app-idea'
curl -s -X POST http://127.0.0.1:8000/ui/generate -H 'content-type: application/x-www-form-urlencoded' --data-urlencode 'title=English UI bundle' --data-urlencode 'brief_text=Need a local tool for internal reporting. Keep it local-first. Budget under $10k.' --data-urlencode 'demo_name=internal-operations-tool' --data-urlencode 'output_label=audit-ui-bundle'
python3 - <<'PY'
from specforge.pipeline.analyze import analyze_brief
from specforge.pipeline.intake import create_raw_brief, normalize_brief
cases = {
'case1': 'Need a simple MVP with web and mobile, Slack, Stripe, CRM, analytics, and admin. Budget under $5k. Need it in 2 weeks. Team is just me.',
'case2': 'Нужен простой MVP: веб и мобильное приложение, Slack, CRM, биллинг, аналитика. Бюджет до $5k. Срок 2 недели. Команда 2 человека.',
'case3': 'Need web and mobile for a tiny two-person team in 3 weeks. Also need enterprise SSO, audit logs, and integrations. Keep it cheap.',
}
for name, text in cases.items():
    _, report = analyze_brief(normalize_brief(create_raw_brief(text)))
    print(name, len(report.contradictions), [item.category for item in report.contradictions])
PY
python3 - <<'PY'
from pathlib import Path
from specforge.pipeline import create_raw_brief, normalize_brief, analyze_brief, generate_delivery_pack, export_delivery_pack
text = '''Русский экспорт
Нужен локальный инструмент для агентства.
Цели:
- Быстро разбирать клиентские брифы
Ограничения:
- Бюджет до $12k
- Нужен веб и мобильное приложение за 3 недели
- Команда 2 человека
'''
brief = normalize_brief(create_raw_brief(text, title='Русский экспорт'))
analyzed, report = analyze_brief(brief)
pack = generate_delivery_pack(analyzed)
out = export_delivery_pack(pack, output_root=Path('outputs'), run_label='audit-ru-bundle')
print(out)
print('contradictions', len(report.contradictions), [item.category for item in report.contradictions])
PY
find outputs -maxdepth 2 -type d | sort
ls -la outputs
sed -n '1,240p' src/specforge/pipeline/export.py
sed -n '1,220p' outputs/audit-ru-bundle/analysis_report.md
sed -n '1,220p' outputs/audit-ru-bundle/brief.md
sed -n '1,220p' outputs/audit-ru-bundle/summary.json
curl -s -X POST http://127.0.0.1:8000/ui/new -H 'content-type: application/x-www-form-urlencoded' --data-urlencode 'demo_name=founder-app-idea' --data-urlencode 'previous_brief_text=хочу приложение'
python3 - <<'PY'
from specforge.pipeline.analyze import analyze_brief
from specforge.pipeline.intake import create_raw_brief, normalize_brief
text = 'Need local brief analysis. Нужен MVP за 2 недели. Budget under $5k. Web and mobile.'
brief = normalize_brief(create_raw_brief(text, title='mixed'))
_, report = analyze_brief(brief)
print('summary', brief.summary)
print('contradictions', len(report.contradictions), [c.description for c in report.contradictions])
print('questions', report.prioritized_open_questions[:3])
PY
nl -ba src/specforge/pipeline/analysis_decisions.py | sed -n '1,260p'
nl -ba src/specforge/ui/templates/index.html | sed -n '100,210p'
nl -ba src/specforge/pipeline/language.py | sed -n '1,120p'
nl -ba README.md | sed -n '10,40p'
```

## What passed

- `make lint`
  - Result: `All checks passed!`
- `make test`
  - Result: `28 passed in 0.43s`
- CLI verification
  - `python3 -m specforge.cli analyze --input examples/contradictory_founder_brief.txt`
  - Result: printed deterministic summary with `Ambiguities: 2`, `Contradictions: 5`, `Missing decisions: 1`
- Eval smoke
  - `python3 -m specforge.eval.runner --case-id internal_clear_local_tool`
  - Result: `Cases: 1`, `Passed: 1`, `Failed: 0`
- Full eval
  - `make eval`
  - Result: `Cases: 20`, `Passed: 20`, `Failed: 0`, `Score percent: 100.0`
- Live API health
  - `curl -s http://127.0.0.1:8000/health`
  - Result: `{"status":"ok","app":"specforge","stage":"stage-5-6-pre-audit-polish"}`
- Live UI home
  - `curl -s http://127.0.0.1:8000/ui`
  - Result: rendered HTML with demo selector, intake form, and empty-state results panel
- Live UI generate
  - `curl -s -X POST http://127.0.0.1:8000/ui/generate ...`
  - Result: rendered generated bundle view with artifact previews and repo-local path `outputs/audit-ui-bundle`
- Live UI reset
  - `curl -s -X POST http://127.0.0.1:8000/ui/new ...`
  - Result: rendered cleared intake form and empty results panel

## What failed

- Initial live server start inside sandbox:
  - `python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8000`
  - Result: bind failed with `operation not permitted`
  - Resolution: reran with approved escalation and verified the live app successfully.

## Verified behavior that is weaker than claims

- Russian API smoke
  - Input: low-budget, 2-week, web+mobile brief in Russian
  - Result: `contradictions: 0`
- English API smoke
  - Input: tight-budget, 2-week, web+mobile brief in English
  - Result: `contradictions: 0`
- Russian generated export
  - Input included budget, 3-week deadline, web+mobile, team of 2
  - Result: exported bundle created, but `contradictions 0 []`
- Stress cases
  - `case1`: `4` contradictions with repeated families
  - `case2`: `3` contradictions
  - `case3`: only `1` contradiction despite broad overloaded scope
- UI localization gaps
  - Russian UI results page still showed `Ambiguities`, `Contradictions`, `Missing decisions`, `Assumptions`
  - `POST /ui/new` returned Russian copy but `<html lang="en">`

## What was not runnable or not fully verified

- No real browser automation was run; UI verification used live HTML over HTTP, not interactive browser sessions.
- No external deployment, auth, persistence, or multi-user checks were attempted because those are out of scope and not claimed.
