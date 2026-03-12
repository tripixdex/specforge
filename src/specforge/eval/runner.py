"""Deterministic local evaluation runner for SpecForge."""

from __future__ import annotations

import argparse
from pathlib import Path

from specforge.domain.models import AnalysisReport
from specforge.eval.loader import load_eval_cases
from specforge.eval.models import EvalCase, EvalCaseResult, EvalCheckResult, EvalRunSummary
from specforge.eval.reporting import write_summary_artifacts
from specforge.pipeline import (
    analyze_brief,
    create_raw_brief,
    export_delivery_pack,
    generate_delivery_pack,
    normalize_brief,
)

REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_OUTPUT_ROOT = REPO_ROOT / "outputs" / "evals" / "stage-05"
DEFAULT_REQUIRED_ARTIFACTS = [
    "analysis_report.md",
    "assumption_ledger.md",
    "assumptions.md",
    "brief.md",
    "constraints.md",
    "mvp_cut_plan.md",
    "open_questions.md",
    "risk_register.md",
    "scope.md",
    "summary.json",
]


def run_evaluation(
    *,
    output_root: Path = DEFAULT_OUTPUT_ROOT,
    case_ids: set[str] | None = None,
) -> EvalRunSummary:
    """Run the evaluation corpus and write per-case bundles under a local directory."""

    cases, corpus_files = load_eval_cases()
    selected_cases = [case for case in cases if case_ids is None or case.case_id in case_ids]
    if not selected_cases:
        raise ValueError("No eval cases selected.")

    output_root.mkdir(parents=True, exist_ok=True)
    results = [run_case(case, output_root=output_root) for case in selected_cases]
    passed_cases = sum(1 for item in results if item.passed)
    total_cases = len(results)
    summary = EvalRunSummary(
        total_cases=total_cases,
        passed_cases=passed_cases,
        failed_cases=total_cases - passed_cases,
        score_percent=round((passed_cases / total_cases) * 100, 1),
        results=results,
        corpus_files=[str(path) for path in corpus_files],
        output_root=str(output_root.resolve()),
    )
    write_summary_artifacts(summary, output_root=output_root)
    return summary


def run_case(case: EvalCase, *, output_root: Path) -> EvalCaseResult:
    """Execute one eval case end to end."""

    brief = normalize_brief(create_raw_brief(case.brief_text, title=case.title))
    analyzed, report = analyze_brief(brief)
    pack = generate_delivery_pack(analyzed)
    output_dir = export_delivery_pack(pack, output_root=output_root, run_label=case.case_id)
    generated_files = sorted(path.name for path in output_dir.iterdir() if path.is_file())
    checks = build_case_checks(case, report=report, generated_files=generated_files)
    passed = all(check.passed for check in checks)
    score = round(sum(1 for check in checks if check.passed) / len(checks), 3)
    return EvalCaseResult(
        case_id=case.case_id,
        segment=case.segment,
        passed=passed,
        score=score,
        counts={
            "ambiguities": len(report.ambiguities),
            "contradictions": len(report.contradictions),
            "missing_decisions": len(report.missing_decisions),
            "assumptions": len(report.assumptions),
            "open_questions": len(report.prioritized_open_questions),
        },
        checks=checks,
        generated_files=generated_files,
        output_path=str(output_dir.resolve()),
    )


