import copy

from ris_client.models import CaseLawDocument, FederalLawDocument

from .fixtures.api_responses import CASE_LAW_RAW_DOC, FEDERAL_LAW_RAW_DOC


def test_section_number_falls_back_to_artikelnummer():
    raw = copy.deepcopy(FEDERAL_LAW_RAW_DOC)
    br_kons = raw["Data"]["Metadaten"]["Bundesrecht"]["BrKons"]
    del br_kons["Paragraphnummer"]
    br_kons["Artikelnummer"] = "7"
    assert FederalLawDocument.from_raw(raw).section_number == "7"


def test_effective_date_falls_back_to_typo_variant():
    """The API uses both 'Inkrafttretensdatum' and 'Inkrafttretedatum'."""
    raw = copy.deepcopy(FEDERAL_LAW_RAW_DOC)
    br_kons = raw["Data"]["Metadaten"]["Bundesrecht"]["BrKons"]
    del br_kons["Inkrafttretensdatum"]
    br_kons["Inkrafttretedatum"] = "2020-06-15"
    assert FederalLawDocument.from_raw(raw).effective_date == "2020-06-15"


def test_abbreviation_falls_back_to_parent_bundesrecht():
    raw = copy.deepcopy(FEDERAL_LAW_RAW_DOC)
    del raw["Data"]["Metadaten"]["Bundesrecht"]["BrKons"]["Abkuerzung"]
    assert FederalLawDocument.from_raw(raw).abbreviation == "MRG"


def test_double_encoded_utf8_fixed_in_from_raw():
    raw = copy.deepcopy(FEDERAL_LAW_RAW_DOC)
    garbled = "Kündigung".encode("utf-8").decode("latin-1")
    raw["Data"]["Metadaten"]["Bundesrecht"]["BrKons"]["Schlagworte"] = garbled
    assert FederalLawDocument.from_raw(raw).keywords == "Kündigung"


def test_court_falls_back_to_organ():
    raw = copy.deepcopy(CASE_LAW_RAW_DOC)
    del raw["Data"]["Metadaten"]["Judikatur"]["Justiz"]["Gericht"]
    assert CaseLawDocument.from_raw(raw).court == "OGH"


def test_missing_justiz_block_doesnt_crash():
    raw = copy.deepcopy(CASE_LAW_RAW_DOC)
    del raw["Data"]["Metadaten"]["Judikatur"]["Justiz"]
    doc = CaseLawDocument.from_raw(raw)
    assert doc.court == "OGH"
    assert doc.linked_decisions == []
