from typing import Any, Dict, Optional
import openai
from anthropic import Anthropic
from ..config.settings import OPENAI_API_KEY, ANTHROPIC_API_KEY, DEFAULT_MODEL
from ..utils.retry import retry_with_backoff
from ..utils.cost_monitor import CostMonitor
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

class AIClient:
    """Wrapper for OpenAI and Anthropic APIs."""

    def __init__(self, cost_monitor: Optional[CostMonitor] = None):
        self.openai_client = openai.AsyncOpenAI(api_key=OPENAI_API_KEY) if OPENAI_API_KEY else None
        self.anthropic_client = Anthropic(api_key=ANTHROPIC_API_KEY) if ANTHROPIC_API_KEY else None
        self.cost_monitor = cost_monitor or CostMonitor()

    @retry_with_backoff()
    async def generate(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        model: str = DEFAULT_MODEL,
        **kwargs: Any
    ) -> str:
        """Generates completion using the specified model."""
        if model.startswith("gpt"):
            return await self._generate_openai(prompt, system_prompt, model, **kwargs)
        elif model.startswith("claude"):
            return await self._generate_anthropic(prompt, system_prompt, model, **kwargs)
        else:
            raise ValueError(f"Unsupported model: {model}")

    async def _generate_openai(self, prompt: str, system_prompt: str, model: str, **kwargs: Any) -> str:
        if not self.openai_client:
            raise ValueError("OpenAI API key not configured")
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})

        response = await self.openai_client.chat.completions.create(
            model=model,
            messages=messages,
            **kwargs
        )
        
        content = response.choices[0].message.content
        if self.cost_monitor:
            self.cost_monitor.track(
                model=model,
                prompt_tokens=response.usage.prompt_tokens,
                completion_tokens=response.usage.completion_tokens
            )
        return content

    async def _generate_anthropic(self, prompt: str, system_prompt: str, model: str, **kwargs: Any) -> str:
        if not self.anthropic_client:
            raise ValueError("Anthropic API key not configured")
        
        response = self.anthropic_client.messages.create(
            model=model,
            max_tokens=kwargs.get("max_tokens", 1024),
            system=system_prompt,
            messages=[{"role": "user", "content": prompt}]
        )
        
        content = response.content[0].text
        if self.cost_monitor:
            self.cost_monitor.track(
                model=model,
                prompt_tokens=response.usage.input_tokens,
                completion_tokens=response.usage.output_tokens
            )
        return content
