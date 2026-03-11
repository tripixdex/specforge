"""Markdown rendering helpers for exported delivery packs."""

from __future__ import annotations

from specforge.domain.models import AssumptionItem, DeliveryPack


def render_brief_markdown(pack: DeliveryPack) -> str:
    """Render the normalized brief as markdown."""

    audience = ", ".join(pack.brief.audience) if pack.brief.audience else "Unspecified"
    references = render_bullets(pack.brief.references, fallback="- None captured")
    notes = render_bullets(pack.brief.notes, fallback="- None captured")
    explicit_inputs = render_bullets(pack.explicit_user_input, fallback="- None captured")
    inferred = render_bullets(pack.inferred_structure, fallback="- None inferred")
    unresolved = render_bullets(
        pack.open_questions[:5],
        fallback="- No unresolved questions were generated",
    )
    return "\n".join(
        [
            "# Stage 2 Deterministic Draft: Brief",
            "",
            f"Title: {pack.brief.title}",
            f"Product Type: {pack.brief.product_type or 'Unspecified'}",
            f"Audience: {audience}",
            "",
            "## Summary",
            pack.brief_summary,
            "",
            "## Explicit User Input",
            explicit_inputs,
            "",
            "## Inferred Structure",
            inferred,
            "",
            "## Unresolved Questions",
            unresolved,
            "",
            "## Notes",
            notes,
            "",
            "## References",
            references,
            "",
            "## Source Text",
            "```text",
            pack.brief.normalized_text,
            "```",
        ]
    )


def render_scope_markdown(pack: DeliveryPack) -> str:
    """Render the scope draft."""

    goals = render_bullets(pack.goals, fallback="- No explicit goals were extracted")
    non_goals = render_bullets(pack.non_goals, fallback="- No explicit non-goals were extracted")
    scope = render_bullets(pack.scope_draft, fallback="- Scope draft is still minimal")
    return "\n".join(
        [
            "# Stage 2 Deterministic Draft: Scope",
            "",
            "## Goals",
            goals,
            "",
            "## Non-Goals",
            non_goals,
            "",
            "## Scope Draft",
            scope,
            "",
            "## First Step Recommendation",
            pack.first_step_recommendation,
        ]
    )


def render_constraints_markdown(pack: DeliveryPack) -> str:
    """Render structured constraints."""

    return "\n".join(
        [
            "# Stage 2 Deterministic Draft: Constraints",
            "",
            f"- Budget: {pack.constraints.budget or 'Unspecified'}",
            f"- Timeline: {pack.constraints.timeline or 'Unspecified'}",
            f"- Team Size: {pack.constraints.team_size or 'Unspecified'}",
            f"- Audience Hint: {pack.constraints.audience_hint or 'Unspecified'}",
            "- Platform Hints: "
            + (
                ", ".join(pack.constraints.platform_hints)
                if pack.constraints.platform_hints
                else "None extracted"
            ),
            "- Tradeoffs: "
            + (
                ", ".join(pack.constraints.speed_quality_budget_tradeoffs)
                if pack.constraints.speed_quality_budget_tradeoffs
                else "None extracted"
            ),
            "",
            "## Explicit Constraints",
            render_bullets(pack.constraints.explicit_constraints, fallback="- None extracted"),
        ]
    )


def render_open_questions_markdown(pack: DeliveryPack) -> str:
    """Render prioritized open questions."""

    return "\n".join(
        [
            "# Stage 2 Deterministic Draft: Open Questions",
            "",
            render_bullets(pack.open_questions, fallback="- No open questions were generated"),
        ]
    )


def render_assumptions_markdown(pack: DeliveryPack) -> str:
    """Render a short assumptions summary for compatibility with Stage 1 outputs."""

    return "\n".join(
        [
            "# Stage 2 Deterministic Draft: Assumptions",
            "",
            render_assumption_lines(pack.assumptions)
            or "- No deterministic assumptions were added",
        ]
    )


def render_assumption_ledger_markdown(pack: DeliveryPack) -> str:
    """Render the richer assumption ledger."""

    if not pack.assumptions:
        body = "- No deterministic assumptions were added"
    else:
        sections = []
        for item in pack.assumptions:
            sections.extend(render_assumption_block(item))
        body = "\n".join(sections)
    return "\n".join(["# Stage 2 Deterministic Draft: Assumption Ledger", "", body])


def render_analysis_report_markdown(pack: DeliveryPack) -> str:
    """Render the structured analysis report."""

    report = pack.analysis
    return "\n".join(
        [
            "# Stage 2 Deterministic Draft: Analysis Report",
            "",
            "## Counts",
            *(f"- {key}: {value}" for key, value in pack.analysis_counts.items()),
            "",
            "## Ambiguities",
            render_analysis_lines(report.ambiguities, fallback="- No ambiguity findings"),
            "",
            "## Contradictions",
            render_analysis_lines(report.contradictions, fallback="- No contradiction findings"),
            "",
            "## Missing Decisions",
            render_analysis_lines(report.missing_decisions, fallback="- No missing decisions"),
            "",
            "## Prioritized Open Questions",
            render_bullets(report.prioritized_open_questions, fallback="- No open questions"),
        ]
    )


def render_mvp_cut_plan_markdown(pack: DeliveryPack) -> str:
    """Render the recommended MVP cut plan."""

    cut = render_bullets(
        pack.recommended_mvp_cut,
        fallback="- No MVP cut recommendation was generated",
    )
    risky = render_bullets(
        pack.why_this_is_risky,
        fallback="- No major risks were generated",
    )
    return "\n".join(
        [
            "# Stage 2 Deterministic Draft: MVP Cut Plan",
            "",
            "## Recommended MVP Cut",
            cut,
            "",
            "## Why This Is Risky",
            risky,
        ]
    )


def render_risk_register_markdown(pack: DeliveryPack) -> str:
    """Render the seeded risk register."""

    return "\n".join(
        [
            "# Stage 2 Deterministic Draft: Risk Register",
            "",
            render_bullets(pack.risk_register, fallback="- No deterministic risks were seeded"),
        ]
    )


def render_analysis_lines(items: list[object], *, fallback: str) -> str:
    """Render finding objects with evidence and recommendations."""

    if not items:
        return fallback
    lines: list[str] = []
    for item in items:
        lines.append(
            f"- [{item.severity}] {item.category}: {item.description} "
            f"(source_type: {item.source_type}; recommendation: {item.recommendation})"
        )
        if getattr(item, "evidence", None):
            evidence = "; ".join(getattr(item, "evidence")[:3])
            lines.append(f"  Evidence: {evidence}")
    return "\n".join(lines)


def render_assumption_lines(items: list[AssumptionItem]) -> str:
    """Render assumption items as one-line bullets."""

    return "\n".join(
        f"- {item.statement} ({item.confidence}; rationale: {item.rationale})"
        for item in items
    )


def render_assumption_block(item: AssumptionItem) -> list[str]:
    """Render one assumption as a short block."""

    lines = [
        f"- [{item.confidence}] {item.category}: {item.statement}",
        f"  Description: {item.description}",
        f"  Rationale: {item.rationale}",
        f"  Recommendation: {item.recommendation}",
        f"  Source Type: {item.source_type}",
    ]
    if item.evidence:
        lines.append(f"  Evidence: {'; '.join(item.evidence[:3])}")
    return lines


def render_bullets(values: list[str], *, fallback: str) -> str:
    """Render a list of values as bullet lines."""

    if not values:
        return fallback
    return "\n".join(f"- {value}" for value in values)
