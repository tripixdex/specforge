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
from specforge.pipeline.language import detect_language


def infer_contradictions(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
) -> list[ContradictionFinding]:
    """Detect conflicting planning signals."""

    findings: list[ContradictionFinding] = []
    lowered = brief.normalized_text.lower()
    locale = detect_language(brief.normalized_text)
    broad_scope = has_broad_scope_signal(brief)
    enterprise_scope = has_enterprise_scope_signal(lowered)
    budget_text = (constraints.budget or "").lower()
    low_budget = any(
        word in budget_text or word in lowered
        for word in [
            "budget",
            "cheap",
            "below $",
            "under $",
            "бюджет",
            "дешево",
            "недорого",
            "lean",
            "bootstrap",
        ]
    )
    timeline_text = (constraints.timeline or "").lower()
    short_timeline = any(
        word in timeline_text or word in lowered
        for word in [
            "asap",
            "day",
            "week",
            "weeks",
            "срочно",
            "дн",
            "недел",
            "quickly",
            "fast",
            "быстро",
        ]
    )
    overloaded_integrations = any(
        word in lowered
        for word in [
            "integrations",
            "integration",
            "slack",
            "stripe",
            "crm",
            "erp",
            "calendar",
            "email",
            "интеграц",
            "slack",
            "stripe",
            "crm",
            "erp",
            "календар",
            "почт",
        ]
    )
    simple_mvp = any(
        word in lowered
        for word in [
            "mvp",
            "minimal",
            "prototype",
            "simple mvp",
            "простой mvp",
            "минимальн",
            "прототип",
        ]
    )
    multi_platform = len(constraints.platform_hints) > 1 or any(
        word in lowered
        for word in [
            "web and mobile",
            "mobile and web",
            "ios and android",
            "веб и мобильн",
            "ios и android",
        ]
    )
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
                    "Бриф одновременно просит быстро, дешево и с широким набором функций."
                    if locale == "ru"
                    else "The brief asks for speed and low cost while also implying a "
                    "broad feature surface."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    [
                        "speed",
                        "budget",
                        "dashboard",
                        "all-in-one",
                        "multiple workflows",
                        "быстро",
                        "бюджет",
                        "все в одном",
                        "интеграц",
                    ],
                ),
                recommendation=(
                    "Сведите первую версию к одному основному workflow "
                    "и отложите вторичные зоны функционала."
                    if locale == "ru"
                    else "Cut the first release to one primary workflow and defer "
                    "secondary feature areas."
                ),
                source_type="inferred",
            )
        )
    if simple_mvp and enterprise_scope:
        findings.append(
            ContradictionFinding(
                category="minimal-mvp-vs-enterprise-scope",
                severity="high",
                description=(
                    "Бриф называет решение минимальным MVP, "
                    "но одновременно требует enterprise-объем."
                    if locale == "ru"
                    else "The brief describes a minimal MVP while also requesting "
                    "enterprise-grade scope."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    [
                        "mvp",
                        "minimal",
                        "enterprise",
                        "sso",
                        "audit",
                        "compliance",
                        "минимальн",
                        "аудит",
                        "комплаенс",
                    ],
                ),
                recommendation=(
                    "Уберите enterprise-требования из первого этапа "
                    "или перестаньте называть его минимальным."
                    if locale == "ru"
                    else "Remove enterprise requirements from the first milestone or "
                    "stop calling it minimal."
                ),
                source_type="explicit",
            )
        )
    if (
        short_timeline
        and infer_team_size_count(constraints.team_size) <= 2
        and (broad_scope or multi_platform)
    ):
        findings.append(
            ContradictionFinding(
                category="small-team-aggressive-deadline-broad-scope",
                severity="high",
                description=(
                    "Маленькая команда, короткий срок и широкий объем плохо сочетаются."
                    if locale == "ru"
                    else "A small team, aggressive deadline, and broad scope are in tension."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    [
                        constraints.timeline or "",
                        constraints.team_size or "",
                        "goals",
                        "platform",
                        "команда",
                        "срок",
                        "мобиль",
                    ],
                ),
                recommendation=(
                    "Сузьте первую поставку до одного ядра продукта до фиксации дедлайна."
                    if locale == "ru"
                    else "Reduce scope to a narrower MVP cut before committing to the deadline."
                ),
                source_type="inferred",
            )
        )
    if low_budget and short_timeline and (overloaded_integrations or broad_scope):
        findings.append(
            ContradictionFinding(
                category="fast-cheap-feature-rich",
                severity="high",
                description=(
                    "Низкий бюджет, короткий срок и насыщенный набор "
                    "функций создают явное противоречие."
                    if locale == "ru"
                    else "Low budget, short timeline, and a broad feature set "
                    "create an obvious delivery contradiction."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    [
                        constraints.budget or "",
                        constraints.timeline or "",
                        "integrations",
                        "analytics",
                        "billing",
                        "интеграц",
                        "аналитик",
                        "биллинг",
                    ],
                ),
                recommendation=(
                    "Оставьте в первом релизе один основной сценарий "
                    "и минимальный набор интеграций."
                    if locale == "ru"
                    else "Keep the first release to one core workflow "
                    "and a minimal integration set."
                ),
                source_type="inferred",
            )
        )
    if simple_mvp and (enterprise_scope or overloaded_integrations or multi_platform):
        findings.append(
            ContradictionFinding(
                category="minimal-mvp-vs-enterprise-scope",
                severity="high",
                description=(
                    "Формулировка про простой MVP конфликтует с "
                    "enterprise-объемом, множеством интеграций "
                    "или мультиплатформенностью."
                    if locale == "ru"
                    else "The brief calls this a simple MVP while also asking "
                    "for enterprise breadth, many integrations, "
                    "or multi-platform support."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    [
                        "mvp",
                        "simple",
                        "enterprise",
                        "integrations",
                        "web",
                        "mobile",
                        "простой",
                        "интеграц",
                        "мобиль",
                    ],
                ),
                recommendation=(
                    "Оставьте у MVP один канал, одну роль и минимальный "
                    "набор обязательных функций."
                    if locale == "ru"
                    else "Keep the MVP to one channel, one role, "
                    "and the minimum mandatory capability set."
                ),
                source_type="explicit",
            )
        )
    return dedupe_contradictions(findings)


