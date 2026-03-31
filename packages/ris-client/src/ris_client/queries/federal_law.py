from datetime import date

from ris_client.enums import SectionType, SortDirection


def build_search_params(
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
) -> dict[str, str]:
    params: dict[str, str] = {}

    if keywords is not None:
        params["Suchworte"] = keywords
    if title is not None:
        params["Titel"] = title
    if index is not None:
        params["Index"] = index
    if law_type is not None:
        params["Typ"] = law_type
    if law_number is not None:
        params["Gesetzesnummer"] = law_number

    if section_type is not None:
        params["Abschnitt.Typ"] = section_type.value
        if section_from is not None:
            params["Abschnitt.Von"] = section_from
        if section_to is not None:
            params["Abschnitt.Bis"] = section_to

    if version_date is not None:
        params["Fassung.FassungVom"] = version_date.isoformat()
    else:
        if effective_from is not None:
            params["Fassung.VonInkrafttretensdatum"] = effective_from.isoformat()
        if effective_to is not None:
            params["Fassung.BisInkrafttretensdatum"] = effective_to.isoformat()
        if expiry_from is not None:
            params["Fassung.VonAusserkrafttretensdatum"] = expiry_from.isoformat()
        if expiry_to is not None:
            params["Fassung.BisAusserkrafttretensdatum"] = expiry_to.isoformat()

    if sort_column is not None and sort_direction is not None:
        params["Sortierung.SortedByColumn"] = sort_column
        params["Sortierung.SortDirection"] = sort_direction.value

    return params
