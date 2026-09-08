from datetime import datetime, timezone
from typing import List, Optional

from pydantic import BaseModel, Field


class PageMetadata(BaseModel):
    """
    Metadata associated with a single PDF page.
    """

    document_id: str
    filename: str
    page_number: int = Field(ge=1)
    title: Optional[str] = None
    source: str


class PageDocument(BaseModel):
    """
    Represents one extracted PDF page.

    raw_text:
        Original text extracted directly from the PDF.

    clean_text:
        Text after our cleaning pipeline.

    Keeping both allows us to reproduce and debug preprocessing decisions.
    """

    document_id: str
    filename: str
    page_number: int = Field(ge=1)

    raw_text: str
    clean_text: str

    title: Optional[str] = None
    source: str

    character_count: int = Field(default=0, ge=0)

    metadata: PageMetadata


class DocumentMetadata(BaseModel):
    """
    Metadata describing the entire PDF document.
    """

    document_id: str
    filename: str
    source: str

    title: Optional[str] = None

    page_count: int = Field(default=0, ge=0)
    extracted_character_count: int = Field(default=0, ge=0)
    cleaned_character_count: int = Field(default=0, ge=0)

    processed_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc)
    )


class ProcessedDocument(BaseModel):
    """
    Complete processed document.

    This is the output of Phase 1.
    """

    document_id: str
    filename: str
    source: str

    title: Optional[str] = None

    pages: List[PageDocument]

    metadata: DocumentMetadata

    @property
    def page_count(self) -> int:
        return len(self.pages)

    @property
    def character_count(self) -> int:
        return sum(page.character_count for page in self.pages)