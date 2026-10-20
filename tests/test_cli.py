"""Tests for Seattle School Radar CLI and YAML loader."""

from pathlib import Path
from typing import Any
from unittest.mock import MagicMock

import pytest

import seattle_school_radar.cli as cli_module
from seattle_school_radar.cli import (
    build_parser,
    find_upstream_grill_skill,
    load_profile_from_yaml,
    print_setup_guide,
    run_doctor,
)
from seattle_school_radar.models import ChildStage


def test_load_sample_profile_yaml() -> None:
    yaml_path = Path(__file__).resolve().parents[1] / "examples" / "sample_profile.yaml"
    profile = load_profile_from_yaml(yaml_path)

    assert profile.child_stage == ChildStage.KINDERGARTEN
    assert profile.child_age_years == 5.0
    assert "Lake Washington (LWSD 414)" in profile.target_districts
    assert profile.priorities.stem_focus >= 0.8


def test_build_parser_doctor_setup_flag_defaults_off() -> None:
    args = build_parser().parse_args(["doctor"])
    assert args.command == "doctor"
    assert args.setup is False


def test_build_parser_doctor_setup_flag_enabled() -> None:
    args = build_parser().parse_args(["doctor", "--setup"])
    assert args.command == "doctor"
    assert args.setup is True


def _patch_crawler(
    monkeypatch: pytest.MonkeyPatch, *, bridge_ok: bool, login_ok: bool = False
) -> MagicMock:
    fake = MagicMock()
    fake.connect_bridge.return_value = bridge_ok
    fake.verify_login_state.return_value = (login_ok, "Logged in" if login_ok else "Not logged in")
    monkeypatch.setattr(cli_module, "XHSRadarCrawler", lambda: fake)
    return fake


def test_run_doctor_not_connected(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _patch_crawler(monkeypatch, bridge_ok=False)
    monkeypatch.setattr(cli_module, "find_upstream_grill_skill", lambda **kwargs: None)

    run_doctor(setup=False)

    out = capsys.readouterr().out
    assert "Built-in Matt Pocock Grill Engine" in out
    assert "Operational" in out
    assert "Matt Pocock Grill-me Skill: Built-in operational" in out
    assert "https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me" in out
    assert "Not connected" in out
    assert "https://github.com/shuyuanshi/xiaohongshu-skill" in out
    assert "Automated Setup Guide" not in out


def test_run_doctor_connected_logged_in(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _patch_crawler(monkeypatch, bridge_ok=True, login_ok=True)
    monkeypatch.setattr(cli_module, "find_upstream_grill_skill", lambda **kwargs: None)

    run_doctor(setup=False)

    out = capsys.readouterr().out
    assert "Connected" in out
    assert "Logged in" in out


def test_run_doctor_with_setup_prints_guide(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    _patch_crawler(monkeypatch, bridge_ok=False)
    monkeypatch.setattr(cli_module, "find_upstream_grill_skill", lambda **kwargs: None)

    run_doctor(setup=True)

    out = capsys.readouterr().out
    assert "Automated Setup Guide" in out
    assert "https://github.com/shuyuanshi/xiaohongshu-skill" in out
    assert "git clone https://github.com/shuyuanshi/xiaohongshu-skill.git" in out
    assert "chrome://extensions" in out
    assert "xiaohongshu.com" in out
    assert "npx skills add mattpocock/skills/productivity/grill-me" in out
    assert "already works standalone" in out


def test_run_doctor_reports_upstream_path(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str], tmp_path: Path
) -> None:
    _patch_crawler(monkeypatch, bridge_ok=False)
    found = tmp_path / "grill-me"
    found.mkdir()
    monkeypatch.setattr(cli_module, "find_upstream_grill_skill", lambda **kwargs: found)

    run_doctor(setup=False)

    out = capsys.readouterr().out
    assert str(found) in out
    assert "Matt Pocock Grill-me Skill: Built-in operational" in out


def test_find_upstream_grill_skill_detects_workspace_dir(tmp_path: Path) -> None:
    target = tmp_path / ".agents" / "skills" / "grill-me"
    target.mkdir(parents=True)
    empty_home = tmp_path / "home"
    empty_home.mkdir()

    assert find_upstream_grill_skill(cwd=tmp_path, home=empty_home) == target


def test_find_upstream_grill_skill_returns_none_when_absent(tmp_path: Path) -> None:
    empty_home = tmp_path / "home"
    empty_home.mkdir()

    assert find_upstream_grill_skill(cwd=tmp_path, home=empty_home) is None


def test_print_setup_guide_steps(capsys: pytest.CaptureFixture[str]) -> None:
    print_setup_guide()

    out = capsys.readouterr().out
    assert "Step 1" in out
    assert "Step 2" in out
    assert "Step 3" in out
    assert "https://github.com/mattpocock/skills/tree/main/skills/productivity/grill-me" in out


def test_main_doctor_dispatches_setup_flag(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    calls: dict[str, Any] = {}
    monkeypatch.setattr(cli_module, "run_doctor", lambda *, setup: calls.update({"setup": setup}))
    monkeypatch.setattr("sys.argv", ["seattle-school-radar", "doctor", "--setup"])

    cli_module.main()

    assert calls == {"setup": True}
    capsys.readouterr()


def test_main_doctor_without_setup_flag(
    monkeypatch: pytest.MonkeyPatch, capsys: pytest.CaptureFixture[str]
) -> None:
    calls: dict[str, Any] = {}
    monkeypatch.setattr(cli_module, "run_doctor", lambda *, setup: calls.update({"setup": setup}))
    monkeypatch.setattr("sys.argv", ["seattle-school-radar", "doctor"])

    cli_module.main()

    assert calls == {"setup": False}
    capsys.readouterr()
