"""School Registry: High-fidelity database of Greater Seattle Area schools.

Scope: Greater Seattle Area (King County & Southern Snohomish County).
Zero PII guarantee: Contains only publicly verifiable school data, academic performance metrics,
OSPI Washington State Report Card indicators, GreatSchools analytics, and district transfer policies.
"""

from __future__ import annotations

import re
from typing import Iterable

from seattle_school_radar.models import OSPIMetrics, SchoolRecord

SEATTLE_SCHOOLS_DATABASE: list[SchoolRecord] = [
    # -------------------------------------------------------------
    # Bellevue School District (BSD 405)
    # -------------------------------------------------------------
    SchoolRecord(
        id="newport_heights",
        name="Newport Heights Elementary",
        name_cn="纽波特高地小学 (Newport Heights)",
        district="Bellevue School District (BSD 405)",
        category="Public Community / Dual-Language Track",
        grades="K-5",
        city="Bellevue",
        gs_rating="9/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=75.6,
            ela_proficiency_pct=73.8,
            science_proficiency_pct=80.2,
            state_rank_percentile=6.5,
            student_growth_percentile=58.0,
            diversity_index=0.68,
        ),
        feeder_pathway="Tyee Middle School -> Newport High School",
        why_score=(
            "【评分深度拆解】：纯学术测试稳居全华州前 6.5%，学生成长指数 (Student Progress) 达 8/10。"
            "兼收常规社区学生、韩语双语与 PACIFIC 融合教学，生源多元化程度高于纯亚裔集中校。"
            "在 GreatSchools 的 Equity（弱势群体公平度）维度略受生源异质性拉平，但综合学术实力极为稳固。"
        ),
        curriculum_style="Balanced Academic & Inclusive Leadership",
        transfer_lottery_status="BSD Procedure 3141P 跨区开放申请（每年1-2月窗口，部分年级有可用容量）",
        annual_tuition="Free (Public)",
        key_tags=["BSD", "NewportFeeder", "DualLanguageTrack", "BalancedExcellence", "Public"],
    ),
    SchoolRecord(
        id="somerset_elem",
        name="Somerset Elementary",
        name_cn="萨默塞特小学 (Somerset)",
        district="Bellevue School District (BSD 405)",
        category="Public Academic Powerhouse / Prism Gifted",
        grades="K-5",
        city="Bellevue",
        gs_rating="10/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=88.4,
            ela_proficiency_pct=86.2,
            science_proficiency_pct=91.5,
            state_rank_percentile=1.2,
            student_growth_percentile=65.0,
            diversity_index=0.45,
        ),
        feeder_pathway="Tyee Middle School -> Newport High School",
        why_score=(
            "【评分深度拆解】：全华州排名前 1.5% 的学术天花板。驻扎 BSD Prism 天才班项目，"
            "亚裔与高科技家庭生源比例极高，SBA 标准化考试数理达标率逼近 90%。"
            "高学术输出的代价是课外补习密度极高、同侪竞争压力 (Peer Pressure) 显著。"
        ),
        curriculum_style="High-Intensity Academic Rigor & Accelerated Math",
        transfer_lottery_status="常年容量饱满 (Overcrowded)，跨区申请难度极高",
        annual_tuition="Free (Public)",
        key_tags=["BSD", "PrismGifted", "AcademicSuperstar", "HighPeerPressure", "Public"],
    ),
    SchoolRecord(
        id="medina_elem",
        name="Medina Elementary",
        name_cn="麦地那小学 (Medina)",
        district="Bellevue School District (BSD 405)",
        category="Public Community High-Wealth",
        grades="K-5",
        city="Medina",
        gs_rating="10/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=85.2,
            ela_proficiency_pct=84.9,
            science_proficiency_pct=89.0,
            state_rank_percentile=2.1,
            student_growth_percentile=62.0,
            diversity_index=0.52,
        ),
        feeder_pathway="Chinook Middle School -> Bellevue High School",
        why_score=(
            "【评分深度拆解】：坐拥全美顶级高净值居住区生源，家委会筹款极其丰沛，全职教辅配比充裕。"
            "兼具顶级学术成绩与完善的体育、马术、管弦乐等高端课外生态。"
        ),
        curriculum_style="Traditional Rigor with Elite Enrichment",
        transfer_lottery_status="学区内严格对口，极少释放跨区名额",
        annual_tuition="Free (Public)",
        key_tags=["BSD", "BellevueHighFeeder", "TopTierWealth", "CommunitySupport", "Public"],
    ),
    SchoolRecord(
        id="jing_mei_elem",
        name="Jing Mei Elementary",
        name_cn="景美小学 (Jing Mei)",
        district="Bellevue School District (BSD 405)",
        category="Public Choice / Mandarin Dual Language",
        grades="K-5",
        city="Bellevue",
        gs_rating="9/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=78.1,
            ela_proficiency_pct=76.5,
            science_proficiency_pct=82.0,
            state_rank_percentile=5.0,
            student_growth_percentile=60.0,
            diversity_index=0.58,
        ),
        feeder_pathway="Highland Middle School (Dual Immersion) -> Interlake High School",
        why_score=(
            "【评分深度拆解】：大西雅图公立唯一的 50/50 沉浸式中文双语 Choice 小学。"
            "从 Kindergarten 开始中英半日交替授课，数学以中文为教学语言。全华州学术排名前 5%。"
            "抽签制入学，全西雅图华人家长极高关注度。"
        ),
        curriculum_style="Mandarin Dual Language Immersion (50/50 Model)",
        transfer_lottery_status="每年 1 月开放 BSD Choice 摇号抽签（跨学区居民亦可申请，但学区内居民优先池）",
        annual_tuition="Free (Public Choice)",
        key_tags=["BSD", "MandarinImmersion", "ChoiceLottery", "Bilingual", "PublicChoice"],
    ),
    # -------------------------------------------------------------
    # Lake Washington School District (LWSD 414)
    # -------------------------------------------------------------
    SchoolRecord(
        id="tesla_stem_high",
        name="Tesla STEM High School",
        name_cn="特斯拉理工高中 (Tesla STEM)",
        district="Lake Washington School District (LWSD 414)",
        category="Public Choice Magnet (Grades 9-12)",
        grades="9-12",
        city="Redmond",
        gs_rating="10/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=92.5,
            ela_proficiency_pct=91.0,
            science_proficiency_pct=95.2,
            state_rank_percentile=0.5,
            student_growth_percentile=70.0,
            diversity_index=0.60,
        ),
        feeder_pathway="LWSD Choice High School (Application/Lottery)",
        why_score=(
            "【评分深度拆解】：全美公立高中前 20 名常客。项目制 (PBL) 深入对接微软/亚马逊/波音科研导师，"
            "提供神经科学、太空探索、自动化机器人等研究生级别实验室先修，AP 满分率极高。"
        ),
        curriculum_style="Project-Based STEM, Engineering & Biomedical Research",
        transfer_lottery_status="每年 12月-1月全学区 8 年级学生申请抽签",
        annual_tuition="Free (Public Magnet)",
        key_tags=["LWSD", "STEMMagnet", "Top20Nationwide", "ResearchPBL", "PublicChoice"],
    ),
    SchoolRecord(
        id="rockwell_elem",
        name="Norman Rockwell Elementary",
        name_cn="诺曼罗克韦尔小学 (Rockwell)",
        district="Lake Washington School District (LWSD 414)",
        category="Public Community High-Achieving",
        grades="K-5",
        city="Redmond",
        gs_rating="10/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=84.7,
            ela_proficiency_pct=83.5,
            science_proficiency_pct=88.6,
            state_rank_percentile=3.0,
            student_growth_percentile=64.0,
            diversity_index=0.62,
        ),
        feeder_pathway="Redmond Middle School -> Redmond High School",
        why_score=(
            "【评分深度拆解】：雷德蒙德 (Redmond) 微软园区核心腹地公立顶流。"
            "数理表现极度稳固，家委会活跃，校风积极向上，科学展与数学俱乐部参与度高。"
        ),
        curriculum_style="Strong Standardized Curriculum & Math Enrichment",
        transfer_lottery_status="学区内 Variance / 跨区申请视空余学位动态评审",
        annual_tuition="Free (Public)",
        key_tags=["LWSD", "RedmondCore", "STEMFriendly", "TopPublic", "Public"],
    ),
    # -------------------------------------------------------------
    # Issaquah School District (ISD 411)
    # -------------------------------------------------------------
    SchoolRecord(
        id="newcastle_elem",
        name="Newcastle Elementary",
        name_cn="纽卡斯尔小学 (Newcastle Elementary)",
        district="Issaquah School District (ISD 411)",
        category="Public Community Top-Tier",
        grades="K-5",
        city="Newcastle",
        gs_rating="9/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=79.8,
            ela_proficiency_pct=75.4,
            science_proficiency_pct=88.2,
            state_rank_percentile=7.8,
            student_growth_percentile=61.0,
            diversity_index=0.65,
        ),
        feeder_pathway="Maywood Middle School -> Liberty High School",
        why_score=(
            "【评分深度拆解】：依托高尔夫球场与东侧山林社区的高素质科技中产生源，"
            "科学科目达标率高达 88.2%，家委会募捐强劲，社区环境安全优雅，整体氛围健康均衡。"
        ),
        curriculum_style="Balanced Whole-Child & Strong Science Inquiry",
        transfer_lottery_status="每年 2 月开放 ISD Choice / Inter-District Transfer 申请",
        annual_tuition="Free (Public)",
        key_tags=["ISD", "Newcastle", "BalancedExcellence", "SafeCommunity", "Public"],
    ),
    # -------------------------------------------------------------
    # Mercer Island School District (MISD 400)
    # -------------------------------------------------------------
    SchoolRecord(
        id="lakeridge_elem",
        name="Lakeridge Elementary",
        name_cn="湖脊小学 (Lakeridge)",
        district="Mercer Island School District (MISD 400)",
        category="Public Community Island-Exclusive",
        grades="K-5",
        city="Mercer Island",
        gs_rating="9/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=81.3,
            ela_proficiency_pct=82.0,
            science_proficiency_pct=86.5,
            state_rank_percentile=4.5,
            student_growth_percentile=59.0,
            diversity_index=0.55,
        ),
        feeder_pathway="Islander Middle School -> Mercer Island High School",
        why_score=(
            "【评分深度拆解】：默瑟岛 (Mercer Island) 独立学区标杆。生源极度纯粹且稳定，"
            "从小学到高中形成闭环，师生比极佳，艺术与体育资源丰沛，几乎无恶性恶性竞争。"
        ),
        curriculum_style="Supportive Community & High-Trust Learning",
        transfer_lottery_status="除岛上全职教职工子女外，对外跨区几乎零名额",
        annual_tuition="Free (Public)",
        key_tags=["MISD", "MercerIsland", "SafeIsland", "HighWealth", "Public"],
    ),
    # -------------------------------------------------------------
    # Seattle Public Schools (SPS 314)
    # -------------------------------------------------------------
    SchoolRecord(
        id="cascadia_elem",
        name="Cascadia Elementary",
        name_cn="卡斯卡迪亚资优小学 (Cascadia)",
        district="Seattle Public Schools (SPS 314)",
        category="Public Highly Capable (HCC) Magnet",
        grades="1-5",
        city="Seattle",
        gs_rating="10/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=89.5,
            ela_proficiency_pct=91.2,
            science_proficiency_pct=92.0,
            state_rank_percentile=1.0,
            student_growth_percentile=66.0,
            diversity_index=0.55,
        ),
        feeder_pathway="Robert Eagle Staff Middle (HCC) -> Lincoln High / Garfield High",
        why_score=(
            "【评分深度拆解】：西雅图学区公立资优 (HCC) 旗舰小学。全员通过 Cognitive Abilities Test (CogAT) 达标入读，"
            "全科先修超前 1-2 年级教学，学术表现居西雅图公立榜首。"
        ),
        curriculum_style="Accelerated Gifted Curriculum (HCC Track)",
        transfer_lottery_status="需通过 SPS 统一 CogAT 资优资质鉴定后入读",
        annual_tuition="Free (Public)",
        key_tags=["SPS", "Cascadia", "HCCGifted", "SeattlePublic", "Public"],
    ),
    SchoolRecord(
        id="garfield_high",
        name="Garfield High School",
        name_cn="加菲尔德高中 (Garfield)",
        district="Seattle Public Schools (SPS 314)",
        category="Public Comprehensive & HCC High",
        grades="9-12",
        city="Seattle",
        gs_rating="8/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=68.5,
            ela_proficiency_pct=78.2,
            science_proficiency_pct=72.0,
            state_rank_percentile=15.0,
            student_growth_percentile=55.0,
            diversity_index=0.78,
        ),
        feeder_pathway="Washington Middle / Eagle Staff Middle -> Garfield High",
        why_score=(
            "【评分深度拆解】：西雅图历史最悠久的综合公立高中。驻扎全学区 HCC 资优项目、全美顶尖爵士乐团与管弦乐团。"
            "常春藤录取亮眼，但因全校生源极度两极分化（普通班 vs HCC/AP 班），总分被综合指标拉平，需认清其 AP 班生态。"
        ),
        curriculum_style="Rigorous AP & Internationally Acclaimed Jazz/Arts",
        transfer_lottery_status="SPS 每年 2 月 Open Enrollment 申请",
        annual_tuition="Free (Public)",
        key_tags=["SPS", "Garfield", "HCCFeeder", "JazzMusic", "Public"],
    ),
    # -------------------------------------------------------------
    # Northshore School District (NSD 417)
    # -------------------------------------------------------------
    SchoolRecord(
        id="north_creek_high",
        name="North Creek High School",
        name_cn="北溪高中 (North Creek)",
        district="Northshore School District (NSD 417)",
        category="Public Comprehensive STEM High",
        grades="9-12",
        city="Bothell",
        gs_rating="9/10",
        ospi_metrics=OSPIMetrics(
            math_proficiency_pct=76.8,
            ela_proficiency_pct=81.0,
            science_proficiency_pct=83.5,
            state_rank_percentile=8.0,
            student_growth_percentile=60.0,
            diversity_index=0.64,
        ),
        feeder_pathway="Skyview Middle School -> North Creek High",
        why_score=(
            "【评分深度拆解】：北岸学区 (Northshore) 新建高科技标杆高中。校舍现代感十足，"
            "重点对接生物医药与工程类先修课程，吸引大量 Bothell 科技走廊家庭入驻。"
        ),
        curriculum_style="Modern STEM Collaboration & AP Acceleration",
        transfer_lottery_status="NSD 学区内 Choice/Waiver 申请",
        annual_tuition="Free (Public)",
        key_tags=["NSD", "NorthCreek", "Bothell", "ModernSTEM", "Public"],
    ),
    # -------------------------------------------------------------
    # Top Independent Private Schools (大西雅图顶级私立)
    # -------------------------------------------------------------
    SchoolRecord(
        id="lakeside_school",
        name="Lakeside School",
        name_cn="湖滨学校 (Lakeside)",
        district="Independent Private",
        category="Elite Independent Day School (5-12)",
        grades="5-12",
        city="Seattle",
        gs_rating="N/A (Private Elite)",
        ospi_metrics=None,
        feeder_pathway="Lakeside Middle (5-8) -> Lakeside Upper (9-12)",
        why_score=(
            "【顶私深度剖析】：全美前 3 顶尖走读私立，比尔·盖茨母校。常春藤及美本 T20 录取率超 30%。"
            "以苏格拉底研讨法、深度独立科研课题与全球公民领导力著称。录取率约 12-15%，竞争极度白热化。"
        ),
        curriculum_style="Socratic Seminar, Rigorous Humanities & Global Leadership",
        transfer_lottery_status="每年 11月-1月通过 Ravenna 网申，需 ISEE/SSAT 与深度家庭面试",
        annual_tuition="$46,000 - $49,000",
        key_tags=["ElitePrivate", "Lakeside", "IvyLeagueFeeder", "Top1InWA", "Private"],
    ),
    SchoolRecord(
        id="the_overlake_school",
        name="The Overlake School",
        name_cn="欧弗莱克私立学校 (Overlake)",
        district="Independent Private",
        category="Elite Independent Day School (5-12)",
        grades="5-12",
        city="Redmond",
        gs_rating="N/A (Private Elite)",
        ospi_metrics=None,
        feeder_pathway="Overlake Middle (5-8) -> Overlake Upper (9-12)",
        why_score=(
            "【顶私深度剖析】：坐落于 Redmond 75 英亩生态森林校园。兼备极高的 STEM 理科研究能力与人文学术，"
            "注重体验式户外教学 (Project Week) 与学生心理健康。西雅图科技精英家庭私立首选之一。"
        ),
        curriculum_style="Project-Based, Outdoor Experiential & Rigorous STEM",
        transfer_lottery_status="每年 1月 Ravenna 截止，主要招生年级为 Grade 5 与 Grade 9",
        annual_tuition="$45,000 - $48,000",
        key_tags=["ElitePrivate", "Overlake", "75AcreCampus", "STEMHumanities", "Private"],
    ),
    SchoolRecord(
        id="open_window_school",
        name="Open Window School",
        name_cn="开窗学校 (Open Window / OWS)",
        district="Independent Private",
        category="Gifted Independent Day School (K-8)",
        grades="K-8",
        city="Bellevue",
        gs_rating="N/A (Private Gifted)",
        ospi_metrics=None,
        feeder_pathway="出口直通 Lakeside, Overlake, EPS, Seattle Academy 等顶私或顶级公立高",
        why_score=(
            "【顶私深度剖析】：华盛顿州唯一一家专门针对资优/天才儿童 (Gifted/Talented) 的独立私立学校。"
            "坐落于 Cougar Mountain 山麓，入学需提供专业 IQ 心理评测 (WISC-V 或 WPPSI-IV，需达 130+ 阈值)。"
            "重在因材施教满足孩子超常智力渴望，同时深度强化社交情绪韧性 (Social-Emotional Learning)。"
        ),
        curriculum_style="Accelerated Inquiry & Social-Emotional Learning for Gifted Minds",
        transfer_lottery_status="每年 1 月 Ravenna 申请截止，需 IQ 测试报告及入校综合观察日",
        annual_tuition="$36,000 - $41,000",
        key_tags=["GiftedPrivate", "OWS", "CougarMountain", "SocialEmotional", "Private"],
    ),
    SchoolRecord(
        id="bellevue_childrens_academy",
        name="Bellevue Children's Academy (BCA)",
        name_cn="贝尔维尤少儿学院 (BCA)",
        district="Independent Private",
        category="IB PYP Accelerated Private (Pre-K-8)",
        grades="Pre-K-8",
        city="Bellevue",
        gs_rating="N/A (Private Accelerated)",
        ospi_metrics=None,
        feeder_pathway="直升兄弟学校 Willows Preparatory School (WPS / IB MYP & DP)",
        why_score=(
            "【学术私立剖析】：严格执行 IB Primary Years Programme (PYP) 框架。"
            "数学超前先修 1-2 年级，学术进度快，课后拓展充实。深受重视学术扎实度与严谨纪律的东区科技家庭青睐。"
        ),
        curriculum_style="IB PYP Framework with Rigorous Math Acceleration",
        transfer_lottery_status="滚动招生 (Rolling Admissions) 结合年级空位，需学生入园评估",
        annual_tuition="$24,000 - $28,000",
        key_tags=["IBPYP", "BCA", "MathAcceleration", "BellevuePrivate", "Private"],
    ),
    SchoolRecord(
        id="cedar_crest_academy",
        name="Cedar Crest Academy (CCA)",
        name_cn="雪松冠学院 (CCA)",
        district="Independent Private",
        category="Traditional Accelerated Private (Pre-K-5)",
        grades="Pre-K-5",
        city="Bellevue / Kirkland / Redmond",
        gs_rating="N/A (Private)",
        ospi_metrics=None,
        feeder_pathway="5 年级毕业广泛考入 Lakeside, Overlake, OWS 或转入顶级公立 Prism/Quest",
        why_score=(
            "【传统私立剖析】：东区拥有 4 个校区的小班精品私立。侧重早期阅读、拼写和传统扎实数学训练。"
            "师生比通常 1:8 到 1:12，纪律好，适合希望低龄阶段打下绝对严密基本功的家庭。"
        ),
        curriculum_style="Traditional Mastery, Phonics & Direct Instruction",
        transfer_lottery_status="每年 12月-2月开放下学年学位预订，先到先审",
        annual_tuition="$21,000 - $25,000",
        key_tags=["CCA", "SmallClass", "PhonicsMastery", "EastsideCampuses", "Private"],
    ),
    SchoolRecord(
        id="eastside_prep",
        name="Eastside Preparatory School (EPS)",
        name_cn="东区预科学校 (Eastside Prep / EPS)",
        district="Independent Private",
        category="Innovative Independent (5-12)",
        grades="5-12",
        city="Kirkland",
        gs_rating="N/A (Private)",
        ospi_metrics=None,
        feeder_pathway="Middle School (5-8) -> Upper School (9-12)",
        why_score=(
            "【创新私立剖析】：Kirkland 毗邻科技走廊的新晋顶尖独立私立。强调批判性思维、跨学科科研与设计思维。"
            "高中部升学走势迅猛，硬件设施极具现代感，深受西雅图新一代年轻科技新贵欢迎。"
        ),
        curriculum_style="Interdisciplinary Design Thinking & Scientific Inquiry",
        transfer_lottery_status="1 月 Ravenna 申请截止，考查学生创造力与沟通表达",
        annual_tuition="$44,000 - $47,000",
        key_tags=["EPS", "Kirkland", "DesignThinking", "ModernPrivate", "Private"],
    ),
    SchoolRecord(
        id="the_bush_school",
        name="The Bush School",
        name_cn="布什学校 (The Bush School)",
        district="Independent Private",
        category="Progressive Independent Day (K-12)",
        grades="K-12",
        city="Seattle",
        gs_rating="N/A (Private)",
        ospi_metrics=None,
        feeder_pathway="Lower School -> Middle School -> Upper School",
        why_score=(
            "【进步主义私立剖析】：西雅图唯一一家位于市区的 K-12 进步主义独立私校。"
            "注重体验式学习、户外教育 (AMP/Cascade) 与社会责任，极其强调学生心理健康与自由探究。"
        ),
        curriculum_style="Progressive Experiential & Inquiry-Based",
        transfer_lottery_status="1 月通过 Ravenna 统一截止",
        annual_tuition="$42,000 - $48,000",
        key_tags=["BushSchool", "Progressive", "K12Private", "SeattlePrivate", "Private"],
    ),
    SchoolRecord(
        id="seattle_country_day",
        name="Seattle Country Day School (SCDS)",
        name_cn="西雅图乡村走读学校 (SCDS)",
        district="Independent Private",
        category="Inquiry Gifted Day School (K-8)",
        grades="K-8",
        city="Seattle",
        gs_rating="N/A (Private Gifted)",
        ospi_metrics=None,
        feeder_pathway="毕业生广泛考入 Lakeside, UPrep, SAAS, Bush 或顶级公立高",
        why_score=(
            "【探究型资优剖析】：Queen Anne 山麓专注资优儿童的 K-8 私立。强调探究式学习 (Inquiry for Inquiry's Sake)，"
            "需 IQ 认知评估报告。校风相较 OWS 更偏向人文与自由探索。"
        ),
        curriculum_style="Inquiry-Based Gifted Acceleration",
        transfer_lottery_status="1 月申请截止，需 IQ 测试与入园观察",
        annual_tuition="$37,000 - $41,000",
        key_tags=["SCDS", "Gifted", "QueenAnne", "Inquiry", "Private"],
    ),
    SchoolRecord(
        id="epiphany_school",
        name="Epiphany School",
        name_cn="显圣学校 (Epiphany School)",
        district="Independent Private",
        category="Independent Early Elementary (Pre-K-5)",
        grades="Pre-K-5",
        city="Seattle",
        gs_rating="N/A (Private)",
        ospi_metrics=None,
        feeder_pathway="毕业生广泛升入 Lakeside, Overlake, SAAS, Bush, UPrep",
        why_score=(
            "【精品低龄私立剖析】：坐落于 Madrona 的百年历史精致小学。高度注重早期品格培养、关爱社区与扎实阅读习惯。"
            "校园精致紧凑，师生关系温暖亲密，被誉为通往西雅图顶尖中学的黄金跳板。"
        ),
        curriculum_style="Nurturing Academic & Character Development",
        transfer_lottery_status="1 月统一申请截止",
        annual_tuition="$32,000 - $36,000",
        key_tags=["Epiphany", "PreK5", "Madrona", "CharacterEducation", "Private"],
    ),
]


