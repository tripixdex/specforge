"""Deterministic delivery-pack generation with Stage 2 analysis integration."""

from __future__ import annotations

from datetime import UTC, datetime

from specforge.domain.models import AnalysisReport, DeliveryPack, NormalizedBrief
from specforge.pipeline.intake import dedupe
from specforge.pipeline.language import (
    detect_language,
    display_audience,
    display_audience_mode,
    display_platform_hints,
    display_product_type,
)


def generate_delivery_pack(brief: NormalizedBrief) -> DeliveryPack:
    """Build a deterministic Stage 2 delivery-pack skeleton."""

    analysis = brief.analysis or AnalysisReport(assumptions=brief.assumptions)
    scope_draft = build_scope_draft(brief)
    first_step = build_first_step_recommendation(brief, analysis)
    explicit_user_input = build_explicit_user_input(brief)
    inferred_structure = build_inferred_structure(brief, analysis)
    why_risky = build_why_risky(analysis, brief.risks)

    return DeliveryPack(
        generated_at=datetime.now(UTC).isoformat(),
        brief=brief,
        analysis=analysis,
        brief_summary=build_brief_summary(brief),
        goals=brief.goals,
        non_goals=brief.non_goals,
        scope_draft=scope_draft,
        explicit_user_input=explicit_user_input,
        inferred_structure=inferred_structure,
        constraints=brief.constraints,
        open_questions=analysis.prioritized_open_questions or brief.open_questions,
        assumptions=analysis.assumptions or brief.assumptions,
        risk_register=dedupe(brief.risks),
        recommended_mvp_cut=analysis.recommended_mvp_cut,
        why_this_is_risky=why_risky,
        first_step_recommendation=first_step,
        analysis_counts=build_analysis_counts(analysis),
    )


def build_brief_summary(brief: NormalizedBrief) -> str:
    """Create a compact deterministic summary sentence."""

    locale = detect_language(brief.normalized_text)
    product = display_product_type(brief.product_type, locale) or "product concept"
    if locale == "ru":
        product = display_product_type(brief.product_type, locale) or "продуктовая идея"
        audience = (
            ", ".join(display_audience(brief.audience, locale))
            if brief.audience
            else "неуказанная аудитория"
        )
    else:
        audience = (
            ", ".join(display_audience(brief.audience, locale))
            if brief.audience
            else "an unspecified audience"
        )
    if brief.goals:
        if locale == "ru":
            return (
                f"{brief.title} — это {product} для аудитории: {audience}. "
                f"Главная цель: {brief.goals[0]}."
            )
        article = "an" if product[:1].lower() in {"a", "e", "i", "o", "u"} else "a"
        return (
            f"{brief.title} is {article} {product} aimed at {audience}. "
            f"Primary goal: {brief.goals[0]}."
        )
    if locale == "ru":
        return (
            f"{brief.title} — это {product} для аудитории: {audience}. "
            "Цели все еще нужно уточнить."
        )
    article = "an" if product[:1].lower() in {"a", "e", "i", "o", "u"} else "a"
    return (
        f"{brief.title} is {article} {product} aimed at {audience}. "
        "Goals still need clarification."
    )


def build_scope_draft(brief: NormalizedBrief) -> list[str]:
    """Assemble a small deterministic scope draft."""

    locale = detect_language(brief.normalized_text)
    items = []
    if brief.product_type:
        display_product = display_product_type(brief.product_type, locale) or brief.product_type
        items.append(
            f"Соберите первый контур решения вокруг формата {display_product}."
            if locale == "ru"
            else f"Shape the first scoped draft around a {display_product}."
        )
    if brief.audience:
        display_audiences = ", ".join(display_audience(brief.audience, locale))
        items.append(
            f"Ставьте в приоритет потребности аудитории: {display_audiences}."
            if locale == "ru"
            else f"Prioritize the needs of {display_audiences}."
        )
    if brief.goals:
        if locale == "ru":
            items.extend(f"Поддержать цель: {goal}." for goal in brief.goals[:3])
        else:
            items.extend(f"Support goal: {goal}." for goal in brief.goals[:3])
    if brief.non_goals:
        if locale == "ru":
            items.extend(f"Пока оставить вне объема: {item}." for item in brief.non_goals[:3])
        else:
            items.extend(f"Keep out of scope for now: {item}." for item in brief.non_goals[:3])
    if brief.constraints.platform_hints:
        platform_hints = ", ".join(
            display_platform_hints(brief.constraints.platform_hints[:4], locale)
        )
        if locale == "ru":
            items.append("Учитывать сигналы по платформе: " + platform_hints + ".")
        else:
            items.append("Respect platform hints: " + platform_hints + ".")
    return dedupe(items)


