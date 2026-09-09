from __future__ import annotations

from ollama import Client

from app.generation.llm import LLM


class OllamaLLM(LLM):

    def __init__(
        self,
        model_name: str = "llama3.2:3b",
        temperature: float = 0.0,
        max_output_tokens: int = 1000,
        host: str = "http://localhost:11434",
    ) -> None:

        if not model_name.strip():
            raise ValueError(
                "model_name cannot be empty."
            )

        if not 0 <= temperature <= 2:
            raise ValueError(
                "temperature must be between 0 and 2."
            )

        if max_output_tokens <= 0:
            raise ValueError(
                "max_output_tokens must be greater than zero."
            )

        self._model_name = model_name
        self.temperature = temperature
        self.max_output_tokens = max_output_tokens

        self.client = Client(
            host=host
        )

    @property
    def model_name(self) -> str:
        return self._model_name

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:

        if not system_prompt.strip():
            raise ValueError(
                "system_prompt cannot be empty."
            )

        if not user_prompt.strip():
            raise ValueError(
                "user_prompt cannot be empty."
            )

        response = self.client.chat(
            model=self.model_name,
            messages=[
                {
                    "role": "system",
                    "content": system_prompt,
                },
                {
                    "role": "user",
                    "content": user_prompt,
                },
            ],
            options={
                "temperature": self.temperature,
                "num_predict": self.max_output_tokens,
            },
        )

        answer = response.message.content

        if not answer or not answer.strip():
            raise RuntimeError(
                "LLM returned an empty response."
            )

        return answer.strip()