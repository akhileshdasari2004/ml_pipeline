from typing import Any, Dict, Optional
from .client import AIClient

class SimulationClient(AIClient):
    """Mock AI responses for development and testing."""

    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = "mock-model",
        **kwargs: Any
    ) -> str:
        """Returns a simulated AI response."""
        return f"[MOCK RESPONSE for model {model}]\nResponse to: {prompt[:50]}..."
