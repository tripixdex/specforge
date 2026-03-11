"""Deterministic contradiction and missing-decision rules."""

from __future__ import annotations

from specforge.domain.models import (
    ConstraintSet,
    ContradictionFinding,
    MissingDecision,
    NormalizedBrief,
)
from specforge.pipeline.analysis_signals import (
    collect_contradiction_evidence,
    find_evidence,
    has_broad_scope_signal,
    has_enterprise_scope_signal,
    has_monetization_signal,
    has_owner_signal,
    has_security_signal,
    infer_team_size_count,
    requires_security_decision,
)


def infer_contradictions(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
) -> list[ContradictionFinding]:
    """Detect conflicting planning signals."""

    findings: list[ContradictionFinding] = []
    lowered = brief.normalized_text.lower()
    broad_scope = has_broad_scope_signal(brief)
    enterprise_scope = has_enterprise_scope_signal(lowered)
    if (
        "speed prioritized" in constraints.speed_quality_budget_tradeoffs
        and "budget prioritized" in constraints.speed_quality_budget_tradeoffs
        and broad_scope
    ):
        findings.append(
            ContradictionFinding(
                category="fast-cheap-feature-rich",
                severity="high",
                description=(
                    "The brief asks for speed and low cost while also implying a "
                    "broad feature surface."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    ["speed", "budget", "dashboard", "all-in-one", "multiple workflows"],
                ),
                recommendation=(
                    "Cut the first release to one primary workflow and defer "
                    "secondary feature areas."
                ),
                source_type="inferred",
            )
        )
    if any(word in lowered for word in ["mvp", "minimal", "prototype"]) and enterprise_scope:
        findings.append(
            ContradictionFinding(
                category="minimal-mvp-vs-enterprise-scope",
                severity="high",
                description=(
                    "The brief describes a minimal MVP while also requesting "
                    "enterprise-grade scope."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    ["mvp", "minimal", "enterprise", "sso", "audit", "compliance"],
                ),
                recommendation=(
                    "Remove enterprise requirements from the first milestone or "
                    "stop calling it minimal."
                ),
                source_type="explicit",
            )
        )
    if constraints.timeline and infer_team_size_count(constraints.team_size) <= 2 and broad_scope:
        if any(word in constraints.timeline.lower() for word in ["asap", "day", "week", "weeks"]):
            findings.append(
                ContradictionFinding(
                    category="small-team-aggressive-deadline-broad-scope",
                    severity="high",
                    description=(
                        "A small team, aggressive deadline, and broad scope are "
                        "in tension."
                    ),
                    evidence=collect_contradiction_evidence(
                        brief,
                        [
                            constraints.timeline,
                            constraints.team_size or "",
                            "goals",
                            "platform",
                        ],
                    ),
                    recommendation=(
                        "Reduce scope to a narrower MVP cut before committing "
                        "to the deadline."
                    ),
                    source_type="inferred",
                )
            )
    return findings


def infer_missing_decisions(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
) -> list[MissingDecision]:
    """Collect planning decisions that should be made before deeper generation."""

    decisions: list[MissingDecision] = []
    lowered = brief.normalized_text.lower()
    if not brief.audience:
        decisions.append(
            MissingDecision(
                category="target_user",
                severity="high",
                description="The target user decision is still unresolved.",
                evidence=[brief.summary],
                recommendation=(
                    "Choose a single primary user before expanding detailed "
                    "requirements."
                ),
                source_type="unresolved",
            )
        )
    if not constraints.platform_hints:
        decisions.append(
            MissingDecision(
                category="platform",
                severity="high",
                description="The first platform decision is not made.",
                evidence=[brief.summary],
                recommendation="Choose one initial platform and treat others as deferred.",
                source_type="unresolved",
            )
        )
    if constraints.audience_hint in {"b2b", "b2c"} and not has_monetization_signal(brief):
        decisions.append(
            MissingDecision(
                category="pricing",
                severity="medium",
                description=(
                    "The brief does not say whether pricing is deferred or what "
                    "pricing direction exists."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    ["b2b", "b2c", "client", "customer"],
                )[:2],
                recommendation=(
                    "Decide whether pricing is part of scope, intentionally "
                    "deferred, or fixed by business model."
                ),
                source_type="unresolved",
            )
        )
    if requires_security_decision(lowered) and not has_security_signal(lowered):
        decisions.append(
            MissingDecision(
                category="compliance_security",
                severity="high",
                description=(
                    "The brief implies sensitive or enterprise usage but leaves "
                    "security and compliance decisions open."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    ["enterprise", "patient", "financial", "customer data", "compliance"],
                )[:3],
                recommendation=(
                    "Decide the minimum security/compliance bar before committing "
                    "to enterprise or sensitive data scope."
                ),
                source_type="unresolved",
            )
        )
    if constraints.audience_hint == "internal" and not has_owner_signal(lowered):
        decisions.append(
            MissingDecision(
                category="ownership_operations",
                severity="medium",
                description=(
                    "The brief does not identify who owns or operates the internal "
                    "workflow after launch."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    ["internal", "ops team", "operations team"],
                )[:2],
                recommendation=(
                    "Assign an owner for the workflow, admin tasks, and "
                    "operational upkeep."
                ),
                source_type="unresolved",
            )
        )
    return decisions
