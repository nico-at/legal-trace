from datetime import date

from ris_client.enums import LegalDomain, SortDirection


def build_search_params(
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
) -> dict[str, str]:
    params: dict[str, str] = {}

    if keywords is not None:
        params["Suchworte"] = keywords
    if norm is not None:
        params["Norm"] = norm
    if case_number is not None:
        params["Geschaeftszahl"] = case_number
    if legal_principle_number is not None:
        params["Rechtssatznummer"] = legal_principle_number
    if legal_domain is not None:
        params["Rechtsgebiet"] = legal_domain.value
    if subject_area is not None:
        params["Fachgebiet"] = subject_area
    if court is not None:
        params["Gericht"] = court

    if decision_date_from is not None:
        params["EntscheidungsdatumVon"] = decision_date_from.isoformat()
    if decision_date_to is not None:
        params["EntscheidungsdatumBis"] = decision_date_to.isoformat()

    if search_in_principles is True:
        params["Dokumenttyp.SucheInRechtssaetzen"] = "true"
    if search_in_decisions is True:
        params["Dokumenttyp.SucheInEntscheidungstexten"] = "true"

    if legal_assessment is not None:
        params["RechtlicheBeurteilung"] = legal_assessment
    if operative_part is not None:
        params["Spruch"] = operative_part
    if reference is not None:
        params["Fundstelle"] = reference

    if sort_column is not None and sort_direction is not None:
        params["Sortierung.SortedByColumn"] = sort_column
        params["Sortierung.SortDirection"] = sort_direction.value

    return params
