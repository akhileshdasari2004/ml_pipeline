from typing import Optional, List
from pydantic import BaseModel, Field

class TextChunk(BaseModel):
    """Represents a chunk of text from a source document."""
    document_id: str
    chunk_id: str
    text: str
    index: int
    start_idx: int
    end_idx: int
    prev_context: Optional[str] = None
    next_context: Optional[str] = None
    metadata: dict = Field(default_factory=dict)
