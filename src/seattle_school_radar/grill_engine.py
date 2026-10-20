"""Grill Engine: Relentless interview & decision-tree pruning for Seattle parents.

Implements Matt Pocock's grill-me / grilling protocol:
1. Maps decisions as a design tree with explicit dynamic branches.
2. Dynamically prunes the frontier based on Round 1 prerequisites (e.g. stage, district).
3. Provides AI-recommended answers for every question ("yes" accepts the recommendation).
4. Relentlessly grills ambiguous parent demands (e.g., "well-rounded", "good school", "whatever works")
   by presenting realistic, hard trade-offs.
5. Robust bilingual parser (English & Chinese) converging into a strictly validated ParentProfile.
"""

from __future__ import annotations

from typing import Callable

from seattle_school_radar.models import (
    BudgetType,
    ChildStage,
    EducationalPriority,
    FrontierQuestion,
    ParentProfile,
)


class GrillSession:
    """Manages dynamic multi-round decision tree grilling for school radar targeting."""

    def __init__(self) -> None:
        self.round_history: list[FrontierQuestion] = []
        self.answers: dict[str, str] = {}

    def get_round_1_frontier(self) -> list[FrontierQuestion]:
        """Round 1: Hard demographic and timeline boundary questions."""
        q1 = FrontierQuestion(
            id="Q1_AGE_STAGE",
            round_num=1,
            title="孩子当前实际年龄与计划入学学段",
            question_body=(
                "大西雅图公立与私立的招生报名窗口存在严格截止日（9月1日满 5 周岁入读公立 Kindergarten；"
                "私立提前 1 年申请，通常 1 月上旬截止）。\n"
                "请问孩子目前多大？计划什么时候入读哪一个学段？\n"
                "可选项：\n"
                "  A. 幼儿期 (0-2 岁 Infant/Toddler) - 提前关注学区房与日托/Pre-K 规划\n"
                "  B. 学前学龄 (3-4 岁 Pre-K) - 倒排次年 Kindergarten 抽签与私校申请\n"
                "  C. 幼升小 (5 岁 Kindergarten) - 确定公立对口注册或 Choice Transfer\n"
                "  D. 小学插班 (Grades 1-5 Elementary) - 考虑跨区/转学或资优 Prism/Quest 考试\n"
                "  E. 小升初/初升高 (Grades 6-12 Middle/High) - 锁定高中出口与升学通道"
            ),
            recommended_answer="学前学龄 (3-4 岁 Pre-K)，需提前 1~2 年梳理公立对口学区房、跨区 Choice 抽签及私立申请节奏。",
            options=[
                "0-2 岁 Infant/Toddler",
                "3-4 岁 Pre-K",
                "5 岁 Kindergarten",
                "Grades 1-5 Elementary",
                "Grades 6-12 Middle/High",
            ],
        )

        q2 = FrontierQuestion(
            id="Q2_TARGET_DISTRICTS",
            round_num=1,
            title="重点意向公立学区与私校体系范围",
            question_body=(
                "大西雅图区域不同板块教育生态差异极大。请明确你们目前主要考虑哪几个学区或教育体系？\n"
                "可选项：\n"
                "  A. Bellevue 学区 (BSD 405) - Newport, Somerset, Medina, Jing Mei 双语\n"
                "  B. Lake Washington 学区 (LWSD 414) - Redmond, Kirkland, Tesla STEM, ICS\n"
                "  C. Issaquah 学区 (ISD 411) - Newcastle, Grand Ridge, Skyline, Liberty\n"
                "  D. Mercer Island 学区 (MISD 400) - 独立岛屿学区，生源纯粹稳定\n"
                "  E. 西雅图市区 (SPS 314) - 资优 HCC 或公立名校 (Cascadia, Garfield, Roosevelt)\n"
                "  F. 顶尖独立私立体系 - Lakeside, Overlake, Open Window (OWS), BCA, CCA, Bush 等\n"
                "  G. 跨区开放申请组合 (BSD Choice + ISD/LWSD 混合考察)"
            ),
            recommended_answer="以东区核心公立（Bellevue BSD + Lake Washington LWSD）为基底，重点考察社区对口及跨区 Choice，同时兼顾高契合度私校（OWS/Overlake）。",
            options=[
                "Bellevue (BSD 405)",
                "Lake Washington (LWSD 414)",
                "Issaquah (ISD 411)",
                "Mercer Island (MISD 400)",
                "Seattle (SPS 314)",
                "Top Private (Lakeside/Overlake/OWS/BCA)",
                "Hybrid Multi-District",
            ],
        )

        self.round_history.extend([q1, q2])
        return [q1, q2]

    def get_round_2_grill_frontier(self, r1_answers: dict[str, str]) -> list[FrontierQuestion]:
        """Round 2: The Relentless Grill with Dynamic Pruning based on Round 1 answers."""
        q1_text = r1_answers.get("Q1_AGE_STAGE", "").lower()
        q2_text = r1_answers.get("Q2_TARGET_DISTRICTS", "").lower()

        is_high_school = (
            "high" in q1_text or "初升高" in q1_text or "6-12" in q1_text or "middle" in q1_text
        )
        is_pure_public = "private" not in q2_text and "私立" not in q2_text

        questions: list[FrontierQuestion] = []

        # Dynamic Q3: Rigor vs Wellbeing (Core Trade-off)
        if is_high_school:
            q3 = FrontierQuestion(
                id="Q3_GRILL_RIGOR_VS_WELLBEING",
                round_num=2,
                title="【Grill 核心】高中 AP/STEM 竞赛刷题天花板 vs 心理弹性与综合背景",
                question_body=(
                    "高中阶段 GPA 与 AP 课程对大学申请至关重要：\n"
                    "• Tesla STEM / Newport High: 极其高强度的 STEM 科研与 AP 压测，常春藤与 CMU/MIT 录取率高，但同侪学业竞争白热化；\n"
                    "• Overlake / Bush / Liberty High: 注重全人探索、领导力与健康心理弹性，学术节奏稳健但恶性刷题压力较小。\n"
                    "高中出口你愿意接受哪种同侪生态？"
                ),
                recommended_answer="在保证优质 AP 与 STEM 科研平台的前提下，优先注重孩子的心理弹性与全面背景塑造，避免恶性内卷。",
                options=["极度追求 AP/竞赛天花板", "优质学术与心理健康平衡", "全人探究与自主发展"],
            )
        else:
            q3 = FrontierQuestion(
                id="Q3_GRILL_RIGOR_VS_WELLBEING",
                round_num=2,
                title="【Grill 核心】小学/初中基础：学术压测与同侪竞争 vs 心理健康与弹性",
                question_body=(
                    "很多家长第一反应是'既要学术拔尖，又要孩子开开心心'，但现实往往存在硬性挤出效应：\n"
                    "• Somerset / Medina 等学术神校：SBA 数理达标率逼近 90%，但伴随的是 80%+ 亚裔高压氛围，大量家庭在 Kumon/AoPS 深度投入；\n"
                    "• Open Window (OWS) / Bush / Newport Heights：注重全人关怀、社交情绪韧性 (SEL) 与探究式学习，学术环境包容但刷题节奏平缓。\n"
                    "如果只能以一个为主线，你的底线选择是？"
                ),
                recommended_answer="在保障扎实公立学术底座的前提下（如 Newport Heights / Rockwell / Newcastle），优先保护孩子的内驱力与心理健康，拒绝极端应试内卷校。",
                options=[
                    "极度追求学术压测与 AP/奥数天花板",
                    "追求平衡型优质学术与健康成长",
                    "以探究式教育与社交情绪韧性为首选",
                ],
            )
        questions.append(q3)

        # Dynamic Q4: Pruned by Stage (Elementary stages get Bilingual immersion grill, High school gets Curriculum track grill)
        if not is_high_school:
            q4 = FrontierQuestion(
                id="Q4_GRILL_BILINGUAL_STRATEGY",
                round_num=2,
                title="【Grill 核心】全日制双语沉浸 vs 本土纯美本升学加速",
                question_body=(
                    "华州公立唯一的 50/50 沉浸式中文双语 Choice 景美小学 (Jing Mei) 极其热门。\n"
                    "但客观事实是：50% 中文授课不可避免会挤占全英文学术和 ELA 深度阅读课时，到 G3-G5 阶段部分家长会产生'英文词汇深度不足'的焦虑。\n"
                    "你们家庭的真实语言策略是？"
                ),
                recommended_answer="以英文母语级学术能力与阅读深度为主干，中文双语作为家庭与课外文化熏陶，不把全日制双语抽签作为单一刚需绑定。",
                options=[
                    "全日制双语沉浸为刚需",
                    "英文纯学术为主，家庭保留中文",
                    "对双语无执念，纯美本学术优先",
                ],
            )
        else:
            q4 = FrontierQuestion(
                id="Q4_GRILL_CURRICULUM_TRACK",
                round_num=2,
                title="【Grill 核心】AP 密集体系 vs IB Diploma 国际文凭体系",
                question_body=(
                    "大西雅图高中分为两大主流学术体系：\n"
                    "• AP 体系 (Newport, Bellevue, Tesla STEM, Skyline): 单科自由度高，适合理科先修与美本换学分；\n"
                    "• IB Diploma 体系 (Interlake High, Willows Prep): 强调批判性大论文 (EE) 与认识论 (TOK)，人文与全科要求极高。\n"
                    "你的学术课程偏向是？"
                ),
                recommended_answer="倾向 AP 灵活单科加速体系，利于集中优势突破理科与竞赛先修。",
                options=["AP 灵活单科加速", "IB Diploma 全人体系", "常规高中文凭 + 社区实践"],
            )
        questions.append(q4)

        # Dynamic Q5: Parent involvement
        q5 = FrontierQuestion(
            id="Q5_GRILL_PARENT_TIME_BUDGET",
            round_num=2,
            title="【Grill 核心】家长时间精力与家委会 (PTSA) 卷度容忍度",
            question_body=(
                "许多顶尖学校（尤其是特色 Choice 学校和高端独立私立）的背后，是家长每月 10-20 小时的深度志愿绑定与筹款晚宴；\n"
                "而双职工高频出差/大厂家庭往往疲惫不堪。你们家庭在孩子教育上每周能投入多少物理时间？"
            ),
            recommended_answer="双职工家庭时间有限，期望学校建立成熟独立的教学与课后托管闭环，拒绝把学校运营负担转嫁为家长考勤压力。",
            options=[
                "双职工忙碌：需要完善的托管与独立闭环",
                "适度参与：每周能抽出 2-4 小时",
                "全力投入：家长一方可全职深度介入学校志愿",
            ],
        )
        questions.append(q5)

        # Dynamic Q6: Financial ROI (Pruned if pure public in R1)
        if is_pure_public:
            q6 = FrontierQuestion(
                id="Q6_GRILL_FINANCIAL_ROI",
                round_num=2,
                title="【Grill 核心】公立对口买房地税溢价 vs 跨区 Choice 抽签的通勤成本",
                question_body=(
                    "既然锁定公立体系，主要权衡在于：\n"
                    "• 购买高价对口学区房 (如 Medina, Somerset, Mercer Island): 承受极高地税与房价溢价，但步行/近距入读；\n"
                    "• 申请跨区 Open Enrollment / Choice Transfer (如 BSD 3141P): 居住在周边高性价比社区，但每日需跨区接送 30-40 分钟。\n"
                    "你的通勤与居住策略是？"
                ),
                recommended_answer="精选高性价比东区成熟社区，积极利用学区开放申请政策撬动跨区优质单体校，同时兼顾通勤动线。",
                options=["坚定对口买房", "跨区 Choice 抽签 + 接送通勤", "居住地就近普通公立"],
            )
        else:
            q6 = FrontierQuestion(
                id="Q6_GRILL_FINANCIAL_ROI",
                round_num=2,
                title="【Grill 核心】每年 $35k-$55k 私立学费 vs 公立房产税溢价的 ROI 算账",
                question_body=(
                    "西雅图东区优质公立依靠房产税支撑，教学质量全美前列；\n"
                    "而私立走读（Lakeside, Overlake, OWS）每年净学费 $38,000 - $49,000（加上捐款与杂费超 $55k/年）。\n"
                    "如果一个孩子从 K 读到 12 年级，纯私校开销超 60-70 万美元税后现金。你的财务与升学策略是？"
                ),
                recommended_answer="公立打底（通过买房或 Procedure 3141P 锁定优质单体校），同时为高契合度特色校（如 OWS 资优或 Overlake）保留机动申请预算，不做盲目私校跟风。",
                options=[
                    "纯公立路径：依靠地税与社区强校",
                    "公私兼修：公立保底，择机冲刺顶级私校",
                    "坚定全私立：锁定顶私闭环",
                ],
            )
        questions.append(q6)

        self.round_history.extend(questions)
        return questions

    def build_parent_profile(self, answers: dict[str, str]) -> ParentProfile:
        """Translates raw answers into a verified, typed ParentProfile with robust parsing."""
        self.answers.update(answers)

        # Derive age and stage
        q1_raw = answers.get("Q1_AGE_STAGE", "").lower()
        if any(w in q1_raw for w in ["0-2", "infant", "toddler", "幼儿"]):
            age = 1.5
            stage = ChildStage.INFANT_TODDLER
            target_year = 2029
        elif any(w in q1_raw for w in ["3-4", "pre-k", "preschool", "学前"]):
            age = 3.5
            stage = ChildStage.PRE_K
            target_year = 2027
        elif any(w in q1_raw for w in ["5", "kindergarten", "幼升小"]):
            age = 5.0
            stage = ChildStage.KINDERGARTEN
            target_year = 2026
        elif any(w in q1_raw for w in ["1-5", "elementary", "小学"]):
            age = 8.0
            stage = ChildStage.ELEMENTARY
            target_year = 2026
        elif any(w in q1_raw for w in ["6-12", "middle", "high", "初中", "高中"]):
            age = 13.0
            stage = ChildStage.HIGH
            target_year = 2026
        else:
            age = 5.0
            stage = ChildStage.KINDERGARTEN
            target_year = 2026

        # Derive districts
        q2_raw = answers.get("Q2_TARGET_DISTRICTS", "").lower()
        districts: list[str] = []
        if "bellevue" in q2_raw or "bsd" in q2_raw:
            districts.append("Bellevue (BSD 405)")
        if "lake washington" in q2_raw or "lwsd" in q2_raw:
            districts.append("Lake Washington (LWSD 414)")
        if "issaquah" in q2_raw or "isd" in q2_raw:
            districts.append("Issaquah (ISD 411)")
        if "mercer island" in q2_raw or "misd" in q2_raw:
            districts.append("Mercer Island (MISD 400)")
        if "seattle" in q2_raw or "sps" in q2_raw:
            districts.append("Seattle (SPS 314)")
        if "northshore" in q2_raw or "nsd" in q2_raw:
            districts.append("Northshore (NSD 417)")
        if "private" in q2_raw or "私立" in q2_raw:
            districts.append("Independent Private")

        if not districts:
            districts = ["Bellevue (BSD 405)", "Lake Washington (LWSD 414)"]

        # Derive priorities from Grill Round 2
        q3_ans = answers.get("Q3_GRILL_RIGOR_VS_WELLBEING", "").lower()
        q4_ans = (
            answers.get("Q4_GRILL_BILINGUAL_STRATEGY", "").lower()
            or answers.get("Q4_GRILL_CURRICULUM_TRACK", "").lower()
        )
        q5_ans = answers.get("Q5_GRILL_PARENT_TIME_BUDGET", "").lower()
        q6_ans = answers.get("Q6_GRILL_FINANCIAL_ROI", "").lower()

        # Rigor vs wellbeing
        if any(w in q3_ans for w in ["极度", "天花板", "奥数", "extreme", "high peer", "olympiad"]):
            academic_rigor = 0.95
            well_being = 0.65
        elif any(
            w in q3_ans
            for w in [
                "探究",
                "弹性",
                "whole child",
                "sel",
                "wellbeing",
                "well-being",
                "balanced",
                "平衡",
            ]
        ):
            academic_rigor = 0.75
            well_being = 0.90
        else:
            academic_rigor = 0.80
            well_being = 0.85

        # Bilingual
        if any(w in q4_ans for w in ["全日制", "刚需", "bilingual", "immersion"]):
            bilingual = 0.85
        else:
            bilingual = 0.25

        # Time budget
        if any(w in q5_ans for w in ["全力", "全职", "heavy", "full-time"]):
            time_tol = 0.90
        elif any(w in q5_ans for w in ["适度", "moderate"]):
            time_tol = 0.50
        else:
            time_tol = 0.30

        # Budget type
        if any(w in q6_ans for w in ["纯公立", "对口买房", "public only"]):
            budget = BudgetType.PUBLIC_COMMUNITY
        elif any(w in q6_ans for w in ["全私立", "坚定", "private only"]):
            budget = BudgetType.PRIVATE_PREMIUM
        else:
            budget = BudgetType.FLEXIBLE

        priorities = EducationalPriority(
            academic_rigor=academic_rigor,
            stem_focus=0.80,
            well_being_resilience=well_being,
            bilingual_immersion=bilingual,
            whole_child_inquiry=0.75,
            parent_involvement_tolerance=time_tol,
        )

        return ParentProfile(
            child_age_years=age,
            child_stage=stage,
            target_entry_year=target_year,
            target_districts=districts,
            budget_type=budget,
            priorities=priorities,
            specific_interests=["STEM Exploration", "Logic & Math", "Safe School Culture"],
            notes="Configured via dynamic grill-me decision interview.",
        )


