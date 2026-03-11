# Evaluation Plan

## Evaluation Philosophy

SpecForge should first be evaluated on traceability and usefulness, not on intelligence theater. Stage 5 uses a local deterministic rubric: can the pipeline expose obvious tensions, missing decisions, and output completeness honestly and consistently across a varied brief corpus?

## Stage 5 Corpus Coverage

- vague founder briefs
- contradictory founder briefs
- underspecified client briefs
- realistic SMB briefs
- noisy internal-tool briefs
- impossible triangle cases
- subtle near-miss ambiguity cases
- briefs missing platform, user, monetization, budget, timeline, or security constraints

The Stage 5 corpus lives under [eval/](/Users/vladgurov/Desktop/work/specforge/eval) and currently includes 20 cases split across four files.

## Stage 5 Checks

Each case encodes practical expectations such as:

- `ambiguities >= N`
- `contradictions >= N`
- `missing_decisions >= N`
- `assumptions >= N`
- required ambiguity, contradiction, or missing-decision categories
- non-empty recommended MVP cut
- required generated artifacts including `analysis_report.md`, `assumption_ledger.md`, and `summary.json`

The runner does not require exact wording matches.

## Run Evals

```bash
make eval
python3 -m specforge.eval.runner
python3 -m specforge.eval.runner --case-id internal_clear_local_tool
```

Artifacts are written under [outputs/evals/](/Users/vladgurov/Desktop/work/specforge/outputs/evals).

## Limits

- this is a local deterministic rubric, not a statistically rigorous benchmark
- the corpus checks useful structure, not semantic quality in every sentence
- expert manual review is still needed for real audit-grade claims
