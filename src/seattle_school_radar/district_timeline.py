"""District timelines and critical open enrollment / lottery windows in Greater Seattle."""

from __future__ import annotations

import datetime

from seattle_school_radar.models import DistrictDeadline, ParentProfile


def get_upcoming_district_deadlines(
    current_date: datetime.date | None = None,
    profile: ParentProfile | None = None,
) -> list[DistrictDeadline]:
    """Generates an action-oriented timeline of admission & enrollment windows for Greater Seattle."""
    current_date = current_date or datetime.date.today()
    this_year = current_date.year

    deadlines: list[DistrictDeadline] = [
        DistrictDeadline(
            district_or_school="Bellevue School District (BSD 405)",
            window_name="BSD Open Enrollment (Procedure 3141P 跨区申请)",
            deadline_date=f"{this_year + 1}-01-15 至 {this_year + 1}-02-14",
            policy_reference="BSD Procedure 3141P / Open Enrollment",
            action_note=(
                "非 Bellevue 居民入读 BSD 学校的关键窗口。通过优先次序池审批；"
                "Newport Heights、Enatai 等校通常有可用容量；Jing Mei 需同步递交 Choice 申请。"
            ),
        ),
        DistrictDeadline(
            district_or_school="Bellevue School District (BSD 405)",
            window_name="Choice Schools & Programs Lottery (景美小学/Big Picture 抽签)",
            deadline_date=f"{this_year + 1}-01-10 至 {this_year + 1}-01-31",
            policy_reference="BSD Choice Lottery Guidelines",
            action_note=(
                "景美小学 (Jing Mei Mandarin Immersion) 每年 1 月开放摇号抽签；"
                "学区内外均可递交，2 月初统一电脑摇号出结果并产生 Waiting List。"
            ),
        ),
        DistrictDeadline(
            district_or_school="Issaquah School District (ISD 411)",
            window_name="ISD Inter-District Transfer (跨区 Choice Transfer)",
            deadline_date=f"{this_year + 1}-02-01 至 {this_year + 1}-02-28",
            policy_reference="ISD Regulation 3141 / Choice Transfer Portal",
            action_note=(
                "非 Issaquah 学区居民申请 Newcastle Elementary、Challenger 等校通道；"
                "需先从原对口学区释放 Choice Transfer Request，再向 ISD 提交。"
            ),
        ),
        DistrictDeadline(
            district_or_school="Lake Washington School District (LWSD 414)",
            window_name="LWSD Choice High Schools & Middle Schools Lottery",
            deadline_date=f"{this_year}-12-01 至 {this_year + 1}-01-08",
            policy_reference="LWSD Choice Schools Application",
            action_note=(
                "Tesla STEM、ICS (International Community School) 申请截止通常在每年 1 月初；"
                "面向全体 8 年级在读学生，抽签与材料审核并举。"
            ),
        ),
        DistrictDeadline(
            district_or_school="Seattle Public Schools (SPS 314)",
            window_name="SPS Open Enrollment for School Choice",
            deadline_date=f"{this_year + 1}-02-01 至 {this_year + 1}-02-28",
            policy_reference="SPS Annual School Choice Window",
            action_note=(
                "西雅图学区公立 Option Schools (如 TOPS, Thornton Creek) 与资优 Highly Capable (HCC) 确认。"
            ),
        ),
        DistrictDeadline(
            district_or_school="Independent Private Schools (Lakeside, Overlake, OWS, EPS)",
            window_name="Ravenna Hub / SAO 统一网申截止日",
            deadline_date=f"{this_year + 1}-01-09 至 {this_year + 1}-01-16",
            policy_reference="Puget Sound Independent Schools (PSIS) Timeline",
            action_note=(
                "大西雅图顶级独立走读私立统一网申截止；包含家长问卷、成绩单、推荐信及面试预约；"
                "OWS 需在 1 月中旬前提交专业 IQ 测试报告；3 月中旬统一发榜。"
            ),
        ),
    ]

    return deadlines
