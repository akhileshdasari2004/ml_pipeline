from typing import List, Optional
from ..models.chunk import TextChunk
from ..models.document import SourceDocument
from ..config.settings import CHUNK_SIZE, CHUNK_OVERLAP

class SmartChunker:
    """Splits text into overlapping chunks."""

    def __init__(self, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP):
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

    def chunk(self, doc: SourceDocument) -> List[TextChunk]:
        """Chunks a document into smaller pieces."""
        text = doc.content
        chunks = []
        
        # Simple character-based chunking for now (could be token-based)
        start = 0
        idx = 0
        while start < len(text):
            end = min(start + self.chunk_size, len(text))
            
            # Find a good break point (newline or space) near the end
            if end < len(text):
                last_space = text.rfind(" ", start, end)
                if last_space != -1 and last_space > start + (self.chunk_size * 0.7):
                    end = last_space

            chunk_text = text[start:end].strip()
            
            # Context windowing
            prev_context = text[max(0, start - 200):start] if start > 0 else None
            next_context = text[end:min(len(text), end + 200)] if end < len(text) else None

            chunks.append(TextChunk(
                document_id=doc.id,
                chunk_id=f"{doc.id}_ch_{idx}",
                text=chunk_text,
                index=idx,
                start_idx=start,
                end_idx=end,
                prev_context=prev_context,
                next_context=next_context
            ))

            start = end - self.chunk_overlap
            if start >= len(text) - self.chunk_overlap:
                break
            idx += 1

        return chunks
