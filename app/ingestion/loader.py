from pathlib import Path
from typing import List

import fitz

from app.core.exceptions import (
    EmptyPDFError,
    InvalidPDFError,
    PDFExtractionError,
)
from app.models.document import PageDocument


class PDFLoader:
    """
    Loads a PDF and extracts text page-by-page.
    """

    def __init__(self, document_id: str, source: str):
        self.document_id = document_id
        self.source = source

    def load(self, file_path: Path) -> List[PageDocument]:
        """
        Extract text from every page in a PDF.

        Returns:
            List[PageDocument]
        """

        if not file_path.exists():
            raise FileNotFoundError(
                f"PDF file does not exist: {file_path}"
            )

        if not file_path.is_file():
            raise InvalidPDFError(
                f"Path is not a file: {file_path}"
            )

        if file_path.suffix.lower() != ".pdf":
            raise InvalidPDFError(
                f"Expected a PDF file, received: {file_path.suffix}"
            )

        try:
            pdf = fitz.open(file_path)
        except Exception as exc:
            raise InvalidPDFError(
                f"Unable to open PDF: {file_path}"
            ) from exc

        try:
            if pdf.page_count == 0:
                raise EmptyPDFError(
                    f"PDF contains no pages: {file_path}"
                )

            pages = []

            for page_index in range(pdf.page_count):
                page = pdf.load_page(page_index)

                text = page.get_text("text")

                page_document = PageDocument(
                    document_id=self.document_id,
                    filename=file_path.name,
                    page_number=page_index + 1,
                    raw_text=text,
                    clean_text=text,
                    title=None,
                    source=self.source,
                    character_count=len(text),
                    metadata={
                        "document_id": self.document_id,
                        "filename": file_path.name,
                        "page_number": page_index + 1,
                        "title": None,
                        "source": self.source,
                    },
                )

                pages.append(page_document)

            return pages

        except EmptyPDFError:
            raise

        except Exception as exc:
            raise PDFExtractionError(
                f"Failed to extract text from PDF: {file_path}"
            ) from exc

        finally:
            pdf.close()