"""Markdown rendering helpers for exported delivery packs."""

from __future__ import annotations

from specforge.domain.models import AssumptionItem, DeliveryPack
from specforge.pipeline.language import (
    category_label,
    detect_language,
    display_audience,
    display_audience_mode,
    display_platform_hints,
    display_product_type,
    display_team_size,
    display_tradeoffs,
)


def render_brief_markdown(pack: DeliveryPack) -> str:
    """Render the normalized brief as markdown."""

    locale = detect_language(pack.brief.normalized_text)
    audience = (
        ", ".join(display_audience(pack.brief.audience, locale))
        if pack.brief.audience
        else ("Не указана" if locale == "ru" else "Unspecified")
    )
    product_type = display_product_type(pack.brief.product_type, locale)
    references = render_bullets(
        pack.brief.references,
        fallback="- Ничего не зафиксировано" if locale == "ru" else "- None captured",
    )
    notes = render_bullets(
        pack.brief.notes,
        fallback="- Ничего не зафиксировано" if locale == "ru" else "- None captured",
    )
    explicit_inputs = render_bullets(
        pack.explicit_user_input,
        fallback="- Ничего не зафиксировано" if locale == "ru" else "- None captured",
    )
    inferred = render_bullets(
        pack.inferred_structure,
        fallback="- Ничего не выведено" if locale == "ru" else "- None inferred",
    )
    unresolved = render_bullets(
        pack.open_questions[:5],
        fallback=(
            "- Открытые вопросы не были сгенерированы"
            if locale == "ru"
            else "- No unresolved questions were generated"
        ),
    )
    return "\n".join(
        [
            "# SpecForge: Бриф" if locale == "ru" else "# SpecForge Brief",
            "",
            f"{'Название' if locale == 'ru' else 'Title'}: {pack.brief.title}",
            f"{'Тип продукта' if locale == 'ru' else 'Product Type'}: "
            f"{product_type or ('Не указан' if locale == 'ru' else 'Unspecified')}",
            f"{'Аудитория' if locale == 'ru' else 'Audience'}: {audience}",
            "",
            "## Резюме" if locale == "ru" else "## Summary",
            pack.brief_summary,
            "",
            "## Явно указано в брифе" if locale == "ru" else "## Explicit Brief Input",
            explicit_inputs,
            "",
            "## Детерминированная интерпретация"
            if locale == "ru"
            else "## Deterministic Interpretation",
            inferred,
            "",
            "## Приоритетные открытые вопросы"
            if locale == "ru"
            else "## Priority Open Questions",
            unresolved,
            "",
            "## Заметки" if locale == "ru" else "## Notes",
            notes,
            "",
            "## Ссылки" if locale == "ru" else "## References",
            references,
            "",
            "## Исходный текст" if locale == "ru" else "## Source Text",
            "```text",
            pack.brief.normalized_text,
            "```",
        ]
    )


def render_scope_markdown(pack: DeliveryPack) -> str:
    """Render the scope draft."""

    locale = detect_language(pack.brief.normalized_text)
    goals = render_bullets(
        pack.goals,
        fallback="- Явные цели не выделены"
        if locale == "ru"
        else "- No explicit goals were extracted",
    )
    non_goals = render_bullets(
        pack.non_goals,
        fallback=(
            "- Явные не-цели не выделены"
            if locale == "ru"
            else "- No explicit non-goals were extracted"
        ),
    )
    scope = render_bullets(
        pack.scope_draft,
        fallback="- Черновик объема пока слишком узкий"
        if locale == "ru"
        else "- Scope draft is still minimal",
    )
    return "\n".join(
        [
            "# SpecForge: Объем" if locale == "ru" else "# SpecForge Scope",
            "",
            "## Цели" if locale == "ru" else "## Goals",
            goals,
            "",
            "## Не-цели" if locale == "ru" else "## Non-Goals",
            non_goals,
            "",
            "## Черновик объема" if locale == "ru" else "## Scope Draft",
            scope,
            "",
            "## Первая рекомендация" if locale == "ru" else "## First Step Recommendation",
            pack.first_step_recommendation,
        ]
    )


