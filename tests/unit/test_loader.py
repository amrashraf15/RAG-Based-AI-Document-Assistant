from pathlib import Path

import fitz
import pytest

from app.core.exceptions import InvalidPDFError
from app.ingestion.loader import PDFLoader


def create_test_pdf(path: Path):
    document = fitz.open()

    page = document.new_page()

    page.insert_text(
        (72, 72),
        "Machine learning is a field of artificial intelligence.",
    )

    document.save(path)
    document.close()


def test_pdf_loader_extracts_pages(tmp_path):
    pdf_path = tmp_path / "test.pdf"

    create_test_pdf(pdf_path)

    loader = PDFLoader(
        document_id="doc_test",
        source=str(pdf_path),
    )

    pages = loader.load(pdf_path)

    assert len(pages) == 1

    assert pages[0].document_id == "doc_test"
    assert pages[0].filename == "test.pdf"
    assert pages[0].page_number == 1

    assert "Machine learning" in pages[0].raw_text


def test_pdf_loader_rejects_non_pdf(tmp_path):
    file_path = tmp_path / "test.txt"

    file_path.write_text(
        "This is not a PDF.",
        encoding="utf-8",
    )

    loader = PDFLoader(
        document_id="doc_test",
        source=str(file_path),
    )

    with pytest.raises(InvalidPDFError):
        loader.load(file_path)