"""Tests for Xiaohongshu crawler and anti-ban mechanics."""

from seattle_school_radar.models import SchoolRecord
from seattle_school_radar.xhs_radar import (
    HumanJitter,
    RateLimiter,
    RiskDetector,
    SmoothScroller,
    XHSRadarCrawler,
)


def test_human_jitter_distribution() -> None:
    t = HumanJitter.micro_sleep(min_ms=10, max_ms=30)
    assert 0.01 <= t <= 0.04


def test_rate_limiter_window() -> None:
    limiter = RateLimiter(max_requests=2, window_seconds=1.0)
    limiter.acquire()
    limiter.acquire()
    assert len(limiter.timestamps) == 2


def test_risk_detector_and_smooth_scroller() -> None:
    crawler = XHSRadarCrawler()
    # Mock crawler without bridge connection safely evaluates to False
    has_risk, reason = RiskDetector.check_risk(crawler)
    assert not has_risk
    assert reason == ""

    # SmoothScroller executes safely without bridge
    res = SmoothScroller.scroll(crawler, total_distance=400, steps=3)
    assert res is None


def test_xhs_crawler_synthesis() -> None:
    school = SchoolRecord(
        id="newport_heights",
        name="Newport Heights Elementary",
        name_cn="纽波特高地小学",
        district="Bellevue School District (BSD 405)",
        category="Public",
        grades="K-5",
        city="Bellevue",
        gs_rating="9/10",
        why_score="Balanced",
        curriculum_style="Balanced",
    )
    crawler = XHSRadarCrawler()
    summary = crawler.search_school_buzz(school)
    assert summary.school_id == "newport_heights"
    assert len(summary.highlights) >= 2
    assert len(summary.pitfalls_and_concerns) >= 1
    assert "Newport" in summary.highlights[0]
