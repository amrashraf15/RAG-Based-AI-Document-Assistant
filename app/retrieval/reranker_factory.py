from __future__ import annotations

from app.retrieval.reranker import Reranker
from app.retrieval.sentence_transformer_reranker import (
    SentenceTransformerReranker,
)


def create_reranker(
    provider: str = "sentence_transformers",
    model_name: str = (
        "cross-encoder/ms-marco-MiniLM-L-6-v2"
    ),
    device: str | None = None,
    batch_size: int = 16,
) -> Reranker:

    provider = provider.lower().strip()

    if provider == "sentence_transformers":
        return SentenceTransformerReranker(
            model_name=model_name,
            device=device,
            batch_size=batch_size,
        )

    raise ValueError(
        f"Unsupported reranker provider: {provider}"
    )