def build_explicit_user_input(brief: NormalizedBrief) -> list[str]:
    """Collect explicit source claims for display in the pack."""

    explicit = brief.goals[:3] + brief.non_goals[:3] + brief.constraints.explicit_constraints[:4]
    return dedupe(explicit)


def build_inferred_structure(
    brief: NormalizedBrief,
    analysis: AnalysisReport,
) -> list[str]:
    """Collect deterministic inferences for display in the pack."""

    locale = detect_language(brief.normalized_text)
    inferred = []
    if brief.product_type:
        display_product = display_product_type(brief.product_type, locale) or brief.product_type
        inferred.append(
            f"Предполагаемый тип продукта: {display_product}."
            if locale == "ru"
            else f"Inferred product type: {display_product}."
        )
    if brief.constraints.audience_hint:
        display_mode = display_audience_mode(brief.constraints.audience_hint, locale)
        inferred.append(
            f"Предполагаемый режим аудитории: {display_mode}."
            if locale == "ru"
            else f"Inferred audience mode: {display_mode}."
        )
    if brief.constraints.platform_hints:
        platform_hints = ", ".join(display_platform_hints(brief.constraints.platform_hints, locale))
        if locale == "ru":
            inferred.append("Предполагаемые платформенные сигналы: " + platform_hints + ".")
        else:
            inferred.append("Inferred platform hints: " + platform_hints + ".")
    if analysis.contradictions:
        if locale == "ru":
            inferred.append(
                "Обнаружена перегрузка требований в "
                f"{len(analysis.contradictions)} зоне(ах) планирования."
            )
        else:
            inferred.append(
                "Detected requirement overload across "
                f"{len(analysis.contradictions)} planning area(s)."
            )
    return dedupe(inferred)


def build_why_risky(analysis: AnalysisReport, existing_risks: list[str]) -> list[str]:
    """Explain risk in terms of contradictions and unresolved decisions."""

    risky = [item.description for item in analysis.contradictions]
    risky.extend(item.description for item in analysis.missing_decisions)
    risky.extend(existing_risks)
    return dedupe(risky)


def build_first_step_recommendation(
    brief: NormalizedBrief,
    analysis: AnalysisReport,
) -> str:
    """Recommend the next delivery action based on analysis."""

    locale = detect_language(brief.normalized_text)
    if analysis.prioritized_open_questions:
        if locale == "ru":
            return (
                "Сначала ответьте на главный открытый вопрос, а потом расширяйте объем: "
                f"{analysis.prioritized_open_questions[0]}"
            )
        return (
            "Resolve the top unresolved question before expanding scope: "
            f"{analysis.prioritized_open_questions[0]}"
        )
    if analysis.recommended_mvp_cut:
        return analysis.recommended_mvp_cut[0]
    if brief.goals:
        if locale == "ru":
            return (
                "Превратите нормализованные цели в чеклист первого этапа "
                "и вручную подтвердите первые критерии приемки."
            )
        return (
            "Turn the normalized goals into a milestone-1 checklist and confirm "
            "the first acceptance criteria manually."
        )
    if locale == "ru":
        return (
            "Сначала уточните целевого пользователя и желаемый результат, "
            "а потом переходите к детальному планированию."
        )
    return "Clarify the target user and desired outcome before attempting detailed planning."


def build_analysis_counts(analysis: AnalysisReport) -> dict[str, int]:
    """Return summary counts for the analysis layer."""

    return {
        "ambiguities": len(analysis.ambiguities),
        "contradictions": len(analysis.contradictions),
        "missing_decisions": len(analysis.missing_decisions),
        "assumptions": len(analysis.assumptions),
        "open_questions": len(analysis.prioritized_open_questions),
    }
