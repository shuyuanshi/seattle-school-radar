"""Tests for Seattle School Radar models."""

from seattle_school_radar.models import (
    BudgetType,
    ChildStage,
    EducationalPriority,
    ParentProfile,
    SchoolRecord,
)


def test_parent_profile_creation() -> None:
    profile = ParentProfile(
        child_age_years=3.0,
        child_stage=ChildStage.PRE_K,
        target_entry_year=2027,
        target_districts=["Bellevue (BSD 405)"],
        budget_type=BudgetType.PUBLIC_CHOICE,
        priorities=EducationalPriority(academic_rigor=0.8, well_being_resilience=0.9),
    )
    assert profile.child_age_years == 3.0
    assert profile.child_stage == ChildStage.PRE_K
    assert "Bellevue (BSD 405)" in profile.target_districts
    assert profile.priorities.academic_rigor == 0.8


def test_school_record_creation() -> None:
    school = SchoolRecord(
        id="test_school",
        name="Test Elementary",
        name_cn="测试小学",
        district="Bellevue School District (BSD 405)",
        category="Public Community",
        grades="K-5",
        city="Bellevue",
        gs_rating="9/10",
        why_score="Strong test scores and inclusive culture.",
        curriculum_style="Balanced",
    )
    assert school.id == "test_school"
    assert school.annual_tuition is None
