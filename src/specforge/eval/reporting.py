"""Summary rendering for eval results."""

from __future__ import annotations

import json
from pathlib import Path

from specforge.eval.models import EvalRunSummary


def write_summary_artifacts(summary: EvalRunSummary, *, output_root: Path) -> None:
    """Write stable JSON and markdown eval summaries."""

    json_path = output_root / "eval_summary.json"
    markdown_path = output_root / "eval_summary.md"
    json_path.write_text(json.dumps(summary.model_dump(), indent=2), encoding="utf-8")
    markdown_path.write_text(render_markdown_summary(summary), encoding="utf-8")


def render_markdown_summary(summary: EvalRunSummary) -> str:
    """Render a compact markdown summary artifact."""

    lines = [
        "# SpecForge Eval Summary",
        "",
        f"- Total cases: {summary.total_cases}",
        f"- Passed cases: {summary.passed_cases}",
        f"- Failed cases: {summary.failed_cases}",
        f"- Score percent: {summary.score_percent}",
        f"- Output root: `{summary.output_root}`",
        "",
        "## Cases",
        "",
    ]
    for result in summary.results:
        status = "PASS" if result.passed else "FAIL"
        lines.append(f"- `{result.case_id}` [{result.segment}] {status} ({result.score})")
    return "\n".join(lines) + "\n"
