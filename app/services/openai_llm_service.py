"""OpenAI LLM service implementation conforming to the LLMService Protocol."""

from __future__ import annotations

import json
from typing import Any

from app.services.llm_service import LLMServiceError, LLMInvalidJSONError


class OpenAILLMService:
    """OpenAI-backed LLM service implementing the LLMService Protocol."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        from app.config import OPENAI_API_KEY, OPENAI_LLM_MODEL

        self._api_key = api_key if api_key is not None else OPENAI_API_KEY
        self._model = model if model is not None else OPENAI_LLM_MODEL

    def generate_text(self, prompt: str) -> str:
        """Call OpenAI chat completions and return the assistant reply."""

        try:
            import openai
        except ImportError as exc:
            raise LLMServiceError(
                "pip install 'foundergraph-lab[graphrag]' to use the OpenAI backend"
            ) from exc

        response = openai.OpenAI(api_key=self._api_key).chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
        )
        return response.choices[0].message.content.strip()

    def generate_json(self, prompt: str) -> Any:
        """Call OpenAI with JSON mode enforced and parse the response."""

        try:
            import openai
        except ImportError as exc:
            raise LLMServiceError(
                "pip install 'foundergraph-lab[graphrag]' to use the OpenAI backend"
            ) from exc

        response = openai.OpenAI(api_key=self._api_key).chat.completions.create(
            model=self._model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000,
            response_format={"type": "json_object"},
        )
        result = response.choices[0].message.content.strip()
        try:
            return json.loads(result)
        except json.JSONDecodeError as exc:
            raise LLMInvalidJSONError("OpenAI response was not valid JSON") from exc