def render_constraints_markdown(pack: DeliveryPack) -> str:
    """Render structured constraints."""

    locale = detect_language(pack.brief.normalized_text)
    audience_hint = display_audience_mode(pack.constraints.audience_hint, locale) or (
        "Не указан" if locale == "ru" else "Unspecified"
    )
    platform_hints = display_platform_hints(pack.constraints.platform_hints, locale)
    team_size = display_team_size(pack.constraints.team_size, locale) or team_size_fallback(locale)
    tradeoffs = display_tradeoffs(pack.constraints.speed_quality_budget_tradeoffs, locale)
    return "\n".join(
        [
            "# SpecForge: Ограничения" if locale == "ru" else "# SpecForge Constraints",
            "",
            f"- {'Бюджет' if locale == 'ru' else 'Budget'}: "
            f"{pack.constraints.budget or ('Не указан' if locale == 'ru' else 'Unspecified')}",
            f"- {'Сроки' if locale == 'ru' else 'Timeline'}: "
            f"{pack.constraints.timeline or ('Не указаны' if locale == 'ru' else 'Unspecified')}",
            f"- {'Команда' if locale == 'ru' else 'Team Size'}: {team_size}",
            f"- {'Сигнал по аудитории' if locale == 'ru' else 'Audience Hint'}: "
            f"{audience_hint}",
            f"- {'Платформенные сигналы' if locale == 'ru' else 'Platform Hints'}: "
            + (
                ", ".join(platform_hints)
                if platform_hints
                else ("Не выделены" if locale == "ru" else "None extracted")
            ),
            f"- {'Компромиссы' if locale == 'ru' else 'Tradeoffs'}: "
            + (
                ", ".join(tradeoffs)
                if tradeoffs
                else ("Не выделены" if locale == "ru" else "None extracted")
            ),
            "",
            "## Явные ограничения" if locale == "ru" else "## Explicit Constraints",
            render_bullets(
                pack.constraints.explicit_constraints,
                fallback="- Ничего не выделено" if locale == "ru" else "- None extracted",
            ),
        ]
    )


def render_open_questions_markdown(pack: DeliveryPack) -> str:
    """Render prioritized open questions."""

    locale = detect_language(pack.brief.normalized_text)
    return "\n".join(
        [
            "# SpecForge: Открытые вопросы" if locale == "ru" else "# SpecForge Open Questions",
            "",
            render_bullets(
                pack.open_questions,
                fallback="- Открытые вопросы не были сгенерированы"
                if locale == "ru"
                else "- No open questions were generated",
            ),
        ]
    )


def render_assumptions_markdown(pack: DeliveryPack) -> str:
    """Render a short assumptions summary for compatibility with Stage 1 outputs."""

    locale = detect_language(pack.brief.normalized_text)
    return "\n".join(
        [
            "# SpecForge: Допущения" if locale == "ru" else "# SpecForge Assumptions",
            "",
            render_assumption_lines(pack.assumptions)
            or (
                "- Детерминированные допущения не были добавлены"
                if locale == "ru"
                else "- No deterministic assumptions were added"
            ),
        ]
    )


def render_assumption_ledger_markdown(pack: DeliveryPack) -> str:
    """Render the richer assumption ledger."""

    locale = detect_language(pack.brief.normalized_text)
    if not pack.assumptions:
        body = (
            "- Детерминированные допущения не были добавлены"
            if locale == "ru"
            else "- No deterministic assumptions were added"
        )
    else:
        sections = []
        for item in pack.assumptions:
            sections.extend(render_assumption_block(item))
        body = "\n".join(sections)
    header = "# SpecForge: Реестр допущений" if locale == "ru" else "# SpecForge Assumption Ledger"
    return "\n".join([header, "", body])


def render_analysis_report_markdown(pack: DeliveryPack) -> str:
    """Render the structured analysis report."""

    report = pack.analysis
    locale = detect_language(pack.brief.normalized_text)
    count_labels = localized_count_labels(locale)
    return "\n".join(
        [
            "# SpecForge: Аналитический отчет" if locale == "ru" else "# SpecForge Analysis Report",
            "",
            "## Счетчики" if locale == "ru" else "## Counts",
            *(
                f"- {count_labels.get(key, key)}: {value}"
                for key, value in pack.analysis_counts.items()
            ),
            "",
            "## Неясности" if locale == "ru" else "## Ambiguities",
            render_analysis_lines(
                report.ambiguities,
                locale=locale,
                fallback="- Неясности не обнаружены"
                if locale == "ru"
                else "- No ambiguity findings",
            ),
            "",
            "## Противоречия" if locale == "ru" else "## Contradictions",
            render_analysis_lines(
                report.contradictions,
                locale=locale,
                fallback="- Противоречия не обнаружены"
                if locale == "ru"
                else "- No contradiction findings",
            ),
            "",
            "## Недостающие решения" if locale == "ru" else "## Missing Decisions",
            render_analysis_lines(
                report.missing_decisions,
                locale=locale,
                fallback="- Недостающие решения не обнаружены"
                if locale == "ru"
                else "- No missing decisions",
            ),
            "",
            "## Приоритетные открытые вопросы"
            if locale == "ru"
            else "## Prioritized Open Questions",
            render_bullets(
                report.prioritized_open_questions,
                fallback="- Открытых вопросов нет" if locale == "ru" else "- No open questions",
            ),
        ]
    )


