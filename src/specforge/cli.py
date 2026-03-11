"""Minimal CLI for the Stage 2 deterministic SpecForge flow."""

from __future__ import annotations

import argparse
from pathlib import Path

from specforge.domain.models import AnalysisReport
from specforge.pipeline import (
    analyze_brief,
    create_raw_brief,
    export_delivery_pack,
    generate_delivery_pack,
    normalize_brief,
)

DEFAULT_DEMO_INPUT = Path("examples/founder_app_idea.txt")


def build_parser() -> argparse.ArgumentParser:
    """Create the CLI argument parser."""

    parser = argparse.ArgumentParser(prog="python -m specforge.cli")
    subparsers = parser.add_subparsers(dest="command", required=True)

    demo_parser = subparsers.add_parser(
        "demo",
        help="Run the deterministic pipeline against a bundled sample brief.",
    )
    demo_parser.add_argument("--input", default=str(DEFAULT_DEMO_INPUT))
    demo_parser.add_argument("--output-root", default="outputs")
    demo_parser.add_argument("--run-label", default="demo-founder-app")

    generate_parser = subparsers.add_parser(
        "generate",
        help="Generate a deterministic pack from an input brief.",
    )
    generate_parser.add_argument("--input", required=True)
    generate_parser.add_argument("--output-root", default="outputs")
    generate_parser.add_argument("--run-label", default=None)

    analyze_parser = subparsers.add_parser(
        "analyze",
        help="Analyze a brief and print a concise structured summary.",
    )
    analyze_parser.add_argument("--input", required=True)

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the selected CLI command."""

    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "analyze":
        analyzed, report, _ = run_analysis(Path(args.input))
        print(render_analysis_console(analyzed.summary, report))
        return 0

    if args.command in {"demo", "generate"}:
        input_path = Path(args.input)
        output_dir, report = run_generate(
            input_path,
            output_root=Path(args.output_root),
            run_label=args.run_label,
        )
        print(render_export_console(output_dir, report))
        return 0

    parser.error(f"Unknown command: {args.command}")
    return 2


def run_analysis(input_path: Path):
    """Run intake and analysis without exporting artifacts."""

    source_text = input_path.read_text(encoding="utf-8")
    raw_brief = create_raw_brief(
        source_text,
        title=input_path.stem.replace("_", " ").title(),
    )
    normalized = normalize_brief(raw_brief)
    analyzed, report = analyze_brief(normalized)
    return analyzed, report, raw_brief


def run_generate(
    input_path: Path,
    *,
    output_root: Path,
    run_label: str | None,
) -> tuple[Path, AnalysisReport]:
    """Run the deterministic pipeline for a text file and export the pack."""

    analyzed, report, _ = run_analysis(input_path)
    pack = generate_delivery_pack(analyzed)
    output_dir = export_delivery_pack(pack, output_root=output_root, run_label=run_label)
    return output_dir, report


def render_analysis_console(summary: str, report: AnalysisReport) -> str:
    """Render a concise analysis summary for terminal output."""

    top_questions = report.prioritized_open_questions[:3]
    recommended_cut = report.recommended_mvp_cut[:3]
    lines = [
        f"Summary: {summary}",
        f"Analyzer: {report.analyzer_type}",
        f"Ambiguities: {len(report.ambiguities)}",
        f"Contradictions: {len(report.contradictions)}",
        f"Missing decisions: {len(report.missing_decisions)}",
        "Top unresolved questions:",
    ]
    if top_questions:
        lines.extend(f"- {question}" for question in top_questions)
    else:
        lines.append("- None")
    lines.append("Recommended MVP cut:")
    if recommended_cut:
        lines.extend(f"- {item}" for item in recommended_cut)
    else:
        lines.append("- None")
    return "\n".join(lines)


def render_export_console(output_dir: Path, report: AnalysisReport) -> str:
    """Render a concise export summary for terminal output."""

    top_question = (
        report.prioritized_open_questions[0]
        if report.prioritized_open_questions
        else "None"
    )
    return "\n".join(
        [
            f"Output: {output_dir}",
            f"Ambiguities: {len(report.ambiguities)}",
            f"Contradictions: {len(report.contradictions)}",
            f"Missing decisions: {len(report.missing_decisions)}",
            f"Top unresolved question: {top_question}",
            (
                f"Recommended MVP cut: {report.recommended_mvp_cut[0]}"
                if report.recommended_mvp_cut
                else "Recommended MVP cut: None"
            ),
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
