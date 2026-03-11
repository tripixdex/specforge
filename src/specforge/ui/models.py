"""View models for the local SpecForge browser UI."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FindingView(BaseModel):
    """UI-friendly rendering of one analysis finding."""

    category: str
    severity: str
    description: str
    recommendation: str
    evidence: list[str] = Field(default_factory=list)


class ArtifactPreviewView(BaseModel):
    """UI-friendly rendering of one exported artifact."""

    name: str
    relative_path: str
    kind: str
    preview: str


class UiResultView(BaseModel):
    """Full UI state for one analyzed or generated brief."""

    title: str
    source_text: str
    normalized_summary: str
    ambiguity_findings: list[FindingView] = Field(default_factory=list)
    contradiction_findings: list[FindingView] = Field(default_factory=list)
    missing_decisions: list[FindingView] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    recommended_mvp_cut: list[str] = Field(default_factory=list)
    output_path: str | None = None
    artifact_previews: list[ArtifactPreviewView] = Field(default_factory=list)
    artifact_names: list[str] = Field(default_factory=list)
    mode: str
    counts: dict[str, int] = Field(default_factory=dict)
