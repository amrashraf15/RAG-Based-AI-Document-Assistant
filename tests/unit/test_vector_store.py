from __future__ import annotations

from pathlib import Path

from app.models.embedding import EmbeddedChunk
from app.retrieval.qdrant_store import (
    QdrantVectorStore,
)


def make_chunk(
    chunk_id: str,
    embedding: list[float],
    text: str,
) -> EmbeddedChunk:
    return EmbeddedChunk(
        chunk_id=chunk_id,
        document_id="doc_test",
        filename="test.pdf",
        page_number=1,
        chunk_index=0,
        text=text,
        token_count=10,
        character_count=len(text),
        title="Test",
        source="test.pdf",
        embedding=embedding,
        embedding_model=(
            "BAAI/bge-small-en-v1.5"
        ),
        embedding_dimension=len(
            embedding
        ),
        normalized=True,
    )


def test_create_collection_and_count(
    tmp_path: Path,
) -> None:
    store = QdrantVectorStore(
        collection_name="test_collection",
        path=str(tmp_path / "qdrant"),
    )

    try:
        assert not store.collection_exists()

        store.create_collection(
            vector_size=3
        )

        assert store.collection_exists()
        assert store.count() == 0

    finally:
        store.delete_collection()
        store.close()


def test_upsert_and_search(
    tmp_path: Path,
) -> None:
    store = QdrantVectorStore(
        collection_name="test_collection",
        path=str(tmp_path / "qdrant"),
    )

    chunks = [
        make_chunk(
            chunk_id="chunk_1",
            embedding=[1.0, 0.0, 0.0],
            text="Machine learning project.",
        ),
        make_chunk(
            chunk_id="chunk_2",
            embedding=[0.0, 1.0, 0.0],
            text="Web development project.",
        ),
    ]

    try:
        store.upsert(chunks)

        assert store.count() == 2

        results = store.search(
            query_vector=[1.0, 0.0, 0.0],
            top_k=1,
        )

        assert len(results) == 1

        assert (
            results[0].chunk_id
            == "chunk_1"
        )

        assert (
            results[0].text
            == "Machine learning project."
        )

    finally:
        store.delete_collection()
        store.close()


def test_metadata_filter(
    tmp_path: Path,
) -> None:
    store = QdrantVectorStore(
        collection_name="test_collection",
        path=str(tmp_path / "qdrant"),
    )

    chunk_1 = make_chunk(
        chunk_id="chunk_1",
        embedding=[1.0, 0.0, 0.0],
        text="Document one.",
    )

    # Create the second chunk from the first chunk's
    # serialized data, then override the fields we need.
    chunk_2_data = chunk_1.model_dump(
        mode="python"
    )

    chunk_2_data.update(
        {
            "chunk_id": "chunk_2",
            "document_id": "doc_other",
            "text": "Document two.",
        }
    )

    chunk_2 = EmbeddedChunk(
        **chunk_2_data
    )

    try:
        store.upsert(
            [chunk_1, chunk_2]
        )

        results = store.search(
            query_vector=[1.0, 0.0, 0.0],
            top_k=5,
            filters={
                "document_id": "doc_other"
            },
        )

        assert len(results) == 1

        assert (
            results[0].document_id
            == "doc_other"
        )

        assert (
            results[0].chunk_id
            == "chunk_2"
        )

        assert (
            results[0].text
            == "Document two."
        )

    finally:
        store.delete_collection()
        store.close()


def test_empty_search_when_collection_missing(
    tmp_path: Path,
) -> None:
    store = QdrantVectorStore(
        collection_name="missing",
        path=str(tmp_path / "qdrant"),
    )

    try:
        results = store.search(
            query_vector=[1.0, 0.0, 0.0],
            top_k=5,
        )

        assert results == []

    finally:
        store.close()