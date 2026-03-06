from typing import List
from .cleaner import TextCleaner
from .chunker import SmartChunker
from ..models.document import SourceDocument
from ..models.chunk import TextChunk
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

class ProcessingPipeline:
    """Orchestrates the cleaning and chunking flow."""

    def __init__(self):
        self.cleaner = TextCleaner()
        self.chunker = SmartChunker()

    def process(self, documents: List[SourceDocument]) -> List[TextChunk]:
        """Cleans and chunks a list of documents."""
        logger.info(f"Processing {len(documents)} documents")
        all_chunks = []
        
        for doc in documents:
            # 1. Clean
            doc.content = self.cleaner.clean(doc.content)
            doc.word_count = len(doc.content.split())
            
            # 2. Chunk
            chunks = self.chunker.chunk(doc)
            all_chunks.extend(chunks)
            
            logger.info(f"Document {doc.id} processed into {len(chunks)} chunks")
            
        return all_chunks
