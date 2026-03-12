# SpecForge Re-Audit Expert Report

## Executive summary
SpecForge is a real local demo product, not vaporware. The repo runs, the CLI/API/UI paths work, exports are generated locally, and the eval harness is operational. That is the good news.

The project is still not freeze-ready as a flagship portfolio piece. The main blockers are not infrastructure failures. They are credibility failures: overloaded-brief contradiction detection is still brittle to realistic phrasing, Russian-facing exports still leak English product labels and awkward mixed-language phrasing, and several generated outputs are structurally neat but strategically shallow. The repo is closer to a solid MVP than a finished showcase.

Verdict: `MVP BUT NEEDS FIXES`

Portfolio-readiness score: `7.2/10`

## What the repo actually is
SpecForge is a deterministic local brief-analysis pipeline with three product surfaces:

- CLI for `analyze`, `generate`, and `demo`
- FastAPI endpoints for `/health`, `/analyze`, `/generate`, and `/demo`
- Server-rendered browser UI at `/` and `/ui`

It normalizes plain-text briefs, infers ambiguities, contradictions, missing decisions, and assumptions, then exports a repo-local bundle of markdown and JSON artifacts under `outputs/`.

This description is verified by actual runs, not just README claims.

## Current verified capabilities
- `make lint` passed.
- `make test` passed with 31 tests.
- CLI `analyze` worked on bundled and custom briefs.
- CLI `generate` wrote a local bundle under `outputs/`.
- FastAPI server started locally on `127.0.0.1:8000`.
- API `GET /health` returned the expected health payload.
- API `POST /analyze` returned structured counts, open questions, and MVP guidance.
- API `POST /generate` wrote a bundle with expected artifact files.
- UI `GET /ui` rendered the full intake flow.
- UI `POST /ui/analyze` rendered localized analysis output.
- UI `POST /ui/generate` rendered generated-bundle preview data.
- UI `POST /ui/new` reset the flow and restored the empty state.
- Eval runner completed 22/22 passing cases and wrote outputs under `outputs/evals/stage-05`.

## Portfolio-readiness assessment
Strengths:

- The repo is understandable within a few minutes.
- The project is runnable locally with standard Python tooling.
- Structure is mostly sane: `domain`, `pipeline`, `api`, `ui`, `eval`, and tests are separated cleanly.
- The product has actual surfaces, not just an internal library.
- The UI is calm and recruiter-demo friendly by default.

Weaknesses:

- The strongest README claims are overstated. The repo does not yet feel robust enough to freeze as a flagship.
- The eval harness is strong as local engineering scaffolding, but it is still structurally self-referential. It proves the rules match the corpus more than it proves the product is resilient.
- A hiring manager looking closely will find mixed-language exports, brittle contradiction detection, and shallow generated recommendations quickly.
- A tracked `.DS_Store` file is small, but it signals avoidable portfolio sloppiness.

Assessment: credible MVP, not a “freeze now” portfolio showcase.

## Product usefulness assessment
Useful now:

- It turns vague briefs into explicit unanswered questions reliably.
- It is good at surfacing missing basics: user, platform, success criteria, timing, ownership.
- It gives a deterministic first-pass triage layer for local demo use.

Weak now:

- Several outputs are too shallow to feel like strong delivery artifacts.
- “Recommended MVP cut” often collapses into rephrasing the source sentence instead of actually decomposing scope.
- On overloaded briefs, the recommendations can still be generic and obvious rather than surgically helpful.

Practical judgment: helpful as a brief hygiene tool, not yet strong as a serious planning assistant.

## UX/UI audit
What works:

- Flow is clear: intake, analysis, generation.
- Empty state is explicit.
- Reset is present and works.
- Local-only output messaging is visible and trust-building.
- Generated bundle preview is integrated into the main flow.
- Russian UI localization is materially better than a partially translated shell.

What still hurts:

- Demo option labels remain English even when the UI switches to Russian.
- Results are text-heavy and still feel closer to a structured diagnostic console than a polished local product.
- Output readability is acceptable, but artifact previews do not create much “wow” value for a recruiter demo.
- The UI feels calm, but not memorable.

Assessment: solid MVP UX, not premium portfolio UX.

