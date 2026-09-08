from __future__ import annotations

import pytest

from app.embeddings.base import EmbeddingModel
from app.embeddings.pipeline import EmbeddingPipeline
from app.models.chunk import (
    ChunkMetadata,
    DocumentChunk,
)


class FakeEmbeddingModel(
    EmbeddingModel
):
    def __init__(
        self,
        dimension: int = 4,
    ):
        self._dimension = dimension

    @property
    def model_name(self) -> str:
        return "fake-model"

    @property
    def dimension(self) -> int:
        return self._dimension

    def embed_documents(
        self,
        texts,
    ):
        return [
            [float(i)] * self.dimension
            for i in range(len(texts))
        ]

    def embed_query(
        self,
        text: str,
    ):
        return [1.0] * self.dimension


def create_chunk(
    index: int = 0,
) -> DocumentChunk:

    return DocumentChunk(
        chunk_id=(
            f"doc_test_chunk_{index:06d}"
        ),
        document_id="doc_test",
        filename="test.pdf",
        page_number=1,
        chunk_index=index,
        text="Machine learning is useful.",
        token_count=5,
        character_count=30,
        title="Test Document",
        source="test.pdf",
        metadata=ChunkMetadata(
            document_id="doc_test",
            filename="test.pdf",
            page_number=1,
            chunk_id=(
                f"doc_test_chunk_{index:06d}"
            ),
            chunk_index=index,
            title="Test Document",
            source="test.pdf",
        ),
    )


def test_embedding_model_interface():
    model = FakeEmbeddingModel(
        dimension=4
    )

    assert model.model_name == "fake-model"
    assert model.dimension == 4

    embeddings = model.embed_documents(
        ["hello", "world"]
    )

    assert len(embeddings) == 2
    assert len(embeddings[0]) == 4


def test_query_embedding():
    model = FakeEmbeddingModel(
        dimension=8
    )

    embedding = model.embed_query(
        "machine learning"
    )

    assert len(embedding) == 8


def test_embedding_pipeline():
    model = FakeEmbeddingModel(
        dimension=4
    )

    pipeline = EmbeddingPipeline(
        embedding_model=model
    )

    chunks = [
        create_chunk(0),
        create_chunk(1),
        create_chunk(2),
    ]

    embedded = pipeline.embed_chunks(
        chunks
    )

    assert len(embedded) == 3

    assert (
        embedded[0].chunk_id
        == "doc_test_chunk_000000"
    )

    assert (
        embedded[0].document_id
        == "doc_test"
    )

    assert (
        embedded[0].page_number
        == 1
    )

    assert (
        embedded[0].embedding_model
        == "fake-model"
    )

    assert (
        embedded[0].embedding_dimension
        == 4
    )

    assert len(
        embedded[0].embedding
    ) == 4


def test_empty_chunks():
    model = FakeEmbeddingModel()

    pipeline = EmbeddingPipeline(
        embedding_model=model
    )

    result = pipeline.embed_chunks([])

    assert result == []


def test_invalid_embedding_dimension():
    class BadEmbeddingModel(
        FakeEmbeddingModel
    ):
        @property
        def dimension(self):
            return 4

        def embed_documents(
            self,
            texts,
        ):
            return [
                [1.0, 2.0]
                for _ in texts
            ]

    pipeline = EmbeddingPipeline(
        embedding_model=BadEmbeddingModel()
    )

    with pytest.raises(
        RuntimeError,
        match="Embedding dimension mismatch",
    ):
        pipeline.embed_chunks(
            [create_chunk()]
        )