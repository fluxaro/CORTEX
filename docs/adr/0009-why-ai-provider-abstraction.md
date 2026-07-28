# ADR 0009: Why AI Provider Abstraction

## Status
Accepted

## Context
AI language model APIs are expensive, subject to rate limits, and change rapidly. Hardcoding a dependency on any single provider (e.g., OpenAI) would make the system brittle and block offline development and testing.

## Decision
Implement an **AI Provider Abstraction** (`AIProviderFactory`) that returns a concrete provider instance based on the `AI_PROVIDER` environment variable.

## Interface

```python
class BaseAIProvider(ABC):
    @abstractmethod
    async def generate(self, prompt: str, context: dict) -> str:
        """Generate AI text from a structured prompt and context."""
        ...
```

## Supported Providers
| Provider | `AI_PROVIDER` value | Notes |
| :--- | :--- | :--- |
| OpenAI GPT-4o | `openai` | Requires `OPENAI_API_KEY` |
| Anthropic Claude 3.5 | `anthropic` | Requires `ANTHROPIC_API_KEY` |
| Google Gemini | `gemini` | Requires `GEMINI_API_KEY` |
| Azure OpenAI | `azure` | Requires Azure endpoint |
| Ollama (local LLM) | `ollama` | Fully offline |
| MockProvider | `mock` | Deterministic, no API key needed |

## Critical Design Constraint
**The AI layer must NEVER read raw source code.** All AI prompts are constructed exclusively from structured metrics already stored in PostgreSQL (scores, counts, finding names, file paths). This ensures:
1. No sensitive source code leaks to external AI APIs.
2. AI outputs are fully reproducible from database state alone.
3. The system is functional without any AI key (MockProvider).

## Consequences
- All AI-generated content is labelled as AI-generated in the UI and database.
- MockProvider enables the full test suite to run without any external API calls.