def execute_interactive_grill(
    session: GrillSession | None = None,
    input_fn: Callable[[str], str] = input,
    print_fn: Callable[..., None] = print,
) -> ParentProfile:
    """Runs a live interactive Grill session via console.

    Prompts the user question-by-question, displaying recommended answers.
    Pressing Enter or typing 'yes' / 'y' immediately adopts the recommendation.
    """
    session = session or GrillSession()
    print_fn("\n" + "=" * 70)
    print_fn("🎯 [Seattle School Radar] 家长决策树 Grill 质询协议启动")
    print_fn("采用 Matt Pocock grill-me 标准：直击核心矛盾与真实 Trade-off。")
    print_fn("提示：直接按回车或输入 'yes' 即可采纳系统推荐方案。")
    print_fn("=" * 70 + "\n")

    # Round 1
    r1_questions = session.get_round_1_frontier()
    r1_answers: dict[str, str] = {}
    for q in r1_questions:
        print_fn(f"\n❓ **{q.id}** - **{q.title}**:")
        print_fn(q.question_body)
        print_fn(f"\n➡️ 推荐方案: {q.recommended_answer}\n")
        try:
            user_in = input_fn("你的选择 [直接回车/yes采纳推荐方案, 或输入自定义偏好]: ").strip()
        except (EOFError, KeyboardInterrupt):
            user_in = ""

        if not user_in or user_in.lower() in ("yes", "y", "ok", "确认", "采纳"):
            r1_answers[q.id] = q.recommended_answer
        else:
            r1_answers[q.id] = user_in

    # Round 2
    r2_questions = session.get_round_2_grill_frontier(r1_answers)
    r2_answers: dict[str, str] = {}
    print_fn("\n" + "-" * 70)
    print_fn("🔥 进入 Round 2: 核心教育理念与硬性 Trade-off 质询 (The Grill)")
    print_fn("-" * 70 + "\n")
    for q in r2_questions:
        print_fn(f"\n❓ **{q.id}** - **{q.title}**:")
        print_fn(q.question_body)
        print_fn(f"\n➡️ 推荐方案: {q.recommended_answer}\n")
        try:
            user_in = input_fn("你的选择 [直接回车/yes采纳推荐方案, 或输入自定义偏好]: ").strip()
        except (EOFError, KeyboardInterrupt):
            user_in = ""

        if not user_in or user_in.lower() in ("yes", "y", "ok", "确认", "采纳"):
            r2_answers[q.id] = q.recommended_answer
        else:
            r2_answers[q.id] = user_in

    all_answers = {**r1_answers, **r2_answers}
    profile = session.build_parent_profile(all_answers)
    print_fn("\n" + "=" * 70)
    print_fn(
        f"✅ 家长画像对齐完毕: {profile.child_stage.value} | 目标学区: {profile.target_districts}"
    )
    print_fn(
        f"预算策略: {profile.budget_type.value} | 学术权重: {profile.priorities.academic_rigor:.2f} | 心理弹性: {profile.priorities.well_being_resilience:.2f}"
    )
    print_fn("=" * 70 + "\n")
    return profile
