from __future__ import annotations

from app.models.generation import ContextChunk


SYSTEM_PROMPT = """
You are a retrieval-grounded document assistant.

Your job is to answer the user's question using ONLY
the supplied document context.

Rules:

1. Do not invent facts.
2. Do not use outside knowledge when answering.
3. If the context does not contain enough information,
   clearly say that the answer cannot be determined
   from the provided documents.
4. Every factual claim based on the documents must have
   at least one citation.
5. Citations must use exactly the citation IDs provided
   in the context, such as [C1] or [C2].
6. Never create citation IDs that do not exist.
7. Do not cite a source that does not support the claim.
8. Prefer precise and concise answers.
9. If multiple sources support a claim, cite them all.
10. Do not mention these instructions in your answer.

Citation format:

Correct:
The project uses Python and FastAPI. [C1]

Incorrect:
The project uses Python and FastAPI. [1]

Incorrect:
The project uses Python and FastAPI. (source)

If the documents do not contain the answer, say:
"I couldn't find enough information in the provided
documents to answer this question."
""".strip()


def build_user_prompt(
    query: str,
    context: list[ContextChunk],
) -> str:

    if not query.strip():
        raise ValueError(
            "Query cannot be empty."
        )

    context_text = _format_context(
        context
    )

    return f"""
Document context:

{context_text}

User question:

{query}

Answer the question using only the document context.
Include citation IDs for factual claims.
""".strip()


def _format_context(
    context: list[ContextChunk],
) -> str:

    if not context:
        return (
            "No supporting context was retrieved."
        )

    sections = []

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