# Executive summary

SpecForge is close, but it should not be frozen yet as a flagship portfolio project.

The repo is a credible local deterministic brief-analysis demo with a real CLI, FastAPI surface, server-rendered UI, export pipeline, and a working eval harness. `make lint`, `make test`, and the full eval run all passed. Contradiction detection on overloaded English and Russian briefs is strong and restrained on the near-miss case.

The smallest remaining freeze blockers are polish blockers, not architecture blockers: Russian export artifacts still leak obvious English/internal field values, and the normal demo path still exposes stage/remediation wording and raw internal JSON metadata. Those issues directly cut against the "intentionally finished" bar for a flagship portfolio freeze.

# What the repo actually is

SpecForge is a local-first deterministic rules engine for turning messy briefs into:

- structured analysis findings
- recommended MVP cuts and open questions
- repo-local markdown and JSON export bundles
- the same flow through CLI, API, UI, and eval surfaces

It is not an LLM product, hosted SaaS, or autonomous PM system. The current implementation is a disciplined local demo product with bounded scope.

# Current verified capabilities

- `make lint` passed.
- `make test` passed with 38 tests.
- `python3 -m specforge.eval.runner` passed 26/26 eval cases.
- CLI analysis worked on a realistic overloaded English brief and reported 4 ambiguities, 3 contradictions, and 2 missing decisions.
- Direct pipeline smoke checks showed:
  - EN overloaded: 3 contradictions in the expected curated families.
  - RU overloaded: 3 contradictions in the expected curated families.
  - Near miss: 0 contradictions.
- Live API verification worked for `/health`, `/demo`, and `/generate`.
- Live UI verification worked for `/ui`, `/ui/generate`, and `/ui/new`.
- API output-label validation rejected `../escape` with a 422 validation error.
- EN and RU export bundles were generated under repo-local `outputs/`.

# Freeze-readiness assessment

Not freeze-ready yet.

Why it is close:

- The product concept is legible quickly.
- The deterministic scope is honest and mostly well executed.
- The repo runs cleanly and the evaluation harness gives the project real credibility.

Why it still misses the flagship freeze bar:

- The normal RU export path still leaks English/internal display values.
- The normal demo path still shows stage/remediation wording and raw internal metadata.
- The repo root is cluttered with audit artifacts, which weakens first-impression polish for portfolio review.

# Contradiction-detection assessment

Strong overall.

- EN overloaded brief: contradiction behavior was strong and curated, with exactly 3 contradictions in `fast-cheap-feature-rich`, `small-team-aggressive-deadline-broad-scope`, and `minimal-mvp-vs-enterprise-scope`.
- RU overloaded brief: same result, also exactly 3 contradictions with coherent RU-facing questions and MVP guidance.
- Near-miss brief: contradiction count stayed at 0, which is the right restraint.

Residual issue:

- The near-miss brief still received MVP guidance to choose one primary platform even though mobile was explicitly deferred post-MVP. That is not a contradiction false positive, but it is still mildly over-eager product advice.

# Language behavior assessment

Mixed.

Verified good:

- RU input produced coherent RU-facing API output, UI output, open questions, and MVP guidance.
- EN input produced coherent EN-facing output.
- Core human-facing labels like audience, platform, tradeoffs, and team size are localized in several exported artifacts.

Verified bad:

- Russian export artifacts still leak English/internal values in a normal path. In `outputs/freeze-ru-api/analysis_report.md`, the RU report still shows `ambiguities`, `contradictions`, `missing_decisions`, `source_type`, and enum values like `unresolved`, `inferred`, and `explicit`.
- README claims about stronger bilingual export consistency are therefore only partially verified.

# Artifact quality assessment

Good MVP quality, not outstanding product polish.

- The generated artifact set is useful for the concept: `brief.md`, `scope.md`, `constraints.md`, `open_questions.md`, `analysis_report.md`, `mvp_cut_plan.md`, and `risk_register.md` are materially usable for a local demo.
- The MVP cut output is more useful than a toy summary because it separates scope cuts, unresolved decisions, and major risks.
- The bundle is still somewhat prototype-like because `summary.json` is exposed as a normal preview artifact and internal schema vocabulary is not fully hidden.

# UX/UI assessment

Mostly solid.

- Flow clarity is good: intake, analysis, generation.
- Empty states are explicit and readable.
- Reset/new-brief flow worked and correctly cleared the textarea and title while retaining RU locale on the reset path.
- Output-path display is calmer than dumping an absolute path immediately.

Remaining UX/UI polish issues:

- The UI hero still presents `SpecForge Stage 5.9`, which reads like an internal delivery milestone rather than a finished product.
- The generated artifact preview includes raw `summary.json`, exposing internal fields like `stage_label` in the user-facing demo path.

# Engineering quality assessment

Overall engineering quality is good.

- Repo structure is sensible and modular.
- Tests and eval coverage are strong for a project of this size.
- Output safety is good: API generation stays under `outputs/`, and invalid traversal-style labels are rejected.
- File sizes are generally reasonable. The only notably large module is `analysis_signals.py` at 546 lines, which is acceptable but the first place likely to become unwieldy.

Engineering/presentation gaps:

- Docs are directionally truthful, but the README overstates export-language polish relative to the current RU export evidence.
- Repo root presentation is noisy for a flagship portfolio project because prior audit and report artifacts are mixed into the top level.

# Top findings ranked by severity

1. High: Russian export artifacts still leak English/internal display values in the normal user path, which directly contradicts the intended bilingual-finish bar and weakens README truthfulness. Evidence: [src/specforge/pipeline/export_render.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export_render.py#L232), [src/specforge/pipeline/export_render.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/pipeline/export_render.py#L335), [outputs/freeze-ru-api/analysis_report.md](/Users/vladgurov/Desktop/work/specforge/outputs/freeze-ru-api/analysis_report.md)
2. Medium: Internal stage/remediation wording still leaks through the public demo surface and API, so the product does not feel intentionally finished. Evidence: [src/specforge/ui/copy.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/copy.py#L13), [src/specforge/api/schemas.py](/Users/vladgurov/Desktop/work/specforge/src/specforge/api/schemas.py#L146), [README.md](/Users/vladgurov/Desktop/work/specforge/README.md#L3)
3. Medium: The UI previews raw `summary.json`, exposing internal metadata such as `stage_label` and `generated_at` in the normal generation flow. Evidence: [src/specforge/ui/templates/index.html](/Users/vladgurov/Desktop/work/specforge/src/specforge/ui/templates/index.html#L256), [outputs/freeze-en-ui/summary.json](/Users/vladgurov/Desktop/work/specforge/outputs/freeze-en-ui/summary.json)
4. Low: The near-miss brief avoided contradiction false positives, but MVP guidance still overreacts to explicitly deferred mobile scope, which suggests the restraint layer is not fully tuned yet.
5. Low: The repo root remains cluttered with audit artifacts and reports, which hurts flagship portfolio presentation even though it does not break the product.

# Final verdict

MVP BUT NEEDS FIXES

Should SpecForge now be frozen as a flagship portfolio project?

No.

It is a good MVP and a credible local demo product, but it is not yet polished enough to freeze as a flagship portfolio repo. The smallest blockers are:

- fully localize RU export artifacts
- remove internal stage/remediation language from the public demo path
- stop surfacing raw internal JSON metadata in the main UI preview flow
