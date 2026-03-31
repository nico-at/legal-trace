"""Integration tests against the real RIS API.

Run:  uv pytest -m integration
"""

import pytest

from ris_client import PageSize, RISClient, SectionType

pytestmark = pytest.mark.integration


async def test_search_and_parse_federal_law():
    """Search MRG by law number and verify key fields survive parsing."""
    async with RISClient() as client:
        results = await client.search_federal_law(
            law_number="10002531",
            page_size=PageSize.TEN,
            max_pages=1,
        )
    assert len(results) > 0
    doc = results[0]
    assert doc.id
    assert doc.law_number == "10002531"
    assert doc.short_title
    assert doc.effective_date
    assert doc.document_url


async def test_fetch_law_section_html():
    async with RISClient() as client:
        results = await client.search_federal_law(
            law_number="10002531",
            section_type=SectionType.PARAGRAPH,
            section_from="1",
            section_to="1",
            max_pages=1,
        )
        assert len(results) >= 1
        html_url = next(
            (u.url for cr in results[0].content_urls for u in cr.urls if u.data_type == "Html"),
            None,
        )
        if html_url:
            html = await client.fetch_document(html_url)
            assert len(html) > 100


async def test_search_and_parse_case_law():
    async with RISClient() as client:
        results = await client.search_case_law(
            norm="MRG § 30",
            search_in_principles=True,
            page_size=PageSize.TEN,
            max_pages=1,
        )
    assert len(results) > 0
    doc = results[0]
    assert doc.id
    assert doc.court
    assert doc.decision_date
    assert len(doc.case_numbers) > 0


async def test_fetch_case_law_html():
    async with RISClient() as client:
        results = await client.search_case_law(
            norm="MRG § 30",
            search_in_principles=True,
            page_size=PageSize.TEN,
            max_pages=1,
        )
        assert len(results) > 0
        html_url = next(
            (u.url for cr in results[0].content_urls for u in cr.urls if u.data_type == "Html"),
            None,
        )
        if html_url:
            html = await client.fetch_document(html_url)
            assert len(html) > 50


async def test_pagination_across_multiple_pages():
    """MRG has 50+ sections - 2 pages of 10 should give >10 results."""
    async with RISClient() as client:
        results = await client.search_federal_law(
            law_number="10002531",
            page_size=PageSize.TEN,
            max_pages=2,
        )
    assert len(results) > 10
