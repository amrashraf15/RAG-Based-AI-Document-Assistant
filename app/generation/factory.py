from __future__ import annotations

from app.generation.llm import LLM
from app.generation.ollama_llm import OllamaLLM


def create_llm(
    provider: str = "ollama",
    model_name: str = "llama3.2:3b",
    temperature: float = 0.0,
    max_output_tokens: int = 1000,
    host: str = "http://localhost:11434",
) -> LLM:

    provider = provider.lower().strip()

    if provider == "ollama":
        return OllamaLLM(
            model_name=model_name,
            temperature=temperature,
            max_output_tokens=max_output_tokens,
            host=host,
        )

    raise ValueError(
        f"Unsupported LLM provider: {provider}"
    )