from __future__ import annotations

from typing import Any

from app.models.search import SearchResult
from app.models.hybrid import HybridSearchResult
from app.retrieval.lexical_store import LexicalStore
from app.retrieval.vector_store import VectorStore
from app.embeddings.base import EmbeddingModel


class HybridRetriever:
    """
    Combines dense semantic retrieval with lexical BM25
    retrieval using weighted reciprocal rank fusion.
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel,
        vector_store: VectorStore,
        lexical_store: LexicalStore,
        dense_weight: float = 0.5,
        lexical_weight: float = 0.5,
        rrf_k: int = 60,
    ) -> None:
        if dense_weight < 0:
            raise ValueError(
                "dense_weight must be non-negative."
            )

        if lexical_weight < 0:
            raise ValueError(
                "lexical_weight must be non-negative."
            )

        if dense_weight + lexical_weight <= 0:
            raise ValueError(
                "At least one retrieval weight must be positive."
            )

        if rrf_k <= 0:
            raise ValueError(
                "rrf_k must be greater than zero."
            )

        self.embedding_model = embedding_model
        self.vector_store = vector_store
        self.lexical_store = lexical_store

        self.dense_weight = dense_weight
        self.lexical_weight = lexical_weight
        self.rrf_k = rrf_k

    def retrieve(
        self,
        query: str,
        top_k: int = 5,
        candidate_k: int = 20,
        filters: dict[str, Any] | None = None,
    ) -> list[HybridSearchResult]:

        if not isinstance(query, str):
            raise TypeError(
                "Query must be a string."
            )

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        if candidate_k <= 0:
            raise ValueError(
                "candidate_k must be greater than zero."
            )

        if candidate_k < top_k:
            raise ValueError(
                "candidate_k must be greater than "
                "or equal to top_k."
            )

        query_vector = (
            self.embedding_model.embed_query(
                query
            )
        )

        dense_results = self.vector_store.search(
            query_vector=query_vector,
            top_k=candidate_k,
            filters=filters,
        )

        lexical_results = self.lexical_store.search(
            query=query,
            top_k=candidate_k,
            filters=filters,
        )

        dense_rank = {
            result.chunk_id: index + 1
            for index, result
            in enumerate(dense_results)
        }

        lexical_rank = {
            result.chunk_id: index + 1
            for index, result
            in enumerate(lexical_results)
        }

        lexical_scores = (
            self.lexical_store.score(query)
        )

        lexical_score_by_chunk_id = {
            result.chunk_id: lexical_scores[index]
            for index, result
            in enumerate(
                self.lexical_store.results
            )
        }

        by_chunk_id: dict[
            str,
            SearchResult,
        ] = {}

        for result in dense_results:
            by_chunk_id[
                result.chunk_id
            ] = result

        for result in lexical_results:
            by_chunk_id[
                result.chunk_id
            ] = result

        fused_results = []

        for chunk_id, result in by_chunk_id.items():

            dense_score = result.score

            lexical_score = (
                lexical_score_by_chunk_id.get(
                    chunk_id,
                    0.0,
                )
            )

            fused_score = (
                self.dense_weight
                * self._rrf_score(
                    dense_rank.get(chunk_id)
                )
                + self.lexical_weight
                * self._rrf_score(
                    lexical_rank.get(chunk_id)
                )
            )

            fused_results.append(
                HybridSearchResult(
                    chunk_id=result.chunk_id,
                    document_id=result.document_id,
                    filename=result.filename,
                    page_number=result.page_number,
                    chunk_index=result.chunk_index,
                    text=result.text,
                    dense_score=dense_score,
                    lexical_score=lexical_score,
                    fused_score=fused_score,
                    title=result.title,
                    source=result.source,
                    token_count=result.token_count,
                    character_count=result.character_count,
                    embedding_model=result.embedding_model,
                    embedding_dimension=(
                        result.embedding_dimension
                    ),
                    normalized=result.normalized,
                )
            )

        fused_results.sort(
            key=lambda result: result.fused_score,
            reverse=True,
        )

        return fused_results[:top_k]

    def _rrf_score(
        self,
        rank: int | None,
    ) -> float:
        if rank is None:
            return 0.0

        return 1.0 / (
            self.rrf_k + rank
        )