def team_size_fallback(locale: str) -> str:
    """Return a short localized fallback for missing team size."""

    return "Не указана" if locale == "ru" else "Unspecified"


def render_mvp_cut_plan_markdown(pack: DeliveryPack) -> str:
    """Render the recommended MVP cut plan."""

    locale = detect_language(pack.brief.normalized_text)
    cut = render_bullets(
        pack.recommended_mvp_cut,
        fallback="- Рекомендация по MVP не была сгенерирована"
        if locale == "ru"
        else "- No MVP cut recommendation was generated",
    )
    risky = render_bullets(
        pack.why_this_is_risky,
        fallback="- Существенные риски не были сгенерированы"
        if locale == "ru"
        else "- No major risks were generated",
    )
    return "\n".join(
        [
            "# SpecForge: План MVP" if locale == "ru" else "# SpecForge MVP Cut Plan",
            "",
            "## Рекомендуемый MVP" if locale == "ru" else "## Recommended MVP Cut",
            cut,
            "",
            "## Почему это рискованно" if locale == "ru" else "## Why This Is Risky",
            risky,
        ]
    )


def render_risk_register_markdown(pack: DeliveryPack) -> str:
    """Render the seeded risk register."""

    locale = detect_language(pack.brief.normalized_text)
    return "\n".join(
        [
            "# SpecForge: Реестр рисков" if locale == "ru" else "# SpecForge Risk Register",
            "",
            render_bullets(
                pack.risk_register,
                fallback="- Детерминированные риски не были добавлены"
                if locale == "ru"
                else "- No deterministic risks were seeded",
            ),
        ]
    )


def render_analysis_lines(items: list[object], *, locale: str, fallback: str) -> str:
    """Render finding objects with evidence and recommendations."""

    if not items:
        return fallback
    lines: list[str] = []
    for item in items:
        lines.append(
            f"- [{item.severity}] {category_label(item.category, locale)}: {item.description} "
            f"({'рекомендация' if locale == 'ru' else 'recommendation'}: {item.recommendation})"
        )
        if getattr(item, "evidence", None):
            evidence = "; ".join(getattr(item, "evidence")[:3])
            lines.append(f"  {'Доказательства' if locale == 'ru' else 'Evidence'}: {evidence}")
    return "\n".join(lines)


def render_assumption_lines(items: list[AssumptionItem]) -> str:
    """Render assumption items as one-line bullets."""

    locale = detect_language(items[0].statement) if items else "en"
    return "\n".join(
        f"- {item.statement} ({item.confidence}; "
        f"{'обоснование' if locale == 'ru' else 'rationale'}: {item.rationale})"
        for item in items
    )


def render_assumption_block(item: AssumptionItem) -> list[str]:
    """Render one assumption as a short block."""

    locale = detect_language(item.statement)
    lines = [
        f"- [{item.confidence}] {category_label(item.category, locale)}: {item.statement}",
        f"  {'Описание' if locale == 'ru' else 'Description'}: {item.description}",
        f"  {'Обоснование' if locale == 'ru' else 'Rationale'}: {item.rationale}",
        f"  {'Рекомендация' if locale == 'ru' else 'Recommendation'}: {item.recommendation}",
    ]
    if item.evidence:
        lines.append(
            f"  {'Доказательства' if locale == 'ru' else 'Evidence'}: "
            f"{'; '.join(item.evidence[:3])}"
        )
    return lines


def render_bullets(values: list[str], *, fallback: str) -> str:
    """Render a list of values as bullet lines."""

    if not values:
        return fallback
    return "\n".join(f"- {value}" for value in values)


def localized_count_labels(locale: str) -> dict[str, str]:
    """Return localized labels for public analysis counts."""

    if locale == "ru":
        return {
            "ambiguities": "Неясности",
            "contradictions": "Противоречия",
            "missing_decisions": "Недостающие решения",
            "assumptions": "Допущения",
            "open_questions": "Открытые вопросы",
        }
    return {
        "ambiguities": "Ambiguities",
        "contradictions": "Contradictions",
        "missing_decisions": "Missing decisions",
        "assumptions": "Assumptions",
        "open_questions": "Open questions",
    }
