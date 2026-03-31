from datetime import date

from ris_client.enums import SortDirection
from ris_client.queries import case_law as case_law_query
from ris_client.queries import federal_law as federal_law_query


def test_version_date_suppresses_effective_and_expiry_dates():
    params = federal_law_query.build_search_params(
        version_date=date(2026, 1, 1),
        effective_from=date(2020, 1, 1),
        expiry_from=date(2020, 6, 1),
    )
    assert "Fassung.FassungVom" in params
    assert "Fassung.VonInkrafttretensdatum" not in params
    assert "Fassung.VonAusserkrafttretensdatum" not in params


def test_section_range_ignored_without_section_type():
    params = federal_law_query.build_search_params(section_from="30", section_to="35")
    assert "Abschnitt.Von" not in params
    assert "Abschnitt.Bis" not in params


def test_sorting_requires_both_column_and_direction():
    assert "Sortierung.SortedByColumn" not in federal_law_query.build_search_params(
        sort_column="ArtikelParagraphAnlage"
    )
    both = federal_law_query.build_search_params(
        sort_column="Kurzinformation", sort_direction=SortDirection.DESCENDING,
    )
    assert both["Sortierung.SortedByColumn"] == "Kurzinformation"
    assert both["Sortierung.SortDirection"] == "Descending"


def test_search_in_flags_only_set_on_true():
    params = case_law_query.build_search_params(
        search_in_principles=False, search_in_decisions=False
    )
    assert "Dokumenttyp.SucheInRechtssaetzen" not in params
    assert "Dokumenttyp.SucheInEntscheidungstexten" not in params
