from __future__ import annotations

import pytest

from app.generation.answer import AnswerGenerator
from app.generation.context import ContextBuilder
from app.generation.llm import LLM
from app.models.hybrid import HybridSearchResult


class FakeLLM(LLM):

    def __init__(
        self,
        response: str,
    ) -> None:

        self.response = response

    @property
    def model_name(self) -> str:
        return "fake-model"

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        return self.response


def make_result(
    text: str,
) -> HybridSearchResult:

    return HybridSearchResult(
        chunk_id="chunk_1",
        document_id="doc_test",
        filename="test.pdf",
        page_number=1,
        chunk_index=0,
        text=text,
        dense_score=0.9,
        lexical_score=4.2,
        fused_score=0.0164,
        title=None,
        source="test.pdf",
        token_count=10,
        character_count=len(text),
        embedding_model="fake",
        embedding_dimension=3,
        normalized=True,
    )


def test_grounded_answer() -> None:

    generator = AnswerGenerator(
        llm=FakeLLM(
            "The project uses Python. [C1]"
        ),
        context_builder=ContextBuilder(),
    )

    response = generator.answer(
        query="What language is used?",
        results=[
            make_result(
                "The project uses Python."
            )
        ],
    )

    assert response.grounded

    assert response.answer == (
        "The project uses Python. [C1]"
    )

    assert response.citation_ids == [
        "C1"
    ]

    assert len(response.citations) == 1


def test_ungrounded_answer() -> None:

    generator = AnswerGenerator(
        llm=FakeLLM(
            "The project uses Java. [C99]"
        ),
        context_builder=ContextBuilder(),
    )

    response = generator.answer(
        query="What language is used?",
        results=[
            make_result(
                "The project uses Python."
            )
        ],
    )

    assert not response.grounded


def test_no_context() -> None:

    generator = AnswerGenerator(
        llm=FakeLLM(
            "This should not be used."
        ),
        context_builder=ContextBuilder(),
    )

    response = generator.answer(
        query="Unknown?",
        results=[],
    )

    assert not response.grounded
    assert response.citations == []


def test_empty_query() -> None:

    generator = AnswerGenerator(
        llm=FakeLLM(
            "Answer [C1]"
        ),
        context_builder=ContextBuilder(),
    )

    with pytest.raises(ValueError):

        generator.answer(
            query="",
            results=[],
        )