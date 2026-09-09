from __future__ import annotations

import uuid
from typing import Any

from qdrant_client import QdrantClient, models

from app.models.embedding import EmbeddedChunk
from app.models.search import SearchResult
from app.retrieval.vector_store import VectorStore


class QdrantVectorStore(VectorStore):
    def __init__(
        self,
        collection_name: str,
        path: str | None = None,
        url: str | None = None,
        api_key: str | None = None,
        timeout: float = 30.0,
    ):
        if not collection_name.strip():
            raise ValueError(
                "collection_name cannot be empty."
            )

        if path and url:
            raise ValueError(
                "Use either path or url, not both."
            )

        self.collection_name = collection_name

        if url and url.strip():
            self.client = QdrantClient(
                url=url.strip(),
                api_key=api_key,
                timeout=timeout,
            )
        else:
            if not path:
                raise ValueError(
                    "A Qdrant path or URL is required."
                )

            self.client = QdrantClient(
                path=path,
            )

    def create_collection(
        self,
        vector_size: int,
    ) -> None:
        if vector_size <= 0:
            raise ValueError(
                "vector_size must be greater than zero."
            )

        if self.collection_exists():
            existing = (
                self.client.get_collection(
                    self.collection_name
                )
            )

            existing_size = (
                existing.config.params.vectors.size
            )

            if existing_size != vector_size:
                raise ValueError(
                    "Existing collection vector size "
                    f"is {existing_size}, but received "
                    f"{vector_size}."
                )

            return

        self.client.create_collection(
            collection_name=self.collection_name,
            vectors_config=models.VectorParams(
                size=vector_size,
                distance=models.Distance.COSINE,
            ),
        )

    def collection_exists(self) -> bool:
        return self.client.collection_exists(
            collection_name=self.collection_name,
        )

    def upsert(
        self,
        chunks: list[EmbeddedChunk],
    ) -> None:
        if not chunks:
            return

        vector_dimension = (
            chunks[0].embedding_dimension
        )

        for chunk in chunks:
            if (
                len(chunk.embedding)
                != vector_dimension
            ):
                raise ValueError(
                    "All embeddings must have the "
                    "same dimension."
                )

            if (
                chunk.embedding_dimension
                != vector_dimension
            ):
                raise ValueError(
                    "Embedding metadata dimension "
                    "does not match vector dimension."
                )

        self.create_collection(
            vector_size=vector_dimension,
        )

        points = [
            models.PointStruct(
                id=self._point_id(
                    chunk.chunk_id
                ),
                vector=chunk.embedding,
                payload=self._build_payload(
                    chunk
                ),
            )
            for chunk in chunks
        ]

        self.client.upsert(
            collection_name=self.collection_name,
            points=points,
            wait=True,
        )

    def search(
        self,
        query_vector: list[float],
        top_k: int = 5,
        filters: dict[str, Any] | None = None,
    ) -> list[SearchResult]:
        if not query_vector:
            raise ValueError(
                "query_vector cannot be empty."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        if not self.collection_exists():
            return []

        query_filter = self._build_filter(
            filters
        )

        response = self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            query_filter=query_filter,
            limit=top_k,
            with_payload=True,
        )

        results: list[SearchResult] = []

        for point in response.points:
            payload = point.payload or {}

            results.append(
                SearchResult(
                    chunk_id=payload["chunk_id"],
                    document_id=payload[
                        "document_id"
                    ],
                    filename=payload["filename"],
                    page_number=payload[
                        "page_number"
                    ],
                    chunk_index=payload[
                        "chunk_index"
                    ],
                    text=payload["text"],
                    score=float(point.score),
                    title=payload.get("title"),
                    source=payload["source"],
                    token_count=payload[
                        "token_count"
                    ],
                    character_count=payload[
                        "character_count"
                    ],
                    embedding_model=payload[
                        "embedding_model"
                    ],
                    embedding_dimension=payload[
                        "embedding_dimension"
                    ],
                    normalized=payload.get(
                        "normalized",
                        True,
                    ),
                )
            )

        return results

    def count(self) -> int:
        if not self.collection_exists():
            return 0

        result = self.client.count(
            collection_name=self.collection_name,
            exact=True,
        )

        return result.count

    def delete_collection(self) -> None:
        if self.collection_exists():
            self.client.delete_collection(
                collection_name=self.collection_name,
            )

    def close(self) -> None:
        self.client.close()

    @staticmethod
    def _point_id(
        chunk_id: str,
    ) -> str:
        return str(
            uuid.uuid5(
                uuid.NAMESPACE_URL,
                f"rag-document-assistant:{chunk_id}",
            )
        )

    @staticmethod
    def _build_payload(
        chunk: EmbeddedChunk,
    ) -> dict[str, Any]:
        return {
            "chunk_id": chunk.chunk_id,
            "document_id": chunk.document_id,
            "filename": chunk.filename,
            "page_number": chunk.page_number,
            "chunk_index": chunk.chunk_index,
            "text": chunk.text,
            "title": chunk.title,
            "source": chunk.source,
            "token_count": chunk.token_count,
            "character_count": chunk.character_count,
            "embedding_model": (
                chunk.embedding_model
            ),
            "embedding_dimension": (
                chunk.embedding_dimension
            ),
            "normalized": chunk.normalized,
        }

    @staticmethod
    def _build_filter(
        filters: dict[str, Any] | None,
    ) -> models.Filter | None:
        if not filters:
            return None

        conditions: list[models.FieldCondition] = []

        for field, value in filters.items():
            if value is None:
                continue

            conditions.append(
                models.FieldCondition(
                    key=field,
                    match=models.MatchValue(
                        value=value
                    ),
                )
            )

        if not conditions:
            return None

        return models.Filter(
            must=conditions,
        )