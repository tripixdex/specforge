import json
from pathlib import Path

from specforge.pipeline.analyze import analyze_brief
from specforge.pipeline.export import export_delivery_pack
from specforge.pipeline.generate import generate_delivery_pack
from specforge.pipeline.intake import create_raw_brief, normalize_brief


def test_generation_and_export_create_analysis_artifacts(tmp_path: Path) -> None:
    text = """
    Internal Ops Tool
    Goals:
    - Reduce manual weekly reporting
    - Give the operations team one place to review blockers
    Constraints:
    - Keep it local-first
    - Budget under $10k
    """

    normalized = normalize_brief(create_raw_brief(text))
    analyzed, report = analyze_brief(normalized)
    pack = generate_delivery_pack(analyzed)
    output_dir = export_delivery_pack(pack, output_root=tmp_path, run_label="test-bundle")

    expected_files = {
        "analysis_report.md",
        "assumption_ledger.md",
        "brief.md",
        "constraints.md",
        "mvp_cut_plan.md",
        "open_questions.md",
        "risk_register.md",
        "scope.md",
        "summary.json",
    }

    assert pack.analysis is report
    assert expected_files.issubset({path.name for path in output_dir.iterdir()})

    summary = json.loads((output_dir / "summary.json").read_text(encoding="utf-8"))
    assert summary["analysis_counts"]["ambiguities"] >= 0
    assert "recommended_mvp_cut" in summary
    assert "Stage 2 Deterministic Draft" not in (output_dir / "analysis_report.md").read_text(
        encoding="utf-8"
    )


def test_export_slugifies_cyrillic_titles_readably(tmp_path: Path) -> None:
    text = """
    Платформа для агентства
    Нужен локальный инструмент для клиентских брифов.
    """

    normalized = normalize_brief(create_raw_brief(text))
    analyzed, _ = analyze_brief(normalized)
    pack = generate_delivery_pack(analyzed)
    output_dir = export_delivery_pack(pack, output_root=tmp_path)

    assert "platforma-dlya-agentstva" in output_dir.name
