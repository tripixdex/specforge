"""Typed request and response models for the SpecForge API."""

from __future__ import annotations

from typing import Any, Literal

from pydantic import BaseModel, ConfigDict, Field, field_validator

from specforge.input_validation import (
    MAX_BRIEF_LENGTH,
    MAX_LABEL_LENGTH,
    MAX_TITLE_LENGTH,
    normalize_brief_text,
    normalize_metadata,
    normalize_optional_text,
)

LABEL_PATTERN = r"^[A-Za-z0-9][A-Za-z0-9 _-]{0,63}$"


class BriefRequestBase(BaseModel):
    """Shared request fields for analysis and generation."""

    model_config = ConfigDict(extra="forbid")

    brief_text: str = Field(
        ...,
        min_length=1,
        max_length=MAX_BRIEF_LENGTH,
        description="Raw plain-text product brief.",
    )
    title: str | None = Field(default=None, max_length=MAX_TITLE_LENGTH)
    source_type: str | None = Field(default="api", max_length=40)
    product_type: str | None = Field(default=None, max_length=80)
    audience: list[str] = Field(default_factory=list, max_length=10)
    goals: list[str] = Field(default_factory=list, max_length=20)
    non_goals: list[str] = Field(default_factory=list, max_length=20)
    notes: list[str] = Field(default_factory=list, max_length=20)
    references: list[str] = Field(default_factory=list, max_length=20)
    metadata: dict[str, str] = Field(default_factory=dict)

    @field_validator("brief_text")
    @classmethod
    def validate_brief_text(cls, value: str) -> str:
        """Reject empty or whitespace-only briefs."""

        return normalize_brief_text(value)

    @field_validator("title", "source_type", "product_type")
    @classmethod
    def validate_optional_text(cls, value: str | None, info) -> str | None:
        """Trim optional text fields and reject oversized values."""

        field_name = info.field_name or "field"
        max_length = MAX_TITLE_LENGTH if field_name == "title" else 80
        if field_name == "source_type":
            max_length = 40
        return normalize_optional_text(value, field_name=field_name, max_length=max_length)

    @field_validator("metadata")
    @classmethod
    def validate_metadata(cls, value: dict[str, str]) -> dict[str, str]:
        """Keep metadata small and stringly typed."""

        return normalize_metadata(value)


class AnalyzeRequest(BriefRequestBase):
    """Analyze a brief without exporting files."""

    analysis_mode: Literal["deterministic"] = "deterministic"


class GenerateRequest(BriefRequestBase):
    """Generate a local delivery bundle from a brief."""

    analysis_mode: Literal["deterministic"] = "deterministic"
    output_label: str | None = Field(
        default=None,
        max_length=MAX_LABEL_LENGTH,
        pattern=LABEL_PATTERN,
        description="Optional label used to name the repo-local output folder.",
    )

    @field_validator("output_label", mode="before")
    @classmethod
    def validate_output_label(cls, value: str | None) -> str | None:
        """Strip label whitespace before pattern validation."""

        return normalize_optional_text(
            value,
            field_name="output_label",
            max_length=MAX_LABEL_LENGTH,
        )


class FindingCounts(BaseModel):
    """Summary counts for analysis output."""

    ambiguities: int
    contradictions: int
    missing_decisions: int
    assumptions: int
    open_questions: int


class BriefSummaryResponse(BaseModel):
    """Structured normalized brief summary."""

    title: str
    product_type: str | None = None
    audience: list[str] = Field(default_factory=list)
    goals: list[str] = Field(default_factory=list)
    non_goals: list[str] = Field(default_factory=list)
    summary: str


class AnalyzeResponse(BaseModel):
    """Structured analysis response."""

    brief: BriefSummaryResponse
    analysis_mode: Literal["deterministic"] = "deterministic"
    normalized_summary: str
    counts: FindingCounts
    top_open_questions: list[str] = Field(default_factory=list)
    recommended_mvp_cut: list[str] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)


class GenerateResponse(AnalyzeResponse):
    """Structured generation response with export details."""

    output_path: str
    artifact_files: list[str] = Field(default_factory=list)


class DemoResponse(BaseModel):
    """Demo metadata and sample analysis response."""

    demo_name: str
    demo_input_path: str
    available_demos: list[str] = Field(default_factory=list)
    sample_analysis: AnalyzeResponse


class HealthResponse(BaseModel):
    """Simple API health response."""

    status: Literal["ok"] = "ok"
    app: Literal["specforge"] = "specforge"
    stage: Literal["stage-5-7-final-fix-pass"] = "stage-5-7-final-fix-pass"


class ErrorResponse(BaseModel):
    """Normalized API error response."""

    error: str
    detail: str | list[dict[str, Any]]
