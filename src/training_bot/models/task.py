from typing import Dict, Any, Optional
from pydantic import BaseModel, Field
from ..config.constants import TaskType

class TaskTemplate(BaseModel):
    """Configuration for a specific data generation task."""
    task_type: TaskType
    prompt_template: str
    ai_params: Dict[str, Any] = Field(default_factory=lambda: {"temperature": 0.7, "max_tokens": 1000})
    system_prompt: Optional[str] = None
    examples: Optional[str] = None
