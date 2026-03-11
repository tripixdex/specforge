"""Filesystem export for deterministic Stage 2 delivery packs."""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

from specforge.domain.models import DeliveryArtifact, DeliveryPack
from specforge.pipeline.export_render import (
    render_analysis_report_markdown,
    render_assumption_ledger_markdown,
    render_assumptions_markdown,
    render_brief_markdown,
    render_constraints_markdown,
    render_mvp_cut_plan_markdown,
    render_open_questions_markdown,
    render_risk_register_markdown,
    render_scope_markdown,
)


def export_delivery_pack(
    pack: DeliveryPack,
    *,
    output_root: str | Path = "outputs",
    run_label: str | None = None,
) -> Path:
    """Write a delivery pack bundle to the local filesystem."""

    root = Path(output_root).resolve()
    root.mkdir(parents=True, exist_ok=True)
    bundle_name = run_label or default_bundle_name(pack.brief.title)
    output_dir = root / slugify(bundle_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    pack.analysis_counts = pack.analysis_counts or {
        "ambiguities": len(pack.analysis.ambiguities),
        "contradictions": len(pack.analysis.contradictions),
        "missing_decisions": len(pack.analysis.missing_decisions),
        "assumptions": len(pack.assumptions),
        "open_questions": len(pack.open_questions),
    }

    artifact_specs = {
        "brief.md": render_brief_markdown(pack),
        "scope.md": render_scope_markdown(pack),
        "constraints.md": render_constraints_markdown(pack),
        "open_questions.md": render_open_questions_markdown(pack),
        "assumptions.md": render_assumptions_markdown(pack),
        "assumption_ledger.md": render_assumption_ledger_markdown(pack),
        "analysis_report.md": render_analysis_report_markdown(pack),
        "mvp_cut_plan.md": render_mvp_cut_plan_markdown(pack),
        "risk_register.md": render_risk_register_markdown(pack),
    }

    artifacts: list[DeliveryArtifact] = []
    for file_name, content in artifact_specs.items():
        file_path = output_dir / file_name
        file_path.write_text(content, encoding="utf-8")
        artifacts.append(
            DeliveryArtifact(
                name=file_name,
                kind="markdown",
                relative_path=file_name,
                content=content,
            )
        )

    pack.artifacts = artifacts
    pack.output_dir = str(output_dir)
    summary_path = output_dir / "summary.json"
    summary_path.write_text(json.dumps(pack.model_dump(), indent=2), encoding="utf-8")
    pack.artifacts.append(
        DeliveryArtifact(
            name="summary.json",
            kind="json",
            relative_path="summary.json",
            content=summary_path.read_text(encoding="utf-8"),
        )
    )
    return output_dir


def default_bundle_name(title: str) -> str:
    """Create a timestamped default bundle name."""

    timestamp = datetime.now(UTC).strftime("%Y%m%d-%H%M%S")
    return f"{title}-{timestamp}"


def slugify(value: str) -> str:
    """Create a filesystem-safe directory name."""

    slug = re.sub(r"[^a-zA-Z0-9]+", "-", value.strip().lower()).strip("-")
    return slug or "specforge-output"
