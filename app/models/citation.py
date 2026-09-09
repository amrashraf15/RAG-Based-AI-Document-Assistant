from __future__ import annotations

from pydantic import BaseModel, Field


class Citation(BaseModel):
    citation_id: str

    chunk_id: str
    document_id: str

    filename: str

    page_number: int = Field(ge=1)

    text: str

    title: str | None = None
    source: str