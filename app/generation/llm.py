from __future__ import annotations

from abc import ABC, abstractmethod


class LLM(ABC):

    @property
    @abstractmethod
    def model_name(self) -> str:
        raise NotImplementedError

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
    ) -> str:
        raise NotImplementedError