import hashlib
import json
from pathlib import Path
from typing import Optional

from app.core.config import ensure_directories, settings
from app.core.exceptions import (
    EmptyPDFError,
    PDFSizeLimitError,
)
from app.ingestion.cleaner import TextCleaner
from app.ingestion.loader import PDFLoader
from app.models.document import (
    DocumentMetadata,
    ProcessedDocument,
)


class DocumentIngestionPipeline:
    """
    End-to-end Phase 1 document ingestion pipeline.
    """

    def __init__(
        self,
        cleaner: Optional[TextCleaner] = None,
    ):
        self.cleaner = cleaner or TextCleaner()

        ensure_directories()

    def process(
        self,
        file_path: Path,
    ) -> ProcessedDocument:
        """
        Process one PDF document.

        Pipeline:

            PDF
             ↓
            validate
             ↓
            extract
             ↓
            clean
             ↓
            metadata
             ↓
            ProcessedDocument
        """

        file_path = Path(file_path)

        self._validate_file(file_path)

        document_id = self._generate_document_id(file_path)

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
            if not self.cleaner.is_empty(page.clean_text)
        ]

        if not meaningful_pages:
            raise EmptyPDFError(
                f"No meaningful text could be extracted from: "
                f"{file_path.name}"
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

        # Add title to page metadata.
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
            extracted_character_count=extracted_character_count,
            cleaned_character_count=cleaned_character_count,
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

    def _validate_file(self, file_path: Path) -> None:
        """
        Validate the input PDF.
        """

        if not file_path.exists():
            raise FileNotFoundError(
                f"File does not exist: {file_path}"
            )

        if not file_path.is_file():
            raise ValueError(
                f"Input path is not a file: {file_path}"
            )

        if file_path.suffix.lower() != ".pdf":
            raise ValueError(
                "Only PDF files are supported."
            )

        file_size = file_path.stat().st_size

        if file_size > settings.max_pdf_size_bytes:
            raise PDFSizeLimitError(
                f"PDF exceeds maximum allowed size of "
                f"{settings.max_pdf_size_mb} MB."
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
        Generate a deterministic document ID from file contents.

        This means identical files receive the same ID.
        """

        hasher = hashlib.sha256()

        with file_path.open("rb") as file:
            while chunk := file.read(1024 * 1024):
                hasher.update(chunk)

        return f"doc_{hasher.hexdigest()[:16]}"

    def _extract_title(
        self,
        file_path: Path,
        pages,
    ) -> Optional[str]:
        """
        Attempt to determine a simple document title.

        Current strategy:
        1. Use PDF filename.
        2. If first page has a short first line, prefer it.

        This is intentionally simple for Phase 1.
        """

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
        """
        Save processed document as JSON.

        JSON is useful during development because it lets us
        inspect exactly what the pipeline produced.

        Later, this can be replaced or complemented by a database.
        """

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