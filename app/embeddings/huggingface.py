from __future__ import annotations

from typing import Sequence

from sentence_transformers import SentenceTransformer
from torch import device

from app.embeddings.base import EmbeddingModel


class HuggingFaceEmbeddingModel(
    EmbeddingModel
):
    """
    Sentence Transformers / Hugging Face embedding implementation.
    """

    def __init__(
        self,
        model_name: str = "BAAI/bge-small-en-v1.5",
        device: str | None = None,
        batch_size: int = 32,
        normalize_embeddings: bool = True,
    ):
        if batch_size <= 0:
            raise ValueError(
                "batch_size must be greater than zero."
            )

        self._model_name = model_name
        self.batch_size = batch_size
        self.normalize_embeddings = (
            normalize_embeddings
        )

        model_kwargs = {}

        if device and device.strip():
            model_kwargs["device"] = device.strip()

        self.model = SentenceTransformer(
            model_name,
            **model_kwargs,
        )

        self._dimension = (
            self.model.get_sentence_embedding_dimension()
        )

        if self._dimension is None:
            raise RuntimeError(
                "Unable to determine embedding dimension."
            )

    @property
    def model_name(self) -> str:
        return self._model_name

    @property
    def dimension(self) -> int:
        return int(self._dimension)

    def embed_documents(
        self,
        texts: Sequence[str],
    ) -> list[list[float]]:
        """
        Embed multiple document chunks.
        """

        if not texts:
            return []

        self._validate_texts(texts)

        embeddings = self.model.encode(
            list(texts),
            batch_size=self.batch_size,
            normalize_embeddings=self.normalize_embeddings,
            convert_to_numpy=True,
            show_progress_bar=False,
        )

        return embeddings.tolist()

    def embed_query(
        self,
        text: str,
    ) -> list[float]:
        """
        Embed a single search query.
        """

        if not isinstance(text, str):
            raise TypeError(
                "Query text must be a string."
            )

        if not text.strip():
            raise ValueError(
                "Query text cannot be empty."
            )

        embedding = self.model.encode(
            [text],
            batch_size=1,
            normalize_embeddings=self.normalize_embeddings,
            convert_to_numpy=True,
            show_progress_bar=False,
        )[0]

        return embedding.tolist()

    @staticmethod
    def _validate_texts(
        texts: Sequence[str],
    ) -> None:
        """
        Validate document texts before embedding.
        """

        for index, text in enumerate(texts):
            if not isinstance(text, str):
                raise TypeError(
                    f"Text at index {index} must be a string."
                )

            if not text.strip():
                raise ValueError(
                    f"Text at index {index} cannot be empty."
                )