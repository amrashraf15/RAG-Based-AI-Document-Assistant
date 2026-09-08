from __future__ import annotations

import hashlib
import re
from typing import Iterable

import tiktoken
from pydantic import BaseModel, Field, field_validator

from app.models.chunk import DocumentChunk, ChunkMetadata
from app.models.document import ProcessedDocument


class ChunkingConfig(BaseModel):
    """
    Configuration for document chunking.
    """

    chunk_size: int = Field(
        default=500,
        gt=0,
        description="Maximum number of tokens per chunk.",
    )

    chunk_overlap: int = Field(
        default=100,
        ge=0,
        description="Number of overlapping tokens between chunks.",
    )

    @field_validator("chunk_overlap")
    @classmethod
    def validate_overlap(cls, value: int, info):
        chunk_size = info.data.get("chunk_size")

        if chunk_size is not None and value >= chunk_size:
            raise ValueError(
                "chunk_overlap must be smaller than chunk_size"
            )

        return value


class Tokenizer:
    """
    Wrapper around tiktoken.
    """

    def __init__(
        self,
        encoding_name: str = "cl100k_base",
    ):
        self.encoding = tiktoken.get_encoding(
            encoding_name
        )

    def encode(self, text: str) -> list[int]:
        return self.encoding.encode(
            text,
            disallowed_special=(),
        )

    def decode(self, tokens: list[int]) -> str:
        return self.encoding.decode(tokens)

    def count(self, text: str) -> int:
        return len(self.encode(text))


class RecursiveTextChunker:
    """
    Splits processed document pages into token-based chunks.

    Important guarantees:

    1. Every chunk has at most `chunk_size` tokens.
    2. Chunk overlap is approximately `chunk_overlap` tokens.
    3. Page metadata is preserved.
    4. Original document text remains untouched.
    """

    def __init__(
        self,
        config: ChunkingConfig | None = None,
        tokenizer: Tokenizer | None = None,
    ):
        self.config = config or ChunkingConfig()
        self.tokenizer = tokenizer or Tokenizer()

    def chunk_document(
        self,
        document: ProcessedDocument,
    ) -> list[DocumentChunk]:
        """
        Chunk every page in the processed document.

        Pages are processed independently so that each chunk
        retains an unambiguous page number for future citations.
        """

        chunks: list[DocumentChunk] = []

        global_chunk_index = 0

        for page in document.pages:
            if not page.clean_text:
                continue

            text = self._normalize_text(
                page.clean_text
            )

            if not text:
                continue

            page_chunks = self._chunk_text(
                text
            )

            for chunk_text in page_chunks:
                token_count = self.tokenizer.count(
                    chunk_text
                )

                # Defensive invariant.
                #
                # This should never fail, but keeping this
                # check here prevents invalid chunks from
                # silently entering the retrieval pipeline.
                if token_count > self.config.chunk_size:
                    raise RuntimeError(
                        "Chunking invariant violated: "
                        f"chunk contains {token_count} tokens "
                        f"but maximum is "
                        f"{self.config.chunk_size}."
                    )

                chunk_id = self._build_chunk_id(
                    document_id=document.document_id,
                    chunk_index=global_chunk_index,
                )

                metadata = ChunkMetadata(
                    document_id=document.document_id,
                    filename=document.filename,
                    page_number=page.page_number,
                    chunk_id=chunk_id,
                    chunk_index=global_chunk_index,
                    title=document.title,
                    source=document.source,
                )

                chunk = DocumentChunk(
                    chunk_id=chunk_id,
                    document_id=document.document_id,
                    filename=document.filename,
                    page_number=page.page_number,
                    chunk_index=global_chunk_index,
                    text=chunk_text,
                    token_count=token_count,
                    character_count=len(chunk_text),
                    title=document.title,
                    source=document.source,
                    metadata=metadata,
                )

                chunks.append(chunk)

                global_chunk_index += 1

        return chunks

    def _chunk_text(
        self,
        text: str,
    ) -> list[str]:
        """
        Split text into overlapping token windows.

        We operate directly on token IDs rather than repeatedly
        splitting strings. This guarantees the requested maximum
        token window size.
        """

        tokens = self.tokenizer.encode(text)

        if not tokens:
            return []

        chunk_size = self.config.chunk_size
        overlap = self.config.chunk_overlap

        # Short text: one chunk.
        if len(tokens) <= chunk_size:
            return [
                self.tokenizer.decode(tokens)
            ]

        step = chunk_size - overlap

        chunks: list[str] = []

        start = 0

        while start < len(tokens):
            end = min(
                start + chunk_size,
                len(tokens),
            )

            token_window = tokens[start:end]

            if not token_window:
                break

            chunk_text = self.tokenizer.decode(
                token_window
            )

            # Re-tokenize the decoded text.
            #
            # Normally this is exactly `len(token_window)`,
            # but tokenization can differ at boundaries.
            actual_tokens = self.tokenizer.encode(
                chunk_text
            )

            # If decoding/re-encoding produced too many
            # tokens, shrink the window until the invariant
            # is guaranteed.
            while (
                len(actual_tokens) > chunk_size
                and len(token_window) > 1
            ):
                token_window = token_window[:-1]

                chunk_text = self.tokenizer.decode(
                    token_window
                )

                actual_tokens = self.tokenizer.encode(
                    chunk_text
                )

            if len(actual_tokens) > chunk_size:
                raise RuntimeError(
                    "Unable to construct a valid chunk "
                    f"with <= {chunk_size} tokens."
                )

            chunks.append(chunk_text)

            # We reached the end of the document.
            if end >= len(tokens):
                break

            # Move forward while preserving overlap.
            start += step

        return chunks

    @staticmethod
    def _normalize_text(
        text: str,
    ) -> str:
        """
        Light normalization before tokenization.

        Heavy cleaning belongs to the Phase 1 cleaner.
        """

        text = text.replace(
            "\r\n",
            "\n",
        )

        text = text.replace(
            "\r",
            "\n",
        )

        # Normalize repeated whitespace while preserving
        # paragraph boundaries.
        text = re.sub(
            r"[ \t]+",
            " ",
            text,
        )

        text = re.sub(
            r"\n{3,}",
            "\n\n",
            text,
        )

        return text.strip()

    @staticmethod
    def _build_chunk_id(
        document_id: str,
        chunk_index: int,
    ) -> str:
        """
        Generate a deterministic chunk ID.

        Example:
            document_id = "doc_test"
            chunk_index = 0

            Result:
            doc_test_chunk_000000
        """

        return (
            f"{document_id}_"
            f"chunk_{chunk_index:06d}"
        )