def build_case_checks(
    case: EvalCase,
    *,
    report: AnalysisReport,
    generated_files: list[str],
) -> list[EvalCheckResult]:
    """Score one case against structural expectations."""

    expectations = case.expectations
    required_artifacts = expectations.required_artifacts or DEFAULT_REQUIRED_ARTIFACTS
    ambiguity_categories = {item.category for item in report.ambiguities}
    contradiction_categories = {item.category for item in report.contradictions}
    missing_decision_categories = {item.category for item in report.missing_decisions}

    checks = [
        threshold_check(
            "ambiguity_count",
            actual=len(report.ambiguities),
            minimum=expectations.min_ambiguities,
        ),
        threshold_check(
            "contradiction_count",
            actual=len(report.contradictions),
            minimum=expectations.min_contradictions,
        ),
        max_threshold_check(
            "contradiction_count_ceiling",
            actual=len(report.contradictions),
            maximum=expectations.max_contradictions,
        ),
        threshold_check(
            "missing_decision_count",
            actual=len(report.missing_decisions),
            minimum=expectations.min_missing_decisions,
        ),
        threshold_check(
            "assumption_count",
            actual=len(report.assumptions),
            minimum=expectations.min_assumptions,
        ),
        EvalCheckResult(
            name="recommended_mvp_cut",
            passed=(not expectations.require_mvp_cut) or bool(report.recommended_mvp_cut),
            detail=(
                f"recommended_mvp_cut={len(report.recommended_mvp_cut)}"
                if report.recommended_mvp_cut
                else "recommended_mvp_cut=0"
            ),
        ),
        category_check(
            "ambiguity_categories",
            actual=ambiguity_categories,
            required=expectations.required_ambiguity_categories,
        ),
        category_check(
            "contradiction_categories",
            actual=contradiction_categories,
            required=expectations.required_contradiction_categories,
        ),
        category_check(
            "missing_decision_categories",
            actual=missing_decision_categories,
            required=expectations.required_missing_decision_categories,
        ),
        artifact_check(generated_files, required_artifacts),
    ]
    return checks


def threshold_check(name: str, *, actual: int, minimum: int) -> EvalCheckResult:
    """Compare one count threshold."""

    return EvalCheckResult(
        name=name,
        passed=actual >= minimum,
        detail=f"actual={actual}, expected>={minimum}",
    )


def max_threshold_check(name: str, *, actual: int, maximum: int | None) -> EvalCheckResult:
    """Optionally enforce a ceiling to keep outputs curated rather than noisy."""

    if maximum is None:
        return EvalCheckResult(
            name=name,
            passed=True,
            detail=f"actual={actual}, expected=unbounded",
        )
    return EvalCheckResult(
        name=name,
        passed=actual <= maximum,
        detail=f"actual={actual}, expected<={maximum}",
    )


def category_check(name: str, *, actual: set[str], required: list[str]) -> EvalCheckResult:
    """Check that required structural categories appear."""

    missing = sorted(set(required) - actual)
    return EvalCheckResult(
        name=name,
        passed=not missing,
        detail=(
            f"present={sorted(actual)}"
            if not required
            else f"required={sorted(required)}, missing={missing}, present={sorted(actual)}"
        ),
    )


def artifact_check(generated_files: list[str], required_artifacts: list[str]) -> EvalCheckResult:
    """Ensure the exported bundle includes the expected files."""

    missing = sorted(set(required_artifacts) - set(generated_files))
    return EvalCheckResult(
        name="artifact_completeness",
        passed=not missing,
        detail=f"missing={missing}, generated={generated_files}",
    )


def build_parser() -> argparse.ArgumentParser:
    """Create the eval runner CLI parser."""

    parser = argparse.ArgumentParser(prog="python -m specforge.eval.runner")
    parser.add_argument("--output-root", default=str(DEFAULT_OUTPUT_ROOT))
    parser.add_argument("--case-id", action="append", dest="case_ids", default=None)
    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the evaluation harness from the command line."""

    args = build_parser().parse_args(argv)
    summary = run_evaluation(
        output_root=Path(args.output_root),
        case_ids=set(args.case_ids) if args.case_ids else None,
    )
    print(
        "\n".join(
            [
                f"Eval output: {summary.output_root}",
                f"Cases: {summary.total_cases}",
                f"Passed: {summary.passed_cases}",
                f"Failed: {summary.failed_cases}",
                f"Score percent: {summary.score_percent}",
            ]
        )
    )
    return 0 if summary.failed_cases == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
