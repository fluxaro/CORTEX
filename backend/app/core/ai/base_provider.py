"""Abstract base interface for AI Providers."""

from abc import ABC, abstractmethod


class BaseAIProvider(ABC):
    """Abstract base class for LLM AI providers (OpenAI, Gemini, Anthropic, Ollama, Mock)."""

    @property
    @abstractmethod
    def provider_name(self) -> str:
        """Name of AI provider."""
        pass

    @abstractmethod
    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate text completion from prompt."""
        pass
