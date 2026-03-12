# SpecForge Re-Audit Terminal Evidence

## Commands run
```bash
git status --short
sed -n '1,240p' README.md
sed -n '1,240p' Makefile
sed -n '1,260p' pyproject.toml
sed -n '1,260p' src/specforge/pipeline/analyze.py
sed -n '1,260p' src/specforge/pipeline/analysis_contradictions.py
sed -n '1,260p' src/specforge/pipeline/generate.py
sed -n '1,260p' src/specforge/api/routes.py
sed -n '1,260p' src/specforge/ui/routes.py
sed -n '1,260p' tests/test_analyze.py
sed -n '1,260p' tests/test_api.py
sed -n '1,320p' tests/test_ui.py
sed -n '1,260p' tests/test_eval.py
find src tests -type f \( -name '*.py' -o -name '*.html' -o -name '*.css' \) -maxdepth 5 -print0 | xargs -0 wc -l | sort -nr | head -20
make lint
make test
python3 -m specforge.cli analyze --input examples/contradictory_founder_brief.txt
python3 -m specforge.eval.runner
python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8000
cat > /tmp/specforge_ru_overloaded.txt <<'EOF'
...ru overloaded brief...
EOF
python3 -m specforge.cli analyze --input /tmp/specforge_ru_overloaded.txt
cat > /tmp/specforge_en_overloaded.txt <<'EOF'
...en overloaded brief...
EOF
python3 -m specforge.cli analyze --input /tmp/specforge_en_overloaded.txt
cat > /tmp/specforge_short_brief.txt <<'EOF'
Need an app.
EOF
python3 -m specforge.cli analyze --input /tmp/specforge_short_brief.txt
curl -s http://127.0.0.1:8000/health
curl -s -X POST http://127.0.0.1:8000/analyze -H 'content-type: application/json' -d '{"title":"RU Audit","brief_text":"..."}'
curl -s -X POST http://127.0.0.1:8000/generate -H 'content-type: application/json' -d '{"title":"API Audit Bundle","output_label":"api-audit-bundle","brief_text":"..."}'
curl -s http://127.0.0.1:8000/ui | sed -n '1,80p'
curl -s -X POST http://127.0.0.1:8000/ui/analyze -F 'title=RU UI Audit' -F 'brief_text=...' -F 'demo_name=founder-app-idea' | sed -n '1,220p'
curl -s -X POST http://127.0.0.1:8000/ui/generate -F 'title=UI Audit Bundle' -F 'output_label=ui-audit-bundle' -F 'brief_text=...' -F 'demo_name=internal-operations-tool' | sed -n '1,260p'
curl -s -X POST http://127.0.0.1:8000/ui/new -F 'demo_name=founder-app-idea' -F 'previous_brief_text=хочу приложение' | rg -n 'Начните с анализа|Guided results|Новый бриф'
python3 -m specforge.eval.runner --case-id founder_ru_overloaded_brief --case-id edge_english_overloaded_multiplatform_mvp
curl -s -X POST http://127.0.0.1:8000/ui/analyze -F 'title=' -F 'brief_text=Need an app.' -F 'demo_name=founder-app-idea' | sed -n '1,220p'
cat > /tmp/specforge_ru_generate.txt <<'EOF'
...ru generation brief...
EOF
python3 -m specforge.cli generate --input /tmp/specforge_ru_generate.txt --output-root outputs --run-label ru-audit-bundle
find outputs/api-audit-bundle -maxdepth 1 -type f | sort
find outputs/ru-audit-bundle -maxdepth 1 -type f | sort
sed -n '1,240p' outputs/api-audit-bundle/analysis_report.md
sed -n '1,240p' outputs/api-audit-bundle/brief.md
sed -n '1,240p' outputs/api-audit-bundle/mvp_cut_plan.md
sed -n '1,240p' outputs/api-audit-bundle/scope.md
sed -n '1,240p' outputs/api-audit-bundle/open_questions.md
sed -n '1,240p' outputs/ru-audit-bundle/analysis_report.md
sed -n '1,220p' outputs/ru-audit-bundle/brief.md
sed -n '1,220p' outputs/ru-audit-bundle/summary.json
git ls-files | rg '__pycache__|\.pyc$|\.DS_Store$'
```

## Concise outputs
### Passed
- `make lint`
  - `All checks passed!`
- `make test`
  - `31 passed in 0.44s`
- CLI analyze on bundled contradictory founder brief
  - `Contradictions: 3`
- Full eval run
  - `Cases: 22`
  - `Passed: 22`
  - `Failed: 0`
  - `Score percent: 100.0`
- API health
  - `{"status":"ok","app":"specforge","stage":"stage-5-7-final-fix-pass"}`
- API generate
  - returned `output_path` under `outputs/api-audit-bundle`
  - returned expected artifact file list
- UI home
  - rendered title, workflow steps, demo selector, and input form
- UI analyze
  - rendered Russian page with localized labels and contradiction cards
- UI generate
  - rendered generated bundle state and artifact list
- UI new
  - returned reset state containing `Начните с анализа`
- Eval spot-check on overloaded corpus cases
  - `Cases: 2`
  - `Passed: 2`
  - `Failed: 0`

### Failed or weak
- Realistic Russian overloaded smoke brief via CLI
  - `Противоречия: 2`
  - expected for a robust result: `3`
- Realistic English overloaded smoke brief via CLI
  - `Contradictions: 2`
  - expected for a robust result: `3`
- Russian export artifact quality
  - verified mixed-language values in `brief.md`
  - example: `Тип продукта: software tool`
  - example: `Аудитория: operations team`
  - example: `local-first`
- Artifact usefulness
  - `scope.md` and `mvp_cut_plan.md` were valid but thin
  - recommendations often restated obvious issues rather than decomposing scope

### Notable repo-quality evidence
- Largest files found:
  - `src/specforge/pipeline/analysis_signals.py` `461`
  - `src/specforge/pipeline/export_render.py` `370`
  - `src/specforge/pipeline/intake.py` `351`
- Tracked junk file:
  - `.DS_Store`

## What passed
- Core local run path
- CLI path
- API path
- UI path
- Eval path
- Empty-state and reset flow
- Local output generation

## What failed
- Robust contradiction detection across realistic overloaded wording variants
- Full language consistency for Russian-facing exported artifacts
- High-value artifact usefulness beyond structured diagnostics

## What was not runnable
- Nothing essential was blocked. All required verification dimensions were runnable locally.
