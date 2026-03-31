# LegalTrace

Wie zuverlässig identifizieren LLMs die für eine österreichische Rechtsfrage relevanten Rechtsquellen?

LegalTrace ist ein Benchmark, der die Quellenidentifikation von LLMs im österreichischen Recht evaluiert. Drei Retrieval-Architekturen (Direct Prompting, Web Search und agentische Tool-Calls über die RIS-API) werden über mehrere Foundation Models hinweg verglichen.

## Stand: Milestone 1 (31.03.2026)

- **RIS-Client** (`packages/ris-client/`): Python-Wrapper für die RIS OGD API v2.6. Unterstützt Bundesrecht-Suche (Stichtagsabfrage, Paragraphen-Lookup) und Judikatur-Suche (Rechtssätze, Entscheidungen).
- **RIS-MCP-Server** (`packages/ris-mcp/`): MCP-Server mit 5 Tools, der den RIS-Client für agentische LLM-Nutzung bereitstellt. Alle Abfragen verwenden den fixen Stichtag 01.01.2026.
- **Annotationsschema** (`benchmark/schema/`): JSON-Schema, internes Codebook (v0.5.0) und Annotator-Codebook für die Benchmark-Erstellung. Zwei ausgearbeitete Beispiele in `examples.jsonl`.

## Struktur

```
packages/
  ris-client/        Python-Client für die RIS OGD API v2.6
  ris-mcp/           MCP-Server mit 5 Legal-Research-Tools

benchmark/
  schema/            Annotationsschema, Codebook, Beispiele
```

## Setup

Setzt Python >= 3.12 und [uv](https://docs.astral.sh/uv/) voraus.

```bash
uv sync
```

## Tests

```bash
uv run pytest                # Unit-Tests (ohne RIS-API)
uv run pytest -m integration # Integration-Tests (mit RIS-API)
```
