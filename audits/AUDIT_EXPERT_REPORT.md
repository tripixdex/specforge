# SpecForge Independent Audit

## Executive summary

SpecForge is a real local-first deterministic brief-analysis demo, not a fake shell. The repository has working CLI, FastAPI, server-rendered UI, repo-local export flow, and a deterministic eval harness. It is materially more complete than a typical portfolio prototype.

It is not freeze-ready yet.

Main reason: the contradiction layer is still not reliable enough for the README-level claim of "stronger deterministic contradiction rules for overloaded briefs." In live checks, plausible overloaded briefs with low budget, short timeline, and multi-platform scope still passed with `0` contradictions. The UI and exported Russian artifacts also show partial, not full, language-following.

Verdict: `MVP BUT NEEDS FIXES`

Portfolio readiness score: `7.6/10`

## Repo purpose

### VERIFIED

- SpecForge is a local deterministic pipeline that turns plain-text product briefs into:
  - normalized brief structure
  - analysis findings
  - generated markdown/json delivery artifacts
  - repo-local exported bundles under `outputs/`
- It exposes the same core flow through:
  - CLI
  - FastAPI JSON API
  - server-rendered browser UI
  - local eval harness

### INFERRED

- The project is aimed at portfolio/demo presentation more than real production use.
- The repo is trying to present engineering discipline: typed models, modular packages, tests, evals, and scoped claims.

### NOT VERIFIED

- Real user adoption, product-market fit, or decision-making value in non-demo settings.
- Performance under sustained use or large briefs beyond local smoke scale.

## Current verified capabilities

### VERIFIED

- Deterministic brief normalization.
- Ambiguity detection.
- Missing-decision detection.
- Assumption handling.
- Delivery-pack generation.
- Safe repo-local exports for API and UI.
- CLI commands: `analyze`, `generate`, `demo`.
- FastAPI endpoints: `/health`, `/analyze`, `/generate`, `/demo`.
- Local browser UI at `/` and `/ui`.
- Eval harness with 20 local cases.
- Russian and English output generation exists across API/UI/artifacts.
- `New brief` reset path exists in the UI.

### VERIFIED BUT PARTIAL

- Contradiction detection works on many obvious overloaded cases, but not consistently enough.
- Language-following works in many places, but not end-to-end consistently.

### NOT VERIFIED

- Any browser-side behavior beyond server-rendered HTML responses.
- Multi-user, persistence, cloud, auth, or external integrations.

## Docs truth audit

### Mostly true

- The README scope is disciplined and does not pretend this is SaaS or autonomous PM software.
- The listed surfaces are real: CLI, API, UI, eval, repo-local outputs.
- The local-only export restriction for API/UI is real and enforced in service code.

### Overstated or soft

