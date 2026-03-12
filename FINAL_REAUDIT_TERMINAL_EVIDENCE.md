# Final Re-Audit Terminal Evidence

## Commands run

```bash
pwd
ls -la
rg --files
sed -n '1,220p' README.md
sed -n '1,220p' Makefile
sed -n '1,260p' pyproject.toml
sed -n '1,260p' src/specforge/cli.py
sed -n '1,320p' src/specforge/api/routes.py
sed -n '1,320p' src/specforge/api/schemas.py
sed -n '1,300p' src/specforge/ui/routes.py
sed -n '1,260p' src/specforge/ui/service.py
sed -n '1,260p' src/specforge/pipeline/analysis_contradictions.py
sed -n '1,240p' src/specforge/pipeline/analysis_signals.py
sed -n '1,260p' src/specforge/pipeline/export.py
sed -n '1,260p' src/specforge/pipeline/export_render.py
git status --short
find src -type f | xargs wc -l | sort -nr | head -n 20
make lint
make test
python3 -m specforge.cli demo
make eval
mkdir -p .tmp && cat > .tmp/ru_overloaded_brief.txt <<'EOF'
Нужен простой MVP для сервиса записи к врачам. Хотим веб, iOS и Android сразу, интеграции с CRM, платежами, аналитикой, телефонией и госуслугами. Команда 2 человека, бюджет маленький, запуск через 3 недели. Для клиник enterprise-уровня нужны SSO, аудит действий, роли и кастомные отчеты уже в первом релизе.
EOF
mkdir -p .tmp && cat > .tmp/en_overloaded_brief.txt <<'EOF'
We need a simple MVP for a field service operations product. Launch in 4 weeks with a team of 2 and a tight budget, but the first release should include web plus iOS and Android, offline mode, SSO, audit logs, custom analytics, Stripe billing, QuickBooks sync, HubSpot sync, and an admin console for enterprise customers.
EOF
mkdir -p .tmp && cat > .tmp/near_miss_brief.txt <<'EOF'
Build a simple internal web dashboard for one operations team. Start with web only. The team is 4 people, the budget is reasonable, and the target is a pilot in 10 weeks. Nice-to-have ideas for later include mobile access and deeper analytics, but those are explicitly post-MVP.
EOF
python3 -m specforge.cli analyze --input .tmp/ru_overloaded_brief.txt
python3 -m specforge.cli analyze --input .tmp/en_overloaded_brief.txt
python3 -m specforge.cli analyze --input .tmp/near_miss_brief.txt
python3 -m specforge.cli generate --input .tmp/en_overloaded_brief.txt --run-label en-cli-export
python3 -m specforge.cli generate --input .tmp/near_miss_brief.txt --run-label near-miss-export
python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8012
curl -s http://127.0.0.1:8012/health
curl -s http://127.0.0.1:8012/ui
curl -s -X POST http://127.0.0.1:8012/analyze -H 'content-type: application/json' -d '{"brief_text":"We need a simple MVP for a field service operations product. Launch in 4 weeks with a team of 2 and a tight budget, but the first release should include web plus iOS and Android, offline mode, SSO, audit logs, custom analytics, Stripe billing, QuickBooks sync, HubSpot sync, and an admin console for enterprise customers.","title":"EN Overloaded API"}'
curl -s -X POST http://127.0.0.1:8012/generate -H 'content-type: application/json' -d '{"brief_text":"Нужен простой MVP для сервиса записи к врачам. Хотим веб, iOS и Android сразу, интеграции с CRM, платежами, аналитикой, телефонией и госуслугами. Команда 2 человека, бюджет маленький, запуск через 3 недели. Для клиник enterprise-уровня нужны SSO, аудит действий, роли и кастомные отчеты уже в первом релизе.","title":"RU API Export","output_label":"ru-api-export"}'
curl -s -X POST http://127.0.0.1:8012/ui/generate -F 'title=RU UI Smoke' -F 'output_label=ru-ui-smoke' -F 'demo_name=founder_app_idea' -F 'brief_text=Нужен простой MVP для сервиса записи к врачам. Хотим веб, iOS и Android сразу, интеграции с CRM, платежами, аналитикой, телефонией и госуслугами. Команда 2 человека, бюджет маленький, запуск через 3 недели. Для клиник enterprise-уровня нужны SSO, аудит действий, роли и кастомные отчеты уже в первом релизе.'
curl -s -X POST http://127.0.0.1:8012/ui/new -F 'demo_name=founder-app-idea' -F 'previous_brief_text=Нужен короткий бриф'
python3 - <<'PY'
import json, pathlib
root = pathlib.Path('eval')
count = 0
for path in root.glob('*.json'):
    data = json.loads(path.read_text())
    print(path.name, len(data))
    count += len(data)
print('TOTAL', count)
PY
sed -n '1,220p' outputs/ru-api-export/constraints.md
sed -n '1,220p' outputs/ru-api-export/brief.md
sed -n '1,220p' outputs/en-cli-export/constraints.md
sed -n '1,220p' outputs/en-cli-export/brief.md
sed -n '1,220p' outputs/en-cli-export/mvp_cut_plan.md
sed -n '1,260p' outputs/near-miss-export/analysis_report.md
sed -n '1,220p' outputs/evals/stage-05/eval_summary.json
```

