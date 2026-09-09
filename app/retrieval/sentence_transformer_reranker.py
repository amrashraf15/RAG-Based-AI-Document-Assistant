from __future__ import annotations

from typing import Sequence

from sentence_transformers import CrossEncoder

from app.models.search import SearchResult
from app.retrieval.reranker import Reranker


class SentenceTransformerReranker(Reranker):

    def __init__(
        self,
        model_name: str = (
            "cross-encoder/ms-marco-MiniLM-L-6-v2"
        ),
        device: str | None = None,
        batch_size: int = 16,
    ):
        if not model_name.strip():
            raise ValueError(
                "model_name cannot be empty."
            )

        if batch_size <= 0:
            raise ValueError(
                "batch_size must be greater than zero."
            )

        self._model_name = model_name
        self._batch_size = batch_size

        model_kwargs = {}

        if device and device.strip():
            model_kwargs["device"] = device.strip()

        self.model = CrossEncoder(
            model_name,
            **model_kwargs,
        )

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def batch_size(self) -> int:
        return self._batch_size

    def rerank(
        self,
        query: str,
        results: Sequence[SearchResult],
    ) -> list[float]:

        if not isinstance(query, str):
            raise TypeError(
                "Query must be a string."
            )

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        if not results:
            return []

        pairs = [
            [query, result.text]
            for result in results
        ]

        scores = self.model.predict(
            pairs,
            batch_size=self.batch_size,
            show_progress_bar=False,
        )

        return [
            float(score)
            for score in scores
        ]