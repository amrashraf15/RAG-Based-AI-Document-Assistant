from __future__ import annotations

from typing import Any, Sequence

import pytest

from app.models.search import SearchResult
from app.retrieval.hybrid import (
    HybridRetriever,
)
from app.retrieval.lexical_store import (
    LexicalStore,
)
from app.retrieval.vector_store import (
    VectorStore,
)


class FakeEmbeddingModel:

    @property
    def model_name(self) -> str:
        return "fake"

    @property
    def dimension(self) -> int:
        return 3

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        return [1.0, 0.0, 0.0]


class FakeVectorStore(VectorStore):

    def __init__(
        self,
        results: list[SearchResult],
    ):
        self.results = results

    def create_collection(
        self,
        vector_size: int,
    ) -> None:
        pass

    def collection_exists(self) -> bool:
        return True

    def upsert(
        self,
        chunks: list[Any],
    ) -> None:
        pass

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[SearchResult]:

        results = self.results

        if filters:
            results = [
                result
                for result in results
                if all(
                    getattr(
                        result,
                        field,
                    )
                    == value
                    for field, value
                    in filters.items()
                )
            ]

        return results[:top_k]

    def count(self) -> int:
        return len(self.results)

    def delete_collection(self) -> None:
        pass

    def close(self) -> None:
        pass


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
        title=None,
        source="test.pdf",
        token_count=10,
        character_count=len(text),
        embedding_model="fake",
        embedding_dimension=3,
        normalized=True,
    )


def test_hybrid_retrieval() -> None:
    results = [
        make_result(
            "chunk_1",
            "machine learning project",
            0.95,
        ),
        make_result(
            "chunk_2",
            "web development project",
            0.80,
        ),
    ]

    vector_store = FakeVectorStore(
        results
    )

    lexical_store = LexicalStore(
        results
    )

    retriever = HybridRetriever(
        embedding_model=FakeEmbeddingModel(),
        vector_store=vector_store,
        lexical_store=lexical_store,
    )

    ranked = retriever.retrieve(
        query="machine learning",
        top_k=2,
        candidate_k=2,
    )

    assert len(ranked) == 2

    assert (
        ranked[0].chunk_id
        == "chunk_1"
    )

    assert (
        ranked[0].dense_score
        == pytest.approx(0.95)
    )

    assert (
        ranked[0].lexical_score
        > 0
    )

    assert (
        ranked[0].fused_score
        > ranked[1].fused_score
    )


def test_candidate_k_validation() -> None:
    results = [
        make_result(
            "chunk_1",
            "machine learning",
            0.9,
        )
    ]

    retriever = HybridRetriever(
        embedding_model=FakeEmbeddingModel(),
        vector_store=FakeVectorStore(
            results
        ),
        lexical_store=LexicalStore(
            results
        ),
    )

    with pytest.raises(ValueError):
        retriever.retrieve(
            query="machine",
            top_k=5,
            candidate_k=2,
        )


def test_weight_validation() -> None:
    results = [
        make_result(
            "chunk_1",
            "machine learning",
            0.9,
        )
    ]

    with pytest.raises(ValueError):
        HybridRetriever(
            embedding_model=FakeEmbeddingModel(),
            vector_store=FakeVectorStore(
                results
            ),
            lexical_store=LexicalStore(
                results
            ),
            dense_weight=0,
            lexical_weight=0,
        )