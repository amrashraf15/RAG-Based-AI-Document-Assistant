from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence

from app.models.search import SearchResult


class Reranker(ABC):

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @property
    @abstractmethod
    def batch_size(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def rerank(
        self,
        query: str,
        results: Sequence[SearchResult],
    ) -> list[float]:
        raise NotImplementedError