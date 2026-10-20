"""Tests for OSPI and GreatSchools analytics engine."""

from seattle_school_radar.models import OSPIMetrics, SchoolRecord
from seattle_school_radar.ospi_engine import OSPIAnalyticsEngine


def test_ospi_public_school_analysis() -> None:
    school = SchoolRecord(
        id="test_public",
        name="Test Public Elementary",
        name_cn="测试公立小学",
        district="Bellevue School District (BSD 405)",
        category="Public Community",
        grades="K-5",
        city="Bellevue",
        gs_rating="9/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=80.0,
            ela_proficiency_pct=78.0,
            science_proficiency_pct=85.0,
            state_rank_percentile=5.0,
            student_growth_percentile=60.0,
            diversity_index=0.65,
        ),
        why_score="Balanced excellence.",
        curriculum_style="Standardized",
    )
    dissect = OSPIAnalyticsEngine.dissect_school_score(school)
    assert dissect["type"] == "Public State-Funded"
    assert "80.0%" in dissect["highlights"][0]
    assert "生源呈现健康的多元化" in dissect["equity_analysis"]


def test_ospi_private_school_analysis() -> None:
    school = SchoolRecord(
        id="test_private",
        name="Test Private Academy",
        name_cn="测试私立学院",
        district="Independent Private",
        category="Elite Private",
        grades="5-12",
        city="Seattle",
        gs_rating="N/A (Private)",
        ospi_metrics=None,
        why_score="Elite college placement.",
        curriculum_style="Seminar",
    )
    dissect = OSPIAnalyticsEngine.dissect_school_score(school)
    assert dissect["type"] == "Private / Independent"