## Concise outputs

### Passed

`make lint`

```text
python3 -m ruff check src tests
All checks passed!
```

`make test`

```text
35 passed in 0.42s
```

`python3 -m specforge.cli demo`

```text
Output: /Users/vladgurov/Desktop/work/specforge/outputs/demo-founder-app
Ambiguities: 0
Contradictions: 3
Missing decisions: 0
```

`make eval`

```text
Eval output: /Users/vladgurov/Desktop/work/specforge/outputs/evals/stage-05
Cases: 25
Passed: 25
Failed: 0
Score percent: 100.0
```

Live API health:

```json
{"status":"ok","app":"specforge","stage":"stage-5-9-freeze-focused-remediation"}
```

Live API analyze:

```json
{"counts":{"ambiguities":5,"contradictions":3,"missing_decisions":2,"assumptions":0,"open_questions":10}, ...}
```

Live API generate:

```json
{"counts":{"ambiguities":4,"contradictions":3,"missing_decisions":2,"assumptions":0,"open_questions":9},"output_path":"/Users/vladgurov/Desktop/work/specforge/outputs/ru-api-export","artifact_files":["analysis_report.md","assumption_ledger.md","assumptions.md","brief.md","constraints.md","mvp_cut_plan.md","open_questions.md","risk_register.md","scope.md","summary.json"]}
```

Live UI GET `/ui`

```text
Returned full HTML page with intake form, demo picker, and explicit empty state.
```

Live UI POST `/ui/generate`

```text
Returned full localized Russian HTML page with counts, findings, open questions, MVP cut, output path, and artifact previews.
```

Live UI POST `/ui/new`

```text
Returned intake-state HTML with cleared title/text/results.
```

RU overloaded CLI analyze:

```text
Неясности: 4
Противоречия: 3
Недостающие решения: 2
```

EN overloaded CLI analyze:

```text
Ambiguities: 5
Contradictions: 3
Missing decisions: 2
```

Eval corpus count check:

```text
edge_cases.json 7
client_cases.json 5
founder_cases.json 8
internal_cases.json 5
TOTAL 25
```

### Failed

Near-miss contradiction restraint:

```text
python3 -m specforge.cli analyze --input .tmp/near_miss_brief.txt
...
Contradictions: 2
```

Near-miss exported analysis confirmed the false positives:

```text
- [high] Fast, cheap, and feature-rich at once
- [high] Minimal MVP vs enterprise scope
```

Russian export language/constraint quality issues:

From `outputs/ru-api-export/constraints.md`:

```text
- Бюджет: Не указан
- Команда: 2 people
```

That output came from a Russian brief containing `бюджет маленький` and `Команда 2 человека`.

README truthfulness mismatch:

```text
README claims 22 local eval cases.
Actual corpus and tests verify 25.
```

UI localization polish issue on reset:

```text
POST /ui/new returned Russian page copy but root tag rendered as <html lang="en">.
```

### One failed command attempt

```bash
curl -s -X POST http://127.0.0.1:8012/analyze -H 'content-type: application/json' --data-binary @- <<'EOF'
...
EOF
```

Result:

```text
exit code 7
```

The API itself was subsequently verified successfully with a corrected `curl -d` command.

## What passed

- Lint
- Full test suite
- CLI demo
- CLI analyze/generate
- Full eval run
- Live FastAPI startup
- Live API health/analyze/generate
- Live UI load/generate/reset
- EN overloaded contradiction detection
- RU overloaded contradiction detection
- EN export language smoke-check

## What failed

- Near-miss contradiction smoke-check
- RU export language smoke-check
- README accuracy on eval corpus size
- UI root language attribute consistency on reset

## What was not runnable

- Nothing material. All required verification surfaces were runnable locally.
