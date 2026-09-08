from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Sequence


class EmbeddingModel(ABC):
    """
    Abstract interface for embedding models.

    The rest of the RAG system depends on this interface rather
    than directly depending on a specific embedding provider.
    """

    @property
    @abstractmethod
    def model_name(self) -> str:
        """
        Return the model identifier.
        """
        raise NotImplementedError

    @property
    @abstractmethod
    def dimension(self) -> int:
        """
        Return the dimensionality of the embedding vectors.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_documents(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:
        """
        Generate embeddings for multiple documents/chunks.
        """
        raise NotImplementedError

    @abstractmethod
    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        """
        Generate an embedding for a search query.
        """
        raise NotImplementedError

    def embed_texts(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:
        """
        Convenience alias for document embedding.
        """
        return self.embed_documents(texts)