from __future__ import annotations

import pytest

from app.models.search import SearchResult
from app.retrieval.sentence_transformer_reranker import (
    SentenceTransformerReranker,
)


@pytest.mark.integration
def test_real_reranker() -> None:
    reranker = SentenceTransformerReranker(
        model_name=(
            "cross-encoder/"
            "ms-marco-MiniLM-L-6-v2"
        ),
        batch_size=2,
    )

    results = [
        SearchResult(
            chunk_id="chunk_1",
            document_id="doc_test",
            filename="test.pdf",
            page_number=1,
            chunk_index=0,
            text=(
                "Machine learning is a field "
                "of artificial intelligence."
            ),
            score=0.8,
            title=None,
            source="test.pdf",
            token_count=10,
            character_count=60,
            embedding_model=(
                "BAAI/bge-small-en-v1.5"
            ),
            embedding_dimension=384,
            normalized=True,
        ),
        SearchResult(
            chunk_id="chunk_2",
            document_id="doc_test",
            filename="test.pdf",
            page_number=2,
            chunk_index=1,
            text=(
                "Python is commonly used for "
                "web development."
            ),
            score=0.7,
            title=None,
            source="test.pdf",
            token_count=10,
            character_count=50,
            embedding_model=(
                "BAAI/bge-small-en-v1.5"
            ),
            embedding_dimension=384,
            normalized=True,
        ),
    ]

    scores = reranker.rerank(
        query="What is machine learning?",
        results=results,
    )

    assert len(scores) == 2
    assert all(
        isinstance(score, float)
        for score in scores
    )