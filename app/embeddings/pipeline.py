from __future__ import annotations

import json
from pathlib import Path

from app.embeddings.base import EmbeddingModel
from app.models.chunk import DocumentChunk
from app.models.embedding import EmbeddedChunk


class EmbeddingPipeline:
    """
    Converts DocumentChunk objects into EmbeddedChunk objects.
    """

    def __init__(
        self,
        embedding_model: EmbeddingModel,
    ):
        self.embedding_model = embedding_model

    def embed_chunks(
        self,
        chunks: list[DocumentChunk],
    ) -> list[EmbeddedChunk]:
        """
        Generate embeddings for all document chunks.
        """

        if not chunks:
            return []

        texts = [
            chunk.text
            for chunk in chunks
        ]

        embeddings = (
            self.embedding_model.embed_documents(
                texts
            )
        )

        if len(embeddings) != len(chunks):
            raise RuntimeError(
                "Embedding model returned a different "
                "number of embeddings than input chunks."
            )

        embedded_chunks: list[EmbeddedChunk] = []

        for chunk, embedding in zip(
            chunks,
            embeddings,
        ):
            if (
                len(embedding)
                != self.embedding_model.dimension
            ):
                raise RuntimeError(
                    "Embedding dimension mismatch."
                )

            embedded_chunks.append(
                EmbeddedChunk(
                    chunk_id=chunk.chunk_id,
                    document_id=chunk.document_id,
                    filename=chunk.filename,
                    page_number=chunk.page_number,
                    chunk_index=chunk.chunk_index,
                    text=chunk.text,
                    token_count=chunk.token_count,
                    character_count=chunk.character_count,
                    title=chunk.title,
                    source=chunk.source,
                    embedding=embedding,
                    embedding_model=(
                        self.embedding_model.model_name
                    ),
                    embedding_dimension=(
                        self.embedding_model.dimension
                    ),
                    normalized=(
                        self.embedding_model.normalized
                    ),
                )
            )

        return embedded_chunks

    @staticmethod
    def save_embeddings(
        chunks: list[EmbeddedChunk],
        output_path: Path,
    ) -> None:
        """
        Save embedded chunks to JSON.
        """

        output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        data = [
            chunk.model_dump(
                mode="json"
            )
            for chunk in chunks
        ]

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:
            json.dump(
                data,
                file,
                ensure_ascii=False,
                indent=2,
            )