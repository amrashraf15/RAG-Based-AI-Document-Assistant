from __future__ import annotations

import pytest

from app.retrieval.bm25 import BM25


def test_empty_documents() -> None:
    bm25 = BM25([])

    assert bm25.score("machine learning") == []
    assert bm25.top_k("machine learning") == []


def test_matching_document_scores_higher() -> None:
    bm25 = BM25(
        [
            "machine learning and artificial intelligence",
            "web development with React",
            "database administration",
        ]
    )

    scores = bm25.score(
        "machine learning"
    )

    assert scores[0] > scores[1]
    assert scores[0] > scores[2]


def test_top_k() -> None:
    bm25 = BM25(
        [
            "machine learning",
            "web development",
            "machine learning projects",
        ]
    )

    results = bm25.top_k(
        "machine learning",
        k=2,
    )

    assert len(results) == 2
    assert results[0][0] in {0, 2}


def test_empty_query_raises() -> None:
    bm25 = BM25(
        ["machine learning"]
    )

    with pytest.raises(ValueError):
        bm25.score("")


def test_invalid_k_raises() -> None:
    bm25 = BM25(
        ["machine learning"]
    )

    with pytest.raises(ValueError):
        bm25.top_k(
            "machine",
            k=0,
        )


def test_invalid_b_raises() -> None:
    with pytest.raises(ValueError):
        BM25(
            ["test"],
            b=1.5,
        )


def test_invalid_k1_raises() -> None:
    with pytest.raises(ValueError):
        BM25(
            ["test"],
            k1=-1,
        )