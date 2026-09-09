from __future__ import annotations

from app.generation.citations import (
    build_citations,
    extract_citation_ids,
    validate_citations,
)
from app.generation.context import ContextBuilder
from app.generation.llm import LLM
from app.generation.prompts import (
    SYSTEM_PROMPT,
    build_user_prompt,
)
from app.models.generation import RAGResponse
from app.models.hybrid import HybridSearchResult


class AnswerGenerator:

    def __init__(
        self,
        llm: LLM,
        context_builder: ContextBuilder,
        require_citations: bool = True,
    ) -> None:

        self.llm = llm
        self.context_builder = context_builder
        self.require_citations = require_citations

    def answer(
        self,
        query: str,
        results: list[HybridSearchResult],
    ) -> RAGResponse:

        if not isinstance(query, str):
            raise TypeError(
                "Query must be a string."
            )

        if not query.strip():
            raise ValueError(
                "Query cannot be empty."
            )

        context = self.context_builder.build(
            results
        )

        if not context:

            return RAGResponse(
                query=query,
                answer=(
                    "I couldn't find enough information "
                    "in the provided documents to answer "
                    "this question."
                ),
                citations=[],
                model=self.llm.model_name,
                grounded=False,
                citation_ids=[],
            )

        user_prompt = build_user_prompt(
            query=query,
            context=context,
        )

        answer = self.llm.generate(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=user_prompt,
        )

        citation_ids = extract_citation_ids(
            answer
        )

        grounded = validate_citations(
            answer=answer,
            context=context,
            require_citations=(
                self.require_citations
            ),
        )

        citations = build_citations(
            citation_ids=citation_ids,
            context=context,
        )

        return RAGResponse(
            query=query,
            answer=answer,
            citations=citations,
            model=self.llm.model_name,
            grounded=grounded,
            citation_ids=citation_ids,
        )