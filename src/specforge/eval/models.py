"""Typed models for the local evaluation harness."""

from __future__ import annotations

from pydantic import BaseModel, Field


class EvalExpectations(BaseModel):
    """Practical structural expectations for one eval case."""

    min_ambiguities: int = 0
    min_contradictions: int = 0
    min_missing_decisions: int = 0
    min_assumptions: int = 0
    require_mvp_cut: bool = True
    required_ambiguity_categories: list[str] = Field(default_factory=list)
    required_contradiction_categories: list[str] = Field(default_factory=list)
    required_missing_decision_categories: list[str] = Field(default_factory=list)
    required_artifacts: list[str] = Field(default_factory=list)


class EvalCase(BaseModel):
    """One corpus case."""

    case_id: str
    segment: str
    title: str
    brief_text: str
    expectations: EvalExpectations


class EvalCheckResult(BaseModel):
    """One scored check inside an eval case."""

    name: str
    passed: bool
    detail: str


class EvalCaseResult(BaseModel):
    """Recorded result for one eval case."""

    case_id: str
    segment: str
    passed: bool
    score: float
    counts: dict[str, int]
    checks: list[EvalCheckResult] = Field(default_factory=list)
    generated_files: list[str] = Field(default_factory=list)
    output_path: str


class EvalRunSummary(BaseModel):
    """Top-level eval run artifact."""

    stage: str = "stage-5-eval-and-hardening"
    total_cases: int
    passed_cases: int
    failed_cases: int
    score_percent: float
    results: list[EvalCaseResult] = Field(default_factory=list)
    corpus_files: list[str] = Field(default_factory=list)
    output_root: str
