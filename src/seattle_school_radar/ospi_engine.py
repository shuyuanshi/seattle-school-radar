"""OSPI & GreatSchools Analytics Engine.

Explains and contextualizes Washington State Report Card (OSPI) SBA scores,
Student Growth Percentiles (SGP), and GreatSchools ratings for Greater Seattle schools.
"""

from __future__ import annotations

from typing import Any

from seattle_school_radar.models import SchoolRecord


class OSPIAnalyticsEngine:
    """Analytical helper to break down WA state metrics and GreatSchools ratings."""

    @staticmethod
    def dissect_school_score(school: SchoolRecord) -> dict[str, Any]:
        """Provides an analytical breakdown of why a school received its score."""
        metrics = school.ospi_metrics
        if not metrics:
            return {
                "school_id": school.id,
                "school_name": school.name,
                "type": "Private / Independent",
                "summary": "私立学校不参与华州 SBA 标准化统考，学术实力参考 ISEE/SSAT 中位数、AP/IB 满分率及升学出口走向。",
                "analysis": school.why_score,
            }

        # Analyze Public school scores
        state_avg_math = 50.0
        state_avg_ela = 55.0
        state_avg_sci = 45.0

        math_diff = metrics.math_proficiency_pct - state_avg_math
        ela_diff = metrics.ela_proficiency_pct - state_avg_ela
        sci_diff = metrics.science_proficiency_pct - state_avg_sci

        analysis_points = [
            f"华州 SBA 数理达标率 {metrics.math_proficiency_pct:.1f}% (超全州均线 {math_diff:+.1f}%)",
            f"华州 SBA 英语 (ELA) 达标率 {metrics.ela_proficiency_pct:.1f}% (超全州均线 {ela_diff:+.1f}%)",
            f"华州 SBA 科学达标率 {metrics.science_proficiency_pct:.1f}% (超全州均线 {sci_diff:+.1f}%)",
            f"全华州综合学术排名前 {metrics.state_rank_percentile:.1f}%",
            f"学生进步指数 (Student Growth Percentile): {metrics.student_growth_percentile:.0f}/100",
        ]

        equity_note = ""
        if metrics.diversity_index > 0.60:
            equity_note = (
                "【生源结构提示】：生源呈现健康的多元化与包容性。在 GreatSchools 的 Equity 指标中，"
                "由于需统计非母语英语学习者 (ELL) 和特教融合群体的基准线，总体评分偶受拉平，"
                "但这属于正常公立健康生态，非核心学术滑坡。"
            )
        else:
            equity_note = (
                "【生源结构提示】：生源以高学术亚裔/科技家庭高度集中，SBA 测验输出极高，"
                "需注意同侪内卷指数与校外课外补习依赖度。"
            )

        return {
            "school_id": school.id,
            "school_name": school.name,
            "type": "Public State-Funded",
            "gs_rating": school.gs_rating,
            "highlights": analysis_points,
            "equity_analysis": equity_note,
            "deep_dive": school.why_score,
        }
