from unittest.mock import AsyncMock, MagicMock

from ris_client import Application, SectionType
from ris_client.models import (
    CaseLawDocument,
    ContentReference,
    ContentUrl,
    FederalLawDocument,
)
from ris_mcp.server import (
    _strip_html,
    get_decision,
    get_law_text,
    get_law_toc,
    search_case_law,
)


def _make_ctx(client_mock: AsyncMock) -> MagicMock:
    ctx = MagicMock()
    ctx.request_context.lifespan_context.client = client_mock
    return ctx


def _make_federal_law_doc(**overrides) -> FederalLawDocument:
    defaults = dict(
        id="NOR40238671", short_title="Mietrechtsgesetz", full_title="Bundesgesetz MRG",
        section="§ 30", section_number="30", document_type="NOR", law_number="10002531",
        law_type="BG", abbreviation="MRG", effective_date="1982-01-01", expiry_date=None,
        amendment="", indices=[], keywords="", document_url="", full_law_url="",
        content_urls=[],
    )
    defaults.update(overrides)
    return FederalLawDocument(**defaults)


def _make_case_law_doc(**overrides) -> CaseLawDocument:
    defaults = dict(
        id="JJR_TEST", document_type="Rechtssatz", case_numbers=["2 Ob 156/15b"],
        decision_date="2015-09-01", ecli="", court="OGH", norms=["MRG § 30"],
        keywords="", legal_domains=[], subject_areas=[],
        legal_principle_numbers=["RS0067816"], linked_decisions=[],
        leitsatz="", decision_type="",
        document_url="", full_decision_url="", legal_principles_url="", content_urls=[],
    )
    defaults.update(overrides)
    return CaseLawDocument(**defaults)


def test_strip_html_on_realistic_ris_page():
    html = """
    <html>
    <head>
        <title>Bundesnormen</title>
        <style type="text/css">.Titel { font-weight: bold; }</style>
    </head>
    <body>
        <div class="Titel">§ 30 MRG</div>
        <div class="AbsatzText">
            (1) Der Vermieter kann den Mietvertrag nur aus wichtigem Grund kündigen.
        </div>
    </body>
    </html>
    """
    result = _strip_html(html)
    assert "§ 30 MRG" in result
    assert "wichtigem Grund" in result
    assert "<div" not in result
    assert "font-weight" not in result
    assert "Bundesnormen" not in result


async def test_get_law_text_fetches_and_strips_html():
    html_url = ContentUrl(DataType="Html", Url="https://ris.example.com/doc.html")
    ref = ContentReference(ContentType="MainDocument", Name="§ 30", urls=[html_url])
    doc = _make_federal_law_doc(content_urls=[ref])

    client = AsyncMock()
    client.search_federal_law.return_value = [doc]
    client.fetch_document.return_value = "<p>Legal text here.</p>"

    result = await get_law_text(_make_ctx(client), law_number="10002531")
    assert "Legal text here." in result
    client.fetch_document.assert_called_once_with("https://ris.example.com/doc.html")


async def test_get_law_text_uses_section_type_all():
    client = AsyncMock()
    client.search_federal_law.return_value = []
    await get_law_text(_make_ctx(client), law_number="10000138", section="47")
    _, kwargs = client.search_federal_law.call_args
    assert kwargs["section_type"] == SectionType.ALL


async def test_get_law_toc_suppresses_title_when_law_number_given():
    client = AsyncMock()
    client.search_federal_law.return_value = []
    await get_law_toc(_make_ctx(client), law_number="10002531", title="MRG")
    _, kwargs = client.search_federal_law.call_args
    assert kwargs["law_number"] == "10002531"
    assert kwargs["title"] is None


async def test_get_law_toc_passes_section_range():
    client = AsyncMock()
    client.search_federal_law.return_value = []
    await get_law_toc(
        _make_ctx(client), law_number="10001622",
        section_from="1290", section_to="1300",
    )
    _, kwargs = client.search_federal_law.call_args
    assert kwargs["section_from"] == "1290"
    assert kwargs["section_to"] == "1300"
    assert kwargs["section_type"] == SectionType.ALL


