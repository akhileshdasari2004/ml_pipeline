from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List, Any

@dataclass
class TokenUsage:
    """Tracks token usage and estimated costs."""
    prompt_tokens: int = 0
    completion_tokens: int = 0
    total_tokens: int = 0
    estimated_cost: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

class CostMonitor:
    """Monitors and estimates costs for LLM API calls."""
    
    # Simple estimation rates per 1k tokens (Update as per model)
    RATES = {
        "gpt-4": {"prompt": 0.03, "completion": 0.06},
        "gpt-3.5-turbo": {"prompt": 0.0005, "completion": 0.0015},
        "claude-3-opus": {"prompt": 0.015, "completion": 0.075},
        "claude-3-sonnet": {"prompt": 0.003, "completion": 0.015},
    }

    def __init__(self) -> None:
        self.history: List[TokenUsage] = []
        self.total_prompt_tokens = 0
        self.total_completion_tokens = 0
        self.total_cost = 0.0

    def track(self, model: str, prompt_tokens: int, completion_tokens: int) -> TokenUsage:
        rate = self.RATES.get(model, {"prompt": 0.0, "completion": 0.0})
        cost = (prompt_tokens * rate["prompt"] / 1000) + (completion_tokens * rate["completion"] / 1000)
        
        usage = TokenUsage(
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            total_tokens=prompt_tokens + completion_tokens,
            estimated_cost=cost
        )
        
        self.history.append(usage)
        self.total_prompt_tokens += prompt_tokens
        self.total_completion_tokens += completion_tokens
        self.total_cost += cost
        
        return usage

    def get_summary(self) -> Dict[str, Any]:
        return {
            "total_tokens": self.total_prompt_tokens + self.total_completion_tokens,
            "total_prompt_tokens": self.total_prompt_tokens,
            "total_completion_tokens": self.total_completion_tokens,
            "total_estimated_cost": f"${self.total_cost:.4f}",
            "call_count": len(self.history)
        }
