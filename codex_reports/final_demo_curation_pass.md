# Final Demo Curation Pass

## What changed in the default demo path

- Curated the default bundled founder demo brief in [examples/founder_app_idea.txt](/Users/vladgurov/Desktop/work/specforge/examples/founder_app_idea.txt) so it reads like a sensible success-path founder brief instead of an accidental overload case.
- Updated the demo catalog in [src/specforge/demo_catalog.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/demo_catalog.py) so the default public label/title is `Founder scope tool`, which avoids misleading the public demo into a mobile-app inference.
- Removed `demo_input_path` from the public `/demo` response in [src/specforge/api/schemas.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/api/schemas.py) and [src/specforge/api/service.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/api/service.py).
- Cleaned remaining Russian public wording in [src/specforge/pipeline/language.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/language.py), [src/specforge/pipeline/analysis_contradictions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_contradictions.py), [src/specforge/pipeline/analysis_outcomes.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_outcomes.py), and [src/specforge/pipeline/generate.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/generate.py) by replacing leftover English/public-jarring terms like `workflow` and `enterprise-*` with calmer Russian-facing phrasing in human-facing outputs.
- Updated the minimal truth-bearing docs in [README.md](/Users/vladgurov/Desktop/work/specforge/README.md), [docs/DEMO_SCENARIOS.md](/Users/vladgurov/Desktop/work/specforge/docs/DEMO_SCENARIOS.md), [docs/ACCEPTANCE_CRITERIA.md](/Users/vladgurov/Desktop/work/specforge/docs/ACCEPTANCE_CRITERIA.md), and [REPORT_INDEX.md](/Users/vladgurov/Desktop/work/specforge/REPORT_INDEX.md).
- Added regression coverage in [tests/test_api.py](/Users/vladgurov/Desktop/work/specforge/tests/test_api.py) and updated the renamed demo-label assertion in [tests/test_ui.py](/Users/vladgurov/Desktop/work/specforge/tests/test_ui.py).

## Why these changes improve public demo credibility

- The default public `/demo` path now shows a clean founder success-path example with `0` contradictions and no missing decisions.
- The public demo response no longer exposes an absolute local file path, so it reads like a product surface instead of an implementation trace.
- The default demo label is calmer and more accurate for a hiring-manager scan.
- Russian public exports now read more naturally in the normal preview path and no longer surface the most obvious mixed-language phrasing in MVP guidance.
- The changes stay narrow: no architecture changes, no new features, and no global weakening of overload detection.

## Commands run

```bash
make lint
make test
python3 -m specforge.cli analyze --input examples/founder_app_idea.txt
PYTHONPATH=src python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8012
curl -s http://127.0.0.1:8012/demo
curl -s -X POST http://127.0.0.1:8012/generate -H 'content-type: application/json' -d '{"title":"API RU Export","brief_text":"Нужен простой MVP для сервисного бизнеса в короткий срок, максимум за 2 недели. Бюджет маленький, до $4k, и команда всего 2 человека. С первого релиза нужны веб и мобильное приложение, CRM, Slack, Stripe, аналитика, роли доступа, админка и отчеты. Нужно сделать быстро и недорого.","output_label":"api-ru-export-final"}'
sed -n '1,200p' outputs/api-ru-export-final/mvp_cut_plan.md
curl -s http://127.0.0.1:8012/ui -o /tmp/specforge_ui_home_final.html
rg -n "Founder scope tool|Start with analysis|Load demo|Guided results|New brief" /tmp/specforge_ui_home_final.html
```

## Results

- `make lint`: passed.
- `make test`: passed, `39 passed`.
- Default founder demo CLI check: passed with `0` contradictions and `0` missing decisions.
- Live `/demo` verification: passed.
  - no `demo_input_path`
  - default sample returned `product_type: web app`
  - default sample returned `contradictions: 0`
- RU public export smoke check: passed.
  - public-facing MVP text now uses `корпоративные требования` and `главный сценарий`
  - no leftover `workflow` wording in the inspected RU preview artifact
- UI preview smoke check: passed.
  - default demo label is `Founder scope tool`
  - `Load demo`, `New brief`, `Guided results`, and `Start with analysis` are present in the public path

## Freeze recommendation

`FREEZE AS PORTFOLIO ASSET`

This pass resolved the remaining showcase-path credibility issues without broadening scope or weakening the actual product logic. SpecForge should now be treated as frozen for portfolio use.
