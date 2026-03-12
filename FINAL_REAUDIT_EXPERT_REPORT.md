# Final Re-Audit Expert Report

## Executive summary

SpecForge is a real, runnable local demo product, not a fake shell. The repository has a coherent deterministic pipeline, clean modular structure, passing lint/tests, a working CLI/API/UI, and a working local eval harness. It is materially beyond a throwaway prototype.

It is not freeze-ready as a flagship portfolio project yet.

The main reasons are not cosmetic. In live smoke checks, the contradiction system still produced false positives on a realistic near-miss brief that explicitly deferred post-MVP scope. Russian-facing exports also still leak English values such as `2 people`, and a plain-language Russian budget phrase (`бюджет маленький`) was not recognized as a budget signal, which weakens both artifact trustworthiness and the claim of stronger bilingual behavior. There is also a docs truthfulness miss: README claims 22 eval cases while the current corpus and tests verify 25.

Verdict: `MVP BUT NEEDS FIXES`

Portfolio readiness score: `7.6/10`

## What the repo actually is

SpecForge is a deterministic local-first brief analysis and artifact generation tool with:

- a Python package under [`src/specforge`](/Users/vladgurov/Desktop/work/specforge/src/specforge)
- CLI flows for `analyze`, `generate`, and `demo`
- a FastAPI app with JSON endpoints and a server-rendered UI
- export of repo-local markdown and JSON bundles under [`outputs/`](/Users/vladgurov/Desktop/work/specforge/outputs)
- a local eval corpus and harness under [`eval/`](/Users/vladgurov/Desktop/work/specforge/eval)

It is not production software. It is a serious local demo/MVP with a deterministic rules pipeline.

## Current verified capabilities

Verified directly from terminal and live behavior:

- `make lint` passes.
- `make test` passes with 35 tests.
- CLI demo works and writes a bundle under `outputs/demo-founder-app`.
- Full eval harness runs and reports 25/25 passing cases.
- Live FastAPI server starts with `python3 -m uvicorn specforge.api.app:app --host 127.0.0.1 --port 8012`.
- `GET /health` returns the expected healthy JSON payload.
- `POST /analyze` returns structured JSON with counts, top questions, and MVP cut guidance.
- `POST /generate` returns structured JSON and writes a repo-local export bundle.
- `GET /ui` renders the intake UI and empty state.
- `POST /ui/generate` renders a localized results page with artifact previews and repo-local output path.
- `POST /ui/new` clears the form and returns the UI to intake state.
- English overloaded and Russian overloaded briefs both trigger curated contradiction findings.
- Export bundles contain the expected artifact set.

## Freeze-readiness assessment

Not freeze-ready.

What is strong enough:

- The project looks real quickly. A hiring manager can run it and see actual deterministic behavior.
- The repository structure is disciplined and not bloated.
- The product has enough surface area to be credible: CLI, API, UI, evals, and exported artifacts.

What still blocks a freeze:

- Contradiction detection still overfires on at least one realistic near-miss case, which undercuts trust in the core product claim.
- Russian-facing output is still not fully coherent in generated artifacts.
- README is not fully truthful to the current repo state.
- A few finishing details still feel “almost done” rather than intentionally finished.

For a flagship portfolio freeze, the core judgment engine needs to feel reliably calibrated, not just functional.

## Product usefulness assessment

The product concept is valid and the tool is useful on messy briefs. It surfaces:

- missing audience/platform/pricing decisions
- overloaded first-release scope
- suggested MVP cuts
- exportable planning artifacts

This is materially better than a structured prototype because the outputs are inspectable, deterministic, and available across three interfaces.

Limits that still matter:

- The outputs are useful as a planning aid, not yet trustworthy enough as a polished “audit-grade” assistant.
- False positives in contradiction handling create the risk of noisy or overbearing guidance.
- Some generated sections still have mild prototype smell when inputs are sparse or phrased casually.

## UX/UI audit

Strengths:

- The UI is calm, readable, and recruiter-demo friendly.
- The three-step flow is easy to understand.
- Empty state is explicit and decent.
- Bundle path presentation is calmer than dumping a raw absolute path.
- Artifact previews are genuinely useful in-demo.
- `New brief` works and clears stale results.

Issues:

