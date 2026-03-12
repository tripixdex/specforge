"""Deterministic ambiguity rules."""

from __future__ import annotations

from specforge.domain.models import AmbiguityFinding, ConstraintSet, NormalizedBrief
from specforge.pipeline.analysis_signals import (
    contains_vague_goals,
    find_evidence,
    has_monetization_signal,
    has_success_signal,
)
from specforge.pipeline.language import detect_language


def infer_ambiguities(brief: NormalizedBrief, constraints: ConstraintSet) -> list[AmbiguityFinding]:
    """Collect ambiguous or underspecified planning signals."""

    findings: list[AmbiguityFinding] = []
    locale = detect_language(brief.normalized_text)
    if not brief.audience:
        findings.append(
            AmbiguityFinding(
                category="audience",
                severity="high",
                description=(
                    "Основной пользователь или покупатель не определен."
                    if locale == "ru"
                    else "The primary user or buyer is not clearly identified."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    ["user", "customer", "client", "team", "пользоват", "клиент", "команд"],
                )[:2],
                recommendation=(
                    "Назовите одного основного пользователя или покупателя для первой версии."
                    if locale == "ru"
                    else "Name one primary user or buyer for the first release."
                ),
                source_type="unresolved",
                question=(
                    "Кто является основным пользователем или покупателем первой версии?"
                    if locale == "ru"
                    else "Who is the primary user or buyer for the first release?"
                ),
            )
        )
    if not constraints.platform_hints:
        findings.append(
            AmbiguityFinding(
                category="platform",
                severity="high",
                description=(
                    "В брифе не указана первая целевая платформа."
                    if locale == "ru"
                    else "The brief does not make the first platform explicit."
                ),
                evidence=[brief.summary],
                recommendation=(
                    "Выберите первую платформу до расширения объема."
                    if locale == "ru"
                    else "Choose a first platform before expanding the scope narrative."
                ),
                source_type="unresolved",
                question=(
                    "Какая платформа важнее первой: веб, мобильная, десктоп, CLI, API "
                    "или внутренний рабочий инструмент?"
                    if locale == "ru"
                    else "What platform matters first: web, mobile, desktop, CLI, API, "
                    "or internal workflow tooling?"
                ),
            )
        )
    if not brief.goals or contains_vague_goals(brief.goals):
        findings.append(
            AmbiguityFinding(
                category="goals",
                severity="high" if not brief.goals else "medium",
                description=(
                    "Цели отсутствуют или сформулированы слишком расплывчато."
                    if locale == "ru"
                    else "The goals are missing or too vague to anchor scope cleanly."
                ),
                evidence=brief.goals[:2] or [brief.summary],
                recommendation=(
                    "Переформулируйте цели как конкретные результаты, а не общие пожелания."
                    if locale == "ru"
                    else "Rewrite the goals as concrete outcomes, not general aspirations."
                ),
                source_type="unresolved" if not brief.goals else "inferred",
                question=(
                    "Какие один-три конкретных результата будут означать успех?"
                    if locale == "ru"
                    else "What are the one to three concrete outcomes that define success?"
                ),
            )
        )
    if not has_success_signal(brief):
        findings.append(
            AmbiguityFinding(
                category="success_criteria",
                severity="medium",
                description=(
                    "Явные критерии успеха или измеримый сигнал завершения не найдены."
                    if locale == "ru"
                    else "No explicit success criteria, metric, or concrete completion "
                    "signal was found."
                ),
                evidence=brief.goals[:2] or [brief.summary],
                recommendation=(
                    "Добавьте хотя бы один измеримый или бинарный "
                    "критерий успеха для первой версии."
                    if locale == "ru"
                    else "Add one measurable or binary success check for the first release."
                ),
                source_type="unresolved",
                question=(
                    "Как команда поймет, что первая версия успешна?"
                    if locale == "ru"
                    else "How will the team know the first release is successful?"
                ),
            )
        )
    if not has_monetization_signal(brief) and constraints.audience_hint in {"b2b", "b2c"}:
        findings.append(
            AmbiguityFinding(
                category="monetization",
                severity="medium",
                description=(
                    "Бриф описывает внешний продукт, но не дает направления по монетизации."
                    if locale == "ru"
                    else "The brief describes an external product but gives no pricing "
                    "or monetization direction."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    ["client", "customer", "b2b", "b2c", "клиент", "пользоват"],
                )[:2],
                recommendation=(
                    "Укажите, будет ли монетизация подписочной, usage-based, "
                    "внутренним cost center или осознанно отложенной."
                    if locale == "ru"
                    else "State whether pricing is subscription, usage-based, internal "
                    "cost center, or deferred."
                ),
                source_type="unresolved",
                question=(
                    "Как продукт должен зарабатывать деньги, "
                    "или решение по цене осознанно отложено?"
                    if locale == "ru"
                    else "How is the product expected to make money, or is pricing "
                    "intentionally deferred?"
                ),
            )
        )
    if not constraints.budget:
        findings.append(
            AmbiguityFinding(
                category="budget",
                severity="medium",
                description=(
                    "Не найден ориентир по бюджету или лимиту расходов."
                    if locale == "ru"
                    else "No budget range or spend ceiling was found."
                ),
                evidence=[brief.summary],
                recommendation=(
                    "Добавьте хотя бы грубый лимит бюджета, чтобы держать объем реалистичным."
                    if locale == "ru"
                    else "Add a rough budget ceiling to keep scope realistic."
                ),
                source_type="unresolved",
                question=(
                    "Какой бюджет ограничивает эту работу?"
                    if locale == "ru"
                    else "What budget range constrains this work?"
                ),
            )
        )
    if not constraints.timeline:
        findings.append(
            AmbiguityFinding(
                category="timeline",
                severity="medium",
                description=(
                    "Не найдено ограничение по срокам поставки."
                    if locale == "ru"
                    else "No delivery timing constraint was found."
                ),
                evidence=[brief.summary],
                recommendation=(
                    "Укажите дату или timebox, под который должен оптимизироваться MVP."
                    if locale == "ru"
                    else "State the date or timebox the MVP should optimize for."
                ),
                source_type="unresolved",
                question=(
                    "На какой срок или дедлайн должно ориентироваться планирование?"
                    if locale == "ru"
                    else "What timeline or deadline should delivery planning optimize for?"
                ),
            )
        )
    return findings
