from __future__ import annotations

from app.generation.prompts import (
    SYSTEM_PROMPT,
    build_user_prompt,
)
from app.models.generation import ContextChunk


def test_system_prompt_contains_grounding_rules() -> None:

    assert "ONLY" in SYSTEM_PROMPT
    assert "citation" in SYSTEM_PROMPT.lower()
    assert "[C1]" in SYSTEM_PROMPT


def test_user_prompt_contains_context() -> None:

    context = [
        ContextChunk(
            citation_id="C1",
            chunk_id="chunk_1",
            document_id="doc_1",
            filename="test.pdf",
            page_number=2,
            text="Machine learning project.",
            score=0.9,
            title=None,
            source="test.pdf",
        )
    ]

    prompt = build_user_prompt(
        query="What project uses machine learning?",
        context=context,
    )

    assert "C1" in prompt
    assert "Machine learning project." in prompt
    assert (
        "What project uses machine learning?"
        in prompt
    )