async def test_search_case_law_rejects_invalid_legal_domain():
    result = await search_case_law(
        court="OGH", ctx=_make_ctx(AsyncMock()),
        query="test", legal_domain="InvalidDomain",
    )
    assert "Error" in result


async def test_search_case_law_rejects_invalid_court():
    result = await search_case_law(
        court="BGH", ctx=_make_ctx(AsyncMock()), query="test",
    )
    assert "Error" in result
    assert "BGH" in result


async def test_search_case_law_uses_correct_application_for_vfgh():
    client = AsyncMock()
    client.search_case_law.return_value = []
    await search_case_law(court="VfGH", ctx=_make_ctx(client), query="Asyl")
    _, kwargs = client.search_case_law.call_args
    assert kwargs["application"] == Application.CONSTITUTIONAL_COURT


async def test_search_case_law_uses_correct_application_for_vwgh():
    client = AsyncMock()
    client.search_case_law.return_value = []
    await search_case_law(court="VwGH", ctx=_make_ctx(client), query="Asyl")
    _, kwargs = client.search_case_law.call_args
    assert kwargs["application"] == Application.ADMINISTRATIVE_COURT


async def test_get_decision_searches_principles_for_rs_number():
    client = AsyncMock()
    client.search_case_law.return_value = [_make_case_law_doc()]
    client.fetch_document.return_value = "<p>Text</p>"
    await get_decision(court="OGH", ctx=_make_ctx(client), legal_principle_number="RS0067816")
    _, kwargs = client.search_case_law.call_args
    assert kwargs["search_in_principles"] is True
    assert kwargs["application"] == Application.JUSTICE


async def test_get_decision_searches_decisions_for_case_number():
    client = AsyncMock()
    client.search_case_law.return_value = [_make_case_law_doc()]
    client.fetch_document.return_value = "<p>Text</p>"
    await get_decision(court="OGH", ctx=_make_ctx(client), case_number="2 Ob 156/15b")
    _, kwargs = client.search_case_law.call_args
    assert kwargs["search_in_decisions"] is True


async def test_search_case_law_document_type_entscheidungstexte():
    client = AsyncMock()
    client.search_case_law.return_value = []
    await search_case_law(
        court="OGH", ctx=_make_ctx(client), query="test",
        document_type="Entscheidungstexte",
    )
    _, kwargs = client.search_case_law.call_args
    assert kwargs["search_in_principles"] is False
    assert kwargs["search_in_decisions"] is True


async def test_search_case_law_document_type_both():
    client = AsyncMock()
    client.search_case_law.return_value = []
    await search_case_law(
        court="OGH", ctx=_make_ctx(client), query="test",
        document_type="Both",
    )
    _, kwargs = client.search_case_law.call_args
    assert kwargs["search_in_principles"] is True
    assert kwargs["search_in_decisions"] is True


async def test_search_case_law_document_type_default_is_rechtssaetze():
    client = AsyncMock()
    client.search_case_law.return_value = []
    await search_case_law(
        court="OGH", ctx=_make_ctx(client), query="test",
    )
    _, kwargs = client.search_case_law.call_args
    assert kwargs["search_in_principles"] is True
    assert kwargs["search_in_decisions"] is False


async def test_search_case_law_rejects_invalid_document_type():
    result = await search_case_law(
        court="OGH", ctx=_make_ctx(AsyncMock()),
        query="test", document_type="Invalid",
    )
    assert "Error" in result


async def test_get_decision_uses_vfgh_application():
    client = AsyncMock()
    client.search_case_law.return_value = [_make_case_law_doc()]
    client.fetch_document.return_value = "<p>Text</p>"
    await get_decision(court="VfGH", ctx=_make_ctx(client), case_number="G3504/2023")
    _, kwargs = client.search_case_law.call_args
    assert kwargs["application"] == Application.CONSTITUTIONAL_COURT
