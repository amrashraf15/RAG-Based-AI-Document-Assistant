from __future__ import annotations

from typing import Any

from app.embeddings.base import EmbeddingModel
from app.models.search import SearchResult
from app.retrieval.vector_store import VectorStore


class SemanticRetriever:
    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
    ):
        self.embedding_model = embedding_model
        self.vector_store = vector_store

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        if not isinstance(query, str):
            raise TypeError(
                "Query must be a string."
            )

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        query_vector = (
            self.embedding_model.embed_query(
                query
            )
        )

        return self.vector_store.search(
            query_vector=query_vector,
            top_k=top_k,
            filters=filters,
        )