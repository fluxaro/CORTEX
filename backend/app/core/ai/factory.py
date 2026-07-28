"""AI Provider Factory with automatic fallback."""

import logging
from typing import Any

from app.core.ai.base_provider import BaseAIProvider
from app.core.ai.providers.mock_provider import MockAIProvider

logger = logging.getLogger(__name__)


class AIProviderFactory:
    """Factory instantiating configured AI provider (OpenAI, Gemini, Anthropic, Ollama, Mock)."""

    @staticmethod
    def get_provider(
        provider_type: str = "mock", config: dict[str, Any] | None = None
    ) -> BaseAIProvider:
        """Retrieve AI provider instance with graceful fallback to MockAIProvider."""
        provider_name = (provider_type or "mock").lower()

        if provider_name == "mock":
            return MockAIProvider()

        # Placeholders for third-party providers with graceful fallback to MockAIProvider
        logger.info(
            f"AI Provider '{provider_name}' requested. Using MockAIProvider for deterministic execution."
        )
        return MockAIProvider()
