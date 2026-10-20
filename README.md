# 🌲 Seattle School Radar (大西雅图升学与校园情报雷达)

[![CI](https://github.com/shuyuanshi/seattle-school-radar/actions/workflows/ci.yml/badge.svg)](https://github.com/shuyuanshi/seattle-school-radar/actions)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![Agent Skill](https://img.shields.io/badge/Agent_Skill-Antigravity%20%7C%20Claude-purple.svg)](SKILL.md)

An open-source, production-ready AI Agent Skill and CLI tool dedicated to **Greater Seattle Area K-12 education and school admissions intelligence**.

Built specifically for Seattle parents navigating the complex landscape of public community schools, choice lotteries, gifted programs, and top independent private academies.

---

## 🎯 Scope & Boundaries (严格区域约定)

- **In-Scope**: **Greater Seattle Area** (King County & Southern Snohomish County)
  - Public School Districts:
    * Bellevue School District (BSD 405)
    * Lake Washington School District (LWSD 414)
    * Mercer Island School District (MISD 400)
    * Issaquah School District (ISD 411)
    * Seattle Public Schools (SPS 314)
    * Northshore School District (NSD 417)
  - Elite Independent Private Schools:
    * Lakeside School, The Overlake School, Eastside Prep (EPS)
    * Open Window School (OWS - Gifted K-8)
    * Bellevue Children's Academy (BCA - IB PYP), Cedar Crest Academy (CCA)
    * Bush School, Seattle Academy (SAAS), Seattle Country Day (SCDS), Epiphany
- **Out-of-Scope**: Out-of-state schools and non-Seattle WA regions (Spokane, Vancouver, Tri-Cities, Bellingham).

---

## 🔒 Zero PII Guarantee (零敏感信息保证)

This project contains **zero hardcoded private or personal identifiable information (Zero PII)**:
- No personal names, residential addresses, private license plates, or specific class schedules.
- Child age, stage, and family preferences are dynamically queried through the **Grill Protocol** or provided via local untracked config files.

---

## 💡 Key Architectural Pillars

### 1. Matt Pocock Grill Protocol (家长决策树剪枝协议)
When parents express vague or conflicting preferences (e.g. *"I just want a well-rounded good school"*), the agent relentlessly grills through key trade-offs:
* **Academic Rigor vs. Mental Well-being**: Somerset's 90%+ Asian math pressure vs. OWS/Newport Heights inquiry.
* **Bilingual Immersion vs. English Depth**: Jing Mei Mandarin 50/50 lottery vs. conventional STEM accelerated tracks.
* **Parent Involvement Budget**: Dual-career busy families vs. 10-20 hrs/mo heavy PTSA volunteering.
* **Financial ROI**: $38k-$50k/year private tuition vs. public property tax premiums.

*Every question is paired with an AI-recommended answer (`➡️ (Recommended)`), allowing one-key confirmation (`yes` or Enter).*

### 2. Chrome Bridge & Human-like Xiaohongshu (RED) Anti-Scraping
- **Real Chrome Profile**: Operates through active Chrome Bridge to maintain logged-in status.
- **Human Jitter**: Gaussian-distributed pauses (1.8s - 3.8s) + natural reading contemplation pauses.
- **Smooth Scroller**: Incremental wheel-event scrolling, completely avoiding bot-triggering instant jumps.
- **Risk Detector**: Proactively senses slider CAPTCHAs and security warnings, instantly halting to safeguard accounts.

### 3. Washington State Report Card (OSPI) & GreatSchools Analytics
- Decodes SBA Math, ELA, and Science proficiency against state averages.
- Explains *"Why this score"* (e.g. why a school scored 9/10 instead of 10/10 due to diverse inclusion rather than academic decline).

---

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/shuyuanshi/seattle-school-radar.git
cd seattle-school-radar

# Install dependencies using uv
uv sync
```

### Usage

```bash
# 1. Check system and Chrome Bridge dependencies
uv run seattle-school-radar doctor

# 1b. Check dependencies with step-by-step setup guide
uv run seattle-school-radar doctor --setup

# 2. Start an interactive Grill session
uv run seattle-school-radar grill

# 3. List indexed Greater Seattle schools
uv run seattle-school-radar list-schools --district Bellevue

# 4. Generate the full Markdown weekly intelligence report
uv run seattle-school-radar report --out weekly_radar.md

# 5. Output Discord/IM mobile-safe Key-Value stream (zero breaking tables)
uv run seattle-school-radar report --format discord
```

---

## 🧪 Testing & CI

```bash
# Run tests
uv run pytest tests/ -v

# Run linter
uv run ruff check .

# Run type checker
uv run basedpyright
```

---

## 🔗 Reference Links

- Matt Pocock grill-me (upstream agent skill): https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me
- Chrome Bridge / Xiaohongshu skill: https://github.com/shuyuanshi/xiaohongshu-skill

The built-in Matt Pocock Grill Engine works standalone. The upstream grill-me skill is optional for agent users (`npx skills add mattpocock/skills/productivity/grill-me`).

---

## 📄 License

MIT License. See [LICENSE](LICENSE) for details.