- The reset flow can render Russian copy while `<html lang>` remains `en` because the template keys language off `result.language` only; there is no result on reset. See [`src/specforge/ui/templates/index.html:2`](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/templates/index.html#L2).
- Demo option labels remain English even on Russian-facing pages. This is acceptable for an MVP, but not polished.
- The UI is good enough for demoing, but not yet polished enough to feel unequivocally “finished”.

## Language behavior audit

English:

- English input produced coherent English CLI, API, UI, and export-facing generated text.
- English export bundle quality is acceptable for a local MVP.

Russian:

- Russian input produced mostly coherent Russian UI and exported headings/body text.
- Mixed-language leakage remains visible in generated artifacts. Example from live generated [`outputs/ru-api-export/constraints.md`](/Users/vladgurov/Desktop/work/specforge/outputs/ru-api-export/constraints.md): `Команда: 2 people`.
- Russian budget phrasing is not consistently recognized. The same file reports `Бюджет: Не указан` for a brief containing `бюджет маленький`.

Mixed-language leakage:

- Acceptable for an MVP in some minor places.
- Not acceptable yet for a flagship freeze when the repo explicitly claims stronger bilingual consistency.

## Contradiction-detection audit

What worked:

- English overloaded brief: 3 contradictions, curated rather than spammy.
- Russian overloaded brief: 3 contradictions, also curated rather than spammy.
- Eval corpus includes overload variants and contradiction ceilings.

What failed:

- A realistic near-miss brief that explicitly said mobile and deeper analytics were post-MVP still produced 2 contradiction findings in live CLI/export runs.
- Output from [`outputs/near-miss-export/analysis_report.md`](/Users/vladgurov/Desktop/work/specforge/outputs/near-miss-export/analysis_report.md) shows:
  - `Fast, cheap, and feature-rich at once`
  - `Minimal MVP vs enterprise scope`
- That is a material calibration problem. The product is supposed to help with messy briefs, and overcalling contradictions on a restrained brief directly damages usefulness.

Likely root cause from code:

- `has_broad_scope_signal()` treats generic terms like `analytics`, `dashboard`, `admin`, and `reporting` as broad-scope markers without sufficient context. See [`src/specforge/pipeline/analysis_signals.py:250`](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_signals.py#L250).
- `has_low_budget_signal()` misses phrase variants like `budget is reasonable` vs true low-budget phrasing, and Russian low-budget handling misses `бюджет маленький`. See [`src/specforge/pipeline/analysis_signals.py:318`](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_signals.py#L318).

## Artifact quality audit

Strengths:

- Bundle completeness is good.
- Artifact naming is consistent.
- `mvp_cut_plan.md`, `analysis_report.md`, and `risk_register.md` are the most useful outputs.
- Output paths stay repo-local through API and UI.

Weaknesses:

- Some artifact lines still read formulaically.
- Russian bundles still contain English value leakage.
- Constraint extraction misses some plain-language signals, which hurts trust.
- The brief artifact summary can become generic when explicit goals are thin.

Overall artifact quality is solid MVP quality, not flagship-finish quality.

## Engineering quality audit

Strengths:

- Clean top-level repo layout.
- Modules are reasonably scoped; no obviously absurd source file sizes.
- Test suite is fast and passing.
- Eval harness is real and writes inspectable artifacts.
- Input validation and output-root restriction are in place for API/UI flows.
- Run ergonomics are good; documented `uvicorn` path works without `PYTHONPATH=src`.

Weaknesses:

- Docs truthfulness has at least one concrete mismatch: README says 22 eval cases, actual corpus/tested total is 25.
- Eval coverage is helpful but not strong enough to catch the observed near-miss contradiction overfire.
- A few polish bugs remain in localization/UI semantics.

## Top findings ranked by severity

1. High: Realistic near-miss contradiction false positives remain in the live product.
   Evidence: [`outputs/near-miss-export/analysis_report.md`](/Users/vladgurov/Desktop/work/specforge/outputs/near-miss-export/analysis_report.md)

2. High: Russian export language is still not consistently Russian-facing.
   Evidence: [`outputs/ru-api-export/constraints.md`](/Users/vladgurov/Desktop/work/specforge/outputs/ru-api-export/constraints.md)

3. Medium: Russian plain-language budget phrasing is not reliably extracted, which weakens artifact trustworthiness.
   Evidence: [`outputs/ru-api-export/constraints.md`](/Users/vladgurov/Desktop/work/specforge/outputs/ru-api-export/constraints.md)

4. Medium: README is not fully truthful to current repository state on eval corpus size.
   Evidence: [`README.md`](/Users/vladgurov/Desktop/work/specforge/README.md), [`tests/test_eval.py:10`](/Users/vladgurov/Desktop/work/specforge/tests/test_eval.py#L10)

5. Low: UI reset flow can render localized Russian content while root HTML language remains `en`.
   Evidence: [`src/specforge/ui/templates/index.html:2`](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/templates/index.html#L2)

## Final verdict

`MVP BUT NEEDS FIXES`

Smallest remaining blockers before a credible freeze:

- fix contradiction restraint so realistic near-miss cases stay quiet
- remove remaining Russian/English leakage in exported artifact values
- improve Russian budget phrase extraction for plain-language wording
- correct README truthfulness mismatch

If those are fixed and re-verified, this could reasonably move into freeze-ready territory.
