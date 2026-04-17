from ris_client.models import CaseLawDocument, FederalLawDocument


def format_legislation_list(docs: list[FederalLawDocument]) -> str:
    if not docs:
        return "No results found."

    seen: dict[str, FederalLawDocument] = {}
    for doc in docs:
        if doc.law_number not in seen:
            seen[doc.law_number] = doc

    lines = [f"Found {len(seen)} law(s):\n"]
    for doc in seen.values():
        title = doc.short_title or doc.full_title
        lines.append(
            f"- {title}"
            f" [Gesetzesnummer: {doc.law_number}]"
            f" (Type: {doc.law_type})"
        )
    return "\n".join(lines)


def format_law_toc(docs: list[FederalLawDocument], title: str) -> str:
    if not docs:
        return f"No sections found for '{title}'."

    lines = [f"Structure of {docs[0].short_title or title} ({len(docs)} sections):\n"]
    for doc in docs:
        section = doc.section or "-"
        info = doc.full_title.split("<br/>")[0] if "<br/>" in doc.full_title else doc.full_title
        lines.append(f"  {section}  {info}")
    return "\n".join(lines)


def format_law_text(doc: FederalLawDocument, text: str) -> str:
    header = (
        f"{doc.short_title} {doc.section}\n"
        f"Effective: {doc.effective_date}"
    )
    if doc.expiry_date:
        header += f" | Expires: {doc.expiry_date}"
    return f"{header}\n\n{text}"


def format_case_law_list(docs: list[CaseLawDocument]) -> str:
    if not docs:
        return "No results found."

    lines = [f"Found {len(docs)} result(s):\n"]
    for doc in docs:
        rs = ", ".join(doc.legal_principle_numbers) if doc.legal_principle_numbers else "-"
        case_nums = doc.case_numbers[0] if doc.case_numbers else "-"
        norms = ", ".join(doc.norms[:5]) if doc.norms else "-"
        suffix = f", +{len(doc.norms) - 5} more" if len(doc.norms) > 5 else ""

        lines.append(
            f"- [{doc.document_type}] RS {rs} | {doc.court} {case_nums} ({doc.decision_date})"
        )
        lines.append(f"  Norms: {norms}{suffix}")

        if doc.leitsatz:
            truncated = doc.leitsatz[:200] + "..." if len(doc.leitsatz) > 200 else doc.leitsatz
            lines.append(f"  Leitsatz: {truncated}")

        if doc.linked_decisions:
            lead = doc.linked_decisions[0]
            lines.append(
                f"  Lead decision: {lead.court} {lead.case_number} ({lead.decision_date})"
            )
    return "\n".join(lines)


def format_decision(doc: CaseLawDocument, text: str | None = None) -> str:
    case_nums = ", ".join(doc.case_numbers) if doc.case_numbers else "-"
    lines = [
        f"{doc.document_type}: {doc.court} {case_nums}",
        f"Date: {doc.decision_date}",
    ]
    if doc.decision_type:
        lines.append(f"Decision type: {doc.decision_type}")
    if doc.ecli:
        lines.append(f"ECLI: {doc.ecli}")
    if doc.norms:
        lines.append(f"Norms: {', '.join(doc.norms)}")
    if doc.legal_principle_numbers:
        lines.append(f"Rechtssatznummern: {', '.join(doc.legal_principle_numbers)}")
    if doc.linked_decisions:
        lines.append(f"Linked decisions ({len(doc.linked_decisions)}):")
        for ld in doc.linked_decisions[:10]:
            lines.append(f"  - {ld.court} {ld.case_number} ({ld.decision_date})")
        if len(doc.linked_decisions) > 10:
            lines.append(f"  ... and {len(doc.linked_decisions) - 10} more")

    if doc.leitsatz:
        lines.append(f"Leitsatz: {doc.leitsatz}")

    if text:
        lines.append(f"\n--- Full Text ---\n{text}")

    return "\n".join(lines)
