from __future__ import annotations

from app.generation.context import ContextBuilder
from app.models.hybrid import HybridSearchResult


def make_result(
    chunk_id: str,
    text: str,
) -> HybridSearchResult:

    return HybridSearchResult(
        chunk_id=chunk_id,
        document_id="doc_test",
        filename="test.pdf",
        page_number=1,
        chunk_index=0,
        text=text,
        dense_score=0.9,
        lexical_score=4.2,
        fused_score=0.0164,
        title="Test",
        source="test.pdf",
        token_count=10,
        character_count=len(text),
        embedding_model="fake",
        embedding_dimension=3,
        normalized=True,
    )


def test_context_building() -> None:

    builder = ContextBuilder(
        max_chars=5000
    )

    context = builder.build(
        [
            make_result(
                "chunk_1",
                "Machine learning.",
            ),
            make_result(
                "chunk_2",
                "Web development.",
            ),
        ]
    )

    assert len(context) == 2

    assert (
        context[0].citation_id
        == "C1"
    )

    assert (
        context[1].citation_id
        == "C2"
    )

    assert (
        context[0].score
        == 0.0164
    )


def test_context_respects_limit() -> None:

    builder = ContextBuilder(
        max_chars=150
    )

    context = builder.build(
        [
            make_result(
                "chunk_1",
                "A" * 100,
            ),
            make_result(
                "chunk_2",
                "B" * 100,
            ),
        ]
    )

    assert len(context) <= 1


def test_format_context() -> None:

    builder = ContextBuilder()

    context = builder.build(
        [
            make_result(
                "chunk_1",
                "Machine learning.",
            )
        ]
    )

    formatted = builder.format_for_llm(
        context
    )

    assert "[C1]" in formatted
    assert "Machine learning." in formatted
    assert "test.pdf" in formatted