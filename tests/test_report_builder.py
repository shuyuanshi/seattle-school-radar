"""Tests for Seattle School Radar Report Builder."""

from seattle_school_radar.models import (
    BudgetType,
    ChildStage,
    EducationalPriority,
    ParentProfile,
    XHSReviewSummary,
)
from seattle_school_radar.report_builder import RadarReportBuilder
from seattle_school_radar.school_registry import SchoolRegistry


def test_report_builder_markdown_and_discord() -> None:
    profile = ParentProfile(
        child_age_years=3.5,
        child_stage=ChildStage.PRE_K,
        target_entry_year=2027,
        target_districts=["Bellevue (BSD 405)", "Independent Private"],
        budget_type=BudgetType.PUBLIC_CHOICE,
        priorities=EducationalPriority(academic_rigor=0.8, well_being_resilience=0.9),
    )
    registry = SchoolRegistry()
    matched = registry.filter_by_criteria(districts=profile.target_districts)

    sample_xhs = [
        XHSReviewSummary(
            school_id="newport_heights",
            school_name="Newport Heights Elementary",
            total_notes_reviewed=10,
            overall_sentiment="Positive",
            highlights=["学术扎实", "双语融合"],
            pitfalls_and_concerns=["坡道接送略堵"],
            parent_feedback_quotes=["‘体验非常好’"],
        )
    ]

    builder = RadarReportBuilder(profile, matched, sample_xhs)

    # 1. Test Markdown output
    md_content = builder.render_markdown()
    assert "# 🌲 大西雅图升学与校园情报周报" in md_content
    assert "Newport Heights" in md_content
    assert "BSD Procedure 3141P" in md_content
    assert "坡道接送略堵" in md_content

    # 2. Test Discord-Safe KV Stream output (zero raw tables)
    discord_content = builder.render_discord_kv_stream()
    assert "🌲 **[Seattle School Radar] 大西雅图升学雷达情报**" in discord_content
    assert "|---|" not in discord_content  # Stictly NO breaking markdown tables
    assert "> • **学区/类型**:" in discord_content
