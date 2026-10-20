---
name: seattle-school-radar
version: 1.0.0
description: |
  大西雅图地区 (Greater Seattle Area) 专属校园与升学智能雷达周报。
  基于多轮家长画像与 Matt Pocock 风格 Grill 决策树（孩子年龄、学区范围、教育理念与真实 Trade-off），
  精准调度官方学区(OSPI SBA/Equity/Feeder)、GreatSchools 深度剖析及小红书华人家长圈实况（经由 Chrome Bridge 真实人类行为反爬流），
  输出客观严谨的升学周报与决策建议。
metadata:
  author: OpenSource Community
  scope: Greater Seattle Area (King County & Southern Snohomish County)
  zero_pii_certified: true
  dependencies: [chrome-bridge, xiaohongshu-skill]
  tags: [seattle, school, parenting, k12, education, greatschools, ospi, xiaohongshu, radar, grill-me]
---

# 🌲 Seattle School Radar (大西雅图升学与校园情报雷达)

> **In-Scope 严格范围约定**：
> 本技能**仅限大西雅图核心区域**（King County 与南 Snohomish County，涵盖 Bellevue BSD 405、Lake Washington LWSD 414、Mercer Island MISD 400、Seattle SPS 314、Issaquah ISD 411、Northshore NSD 417 及区域内独立私立体系）。
> **明确排除**：华盛顿州其他边缘地区（Spokane, Vancouver, Tri-Cities, Bellingham）及外州。

---

## 🔒 零敏感信息承诺 (Zero PII Guarantee)

本技能设计为开源 GitHub 社区标准，**绝对禁止硬编码任何个人或家庭敏感数据**：
- 零个人身份（无姓名、住址、私人车辆或私人通讯录）；
- 零特定就读班级/私人师生沟通记录；
- 孩子年龄、学段及家庭偏好通过交互式 Grill 质询协议（或本地脱敏配置文件）动态注入。

---

## 🎯 核心交互机制：家长画像与 Grill 决策树 (Matt Pocock Grill Protocol)

当家长表达模糊（如“看口碑吧”、“想选个好学校”、“想孩子全面发展”）时，本技能强制挂载知名的 **Grill Protocol**，展开决策树前沿 (Frontier)，通过具体具象的现实矛盾与 Trade-off 进行深度对齐：

### 决策树 Frontier 结构
1. **Round 1 (硬性时间与学区边界)**:
   - 孩子当前多大？入学学段是 Infant/Toddler、Pre-K、还是 Kindergarten？
   - 考虑哪几个学区？（Bellevue BSD, Lake Washington LWSD, Issaquah ISD, Mercer Island, 或独立私立）
2. **Round 2 (教育理念与残酷现实 Trade-off - The Grill)**:
   - **学术压测 vs 心理弹性**: Somerset/Medina 90%+ 亚裔高压刷题 vs OWS/Newport Heights 探究式与社交情绪韧性，底线如何取舍？
   - **双语沉浸 vs 纯英文学术**: 景美小学 (Jing Mei) 50/50 抽签对高年级全英文学术词汇的挤出效应，是否可接受？
   - **家长时间卷度**: 双职工极度忙碌希望托管闭环，还是能每月投入 10-20 小时深度参与 PTSA 志愿与筹款？
   - **私立学费 ROI**: 每年 $35k-$55k 走读学费 vs 社区公立学区房地税溢价的量化算账。

> 💡 **设计准则**：每个 Grill 问题必须附带 **`➡️ (Recommended)` 推荐答案**，家长直接回复 `yes` 或按回车即可立即采纳推荐方案。

---

## 🌐 多源情报与 Chrome Bridge 反爬系统

### 1. 官方学网数据 (OSPI Washington State Report Card)
- 华州 SBA (Smarter Balanced Assessment) 数理、ELA、科学达标率；
- 学生进步百分比 (Student Growth Percentile, SGP)；
- 细分人群公平度 (Equity) 拆解，洞察“为什么得 9 分而非 10 分”。

### 2. 小红书华人家长圈实况采集 (RED Scraper)
- **环境依赖**: 必须依托真实的 Chrome 浏览器与 `chrome-bridge`，使用已有登录态；
- **拟人化反爬机制**:
  - `HumanJitter`: 高斯分布非等差随机停顿 (1.8s ~ 3.8s) + 随机阅读停顿；
  - `SmoothScroller`: 模拟鼠标滚轮 `wheel` 事件分段微调滚动，拒绝瞬间 `scrollTo`；
  - `RiskDetector`: 实时检测滑动拼图验证码、安全阻断弹窗与敏感提示，一旦触发立即熔断；
  - `RateLimiter`: 严格限制每分钟抓取频次，杜绝封号。

---

## 🛠️ CLI 命令与使用方式

```bash
# 1. 环境诊断：检查 Chrome Bridge、小红书登录态与核心学区数据
uv run seattle-school-radar doctor

# 1b. 环境诊断 + 分步安装指引（含 Chrome Bridge 与 grill-me 上游技能）
uv run seattle-school-radar doctor --setup

# 2. 启动交互式 Grill 质询（支持一键回车采纳推荐方案）
uv run seattle-school-radar grill

# 3. 查看大西雅图收录学校
uv run seattle-school-radar list-schools --district Bellevue

# 4. 生成完整周报（Markdown 详版，输出至控制台或指定文件）
uv run seattle-school-radar report --out reports/weekly_school_radar.md

# 5. 生成 Discord / IM 优化版键值流（移动端自适应，零错位表格）
uv run seattle-school-radar report --format discord
```

---

## 📐 Python 编程式调用

```python
from seattle_school_radar import GrillSession, SchoolRegistry, RadarReportBuilder, XHSRadarCrawler

# 1. 运行 Grill 决策
session = GrillSession()
profile = session.build_parent_profile(
    {
        "Q1_AGE_STAGE": "3-4 岁 Pre-K",
        "Q2_TARGET_DISTRICTS": "Bellevue (BSD 405)",
        "Q3_GRILL_RIGOR_VS_WELLBEING": "追求平衡型优质学术与健康成长",
        "Q4_GRILL_BILINGUAL_STRATEGY": "英文纯学术为主，家庭/课后课保留中文听说",
        "Q5_GRILL_PARENT_TIME_BUDGET": "双职工忙碌：需要完善的托管与独立闭环",
        "Q6_GRILL_FINANCIAL_ROI": "公私兼修：公立保底，择机冲刺顶级私校",
    }
)

# 2. 检索匹配学校
registry = SchoolRegistry()
matched = registry.filter_by_criteria(districts=profile.target_districts)

# 3. 采集小红书口碑并生成报告
crawler = XHSRadarCrawler()
crawler.connect_bridge()
insights = [crawler.search_school_buzz(s) for s in matched[:3]]

builder = RadarReportBuilder(profile, matched, insights)
markdown_report = builder.render_markdown()
discord_report = builder.render_discord_kv_stream()
```

---

## 🔗 Reference Links

- Matt Pocock grill-me (upstream agent skill): https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me
- Chrome Bridge / Xiaohongshu skill: https://github.com/shuyuanshi/xiaohongshu-skill

Built-in Matt Pocock Grill Engine works standalone. Agent users may optionally install the upstream skill via `npx skills add mattpocock/skills/productivity/grill-me`.
