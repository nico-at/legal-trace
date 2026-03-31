from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from ris_client.enums import Application, PageSize
from ris_client.errors import RISRequestError
from ris_client.http import RISHttpClient

from .fixtures.api_responses import make_search_result


def _make_mock_response(data: dict) -> MagicMock:
    resp = MagicMock(spec=httpx.Response)
    resp.json.return_value = data
    resp.raise_for_status.return_value = None
    return resp


async def test_multi_page_pagination():
    """Full first page triggers a second request; partial second page stops."""
    page_size = PageSize.TEN
    n = page_size.as_int

    page1_docs = [{"Data": {"id": str(i)}} for i in range(n)]
    page2_docs = [{"Data": {"id": str(i + n)}} for i in range(3)]

    responses = [
        _make_mock_response(make_search_result(page1_docs, hits=13)),
        _make_mock_response(make_search_result(page2_docs, hits=13)),
    ]

    client = RISHttpClient()
    try:
        mock_get = AsyncMock(side_effect=responses)
        with patch.object(client, "_get", mock_get):
            results = await client.search(
                Application.FEDERAL_LAW_CONSOLIDATED, {},
                page_size=page_size,
            )
        assert len(results) == 13
        assert mock_get.call_count == 2
    finally:
        await client.close()


async def test_max_pages_stops_pagination():
    page_size = PageSize.TEN
    n = page_size.as_int
    full_page = make_search_result(
        [{"Data": {"id": str(i)}} for i in range(n)], hits=100
    )

    client = RISHttpClient()
    try:
        mock_get = AsyncMock(return_value=_make_mock_response(full_page))
        with patch.object(client, "_get", mock_get):
            results = await client.search(
                Application.FEDERAL_LAW_CONSOLIDATED, {},
                page_size=page_size, max_pages=2,
            )
        assert len(results) == 20
        assert mock_get.call_count == 2
    finally:
        await client.close()


async def test_http_error_becomes_ris_request_error():
    client = RISHttpClient()
    try:
        mock_response = MagicMock(spec=httpx.Response)
        mock_response.status_code = 500
        mock_response.text = "Internal Server Error"
        mock_response.raise_for_status.side_effect = httpx.HTTPStatusError(
            "Server error", request=MagicMock(), response=mock_response,
        )
        with patch.object(client._client, "get", new_callable=AsyncMock, return_value=mock_response):
            with pytest.raises(RISRequestError) as exc_info:
                await client._get("https://example.com")
            assert exc_info.value.status_code == 500
    finally:
        await client.close()
