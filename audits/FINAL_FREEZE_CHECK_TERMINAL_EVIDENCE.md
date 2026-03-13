# Exact commands run

```bash
make lint
make test
make eval
python3 -m specforge.cli analyze --input /tmp/specforge_en_overloaded.txt
python3 -m specforge.cli analyze --input /tmp/specforge_ru_overloaded.txt
python3 -m specforge.cli analyze --input /tmp/specforge_near_miss.txt
python3 -m specforge.cli generate --input /tmp/specforge_en_overloaded.txt --output-root outputs --run-label freeze-en-cli
python3 -m specforge.cli generate --input /tmp/specforge_ru_overloaded.txt --output-root outputs --run-label freeze-ru-cli
PYTHONPATH=src python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8012
curl -s http://127.0.0.1:8012/health
curl -s http://127.0.0.1:8012/demo
curl -s -X POST http://127.0.0.1:8012/analyze -H 'content-type: application/json' -d '{"title":"API EN Overloaded","brief_text":"Need a simple MVP for a service business within 10 days. Budget is under $5k and the team is just two people. From day one it must include web and mobile apps, Salesforce, Slack, Stripe, analytics, admin reporting, permissions, and billing. Please keep it cheap and move fast."}'
curl -s -X POST http://127.0.0.1:8012/generate -H 'content-type: application/json' -d '{"title":"API RU Export","brief_text":"Нужен простой MVP для сервисного бизнеса в короткий срок, максимум за 2 недели. Бюджет маленький, до $4k, и команда всего 2 человека. С первого релиза нужны веб и мобильное приложение, CRM, Slack, Stripe, аналитика, роли доступа, админка и отчеты. Нужно сделать быстро и недорого.","output_label":"api-ru-export"}'
curl -s http://127.0.0.1:8012/ui -o /tmp/specforge_ui_home.html
curl -s -X POST http://127.0.0.1:8012/ui/generate -F 'title=UI EN Export' -F 'output_label=ui-en-export' -F 'demo_name=founder-app-idea' -F 'brief_text=Need a simple MVP for a service business within 10 days. Budget is under $5k and the team is just two people. From day one it must include web and mobile apps, Salesforce, Slack, Stripe, analytics, admin reporting, permissions, and billing. Please keep it cheap and move fast.' -o /tmp/specforge_ui_en_generate.html
curl -s -X POST http://127.0.0.1:8012/ui/generate -F 'title=UI RU Export' -F 'output_label=ui-ru-export' -F 'demo_name=founder-app-idea' -F 'brief_text=Нужен простой MVP для сервисного бизнеса в короткий срок, максимум за 2 недели. Бюджет маленький, до $4k, и команда всего 2 человека. С первого релиза нужны веб и мобильное приложение, CRM, Slack, Stripe, аналитика, роли доступа, админка и отчеты. Нужно сделать быстро и недорого.' -o /tmp/specforge_ui_ru_generate.html
curl -s -X POST http://127.0.0.1:8012/ui/new -F 'demo_name=founder-app-idea' -F 'previous_brief_text=Need a short test brief.' -o /tmp/specforge_ui_new.html
python3 -m specforge.cli analyze --input examples/founder_app_idea.txt
python3 -m specforge.cli analyze --input examples/internal_operations_tool_brief.txt
```

# Concise outputs

`make lint`

- Passed.
- Output: `All checks passed!`

`make test`

- Passed.
- Output: `39 passed in 0.43s`

`make eval`

- Passed.
- Output: `Cases: 26`, `Passed: 26`, `Failed: 0`, `Score percent: 100.0`

`python3 -m specforge.cli analyze --input /tmp/specforge_en_overloaded.txt`

- Passed.
- Output highlights: `Ambiguities: 3`, `Contradictions: 3`, `Missing decisions: 1`

`python3 -m specforge.cli analyze --input /tmp/specforge_ru_overloaded.txt`

- Passed.
- Output highlights: `Неясности: 1`, `Противоречия: 3`, `Недостающие решения: 1`

`python3 -m specforge.cli analyze --input /tmp/specforge_near_miss.txt`

- Passed.
- Output highlights: `Ambiguities: 3`, `Contradictions: 0`, `Missing decisions: 1`

`python3 -m specforge.cli generate --input /tmp/specforge_en_overloaded.txt --output-root outputs --run-label freeze-en-cli`

- Passed.
- Output highlights: bundle written to `outputs/freeze-en-cli`

`python3 -m specforge.cli generate --input /tmp/specforge_ru_overloaded.txt --output-root outputs --run-label freeze-ru-cli`

- Passed.
- Output highlights: bundle written to `outputs/freeze-ru-cli`

`curl -s http://127.0.0.1:8012/health`

- Passed.
- Response: `{"status":"ok","app":"specforge"}`

`curl -s http://127.0.0.1:8012/demo`

- Passed technically.
- Important behavior: bundled default demo returned `counts.contradictions = 3`
- Response also exposed absolute `demo_input_path`

`curl -s -X POST http://127.0.0.1:8012/analyze ...`

- Passed.
- Important behavior: EN overloaded API path returned `contradictions = 3`

`curl -s -X POST http://127.0.0.1:8012/generate ...`

- Passed.
- Important behavior: RU API path returned RU-facing open questions and wrote `outputs/api-ru-export`

`curl -s http://127.0.0.1:8012/ui -o /tmp/specforge_ui_home.html`

- Passed.
- Verified HTML contained calm public copy and empty analysis state.

`curl -s -X POST http://127.0.0.1:8012/ui/generate ...EN...`

- Passed.
- Verified HTML contained `Generated bundle`, `Repo-local`, `Bundle path`, `analysis_report.md`
- Verified default preview hid technical JSON behind `Bundle technical details`

`curl -s -X POST http://127.0.0.1:8012/ui/generate ...RU...`

- Passed.
- Verified HTML contained `Сгенерированный пакет`, `Локально в репозитории`, `Путь к пакету`
- Verified markdown preview contained RU-facing analysis report content

`curl -s -X POST http://127.0.0.1:8012/ui/new ...`

- Passed.
- Verified empty-state HTML returned with `Start with analysis`

`python3 -m specforge.cli analyze --input examples/founder_app_idea.txt`

- Passed technically.
- Important behavior: default founder demo sample returned `Contradictions: 3`

`python3 -m specforge.cli analyze --input examples/internal_operations_tool_brief.txt`

- Passed.
- Output highlights: `Contradictions: 0`

# What passed

- Lint
- Tests
- Eval harness
- CLI analysis path
- CLI generation path
- API health path
- API analyze path
- API generate path
- UI home path
- UI generate path
- UI reset path
- EN overloaded contradiction detection
- RU overloaded contradiction detection
- Near-miss contradiction restraint
- EN and RU export bundle generation

# What failed

No required command failed at the process level.

Behavioral failures found during verification:

- The default bundled founder demo sample produced 3 contradiction findings that appear over-aggressive for a public showcase brief.
- RU public artifacts still contain some visible English jargon in human-readable output.
- The near-miss path stayed contradiction-quiet, but still produced over-eager platform narrowing guidance.

# What was not runnable

- No real browser session or pixel-level visual verification was run.
- UI verification was performed through live HTML/form responses over the local server path.
