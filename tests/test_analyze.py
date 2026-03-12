from specforge.pipeline.analyze import analyze_brief
from specforge.pipeline.intake import create_raw_brief, normalize_brief


def test_ambiguity_and_missing_decision_detection() -> None:
    text = """
    Under-Specified Client Brief
    We need something modern and powerful for everyone.
    Maybe a dashboard, portal, or some other workflow tool.
    """

    analyzed, report = analyze_brief(normalize_brief(create_raw_brief(text)))

    assert report.ambiguities
    assert any(item.category == "audience" for item in report.ambiguities)
    assert any(item.category == "platform" for item in report.ambiguities)
    assert any(item.category == "target_user" for item in report.missing_decisions)
    assert analyzed.open_questions == report.prioritized_open_questions


def test_contradiction_detection_for_multiple_patterns() -> None:
    text = """
    Contradictory Founder Brief
    Need a minimal MVP in 2 weeks for a solo founder budget.
    Also need enterprise SSO, audit logs, permissions, analytics, billing, and mobile support.
    Keep it cheap and fast.
    Goals:
    - Launch a minimal MVP fast
    - Replace multiple existing tools at once
    Constraints:
    - Budget under $5k
    - Need something usable in 2 weeks
    - Just me
    """

    _, report = analyze_brief(normalize_brief(create_raw_brief(text)))

    categories = {item.category for item in report.contradictions}
    assert "minimal-mvp-vs-enterprise-scope" in categories
    assert "small-team-aggressive-deadline-broad-scope" in categories
    assert "fast-cheap-feature-rich" in categories


def test_russian_overloaded_brief_triggers_contradictions() -> None:
    text = """
    Нужен простой MVP за 2 недели.
    Бюджет очень ограничен, команда из 2 человек.
    При этом нужен веб и мобильное приложение, CRM, Slack, биллинг, аналитика и роли доступа.
    Нужно сделать быстро и недорого.
    """

    analyzed, report = analyze_brief(normalize_brief(create_raw_brief(text)))

    categories = {item.category for item in report.contradictions}
    assert analyzed.summary.startswith("Нужен простой MVP")
    assert "fast-cheap-feature-rich" in categories
    assert "small-team-aggressive-deadline-broad-scope" in categories
    assert any(
        "Сведите" in item.recommendation or "Оставьте" in item.recommendation
        for item in report.contradictions
    )


def test_english_overloaded_brief_with_integrations_triggers_contradictions() -> None:
    text = """
    Need a simple MVP in 10 days with a lean budget.
    Team is just me and one contractor.
    It should include web and mobile, Salesforce, Stripe, Slack, analytics, admin,
    billing, and enterprise permissions.
    Keep it cheap and launch quickly.
    """

    _, report = analyze_brief(normalize_brief(create_raw_brief(text)))

    categories = {item.category for item in report.contradictions}
    assert "fast-cheap-feature-rich" in categories
    assert "minimal-mvp-vs-enterprise-scope" in categories
    assert "small-team-aggressive-deadline-broad-scope" in categories
    assert len(report.contradictions) == 3


def test_overloaded_contradictions_are_curated_not_duplicated() -> None:
    text = """
    Need a simple MVP in 2 weeks on a tight budget.
    Team is just me and one contractor.
    It must launch on web and mobile with Slack, Salesforce, Stripe, analytics,
    billing, admin, SSO, audit logs, and permissions.
    Keep it cheap and move fast.
    """

    _, report = analyze_brief(normalize_brief(create_raw_brief(text)))

    categories = [item.category for item in report.contradictions]
    assert categories == [
        "fast-cheap-feature-rich",
        "small-team-aggressive-deadline-broad-scope",
        "minimal-mvp-vs-enterprise-scope",
    ]


def test_assumptions_and_mvp_cut_are_created() -> None:
    text = """
    Internal Tool
    Need an internal tool for the operations team.
    Keep it local-first.
    Goals:
    - Reduce manual weekly reporting
    """

    _, report = analyze_brief(normalize_brief(create_raw_brief(text)))

    assert report.assumptions
    assert report.recommended_mvp_cut