class SchoolRegistry:
    """Registry query interface for Greater Seattle schools with strict boundary separation."""

    # Explicit mapping of district codes to full district identifiers
    DISTRICT_CODE_MAP = {
        "bsd": "Bellevue School District (BSD 405)",
        "bsd 405": "Bellevue School District (BSD 405)",
        "bellevue": "Bellevue School District (BSD 405)",
        "lwsd": "Lake Washington School District (LWSD 414)",
        "lwsd 414": "Lake Washington School District (LWSD 414)",
        "lake washington": "Lake Washington School District (LWSD 414)",
        "isd": "Issaquah School District (ISD 411)",
        "isd 411": "Issaquah School District (ISD 411)",
        "issaquah": "Issaquah School District (ISD 411)",
        "misd": "Mercer Island School District (MISD 400)",
        "misd 400": "Mercer Island School District (MISD 400)",
        "mercer island": "Mercer Island School District (MISD 400)",
        "sps": "Seattle Public Schools (SPS 314)",
        "sps 314": "Seattle Public Schools (SPS 314)",
        "seattle public": "Seattle Public Schools (SPS 314)",
        "seattle (sps 314)": "Seattle Public Schools (SPS 314)",
        "nsd": "Northshore School District (NSD 417)",
        "nsd 417": "Northshore School District (NSD 417)",
        "northshore": "Northshore School District (NSD 417)",
        "private": "Independent Private",
        "independent private": "Independent Private",
        "top private": "Independent Private",
    }

    def __init__(self, schools: list[SchoolRecord] | None = None) -> None:
        self._schools = schools or list(SEATTLE_SCHOOLS_DATABASE)

    def list_all(self) -> list[SchoolRecord]:
        return list(self._schools)

    def get_by_id(self, school_id: str) -> SchoolRecord | None:
        for s in self._schools:
            if s.id == school_id:
                return s
        return None

    def search_by_district(self, district_keyword: str) -> list[SchoolRecord]:
        kw = district_keyword.lower().strip()
        matched_official = self.DISTRICT_CODE_MAP.get(kw)
        if matched_official:
            return [s for s in self._schools if s.district == matched_official]
        return [s for s in self._schools if kw in s.district.lower()]

    def filter_by_criteria(
        self,
        districts: Iterable[str] | None = None,
        grades: str | None = None,
        max_tuition: float | None = None,
    ) -> list[SchoolRecord]:
        results = list(self._schools)

        if districts:

            def matches_district_strictly(record: SchoolRecord, raw_target: str) -> bool:
                cleaned = raw_target.lower().strip()
                # 1. Check exact map lookup
                if cleaned in self.DISTRICT_CODE_MAP:
                    return record.district == self.DISTRICT_CODE_MAP[cleaned]

                # 2. Check for district codes
                if "bsd" in cleaned:
                    return "BSD 405" in record.district
                if "lwsd" in cleaned or "lake washington" in cleaned:
                    return "LWSD 414" in record.district
                if "isd" in cleaned or "issaquah" in cleaned:
                    return "ISD 411" in record.district
                if "misd" in cleaned or "mercer island" in cleaned:
                    return "MISD 400" in record.district
                if "sps" in cleaned or "seattle public" in cleaned:
                    return "SPS 314" in record.district
                if "nsd" in cleaned or "northshore" in cleaned:
                    return "NSD 417" in record.district
                if "private" in cleaned or "私立" in cleaned:
                    return record.district == "Independent Private"

                # 3. Direct district substring check (strictly on record.district, NOT record.name or record.city)
                return cleaned in record.district.lower()

            results = [
                s for s in results if any(matches_district_strictly(s, d) for d in districts)
            ]

        if grades:
            results = [s for s in results if grades.lower() in s.grades.lower()]

        if max_tuition is not None:

            def extract_max_tuition(tuition_str: str | None) -> float:
                if not tuition_str or "free" in tuition_str.lower():
                    return 0.0
                matches = re.findall(r"[\$]?(\d{1,3}(?:,\d{3})*)", tuition_str)
                if matches:
                    nums = [float(m.replace(",", "")) for m in matches]
                    return max(nums)
                return 0.0

            results = [s for s in results if extract_max_tuition(s.annual_tuition) <= max_tuition]

        return results