- README claim: "Russian and English output that follows the input language in deterministic findings and exported artifacts" in [README.md](/Users/vladgurov/Desktop/work/specforge/README.md#L23).
  - Audit result: partially true, not fully true.
  - Evidence:
    - Russian UI results still render hard-coded English counter labels in [src/specforge/ui/templates/index.html](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/templates/index.html#L120).
    - Russian analysis markdown still uses English count keys like `ambiguities` and `contradictions` in exported `analysis_report.md`.
    - `POST /ui/new` returns Russian copy but `<html lang="en">`, because the template hard-codes `result.language if result else 'en'`.
- README claim: "stronger deterministic contradiction rules for overloaded briefs" in [README.md](/Users/vladgurov/Desktop/work/specforge/README.md#L24).
  - Audit result: directionally true, but not strong enough to rely on as a selling point.
  - Evidence:
    - Live API analysis of `Нужен локальный инструмент... Бюджет ограничен. Нужен веб и мобильное приложение за 2 недели.` returned `contradictions: 0`.
    - Generated Russian export with budget + web/mobile + 3 weeks + team of 2 also returned `contradictions: 0`.

## UX/UI audit

### VERIFIED strengths

- The UI has clear staged flow: intake, analysis, generation.
- Empty state is explicit rather than blank.
- Demo loading is easy and recruiter-demo friendly.
- `New brief` actually clears text/title/results and leaves demo selection available.
- Generated bundle path is shown in a calmer repo-local form with absolute path behind disclosure.
- Artifact previews are useful enough to demonstrate output breadth without leaving the page.

### Weaknesses

- Trustworthiness is still mixed because contradiction misses are visible in exactly the kind of brief a recruiter would try.
- Some UI strings remain English in Russian mode:
  - counter labels
  - `Evidence:` labels
  - demo names
- The reset response can mix Russian body copy with `lang="en"`, which is a polish miss for a project explicitly advertising language-following.
- Artifact previews are readable, but still feel raw and report-like rather than polished decision outputs.

### Portfolio demo judgment

Good enough to demo locally. Not yet clean enough to freeze as-is if the pitch is "deterministic planning quality." The UI sells the workflow better than the analytical depth.

## Language behavior audit

### VERIFIED

- English input produces coherent English findings and open questions.
- Russian input produces coherent Russian findings, open questions, and artifact prose in many paths.
- Mixed-language input is handled deterministically by a simple Cyrillic check in [src/specforge/pipeline/language.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/language.py#L42).

### Problems

- Language selection is simplistic: any Cyrillic forces Russian output.
- Mixed input therefore flips the whole analysis into Russian even if the brief is mostly English.
- UI localization is incomplete due hard-coded template labels in [src/specforge/ui/templates/index.html](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/templates/index.html#L120).
- Exported Russian artifacts still include some English structural wording and count keys.

### Assessment

For a local MVP, language behavior is acceptable but not fully consistent. It should be described as "basic language-following" rather than robust bilingual handling.

## Contradiction-detection audit

### VERIFIED

- The rules do catch several overloaded founder-brief patterns.
- Full eval run passed `20/20`.
- Tests include overloaded English and Russian briefs and they pass.

### Critical weakness

- The rule set still misses obvious overloaded briefs if the wording does not trip its specific heuristics.
- The live misses were not edge gibberish; they were plausible human inputs:
  - low budget + short timeline + web/mobile
  - low budget + short timeline + web/mobile + small team
- This matters because contradiction detection is one of the product's most portfolio-visible claims.

### Why this happens

- `detect_language` is simple but acceptable; the bigger issue is rule gating.
- Contradiction logic in [src/specforge/pipeline/analysis_decisions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_decisions.py#L25) depends on combinations like:
  - `broad_scope`
  - `enterprise_scope`
  - `overloaded_integrations`
  - inferred small team from parsed constraints
- Multi-platform alone is not enough for the `fast-cheap-feature-rich` branch at [src/specforge/pipeline/analysis_decisions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_decisions.py#L218), and the "small team + deadline + scope" branch depends on team extraction succeeding at [src/specforge/pipeline/analysis_decisions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_decisions.py#L184).

### Additional weakness

- Some overloaded cases produce multiple contradiction entries in the same family, which feels noisy rather than precise.
- Example: one stress case produced four contradictions with repeated category families, including two separate `fast-cheap-feature-rich` findings.

### Assessment

This layer is improved, but still weak enough to block a `FREEZE READY` verdict.

## Artifact quality audit

### VERIFIED positives

- Artifact set is broad and useful:
  - `brief.md`
  - `scope.md`
  - `constraints.md`
  - `open_questions.md`
  - `assumptions.md`
  - `assumption_ledger.md`
  - `analysis_report.md`
  - `mvp_cut_plan.md`
  - `risk_register.md`
  - `summary.json`
- Pathing is safe and predictable.
- The artifacts are readable and structurally consistent.

### Remaining prototype smell

- Outputs are still closer to structured internal notes than polished deliverables.
- `summary.json` is very raw and verbose, useful for inspection but not elegant.
- Exported Russian markdown still contains English structural elements in places.
- Some summaries are awkward or overly literal because they reflect deterministic extraction instead of polished editorial synthesis.

### Assessment

Useful for demoing system breadth. Not yet persuasive as high-quality end-user deliverables.

## Architecture audit

### VERIFIED strengths

- Overall modularity is good.
- Transport separation is real:
  - routes in `api/` and `ui/`
  - orchestration in service modules
  - rules in pipeline modules
  - export rendering separate from export filesystem writes
- The codebase is understandable and small enough to review quickly.

### Maintainability risks

- `analysis_decisions.py` is already `441` lines.
- `analysis_signals.py` is `355` lines.
- `export_render.py` is `366` lines.
- `intake.py` is `351` lines.
- `index.html` is `298` lines.

These are not disastrous yet, but they are the first modules likely to become dumping grounds.

### Specific concern

- `analysis_decisions.py` mixes several contradiction heuristics and missing-decision logic in one file. It is still readable, but it is the clearest near-term split candidate.

### Assessment

Architecture is portfolio-positive overall. The repo does not look chaotic. The main risk is rule accretion, not current disorder.

## Tests/evals audit

### VERIFIED

- `make lint` passed.
- `make test` passed: `28` tests.
- `make eval` passed: `20/20` cases.
- Live API health and analyze endpoints responded correctly.
- Live UI routes rendered expected pages over HTTP.

### Important caution

- Passing evals here does not prove analytical strength if the corpus mirrors the current heuristics too closely.
- The live contradiction misses are more damaging than the `20/20` eval pass is reassuring.

## Top findings ranked by severity

1. High: contradiction detection still misses plausible overloaded briefs, so the repo is not yet trustworthy enough to market around deterministic contradiction strength.
2. Medium: language-following is partial, not complete; Russian UI and artifacts still leak English structural labels and even incorrect HTML language metadata.
3. Medium: contradiction output can be noisy and duplicative, which reduces trust and makes the analysis feel less curated.
4. Medium: artifacts are useful but still read like structured prototype output rather than polished portfolio-grade deliverables.
5. Low: several modules are growing into maintenance hotspots, especially [src/specforge/pipeline/analysis_decisions.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/analysis_decisions.py), [src/specforge/pipeline/export_render.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export_render.py), and [src/specforge/pipeline/intake.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/intake.py).

## Portfolio readiness assessment

### What is portfolio-ready now

- The repo demonstrates real engineering work.
- The codebase is modular and test-backed.
- The local demo flow is easy to run and explain.
- The project has enough surfaces to show breadth without obvious fakery.

### What blocks a freeze

- Contradiction detection needs one more serious hardening pass.
- Language-following needs consistency cleanup in UI and export rendering.
- Output wording needs a small editorial pass to reduce prototype smell.

## Final verdict

`MVP BUT NEEDS FIXES`

Not `NOT PORTFOLIO READY`: the project is already substantial and demoable.

Not `FREEZE READY`: the core analysis claim is still too soft in live overloaded-brief checks, and the language/UI polish story is not fully true end-to-end.
