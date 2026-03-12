"""Deterministic contradiction rules tuned for overloaded briefs."""

from __future__ import annotations

from specforge.domain.models import ConstraintSet, ContradictionFinding, NormalizedBrief
from specforge.pipeline.analysis_signals import (
    collect_contradiction_evidence,
    count_integration_signals,
    has_broad_scope_signal,
    has_enterprise_scope_signal,
    has_low_budget_signal,
    has_short_timeline_signal,
    infer_team_size_count,
)
from specforge.pipeline.intake import dedupe
from specforge.pipeline.language import detect_language


def infer_contradictions(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
) -> list[ContradictionFinding]:
    """Detect conflicting planning signals without spamming duplicate findings."""

    lowered = brief.normalized_text.lower()
    locale = detect_language(brief.normalized_text)
    broad_scope = has_broad_scope_signal(brief)
    enterprise_scope = has_enterprise_scope_signal(lowered)
    low_budget = has_low_budget_signal(brief.normalized_text, constraints.budget)
    short_timeline = has_short_timeline_signal(brief.normalized_text, constraints.timeline)
    team_size = infer_team_size_count(constraints.team_size)
    integration_count = count_integration_signals(lowered)
    overloaded_integrations = integration_count >= 2
    tiny_team = team_size <= 2
    multi_platform = len(constraints.platform_hints) > 1 or any(
        phrase in lowered
        for phrase in [
            "web and mobile",
            "mobile and web",
            "ios and android",
            "desktop and mobile",
            "веб и мобиль",
            "мобильное и веб",
            "ios и android",
        ]
    )
    simple_mvp = any(
        word in lowered
        for word in [
            "mvp",
            "minimal",
            "prototype",
            "simple mvp",
            "simple prototype",
            "простой mvp",
            "минимальн",
            "прототип",
            "простое приложение",
        ]
    )
    overloaded_scope = broad_scope or enterprise_scope or overloaded_integrations or multi_platform

    findings: list[ContradictionFinding] = []
    if low_budget and short_timeline and overloaded_scope:
        findings.append(
            ContradictionFinding(
                category="fast-cheap-feature-rich",
                severity="high",
                description=(
                    "Низкий бюджет, короткий срок и перегруженный первый релиз "
                    "создают явный конфликт."
                    if locale == "ru"
                    else "Low budget, short timeline, and an overloaded first release "
                    "create an obvious delivery conflict."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    [
                        constraints.budget or "",
                        constraints.timeline or "",
                        "cheap",
                        "budget",
                        "integrations",
                        "analytics",
                        "billing",
                        "web",
                        "mobile",
                        "дешево",
                        "бюджет",
                        "интеграц",
                        "аналитик",
                        "биллинг",
                        "веб",
                        "мобиль",
                    ],
                ),
                recommendation=(
                    "Оставьте в первом релизе один основной сценарий "
                    "и только обязательные интеграции."
                    if locale == "ru"
                    else "Keep the first release to one core workflow "
                    "and only the mandatory integrations."
                ),
                source_type="inferred",
            )
        )
    elif (
        "speed prioritized" in constraints.speed_quality_budget_tradeoffs
        and "budget prioritized" in constraints.speed_quality_budget_tradeoffs
        and overloaded_scope
    ):
        findings.append(
            ContradictionFinding(
                category="fast-cheap-feature-rich",
                severity="high",
                description=(
                    "Бриф одновременно просит быстро, дешево и с широким набором функций."
                    if locale == "ru"
                    else "The brief asks for speed and low cost while also "
                    "implying a broad first-release scope."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    [
                        "speed",
                        "fast",
                        "budget",
                        "cheap",
                        "integrations",
                        "dashboard",
                        "analytics",
                        "быстро",
                        "бюджет",
                        "дешево",
                        "интеграц",
                        "аналитик",
                    ],
                ),
                recommendation=(
                    "Сведите первый этап к одному workflow и отложите вторичные зоны функционала."
                    if locale == "ru"
                    else "Cut the first milestone to one workflow and defer "
                    "secondary feature areas."
                ),
                source_type="inferred",
            )
        )

    if short_timeline and tiny_team and overloaded_scope:
        findings.append(
            ContradictionFinding(
                category="small-team-aggressive-deadline-broad-scope",
                severity="high",
                description=(
                    "Маленькая команда, короткий срок и перегруженный объем плохо сочетаются."
                    if locale == "ru"
                    else "A small team, aggressive deadline, and overloaded scope are in tension."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    [
                        constraints.timeline or "",
                        constraints.team_size or "",
                        "web",
                        "mobile",
                        "integrations",
                        "admin",
                        "enterprise",
                        "команда",
                        "срок",
                        "веб",
                        "мобиль",
                        "интеграц",
                    ],
                ),
                recommendation=(
                    "Сузьте первую поставку до одного канала "
                    "и одного ключевого сценария до фиксации дедлайна."
                    if locale == "ru"
                    else "Reduce the first release to one channel and one key workflow "
                    "before committing to the deadline."
                ),
                source_type="inferred",
            )
        )

    if simple_mvp and overloaded_scope:
        findings.append(
            ContradictionFinding(
                category="minimal-mvp-vs-enterprise-scope",
                severity="high",
                description=(
                    "Формулировка про простой MVP конфликтует с enterprise-объемом, "
                    "множеством интеграций или мультиплатформенностью."
                    if locale == "ru"
                    else "The brief calls this a simple MVP while also asking "
                    "for enterprise breadth, many integrations, or multi-platform support."
                ),
                evidence=collect_contradiction_evidence(
                    brief,
                    [
                        "mvp",
                        "minimal",
                        "prototype",
                        "enterprise",
                        "sso",
                        "audit",
                        "integrations",
                        "web",
                        "mobile",
                        "минимальн",
                        "простой",
                        "аудит",
                        "интеграц",
                        "веб",
                        "мобиль",
                    ],
                ),
                recommendation=(
                    "Оставьте у MVP один канал, одну роль и минимальный набор обязательных функций."
                    if locale == "ru"
                    else "Keep the MVP to one channel, one user role, "
                    "and the minimum mandatory capability set."
                ),
                source_type="explicit",
            )
        )

    return curate_contradictions(findings)


def curate_contradictions(items: list[ContradictionFinding]) -> list[ContradictionFinding]:
    """Merge duplicate contradiction families into one cleaner finding per category."""

    curated: dict[str, ContradictionFinding] = {}
    for item in items:
        existing = curated.get(item.category)
        if existing is None:
            curated[item.category] = item
            continue
        merged_evidence = dedupe(existing.evidence + item.evidence)[:4]
        curated[item.category] = existing.model_copy(
            update={
                "severity": (
                    "high"
                    if "high" in {existing.severity, item.severity}
                    else existing.severity
                ),
                "source_type": "explicit"
                if "explicit" in {existing.source_type, item.source_type}
                else existing.source_type,
                "evidence": merged_evidence,
            }
        )
    ordered_categories = [
        "fast-cheap-feature-rich",
        "small-team-aggressive-deadline-broad-scope",
        "minimal-mvp-vs-enterprise-scope",
    ]
    return [curated[category] for category in ordered_categories if category in curated]
