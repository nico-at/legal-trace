from enum import StrEnum


class Application(StrEnum):
    # Bundesrecht
    FEDERAL_LAW_CONSOLIDATED = "BrKons"
    FEDERAL_GAZETTE_AUTH = "BgblAuth"
    FEDERAL_GAZETTE_PDF = "BgblPdf"
    FEDERAL_GAZETTE_HISTORIC = "BgblAlt"
    CONSULTATION_DRAFTS = "Begut"
    GOVERNMENT_BILLS = "RegV"
    ENGLISH_TRANSLATIONS = "Erv"

    # Landesrecht
    STATE_LAW_CONSOLIDATED = "LrKons"
    STATE_GAZETTE_AUTH = "LgblAuth"
    STATE_GAZETTE = "Lgbl"
    STATE_GAZETTE_LOWER_AUSTRIA = "LgblNO"
    STATE_ORDINANCE_GAZETTE = "Vbl"

    # Judikatur
    CONSTITUTIONAL_COURT = "Vfgh"
    ADMINISTRATIVE_COURT = "Vwgh"
    NORM_INDEX = "Normenliste"
    JUSTICE = "Justiz"
    FEDERAL_ADMIN_COURT = "Bvwg"
    STATE_ADMIN_COURTS = "Lvwg"
    DATA_PROTECTION = "Dsk"
    DISCIPLINARY = "Dok"
    STAFF_REPRESENTATION = "Pvak"
    EQUAL_TREATMENT = "Gbk"
    INDEPENDENT_ADMIN_SENATES = "Uvs"
    ASYLUM_COURT = "AsylGH"
    FEDERAL_ASYLUM_SENATE = "Ubas"
    ENVIRONMENTAL_SENATE = "Umse"
    COMMUNICATIONS_SENATE = "Bks"
    PROCUREMENT_REVIEW = "Verg"


class Controller(StrEnum):
    FEDERAL_LAW = "Bundesrecht"
    STATE_LAW = "Landesrecht"
    DISTRICTS = "Bezirke"
    MUNICIPALITIES = "Gemeinden"
    CASE_LAW = "Judikatur"
    MISCELLANEOUS = "Sonstige"
    HISTORY = "History"
    VERSION = "Version"


APPLICATION_CONTROLLER: dict[Application, Controller] = {
    # Bundesrecht
    Application.FEDERAL_LAW_CONSOLIDATED: Controller.FEDERAL_LAW,
    Application.FEDERAL_GAZETTE_AUTH: Controller.FEDERAL_LAW,
    Application.FEDERAL_GAZETTE_PDF: Controller.FEDERAL_LAW,
    Application.FEDERAL_GAZETTE_HISTORIC: Controller.FEDERAL_LAW,
    Application.CONSULTATION_DRAFTS: Controller.FEDERAL_LAW,
    Application.GOVERNMENT_BILLS: Controller.FEDERAL_LAW,
    Application.ENGLISH_TRANSLATIONS: Controller.FEDERAL_LAW,
    # Landesrecht
    Application.STATE_LAW_CONSOLIDATED: Controller.STATE_LAW,
    Application.STATE_GAZETTE_AUTH: Controller.STATE_LAW,
    Application.STATE_GAZETTE: Controller.STATE_LAW,
    Application.STATE_GAZETTE_LOWER_AUSTRIA: Controller.STATE_LAW,
    Application.STATE_ORDINANCE_GAZETTE: Controller.STATE_LAW,
    # Judikatur
    Application.CONSTITUTIONAL_COURT: Controller.CASE_LAW,
    Application.ADMINISTRATIVE_COURT: Controller.CASE_LAW,
    Application.NORM_INDEX: Controller.CASE_LAW,
    Application.JUSTICE: Controller.CASE_LAW,
    Application.FEDERAL_ADMIN_COURT: Controller.CASE_LAW,
    Application.STATE_ADMIN_COURTS: Controller.CASE_LAW,
    Application.DATA_PROTECTION: Controller.CASE_LAW,
    Application.DISCIPLINARY: Controller.CASE_LAW,
    Application.STAFF_REPRESENTATION: Controller.CASE_LAW,
    Application.EQUAL_TREATMENT: Controller.CASE_LAW,
    Application.INDEPENDENT_ADMIN_SENATES: Controller.CASE_LAW,
    Application.ASYLUM_COURT: Controller.CASE_LAW,
    Application.FEDERAL_ASYLUM_SENATE: Controller.CASE_LAW,
    Application.ENVIRONMENTAL_SENATE: Controller.CASE_LAW,
    Application.COMMUNICATIONS_SENATE: Controller.CASE_LAW,
    Application.PROCUREMENT_REVIEW: Controller.CASE_LAW,
}


class PageSize(StrEnum):
    TEN = "Ten"
    TWENTY = "Twenty"
    FIFTY = "Fifty"
    ONE_HUNDRED = "OneHundred"

    @property
    def as_int(self) -> int:
        return _PAGE_SIZE_MAP[self]


_PAGE_SIZE_MAP: dict[PageSize, int] = {
    PageSize.TEN: 10,
    PageSize.TWENTY: 20,
    PageSize.FIFTY: 50,
    PageSize.ONE_HUNDRED: 100,
}


class SortDirection(StrEnum):
    ASCENDING = "Ascending"
    DESCENDING = "Descending"


class SectionType(StrEnum):
    ALL = "Alle"
    ARTICLE = "Artikel"
    PARAGRAPH = "Paragraph"
    APPENDIX = "Anlage"


class PublishedSince(StrEnum):
    UNDEFINED = "Undefined"
    ONE_WEEK = "EinerWoche"
    TWO_WEEKS = "ZweiWochen"
    ONE_MONTH = "EinemMonat"
    THREE_MONTHS = "DreiMonaten"
    SIX_MONTHS = "SechsMonaten"
    ONE_YEAR = "EinemJahr"


class DocumentType(StrEnum):
    LEGAL_PRINCIPLE = "Rechtssatz"
    DECISION_TEXT = "Text"


class LegalDomain(StrEnum):
    CIVIL_LAW = "Zivilrecht"
    CRIMINAL_LAW = "Strafrecht"
