from __future__ import annotations

from app.models.generation import ContextChunk
from app.models.hybrid import HybridSearchResult


class ContextBuilder:
    """
    Converts hybrid retrieval results into the context representation
    consumed by the LLM.

    The fused retrieval score is used as the primary relevance score.
    """

    def __init__(
        self,
        max_chars: int = 12000,
    ) -> None:

        if max_chars <= 0:
            raise ValueError(
                "max_chars must be greater than zero."
            )

        self.max_chars = max_chars

    def build(
        self,
        results: list[HybridSearchResult],
    ) -> list[ContextChunk]:

        if not results:
            return []

        context: list[ContextChunk] = []

        current_chars = 0

        for index, result in enumerate(
            results,
            start=1,
        ):
            citation_id = f"C{index}"

            estimated_size = (
                len(result.text)
                + len(citation_id)
                + 100
            )

            if (
                current_chars + estimated_size
                > self.max_chars
            ):
                break

            context.append(
                ContextChunk(
                    citation_id=citation_id,
                    chunk_id=result.chunk_id,
                    document_id=result.document_id,
                    filename=result.filename,
                    page_number=result.page_number,
                    text=result.text,
                    score=result.fused_score,
                    title=result.title,
                    source=result.source,
                )
            )

            current_chars += estimated_size

        return context

    @staticmethod
    def format_for_llm(
        context: list[ContextChunk],
    ) -> str:

        if not context:
            return (
                "No supporting context was retrieved."
            )

        sections: list[str] = []

        for chunk in context:

            sections.append(
                (
                    f"[{chunk.citation_id}]\n"
                    f"Document: {chunk.filename}\n"
                    f"Page: {chunk.page_number}\n"
                    f"Source: {chunk.source}\n"
                    f"Content:\n{chunk.text}"
                )
            )

        return "\n\n".join(sections)