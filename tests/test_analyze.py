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
