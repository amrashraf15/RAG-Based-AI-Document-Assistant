from __future__ import annotations

from typing import Sequence

from app.models.reranking import RerankedResult
from app.models.search import SearchResult
from app.retrieval.reranker import Reranker


class RerankingPipeline:

    def __init__(
        self,
        reranker: Reranker,
    ):
        self.reranker = reranker

    def rerank(
        self,
        query: str,
        results: Sequence[SearchResult],
        top_k: int = 5,
    ) -> list[RerankedResult]:

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

        if not results:
            return []

        scores = self.reranker.rerank(
            query=query,
            results=results,
        )

        if len(scores) != len(results):
            raise RuntimeError(
                "Reranker returned a different number "
                "of scores than input results."
            )

        reranked = [
            RerankedResult(
                chunk_id=result.chunk_id,
                document_id=result.document_id,
                filename=result.filename,
                page_number=result.page_number,
                chunk_index=result.chunk_index,
                text=result.text,
                retrieval_score=result.score,
                reranker_score=score,
                title=result.title,
                source=result.source,
                token_count=result.token_count,
                character_count=result.character_count,
                embedding_model=result.embedding_model,
                embedding_dimension=(
                    result.embedding_dimension
                ),
                normalized=result.normalized,
                reranker_model=(
                    self.reranker.model_name
                ),
            )
            for result, score in zip(
                results,
                scores,
            )
        ]

        reranked.sort(
            key=lambda result: result.reranker_score,
            reverse=True,
        )

        return reranked[:top_k]