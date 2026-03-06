from datetime import datetime
from typing import List, Dict, Any
from pydantic import BaseModel, Field
from .example import TrainingExample

class Dataset(BaseModel):
    """A collection of training examples."""
    id: str
    name: str
    examples: List[TrainingExample] = Field(default_factory=list)
    export_metadata: Dict[str, Any] = Field(default_factory=dict)
    stats: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

    def update_stats(self) -> None:
        self.stats = {
            "count": len(self.examples),
            "avg_quality": sum(e.quality_score for e in self.examples) / len(self.examples) if self.examples else 0,
            "models_used": list(set(e.metadata.get("model", "unknown") for e in self.examples))
        }
