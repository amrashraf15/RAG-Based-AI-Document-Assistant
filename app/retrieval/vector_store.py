from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any

from app.models.embedding import EmbeddedChunk
from app.models.search import SearchResult


class VectorStore(ABC):
    @abstractmethod
    def create_collection(
        self,
        vector_size: int,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def collection_exists(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def upsert(
        self,
        chunks: list[EmbeddedChunk],
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        raise NotImplementedError

    @abstractmethod
    def count(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def delete_collection(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def close(self) -> None:
        raise NotImplementedError