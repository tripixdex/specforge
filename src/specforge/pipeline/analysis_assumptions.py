"""Assumption-specific rules for deterministic analysis."""

from __future__ import annotations

from specforge.domain.models import AssumptionItem, ConstraintSet, NormalizedBrief
from specforge.pipeline.analysis_signals import find_evidence
from specforge.pipeline.language import detect_language


def infer_assumptions(brief: NormalizedBrief, constraints: ConstraintSet) -> list[AssumptionItem]:
    """Create narrow assumptions only where the brief strongly implies them."""

    assumptions: list[AssumptionItem] = []
    locale = detect_language(brief.normalized_text)
    if "local-first" in constraints.platform_hints:
        assumptions.append(
            AssumptionItem(
                category="deployment",
                severity="medium",
                statement=(
                    "Первая версия должна оставлять входы и выходы на локальной машине."
                    if locale == "ru"
                    else "The first release should keep inputs and outputs on the local machine."
                ),
                description=(
                    "Локальное выполнение рассматривается как жесткое допущение для MVP."
                    if locale == "ru"
                    else "Local execution is treated as a hard planning assumption for the MVP."
                ),
                rationale=(
                    "Бриф явно указывает на локальный режим работы."
                    if locale == "ru"
                    else "The brief explicitly references local-first operation."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    [
                        "local-first",
                        "local first",
                        "keep data local",
                        "offline",
                        "локальн",
                        "офлайн",
                    ],
                ),
                recommendation=(
                    "Не включайте хостинговую коллаборацию и удаленное хранилище в первую поставку."
                    if locale == "ru"
                    else "Keep hosted collaboration and remote storage out of the first scoped cut."
                ),
                source_type="explicit",
                confidence="high",
            )
        )
    if constraints.audience_hint == "internal":
        assumptions.append(
            AssumptionItem(
                category="audience",
                severity="medium",
                statement=(
                    "Первая версия должна оптимизироваться под внутренних "
                    "операторов, а не внешних self-serve пользователей."
                    if locale == "ru"
                    else "The first scope should optimize for internal operators rather "
                    "than external self-serve users."
                ),
                description=(
                    "Похоже, что основной контекст использования связан с внутренними операторами."
                    if locale == "ru"
                    else "Internal operator workflows appear to be the primary user context."
                ),
                rationale=(
                    "В брифе используется язык внутренних команд."
                    if locale == "ru"
                    else "The brief uses internal-team language."
                ),
                evidence=find_evidence(
                    brief.normalized_text,
                    [
                        "internal",
                        "operations team",
                        "ops team",
                        "support team",
                        "внутрен",
                        "операцион",
                        "поддержк",
                    ],
                ),
                recommendation=(
                    "Отложите внешние account-management сценарии, "
                    "пока не прояснен внутренний workflow."
                    if locale == "ru"
                    else "Defer external account-management flows until the internal "
                    "workflow is clear."
                ),
                source_type="inferred",
                confidence="medium",
            )
        )
    if not constraints.timeline and brief.goals:
        assumptions.append(
            AssumptionItem(
                category="delivery",
                severity="low",
                statement=(
                    "Планирование будет исходить из узкого первого этапа, "
                    "потому что явный срок не задан."
                    if locale == "ru"
                    else "Planning will default to a narrow first milestone because no "
                    "explicit timeline was given."
                ),
                description=(
                    "Сигнал по срокам не найден, поэтому ранний объем "
                    "должен оставаться консервативным."
                    if locale == "ru"
                    else "No timeline signal was found, so early scope should remain conservative."
                ),
                rationale=(
                    "Отсутствие контекста по срокам делает широкий объем рискованным."
                    if locale == "ru"
                    else "Missing timing context makes broad sequencing risky."
                ),
                evidence=[brief.goals[0]],
                recommendation=(
                    "Подтвердите ожидаемый дедлайн до добавления вторичных сценариев."
                    if locale == "ru"
                    else "Confirm the expected deadline before adding secondary workflows."
                ),
                source_type="unresolved",
                confidence="low",
            )
        )
    return assumptions


def dedupe_assumptions(items: list[AssumptionItem]) -> list[AssumptionItem]:
    """Deduplicate assumptions by statement while preserving order."""

    seen: set[str] = set()
    unique: list[AssumptionItem] = []
    for item in items:
        if item.statement not in seen:
            seen.add(item.statement)
            unique.append(item)
    return unique
