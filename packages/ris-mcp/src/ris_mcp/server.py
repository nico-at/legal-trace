import re
from contextlib import asynccontextmanager
from dataclasses import dataclass
from datetime import date

from mcp.server.fastmcp import Context, FastMCP

from ris_client import (
    LegalDomain,
    PageSize,
    RISClient,
    SectionType,
    SortDirection,
)
from ris_mcp.formatting import (
    format_case_law_list,
    format_decision,
    format_law_text,
    format_law_toc,
    format_legislation_list,
)

# The benchmark reference date - all law queries default to this Stichtag
REFERENCE_DATE = date(2026, 1, 1)

# HTML cleaning patterns
_STYLE_RE = re.compile(r"<style[^>]*>.*?</style>", re.DOTALL | re.IGNORECASE)
_SCRIPT_RE = re.compile(r"<script[^>]*>.*?</script>", re.DOTALL | re.IGNORECASE)
_HEAD_RE = re.compile(r"<head[^>]*>.*?</head>", re.DOTALL | re.IGNORECASE)
_HTML_TAG_RE = re.compile(r"<[^>]+>")


def _strip_html(text: str) -> str:
    text = _HEAD_RE.sub("", text)
    text = _STYLE_RE.sub("", text)
    text = _SCRIPT_RE.sub("", text)
    text = _HTML_TAG_RE.sub(" ", text)
    text = re.sub(r" {2,}", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


@dataclass
class AppContext:
    client: RISClient


@asynccontextmanager
async def app_lifespan(server: FastMCP):
    client = RISClient()
    try:
        yield AppContext(client=client)
    finally:
        await client.close()


mcp = FastMCP(
    "ris-legal",
    instructions=(
        "This server provides access to Austrian legal sources via the RIS "
        "(Rechtsinformationssystem) API. Use these tools to search for laws, "
        "read specific provisions, and find relevant case law. All law queries "
        "return the legal state as of 2026-01-01 unless otherwise specified."
    ),
    lifespan=app_lifespan,
)


def _get_client(ctx: Context) -> RISClient:
    return ctx.request_context.lifespan_context.client


@mcp.tool()
async def search_legislation(
    query: str,
    ctx: Context,
    legal_domain: str | None = None,
) -> str:
    """Search for Austrian federal laws and regulations by keyword.

    Use this to find which laws exist on a topic. Returns a deduplicated
    list of laws with their titles and law numbers (Gesetzesnummer).

    Args:
        query: Search keywords (e.g. "Kündigung Mietvertrag", "Datenschutz")
        legal_domain: Optional filter by legal index/classification
    """
    client = _get_client(ctx)
    results = await client.search_federal_law(
        keywords=query,
        version_date=REFERENCE_DATE,
        page_size=PageSize.ONE_HUNDRED,
        max_pages=3,
    )
    return format_legislation_list(results)


@mcp.tool()
async def get_law_toc(
    ctx: Context,
    law_number: str | None = None,
    title: str | None = None,
) -> str:
    """Get the table of contents (all sections) of a specific Austrian law.

    Use this to understand the structure of a law before looking up
    specific provisions. Provide either law_number or title.

    Args:
        law_number: The Gesetzesnummer (e.g. "10002531" for MRG).
            Use search_legislation to find this number.
        title: Law title or abbreviation (e.g. "Mietrechtsgesetz", "MRG").
            Used as fallback if law_number is not provided.
    """
    if not law_number and not title:
        return "Error: Provide either law_number or title."

    client = _get_client(ctx)
    results = await client.search_federal_law(
        law_number=law_number,
        title=title if not law_number else None,
        version_date=REFERENCE_DATE,
        sort_column="ArtikelParagraphAnlage",
        sort_direction=SortDirection.ASCENDING,
        max_pages=10,
    )
    return format_law_toc(results, title or law_number or "")


@mcp.tool()
async def get_law_text(
    ctx: Context,
    law_number: str | None = None,
    title: str | None = None,
    section: str | None = None,
) -> str:
    """Get the full text of a specific section (paragraph/article) of a law.

    Retrieves the actual legal text content. Provide law_number or title,
    and optionally a specific section number.

    Args:
        law_number: The Gesetzesnummer (e.g. "10002531" for MRG).
        title: Law title or abbreviation (e.g. "MRG"). Fallback if no law_number.
        section: Specific section number (e.g. "30" for § 30). If omitted,
            returns § 0 (the preamble / title provision).
    """
    if not law_number and not title:
        return "Error: Provide either law_number or title."

    client = _get_client(ctx)

    section_type = SectionType.PARAGRAPH
    section_num = section or "0"

    results = await client.search_federal_law(
        law_number=law_number,
        title=title if not law_number else None,
        section_type=section_type,
        section_from=section_num,
        section_to=section_num,
        version_date=REFERENCE_DATE,
        max_pages=1,
    )

    if not results:
        return f"No provision found for section {section_num}."

    doc = results[0]
    html_url = next(
        (url.url for cr in doc.content_urls for url in cr.urls if url.data_type == "Html"),
        None,
    )
    if not html_url:
        return format_law_text(doc, "(No text content available)")

    raw_html = await client.fetch_document(html_url)
    text = _strip_html(raw_html)
    return format_law_text(doc, text)


@mcp.tool()
async def search_case_law(
    ctx: Context,
    query: str | None = None,
    norm: str | None = None,
    legal_domain: str | None = None,
    subject_area: str | None = None,
) -> str:
    """Search for Austrian court decisions and legal principles (Rechtssätze).

    Searches the OGH (Supreme Court) case law database. Returns Rechtssätze
    (condensed legal principles) which identify leading decisions.

    Args:
        query: Free-text search keywords
        norm: Search by legal norm reference (e.g. "MRG § 30", "ABGB § 1118")
        legal_domain: "Zivilrecht" or "Strafrecht"
        subject_area: Specific subject area (e.g. "Arbeitsrecht", "Bestandrecht")
    """
    if not query and not norm:
        return "Error: Provide either query or norm."

    client = _get_client(ctx)

    domain = None
    if legal_domain:
        try:
            domain = LegalDomain(legal_domain)
        except ValueError:
            return f"Error: legal_domain must be 'Zivilrecht' or 'Strafrecht', got '{legal_domain}'"

    results = await client.search_case_law(
        keywords=query,
        norm=norm,
        legal_domain=domain,
        subject_area=subject_area,
        search_in_principles=True,
        page_size=PageSize.FIFTY,
        max_pages=2,
    )
    return format_case_law_list(results)


@mcp.tool()
async def get_decision(
    ctx: Context,
    case_number: str | None = None,
    legal_principle_number: str | None = None,
) -> str:
    """Get a specific court decision or legal principle (Rechtssatz) by identifier.

    Retrieves detailed information including the full text of a decision
    or Rechtssatz. Provide either case_number or legal_principle_number.

    Args:
        case_number: The Geschäftszahl (e.g. "2 Ob 156/15b")
        legal_principle_number: The Rechtssatznummer (e.g. "RS0067816")
    """
    if not case_number and not legal_principle_number:
        return "Error: Provide either case_number or legal_principle_number."

    client = _get_client(ctx)

    if legal_principle_number:
        results = await client.search_case_law(
            legal_principle_number=legal_principle_number,
            search_in_principles=True,
            max_pages=1,
        )
    else:
        results = await client.search_case_law(
            case_number=case_number,
            search_in_decisions=True,
            max_pages=1,
        )

    if not results:
        identifier = case_number or legal_principle_number
        return f"No decision found for '{identifier}'."

    doc = results[0]

    html_url = next(
        (url.url for cr in doc.content_urls for url in cr.urls if url.data_type == "Html"),
        None,
    )
    text = None
    if html_url:
        raw_html = await client.fetch_document(html_url)
        text = _strip_html(raw_html)

    return format_decision(doc, text)


if __name__ == "__main__":
    mcp.run(transport="stdio")
