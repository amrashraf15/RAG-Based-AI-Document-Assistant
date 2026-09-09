from __future__ import annotations

from typing import Sequence

import pytest

from app.models.search import SearchResult
from app.retrieval.reranker import Reranker
from app.retrieval.reranking import (
    RerankingPipeline,
)


def make_result(
    chunk_id: str,
    text: str,
    score: float,
) -> SearchResult:
    return SearchResult(
        chunk_id=chunk_id,
        document_id="doc_test",
        filename="test.pdf",
        page_number=1,
        chunk_index=0,
        text=text,
        score=score,
        title="Test",
        source="test.pdf",
        token_count=10,
        character_count=len(text),
        embedding_model=(
            "BAAI/bge-small-en-v1.5"
        ),
        embedding_dimension=384,
        normalized=True,
    )


class FakeReranker(Reranker):

    def __init__(
        self,
        scores: list[float],
    ):
        self.scores = scores

    @property
    def model_name(self) -> str:
        return "fake-reranker"

    @property
    def batch_size(self) -> int:
        return 2

    def rerank(
        self,
        query: str,
        results: Sequence[SearchResult],
    ) -> list[float]:

        return self.scores


def test_reranking_sorts_by_reranker_score() -> None:
    results = [
        make_result(
            "chunk_1",
            "Machine learning.",
            0.90,
        ),
        make_result(
            "chunk_2",
            "Web development.",
            0.80,
        ),
        make_result(
            "chunk_3",
            "Information retrieval.",
            0.70,
        ),
    ]

    reranker = FakeReranker(
        scores=[0.20, 0.95, 0.50]
    )

    pipeline = RerankingPipeline(
        reranker=reranker,
    )

    ranked = pipeline.rerank(
        query="web development",
        results=results,
        top_k=3,
    )

    assert [
        result.chunk_id
        for result in ranked
    ] == [
        "chunk_2",
        "chunk_3",
        "chunk_1",
    ]


def test_reranking_respects_top_k() -> None:
    results = [
        make_result(
            "chunk_1",
            "One",
            0.90,
        ),
        make_result(
            "chunk_2",
            "Two",
            0.80,
        ),
        make_result(
            "chunk_3",
            "Three",
            0.70,
        ),
    ]

    reranker = FakeReranker(
        scores=[0.1, 0.9, 0.5]
    )

    pipeline = RerankingPipeline(
        reranker=reranker,
    )

    ranked = pipeline.rerank(
        query="test",
        results=results,
        top_k=2,
    )

    assert len(ranked) == 2

    assert ranked[0].chunk_id == "chunk_2"
    assert ranked[1].chunk_id == "chunk_3"


def test_reranking_preserves_retrieval_score() -> None:
    results = [
        make_result(
            "chunk_1",
            "Test document.",
            0.8765,
        )
    ]

    reranker = FakeReranker(
        scores=[0.9234]
    )

    pipeline = RerankingPipeline(
        reranker=reranker,
    )

    ranked = pipeline.rerank(
        query="test",
        results=results,
    )

    assert (
        ranked[0].retrieval_score
        == pytest.approx(0.8765)
    )

    assert (
        ranked[0].reranker_score
        == pytest.approx(0.9234)
    )


def test_empty_results() -> None:
    reranker = FakeReranker([])

    pipeline = RerankingPipeline(
        reranker=reranker,
    )

    results = pipeline.rerank(
        query="test",
        results=[],
    )

    assert results == []


def test_empty_query_raises() -> None:
    reranker = FakeReranker([])

    pipeline = RerankingPipeline(
        reranker=reranker,
    )

    with pytest.raises(ValueError):
        pipeline.rerank(
            query="",
            results=[],
        )


def test_invalid_top_k_raises() -> None:
    reranker = FakeReranker([])

    pipeline = RerankingPipeline(
        reranker=reranker,
    )

    with pytest.raises(ValueError):
        pipeline.rerank(
            query="test",
            results=[],
            top_k=0,
        )