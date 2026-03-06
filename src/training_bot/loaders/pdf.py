from typing import List, Any
from ..models.document import SourceDocument
from pathlib import Path
import PyPDF2
from .base import BaseLoader
from ..config.constants import SourceType
from ..utils.errors import LoadError
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

class PDFLoader(BaseLoader):
    """Loads text from PDF files."""

    @property
    def source_type(self) -> SourceType:
        return SourceType.PDF

    async def load(self, file_path: str, **kwargs: Any) -> List[SourceDocument]:
        logger.info(f"Loading PDF from {file_path}")
        path = Path(file_path)
        if not path.exists():
            raise LoadError(f"File not found: {file_path}")

        try:
            with open(path, "rb") as f:
                reader = PyPDF2.PdfReader(f)
                content = ""
                for page in reader.pages:
                    content += page.extract_text() + "\n"
                
                return [self._create_document(
                    content=content,
                    title=path.name,
                    id_prefix="pdf",
                    metadata={"file_path": str(path), "page_count": len(reader.pages)}
                )]
        except Exception as e:
            logger.error(f"Failed to load PDF {file_path}: {e}")
            raise LoadError(f"PDF load failed: {e}")
