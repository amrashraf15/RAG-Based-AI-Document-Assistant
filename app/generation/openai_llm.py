from __future__ import annotations

from openai import OpenAI

from app.generation.llm import LLM


class OpenAILLM(LLM):

    def __init__(
        self,
        model_name: str = "gpt-5.5",
        api_key: str | None = None,
        temperature: float = 0.0,
        max_output_tokens: int = 1000,
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

        self.client = OpenAI(
            api_key=api_key
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

        response = self.client.responses.create(
            model=self.model_name,
            instructions=system_prompt,
            input=user_prompt,
            max_output_tokens=self.max_output_tokens,
        )

        answer = response.output_text

        if not answer or not answer.strip():
            raise RuntimeError(
                "LLM returned an empty response."
            )

        return answer.strip()