def infer_missing_decisions(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
) -> list[MissingDecision]:
    """Collect planning decisions that should be made before deeper generation."""

    decisions: list[MissingDecision] = []
    lowered = brief.normalized_text.lower()
    locale = detect_language(brief.normalized_text)
    if not brief.audience:
        decisions.append(
            MissingDecision(
                category="target_user",
                severity="high",
                description=(
                    "Решение о целевом пользователе все еще не принято."
                    if locale == "ru"
                    else "The target user decision is still unresolved."
                ),
                evidence=[brief.summary],
                recommendation=(
                    "Выберите одного основного пользователя до детализации требований."
                    if locale == "ru"
                    else "Choose a single primary user before expanding detailed requirements."
                ),
                source_type="unresolved",
            )
        )
    if not constraints.platform_hints:
        decisions.append(
            MissingDecision(
                category="platform",
                severity="high",
                description=(
                    "Решение о первой платформе не принято."
                    if locale == "ru"
                    else "The first platform decision is not made."
                ),
                evidence=[brief.summary],
                recommendation=(
                    "Выберите одну стартовую платформу, а остальные зафиксируйте как отложенные."
                    if locale == "ru"
                    else "Choose one initial platform and treat others as deferred."
                ),
                source_type="unresolved",
            )
        )
    if constraints.audience_hint in {"b2b", "b2c"} and not has_monetization_signal(brief):
        decisions.append(
            MissingDecision(
                category="pricing",
                severity="medium",
                description=(
                    "В брифе не указано, отложено ли ценообразование "
                    "и какое направление по цене предполагается."
                    if locale == "ru"
                    else "The brief does not say whether pricing is deferred or what "
                    "pricing direction exists."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    ["b2b", "b2c", "client", "customer", "клиент", "пользоват"],
                )[:2],
                recommendation=(
                    "Определите, входит ли цена в текущий объем, "
                    "осознанно отложена или уже задана бизнес-моделью."
                    if locale == "ru"
                    else "Decide whether pricing is part of scope, intentionally "
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
                    "Бриф намекает на чувствительные данные или "
                    "enterprise-сценарий, но решения по безопасности "
                    "остаются открытыми."
                    if locale == "ru"
                    else "The brief implies sensitive or enterprise usage but leaves "
                    "security and compliance decisions open."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    [
                        "enterprise",
                        "patient",
                        "financial",
                        "customer data",
                        "compliance",
                        "персональн",
                        "финансов",
                        "комплаенс",
                    ],
                )[:3],
                recommendation=(
                    "Определите минимальную планку по безопасности "
                    "и комплаенсу до фиксации enterprise- или "
                    "data-sensitive объема."
                    if locale == "ru"
                    else "Decide the minimum security/compliance bar before committing "
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
                    "Бриф не определяет, кто будет владеть и поддерживать "
                    "внутренний workflow после запуска."
                    if locale == "ru"
                    else "The brief does not identify who owns or operates the internal "
                    "workflow after launch."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    ["internal", "ops team", "operations team", "внутрен", "операцион"],
                )[:2],
                recommendation=(
                    "Назначьте владельца процесса, админ-задач и операционного сопровождения."
                    if locale == "ru"
                    else "Assign an owner for the workflow, admin tasks, and operational upkeep."
                ),
                source_type="unresolved",
            )
        )
    return decisions


def dedupe_contradictions(items: list[ContradictionFinding]) -> list[ContradictionFinding]:
    """Deduplicate contradiction findings by category and description."""

    seen: set[tuple[str, str]] = set()
    unique: list[ContradictionFinding] = []
    for item in items:
        key = (item.category, item.description)
        if key not in seen:
            seen.add(key)
            unique.append(item)
    return unique
