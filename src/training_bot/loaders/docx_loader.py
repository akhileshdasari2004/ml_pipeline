from docx import Document
from typing import List, Any
from ..models.document import SourceDocument
from pathlib import Path
from .base import BaseLoader
from ..config.constants import SourceType
from ..utils.errors import LoadError
from ..utils.logging import setup_logging

logger = setup_logging(__name__)

class DocxLoader(BaseLoader):
    """Loads text from Word documents."""

    @property
    def source_type(self) -> SourceType:
        return SourceType.DOCX

    async def load(self, file_path: str, **kwargs: Any) -> List[SourceDocument]:
        logger.info(f"Loading DOCX from {file_path}")
        path = Path(file_path)
        try:
            doc = Document(path)
            content = "\n".join([para.text for para in doc.paragraphs])
            return [self._create_document(
                content=content,
                title=path.name,
                id_prefix="docx",
                metadata={"file_path": str(path)}
            )]
        except Exception as e:
            logger.error(f"Failed to load DOCX {file_path}: {e}")
            raise LoadError(f"DOCX load failed: {e}")
