from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel, Field

class TrainingExample(BaseModel):
    """A single training example (input/output pair)."""
    id: str
    document_id: str
    chunk_id: str
    input_text: str
    output_text: str
    quality_score: float = 0.0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)
