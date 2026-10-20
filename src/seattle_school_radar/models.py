"""Data models for Seattle School Radar."""

from __future__ import annotations

from enum import Enum

from pydantic import BaseModel, Field


class ChildStage(str, Enum):
    INFANT_TODDLER = "Infant/Toddler (0-2 yo)"
    PRE_K = "Pre-K / Preschool (3-4 yo)"
    KINDERGARTEN = "Kindergarten (5 yo)"
    ELEMENTARY = "Elementary School (Grades 1-5)"
    MIDDLE = "Middle School (Grades 6-8)"
    HIGH = "High School (Grades 9-12)"


class BudgetType(str, Enum):
    PUBLIC_COMMUNITY = "Public In-District (Community Feeder)"
    PUBLIC_CHOICE = "Public Choice / Lottery / Open Enrollment"
    PRIVATE_MODERATE = "Private Independent (≤$28k/yr)"
    PRIVATE_PREMIUM = "Private Elite / Independent ($35k-$55k/yr)"
    FLEXIBLE = "Flexible / Pragmatic Mix"


class EducationalPriority(BaseModel):
    academic_rigor: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Weight for academic testing & AP/Honors"
    )
    stem_focus: float = Field(
        default=0.7, ge=0.0, le=1.0, description="Weight for math/science/robotics"
    )
    well_being_resilience: float = Field(
        default=0.8,
        ge=0.0,
        le=1.0,
        description="Weight for mental health, low peer pressure, emotional support",
    )
    bilingual_immersion: float = Field(
        default=0.3, ge=0.0, le=1.0, description="Weight for dual-language Chinese/Spanish"
    )
    whole_child_inquiry: float = Field(
        default=0.6,
        ge=0.0,
        le=1.0,
        description="Weight for project-based/inquiry learning vs rote memorization",
    )
    parent_involvement_tolerance: float = Field(
        default=0.3,
        ge=0.0,
        le=1.0,
        description="Parent time capacity (0.0=busy dual-career, 1.0=full-time volunteering)",
    )


class ParentProfile(BaseModel):
    child_age_years: float = Field(..., description="Child age in years, e.g. 2.5 or 5.0")
    child_stage: ChildStage = Field(..., description="Educational stage")
    target_entry_year: int = Field(
        ..., description="Target enrollment school year, e.g. 2026 or 2027"
    )
    target_districts: list[str] = Field(
        default_factory=list, description="Target districts or private tiers"
    )
    budget_type: BudgetType = Field(
        default=BudgetType.FLEXIBLE, description="Education budget preference"
    )
    priorities: EducationalPriority = Field(default_factory=EducationalPriority)
    specific_interests: list[str] = Field(
        default_factory=list, description="e.g. Gifted/Prism, Chess, Tennis, Music"
    )
    notes: str = Field(default="", description="Additional context or notes")


class OSPIMetrics(BaseModel):
    math_proficiency_pct: float
    ela_proficiency_pct: float
    science_proficiency_pct: float
    state_rank_percentile: float = Field(
        description="Top percentile in Washington state, e.g. 5.0 means top 5%"
    )
    student_growth_percentile: float = Field(
        default=50.0, description="Median SGP progress indicator"
    )
    diversity_index: float = Field(default=0.5, description="Demographic diversity balance")


class SchoolRecord(BaseModel):
    id: str
    name: str
    name_cn: str
    district: str
    category: str
    grades: str
    city: str
    gs_rating: str
    ospi_metrics: OSPIMetrics | None = None
    feeder_pathway: str | None = None
    why_score: str
    curriculum_style: str
    transfer_lottery_status: str | None = None
    annual_tuition: str | None = None
    key_tags: list[str] = Field(default_factory=list)


class XHSNoteSnippet(BaseModel):
    title: str
    content_summary: str
    likes: int = 0
    sentiment: str = "Neutral"
    key_takeaways: list[str] = Field(default_factory=list)


class XHSReviewSummary(BaseModel):
    school_id: str
    school_name: str
    total_notes_reviewed: int
    overall_sentiment: str
    highlights: list[str]
    pitfalls_and_concerns: list[str]
    parent_feedback_quotes: list[str]


class FrontierQuestion(BaseModel):
    id: str
    round_num: int
    title: str
    question_body: str
    recommended_answer: str
    options: list[str] = Field(default_factory=list)
    resolved: bool = False
    chosen_answer: str | None = None


class DistrictDeadline(BaseModel):
    district_or_school: str
    window_name: str
    deadline_date: str
    policy_reference: str
    action_note: str


class RadarReport(BaseModel):
    report_date: str
    profile_summary: str
    matched_schools: list[SchoolRecord]
    district_deadlines: list[DistrictDeadline]
    community_insights: list[XHSReviewSummary]
    strategic_recommendations: list[str]
