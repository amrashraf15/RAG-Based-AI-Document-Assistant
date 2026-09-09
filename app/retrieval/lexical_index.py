from __future__ import annotations

from app.models.embedding import EmbeddedChunk
from app.models.search import SearchResult
from app.retrieval.lexical_store import LexicalStore


class LexicalIndexBuilder:

    @staticmethod
    def build(
        chunks: list[EmbeddedChunk],
    ) -> LexicalStore:

        results = [
            SearchResult(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                filename=chunk.filename,
                page_number=chunk.page_number,
                chunk_index=chunk.chunk_index,
                text=chunk.text,
                score=0.0,
                title=chunk.title,
                source=chunk.source,
                token_count=chunk.token_count,
                character_count=chunk.character_count,
                embedding_model=chunk.embedding_model,
                embedding_dimension=(
                    chunk.embedding_dimension
                ),
                normalized=chunk.normalized,
            )
            for chunk in chunks
        ]

        return LexicalStore(
            results=results
        )