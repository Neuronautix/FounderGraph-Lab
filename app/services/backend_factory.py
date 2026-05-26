"""Factory that wires the correct LLM and embedding backends based on EXTRACTION_BACKEND."""

from __future__ import annotations

from typing import Callable, Any

from app.config import EXTRACTION_BACKEND


class BackendFactory:
    """All methods are static and read EXTRACTION_BACKEND at call time."""

    @staticmethod
    def backend_name() -> str:
        return EXTRACTION_BACKEND.lower().strip()

    @staticmethod
    def is_graphrag() -> bool:
        return BackendFactory.backend_name() == "graphrag"

    @staticmethod
    def create_llm():
        """Return an LLMService-conformant object for the active backend."""
        if BackendFactory.is_graphrag():
            from app.services.openai_llm_service import OpenAILLMService
            return OpenAILLMService()
        from app.services.llm_service import OllamaLLMService
        return OllamaLLMService()

    @staticmethod
    def create_embed_fn() -> Callable[[str], list[float]]:
        """Return a callable embed_fn for the active backend."""
        if BackendFactory.is_graphrag():
            from app.services.openai_embed_service import OpenAIEmbedService
            return OpenAIEmbedService()
        from app.services.qdrant_service import QdrantService
        return QdrantService().embed

    @staticmethod
    def create_extractor():
        """Return an EntityExtractor wired to the active backend LLM."""
        from app.services.entity_extractor import EntityExtractor
        return EntityExtractor(llm_service=BackendFactory.create_llm())

    @staticmethod
    def create_qdrant_service():
        """Return a QdrantService wired to the active backend embeddings."""
        from app.services.qdrant_service import QdrantService
        if BackendFactory.is_graphrag():
            embed_fn = BackendFactory.create_embed_fn()
            return QdrantService(embed_fn=embed_fn)
        return QdrantService()
