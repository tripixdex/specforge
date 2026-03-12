from pathlib import Path

from specforge.eval.loader import load_eval_cases
from specforge.eval.runner import run_evaluation


def test_eval_corpus_has_stage_5_coverage() -> None:
    cases, paths = load_eval_cases()

    assert len(paths) == 4
    assert len(cases) >= 25
    segments = {case.segment for case in cases}
    assert "vague founder brief" in segments
    assert "contradictory founder brief" in segments
    assert "realistic SMB brief" in segments
    assert "noisy internal-tool brief" in segments
    assert "impossible triangle" in segments
    case_ids = {case.case_id for case in cases}
    assert "founder_ru_overloaded_brief" in case_ids
    assert "edge_english_overloaded_multiplatform_mvp" in case_ids
    assert "founder_en_realistic_overloaded_phrase_variant" in case_ids
    assert "founder_ru_realistic_overloaded_phrase_variant" in case_ids
    assert "edge_resourced_enterprise_near_miss" in case_ids
    assert "edge_deferred_scope_near_miss" in case_ids


def test_eval_runner_writes_summary_and_bundle(tmp_path: Path) -> None:
    summary = run_evaluation(
        output_root=tmp_path / "eval-output",
        case_ids={"internal_clear_local_tool"},
    )

    assert summary.total_cases == 1
    assert summary.passed_cases == 1
    assert (tmp_path / "eval-output" / "eval_summary.json").exists()
    case_output = Path(summary.results[0].output_path)
    assert (case_output / "summary.json").exists()
