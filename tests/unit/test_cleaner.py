from app.ingestion.cleaner import TextCleaner
from app.models.document import PageDocument


def create_page(
    page_number: int,
    text: str,
) -> PageDocument:
    return PageDocument(
        document_id="doc_test",
        filename="test.pdf",
        page_number=page_number,
        raw_text=text,
        clean_text=text,
        title=None,
        source="test.pdf",
        character_count=len(text),
        metadata={
            "document_id": "doc_test",
            "filename": "test.pdf",
            "page_number": page_number,
            "title": None,
            "source": "test.pdf",
        },
    )


def test_whitespace_normalization():
    cleaner = TextCleaner()

    text = "Hello     world\n\n\n\nThis is a test."

    result = cleaner.clean_text(text)

    assert result == "Hello world\n\nThis is a test."


def test_unicode_normalization():
    cleaner = TextCleaner()

    text = "Machine\u2013Learning"

    result = cleaner.clean_text(text)

    assert result == "Machine-Learning"


def test_zero_width_characters_removed():
    cleaner = TextCleaner()

    text = "Machine\u200bLearning"

    result = cleaner.clean_text(text)

    assert result == "MachineLearning"


def test_empty_text():
    cleaner = TextCleaner()

    assert cleaner.is_empty("") is True
    assert cleaner.is_empty("   \n\t") is True


def test_non_empty_text():
    cleaner = TextCleaner()

    assert cleaner.is_empty("Machine learning") is False


def test_repeated_header_removed():
    cleaner = TextCleaner()

    pages = [
        create_page(
            1,
            "University of Cairo\nIntroduction\nMachine learning..."
        ),
        create_page(
            2,
            "University of Cairo\nModels\nRegression..."
        ),
        create_page(
            3,
            "University of Cairo\nEvaluation\nAccuracy..."
        ),
    ]

    result = cleaner.clean_document(pages)

    for page in result:
        assert "University of Cairo" not in page.clean_text