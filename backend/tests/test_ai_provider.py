"""Tests for AI Provider Abstraction and Factory."""

from app.core.ai.factory import AIProviderFactory
from app.core.ai.providers.mock_provider import MockAIProvider


def test_ai_provider_factory() -> None:
    """Test instantiating AI provider via factory."""
    provider = AIProviderFactory.get_provider("mock")
    assert isinstance(provider, MockAIProvider)
    assert provider.provider_name == "MockAIProvider"

    res = provider.generate("Generate an Executive Summary for repository ProjectIQ.")
    assert "Executive Summary" in res
