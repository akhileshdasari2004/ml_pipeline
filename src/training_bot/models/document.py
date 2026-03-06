from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel, Field
from ..config.constants import SourceType

class SourceDocument(BaseModel):
    """Represents a raw source document."""
    id: str
    title: str
    content: str
    source_type: SourceType
    source_url: Optional[str] = None
    word_count: int = 0
    metadata: Dict[str, Any] = Field(default_factory=dict)
    created_at: datetime = Field(default_factory=datetime.now)

    def __init__(self, **data: Any):
        if "word_count" not in data and "content" in data:
            data["word_count"] = len(data["content"].split())
        super().__init__(**data)
