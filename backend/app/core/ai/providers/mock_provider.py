"""Deterministic Mock AI Provider for offline testing and fallback execution."""

import json

from app.core.ai.base_provider import BaseAIProvider


class MockAIProvider(BaseAIProvider):
    """Fallback offline AI provider generating deterministic summaries and recommendations."""

    @property
    def provider_name(self) -> str:
        return "MockAIProvider"

    def generate(self, prompt: str, system_prompt: str = "") -> str:
        """Generate deterministic structured response based on prompt context."""
        prompt_lower = prompt.lower()

        if "executive summary" in prompt_lower:
            return (
                "Executive Summary: The repository demonstrates solid architectural foundation, "
                "with clear modularity and structured code practices. Minor technical debt exists "
                "in security and documentation which should be addressed prior to enterprise deployment."
            )
        elif "technical summary" in prompt_lower:
            return (
                "Technical Summary: Static code analysis indicates high maintainability with acceptable "
                "cyclomatic complexity. The dependency graph shows clean separation of concerns with minimal circular imports."
            )
        elif "roadmap" in prompt_lower or "recommendation" in prompt_lower:
            return json.dumps(
                [
                    {
                        "category": "Security",
                        "title": "Remediate Hardcoded Secrets",
                        "description": "Move hardcoded credentials into environment variables or vault secret managers.",
                        "timeframe": "Immediate",
                        "priority": "Critical",
                        "difficulty": "Easy",
                        "estimated_hours": 4,
                    },
                    {
                        "category": "Testing",
                        "title": "Increase Unit Test Coverage",
                        "description": "Add integration test cases for API endpoints and database transaction boundaries.",
                        "timeframe": "Short-term",
                        "priority": "High",
                        "difficulty": "Medium",
                        "estimated_hours": 16,
                    },
                ]
            )
        else:
            return f"Deterministic AI Summary based on analysis metrics:\n{prompt[:300]}..."
