from ris_client.models import FederalLawDocument
from ris_mcp.formatting import format_law_toc, format_legislation_list


def _make_federal_law_doc(**overrides) -> FederalLawDocument:
    defaults = dict(
        id="NOR40238671",
        short_title="Mietrechtsgesetz",
        full_title="Bundesgesetz MRG",
        section="§ 30",
        section_number="30",
        document_type="NOR",
        law_number="10002531",
        law_type="BG",
        abbreviation="MRG",
        effective_date="1982-01-01",
        expiry_date=None,
        amendment="",
        indices=[],
        keywords="",
        document_url="",
        full_law_url="",
        content_urls=[],
    )
    defaults.update(overrides)
    return FederalLawDocument(**defaults)


def test_legislation_list_deduplicates_by_law_number():
    """Multiple sections of the same law produce one entry in output."""
    doc1 = _make_federal_law_doc(section="§ 30")
    doc2 = _make_federal_law_doc(section="§ 31")
    result = format_legislation_list([doc1, doc2])
    assert "Found 1 law(s):" in result
    assert result.count("10002531") == 1


def test_law_toc_strips_br_tags_from_titles():
    docs = [_make_federal_law_doc(section="§ 1", full_title="Geltungsbereich<br/>Details")]
    result = format_law_toc(docs, "MRG")
    assert "Geltungsbereich" in result
    assert "<br/>" not in result
    assert "Details" not in result
