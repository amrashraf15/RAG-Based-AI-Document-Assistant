from __future__ import annotations

from typing import Any

from app.embeddings.base import EmbeddingModel
from app.models.search import SearchResult
from app.retrieval.retriever import (
    SemanticRetriever,
)
from app.retrieval.vector_store import (
    VectorStore,
)


class FakeEmbeddingModel(
    EmbeddingModel
):
    @property
    def model_name(self) -> str:
        return "fake-model"

    @property
    def dimension(self) -> int:
        return 3

    def embed_documents(
        self,
        texts: list[str],
    ) -> list[list[float]]:
        return [
            [1.0, 0.0, 0.0]
            for _ in texts
        ]

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        return [1.0, 0.0, 0.0]


class FakeVectorStore(
    VectorStore
):
    def __init__(self) -> None:
        self.last_query_vector = None
        self.last_top_k = None
        self.last_filters = None

    def create_collection(
        self,
        vector_size: int,
    ) -> None:
        pass

    def collection_exists(
        self,
    ) -> bool:
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
        self.last_query_vector = query_vector
        self.last_top_k = top_k
        self.last_filters = filters

        return [
            SearchResult(
                chunk_id="chunk_1",
                document_id="doc_1",
                filename="test.pdf",
                page_number=1,
                chunk_index=0,
                text="Test result",
                score=0.95,
                title="Test",
                source="test.pdf",
                token_count=5,
                character_count=11,
                embedding_model="fake-model",
                embedding_dimension=3,
                normalized=True,
            )
        ]

    def count(self) -> int:
        return 1

    def delete_collection(self) -> None:
        pass

    def close(self) -> None:
        pass


def test_retriever_embeds_query() -> None:
    embedding_model = (
        FakeEmbeddingModel()
    )

    vector_store = (
        FakeVectorStore()
    )

    retriever = SemanticRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    results = retriever.retrieve(
        query="machine learning",
        top_k=3,
    )

    assert len(results) == 1

    assert (
        vector_store.last_query_vector
        == [1.0, 0.0, 0.0]
    )

    assert (
        vector_store.last_top_k
        == 3
    )


def test_retriever_passes_filters() -> None:
    embedding_model = (
        FakeEmbeddingModel()
    )

    vector_store = (
        FakeVectorStore()
    )

    retriever = SemanticRetriever(
        embedding_model=embedding_model,
        vector_store=vector_store,
    )

    filters = {
        "document_id": "doc_123"
    }

    retriever.retrieve(
        query="test",
        top_k=5,
        filters=filters,
    )

    assert (
        vector_store.last_filters
        == filters
    )


def test_retriever_rejects_empty_query() -> None:
    retriever = SemanticRetriever(
        embedding_model=FakeEmbeddingModel(),
        vector_store=FakeVectorStore(),
    )

    try:
        retriever.retrieve("")
        assert False
    except ValueError:
        assert True