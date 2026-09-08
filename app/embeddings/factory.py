from __future__ import annotations

from app.embeddings.base import EmbeddingModel
from app.embeddings.huggingface import (
    HuggingFaceEmbeddingModel,
)


def create_embedding_model(
    provider: str = "huggingface",
    model_name: str = "BAAI/bge-small-en-v1.5",
    device: str | None = None,
    batch_size: int = 32,
    normalize_embeddings: bool = True,
) -> EmbeddingModel:
    """
    Create an embedding model based on the configured provider.
    """

    provider = provider.lower().strip()

    if provider == "huggingface":
        return HuggingFaceEmbeddingModel(
            model_name=model_name,
            device=device,
            batch_size=batch_size,
            normalize_embeddings=normalize_embeddings,
        )

    raise ValueError(
        f"Unsupported embedding provider: {provider}"
    )