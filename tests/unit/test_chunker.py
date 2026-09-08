from app.ingestion.chunker import (
    ChunkingConfig,
    RecursiveTextChunker,
    Tokenizer,
)
from app.models.document import (
    DocumentMetadata,
    PageDocument,
    PageMetadata,
    ProcessedDocument,
)


def create_test_document(
    text: str,
) -> ProcessedDocument:

    page = PageDocument(
        document_id="doc_test",
        filename="test.pdf",
        page_number=1,
        raw_text=text,
        clean_text=text,
        title="Test Document",
        source="test.pdf",
        character_count=len(text),
        metadata=PageMetadata(
            document_id="doc_test",
            filename="test.pdf",
            page_number=1,
            title="Test Document",
            source="test.pdf",
        ),
    )

    return ProcessedDocument(
        document_id="doc_test",
        filename="test.pdf",
        source="test.pdf",
        title="Test Document",
        pages=[page],
        metadata=DocumentMetadata(
            document_id="doc_test",
            filename="test.pdf",
            source="test.pdf",
            title="Test Document",
            page_count=1,
            extracted_character_count=len(text),
            cleaned_character_count=len(text),
        ),
    )


def test_chunking_small_document():
    config = ChunkingConfig(
        chunk_size=100,
        chunk_overlap=20,
    )

    chunker = RecursiveTextChunker(
        config=config
    )

    document = create_test_document(
        "Machine learning is a field of artificial intelligence."
    )

    chunks = chunker.chunk_document(
        document
    )

    assert len(chunks) == 1

    assert (
        "Machine learning"
        in chunks[0].text
    )


def test_large_document_creates_multiple_chunks():
    config = ChunkingConfig(
        chunk_size=50,
        chunk_overlap=10,
    )

    chunker = RecursiveTextChunker(
        config=config
    )

    text = (
        "Machine learning is a field of "
        "artificial intelligence. "
        * 100
    )

    document = create_test_document(text)

    chunks = chunker.chunk_document(
        document
    )

    assert len(chunks) > 1


def test_chunk_size_is_respected():
    config = ChunkingConfig(
        chunk_size=50,
        chunk_overlap=10,
    )

    chunker = RecursiveTextChunker(
        config=config
    )

    text = (
        "Machine learning is a field of "
        "artificial intelligence. "
        * 100
    )

    document = create_test_document(text)

    chunks = chunker.chunk_document(
        document
    )

    for chunk in chunks:
        assert (
            chunk.token_count
            <= 50
        )


def test_chunk_metadata():
    chunker = RecursiveTextChunker(
        config=ChunkingConfig(
            chunk_size=100,
            chunk_overlap=20,
        )
    )

    document = create_test_document(
        "Machine learning is useful."
    )

    chunks = chunker.chunk_document(
        document
    )

    chunk = chunks[0]

    assert chunk.document_id == "doc_test"
    assert chunk.filename == "test.pdf"
    assert chunk.page_number == 1
    assert chunk.chunk_index == 0
    assert chunk.chunk_id.startswith(
        "doc_test_chunk_"
    )


def test_invalid_chunk_size():
    try:
        ChunkingConfig(
            chunk_size=0,
            chunk_overlap=0,
        )
        assert False
    except ValueError:
        assert True


def test_invalid_overlap():
    try:
        ChunkingConfig(
            chunk_size=100,
            chunk_overlap=100,
        )
        assert False
    except ValueError:
        assert True