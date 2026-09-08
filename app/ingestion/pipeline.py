import hashlib
import json
from pathlib import Path
from typing import List, Optional

from app.core.config import ensure_directories, settings
from app.core.exceptions import EmptyPDFError, PDFSizeLimitError
from app.ingestion.cleaner import TextCleaner
from app.ingestion.chunker import (
    ChunkingConfig,
    RecursiveTextChunker,
)
from app.ingestion.loader import PDFLoader
from app.models.chunk import DocumentChunk
from app.models.document import (
    DocumentMetadata,
    ProcessedDocument,
)


class DocumentIngestionPipeline:
    """
    End-to-end document ingestion pipeline.

    Phase 1:
        PDF → pages → cleaned document

    Phase 2:
        cleaned document → chunks
    """

    def __init__(
        self,
        cleaner: Optional[TextCleaner] = None,
        chunker: Optional[RecursiveTextChunker] = None,
    ):
        self.cleaner = cleaner or TextCleaner()

        self.chunker = chunker or RecursiveTextChunker(
            config=ChunkingConfig(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap,
            )
        )

        ensure_directories()

    def process(
        self,
        file_path: Path,
    ) -> ProcessedDocument:
        """
        Phase 1 document processing.

        PDF
        ↓
        validation
        ↓
        extraction
        ↓
        cleaning
        ↓
        ProcessedDocument
        """

        file_path = Path(file_path)

        self._validate_file(file_path)

        document_id = self._generate_document_id(
            file_path
        )

        source = str(file_path.resolve())

        loader = PDFLoader(
            document_id=document_id,
            source=source,
        )

        pages = loader.load(file_path)

        pages = self.cleaner.clean_document(pages)

        meaningful_pages = [
            page
            for page in pages
            if not self.cleaner.is_empty(
                page.clean_text
            )
        ]

        if not meaningful_pages:
            raise EmptyPDFError(
                f"No meaningful text could be extracted "
                f"from: {file_path.name}"
            )

        extracted_character_count = sum(
            len(page.raw_text)
            for page in pages
        )

        cleaned_character_count = sum(
            len(page.clean_text)
            for page in pages
        )

        title = self._extract_title(
            file_path=file_path,
            pages=pages,
        )

        updated_pages = []

        for page in pages:
            updated_page = page.model_copy(
                update={
                    "title": title,
                    "metadata": page.metadata.model_copy(
                        update={
                            "title": title,
                        }
                    ),
                }
            )

            updated_pages.append(updated_page)

        pages = updated_pages

        metadata = DocumentMetadata(
            document_id=document_id,
            filename=file_path.name,
            source=source,
            title=title,
            page_count=len(pages),
            extracted_character_count=(
                extracted_character_count
            ),
            cleaned_character_count=(
                cleaned_character_count
            ),
        )

        document = ProcessedDocument(
            document_id=document_id,
            filename=file_path.name,
            source=source,
            title=title,
            pages=pages,
            metadata=metadata,
        )

        self._save_processed_document(document)

        return document

    def create_chunks(
        self,
        document: ProcessedDocument,
    ) -> List[DocumentChunk]:
        """
        Phase 2 chunking.

        ProcessedDocument
        ↓
        DocumentChunk[]
        """

        chunks = self.chunker.chunk_document(
            document
        )

        self._save_chunks(
            document=document,
            chunks=chunks,
        )

        return chunks

    def process_with_chunks(
        self,
        file_path: Path,
    ) -> tuple[
        ProcessedDocument,
        List[DocumentChunk],
    ]:
        """
        Run Phase 1 + Phase 2.

        Returns:
            (ProcessedDocument, chunks)
        """

        document = self.process(file_path)

        chunks = self.create_chunks(
            document
        )

        return document, chunks

    def _validate_file(
        self,
        file_path: Path,
    ) -> None:

        if not file_path.exists():
            raise FileNotFoundError(
                f"File does not exist: {file_path}"
            )

        if not file_path.is_file():
            raise ValueError(
                f"Input path is not a file: {file_path}"
            )

        if (
            file_path.suffix.lower()
            != settings.allowed_file_extension
        ):
            raise ValueError(
                "Only PDF files are supported."
            )

        file_size = file_path.stat().st_size

        if file_size > settings.max_pdf_size_bytes:
            raise PDFSizeLimitError(
                f"PDF exceeds maximum allowed size "
                f"of {settings.max_pdf_size_mb} MB."
            )

        if file_size == 0:
            raise ValueError(
                "PDF file is empty."
            )

    def _generate_document_id(
        self,
        file_path: Path,
    ) -> str:
        """
        Generate deterministic document ID from file contents.
        """

        hasher = hashlib.sha256()

        with file_path.open("rb") as file:
            while chunk := file.read(
                1024 * 1024
            ):
                hasher.update(chunk)

        return (
            f"doc_{hasher.hexdigest()[:16]}"
        )

    def _extract_title(
        self,
        file_path: Path,
        pages,
    ) -> Optional[str]:

        if pages:
            first_page_text = pages[0].clean_text

            lines = [
                line.strip()
                for line in first_page_text.split("\n")
                if line.strip()
            ]

            if lines:
                first_line = lines[0]

                if 3 <= len(first_line) <= 150:
                    return first_line

        return file_path.stem

    def _save_processed_document(
        self,
        document: ProcessedDocument,
    ) -> Path:

        output_path = (
            settings.processed_dir
            / f"{document.document_id}.json"
        )

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                document.model_dump(mode="json"),
                file,
                indent=2,
                ensure_ascii=False,
            )

        return output_path

    def _save_chunks(
        self,
        document: ProcessedDocument,
        chunks: List[DocumentChunk],
    ) -> Path:
        """
        Save chunks separately from the original document.

        This keeps Phase 1 output independent from Phase 2 output.
        """

        output_path = (
            settings.processed_dir
            / f"{document.document_id}_chunks.json"
        )

        payload = {
            "document_id": document.document_id,
            "filename": document.filename,
            "chunk_size": self.chunker.config.chunk_size,
            "chunk_overlap": (
                self.chunker.config.chunk_overlap
            ),
            "chunk_count": len(chunks),
            "chunks": [
                chunk.model_dump(mode="json")
                for chunk in chunks
            ],
        }

        with output_path.open(
            "w",
            encoding="utf-8",
        ) as file:

            json.dump(
                payload,
                file,
                indent=2,
                ensure_ascii=False,
            )

        return output_path