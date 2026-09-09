from __future__ import annotations

from app.generation.citations import (
    build_citations,
    extract_citation_ids,
    validate_citations,
)
from app.models.generation import ContextChunk


def make_context(
    citation_id: str,
) -> ContextChunk:

    return ContextChunk(
        citation_id=citation_id,
        chunk_id=f"chunk_{citation_id}",
        document_id="doc_test",
        filename="test.pdf",
        page_number=1,
        text="Test context.",
        score=0.9,
        title=None,
        source="test.pdf",
    )


def test_extract_citations() -> None:

    answer = (
        "Machine learning is used here [C1]. "
        "The project also uses Python [C2]. "
        "This repeats [C1]."
    )

    ids = extract_citation_ids(
        answer
    )

    assert ids == [
        "C1",
        "C2",
    ]


def test_build_citations() -> None:

    context = [
        make_context("C1"),
        make_context("C2"),
    ]

    citations = build_citations(
        ["C2", "C1"],
        context,
    )

    assert len(citations) == 2

    assert (
        citations[0].citation_id
        == "C2"
    )

    assert (
        citations[1].citation_id
        == "C1"
    )


def test_valid_citations() -> None:

    context = [
        make_context("C1"),
        make_context("C2"),
    ]

    assert validate_citations(
        "Answer [C1].",
        context,
    )


def test_invalid_citation() -> None:

    context = [
        make_context("C1"),
    ]

    assert not validate_citations(
        "Answer [C99].",
        context,
    )


def test_missing_required_citation() -> None:

    context = [
        make_context("C1"),
    ]

    assert not validate_citations(
        "Answer without citation.",
        context,
        require_citations=True,
    )


def test_citations_optional() -> None:

    context = [
        make_context("C1"),
    ]

    assert validate_citations(
        "Answer without citation.",
        context,
        require_citations=False,
    )