## Language behavior audit
English:

- English UI and API outputs are coherent.
- Short-brief handling is good in English.

Russian:

- Russian UI copy is coherent and mostly consistent.
- Russian contradiction descriptions and recommendations render correctly in the UI and CLI.

Still broken enough to matter:

- Russian exported artifacts still leak English product labels and inferred terms. Example from the verified Russian export: `Тип продукта: software tool`, `Аудитория: operations team`, `local-first`.
- CLI titles derived from file names can override better in-brief Russian titles, producing awkward artifacts such as `Specforge Ru Generate`.
- This is not catastrophic for an internal demo, but it is below flagship portfolio polish.

Assessment: bilingual support is improved, but not consistent enough to claim fully trustworthy language-following exports.

## Contradiction-detection audit
What is verified:

- Corpus cases pass, including overloaded English and Russian eval cases.
- Bundled contradiction demo detects three contradiction families.
- Curated contradiction categories are cleaner than a noisy duplicate list.

What failed under realistic phrasing:

- Russian overloaded smoke brief:
  - realistic brief with low budget + 2-week timeline + web and mobile + multiple integrations + 2-person team
  - actual result: only `2` contradictions, not `3`
- English overloaded smoke brief:
  - realistic brief with low budget + 10-day timeline + web and mobile + several integrations + 2-person team
  - actual result: only `2` contradictions, not `3`

Interpretation:

- The rules are still brittle to phrasing. They pass the curated corpus, but they are not yet reliably robust across equivalent wording.
- This directly undermines the README claim of stronger overloaded-brief detection.

Assessment: improved, but still not strong enough to call solved.

## Artifact quality audit
Strengths:

- Artifact set is complete and consistent.
- Local output handling is safe and constrained for API/UI paths.
- Markdown structure is readable.

Weaknesses:

- Artifacts are often too generic.
- `scope.md` and `mvp_cut_plan.md` can feel thin and repetitive.
- Some “goals” extraction collapses entire paragraphs into a single goal, which poisons downstream usefulness.
- Russian export wording still mixes languages and leaves prototype smell.

Assessment: artifact generation is real, but the artifacts are still intermediate-quality demo outputs, not strong delivery documents.

## Engineering quality audit
Strengths:

- Repo structure is clear.
- Core modules are reasonably separated.
- Test coverage breadth is good for a demo repo: CLI, API, UI, eval, intake, generation.
- Local safety posture is sensible: API/UI export only inside the repo.
- Run ergonomics are straightforward through `make`, CLI, and `uvicorn`.

Weaknesses:

- The eval harness is structurally strong but semantically forgiving.
- The repo still contains some portfolio-noise artifacts, including a tracked `.DS_Store`.
- A few files are getting large enough to deserve more decomposition:
  - `analysis_signals.py` at 461 lines
  - `export_render.py` at 370 lines
  - `intake.py` at 351 lines
- Documentation is directionally truthful, but the wording around contradiction robustness and bilingual consistency is still stronger than the observed behavior.

Assessment: strong MVP engineering quality, not fully tightened portfolio engineering quality.

## Top findings ranked by severity
1. High: Contradiction detection still misses one contradiction family on realistic overloaded wording outside the curated eval phrases. This is the biggest freeze blocker because it targets a headline claim.
2. High: Russian exports are still not language-consistent enough for a polished local MVP. Mixed Russian/English artifact wording is immediately visible.
3. Medium: Generated outputs are often structured-but-shallow. The product helps diagnose briefs more than it helps produce persuasive delivery artifacts.
4. Medium: Eval results overstate confidence. `22/22` passing is real, but the harness does not prove enough semantic robustness.
5. Low: Repository presentation still has avoidable portfolio roughness, including a tracked `.DS_Store` and some residual stage-label framing.

## Final verdict
`MVP BUT NEEDS FIXES`

Smallest remaining blockers before a freeze:

- Make contradiction detection robust to wording variants for tiny-team overloaded briefs in both English and Russian.
- Eliminate mixed-language values from Russian exports.
- Improve artifact usefulness so MVP guidance is more decomposed and less echo-like.
- Remove visible repo sloppiness and tone down any README claims that exceed verified behavior.
