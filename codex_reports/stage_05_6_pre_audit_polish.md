# Stage 5.6 Pre-Audit Polish

## What manual findings were addressed

- output language now follows Russian and English input across deterministic findings, recommendations, and exported artifact text
- contradiction detection is stronger for overloaded briefs: low budget plus short timeline plus broad scope, many integrations plus speed plus low cost, and simple-MVP language paired with enterprise or multi-platform breadth
- the browser UI now exposes a visible `New brief` reset path
- Cyrillic titles now export to readable transliterated folder names instead of collapsing to poor slugs
- artifact preview cards no longer stretch awkwardly when one card expands
- stale `Stage 2 Deterministic Draft` export labels were removed
- the human run path is documented as a verified `uvicorn` command
- very short briefs now show a humane clarification banner and the top missing essentials
- empty-looking sections now render explicit empty states
- the browser UI now shows a shorter repo-local output path first, with the full absolute path still available

## UX principles applied

- user control and freedom: the new reset flow makes it obvious how to leave a stale generated state
- match between system and the real world: Russian briefs now produce Russian deterministic output; English briefs stay English
- consistency and standards: stale stage labels were removed, output naming is more stable, and the official run path is singular and verified
- recognition rather than recall: reset actions, empty states, and clarification prompts are visible instead of implied
- aesthetic and minimalist design: bundle paths are calmer and empty sections no longer look broken
- progressive disclosure: the short repo-local path is shown first, while the full path stays available on demand

## What changed

- added [language.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/language.py) for deterministic locale detection and human-facing category labels
- added [naming.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/naming.py) for title suggestion, transliteration, and safe readable slugs
- localized deterministic copy in the analysis, generation, and export layers
- hardened contradiction rules in [analysis_decisions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_decisions.py) and broadened bilingual signals in [analysis_signals.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_signals.py)
- added [copy.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/copy.py) and updated the UI service, routes, template, and CSS for reset, underspecified, empty, and output-path states
- updated tests for bilingual contradiction coverage, transliterated export naming, short-brief UX, and reset flow

## Commands run

```bash
make lint
make test
python3 -m specforge.cli demo
python3 - <<'PY'
from fastapi.testclient import TestClient
from specforge.api.app import app
client = TestClient(app)
response = client.get('/demo')
print('status', response.status_code)
print('demo_name', response.json()['demo_name'])
PY
python3 - <<'PY'
from specforge.ui.service import analyze_for_ui
result = analyze_for_ui(brief_text='хочу приложение')
print(result.underspecified_banner)
print(result.underspecified_essentials)
PY
python -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8002
curl -s http://127.0.0.1:8002/health
curl -s http://127.0.0.1:8002/ui
```

## Results

- `make lint`: passed
- `make test`: passed, `28 passed`
- `python3 -m specforge.cli demo`: passed and generated [outputs/demo-founder-app](/Users/vladgurov/Desktop/work/specforge/outputs/demo-founder-app)
- API verification on `/demo`: passed with HTTP `200`
- Russian smoke check: passed with Russian contradiction recommendations
- English smoke check: passed with English contradiction recommendations
- short-brief smoke check: passed with a humane clarification banner and top essentials
- reset/new-brief flow smoke check: passed with HTTP `200` and intake-state rendering
- real `uvicorn` launch verification: passed after one escalated local bind check; `/health` and `/ui` both responded correctly

## File-size review

- [analysis_decisions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_decisions.py) grew to support contradiction hardening, but it remains a single-responsibility rules module
- [export_render.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export_render.py) remains a review candidate because rendering plus bilingual headers push it near the soft size threshold
- [ui/templates/index.html](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/templates/index.html) remains a review candidate, but the changes stayed within the server-rendered UI boundary and did not justify a premature component split
- new Stage 5.6 modules stayed small and responsibility-focused

## Remaining limitations before expert audit

- this is still a deterministic local demo, not a production planning engine
- Russian support is practical and heuristic, not a full localization system
- the CLI still exposes `--output-root`, while API and UI remain repo-local only; this divergence is intentional and documented
- contradiction logic is stronger for obvious overload, but it is still rules-based and will miss nuanced tradeoffs

## Verdict

`READY FOR EXPERT AUDIT`
