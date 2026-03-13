"""Higher-level outputs derived from deterministic analysis findings."""

from __future__ import annotations

from specforge.domain.models import (
    AmbiguityFinding,
    ConstraintSet,
    ContradictionFinding,
    MissingDecision,
    NormalizedBrief,
    TraceabilityLink,
)
from specforge.pipeline.analysis_signals import infer_team_size_count, sort_by_severity
from specforge.pipeline.intake import dedupe
from specforge.pipeline.language import detect_language, display_platform_hints


def prioritize_open_questions(
    ambiguities: list[AmbiguityFinding],
    contradictions: list[ContradictionFinding],
    missing_decisions: list[MissingDecision],
) -> list[str]:
    """Create a prioritized open-question list from findings."""

    locale = "en"
    if ambiguities:
        locale = detect_language(ambiguities[0].description)
    elif missing_decisions:
        locale = detect_language(missing_decisions[0].description)
    elif contradictions:
        locale = detect_language(contradictions[0].description)
    questions = [item.question for item in sort_by_severity(ambiguities)]
    for decision in sort_by_severity(missing_decisions):
        prefix = "Нужно решение" if locale == "ru" else "Decision needed"
        questions.append(f"{prefix}: {decision.description}")
    for contradiction in sort_by_severity(contradictions):
        prefix = "Разрешить противоречие" if locale == "ru" else "Resolve contradiction"
        questions.append(f"{prefix}: {contradiction.description}")
    return dedupe(questions)


def infer_mvp_cut(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
    contradictions: list[ContradictionFinding],
    missing_decisions: list[MissingDecision],
) -> list[str]:
    """Recommend a narrower MVP cut from deterministic signals."""

    locale = detect_language(brief.normalized_text)
    cut = []
    if brief.goals:
        cut.append(
            f"Сфокусируйте первую версию на этой главной цели: {brief.goals[0]}"
            if locale == "ru"
            else f"Anchor the first release on this primary goal: {brief.goals[0]}"
        )
    if not brief.audience:
        cut.append(
            "Сначала выберите одного основного пользователя и один главный сценарий."
            if locale == "ru"
            else "Decide on one primary user and one core workflow before expanding scope."
        )
    if len(brief.goals) > 1:
        cut.append(
            "Отложите вторичные цели, пока не подтвержден первый основной сценарий."
            if locale == "ru"
            else "Defer secondary goals until the first workflow is validated."
        )
    if len(constraints.platform_hints) > 1:
        platforms = ", ".join(display_platform_hints(constraints.platform_hints, locale))
        cut.append(
            f"Выберите одну основную платформу вместо распыления между: {platforms}."
            if locale == "ru"
            else f"Choose one primary platform instead of splitting across: {platforms}."
        )
    if any(item.category == "pricing" for item in missing_decisions):
        cut.append(
            "Оставьте цену отдельным следующим решением, "
            "если монетизация не является ядром первого сценария."
            if locale == "ru"
            else "Treat pricing as a follow-up decision unless monetization is core "
            "to the first workflow."
        )
    if any(item.category == "minimal-mvp-vs-enterprise-scope" for item in contradictions):
        cut.append(
            "Уберите из MVP корпоративные требования вроде SSO, аудита и тяжелого комплаенса."
            if locale == "ru"
            else "Remove enterprise-only requirements such as SSO, audit trails, or "
            "compliance-heavy scope from MVP."
        )
        cut.append(
            "Отложите вторичные интеграции, отчетность "
            "и административные поверхности до следующего этапа."
            if locale == "ru"
            else "Defer secondary integrations, reporting surfaces, "
            "and admin-heavy controls to a later milestone."
        )
    if any(
        item.category == "small-team-aggressive-deadline-broad-scope" for item in contradictions
    ):
        cut.append(
            "Сведите релиз к одной роли и одному ключевому сценарию "
            "до сохранения заявленного срока."
            if locale == "ru"
            else "Cut the release to one role and one core workflow before keeping "
            "the stated deadline."
        )
    if not cut:
        cut.append(
            "Сфокусируйте первую версию на одном пользователе, "
            "одном основном сценарии и одном локальном цикле проверки."
            if locale == "ru"
            else "Keep the first release focused on one user, one workflow, and one "
            "local review loop."
        )
    return dedupe(cut)


def build_traceability_links(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
) -> list[TraceabilityLink]:
    """Create lightweight traceability links for key extracted signals."""

    links: list[TraceabilityLink] = []
    for goal in brief.goals[:3]:
        links.append(TraceabilityLink(source_excerpt=goal, target_section="scope.md"))
    for constraint in constraints.explicit_constraints[:3]:
        links.append(TraceabilityLink(source_excerpt=constraint, target_section="constraints.md"))
    return links


def infer_risks(
    brief: NormalizedBrief,
    constraints: ConstraintSet,
    contradictions: list[ContradictionFinding],
    missing_decisions: list[MissingDecision],
) -> list[str]:
    """Seed the risk register from analytical findings."""

    locale = detect_language(brief.normalized_text)
    risks = [item.description for item in contradictions]
    risks.extend(
        item.description for item in missing_decisions if item.severity in {"medium", "high"}
    )
    if constraints.timeline and infer_team_size_count(constraints.team_size) <= 1:
        risks.append(
            "Команда из одного человека вместе с явным сроком повышает риск срыва графика."
            if locale == "ru"
            else "A one-person team plus an explicit delivery timeline increases schedule risk."
        )
    if not brief.audience:
        risks.append(
            "Неясная аудитория ослабляет приоритизацию и критерии приемки."
            if locale == "ru"
            else "Unclear audience definition weakens prioritization and acceptance criteria."
        )
    return dedupe(risks)
