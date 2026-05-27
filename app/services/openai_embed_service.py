"""OpenAI embedding service for FounderGraph-Lab."""

from __future__ import annotations

from app.services.llm_service import LLMServiceError


class OpenAIEmbedService:
    """Embedding service backed by the OpenAI embeddings API."""

    def __init__(self, api_key: str | None = None, model: str | None = None) -> None:
        from app.config import OPENAI_API_KEY, OPENAI_EMBED_MODEL

        self._api_key = api_key if api_key is not None else OPENAI_API_KEY
        self._model = model if model is not None else OPENAI_EMBED_MODEL

    def embed(self, text: str) -> list[float]:
        """Return the embedding vector for *text* from the OpenAI embeddings API."""

        try:
            import openai
        except ImportError as exc:
            raise LLMServiceError(
                "pip install 'foundergraph-lab[graphrag]' to use the OpenAI backend"
            ) from exc

        response = openai.OpenAI(api_key=self._api_key).embeddings.create(
            model=self._model,
            input=text,
        )
        return response.data[0].embedding

    def __call__(self, text: str) -> list[float]:
        """Allow the instance to be used directly as an embed_fn callable."""

        return self.embed(text)
