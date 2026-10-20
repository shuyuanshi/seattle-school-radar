"""Tests for Seattle School Radar CLI and YAML loader."""

from pathlib import Path

from seattle_school_radar.cli import load_profile_from_yaml
from seattle_school_radar.models import ChildStage


def test_load_sample_profile_yaml() -> None:
    yaml_path = Path(__file__).resolve().parents[1] / "examples" / "sample_profile.yaml"
    profile = load_profile_from_yaml(yaml_path)

    assert profile.child_stage == ChildStage.KINDERGARTEN
    assert profile.child_age_years == 5.0
    assert "Lake Washington (LWSD 414)" in profile.target_districts
    assert profile.priorities.stem_focus >= 0.8
