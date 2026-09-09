from __future__ import annotations

import re

from app.models.citation import Citation
from app.models.generation import ContextChunk


_CITATION_PATTERN = re.compile(
    r"\[(C\d+)\]"
)


def extract_citation_ids(
    answer: str,
) -> list[str]:

    if not answer:
        return []

    matches = _CITATION_PATTERN.findall(
        answer
    )

    # Preserve order while removing duplicates.
    return list(
        dict.fromkeys(matches)
    )


def build_citations(
    citation_ids: list[str],
    context: list[ContextChunk],
) -> list[Citation]:

    context_by_id = {
        chunk.citation_id: chunk
        for chunk in context
    }

    citations: list[Citation] = []

    for citation_id in citation_ids:

        chunk = context_by_id.get(
            citation_id
        )

        if chunk is None:
            continue

        citations.append(
            Citation(
                citation_id=citation_id,
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                filename=chunk.filename,
                page_number=chunk.page_number,
                text=chunk.text,
                title=chunk.title,
                source=chunk.source,
            )
        )

    return citations


def validate_citations(
    answer: str,
    context: list[ContextChunk],
    require_citations: bool = True,
) -> bool:

    citation_ids = extract_citation_ids(
        answer
    )

    if require_citations and not citation_ids:
        return False

    valid_ids = {
        chunk.citation_id
        for chunk in context
    }

    return all(
        citation_id in valid_ids
        for citation_id in citation_ids
    )