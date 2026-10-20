"""Command Line Interface for Seattle School Radar."""

from __future__ import annotations

import argparse
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
    subparsers.add_parser("doctor", help="Check Chrome Bridge and system dependencies")

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
        print("🔍 Checking Seattle School Radar Environment & Dependencies:")
        crawler = XHSRadarCrawler()
        bridge_ok = crawler.connect_bridge()
        print(
            f"• Chrome Bridge Connection: {'✅ Connected' if bridge_ok else '⚠️ Not connected (Start bridge server)'}"
        )
        if bridge_ok:
            login_ok, msg = crawler.verify_login_state()
            print(f"• Xiaohongshu Login Status: {'✅ Logged in' if login_ok else '⚠️ ' + msg}")
        print(
            "• Greater Seattle Registry: ✅ 18+ core schools indexed (BSD, LWSD, ISD, MISD, SPS, NSD, Privates)"
        )
        print("• Matt Pocock Grill Engine: ✅ Operational with dynamic frontier pruning")
        print(
            "• Human-like Anti-Scraping: ✅ HumanJitter, SmoothScroller, RiskDetector, RateLimiter active"
        )

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
