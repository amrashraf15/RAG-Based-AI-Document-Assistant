from __future__ import annotations

from app.models.search import SearchResult
from app.retrieval.lexical_store import (
    LexicalStore,
)


def make_result(
    chunk_id: str,
    document_id: str,
    text: str,
) -> SearchResult:
    return SearchResult(
        chunk_id=chunk_id,
        document_id=document_id,
        filename="test.pdf",
        page_number=1,
        chunk_index=0,
        text=text,
        score=0.0,
        title=None,
        source="test.pdf",
        token_count=10,
        character_count=len(text),
        embedding_model=(
            "BAAI/bge-small-en-v1.5"
        ),
        embedding_dimension=384,
        normalized=True,
    )


def test_lexical_search() -> None:
    results = [
        make_result(
            "chunk_1",
            "doc_1",
            "machine learning project",
        ),
        make_result(
            "chunk_2",
            "doc_2",
            "web development project",
        ),
    ]

    store = LexicalStore(
        results
    )

    matches = store.search(
        "machine learning",
        top_k=1,
    )

    assert len(matches) == 1
    assert (
        matches[0].chunk_id
        == "chunk_1"
    )


def test_filter() -> None:
    results = [
        make_result(
            "chunk_1",
            "doc_1",
            "machine learning",
        ),
        make_result(
            "chunk_2",
            "doc_2",
            "machine learning",
        ),
    ]

    store = LexicalStore(
        results
    )

    matches = store.search(
        "machine learning",
        top_k=5,
        filters={
            "document_id": "doc_2"
        },
    )

    assert len(matches) == 1
    assert (
        matches[0].document_id
        == "doc_2"
    )


def test_add_results() -> None:
    store = LexicalStore(
        [
            make_result(
                "chunk_1",
                "doc_1",
                "machine learning",
            )
        ]
    )

    store.add_results(
        [
            make_result(
                "chunk_2",
                "doc_2",
                "web development",
            )
        ]
    )

    assert len(store.results) == 2