"""Tests for Matt Pocock Grill Engine with dynamic pruning and robust parsing."""

from seattle_school_radar.grill_engine import GrillSession, execute_interactive_grill
from seattle_school_radar.models import BudgetType, ChildStage


def test_grill_session_frontier_generation_and_pruning() -> None:
    session = GrillSession()
    r1 = session.get_round_1_frontier()
    assert len(r1) == 2
    assert r1[0].id == "Q1_AGE_STAGE"
    assert r1[1].id == "Q2_TARGET_DISTRICTS"

    # Test round 2 dynamic pruning for Elementary stage
    r1_elem = {
        "Q1_AGE_STAGE": "3-4 岁 Pre-K",
        "Q2_TARGET_DISTRICTS": "Bellevue (BSD 405) + Independent Private",
    }
    r2_elem = session.get_round_2_grill_frontier(r1_elem)
    q_elem_ids = {q.id for q in r2_elem}
    assert "Q3_GRILL_RIGOR_VS_WELLBEING" in q_elem_ids
    assert "Q4_GRILL_BILINGUAL_STRATEGY" in q_elem_ids  # Elementary gets bilingual question
    assert "Q6_GRILL_FINANCIAL_ROI" in q_elem_ids

    # Test round 2 dynamic pruning for High School stage
    r1_high = {
        "Q1_AGE_STAGE": "Grades 6-12 Middle/High",
        "Q2_TARGET_DISTRICTS": "Lake Washington (LWSD 414)",
    }
    r2_high = session.get_round_2_grill_frontier(r1_high)
    q_high_ids = {q.id for q in r2_high}
    assert "Q4_GRILL_CURRICULUM_TRACK" in q_high_ids  # High school gets AP vs IB track question
    assert (
        "Q4_GRILL_BILINGUAL_STRATEGY" not in q_high_ids
    )  # Elementary bilingual question is pruned!


def test_build_profile_english_robust_parsing() -> None:
    """Verifies that English inputs parse correctly into ParentProfile."""
    session = GrillSession()
    answers = {
        "Q1_AGE_STAGE": "Kindergarten (5 yo)",
        "Q2_TARGET_DISTRICTS": "Lake Washington (LWSD 414)",
        "Q3_GRILL_RIGOR_VS_WELLBEING": "Balanced academic rigor with strong whole child SEL",
        "Q4_GRILL_BILINGUAL_STRATEGY": "Standard English curriculum",
        "Q5_GRILL_PARENT_TIME_BUDGET": "Moderate, about 2-4 hours per week",
        "Q6_GRILL_FINANCIAL_ROI": "Public only",
    }
    profile = session.build_parent_profile(answers)
    assert profile.child_stage == ChildStage.KINDERGARTEN
    assert profile.child_age_years == 5.0
    assert "Lake Washington (LWSD 414)" in profile.target_districts
    assert profile.budget_type == BudgetType.PUBLIC_COMMUNITY
    assert profile.priorities.well_being_resilience >= 0.8
    # Session state should be recorded
    assert len(session.answers) >= 5


def test_interactive_grill_headless_eof_error() -> None:
    """Verifies that EOFError in headless / cron environments safely defaults to recommendations."""

    def mock_eof_input(prompt: str) -> str:
        raise EOFError("No TTY attached")

    logs: list[str] = []
    profile = execute_interactive_grill(input_fn=mock_eof_input, print_fn=logs.append)
    assert profile.child_age_years > 0
    assert profile.child_stage.value != ""
    assert len(profile.target_districts) > 0
