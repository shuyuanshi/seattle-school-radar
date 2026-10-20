"""Command Line Interface for Seattle School Radar."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

import yaml

from seattle_school_radar.grill_engine import execute_interactive_grill
from seattle_school_radar.models import (
    BudgetType,
    ChildStage,
    EducationalPriority,
    ParentProfile,
)
from seattle_school_radar.report_builder import RadarReportBuilder
from seattle_school_radar.school_registry import SchoolRegistry
from seattle_school_radar.xhs_radar import XHSRadarCrawler

GRILL_ME_UPSTREAM_URL = (
    "https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me"
)
GRILL_ME_ADD_COMMAND = "npx skills add mattpocock/skills/productivity/grill-me"
XIAOHONGSHU_SKILL_URL = "https://github.com/shuyuanshi/xiaohongshu-skill"
XIAOHONGSHU_SKILL_CLONE_COMMAND = "git clone https://github.com/shuyuanshi/xiaohongshu-skill.git ~/.chrome-bridge/xiaohongshu-skill"

GRILL_ME_CANDIDATE_DIRS = (
    Path(".agents/skills/grill-me"),
    Path(".agents/skills/grilling"),
    Path("skills/grill-me"),
    Path("skills/grilling"),
)


def find_upstream_grill_skill(
    cwd: Path | None = None,
    home: Path | None = None,
) -> Path | None:
    """Locate an external grill-me/grilling skill folder if installed."""
    base = cwd if cwd is not None else Path.cwd()
    candidates: list[Path] = []
    for relative in GRILL_ME_CANDIDATE_DIRS:
        candidates.append(base / relative)
    home_base = home if home is not None else Path.home()
    candidates.append(home_base / ".agents" / "skills" / "grill-me")
    candidates.append(home_base / ".agents" / "skills" / "grilling")
    for candidate in candidates:
        try:
            if candidate.is_dir():
                return candidate
        except OSError:
            continue
    return None


def print_setup_guide() -> None:
    """Print step-by-step setup instructions for optional dependencies."""
    print("\n🛠️  Automated Setup Guide (--setup):")
    print("\n[1/2] Chrome Bridge / Xiaohongshu login:")
    print(f"  Repository: {XIAOHONGSHU_SKILL_URL}")
    print(f"  Clone command: {XIAOHONGSHU_SKILL_CLONE_COMMAND}")
    print("  Step 1: Install dependencies per the repository README.")
    print("  Step 2: Load the unpacked extension in chrome://extensions.")
    print("  Step 3: Open xiaohongshu.com in Chrome and scan the QR code to log in.")
    try:
        if sys.stdin.isatty():
            answer = input("Clone the Xiaohongshu skill repository now? [y/N]: ").strip().lower()
            if answer in ("y", "yes"):
                target = Path.home() / ".chrome-bridge" / "xiaohongshu-skill"
                if target.exists():
                    print(f"Target already exists: {target} (skipping clone).")
                else:
                    target.parent.mkdir(parents=True, exist_ok=True)
                    subprocess.run(
                        [
                            "git",
                            "clone",
                            "https://github.com/shuyuanshi/xiaohongshu-skill.git",
                            str(target),
                        ],
                        check=True,
                    )
                    print(f"✅ Cloned into {target}")
    except (EOFError, KeyboardInterrupt, subprocess.CalledProcessError, OSError) as e:
        print(f"⚠️ Clone skipped or failed ({e}). Run manually:")
        print(f"  {XIAOHONGSHU_SKILL_CLONE_COMMAND}")
    print("\n[2/2] Upstream grill-me agent skill (optional):")
    print("  Built-in Matt Pocock Grill Engine already works standalone; no install required.")
    print("  For agent users who want the upstream skill:")
    print(f"  Option A: {GRILL_ME_ADD_COMMAND}")
    print(
        "  Option B: git clone https://github.com/mattpocock/skills.git "
        "and install skills/productivity/grill-me"
    )
    print(f"  Upstream reference: {GRILL_ME_UPSTREAM_URL}")


def run_doctor(*, setup: bool = False) -> None:
    """Run environment checks, optionally printing the setup guide."""
    print("🔍 Checking Seattle School Radar Environment & Dependencies:")
    crawler = XHSRadarCrawler()
    bridge_ok = crawler.connect_bridge()
    print(
        f"• Chrome Bridge Connection: {'✅ Connected' if bridge_ok else '⚠️ Not connected (Start bridge server)'}"
    )
    if bridge_ok:
        login_ok, msg = crawler.verify_login_state()
        print(f"• Xiaohongshu Login Status: {'✅ Logged in' if login_ok else '⚠️ ' + msg}")
    else:
        print(f"• Xiaohongshu Skill Repository: {XIAOHONGSHU_SKILL_URL}")
    print(
        "• Greater Seattle Registry: ✅ 18+ core schools indexed (BSD, LWSD, ISD, MISD, SPS, NSD, Privates)"
    )
    print("• Built-in Matt Pocock Grill Engine: ✅ Operational")
    upstream = find_upstream_grill_skill()
    if upstream is not None:
        print(
            f"• Matt Pocock Grill-me Skill: Built-in operational | Upstream: {GRILL_ME_UPSTREAM_URL} (found at {upstream})"
        )
    else:
        print(
            f"• Matt Pocock Grill-me Skill: Built-in operational | Upstream: {GRILL_ME_UPSTREAM_URL}"
        )
    print(
        "• Human-like Anti-Scraping: ✅ HumanJitter, SmoothScroller, RiskDetector, RateLimiter active"
    )
    if setup:
        print_setup_guide()


def build_parser() -> argparse.ArgumentParser:
    """Build the CLI argument parser."""
    parser = argparse.ArgumentParser(
        prog="seattle-school-radar",
        description="Greater Seattle Area School & Education Intelligence Radar",
    )
    subparsers = parser.add_subparsers(dest="command", help="Available subcommands")

    # grill command
    subparsers.add_parser("grill", help="Start interactive Matt Pocock-style grill session")

    # report command
    report_parser = subparsers.add_parser("report", help="Generate Seattle school radar report")
    report_parser.add_argument(
        "--profile", type=str, help="Path to parent profile YAML file (bypass interactive grill)"
    )
    report_parser.add_argument(
        "--format", choices=["markdown", "discord"], default="markdown", help="Output format"
    )
    report_parser.add_argument("--out", type=str, help="Output file path")

    # list schools
    list_parser = subparsers.add_parser(
        "list-schools", help="List all indexed Greater Seattle schools"
    )
    list_parser.add_argument("--district", type=str, help="Filter by district keyword")
    list_parser.add_argument(
        "--max-tuition", type=float, help="Filter schools with tuition <= max_tuition"
    )

    # doctor
    doctor_parser = subparsers.add_parser(
        "doctor", help="Check Chrome Bridge and system dependencies"
    )
    doctor_parser.add_argument(
        "--setup",
        action="store_true",
        help="Print step-by-step setup guide for optional dependencies",
    )
    return parser


def load_profile_from_yaml(path: str | Path) -> ParentProfile:
    """Loads a ParentProfile from a sanitized YAML configuration file."""
    yaml_path = Path(path).resolve()
    if not yaml_path.exists():
        raise FileNotFoundError(f"Profile config not found at: {yaml_path}")

    with yaml_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)

    # Convert child_stage string to Enum
    stage_str = data.get("child_stage", "")
    stage = ChildStage.KINDERGARTEN
    for s in ChildStage:
        if s.value == stage_str or stage_str.lower() in s.value.lower():
            stage = s
            break

    # Convert budget_type string to Enum
    budget_str = data.get("budget_type", "")
    budget = BudgetType.FLEXIBLE
    for b in BudgetType:
        if b.value == budget_str or budget_str.lower() in b.value.lower():
            budget = b
            break

    raw_pri = data.get("priorities", {})
    priorities = EducationalPriority(
        academic_rigor=float(raw_pri.get("academic_rigor", 0.7)),
        stem_focus=float(raw_pri.get("stem_focus", 0.7)),
        well_being_resilience=float(raw_pri.get("well_being_resilience", 0.8)),
        bilingual_immersion=float(raw_pri.get("bilingual_immersion", 0.3)),
        whole_child_inquiry=float(raw_pri.get("whole_child_inquiry", 0.7)),
        parent_involvement_tolerance=float(raw_pri.get("parent_involvement_tolerance", 0.3)),
    )

    return ParentProfile(
        child_age_years=float(data.get("child_age_years", 5.0)),
        child_stage=stage,
        target_entry_year=int(data.get("target_entry_year", 2026)),
        target_districts=list(data.get("target_districts", ["Bellevue (BSD 405)"])),
        budget_type=budget,
        priorities=priorities,
        specific_interests=list(data.get("specific_interests", [])),
        notes=str(data.get("notes", "")),
    )


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    registry = SchoolRegistry()

    if args.command == "grill":
        profile = execute_interactive_grill()
        print(f"\nProfile successfully compiled. Target districts: {profile.target_districts}")

    elif args.command == "list-schools":
        if args.district or args.max_tuition is not None:
            districts = [args.district] if args.district else None
            schools = registry.filter_by_criteria(districts=districts, max_tuition=args.max_tuition)
        else:
            schools = registry.list_all()
        print(f"\nIndexed Greater Seattle Schools ({len(schools)} found):")
        for s in schools:
            tuition = f" | {s.annual_tuition}" if s.annual_tuition else ""
            print(
                f"- [{s.district}] {s.name_cn} ({s.name}) | {s.gs_rating} | {s.category}{tuition}"
            )

    elif args.command == "doctor":
        run_doctor(setup=getattr(args, "setup", False))

    elif args.command == "report" or not args.command:
        # Load profile from YAML or run grill
        profile_path = getattr(args, "profile", None)
        if profile_path:
            print(f"Loading parent profile from: {profile_path}")
            profile = load_profile_from_yaml(profile_path)
        else:
            print("启动大西雅图升学雷达生成流程...")
            profile = execute_interactive_grill()

        matched = registry.filter_by_criteria(districts=profile.target_districts)
        crawler = XHSRadarCrawler()
        crawler.connect_bridge()

        insights = []
        for s in matched[:3]:
            insights.append(crawler.search_school_buzz(s))

        builder = RadarReportBuilder(profile, matched, insights)
        fmt = getattr(args, "format", "markdown")
        if fmt == "discord":
            content = builder.render_discord_kv_stream()
        else:
            content = builder.render_markdown()

        out_path = getattr(args, "out", None)
        if out_path:
            Path(out_path).write_text(content, encoding="utf-8")
            print(f"\n✅ 报告已导出至: {out_path}")
        else:
            print("\n" + content)


if __name__ == "__main__":
    main()
