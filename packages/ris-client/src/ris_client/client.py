from datetime import date

from ris_client.enums import (
    Application,
    LegalDomain,
    PageSize,
    SectionType,
    SortDirection,
)
from ris_client.http import DEFAULT_TIMEOUT, MAX_RETRIES, RISHttpClient
from ris_client.models import CaseLawDocument, FederalLawDocument
from ris_client.queries import case_law as case_law_query
from ris_client.queries import federal_law as federal_law_query


class RISClient:
    """High-level async client for the Austrian RIS OGD API."""

    def __init__(
        self,
        timeout: float = DEFAULT_TIMEOUT,
        max_retries: int = MAX_RETRIES,
    ) -> None:
        self._http = RISHttpClient(timeout=timeout, max_retries=max_retries)

    async def close(self) -> None:
        await self._http.close()

    async def __aenter__(self) -> "RISClient":
        return self

    async def __aexit__(self, *args: object) -> None:
        await self.close()

    async def search_federal_law(
        self,
        *,
        keywords: str | None = None,
        title: str | None = None,
        index: str | None = None,
        law_type: str | None = None,
        law_number: str | None = None,
        section_from: str | None = None,
        section_to: str | None = None,
        section_type: SectionType | None = None,
        version_date: date | None = None,
        effective_from: date | None = None,
        effective_to: date | None = None,
        expiry_from: date | None = None,
        expiry_to: date | None = None,
        sort_column: str | None = None,
        sort_direction: SortDirection | None = None,
        page_size: PageSize = PageSize.ONE_HUNDRED,
        max_pages: int | None = None,
    ) -> list[FederalLawDocument]:
        params = federal_law_query.build_search_params(
            keywords=keywords,
            title=title,
            index=index,
            law_type=law_type,
            law_number=law_number,
            section_from=section_from,
            section_to=section_to,
            section_type=section_type,
            version_date=version_date,
            effective_from=effective_from,
            effective_to=effective_to,
            expiry_from=expiry_from,
            expiry_to=expiry_to,
            sort_column=sort_column,
            sort_direction=sort_direction,
        )
        raw_results = await self._http.search(
            Application.FEDERAL_LAW_CONSOLIDATED,
            params,
            page_size=page_size,
            max_pages=max_pages,
        )
        return [FederalLawDocument.from_raw(doc) for doc in raw_results]

    async def search_case_law(
        self,
        *,
        keywords: str | None = None,
        norm: str | None = None,
        case_number: str | None = None,
        legal_principle_number: str | None = None,
        legal_domain: LegalDomain | None = None,
        subject_area: str | None = None,
        court: str | None = None,
        decision_date_from: date | None = None,
        decision_date_to: date | None = None,
        search_in_principles: bool | None = None,
        search_in_decisions: bool | None = None,
        legal_assessment: str | None = None,
        operative_part: str | None = None,
        reference: str | None = None,
        sort_column: str | None = None,
        sort_direction: SortDirection | None = None,
        application: Application = Application.JUSTICE,
        page_size: PageSize = PageSize.ONE_HUNDRED,
        max_pages: int | None = None,
    ) -> list[CaseLawDocument]:
        params = case_law_query.build_search_params(
            keywords=keywords,
            norm=norm,
            case_number=case_number,
            legal_principle_number=legal_principle_number,
            legal_domain=legal_domain,
            subject_area=subject_area,
            court=court,
            decision_date_from=decision_date_from,
            decision_date_to=decision_date_to,
            search_in_principles=search_in_principles,
            search_in_decisions=search_in_decisions,
            legal_assessment=legal_assessment,
            operative_part=operative_part,
            reference=reference,
            sort_column=sort_column,
            sort_direction=sort_direction,
        )
        raw_results = await self._http.search(
            application,
            params,
            page_size=page_size,
            max_pages=max_pages,
        )
        return [CaseLawDocument.from_raw(doc) for doc in raw_results]

    async def fetch_document(self, url: str) -> str:
        return await self._http.fetch_document(url)
