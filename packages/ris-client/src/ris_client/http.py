import logging
from typing import Any

import httpx

from ris_client.enums import APPLICATION_CONTROLLER, Application, PageSize
from ris_client.errors import RISApiError, RISRequestError

logger = logging.getLogger(__name__)

BASE_URL = "https://data.bka.gv.at/ris/api/v2.6"
DEFAULT_TIMEOUT = 30.0
MAX_RETRIES = 2


def _normalize_document_list(results: dict[str, Any]) -> list[dict[str, Any]]:
    """The API returns a single dict when there is one result, a list when multiple."""
    doc_results = results.get("OgdDocumentResults")
    if doc_results is None:
        return []

    hits_text = doc_results.get("Hits", {}).get("#text", "0")
    if int(hits_text) == 0:
        return []

    refs = doc_results.get("OgdDocumentReference")
    if refs is None:
        return []
    if isinstance(refs, dict):
        return [refs]
    return refs


def _check_api_error(data: dict[str, Any]) -> None:
    result = data.get("OgdSearchResult", {})
    error = result.get("Error")
    if error:
        raise RISApiError(
            application=error.get("Applikation", "unknown"),
            message=error.get("Message", "unknown error"),
        )


class RISHttpClient:
    def __init__(
        self,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
    ) -> None:
        transport = httpx.AsyncHTTPTransport(retries=max_retries)
        self._client = httpx.AsyncClient(
            timeout=timeout,
            transport=transport,
        )

    async def close(self) -> None:
        await self._client.aclose()

    async def _get(self, url: str, **kwargs: Any) -> httpx.Response:
        try:
            response = await self._client.get(url, **kwargs)
            response.raise_for_status()
            return response
        except httpx.HTTPStatusError as exc:
            raise RISRequestError(
                f"HTTP {exc.response.status_code}: {exc.response.text[:200]}",
                status_code=exc.response.status_code,
            ) from exc
        except httpx.HTTPError as exc:
            raise RISRequestError(str(exc)) from exc

    async def search(
        self,
        application: Application,
        params: dict[str, str],
        *,
        page_size: PageSize = PageSize.ONE_HUNDRED,
        max_pages: int | None = None,
    ) -> list[dict[str, Any]]:
        controller = APPLICATION_CONTROLLER[application]
        url = f"{BASE_URL}/{controller.value}"

        base_params = {
            "Applikation": application.value,
            "DokumenteProSeite": page_size.value,
            **params,
        }

        all_results: list[dict[str, Any]] = []
        page_size_int = page_size.as_int
        page = 1

        while True:
            query_params = {**base_params, "Seitennummer": str(page)}
            logger.debug("RIS request: %s page=%d", url, page)

            response = await self._get(url, params=query_params)
            data = response.json()
            _check_api_error(data)

            result = data.get("OgdSearchResult", {})
            documents = _normalize_document_list(result)
            all_results.extend(documents)

            if len(documents) < page_size_int:
                break

            page += 1
            if max_pages is not None and page > max_pages:
                break

        logger.debug("RIS search returned %d total results", len(all_results))
        return all_results

    async def fetch_document(self, url: str) -> str:
        response = await self._get(url)
        return response.text
