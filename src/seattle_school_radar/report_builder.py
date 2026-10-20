"""Report Builder: Formats Greater Seattle School Radar reports.

Generates:
1. Full Markdown report (for GitHub repositories, Obsidian vaults, and PDF exports).
2. Discord/IM-Safe Key-Value stream (strictly adheres to mobile-safe, non-breaking formatting).
"""

from __future__ import annotations

import datetime

from seattle_school_radar.district_timeline import get_upcoming_district_deadlines
from seattle_school_radar.models import ParentProfile, RadarReport, SchoolRecord, XHSReviewSummary
from seattle_school_radar.ospi_engine import OSPIAnalyticsEngine


class RadarReportBuilder:
    """Builds structured and formatted Seattle School Radar reports."""

    def __init__(
        self,
        profile: ParentProfile,
        matched_schools: list[SchoolRecord],
        xhs_reviews: list[XHSReviewSummary] | None = None,
    ) -> None:
        self.profile = profile
        self.matched_schools = matched_schools
        self.xhs_reviews = xhs_reviews or []
        self.report_date = datetime.date.today().isoformat()

    def build_radar_report(self) -> RadarReport:
        """Constructs the structured RadarReport object."""
        deadlines = get_upcoming_district_deadlines(profile=self.profile)

        strategic_actions = [
            f"锁定目标学年 {self.profile.target_entry_year} 关键时间窗口：重点关注 BSD Procedure 3141P 与 ISD Choice Transfer 申请周期。",
            "若考虑景美小学 (Jing Mei)，需在每年 1 月准时参与 BSD Choice 摇号，并准备常规公立保底方案。",
            "如评估 Open Window (OWS) 资优私立，建议在入学前一年暑期提前预约第三方专业 IQ 评测 (WISC-V/WPPSI-IV)。",
            "实地考察建议：利用春季学校 Open House 走访目标校，近距离观察校区接送动线与家委会精神面貌。",
        ]

        summary_text = (
            f"学段定位: {self.profile.child_stage.value} (当前约 {self.profile.child_age_years:.1f} 岁) | "
            f"意向学区: {', '.join(self.profile.target_districts)} | "
            f"预算策略: {self.profile.budget_type.value} | "
            f"学术/弹性权衡: 学术 {self.profile.priorities.academic_rigor:.1f} / 心理弹性 {self.profile.priorities.well_being_resilience:.1f}"
        )

        return RadarReport(
            report_date=self.report_date,
            profile_summary=summary_text,
            matched_schools=self.matched_schools,
            district_deadlines=deadlines,
            community_insights=self.xhs_reviews,
            strategic_recommendations=strategic_actions,
        )

    def render_markdown(self) -> str:
        """Renders the comprehensive Markdown report."""
        report = self.build_radar_report()
        lines = [
            "# 🌲 大西雅图升学与校园情报周报 (Seattle School Radar)",
            f"> 生成时间: {report.report_date} · 区域: Greater Seattle Area (King & South Snohomish County)",
            "",
            "## 一、家长需求与 Grill 决策树画像",
            f"- **当前学段**: {self.profile.child_stage.value} (年龄约 {self.profile.child_age_years:.1f} 岁)",
            f"- **目标入学年份**: {self.profile.target_entry_year} 学年",
            f"- **意向学区/体系**: {', '.join(self.profile.target_districts)}",
            f"- **财务与预算模型**: {self.profile.budget_type.value}",
            f"- **核心价值取向**: 学术压测 ({self.profile.priorities.academic_rigor:.2f}) · 心理弹性 ({self.profile.priorities.well_being_resilience:.2f}) · 双语需求 ({self.profile.priorities.bilingual_immersion:.2f})",
            "",
            "---",
            "",
            "## 二、精准匹配学校档案与深度拆解",
        ]

        for s in report.matched_schools:
            dissect = OSPIAnalyticsEngine.dissect_school_score(s)
            lines.extend(
                [
                    f"### 🏫 {s.name_cn} / {s.name}",
                    f"- **所属学区/体系**: {s.district} ({s.city})",
                    f"- **学校类型**: {s.category} | 年级: {s.grades}",
                    f"- **GreatSchools 评级**: `{s.gs_rating}` | 学费: `{s.annual_tuition or 'Free (Public)'}`",
                ]
            )
            if s.feeder_pathway:
                lines.append(f"- **升学通道 (Feeder)**: {s.feeder_pathway}")
            if s.transfer_lottery_status:
                lines.append(f"- **跨区/抽签政策**: {s.transfer_lottery_status}")

            lines.append(f"- **评分逻辑剖析**: {s.why_score}")
            if dissect.get("equity_analysis"):
                lines.append(f"- **生源生态洞察**: {dissect['equity_analysis']}")
            lines.append("")

        lines.extend(
            [
                "---",
                "",
                "## 三、华人家长圈实况与小红书口碑提炼 (Chrome Bridge Anti-Scrape)",
            ]
        )

        if report.community_insights:
            for r in report.community_insights:
                lines.extend(
                    [
                        f"### 💬 {r.school_name} 家长口碑画像",
                        f"- **样本观察**: 覆盖 {r.total_notes_reviewed} 篇本地家长深度实测笔记 | 总体风向: `{r.overall_sentiment}`",
                        "- **高频好评点**:",
                    ]
                )
                for hl in r.highlights:
                    lines.append(f"  * {hl}")
                lines.append("- **潜在挑战与避坑点**:")
                for p in r.pitfalls_and_concerns:
                    lines.append(f"  * {p}")
                lines.append("- **家长原生心声**:")
                for q in r.parent_feedback_quotes:
                    lines.append(f"  > {q}")
                lines.append("")
        else:
            lines.append("_（暂无新增社区口碑缓存，下次采集流水线将按画像自动补充）_\n")

        lines.extend(
            [
                "---",
                "",
                "## 四、大西雅图学区重要申请日历与倒排窗口",
            ]
        )
        for d in report.district_deadlines:
            lines.extend(
                [
                    f"### 📅 {d.district_or_school} - {d.window_name}",
                    f"- **关键时间窗口**: `{d.deadline_date}`",
                    f"- **政策依据**: {d.policy_reference}",
                    f"- **操作指南**: {d.action_note}",
                    "",
                ]
            )

        lines.extend(
            [
                "---",
                "",
                "## 五、升学战略规划与下一阶段 Action Items",
            ]
        )
        for idx, act in enumerate(report.strategic_recommendations, 1):
            lines.append(f"{idx}. {act}")

        return "\n".join(lines)

    def render_discord_kv_stream(self) -> str:
        """Renders Discord-Safe Key-Value stream (zero tables, mobile-friendly)."""
        report = self.build_radar_report()
        blocks = [
            "🌲 **[Seattle School Radar] 大西雅图升学雷达情报**",
            f"> • **报告日期**: {report.report_date}",
            f"> • **画像摘要**: {report.profile_summary}",
            "",
            "🏫 **重点匹配学校推荐清单**",
        ]

        for s in report.matched_schools[:4]:
            blocks.append(
                f"> 🎓 **{s.name_cn}**\n"
                f"> • **学区/类型**: {s.district} · {s.category}\n"
                f"> • **GS评级/费用**: {s.gs_rating} · {s.annual_tuition or '免费公立'}\n"
                f"> • **直升高中**: {s.feeder_pathway or '独立出口'}\n"
                f"> • **生源与得分核心**: {s.why_score[:110]}…"
            )

        if report.community_insights:
            blocks.append("\n💬 **小红书家长圈口碑摘抄**")
            for r in report.community_insights[:2]:
                quote = r.parent_feedback_quotes[0] if r.parent_feedback_quotes else "口碑积极"
                blocks.append(
                    f"> 📝 **{r.school_name}** ({r.overall_sentiment})\n"
                    f"> • **家长原话**: {quote}\n"
                    f"> • **关注点**: {r.pitfalls_and_concerns[0] if r.pitfalls_and_concerns else '无特定异常'}"
                )

        blocks.append("\n📅 **近期核心申请窗口提示**")
        for d in report.district_deadlines[:3]:
            blocks.append(
                f"> ⏰ **{d.window_name}**\n"
                f"> • **截止节点**: {d.deadline_date}\n"
                f"> • **行动建议**: {d.action_note[:90]}…"
            )

        return "\n".join(blocks)
