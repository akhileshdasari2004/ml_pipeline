from typing import List, Dict, Any, Type, Optional
from ..models.document import SourceDocument
from .base import BaseLoader
from .web import WebLoader
from .pdf import PDFLoader
from .markdown import MarkdownLoader
from .csv_loader import CSVLoader
from .docx_loader import DocxLoader
from ..config.constants import SourceType
from ..utils.errors import LoadError
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

class UnifiedLoader:
    """Orchestrates loading from various sources."""

    def __init__(self):
        self._loaders: Dict[SourceType, BaseLoader] = {
            SourceType.WEB: WebLoader(),
            SourceType.PDF: PDFLoader(),
            SourceType.MARKDOWN: MarkdownLoader(),
            SourceType.CSV: CSVLoader(),
            SourceType.DOCX: DocxLoader(),
        }

    def register_loader(self, source_type: SourceType, loader: BaseLoader):
        self._loaders[source_type] = loader

    async def load(self, source: str, source_type: Optional[SourceType] = None, **kwargs: Any) -> List[SourceDocument]:
        if not source_type:
            source_type = self._detect_source_type(source)
        
        loader = self._loaders.get(source_type)
        if not loader:
            raise LoadError(f"No loader registered for source type: {source_type}")
        
        return await loader.load(source, **kwargs)

    def _detect_source_type(self, source: str) -> SourceType:
        if source.startswith(("http://", "https://")):
            return SourceType.WEB
        
        lower_source = source.lower()
        if lower_source.endswith(".pdf"):
            return SourceType.PDF
        if lower_source.endswith((".md", ".markdown")):
            return SourceType.MARKDOWN
        if lower_source.endswith(".csv"):
            return SourceType.CSV
        if lower_source.endswith(".docx"):
            return SourceType.DOCX
        
        raise LoadError(f"Could not auto-detect source type for: {source}")
