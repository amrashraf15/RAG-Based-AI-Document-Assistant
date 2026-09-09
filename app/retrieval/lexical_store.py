from __future__ import annotations

from typing import Any

from app.models.search import SearchResult
from app.retrieval.bm25 import BM25


class LexicalStore:
    """
    In-memory lexical index over SearchResult documents.

    The initial implementation intentionally keeps the
    lexical index in memory. Later we can replace this
    with Elasticsearch/OpenSearch without changing the
    hybrid retrieval interface.
    """

    def __init__(
        self,
        results: list[SearchResult],
        k1: float = 1.5,
        b: float = 0.75,
    ) -> None:
        self.results = list(results)

        self.bm25 = BM25(
            documents=[
                result.text
                for result in self.results
            ],
            k1=k1,
            b=b,
        )

    def search(
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

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        candidate_indices = self.bm25.top_k(
            query=query,
            k=len(self.results),
        )

        filtered_results: list[
            SearchResult
        ] = []

        for index, _score in candidate_indices:
            result = self.results[index]

            if self._matches_filters(
                result,
                filters,
            ):
                filtered_results.append(result)

        return filtered_results[:top_k]

    def score(
        self,
        query: str,
    ) -> list[float]:
        return self.bm25.score(query)

    def add_results(
        self,
        results: list[SearchResult],
    ) -> None:
        self.results.extend(results)

        self.bm25 = BM25(
            documents=[
                result.text
                for result in self.results
            ],
            k1=self.bm25.k1,
            b=self.bm25.b,
        )

    @staticmethod
    def _matches_filters(
        result: SearchResult,
        filters: dict[str, Any] | None,
    ) -> bool:
        if not filters:
            return True

        for field, expected_value in filters.items():
            if expected_value is None:
                continue

            actual_value = getattr(
                result,
                field,
                None,
            )

            if actual_value != expected_value:
                return False

        return True