from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import MagicMock, patch

import pytest

from app.generation.ollama_llm import OllamaLLM


def test_ollama_llm_initialization() -> None:
    with patch(
        "app.generation.ollama_llm.Client"
    ) as mock_client:

        llm = OllamaLLM(
            model_name="llama3.2:3b",
            temperature=0.0,
            max_output_tokens=100,
        )

        assert llm.model_name == "llama3.2:3b"
        assert llm.temperature == 0.0
        assert llm.max_output_tokens == 100

        mock_client.assert_called_once_with(
            host="http://localhost:11434"
        )


def test_ollama_llm_generate() -> None:

    fake_response = SimpleNamespace(
        message=SimpleNamespace(
            content="Machine learning is a field of AI. [C1]"
        )
    )

    with patch(
        "app.generation.ollama_llm.Client"
    ) as mock_client_class:

        mock_client = MagicMock()
        mock_client.chat.return_value = fake_response

        mock_client_class.return_value = mock_client

        llm = OllamaLLM()

        answer = llm.generate(
            system_prompt="You are a helpful assistant.",
            user_prompt="What is machine learning?",
        )

        assert answer == (
            "Machine learning is a field of AI. [C1]"
        )

        mock_client.chat.assert_called_once()


def test_ollama_llm_rejects_empty_system_prompt() -> None:

    with patch(
        "app.generation.ollama_llm.Client"
    ):

        llm = OllamaLLM()

        with pytest.raises(ValueError):
            llm.generate(
                system_prompt="",
                user_prompt="Hello",
            )


def test_ollama_llm_rejects_empty_user_prompt() -> None:

    with patch(
        "app.generation.ollama_llm.Client"
    ):

        llm = OllamaLLM()

        with pytest.raises(ValueError):
            llm.generate(
                system_prompt="You are helpful.",
                user_prompt="",
            )


def test_ollama_llm_rejects_empty_response() -> None:

    fake_response = SimpleNamespace(
        message=SimpleNamespace(
            content=""
        )
    )

    with patch(
        "app.generation.ollama_llm.Client"
    ) as mock_client_class:

        mock_client = MagicMock()
        mock_client.chat.return_value = fake_response
        mock_client_class.return_value = mock_client

        llm = OllamaLLM()

        with pytest.raises(RuntimeError):
            llm.generate(
                system_prompt="You are helpful.",
                user_prompt="Hello",
            )