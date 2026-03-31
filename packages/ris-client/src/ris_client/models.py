from typing import Any

from pydantic import BaseModel, Field


def _ensure_list(value: Any) -> list:
    if value is None:
        return []
    if isinstance(value, dict):
        return [value]
    return value


def _to_str_list(value: str | list[str] | None) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        return [value]
    return value


def _extract_items(parent: dict, key: str) -> list[str]:
    """Handle the RIS pattern where {"Normen": {"item": ...}} can be a dict or absent."""
    value = parent.get(key)
    if not isinstance(value, dict):
        return []
    return _to_str_list(value.get("item"))


def _fix_encoding(text: str) -> str:
    """Fix double-encoded UTF-8 the RIS API sometimes returns."""
    try:
        return text.encode("latin-1").decode("utf-8")
    except (UnicodeDecodeError, UnicodeEncodeError):
        return text


class ContentUrl(BaseModel):
    data_type: str = Field(alias="DataType")
    url: str = Field(alias="Url")


class ContentReference(BaseModel):
    content_type: str = Field(alias="ContentType")
    name: str = Field(alias="Name")
    urls: list[ContentUrl] = Field(default_factory=list)

    @classmethod
    def from_raw(cls, raw: dict) -> "ContentReference":
        url_data = _ensure_list(raw.get("Urls", {}).get("ContentUrl"))
        return cls(
            ContentType=raw.get("ContentType", ""),
            Name=raw.get("Name", ""),
            urls=[ContentUrl(**u) for u in url_data],
        )


def _parse_content_references(doc_list: dict | None) -> list[ContentReference]:
    if doc_list is None:
        return []
    refs = _ensure_list(doc_list.get("ContentReference"))
    return [ContentReference.from_raw(r) for r in refs]


class FederalLawDocument(BaseModel):
    id: str
    short_title: str
    full_title: str
    section: str
    section_number: str
    document_type: str
    law_number: str
    law_type: str
    abbreviation: str
    effective_date: str
    expiry_date: str | None = None
    amendment: str
    indices: list[str]
    keywords: str
    document_url: str
    full_law_url: str
    content_urls: list[ContentReference]

    @classmethod
    def from_raw(cls, raw: dict) -> "FederalLawDocument":
        meta = raw["Data"]["Metadaten"]
        tech = meta["Technisch"]
        general = meta.get("Allgemein", {})
        br = meta["Bundesrecht"]
        br_kons = br.get("BrKons", {})

        return cls(
            id=tech.get("ID", ""),
            short_title=_fix_encoding(br.get("Kurztitel", "")),
            full_title=_fix_encoding(br.get("Titel", "")),
            section=_fix_encoding(br_kons.get("ArtikelParagraphAnlage", "")),
            section_number=br_kons.get(
                "Paragraphnummer", br_kons.get("Artikelnummer", "")
            ),
            document_type=br_kons.get("Dokumenttyp", ""),
            law_number=br_kons.get("Gesetzesnummer", ""),
            law_type=br_kons.get("Typ", ""),
            abbreviation=_fix_encoding(
                br_kons.get("Abkuerzung", br.get("Abkuerzung", ""))
            ),
            effective_date=br_kons.get(
                "Inkrafttretensdatum", br_kons.get("Inkrafttretedatum", "")
            ),
            expiry_date=br_kons.get("Ausserkrafttretensdatum", None),
            amendment=_fix_encoding(br_kons.get("Aenderung", "")),
            indices=_extract_items(br_kons, "Indizes"),
            keywords=_fix_encoding(br_kons.get("Schlagworte", "")),
            document_url=general.get("DokumentUrl", ""),
            full_law_url=br_kons.get("GesamteRechtsvorschriftUrl", ""),
            content_urls=_parse_content_references(raw["Data"].get("Dokumentliste")),
        )


class LinkedDecision(BaseModel):
    case_number: str
    document_type: str
    court: str
    decision_date: str
    note: str
    document_url: str


class CaseLawDocument(BaseModel):
    id: str
    document_type: str
    case_numbers: list[str]
    decision_date: str
    ecli: str
    court: str
    norms: list[str]
    keywords: str
    legal_domains: list[str]
    subject_areas: list[str]
    legal_principle_numbers: list[str]
    linked_decisions: list[LinkedDecision]
    document_url: str
    full_decision_url: str
    legal_principles_url: str
    content_urls: list[ContentReference]

    @classmethod
    def from_raw(cls, raw: dict) -> "CaseLawDocument":
        meta = raw["Data"]["Metadaten"]
        tech = meta["Technisch"]
        general = meta.get("Allgemein", {})
        jud = meta["Judikatur"]
        justiz = jud.get("Justiz", {})

        linked = []
        for item in _ensure_list(justiz.get("Entscheidungstexte", {}).get("item")):
            linked.append(
                LinkedDecision(
                    case_number=item.get("Geschaeftszahl", ""),
                    document_type=item.get("Dokumenttyp", ""),
                    court=item.get("Gericht", ""),
                    decision_date=item.get("Entscheidungsdatum", ""),
                    note=_fix_encoding(item.get("Anmerkung", "")),
                    document_url=item.get("DokumentUrl", ""),
                )
            )

        return cls(
            id=tech.get("ID", ""),
            document_type=jud.get("Dokumenttyp", ""),
            case_numbers=_extract_items(jud, "Geschaeftszahl"),
            decision_date=jud.get("Entscheidungsdatum", ""),
            ecli=jud.get("EuropeanCaseLawIdentifier", ""),
            court=justiz.get("Gericht", tech.get("Organ", "")),
            norms=_extract_items(jud, "Normen"),
            keywords=_fix_encoding(jud.get("Schlagworte", "")),
            legal_domains=_extract_items(justiz, "Rechtsgebiete"),
            subject_areas=_extract_items(justiz, "Fachgebiete"),
            legal_principle_numbers=_extract_items(justiz, "Rechtssatznummern"),
            linked_decisions=linked,
            document_url=general.get("DokumentUrl", ""),
            full_decision_url=jud.get("GesamteEntscheidungUrl", ""),
            legal_principles_url=jud.get("RechtssaetzeUrl", ""),
            content_urls=_parse_content_references(raw["Data"].get("Dokumentliste")),
        )
