from __future__ import annotations

import pytest

from app.generation.factory import create_llm


@pytest.mark.integration
def test_real_ollama_generation() -> None:

    llm = create_llm(
        provider="ollama",
        model_name="llama3.2:3b",
        temperature=0.0,
        max_output_tokens=100,
        host="http://localhost:11434",
    )

    answer = llm.generate(
        system_prompt=(
            "You are a helpful assistant. "
            "Answer concisely."
        ),
        user_prompt="What is machine learning?",
    )

    assert answer
    assert isinstance(answer, str)