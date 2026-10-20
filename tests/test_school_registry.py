"""Tests for Greater Seattle School Registry with strict boundary enforcement."""

from seattle_school_radar.school_registry import SchoolRegistry


def test_registry_loading() -> None:
    registry = SchoolRegistry()
    schools = registry.list_all()
    assert len(schools) >= 14

    # Ensure core Seattle schools exist
    school_ids = {s.id for s in schools}
    assert "newport_heights" in school_ids
    assert "somerset_elem" in school_ids
    assert "jing_mei_elem" in school_ids
    assert "tesla_stem_high" in school_ids
    assert "cascadia_elem" in school_ids
    assert "garfield_high" in school_ids
    assert "north_creek_high" in school_ids
    assert "open_window_school" in school_ids
    assert "lakeside_school" in school_ids
    assert "the_bush_school" in school_ids


def test_strict_lwsd_district_isolation() -> None:
    """Verifies Adversarial Case: Lake Washington (LWSD 414) MUST NOT match Lakeside or Overlake."""
    registry = SchoolRegistry()
    lwsd_schools = registry.filter_by_criteria(districts=["Lake Washington (LWSD 414)"])
    school_names = [s.name for s in lwsd_schools]

    assert "Tesla STEM High School" in school_names
    assert "Norman Rockwell Elementary" in school_names
    # MUST NOT contain private schools or Mercer Island schools matching 'lake' substring
    assert "Lakeside School" not in school_names
    assert "The Overlake School" not in school_names
    assert "Lakeridge Elementary" not in school_names
    for s in lwsd_schools:
        assert "LWSD 414" in s.district


def test_strict_seattle_sps_district_isolation() -> None:
    """Verifies Adversarial Case: Seattle (SPS 314) MUST NOT match Lakeside School."""
    registry = SchoolRegistry()
    sps_schools = registry.filter_by_criteria(districts=["Seattle (SPS 314)"])
    school_names = [s.name for s in sps_schools]

    assert "Cascadia Elementary" in school_names or "Garfield High School" in school_names
    assert "Lakeside School" not in school_names
    for s in sps_schools:
        assert "SPS 314" in s.district


def test_max_tuition_filtering() -> None:
    """Verifies numerical tuition filter logic."""
    registry = SchoolRegistry()
    # Free public schools only
    publics = registry.filter_by_criteria(max_tuition=0.0)
    for p in publics:
        assert p.annual_tuition is None or "free" in p.annual_tuition.lower()

    # Private schools with tuition <= $30,000
    moderate_privates = registry.filter_by_criteria(
        districts=["Independent Private"], max_tuition=30000.0
    )
    for s in moderate_privates:
        assert s.id in ["bellevue_childrens_academy", "cedar_crest_academy"]
