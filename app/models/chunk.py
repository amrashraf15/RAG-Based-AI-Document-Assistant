from typing import Optional

from pydantic import BaseModel, Field


class ChunkMetadata(BaseModel):
    """
    Metadata associated with an individual chunk.

    This metadata will eventually be stored alongside the
    chunk embedding in the vector database.
    """

    document_id: str
    filename: str
    page_number: int = Field(ge=1)

    chunk_id: str
    chunk_index: int = Field(ge=0)

    title: Optional[str] = None
    source: str


class DocumentChunk(BaseModel):
    """
    Represents one retrieval-ready text chunk.
    """

    chunk_id: str

    document_id: str

    filename: str

    page_number: int = Field(ge=1)

    chunk_index: int = Field(ge=0)

    text: str

    token_count: int = Field(ge=0)

    character_count: int = Field(ge=0)

    title: Optional[str] = None

    source: str

    metadata: ChunkMetadata