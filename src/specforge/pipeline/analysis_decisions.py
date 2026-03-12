"""Deterministic contradiction and missing-decision rules."""

from __future__ import annotations

from specforge.domain.models import (
    ConstraintSet,
    MissingDecision,
    NormalizedBrief,
)
from specforge.pipeline.analysis_signals import (
    find_evidence,
    has_monetization_signal,
    has_owner_signal,
    has_security_signal,
    requires_security_decision,
)
from specforge.pipeline.language import detect_language


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
