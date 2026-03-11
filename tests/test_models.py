from specforge.domain.models import (
    AnalysisReport,
    AssumptionItem,
    ConstraintSet,
    ContradictionFinding,
    DeliveryArtifact,
    DeliveryPack,
    MissingDecision,
    NormalizedBrief,
    RawBrief,
)


def test_model_instantiation() -> None:
    raw = RawBrief(
        title="Test brief",
        source_text="Build an internal tool for the ops team.",
        notes=["Messy note"],
    )
    assumption = AssumptionItem(
        category="deployment",
        statement="Local execution is acceptable for the first release.",
        description="The brief suggests a local workflow.",
        rationale="The brief mentions local-first operation.",
        evidence=["Keep it local-first"],
        recommendation="Avoid hosted collaboration in the MVP.",
        source_type="explicit",
        confidence="high",
    )
    brief = NormalizedBrief(
        title="Test brief",
        source_text=raw.source_text,
        normalized_text=raw.source_text,
        summary="Build an internal tool for the ops team.",
        product_type="internal tool",
        audience=["operations team"],
        goals=["Reduce manual updates"],
        constraints=ConstraintSet(platform_hints=["local-first"]),
        assumptions=[assumption],
        open_questions=["What timeline matters most?"],
        risks=["Timeline is not yet specified."],
        analysis=AnalysisReport(
            assumptions=[assumption],
            contradictions=[
                ContradictionFinding(
                    category="scope",
                    description="Scope conflicts with delivery pressure.",
                    evidence=["2 weeks", "all-in-one"],
                    recommendation="Cut the first release.",
                )
            ],
            missing_decisions=[
                MissingDecision(
                    category="ownership_operations",
                    description="Owner is unclear.",
                    evidence=["No owner named"],
                    recommendation="Assign an owner.",
                )
            ],
        ),
    )
    pack = DeliveryPack(
        generated_at="2026-03-11T00:00:00+00:00",
        brief=brief,
        analysis=brief.analysis,
        brief_summary="A deterministic draft for an internal tool.",
        goals=brief.goals,
        constraints=brief.constraints,
        first_step_recommendation="Clarify the deadline before planning implementation.",
        artifacts=[
            DeliveryArtifact(
                name="brief.md",
                kind="markdown",
                relative_path="brief.md",
                content="# Draft",
            )
        ],
    )

    assert raw.title == "Test brief"
    assert brief.assumptions[0].confidence == "high"
    assert pack.analysis.contradictions[0].category == "scope"
    assert pack.artifacts[0].name == "brief.md"
