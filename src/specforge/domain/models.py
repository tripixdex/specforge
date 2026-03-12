"""Core domain models for the SpecForge Stage 2 deterministic pipeline."""

from __future__ import annotations

from typing import Literal

from pydantic import BaseModel, Field

SeverityLevel = Literal["low", "medium", "high"]
SourceType = Literal["explicit", "inferred", "unresolved"]


class ConstraintSet(BaseModel):
    """Structured constraints inferred or supplied from a brief."""

    budget: str | None = None
    timeline: str | None = None
    team_size: str | None = None
    platform_hints: list[str] = Field(default_factory=list)
    audience_hint: str | None = None
    speed_quality_budget_tradeoffs: list[str] = Field(default_factory=list)
    explicit_constraints: list[str] = Field(default_factory=list)
    non_goals: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)


class AssumptionItem(BaseModel):
    """An explicit assumption introduced by deterministic interpretation."""

    category: str = "planning"
    severity: SeverityLevel = "medium"
    statement: str
    description: str
    rationale: str
    evidence: list[str] = Field(default_factory=list)
    recommendation: str
    source_type: SourceType = "inferred"
    confidence: Literal["low", "medium", "high"] = "low"


class AmbiguityFinding(BaseModel):
    """A missing or unclear area that requires follow-up."""

    category: str
    severity: SeverityLevel = "medium"
    description: str
    evidence: list[str] = Field(default_factory=list)
    recommendation: str
    source_type: SourceType = "unresolved"
    question: str


class ContradictionFinding(BaseModel):
    """A conflicting set of signals that weakens planning consistency."""

    category: str
    severity: SeverityLevel = "medium"
    description: str
    evidence: list[str] = Field(default_factory=list)
    recommendation: str
    source_type: SourceType = "inferred"


class MissingDecision(BaseModel):
    """A decision that should be made before deeper planning."""

    category: str
    severity: SeverityLevel = "medium"
    description: str
    evidence: list[str] = Field(default_factory=list)
    recommendation: str
    source_type: SourceType = "unresolved"


class TraceabilityLink(BaseModel):
    """A lightweight link between source evidence and generated output."""

    source_excerpt: str
    target_section: str
    source_type: SourceType = "explicit"


class AnalysisReport(BaseModel):
    """Deterministic analytical findings produced from a normalized brief."""

    stage_label: str = "specforge-deterministic-analysis"
    analyzer_type: str = "deterministic"
    ambiguities: list[AmbiguityFinding] = Field(default_factory=list)
    contradictions: list[ContradictionFinding] = Field(default_factory=list)
    missing_decisions: list[MissingDecision] = Field(default_factory=list)
    assumptions: list[AssumptionItem] = Field(default_factory=list)
    prioritized_open_questions: list[str] = Field(default_factory=list)
    recommended_mvp_cut: list[str] = Field(default_factory=list)
    traceability_links: list[TraceabilityLink] = Field(default_factory=list)


class RawBrief(BaseModel):
    """Unstructured user input before normalization."""

    title: str
    source_text: str
    source_type: str = "freeform-notes"
    product_type: str | None = None
    audience: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    non_goals: list[str] = Field(default_factory=list)
    constraints: ConstraintSet = Field(default_factory=ConstraintSet)
    notes: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    metadata: dict[str, str] = Field(default_factory=dict)


class NormalizedBrief(BaseModel):
    """Structured brief representation produced by intake and analysis."""

    title: str
    source_text: str
    normalized_text: str
    summary: str
    product_type: str | None = None
    audience: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    non_goals: list[str] = Field(default_factory=list)
    constraints: ConstraintSet = Field(default_factory=ConstraintSet)
    assumptions: list[AssumptionItem] = Field(default_factory=list)
    open_questions: list[str] = Field(default_factory=list)
    risks: list[str] = Field(default_factory=list)
    notes: list[str] = Field(default_factory=list)
    references: list[str] = Field(default_factory=list)
    analysis: AnalysisReport | None = None


class DeliveryArtifact(BaseModel):
    """One exported file in a generated delivery pack bundle."""

    name: str
    kind: str
    relative_path: str
    content: str


class DeliveryPack(BaseModel):
    """Deterministic delivery pack generated in Stage 2."""

    stage_label: str = "specforge-deterministic-delivery-pack"
    generated_at: str
    brief: NormalizedBrief
    analysis: AnalysisReport = Field(default_factory=AnalysisReport)
    brief_summary: str
    goals: list[str] = Field(default_factory=list)
    non_goals: list[str] = Field(default_factory=list)
    scope_draft: list[str] = Field(default_factory=list)
    explicit_user_input: list[str] = Field(default_factory=list)
    inferred_structure: list[str] = Field(default_factory=list)
    constraints: ConstraintSet = Field(default_factory=ConstraintSet)
    open_questions: list[str] = Field(default_factory=list)
    assumptions: list[AssumptionItem] = Field(default_factory=list)
    risk_register: list[str] = Field(default_factory=list)
    recommended_mvp_cut: list[str] = Field(default_factory=list)
    why_this_is_risky: list[str] = Field(default_factory=list)
    first_step_recommendation: str
    analysis_counts: dict[str, int] = Field(default_factory=dict)
    artifacts: list[DeliveryArtifact] = Field(default_factory=list)
    output_dir: str | None = None
